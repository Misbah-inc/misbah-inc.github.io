/* ─── MISBAH MOONSIGHTING ENGINE — multilingual, 1448 AH month picker ── */
(function(){
'use strict';

var HIJRI_YEAR = 1448;
var lang=document.documentElement.lang||'en';

var MONTHS={
  en:['','Muharram','Safar','Rabi al-Awwal','Rabi al-Thani','Jumada al-Ula','Jumada al-Akhirah','Rajab',"Sha'ban",'Ramadan','Shawwal',"Dhu al-Qi'dah",'Dhu al-Hijjah'],
  ar:['','مُحَرَّم','صَفَر','رَبِيعُ الأَوَّل','رَبِيعُ الآخِر','جُمَادَى الأُولَى','جُمَادَى الآخِرَة','رَجَب','شَعْبَان','رَمَضَان','شَوَّال','ذُو القَعْدَة','ذُو الحِجَّة'],
  fa:['','محرّم','صفر','ربیع‌الاول','ربیع‌الثانی','جمادی‌الاول','جمادی‌الثانی','رجب','شعبان','رمضان','شوال','ذی‌القعده','ذی‌الحجه'],
  ur:['','محرّم','صفر','ربیع الاول','ربیع الثانی','جمادی الاول','جمادی الثانی','رجب','شعبان','رمضان','شوال','ذو القعدہ','ذوالحجہ']
};

var REGION_NAMES={
  en:{easia:'East Asia & Pacific',aus:'Australia & NZ',seasia:'Southeast Asia',russia:'Russia & Siberia',sasia:'South Asia',persia:'Central Asia',mideast:'Middle East',afeu:'Africa & Europe',amer:'The Americas'},
  ar:{easia:'شرق آسيا والمحيط الهادئ',aus:'أستراليا ونيوزيلندا',seasia:'جنوب شرق آسيا',russia:'روسيا وسيبيريا',sasia:'جنوب آسيا',persia:'آسيا الوسطى',mideast:'الشرق الأوسط',afeu:'أفريقيا وأوروبا',amer:'الأمريكتان'},
  fa:{easia:'آسیای شرقی و اقیانوس آرام',aus:'استرالیا و نیوزیلند',seasia:'آسیای جنوب شرقی',russia:'روسیه و سیبری',sasia:'جنوب آسیا',persia:'آسیای مرکزی',mideast:'خاورمیانه',afeu:'آفریقا و اروپا',amer:'قاره‌های آمریکا'},
  ur:{easia:'مشرقی ایشیا و بحرالکاہل',aus:'آسٹریلیا و نیوزی لینڈ',seasia:'جنوب مشرقی ایشیا',russia:'روس و سائبیریا',sasia:'جنوبی ایشیا',persia:'وسطی ایشیا',mideast:'مشرق وسطیٰ',afeu:'افریقہ و یورپ',amer:'امریکی براعظم'}
};

var VIS_LABELS={
  en:{vis:'Clearly visible',opt:'Binoculars',not:'Not visible'},
  ar:{vis:'مرئي بوضوح',opt:'بالمنظار',not:'غير مرئي'},
  fa:{vis:'قابل رؤیت',opt:'دوربین لازم',not:'قابل رؤیت نیست'},
  ur:{vis:'نظر آتا ہے',opt:'دوربین سے',not:'نظر نہیں آئے گا'}
};

var CONJ_LABEL={en:'Conjunction:',ar:'الاقتران:',fa:'اقتران:',ur:'اقتران:'};
var DATE_LOCALE={en:'en-US',ar:'ar',fa:'fa',ur:'ur'};
var NIGHT_DATE_LABEL={en:'Night Date',ar:'تاريخ الليلة',fa:'تاریخ شب',ur:'رات کی تاریخ'};

function beginsStr(monthName,lang){
  if(lang==='ar') return 'يبدأ '+monthName;
  if(lang==='fa') return monthName+' آغاز می‌شود';
  if(lang==='ur') return monthName+' شروع ہوتا ہے';
  return monthName+' begins';
}

/* ── Gregorian → Hijri ── */
function gToH(gy,gm,gd){
  var jd=Math.floor((1461*(gy+4800+Math.floor((gm-14)/12)))/4)
        +Math.floor((367*(gm-2-12*Math.floor((gm-14)/12)))/12)
        -Math.floor((3*Math.floor((gy+4900+Math.floor((gm-14)/12))/100))/4)+gd-32075;
  var l=jd-1948440+10632,n=Math.floor((l-1)/10631);
  l=l-10631*n+354;
  var j=Math.floor((10985-l)/5316)*Math.floor((50*l)/17719)+Math.floor(l/5670)*Math.floor((43*l)/15238);
  l=l-Math.floor((30-j)/15)*Math.floor((17719*j)/50)-Math.floor(j/16)*Math.floor((15238*j)/43)+29;
  return{y:30*n+j-30,m:Math.floor((24*l)/709),d:l-Math.floor((709*Math.floor((24*l)/709))/24)};
}

/* ── Hijri → approximate Julian Day ── */
function hToJD(hy,hm,hd){
  return Math.floor((11*hy+3)/30)+354*hy+30*hm-Math.floor((hm-1)/2)+hd+1948440-385;
}

/* ── Meeus new moon JDE ── */
function newMoonJDE(k){
  var T=k/1236.85,T2=T*T,T3=T2*T,r=Math.PI/180;
  var JDE=2451550.09766+29.530588861*k+0.00015437*T2-0.000000150*T3;
  var M  =(2.5534   +29.10535670*k -0.0000014*T2)*r;
  var Mp =(201.5643 +385.81693528*k+0.0107582*T2-0.00001238*T3)*r;
  var F  =(160.7108 +390.67050284*k-0.0016118*T2-0.00000227*T3)*r;
  var O  =(124.7746 -1.56375588*k  +0.0020672*T2)*r;
  return JDE
    -0.40720*Math.sin(Mp)-0.17241*Math.sin(M)+0.01608*Math.sin(2*Mp)
    +0.01039*Math.sin(2*F)-0.00739*Math.sin(Mp-M)+0.00514*Math.sin(Mp+M)
    -0.00208*Math.sin(2*M)-0.00111*Math.sin(Mp-2*F)-0.00057*Math.sin(Mp+2*F)
    +0.00056*Math.sin(2*Mp+M)-0.00042*Math.sin(3*Mp)+0.00042*Math.sin(M+2*F)
    +0.00038*Math.sin(M-2*F)-0.00024*Math.sin(2*Mp-M)-0.00017*Math.sin(O)
    -0.00007*Math.sin(Mp+2*F-M);
}

function jdToMs(jd){return(jd-2440587.5)*86400000;}

/* ── Find new moon closest to Hijri H/M/1 ── */
function newMoonForHijriMonth(hy,hm){
  var approxMs=jdToMs(hToJD(hy,hm,1));
  var k0=Math.round((approxMs/86400000+2440587.5-2451550.09766)/29.530588861);
  var best=null,bestDiff=Infinity;
  for(var i=-2;i<=2;i++){
    var ms=jdToMs(newMoonJDE(k0+i));
    var diff=Math.abs(ms-approxMs);
    if(diff<bestDiff){bestDiff=diff;best=ms;}
  }
  return new Date(best);
}

/* ── Precompute all 12 new moons for HIJRI_YEAR ── */
var HIJRI_NMS={};
for(var _m=1;_m<=12;_m++) HIJRI_NMS[_m]=newMoonForHijriMonth(HIJRI_YEAR,_m);

var REGIONS=[
  {id:'easia',  utcH:34,  svgId:'nm-g-easia',   flag:'🌏'},
  {id:'aus',    utcH:32,  svgId:'nm-g-aus',      flag:'🌏'},
  {id:'seasia', utcH:35,  svgId:'nm-g-seasia',   flag:'🌏'},
  {id:'russia', utcH:35,  svgId:'nm-g-russia',   flag:'🌏'},
  {id:'sasia',  utcH:36.5,svgId:'nm-g-sasia',    flag:'🌏'},
  {id:'persia', utcH:37,  svgId:'nm-g-persia',   flag:'🌏'},
  {id:'mideast',utcH:39,  svgId:'nm-g-mideast',  flag:'☽'},
  {id:'afeu',   utcH:42,  svgId:'nm-g-afeu',     flag:'🌍'},
  {id:'amer',   utcH:47,  svgId:'nm-g-americas', flag:'🌎'},
];

var C_VIS='#38b872',C_OPT='#c9a46b',C_NOT='#a03535';

/* Thresholds: <17h not visible, 17-26h binoculars, ≥26h clearly visible */
function visColor(age){return age<17?C_NOT:age<26?C_OPT:C_VIS;}

function lunarAge(nmMs,hoursFromNmMidnight){
  var mid=new Date(nmMs);mid.setUTCHours(0,0,0,0);
  return(mid.getTime()+hoursFromNmMidnight*3600000-nmMs)/3600000;
}

/* ── Main display function — called on month picker / night picker click ──
   nightOff: 0 = conjunction night (utcH-24), 1 = night 1 (utcH) [default], 2 = night 2 (utcH+24) */
function showMonthMap(hm,nightOff){
  if(nightOff===undefined) nightOff=1;
  var months=MONTHS[lang]||MONTHS.en;
  var rnames=REGION_NAMES[lang]||REGION_NAMES.en;
  var vlabels=VIS_LABELS[lang]||VIS_LABELS.en;
  var locale=DATE_LOCALE[lang]||'en-US';
  var FMT={weekday:'short',month:'short',day:'numeric',timeZone:'UTC'};

  var nm=HIJRI_NMS[hm];
  var nmMs=nm.getTime();

  var elM=document.getElementById('nm-cur-month');
  if(elM) elM.textContent=months[hm]+' '+HIJRI_YEAR;

  var elT=document.getElementById('nm-nm-time');
  if(elT) elT.textContent=CONJ_LABEL[lang]+' '+nm.toUTCString().replace(' GMT','')+' UTC';

  var elD=document.getElementById('nm-map-date');
  if(elD) elD.textContent=nm.toLocaleDateString(locale,{month:'short',day:'numeric',timeZone:'UTC'});

  var nmMid=new Date(nmMs);nmMid.setUTCHours(0,0,0,0);
  var nmDayStart=nmMid.getTime();

  /* nightOff mapping: 0 = utcH-24 (conjunction night), 1 = utcH (first night), 2 = utcH+24 (second night) */
  var results=REGIONS.map(function(r){
    var utcHOff=r.utcH+(nightOff-1)*24;
    var age=lunarAge(nmMs,utcHOff);
    var col=visColor(age);
    var dayOff=Math.floor(utcHOff/24);
    var sightDate=new Date(nmDayStart+dayOff*86400000);
    var lbl=col===C_VIS?vlabels.vis:col===C_OPT?vlabels.opt:vlabels.not;
    return{id:r.id,name:rnames[r.id]||r.id,flag:r.flag,col:col,lbl:lbl,age:Math.max(0,age).toFixed(1),sightDate:sightDate,svgId:r.svgId};
  });

  /* Show the date of the selected night (not a prediction — user decides) */
  var elS=document.getElementById('nm-start-date');
  if(elS){
    var nightDate=new Date(nmDayStart+nightOff*86400000);
    elS.textContent=nightDate.toLocaleDateString(locale,FMT);
  }

  /* Visibility gradient: try pre-generated Yallop PNG first, fall back to canvas */
  var visImg=document.getElementById('nm-vis-image');
  if(visImg){
    /* Build PNG filename from NM date + night index */
    var nmD=new Date(nmMs);
    var dateTag=nmD.getUTCFullYear().toString()+
      ('0'+(nmD.getUTCMonth()+1)).slice(-2)+
      ('0'+nmD.getUTCDate()).slice(-2);
    var pngUrl='/moonsighting/maps/vis_n'+nightOff+'_'+dateTag+'.png';

    var testImg=new window.Image();
    testImg.onload=function(){
      visImg.setAttribute('href',pngUrl);
      visImg.setAttributeNS('http://www.w3.org/1999/xlink','href',pngUrl);
    };
    testImg.onerror=function(){
      /* Fallback: approximate canvas gradient (simple lunar-age bands) */
      var nmMidMsG=new Date(nmMs);nmMidMsG.setUTCHours(0,0,0,0);
      var nmHoursG=(nmMs-nmMidMsG.getTime())/3600000;
      var nmDateG=new Date(nmMs);
      var doyG=Math.round((nmDateG-new Date(Date.UTC(nmDateG.getUTCFullYear(),0,1)))/86400000)+1;
      var declR=23.45*Math.sin(2*Math.PI/365*(doyG-81))*Math.PI/180;
      var W=800,H=400;
      var cnv=document.createElement('canvas');cnv.width=W;cnv.height=H;
      var ctx=cnv.getContext('2d');
      ctx.fillStyle='#071220';ctx.fillRect(0,0,W,H);
      for(var py=0;py<H;py++){
        var lat=(90-(py/H)*180)*Math.PI/180;
        var cosHA=-Math.tan(lat)*Math.tan(declR);
        var daylen=cosHA>=1?0:cosHA<=-1?24:2*Math.acos(cosHA)*180/Math.PI/15;
        var base=12+daylen/2+nightOff*24-nmHoursG;
        var x26=Math.max(0,Math.min(W,Math.round((15*(base-26)+180)/360*W)));
        var x17=Math.max(0,Math.min(W,Math.round((15*(base-17)+180)/360*W)));
        if(x26>0){ctx.fillStyle='#38b872';ctx.fillRect(0,py,x26,1);}
        if(x17>x26){ctx.fillStyle='#c9a46b';ctx.fillRect(x26,py,x17-x26,1);}
        if(x17<W){ctx.fillStyle='#a03535';ctx.fillRect(x17,py,W-x17,1);}
      }
      var url=cnv.toDataURL('image/png');
      visImg.setAttribute('href',url);
      visImg.setAttributeNS('http://www.w3.org/1999/xlink','href',url);
    };
    testImg.src=pngUrl;
  } else {
    /* Legacy fallback: color individual region SVG paths */
    results.forEach(function(r){
      var g=document.getElementById(r.svgId);
      if(!g) return;
      var stroke=r.col===C_VIS?'rgba(56,184,114,.35)':r.col===C_OPT?'rgba(201,164,107,.35)':'rgba(160,53,53,.3)';
      g.querySelectorAll('path,circle,polygon').forEach(function(el){
        el.setAttribute('fill',r.col);
        el.setAttribute('stroke',stroke);
      });
    });
  }

  var grid=document.getElementById('nm-region-grid');
  if(grid){
    grid.innerHTML=results.map(function(r){
      return'<div class="nm-rc">'
        +'<div class="nm-rc-dot" style="background:'+r.col+'"></div>'
        +'<div><div class="nm-rc-name">'+r.flag+' '+r.name+'</div>'
        +'<div class="nm-rc-meta">'+r.lbl+' &middot; '+r.age+'h</div></div>'
        +'<div class="nm-rc-date">'+r.sightDate.toLocaleDateString(locale,FMT)+'</div>'
        +'</div>';
    }).join('');
  }
}

/* ── Init on DOM ready ── */
/* ── Static UI translation strings ─────────────────────────────────────── */
var UI={
  en:{
    heroSub:'1448 AH — Select a month to view crescent visibility predictions worldwide',
    selMonth:'Selected Month', predStart:'Night Date',
    night0:'☽₀ Conjunction Night',night0sub:'Day of new moon',
    night1:'☽₁ First Night',night1sub:'Evening after new moon',
    night2:'☽₂ Second Night',night2sub:'Two evenings after',
    legA:'A — Easily visible (naked eye)',legB:'B — Visible under perfect conditions',
    legC:'C — Optical aid to find moon',legD:'D — Optical aid only',legEF:'E/F — Not visible'
  },
  ar:{
    heroSub:'١٤٤٨ هـ — اختر شهراً لعرض توقعات رؤية الهلال حول العالم',
    selMonth:'الشهر المحدد', predStart:'تاريخ الليلة',
    night0:'☽₀ ليلة الاقتران',night0sub:'يوم الهلال الجديد',
    night1:'☽₁ الليلة الأولى',night1sub:'مساء ما بعد الهلال',
    night2:'☽₂ الليلة الثانية',night2sub:'مساءان بعد الهلال',
    legA:'أ — يُرى بالعين المجردة',legB:'ب — يُرى في ظروف مثالية',
    legC:'ج — يحتاج منظاراً',legD:'د — بالمنظار فقط',legEF:'هـ/و — غير مرئي'
  },
  fa:{
    heroSub:'۱۴۴۸ هـ — ماهی را برای مشاهده پیش‌بینی رؤیت هلال انتخاب کنید',
    selMonth:'ماه انتخابی', predStart:'تاریخ شب',
    night0:'☽₀ شب اقتران',night0sub:'روز ماه نو',
    night1:'☽₁ شب اول',night1sub:'شب پس از اقتران',
    night2:'☽₂ شب دوم',night2sub:'دو شب پس از اقتران',
    legA:'الف — با چشم غیر مسلح دیده می‌شود',legB:'ب — در شرایط کامل دیده می‌شود',
    legC:'ج — نیاز به دوربین دارد',legD:'د — فقط با دوربین',legEF:'هـ/و — دیده نمی‌شود'
  },
  ur:{
    heroSub:'١٤٤٨ ہجری — چاند کی رؤیت کی پیش گوئی کے لیے مہینہ منتخب کریں',
    selMonth:'منتخب مہینہ', predStart:'رات کی تاریخ',
    night0:'☽₀ اقتران کی رات',night0sub:'نئے چاند کا دن',
    night1:'☽₁ پہلی رات',night1sub:'نئے چاند کے بعد کی شام',
    night2:'☽₂ دوسری رات',night2sub:'دو شامیں بعد میں',
    legA:'الف — ننگی آنکھ سے نظر آتا ہے',legB:'ب — بہترین حالات میں نظر آتا ہے',
    legC:'ج — دوربین سے تلاش کریں',legD:'د — صرف دوربین سے',legEF:'ہ/و — نظر نہیں آئے گا'
  }
};

document.addEventListener('DOMContentLoaded',function(){
  var today=new Date();
  var hToday=gToH(today.getUTCFullYear(),today.getUTCMonth()+1,today.getUTCDate());
  var curHM=(hToday.y===HIJRI_YEAR)?hToday.m:1;
  var curNight=1;

  /* Translate static UI from UI[lang] */
  var u=UI[lang]||UI.en;
  var hs=document.querySelector('.nm-hero-sub'); if(hs) hs.textContent=u.heroSub;
  var pls=document.querySelectorAll('.nm-pred-label');
  if(pls[0]) pls[0].textContent=u.selMonth;
  if(pls[1]) pls[1].textContent=u.predStart;
  var npArr=document.querySelectorAll('.nm-npick');
  [[0,u.night0,u.night0sub],[1,u.night1,u.night1sub],[2,u.night2,u.night2sub]].forEach(function(x){
    var btn=npArr[x[0]]; if(!btn) return;
    btn.childNodes[0].textContent=x[1];
    var sp=btn.querySelector('span'); if(sp) sp.textContent=x[2];
  });
  var legs=document.querySelectorAll('.nm-legend-item');
  [u.legA,u.legB,u.legC,u.legD,u.legEF].forEach(function(t,i){
    if(legs[i]) legs[i].lastChild.textContent=' '+t;
  });

  /* Translate month picker buttons */
  var picks=document.querySelectorAll('.nm-mpick');
  picks.forEach(function(btn){
    var hm=parseInt(btn.getAttribute('data-hm'),10);
    if(MONTHS[lang]&&MONTHS[lang][hm]) btn.textContent=MONTHS[lang][hm];
    if(hm===curHM) btn.classList.add('nm-mpick--active');
    btn.addEventListener('click',function(){
      picks.forEach(function(b){b.classList.remove('nm-mpick--active');});
      btn.classList.add('nm-mpick--active');
      curHM=hm;
      showMonthMap(curHM,curNight);
    });
  });

  /* Night picker */
  var npicks=document.querySelectorAll('.nm-npick');
  npicks.forEach(function(btn){
    btn.addEventListener('click',function(){
      npicks.forEach(function(b){b.classList.remove('nm-npick--active');});
      btn.classList.add('nm-npick--active');
      curNight=parseInt(btn.getAttribute('data-night'),10);
      showMonthMap(curHM,curNight);
    });
  });

  if(picks.length) showMonthMap(curHM,curNight);
});

})();
