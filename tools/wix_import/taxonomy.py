"""Master tag list + per-article tags. Every article has exactly one MONTH (0 = any time of year), one TYPE, and any number of person/topic tags.

The ar/fa/ur names below were written for this site and have NOT been reviewed by a native speaker.
Month assignments for announcements follow the occasion's Hijri date; entries marked (guess) were inferred from the topic.
"""
LANGS = ['en', 'ar', 'fa', 'ur']

MONTHS = {
 'en': ['Muharram', 'Safar', "Rabi' al-Awwal", "Rabi' al-Thani", 'Jumada al-Awwal', 'Jumada al-Thani', 'Rajab', "Sha'ban", 'Ramadan', 'Shawwal', "Dhu al-Qi'dah", 'Dhu al-Hijjah'],
 'ar': ['مُحَرَّم', 'صَفَر', 'رَبِيعُ الأَوَّل', 'رَبِيعُ الآخِر', 'جُمَادَى الأُولَى', 'جُمَادَى الآخِرَة', 'رَجَب', 'شَعْبَان', 'رَمَضَان', 'شَوَّال', 'ذُو القَعْدَة', 'ذُو الحِجَّة'],
 'fa': ['محرم', 'صفر', 'ربیع‌الاول', 'ربیع‌الثانی', 'جمادی‌الاول', 'جمادی‌الثانی', 'رجب', 'شعبان', 'رمضان', 'شوال', 'ذی‌القعده', 'ذی‌الحجه'],
 'ur': ['محرم', 'صفر', 'ربیع الاول', 'ربیع الثانی', 'جمادی الاول', 'جمادی الثانی', 'رجب', 'شعبان', 'رمضان', 'شوال', 'ذیقعدہ', 'ذوالحجہ']}
MONTH_SLUG = ['muharram', 'safar', 'rabi-al-awwal', 'rabi-al-thani', 'jumada-al-awwal', 'jumada-al-thani', 'rajab', 'shaban', 'ramadan', 'shawwal', 'dhu-al-qidah', 'dhu-al-hijjah']
ANY_MONTH = {'en': 'Any time of year', 'ar': 'على مدار العام', 'fa': 'همه‌ی سال', 'ur': 'پورا سال'}

TYPES = {
 'article': {'en': 'Article', 'ar': 'مقالة', 'fa': 'مقاله', 'ur': 'مضمون'},
 'series': {'en': 'Series', 'ar': 'سلسلة', 'fa': 'سلسله', 'ur': 'سلسلہ'},
 'announcement': {'en': 'Shia calendar announcement', 'ar': 'إعلان مناسبة (التقويم الشيعي)', 'fa': 'اعلان مناسبت (تقویم شیعی)', 'ur': 'شیعہ کیلنڈر کا اعلان'},
}

def _t(group, en, ar, fa, ur): return dict(group=group, en=en, ar=ar, fa=fa, ur=ur)

TAGS = {
 # noble figures (the 'person' group)
 'holy-prophet': _t('person', 'The Holy Prophet (p)', 'النبي الأكرم (ص)', 'پیامبر اکرم (ص)', 'نبی اکرم (ص)'),
 'imam-ali': _t('person', 'Imam Ali (p)', 'الإمام علي (ع)', 'امام علی (ع)', 'امام علی (ع)'),
 'lady-fatimah-zahra': _t('person', 'Lady Fatimah al-Zahra (p)', 'السيدة فاطمة الزهراء (ع)', 'حضرت فاطمه زهرا (س)', 'حضرت فاطمہ زہرا (س)'),
 'imam-hasan': _t('person', 'Imam al-Hasan al-Mujtaba (p)', 'الإمام الحسن المجتبى (ع)', 'امام حسن مجتبی (ع)', 'امام حسن مجتبیٰ (ع)'),
 'imam-hussain': _t('person', 'Imam al-Hussain (p)', 'الإمام الحسين (ع)', 'امام حسین (ع)', 'امام حسین (ع)'),
 'imam-sajjad': _t('person', 'Imam al-Sajjad (p)', 'الإمام السجاد (ع)', 'امام سجاد (ع)', 'امام سجاد (ع)'),
 'imam-baqir': _t('person', 'Imam al-Baqir (p)', 'الإمام الباقر (ع)', 'امام باقر (ع)', 'امام باقر (ع)'),
 'imam-sadiq': _t('person', "Imam Ja'far al-Sadiq (p)", 'الإمام جعفر الصادق (ع)', 'امام جعفر صادق (ع)', 'امام جعفر صادق (ع)'),
 'imam-jawad': _t('person', 'Imam al-Jawad (p)', 'الإمام الجواد (ع)', 'امام جواد (ع)', 'امام جواد (ع)'),
 'imam-ridha': _t('person', 'Imam al-Ridha (p)', 'الإمام الرضا (ع)', 'امام رضا (ع)', 'امام رضا (ع)'),
 'imam-askari': _t('person', 'Imam al-Hasan al-Askari (p)', 'الإمام الحسن العسكري (ع)', 'امام حسن عسکری (ع)', 'امام حسن عسکری (ع)'),
 'imam-mahdi': _t('person', 'Imam al-Mahdi (ajtf)', 'الإمام المهدي (عج)', 'امام مهدی (عج)', 'امام مہدی (عج)'),
 'lady-khadijah': _t('person', 'Lady Khadijah (p)', 'السيدة خديجة (ع)', 'حضرت خدیجه (س)', 'حضرت خدیجہ (س)'),
 'lady-masoumah': _t('person', "Lady Fatimah al-Ma'soumah (p)", 'السيدة فاطمة المعصومة (ع)', 'حضرت فاطمه معصومه (س)', 'حضرت فاطمہ معصومہ (س)'),
 'lady-umm-al-banin': _t('person', 'Lady Umm al-Banin (p)', 'السيدة أم البنين (ع)', 'حضرت ام‌البنین (س)', 'حضرت ام البنین (س)'),
 'lady-ruqayyah': _t('person', 'Lady Ruqayyah (p)', 'السيدة رقية (ع)', 'حضرت رقیه (س)', 'حضرت رقیہ (س)'),
 'muhsin-ibn-ali': _t('person', 'Muhsin ibn Ali (p)', 'محسن بن علي (ع)', 'محسن بن علی (ع)', 'محسن بن علی (ع)'),
 'sayyid-abdul-azim': _t('person', 'Sayyid Abdul Azim al-Hasani (p)', 'السيد عبد العظيم الحسني (ع)', 'حضرت عبدالعظیم حسنی (ع)', 'حضرت عبدالعظیم حسنی (ع)'),
 # topics
 'quran': _t('topic', "The Qur'an", 'القرآن الكريم', 'قرآن کریم', 'قرآن کریم'),
 'supplications': _t('topic', 'Supplications & Salawat', 'الأدعية والصلوات', 'دعاها و صلوات', 'دعائیں اور صلوات'),
 'ziyarat': _t('topic', 'Ziyarat & Shrines', 'الزيارة والمراقد', 'زیارت و بارگاه‌ها', 'زیارت اور مزارات'),
 'mourning': _t('topic', 'Mourning & Elegy', 'العزاء والرثاء', 'عزاداری و مرثیه', 'عزاداری اور مرثیہ'),
 'arbaeen': _t('topic', 'Arbaeen', 'الأربعين', 'اربعین', 'اربعین'),
 'wilayah': _t('topic', 'Wilayah', 'الولاية', 'ولایت', 'ولایت'),
 'ghadir': _t('topic', 'Ghadir', 'الغدير', 'غدیر', 'غدیر'),
 'community-service': _t('topic', 'Community service', 'خدمة المجتمع', 'خدمت به جامعه', 'خدمتِ خلق'),
}

# slug -> (month 0-12, type, [tags]).  slug = path under /articles/.
ITEMS = {
 'rabi_al_awwal': (3, 'article', ['lady-khadijah', 'holy-prophet']),
 'al-kawthar': (0, 'series', ['lady-fatimah-zahra', 'quran']),
 'morning-and-evening-mourning': (1, 'series', ['imam-hussain', 'imam-mahdi', 'mourning']),            # (guess) Muharram: the series is built on Ziarat al-Nahiya
 'virtues-of-ziarat-lady-masoumah': (4, 'article', ['lady-masoumah', 'imam-ridha', 'ziyarat']),
 'hadrat-abdul-azim-hasani': (4, 'announcement', ['sayyid-abdul-azim', 'ziyarat']),
 'month-of-rabi-al-akhir': (4, 'announcement', ['lady-masoumah', 'sayyid-abdul-azim']),
 'supplications-of-salawat': (3, 'article', ['holy-prophet', 'supplications']),
 'letter-of-imam-sadiq-to-the-shia': (3, 'article', ['imam-sadiq']),
 'title-al-sadiq': (3, 'article', ['imam-sadiq']),
 'blessed-marriage-khadijah-and-the-prophet': (3, 'article', ['lady-khadijah', 'holy-prophet']),
 'names-of-the-messenger-of-god': (0, 'article', ['holy-prophet', 'quran']),
 'virtues-of-the-messenger-of-allah': (0, 'article', ['holy-prophet', 'imam-ali']),
 'imam-hasan-al-askari-keeper-of-gods-knowledge': (3, 'article', ['imam-askari', 'wilayah']),
 'the-second-ghadir': (3, 'announcement', ['imam-mahdi', 'wilayah', 'ghadir']),
 'rabi-al-awwal': (3, 'announcement', ['holy-prophet']),
 'martyrdom-of-muhsin-ibn-ali': (2, 'article', ['muhsin-ibn-ali', 'lady-fatimah-zahra']),                # (guess) Ayyam-e-Muhsiniyah falls in Safar
 'husn-al-hassan-in-quran': (0, 'article', ['imam-hasan', 'quran']),
 'ayatul-kursi': (0, 'article', ['quran']),
 'recognition-of-arbaeen': (2, 'series', ['imam-hussain', 'arbaeen']),     # two chapters, /articles/recognition-of-arbaeen/1/ and /2/
 'elegy-of-imam-hussains-thirst': (1, 'article', ['imam-hussain', 'mourning']),                           # (guess) posted just before Muharram
 # Shia calendar announcements
 'announcement-muharram-1448': (1, 'announcement', ['imam-hussain', 'mourning']),
 'majlis-7th-dhu-al-hijjah': (12, 'announcement', ['imam-baqir']),
 'majlis-imam-taqi-al-jawad': (11, 'announcement', ['imam-jawad']),
 'majlis-imam-sadiq-25-shawwal': (10, 'announcement', ['imam-sadiq']),
 'majalis-nights-of-qadr': (9, 'announcement', ['imam-ali']),
 'majlis-umm-al-banin': (6, 'announcement', ['lady-umm-al-banin']),
 'martyrdom-of-fatima-al-zahra-2025': (5, 'announcement', ['lady-fatimah-zahra']),                        # (guess) Ayyam-e-Fatimiyya
 'martyrdom-programs-of-fatima-al-zahra': (5, 'announcement', ['lady-fatimah-zahra']),                    # (guess)
 'martyrdom-programs-prophet-hasan-ridha': (2, 'announcement', ['holy-prophet', 'imam-hasan', 'imam-ridha']),
 'arbaeen-2025-announcement': (2, 'announcement', ['imam-hussain', 'arbaeen']),
 'martyrdom-ruqayyah-and-imam-hasan': (2, 'announcement', ['lady-ruqayyah', 'imam-hasan']),
 'martyrdom-of-imam-al-sajjad': (1, 'announcement', ['imam-sajjad']),
 'muharram-1447-food-drive': (1, 'announcement', ['imam-hussain', 'community-service']),
 'ghadir-day-2025-thank-you': (12, 'announcement', ['imam-ali', 'ghadir', 'community-service']),
 'arrival-of-safar-announcement': (2, 'announcement', ['lady-ruqayyah']),
}
# every Mourning chapter inherits the series' tags
for _n in range(1, 11): ITEMS[f'morning-and-evening-mourning/{_n}'] = ITEMS['morning-and-evening-mourning']
for _n in (1, 2): ITEMS[f'recognition-of-arbaeen/{_n}'] = ITEMS['recognition-of-arbaeen']
# Booklets (PDF -> article series, build_booklets.py): series-level month/tags, with per-booklet tags/month where they differ
ITEMS['muharram-safar-booklets'] = (1, 'series', ['imam-hussain', 'mourning'])
ITEMS['ghadir-booklets'] = (12, 'series', ['imam-ali', 'ghadir'])
ITEMS['ramadan-booklets'] = (9, 'series', ['ziyarat'])
for _n in range(1, 41):
    ITEMS[f'muharram-safar-booklets/{_n}'] = ITEMS['muharram-safar-booklets']
    ITEMS[f'ghadir-booklets/{_n}'] = ITEMS['ghadir-booklets']
    ITEMS[f'ramadan-booklets/{_n}'] = ITEMS['ramadan-booklets']
_MH = ['imam-hussain', 'mourning']
for _n, (_m, _tags) in {3: (1, ['lady-ruqayyah'] + _MH), 4: (1, ['imam-sajjad'] + _MH), 6: (1, ['imam-hasan'] + _MH), 9: (1, ['lady-ruqayyah'] + _MH),
                        10: (1, ['imam-mahdi', 'ziyarat'] + _MH), 11: (1, _MH), 12: (1, ['imam-sajjad', 'ziyarat', 'imam-hussain']), 13: (1, ['lady-ruqayyah'] + _MH),
                        14: (1, ['imam-hasan']), 15: (2, ['lady-umm-al-banin', 'ziyarat']), 16: (2, ['lady-umm-al-banin']), 17: (1, ['lady-ruqayyah'] + _MH),
                        18: (2, ['imam-hussain', 'arbaeen'])}.items():
    ITEMS[f'muharram-safar-booklets/{_n}'] = (_m, 'series', _tags)
for _n, _tags in {6: ['lady-fatimah-zahra', 'ghadir'], 7: ['imam-ali', 'ghadir', 'ziyarat'], 8: ['ziyarat'], 9: ['imam-ali', 'ghadir']}.items():
    ITEMS[f'ghadir-booklets/{_n}'] = (12, 'series', _tags)
ITEMS['ramadan-booklets/1'] = (9, 'series', ['lady-khadijah', 'ziyarat'])
# Lady Khadijah series from the Telegram channels (build_khadijah.py): poems 8 parts, biography 4, ziyarat explanation 4
ITEMS['lady-khadijah-poems'] = (4, 'series', ['lady-khadijah', 'holy-prophet'])
ITEMS['lady-khadijah-biography'] = (4, 'series', ['lady-khadijah'])
ITEMS['lady-khadijah-ziyarat'] = (4, 'series', ['lady-khadijah', 'ziyarat'])
for _n in range(1, 13):
    for _s in ('lady-khadijah-poems', 'lady-khadijah-biography', 'lady-khadijah-ziyarat'): ITEMS[f'{_s}/{_n}'] = ITEMS[_s]
# Sermon of Muttaqin (Imam Ali's sermon, posted weekly since June 2026); the series is filed under Rabi' al-Awwal (month 3)
ITEMS['khutbat-al-muttaqin'] = (3, 'series', ['imam-ali'])
for _n in range(1, 15): ITEMS[f'khutbat-al-muttaqin/{_n}'] = ITEMS['khutbat-al-muttaqin']


def meta(slug):
    return ITEMS.get(slug)


def month_name(lang, m):
    return ANY_MONTH[lang] if m == 0 else MONTHS[lang][m - 1]


def month_path(m):
    return 'any-time' if m == 0 else MONTH_SLUG[m - 1]


def tag_list(slug, lang):
    """[(kind, key, label, href-path-under-/articles/)] for the chips on an article page: month, type, then people/topics."""
    mo, ty, tags = ITEMS[slug]
    out = [('month', mo, month_name(lang, mo), f'month/{month_path(mo)}/'), ('type', ty, TYPES[ty][lang], f'type/{ty}/')]
    out += [('tag', t, TAGS[t][lang], f'tag/{t}/') for t in tags]
    return out
