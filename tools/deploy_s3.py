#!/usr/bin/env python3
"""Publish this site to S3 behind CloudFront (article.misbah-inc.com).

    python3 tools/deploy_s3.py --bucket <bucket> --dist <DISTRIBUTION_ID> --dry-run
    python3 tools/deploy_s3.py --bucket <bucket> --dist <DISTRIBUTION_ID>

Same shape as the Library's deploy script, much smaller because this site is ~7 MB of
pages and images. Run it from a local clone (~/Developer/misbah-website), not from Google Drive.

What it does that a bare `aws s3 sync` does not:
  1. Leaves out everything a reader must never get: .git, .claude, tools/, CLAUDE.md, CHANGELOG.md,
     scripts, and the raw logo PNGs at the repo root. (`--delete` means anything already in the bucket
     that matches an exclude is NOT removed — sync hides excluded keys from the delete pass. Remove by hand
     with `aws s3 rm`.)
  2. Cache headers per file type: pages and css/js ten minutes, images a day (filenames are not hashed).
  3. One CloudFront invalidation (`/*`) per deploy. A wildcard is a single path against the free monthly allowance.
  4. Refuses to run from the wrong folder, so a sync --delete cannot wipe the bucket.
"""
import argparse, pathlib, subprocess, sys

EXCLUDE = [".git/*", ".github/*", ".gitignore", ".gitattributes", ".claude/*", "tools/*",
           "*.md", "*.py", "*.sh", "*.PNG", ".DS_Store", "Thumbs.db", "desktop.ini"]
PAGE_CACHE = "public,max-age=600"
IMAGE_CACHE = "public,max-age=86400"
IMAGE_EXT = ["png", "jpg", "jpeg", "gif", "svg", "ico", "webp", "woff2", "woff"]


def run(cmd, dry):
    print("   $ " + " ".join(cmd))
    return 0 if dry else subprocess.call(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket", required=True)
    ap.add_argument("--dist", help="CloudFront distribution id (omit to skip the invalidation)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    for must in ("index.html", "sitemap.xml", "articles/al-kawthar/index.html", "assets/style.css"):
        if not (root / must).exists():
            sys.exit(f"Refusing to deploy: {must} is missing under {root}. Wrong folder? --delete would empty the bucket.")

    dst = f"s3://{a.bucket}"
    sync = ["aws", "s3", "sync", str(root), dst, "--delete", "--cache-control", PAGE_CACHE, "--only-show-errors"]
    for pat in EXCLUDE:
        sync += ["--exclude", pat]
    if a.dry_run:
        sync.append("--dryrun")
    print("== sync")
    if run(sync, False):
        sys.exit("sync failed")

    print("\n== longer cache for images and fonts")
    cp = ["aws", "s3", "cp", dst, dst, "--recursive", "--exclude", "*"]
    for ext in IMAGE_EXT:
        cp += ["--include", f"*.{ext}"]
    cp += ["--cache-control", IMAGE_CACHE, "--metadata-directive", "REPLACE", "--only-show-errors"]
    if a.dry_run:
        print("   (skipped in --dry-run)")
    elif run(cp, False):
        sys.exit("cache-header pass failed")

    if a.dist and not a.dry_run:
        print("\n== invalidate CloudFront")
        run(["aws", "cloudfront", "create-invalidation", "--distribution-id", a.dist, "--paths", "/*"], False)
    print("\ndone" + (" (dry run — nothing changed)" if a.dry_run else ""))


if __name__ == "__main__":
    main()
