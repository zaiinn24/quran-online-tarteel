# -*- coding: utf-8 -*-
"""Completes every Duas & Azkar page with all authentic duas of the matching Hisn al-Muslim chapters, adds the full 40 Rabbana duas,
and adds new topic pages (sleeping, travel, wudu & masjid). Arabic copied from Hisn al-Muslim / sunnah.com (obvious vowel typos fixed)
or from the King Fahd Complex Uthmani Quran text. English and Roman Urdu meanings written by Quran Online Tarteel."""

QULS = "QULS"


def Q(s, a, w0=0, w1=None):
    return ("Q", s, a, w0, w1)


def apply(PAGES, ORDER):
    def old(slug, when):
        for it in PAGES[slug]["items"]:
            if it[0] == when:
                return it
        raise KeyError((slug, when))

    # ---------------- AZKAR AFTER NAMAZ (complete) ----------------
    p = "azkar-after-namaz"
    tasbih = old(p, "Tasbih after every prayer")
    tasbih = (tasbih[0], tasbih[1],
              tasbih[2] + " Another authentic way is SubhanAllah 33, Alhamdulillah 33 and Allahu Akbar 34 (Sahih Muslim 596).",
              tasbih[3] + " Doosra sahih tareeqa: SubhanAllah 33, Alhamdulillah 33 aur Allahu Akbar 34 martaba (Sahih Muslim 596).",
              tasbih[4], tasbih[5], tasbih[6])
    PAGES[p]["items"] = [
        old(p, "Straight after salam"),
        old(p, "After every prayer"),
        ("La ilaha illallah, la hawla wa la quwwata illa billah",
         "لا إلهَ إلاّ اللّه وحدَهُ لا شريكَ لهُ لهُ الملكُ ولهُ الحَمد وهوَ على كلّ شيءٍ قدير لا حَوْلَ وَلا قوَّةَ إِلاّ بِاللهِ لا إلهَ إلاّ اللّه وَلا نَعْبُدُ إِلاّ إيّاه لَهُ النِّعْمَةُ وَلَهُ الفَضْل وَلَهُ الثَّناءُ الحَسَن لا إلهَ إلاّ اللّهُ مخْلِصينَ لَهُ الدِّينَ وَلَوْ كَرِهَ الكافِرون",
         "Lā ilāha illallāhu waḥdahu lā sharīka lah, lahul-mulku wa lahul-ḥamd, wa huwa `alā kulli shay'in qadīr. Lā ḥawla wa lā quwwata illā billāh. Lā ilāha illallāhu wa lā na`budu illā iyyāh, lahun-ni`matu wa lahul-faḍlu wa lahuth-thanā'ul-ḥasan. Lā ilāha illallāhu mukhliṣīna lahud-dīna wa law karihal-kāfirūn.",
         "There is no god but Allah alone, with no partner; His is the dominion and His is the praise, and He has power over all things. There is no power and no strength except with Allah. There is no god but Allah, and we worship none but Him. His are all blessings, all grace and the most beautiful praise. There is no god but Allah; we dedicate our worship sincerely to Him, even if the disbelievers dislike it.",
         "Allah ke siwa koi mabood nahin, woh akela hai, Us ka koi shareek nahin, badshahi aur tareef Usi ki hai aur woh har cheez par qadir hai. Allah ke siwa na koi taaqat hai na quwwat. Allah ke siwa koi mabood nahin aur hum Us ke siwa kisi ki ibadat nahin karte. Saari nematein, saara fazl aur behtareen tareef Usi ki hai. Allah ke siwa koi mabood nahin, hum khaalis Usi ki ibadat karte hain chahe kafiron ko bura lage.",
         "1", "Sahih Muslim (Hisn al-Muslim 68)"),
        tasbih,
        ("The 3 Quls after every prayer", QULS, "Qul huwallāhu aḥad... Qul a`ūdhu bi-rabbil-falaq... Qul a`ūdhu bi-rabbin-nās...",
         "Recite Surah Al-Ikhlas, Al-Falaq and An-Nas once after every prayer.", "Har namaz ke baad Surah Ikhlas, Surah Falaq aur Surah Naas ek ek baar parhein.",
         "1", "Abu Dawud; An-Nasa'i (Hisn al-Muslim 70)"),
        old(p, "Ayatul Kursi after every prayer"),
        old(p, "After Fajr and Maghrib"),
        old(p, "After Fajr"),
        ("For help in worship (end of every prayer)", "اللّهُمَّ أَعِنِّي عَلى ذِكْرِكَ وَشُكْرِك ، وَحُسْنِ عِبادَتِك",
         "Allāhumma a`innī `alā dhikrika wa shukrika wa ḥusni `ibādatik.",
         "O Allah, help me to remember You, to thank You and to worship You in the best way. The Prophet, peace be upon him, told Mu'adh never to leave it at the end of every prayer.",
         "Ae Allah, apne zikr, apne shukr aur apni achhi ibadat par meri madad farma. Nabi ﷺ ne Hazrat Muaz (RA) ko har namaz ke aakhir mein yeh dua na chhorne ki naseehat ki.",
         "1", "Abu Dawud; An-Nasa'i (Hisn al-Muslim 59)"),
        ("Before salam: seeking protection from four things", "اللّهُمَّ إِنِّي أَعوذُ بِكَ مِنْ عَذابِ القَبْر، وَمِنْ عَذابِ جَهَنَّم، وَمِنْ فِتْنَةِ المَحْيا وَالمَمات، وَمِنْ شَرِّ فِتْنَةِ المَسيحِ الدَّجّال",
         "Allāhumma innī a`ūdhu bika min `adhābil-qabr, wa min `adhābi jahannam, wa min fitnatil-maḥyā wal-mamāt, wa min sharri fitnatil-masīḥid-dajjāl.",
         "O Allah, I seek Your protection from the punishment of the grave, from the punishment of Hell, from the trials of life and death, and from the evil of the trial of the False Messiah (Dajjal). Said in the last sitting, after tashahhud and before salam.",
         "Ae Allah, main qabr ke azaab se, jahannam ke azaab se, zindagi aur maut ke fitnon se aur Masih Dajjal ke fitne ki buraai se Teri panah mangta hoon. (Aakhri qaida mein tashahhud ke baad, salam se pehle.)",
         "1", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 55)"),
        ("Before salam: the dua taught to Abu Bakr", "اللّهُمَّ إِنِّي ظَلَمْتُ نَفْسي ظُلْماً كَثيراً وَلا يَغْفِرُ الذُّنوبَ إِلاّ أَنْت، فَاغْفِر لي مَغْفِرَةً مِنْ عِنْدِك وَارْحَمْني، إِنَّكَ أَنْتَ الغَفورُ الرَّحيم",
         "Allāhumma innī ẓalamtu nafsī ẓulman kathīran wa lā yaghfirudh-dhunūba illā ant, faghfir lī maghfiratan min `indika warḥamnī, innaka antal-ghafūrur-raḥīm.",
         "O Allah, I have wronged myself greatly, and none forgives sins except You. So grant me forgiveness from Yourself and have mercy on me. You are the Forgiving, the Merciful.",
         "Ae Allah, main ne apne aap par bahut zulm kiya, aur Tere siwa koi gunah maaf nahin karta. Pas apni taraf se mujhe bakhsh de aur mujh par reham farma. Beshak Tu bakhshne wala, reham karne wala hai.",
         "1", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 57)"),
        ("Before salam: asking for complete forgiveness", "اللّهُمَّ اغْفِرْ لي ما قَدَّمْتُ وَما أَخَّرْت ، وَما أَسْرَرْتُ وَما أَعْلَنْت ، وَما أَسْرَفْت ، وَما أَنْتَ أَعْلَمُ بِهِ مِنِّي . أَنْتَ المُقَدِّمُ، وَأَنْتَ المُؤَخِّرُ لا إِلهَ إِلاّ أَنْت",
         "Allāhummaghfir lī mā qaddamtu wa mā akhkhartu, wa mā asrartu wa mā a`lantu, wa mā asraftu, wa mā anta a`lamu bihī minnī, antal-muqaddimu wa antal-mu'akhkhiru, lā ilāha illā ant.",
         "O Allah, forgive me what I did before and what I left for later, what I did in secret and what I did openly, what I did in excess, and what You know better than I do. You bring forward and You put back. There is no god but You.",
         "Ae Allah, mere agle aur pichhle gunah, chhup kar aur khule kiye hue gunah, meri zyadtiyan aur woh sab maaf farma jo Tu mujh se zyada jaanta hai. Tu hi aage karne wala aur peeche karne wala hai, Tere siwa koi mabood nahin.",
         "1", "Sahih Muslim (Hisn al-Muslim 58)"),
    ]

    # ---------------- MORNING & EVENING (complete) ----------------
    p = "morning-evening-azkar"
    me = lambda w: old(p, w)
    PAGES[p]["items"] = [
        me("Ayatul Kursi"), me("The 3 Quls: Al-Ikhlas, Al-Falaq, An-Nas"), me("Asbahna wa Asbahal Mulku Lillah"), me("Allahumma Bika Asbahna"), me("Sayyid al-Istighfar"),
        ("Bearing witness to Allah's oneness", "اللّهُمَّ إِنِّي أَصْبَحْتُ أُشْهِدُك ، وَأُشْهِدُ حَمَلَةَ عَرْشِك ، وَمَلائِكَتِك ، وَجَميعَ خَلْقِك ، أَنَّكَ أَنْتَ اللهُ لا إلهَ إلاّ أَنْتَ وَحْدَكَ لا شَريكَ لَك ، وَأَنَّ مُحَمّداً عَبْدُكَ وَرَسولُك",
         "Allāhumma innī aṣbaḥtu ush-hiduka wa ush-hidu ḥamalata `arshik, wa malā'ikatak, wa jamī`a khalqik, annaka antallāhu lā ilāha illā ant, waḥdaka lā sharīka lak, wa anna Muḥammadan `abduka wa rasūluk. (Evening: Allāhumma innī amsaytu...)",
         "O Allah, this morning I call You, the bearers of Your Throne, Your angels and all Your creation to witness that You are Allah, there is no god but You alone, with no partner, and that Muhammad is Your servant and Messenger.",
         "Ae Allah, main ne subah ki aur main Tujhe, Tere Arsh uthane walon ko, Tere farishton ko aur Teri saari makhlooq ko gawah banata hoon ke Tu hi Allah hai, Tere siwa koi mabood nahin, Tu akela hai, Tera koi shareek nahin, aur Muhammad ﷺ Tere bande aur Rasool hain.",
         "4", "Abu Dawud (Hisn al-Muslim 80)"),
        ("Thanking Allah for every blessing", "اللّهُمَّ ما أَصْبَحَ بي مِنْ نِعْمَةٍ أَو بِأَحَدٍ مِنْ خَلْقِك ، فَمِنْكَ وَحْدَكَ لا شريكَ لَك ، فَلَكَ الْحَمْدُ وَلَكَ الشُّكْر",
         "Allāhumma mā aṣbaḥa bī min ni`matin aw bi-aḥadin min khalqik, faminka waḥdaka lā sharīka lak, falakal-ḥamdu wa lakash-shukr. (Evening: Allāhumma mā amsā bī...)",
         "O Allah, whatever blessing I or any of Your creation have this morning is from You alone, with no partner. All praise and all thanks are Yours.",
         "Ae Allah, aaj subah mujhe ya Teri makhlooq mein se kisi ko jo bhi nemat mili hai woh sirf Teri taraf se hai, Tera koi shareek nahin. Pas tamam tareef aur shukr Tere hi liye hai.",
         "1", "Abu Dawud (Hisn al-Muslim 81)"),
        me("For wellbeing"),
        ("Allah is enough for me", "حَسْبِيَ اللّهُ لا إلهَ إلاّ هُوَ عَلَيهِ تَوَكَّلتُ وَهُوَ رَبُّ العَرْشِ العَظيم",
         "Ḥasbiyallāhu lā ilāha illā huwa `alayhi tawakkaltu wa huwa rabbul-`arshil-`aẓīm.",
         "Allah is enough for me. There is no god but Him. In Him I put my trust, and He is the Lord of the Mighty Throne.",
         "Mere liye Allah kaafi hai, Us ke siwa koi mabood nahin. Main ne Usi par bharosa kiya aur woh Arsh-e-Azeem ka Rab hai.",
         "7", "Abu Dawud (Hisn al-Muslim 83)"),
        ("For pardon and wellbeing", "اللّهُمَّ إِنِّي أسْأَلُكَ العَفْوَ وَالعافِيةَ في الدُّنْيا وَالآخِرَة ، اللّهُمَّ إِنِّي أسْأَلُكَ العَفْوَ وَالعافِيةَ في ديني وَدُنْيايَ وَأهْلي وَمالي ، اللّهُمَّ اسْتُرْ عوْراتي وَآمِنْ رَوْعاتي ، اللّهُمَّ احْفَظْني مِن بَينِ يَدَيَّ وَمِن خَلْفي وَعَن يَميني وَعَن شِمالي ، وَمِن فَوْقي ، وَأَعوذُ بِعَظَمَتِكَ أَن أُغْتالَ مِن تَحْتي",
         "Allāhumma innī as'alukal-`afwa wal-`āfiyata fid-dunyā wal-ākhirah. Allāhumma innī as'alukal-`afwa wal-`āfiyata fī dīnī wa dunyāya wa ahlī wa mālī. Allāhummastur `awrātī wa āmin raw`ātī. Allāhummaḥfaẓnī min bayni yadayya wa min khalfī wa `an yamīnī wa `an shimālī wa min fawqī, wa a`ūdhu bi-`aẓamatika an ughtāla min taḥtī.",
         "O Allah, I ask You for pardon and wellbeing in this world and the next. O Allah, I ask You for pardon and wellbeing in my religion, my worldly life, my family and my wealth. O Allah, cover my faults and calm my fears. O Allah, protect me from in front of me and behind me, from my right and my left, and from above me, and I seek protection in Your greatness from being taken unawares from below me.",
         "Ae Allah, main Tujh se duniya aur aakhirat mein maafi aur aafiyat mangta hoon. Ae Allah, main apne deen, apni duniya, apne ghar walon aur apne maal mein maafi aur aafiyat mangta hoon. Ae Allah, meri kamzoriyon par parda daal aur mere khauf ko aman mein badal de. Ae Allah, aage se, peeche se, daayen se, baayen se aur upar se meri hifazat farma, aur main Teri azmat ki panah mangta hoon ke neeche se achanak halaak kiya jaaun.",
         "1", "Abu Dawud; Ibn Majah (Hisn al-Muslim 84)"),
        ("Protection from the evil of oneself and Shaytan", "اللّهُمَّ عالِمَ الغَيْبِ وَالشّهادَةِ فاطِرَ السّماواتِ وَالأرْضِ رَبَّ كلِّ شَيءٍ وَمَليكَه ، أَشْهَدُ أَنْ لا إِلهَ إِلاّ أَنْت ، أَعوذُ بِكَ مِن شَرِّ نَفْسي وَمِن شَرِّ الشَّيْطانِ وَشِرْكِه ، وَأَنْ أَقْتَرِفَ عَلى نَفْسي سوءاً أَوْ أَجُرَّهُ إِلى مُسْلِم",
         "Allāhumma `ālimal-ghaybi wash-shahādah, fāṭiras-samāwāti wal-arḍ, rabba kulli shay'in wa malīkah, ash-hadu an lā ilāha illā ant, a`ūdhu bika min sharri nafsī wa min sharrish-shayṭāni wa shirkih, wa an aqtarifa `alā nafsī sū'an aw ajurrahū ilā muslim.",
         "O Allah, Knower of the unseen and the seen, Creator of the heavens and the earth, Lord and Owner of everything, I bear witness that there is no god but You. I seek Your protection from the evil of my own self, from the evil of Shaytan and his call to shirk, and from doing wrong to myself or bringing it upon any Muslim.",
         "Ae Allah, ghaib aur zaahir ke jaanne wale, aasmanon aur zameen ke paida karne wale, har cheez ke Rab aur Malik, main gawahi deta hoon ke Tere siwa koi mabood nahin. Main apne nafs ki buraai se, Shaitan ki buraai aur us ke shirk se, aur apne aap par koi buraai karne ya kisi Musalman ki taraf us ko le jaane se Teri panah mangta hoon.",
         "1", "At-Tirmidhi; Abu Dawud (Hisn al-Muslim 85)"),
        me("For protection from all harm"),
        ("Pleased with Allah, Islam and the Prophet", "رَضيتُ بِاللهِ رَبَّاً وَبِالإسْلامِ ديناً وَبِمُحَمَّدٍ نَبِيّاً",
         "Raḍītu billāhi rabbā, wa bil-islāmi dīnā, wa bi-Muḥammadin ṣallallāhu `alayhi wa sallama nabiyyā.",
         "I am pleased with Allah as my Lord, with Islam as my religion and with Muhammad, peace be upon him, as my Prophet.",
         "Main Allah ke Rab hone par, Islam ke deen hone par aur Muhammad ﷺ ke Nabi hone par raazi hoon.",
         "3", "Ahmad; An-Nasa'i (Hisn al-Muslim 87)"),
        me("Asking Allah to set every affair right"),
        ("The good of this day", "أَصْبَحْنا وَأَصْبَحَ المُلكُ للهِ رَبِّ العالَمين ، اللّهُمَّ إِنِّي أسْأَلُكَ خَيْرَ هذا اليَوْم ، فَتْحَهُ ، وَنَصْرَهُ ، وَنورَهُ وَبَرَكَتَهُ ، وَهُداهُ ، وَأَعوذُ بِكَ مِنْ شَرِّ ما فيهِ وَشَرِّ ما بَعْدَه",
         "Aṣbaḥnā wa aṣbaḥal-mulku lillāhi rabbil-`ālamīn. Allāhumma innī as'aluka khayra hādhal-yawm, fatḥahū wa naṣrahū wa nūrahū wa barakatahū wa hudāh, wa a`ūdhu bika min sharri mā fīhi wa sharri mā ba`dah. (Evening: Amsaynā wa amsal-mulku lillāhi rabbil-`ālamīn... khayra hādhihil-laylah...)",
         "We have entered the morning and all sovereignty belongs to Allah, Lord of the worlds. O Allah, I ask You for the good of this day: its openings, its help, its light, its blessings and its guidance. I seek Your protection from the evil in it and the evil after it.",
         "Hum ne subah ki aur saari badshahi Allah Rabbul Aalameen ki hai. Ae Allah, main Tujh se is din ki bhalai mangta hoon: is ki kaamyabi, is ki madad, is ka noor, is ki barkat aur is ki hidayat. Aur is din ki aur is ke baad ki buraai se Teri panah mangta hoon.",
         "1", "Abu Dawud (Hisn al-Muslim 89)"),
        ("La ilaha illallah ten times", "لا إلهَ إلاّ اللّهُ وحْدَهُ لا شَريكَ لهُ، لهُ المُلْكُ ولهُ الحَمْد، وهُوَ على كُلّ شَيءٍ قَدير",
         "Lā ilāha illallāhu waḥdahu lā sharīka lah, lahul-mulku wa lahul-ḥamd, wa huwa `alā kulli shay'in qadīr.",
         "There is no god but Allah alone, with no partner; His is the dominion and His is the praise, and He has power over all things. Say it ten times (or once on a lazy day); say it one hundred times in the morning for great reward.",
         "Allah ke siwa koi mabood nahin, woh akela hai, Us ka koi shareek nahin, badshahi aur tareef Usi ki hai aur woh har cheez par qadir hai. Das baar (ya susti ke din ek baar); subah sau baar kehna bahut bara ajr hai.",
         "10", "Sahih al-Bukhari; Sahih Muslim; An-Nasa'i (Hisn al-Muslim 92-93)"),
        me("Glorifying Allah"),
        ("Glory to Allah as much as His creation", "سُبْحانَ اللهِ وَبِحَمْدِهِ عَدَدَ خَلْقِه ، وَرِضا نَفْسِه ، وَزِنَةَ عَرْشِه ، وَمِدادَ كَلِماتِه",
         "Subḥānallāhi wa biḥamdihī `adada khalqih, wa riḍā nafsih, wa zinata `arshih, wa midāda kalimātih.",
         "Glory be to Allah and all praise is His, as many times as the number of His creation, as much as pleases Him, as heavy as His Throne and as endless as His words.",
         "Allah paak hai aur tamam tareef Usi ki hai, Us ki makhlooq ki ginti ke barabar, Us ki raza ke mutabiq, Us ke Arsh ke wazan ke barabar aur Us ke kalimaat ki siyahi ke barabar.",
         "3 (morning)", "Sahih Muslim (Hisn al-Muslim 94)"),
        ("For beneficial knowledge (morning)", "اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْماً نافِعاً وَرِزْقاً طَيِّباً وَعَمَلاً مُتَقَبَّلاً",
         "Allāhumma innī as'aluka `ilman nāfi`an, wa rizqan ṭayyiban, wa `amalan mutaqabbalā.",
         "O Allah, I ask You for beneficial knowledge, good and pure provision, and deeds that are accepted.",
         "Ae Allah, main Tujh se nafa dene wala ilm, paak rizq aur qabool hone wala amal mangta hoon.", "1", "Ibn Majah (Hisn al-Muslim 95)"),
        ("Istighfar one hundred times a day", "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ", "Astaghfirullāha wa atūbu ilayh.",
         "I ask Allah for forgiveness and I turn to Him in repentance.", "Main Allah se maghfirat mangta hoon aur Usi ki taraf tauba karta hoon.", "100", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 96)"),
        me("Evening protection"),
        ("Sending blessings on the Prophet", "اللَّهُمَّ صَلِّ وَ سَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ", "Allāhumma ṣalli wa sallim `alā nabiyyinā Muḥammad.",
         "O Allah, send Your blessings and peace upon our Prophet Muhammad.", "Ae Allah, hamare Nabi Muhammad ﷺ par durood aur salam bhej.", "10", "At-Tabarani (Hisn al-Muslim 98)"),
    ]

    # ---------------- DAILY DUAS FOR KIDS (complete daily set) ----------------
    p = "daily-duas-for-kids"
    k = lambda w: old(p, w)
    PAGES[p]["items"] = [
        k("When waking up"),
        ("When waking up (second dua)", "الحمدُ للهِ الذي عافاني في جَسَدي وَرَدّ عَليّ روحي وَأَذِنَ لي بِذِكْرِه",
         "Alḥamdu lillāhil-ladhī `āfānī fī jasadī, wa radda `alayya rūḥī, wa adhina lī bidhikrih.",
         "All praise is for Allah, who gave my body health, returned my soul to me and allowed me to remember Him.",
         "Tamam tareefein Allah ke liye hain jis ne mere jism ko aafiyat di, meri rooh mujhe wapas lautaayi aur mujhe apna zikr karne ki ijazat di.", "", "At-Tirmidhi (Hisn al-Muslim 3)"),
        k("Before sleeping"),
        ("Before sleeping (gratitude)", "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا، وَكَفَانَا، وَآوَانَا، فَكَمْ مِمَّنْ لاَ كَافِيَ لَهُ وَلاَ مُؤْوِيَ",
         "Alḥamdu lillāhil-ladhī aṭ`amanā wa saqānā wa kafānā wa āwānā, fakam mimman lā kāfiya lahū wa lā mu'wī.",
         "All praise is for Allah, who fed us, gave us drink, took care of our needs and gave us a home, for how many people have no one to care for them and no home.",
         "Tamam tareefein Allah ke liye hain jis ne hamein khilaya, pilaya, hamari zarooratein poori keen aur hamein thikana diya, kitne hi log hain jin ka na koi sahara hai na thikana.", "", "Sahih Muslim (Hisn al-Muslim 108)"),
        k("Before eating"),
        ("If you forget Bismillah before eating", "بسمِ اللَّهِ فِي أَوَّلِهِ وَآخِرِهِ", "Bismillāhi fī awwalihī wa ākhirih.",
         "In the name of Allah, at its beginning and at its end.", "Allah ke naam se, is ke shuru mein bhi aur aakhir mein bhi.", "", "Abu Dawud; At-Tirmidhi (Hisn al-Muslim 178)"),
        ("When given food", "اللَّهُمَّ بَارِكْ لَنَا فِيهِ وَأَطْعِمْنَا خَيْراً مِنْهُ", "Allāhumma bārik lanā fīhi wa aṭ`imnā khayran minh.",
         "O Allah, bless it for us and feed us with something better than it. (When given milk: Allāhumma bārik lanā fīhi wa zidnā minh, O Allah, bless it for us and give us more of it.)",
         "Ae Allah, hamare liye is mein barkat de aur hamein is se behtar khilaa. (Doodh milne par: Allahumma barik lana fihi wa zidna minh, ae Allah is mein barkat de aur hamein aur ata farma.)", "", "At-Tirmidhi (Hisn al-Muslim 179)"),
        k("After eating"),
        ("After eating (second dua)", "الْحَمْدُ للهِ حَمْداً كَثيراً طَيِّباً مُبارَكاً فيه، غَيْرَ مَكْفِيٍّ وَلا مُوَدَّعٍ وَلا مُسْتَغْنىً عَنْهُ رَبَّنا",
         "Alḥamdu lillāhi ḥamdan kathīran ṭayyiban mubārakan fīh, ghayra makfiyyin wa lā muwadda`in wa lā mustaghnan `anhu rabbanā.",
         "All praise is for Allah, much good and blessed praise, praise that never ends, is never abandoned and that we can never do without, our Lord.",
         "Tamam tareefein Allah ke liye hain, bahut zyada, paakeeza aur barkat wali tareef, jo na kabhi khatam ho, na chhori jaaye, aur jis se hum kabhi be-niyaz nahin, ae hamare Rab.", "", "Sahih al-Bukhari (Hisn al-Muslim 181)"),
        k("Before entering the toilet"), k("After leaving the toilet"),
        ("Before wudu", "بِسْمِ الله", "Bismillāh.", "In the name of Allah.", "Allah ke naam se.", "", "Abu Dawud; Ibn Majah (Hisn al-Muslim 12)"),
        k("After wudu"),
        k("When leaving home"),
        k("When getting dressed"),
        ("When taking off clothes", "بِسْمِ الله", "Bismillāh.", "In the name of Allah.", "Allah ke naam se.", "", "At-Tirmidhi (Hisn al-Muslim 9)"),
        k("When you sneeze"),
        k("When angry"),
        ("When something bad happens", "قَدَّرَ اللهُ وَما شاءَ فَعَل", "Qaddarallāhu wa mā shā'a fa`al.",
         "Allah has decreed it, and He does whatever He wills.", "Allah ne yahi muqaddar kiya, aur woh jo chahta hai karta hai.", "", "Sahih Muslim (Hisn al-Muslim 144)"),
        ("When getting into a car or bus", "بِسْمِ اللهِ", "Bismillāh.", "In the name of Allah. (See our travel duas page for the full journey dua.)",
         "Allah ke naam se. (Safar ki poori dua hamare travel duas page par dekhein.)", "", "Abu Dawud (Hisn al-Muslim 210)"),
    ]

    # ---------------- ANXIETY (complete) ----------------
    p = "duas-for-anxiety"
    PAGES[p]["items"] += [
        ("Asking Allah to set every affair right", "يا حَيُّ يا قَيّومُ بِرَحْمَتِكَ أَسْتَغيث ، أَصْلِحْ لي شَأْني كُلَّه ، وَلا تَكِلني إِلى نَفْسي طَرْفَةَ عَين",
         "Yā ḥayyu yā qayyūm, biraḥmatika astaghīth, aṣliḥ lī sha'nī kullah, wa lā takilnī ilā nafsī ṭarfata `ayn.",
         "O Ever-Living, O Sustainer of all, by Your mercy I call for help. Set all my affairs right, and do not leave me to myself even for the blink of an eye.",
         "Ae hamesha zinda rehne wale, ae sab ko qaim rakhne wale, Teri rehmat ke wasile se main madad mangta hoon. Mere saare kaam durust farma de, aur mujhe palak jhapakne ke barabar bhi mere nafs ke hawale na kar.", "", "Al-Hakim, graded authentic (Hisn al-Muslim 88)"),
        ("For fear, bad dreams and restlessness at night", "أَعوذُ بِكَلِماتِ اللّهِ التّامّاتِ مِن غَضَبِهِ وَعِقابِهِ وَشَرِّ عِبادِهِ وَمِنْ هَمَزاتِ الشَّياطينِ وَأَنْ يَحْضرون",
         "A`ūdhu bikalimātillāhit-tāmmāti min ghaḍabihī wa `iqābihī wa sharri `ibādih, wa min hamazātish-shayāṭīni wa an yaḥḍurūn.",
         "I seek protection in the perfect words of Allah from His anger and His punishment, from the evil of His servants, and from the whispers of the devils and from their coming near me.",
         "Main Allah ke mukammal kalimaat ki panah mangta hoon Us ke ghusse aur Us ki saza se, Us ke bandon ki buraai se, aur shaitanon ke waswason se aur is se ke woh mere paas aayen.", "", "Abu Dawud; At-Tirmidhi (Hisn al-Muslim 113)"),
        ("For debt and money worries", "اللّهُمَّ اكْفِني بِحَلالِكَ عَنْ حَرامِك، وَأَغْنِني بِفَضْلِكَ عَمَّنْ سِواك",
         "Allāhummak-finī biḥalālika `an ḥarāmik, wa aghninī bifaḍlika `amman siwāk.",
         "O Allah, make what is halal enough for me so that I need nothing haram, and by Your grace make me need no one but You.",
         "Ae Allah, apne halal ke zariye mujhe haram se bacha kar kaafi kar de, aur apne fazl se mujhe apne siwa har kisi se be-niyaz kar de.", "", "At-Tirmidhi (Hisn al-Muslim 136)"),
        ("When something bad happens", "قَدَّرَ اللهُ وَما شاءَ فَعَل", "Qaddarallāhu wa mā shā'a fa`al.",
         "Allah has decreed it, and He does whatever He wills.", "Allah ne yahi muqaddar kiya, aur woh jo chahta hai karta hai.", "", "Sahih Muslim (Hisn al-Muslim 144)"),
        ("When afraid of someone's harm", "اللّهُمَّ إِنَّا نَجْعَلُكَ في نُحورِهِم، وَنَعوذُ بِكَ مِنْ شُرورِهمْ",
         "Allāhumma innā naj`aluka fī nuḥūrihim, wa na`ūdhu bika min shurūrihim.",
         "O Allah, we place You before them, and we seek Your protection from their evil.",
         "Ae Allah, hum Tujhe un ke muqable mein rakhte hain aur un ki buraiyon se Teri panah mangte hain.", "", "Abu Dawud (Hisn al-Muslim 126)"),
    ]

    # ---------------- ILLNESS (complete) ----------------
    p = "duas-for-illness"
    PAGES[p]["items"] += [
        ("Blowing the 3 Quls over yourself when ill", QULS, "Recite Surah Al-Ikhlas, Al-Falaq and An-Nas, blow lightly into your hands and wipe them over your body.",
         "When the Prophet, peace be upon him, was ill, he would recite the last three surahs, blow lightly into his hands and wipe them over his body.",
         "Jab Nabi ﷺ beemar hote to aakhri teen surtein parh kar apne haathon par halka sa phoonkte aur unhein apne jism par pher lete.", "3", "Sahih al-Bukhari 5016; Sahih Muslim 2192"),
        ("When someone is very ill", "اللّهُمَّ اغْفِرْ لي وَارْحَمْني وَأَلْحِقْني بِالرَّفيقِ الأَعْلى",
         "Allāhummaghfir lī warḥamnī wa alḥiqnī bir-rafīqil-a`lā.",
         "O Allah, forgive me, have mercy on me and join me with the highest companions (in Paradise).",
         "Ae Allah, mujhe bakhsh de, mujh par reham farma aur mujhe sab se buland saathiyon (jannat walon) ke saath mila de.", "", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 150)"),
    ]

    # ---------------- JANAZA (complete) ----------------
    p = "janaza-and-mayyat-duas"
    j = lambda w: old(p, w)
    PAGES[p]["items"] = [
        ("Helping someone near death say the shahada", "لا إله إلا الله", "Lā ilāha illallāh.",
         "Gently remind the dying person to say La ilaha illallah. The Prophet, peace be upon him, said whoever's last words are La ilaha illallah will enter Paradise.",
         "Qareeb-ul-marg shakhs ko narmi se La ilaha illallah ki yaad dilayein. Nabi ﷺ ne farmaya jis ka aakhri kalaam La ilaha illallah ho woh jannat mein daakhil hoga.", "", "Abu Dawud (Hisn al-Muslim 153)"),
        j("When you hear of a death or calamity"),
        ("When closing the eyes of the deceased", "اللَّهُمَّ اغْفِرْ لِفلان (باسمه) وَارْفَعْ دَرَجَتَهُ في المَهْدِيين ، وَاخْلُفْهُ في عَقِبِهِ في الغابِرين، وَاغْفِرْ لَنا وَلَهُ يا رَبَّ العالَمين، وَافْسَحْ لَهُ في قَبْرِهِ وَنَوِّرْ لَهُ فيه",
         "Allāhummaghfir li (name), warfa` darajatahū fil-mahdiyyīn, wakhlufhu fī `aqibihī fil-ghābirīn, waghfir lanā wa lahū yā rabbal-`ālamīn, wafsaḥ lahū fī qabrihī wa nawwir lahū fīh.",
         "O Allah, forgive (name) and raise their rank among the guided. Take care of the family they leave behind. Forgive us and them, O Lord of the worlds. Make their grave spacious and fill it with light.",
         "Ae Allah, (naam) ko bakhsh de, hidayat yafta logon mein is ka darja buland farma, is ke peeche reh jaane walon ki dekh bhaal farma, hamein aur ise bakhsh de ae Rabbul Aalameen, is ki qabr ko kushada kar de aur us mein roshni kar de.", "", "Sahih Muslim (Hisn al-Muslim 155)"),
        j("In the funeral prayer (for the deceased)"),
        j("For all the living and the dead"),
        ("In the funeral prayer (under Allah's protection)", "اللَّهُمَّ إِنَّ فُلانَ بْنَ فُلانٍ في ذِمَّتِك ، وَحَبْلِ جِوارِك ، فَقِهِ مِنْ فِتْنَةِ الْقَبْرِ وَعَذابِ النّار ، وَأَنْتَ أَهْلُ الْوَفاءِ وَالْحَقِّ ، فَاغْفِرْ لَهُ وَارْحَمْهُ ، إِنَّكَ أَنْتَ الغَفورُ الرَّحيم",
         "Allāhumma inna (name) fī dhimmatik wa ḥabli jiwārik, faqihi min fitnatil-qabri wa `adhābin-nār, wa anta ahlul-wafā'i wal-ḥaqq, faghfir lahū warḥamh, innaka antal-ghafūrur-raḥīm.",
         "O Allah, (name) is under Your protection and in Your care, so save them from the trial of the grave and the punishment of the Fire. You always keep Your promise and You are the Truth, so forgive them and have mercy on them. You are the Forgiving, the Merciful.",
         "Ae Allah, (naam) Teri zimmedari aur Teri panah mein hai, pas ise qabr ke fitne aur aag ke azaab se bacha. Tu waada poora karne wala aur haq wala hai, pas ise bakhsh de aur is par reham farma. Beshak Tu bakhshne wala, reham karne wala hai.", "", "Abu Dawud; Ibn Majah (Hisn al-Muslim 158)"),
        ("In the funeral prayer (Allah's servant needs Your mercy)", "اللَّهُمَّ عَبْدُكَ وَابْنُ أَمَتِك، احْتاجَ إِلى رَحْمَتِك، وَأَنْتَ غَنِيٌّ عَنْ عَذابِه، إِنْ كانَ مُحْسِناً فَزِدْ في حَسَناتِه، وَإِنْ كانَ مُسيئاً فَتَجاوَزْ عَنْه",
         "Allāhumma `abduka wabnu amatik, iḥtāja ilā raḥmatik, wa anta ghaniyyun `an `adhābih, in kāna muḥsinan fazid fī ḥasanātih, wa in kāna musī'an fatajāwaz `anh.",
         "O Allah, Your servant, the son of Your maidservant, needs Your mercy, and You have no need to punish him. If he did good, increase his good deeds, and if he did wrong, overlook it.",
         "Ae Allah, Tera banda aur Teri bandi ka beta Teri rehmat ka mohtaaj hai, aur Tu ise azaab dene se be-niyaz hai. Agar yeh neki karne wala tha to is ki nekiyon mein izafa farma, aur agar ghalti karne wala tha to is se dar-guzar farma.", "", "Al-Hakim, graded authentic (Hisn al-Muslim 159)"),
        j("Comforting the family (condolence)"),
        j("When placing the deceased in the grave"),
        ("After the burial", "اللَّهُمَّ اغْفِرْ لَهُ اللَّهُمَّ ثَبِّتْهُ", "Allāhummaghfir lah, Allāhumma thabbit-h.",
         "O Allah, forgive him. O Allah, make him firm. After a burial the Prophet, peace be upon him, would stand and tell the people to ask forgiveness for their brother and ask Allah to make him firm, for he is now being questioned.",
         "Ae Allah, ise bakhsh de. Ae Allah, ise saabit qadam rakh. Dafan ke baad Nabi ﷺ thehar kar farmate ke apne bhai ke liye maghfirat aur saabit qadmi ki dua karo kyunke ab is se sawal ho raha hai.", "", "Abu Dawud (Hisn al-Muslim 164)"),
        j("When visiting the graves"),
        j("For the believers who passed before us"),
    ]

    # ---------------- NIKAH ----------------
    p = "nikah-dua"
    PAGES[p]["items"].insert(2, ("For husband and wife (in private)", "بِسْمِ الله اللّهُمَّ جَنِّبْنا الشَّيْطانَ، وَجَنِّبِ الشَّيْطانَ ما رَزَقْتَنا",
        "Bismillāh. Allāhumma jannibnash-shayṭān, wa jannibish-shayṭāna mā razaqtanā.",
        "In the name of Allah. O Allah, keep Shaytan away from us, and keep Shaytan away from what You bless us with (our children).",
        "Allah ke naam se. Ae Allah, hamein Shaitan se door rakh, aur jo (aulad) Tu hamein ata kare use bhi Shaitan se door rakh.", "", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 192)"))

    # ---------------- NEW CLOTHES ----------------
    p = "new-clothes-dua"
    PAGES[p]["items"] += [
        ("Another dua for someone in new clothes", "اِلبَس جَديداً وَعِشْ حَميداً وَمُتْ شهيداً", "Ilbas jadīdan, wa `ish ḥamīdan, wa mut shahīdā.",
         "Wear new clothes, live a praiseworthy life and die as a martyr.", "Naye kapde pehno, qabil-e-tareef zindagi guzaro aur shahadat ki maut pao.", "", "Ibn Majah (Hisn al-Muslim 8)"),
        ("When taking off clothes", "بِسْمِ الله", "Bismillāh.", "In the name of Allah.", "Allah ke naam se.", "", "At-Tirmidhi (Hisn al-Muslim 9)"),
    ]

    # ---------------- MAGHFIRAT ----------------
    p = "maghfirat-duas"
    PAGES[p]["items"][2:2] = [
        ("Istighfar that forgives even great sins", "أَسْتَغْفِرُ اللَّهَ الْعَظيمَ الَّذِي لاَ إِلَهَ إِلاَّ هُوَ الْحَيُّ القَيّوُمُ وَأَتُوبُ إِلَيهِ",
         "Astaghfirullāhal-`aẓīmal-ladhī lā ilāha illā huwal-ḥayyul-qayyūmu wa atūbu ilayh.",
         "I ask forgiveness of Allah the Mighty, besides whom there is no god, the Ever-Living, the Sustainer of all, and I turn to Him in repentance. The Prophet, peace be upon him, said Allah forgives whoever says this, even if they had fled from the battlefield.",
         "Main azmat wale Allah se maghfirat mangta hoon jis ke siwa koi mabood nahin, jo hamesha zinda aur sab ko qaim rakhne wala hai, aur Usi ki taraf tauba karta hoon.", "", "Abu Dawud; At-Tirmidhi (Hisn al-Muslim 250)"),
        ("The dua taught to Abu Bakr", "اللّهُمَّ إِنِّي ظَلَمْتُ نَفْسي ظُلْماً كَثيراً وَلا يَغْفِرُ الذُّنوبَ إِلاّ أَنْت، فَاغْفِر لي مَغْفِرَةً مِنْ عِنْدِك وَارْحَمْني، إِنَّكَ أَنْتَ الغَفورُ الرَّحيم",
         "Allāhumma innī ẓalamtu nafsī ẓulman kathīran wa lā yaghfirudh-dhunūba illā ant, faghfir lī maghfiratan min `indika warḥamnī, innaka antal-ghafūrur-raḥīm.",
         "O Allah, I have wronged myself greatly, and none forgives sins except You. So grant me forgiveness from Yourself and have mercy on me. You are the Forgiving, the Merciful.",
         "Ae Allah, main ne apne aap par bahut zulm kiya, aur Tere siwa koi gunah maaf nahin karta. Pas apni taraf se mujhe bakhsh de aur mujh par reham farma. Beshak Tu bakhshne wala, reham karne wala hai.", "", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 57)"),
        ("Asking for complete forgiveness", "اللّهُمَّ اغْفِرْ لي ما قَدَّمْتُ وَما أَخَّرْت ، وَما أَسْرَرْتُ وَما أَعْلَنْت ، وَما أَسْرَفْت ، وَما أَنْتَ أَعْلَمُ بِهِ مِنِّي . أَنْتَ المُقَدِّمُ، وَأَنْتَ المُؤَخِّرُ لا إِلهَ إِلاّ أَنْت",
         "Allāhummaghfir lī mā qaddamtu wa mā akhkhartu, wa mā asrartu wa mā a`lantu, wa mā asraftu, wa mā anta a`lamu bihī minnī, antal-muqaddimu wa antal-mu'akhkhiru, lā ilāha illā ant.",
         "O Allah, forgive me what I did before and what I left for later, what I did in secret and what I did openly, what I did in excess, and what You know better than I do. You bring forward and You put back. There is no god but You.",
         "Ae Allah, mere agle aur pichhle gunah, chhup kar aur khule kiye hue gunah, meri zyadtiyan aur woh sab maaf farma jo Tu mujh se zyada jaanta hai. Tu hi aage karne wala aur peeche karne wala hai, Tere siwa koi mabood nahin.", "", "Sahih Muslim (Hisn al-Muslim 58)"),
    ]
    PAGES[p]["items"] += [
        ("In the last ten nights of Ramadan", "اللَّهُمَّ إِنَّكَ عَفُوٌّ كَرِيمٌ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي", "Allāhumma innaka `afuwwun karīmun tuḥibbul-`afwa fa`fu `annī.",
         "O Allah, You are Most Forgiving and Generous, You love to forgive, so forgive me.", "Ae Allah, Tu bahut maaf karne wala aur karam wala hai, maaf karna pasand karta hai, pas mujhe maaf farma de.", "", "At-Tirmidhi 3513, graded sahih"),
    ]

    # ---------------- RAMADAN ----------------
    p = "ramadan-duas"
    PAGES[p]["items"].insert(2, ("At iftar (asking for forgiveness)", "اللّهُمَّ إِنِّي أَسْأَلُكَ بِرَحْمَتِكَ الّتي وَسِعَت كُلَّ شيء، أَنْ تَغْفِرَ لي",
        "Allāhumma innī as'aluka biraḥmatikal-latī wasi`at kulla shay'in an taghfira lī.",
        "O Allah, I ask You by Your mercy, which embraces all things, to forgive me. (A dua of Abdullah ibn Amr at iftar.)",
        "Ae Allah, main Teri us rehmat ke wasile se jo har cheez par chhaayi hui hai, Tujh se sawal karta hoon ke mujhe bakhsh de.", "", "Ibn Majah, graded hasan by Ibn Hajar (Hisn al-Muslim 177)"))

    # ---------------- RABBANA: full 40 ----------------
    p = "rabbana-duas"
    R = [
        ("2:127 · Accept from us", Q(2, 127, 7), "Rabbanā taqabbal minnā innaka antas-samī`ul-`alīm.", "Our Lord, accept this from us. You are the All-Hearing, the All-Knowing.", "Ae hamare Rab, ham se qabool farma, beshak Tu sab kuch sunne wala, jaanne wala hai."),
        ("2:128 · Make us Muslims to You", Q(2, 128, 0), "Rabbanā waj`alnā muslimayni laka wa min dhurriyyatinā ummatan muslimatan lak, wa arinā manāsikanā wa tub `alaynā, innaka antat-tawwābur-raḥīm.", "Our Lord, make us submissive to You and make from our descendants a nation submissive to You. Show us our ways of worship and accept our repentance. You are the Accepter of repentance, the Merciful.", "Ae hamare Rab, hamein apna farmanbardar bana aur hamari aulad mein se bhi ek farmanbardar ummat bana, hamein ibadat ke tareeqe dikha aur hamari tauba qabool farma, beshak Tu tauba qabool karne wala, reham karne wala hai."),
        ("2:201 · Good in this world and the next", Q(2, 201, 3), "Rabbanā ātinā fid-dunyā ḥasanatan wa fil-ākhirati ḥasanatan wa qinā `adhāban-nār.", "Our Lord, give us good in this world and good in the Hereafter, and protect us from the punishment of the Fire.", "Ae hamare Rab, hamein duniya mein bhi bhalai de aur aakhirat mein bhi bhalai de, aur hamein aag ke azaab se bacha."),
        ("2:250 · Patience and firm feet", Q(2, 250, 5), "Rabbanā afrigh `alaynā ṣabran wa thabbit aqdāmanā wanṣurnā `alal-qawmil-kāfirīn.", "Our Lord, pour patience upon us, make our feet firm and help us against the disbelieving people.", "Ae hamare Rab, ham par sabr undel de, hamare qadam jama de aur kafir qaum ke muqable mein hamari madad farma."),
        ("2:286 · Do not take us to task if we forget", Q(2, 286, 12, 18), "Rabbanā lā tu'ākhidhnā in nasīnā aw akhṭa'nā.", "Our Lord, do not take us to task if we forget or make a mistake.", "Ae hamare Rab, agar ham bhool jaayen ya ghalti kar baithen to ham par giraft na farma."),
        ("2:286 · Do not place a heavy burden on us", Q(2, 286, 19, 29), "Rabbanā wa lā taḥmil `alaynā iṣran kamā ḥamaltahū `alal-ladhīna min qablinā.", "Our Lord, do not place on us a burden like the one You placed on those before us.", "Ae hamare Rab, ham par aisa bojh na daal jaisa Tu ne ham se pehle logon par daala."),
        ("2:286 · Do not burden us beyond our strength", Q(2, 286, 30), "Rabbanā wa lā tuḥammilnā mā lā ṭāqata lanā bih, wa`fu `annā waghfir lanā warḥamnā, anta mawlānā fanṣurnā `alal-qawmil-kāfirīn.", "Our Lord, do not burden us with more than we can bear. Pardon us, forgive us and have mercy on us. You are our Protector, so help us against the disbelieving people.", "Ae hamare Rab, ham par itna bojh na daal jis ki hamein taaqat nahin. Hamein maaf farma, bakhsh de aur ham par reham farma. Tu hi hamara Maula hai, pas kafir qaum ke muqable mein hamari madad farma."),
        ("3:8 · Keep our hearts steady", Q(3, 8, 0), "Rabbanā lā tuzigh qulūbanā ba`da idh hadaytanā wa hab lanā min ladunka raḥmah, innaka antal-wahhāb.", "Our Lord, do not let our hearts turn away after You have guided us, and grant us mercy from Yourself. You are the Giver.", "Ae hamare Rab, hidayat dene ke baad hamare dilon ko tedha na kar, aur hamein apne paas se rehmat ata farma. Beshak Tu hi bahut dene wala hai."),
        ("3:9 · You will gather all people", Q(3, 9, 0), "Rabbanā innaka jāmi`un-nāsi liyawmin lā rayba fīh, innallāha lā yukhliful-mī`ād.", "Our Lord, You will surely gather all people on a Day about which there is no doubt. Allah never breaks His promise.", "Ae hamare Rab, beshak Tu tamam logon ko us din jama karne wala hai jis mein koi shak nahin. Beshak Allah waade ke khilaf nahin karta."),
        ("3:16 · We believe, so forgive us", Q(3, 16, 2), "Rabbanā innanā āmannā faghfir lanā dhunūbanā wa qinā `adhāban-nār.", "Our Lord, we have believed, so forgive us our sins and protect us from the punishment of the Fire.", "Ae hamare Rab, ham imaan laaye, pas hamare gunah maaf farma aur hamein aag ke azaab se bacha."),
        ("3:53 · Write us among the witnesses", Q(3, 53, 0), "Rabbanā āmannā bimā anzalta wattaba`nar-rasūla faktubnā ma`ash-shāhidīn.", "Our Lord, we believe in what You have sent down and we follow the Messenger, so write us among those who bear witness.", "Ae hamare Rab, ham us par imaan laaye jo Tu ne utaara aur ham ne Rasool ki pairwi ki, pas hamein gawahi dene walon mein likh le."),
        ("3:147 · Forgive our sins and excesses", Q(3, 147, 6), "Rabbanaghfir lanā dhunūbanā wa isrāfanā fī amrinā wa thabbit aqdāmanā wanṣurnā `alal-qawmil-kāfirīn.", "Our Lord, forgive us our sins and our excesses in our affairs, make our feet firm and help us against the disbelieving people.", "Ae hamare Rab, hamare gunah aur hamare kaamon mein zyadtiyan maaf farma, hamare qadam jama de aur kafir qaum ke muqable mein hamari madad farma."),
        ("3:191 · You did not create this in vain", Q(3, 191, 12), "Rabbanā mā khalaqta hādhā bāṭilā, subḥānaka faqinā `adhāban-nār.", "Our Lord, You did not create all this without purpose. Glory be to You, so protect us from the punishment of the Fire.", "Ae hamare Rab, Tu ne yeh sab bekaar paida nahin kiya. Tu paak hai, pas hamein aag ke azaab se bacha."),
        ("3:192 · Save us from the Fire", Q(3, 192, 0), "Rabbanā innaka man tudkhilin-nāra faqad akhzaytah, wa mā liẓ-ẓālimīna min anṣār.", "Our Lord, whoever You admit into the Fire, You have truly disgraced, and the wrongdoers will have no helpers.", "Ae hamare Rab, jise Tu ne aag mein daakhil kiya use Tu ne ruswa kar diya, aur zalimon ka koi madadgaar nahin."),
        ("3:193 · We heard the caller to faith", Q(3, 193, 0, 9), "Rabbanā innanā sami`nā munādiyan yunādī lil-īmāni an āminū birabbikum fa-āmannā.", "Our Lord, we heard a caller calling to faith, saying, 'Believe in your Lord,' and we believed.", "Ae hamare Rab, ham ne ek pukaarne wale ko suna jo imaan ki taraf bula raha tha ke apne Rab par imaan lao, to ham imaan le aaye."),
        ("3:193 · Let us die among the righteous", Q(3, 193, 10), "Rabbanā faghfir lanā dhunūbanā wa kaffir `annā sayyi'ātinā wa tawaffanā ma`al-abrār.", "Our Lord, forgive our sins, remove our bad deeds from us and let us die among the righteous.", "Ae hamare Rab, hamare gunah maaf farma, hamari buraiyan mita de aur hamein nek logon ke saath maut de."),
        ("3:194 · Give us what You promised", Q(3, 194, 0), "Rabbanā wa ātinā mā wa`attanā `alā rusulika wa lā tukhzinā yawmal-qiyāmah, innaka lā tukhliful-mī`ād.", "Our Lord, give us what You promised us through Your messengers, and do not disgrace us on the Day of Resurrection. You never break Your promise.", "Ae hamare Rab, hamein woh ata farma jis ka Tu ne apne Rasoolon ke zariye waada kiya, aur hamein qayamat ke din ruswa na kar. Beshak Tu waada khilafi nahin karta."),
        ("5:83 · Write us among the witnesses", Q(5, 83, 16), "Rabbanā āmannā faktubnā ma`ash-shāhidīn.", "Our Lord, we believe, so write us among those who bear witness.", "Ae hamare Rab, ham imaan laaye, pas hamein gawahi dene walon mein likh le."),
        ("5:114 · The dua of Isa for provision", Q(5, 114, 4), "Allāhumma rabbanā anzil `alaynā mā'idatan minas-samā'i takūnu lanā `īdan li-awwalinā wa ākhirinā wa āyatan mink, warzuqnā wa anta khayrur-rāziqīn.", "O Allah, our Lord, send down to us a table spread with food from the sky, to be a celebration for the first and last of us and a sign from You. Provide for us; You are the best of providers.", "Ae Allah, hamare Rab, ham par aasman se khane ka dastarkhwan utaar jo hamare aglon aur pichhlon ke liye eid ho aur Teri taraf se ek nishani ho, aur hamein rizq de, Tu sab se behtar rizq dene wala hai."),
        ("7:23 · The dua of Adam and Hawwa", Q(7, 23, 1), "Rabbanā ẓalamnā anfusanā wa il lam taghfir lanā wa tarḥamnā lanakūnanna minal-khāsirīn.", "Our Lord, we have wronged ourselves. If You do not forgive us and have mercy on us, we will surely be among the losers.", "Ae hamare Rab, ham ne apne aap par zulm kiya. Agar Tu ne hamein maaf na kiya aur ham par reham na kiya to ham zaroor nuqsan uthane walon mein se ho jaayenge."),
        ("7:47 · Do not place us with the wrongdoers", Q(7, 47, 7), "Rabbanā lā taj`alnā ma`al-qawmiẓ-ẓālimīn.", "Our Lord, do not place us with the wrongdoing people.", "Ae hamare Rab, hamein zalim logon ke saath na kar."),
        ("7:89 · Judge between us with truth", Q(7, 89, 33), "Rabbanaftaḥ baynanā wa bayna qawminā bil-ḥaqqi wa anta khayrul-fātiḥīn.", "Our Lord, decide between us and our people with truth. You are the best of those who decide.", "Ae hamare Rab, hamare aur hamari qaum ke darmiyan haq ke saath faisla farma, aur Tu sab se behtar faisla karne wala hai."),
        ("7:126 · Pour patience upon us", Q(7, 126, 10), "Rabbanā afrigh `alaynā ṣabran wa tawaffanā muslimīn.", "Our Lord, pour patience upon us and let us die as Muslims.", "Ae hamare Rab, ham par sabr undel de aur hamein Musalman hone ki haalat mein maut de."),
        ("10:85-86 · Do not make us a trial", [Q(10, 85, 4), Q(10, 86, 0)], "Rabbanā lā taj`alnā fitnatan lil-qawmiẓ-ẓālimīn, wa najjinā biraḥmatika minal-qawmil-kāfirīn.", "Our Lord, do not make us a trial for the wrongdoing people, and by Your mercy save us from the disbelieving people.", "Ae hamare Rab, hamein zalim qaum ke liye aazmaish na bana, aur apni rehmat se hamein kafir qaum se nijaat de."),
        ("14:38 · You know what we hide", Q(14, 38, 0), "Rabbanā innaka ta`lamu mā nukhfī wa mā nu`lin, wa mā yakhfā `alallāhi min shay'in fil-arḍi wa lā fis-samā'.", "Our Lord, You know what we hide and what we show. Nothing on earth or in the heavens is hidden from Allah.", "Ae hamare Rab, Tu jaanta hai jo ham chhupate hain aur jo zaahir karte hain, aur Allah se zameen aur aasman mein koi cheez chhupi nahin."),
        ("14:40 · Make me steadfast in prayer", Q(14, 40, 0), "Rabbij`alnī muqīmaṣ-ṣalāti wa min dhurriyyatī, rabbanā wa taqabbal du`ā'.", "My Lord, make me steadfast in prayer, and my children too. Our Lord, accept my dua.", "Ae mere Rab, mujhe aur meri aulad ko namaz qaim karne wala bana. Ae hamare Rab, meri dua qabool farma."),
        ("14:41 · Forgive me and my parents", Q(14, 41, 0), "Rabbanaghfir lī wa liwālidayya wa lil-mu'minīna yawma yaqūmul-ḥisāb.", "Our Lord, forgive me, my parents and the believers on the Day the reckoning takes place.", "Ae hamare Rab, mujhe, mere walidain ko aur sab momino ko us din bakhsh de jis din hisaab qaim hoga."),
        ("18:10 · Mercy and guidance", Q(18, 10, 6), "Rabbanā ātinā min ladunka raḥmatan wa hayyi' lanā min amrinā rashadā.", "Our Lord, grant us mercy from Yourself and guide us rightly in our affair.", "Ae hamare Rab, hamein apne paas se rehmat ata farma aur hamare kaam mein hamare liye rehnumai ka saman kar de."),
        ("20:45 · When afraid", Q(20, 45, 1), "Rabbanā innanā nakhāfu an yafruṭa `alaynā aw an yaṭghā.", "Our Lord, we fear that he will rush to harm us or act wickedly.", "Ae hamare Rab, hamein dar hai ke woh ham par zyadti kare ya sarkashi kare."),
        ("23:109 · We believe, so forgive us", Q(23, 109, 6), "Rabbanā āmannā faghfir lanā warḥamnā wa anta khayrur-rāḥimīn.", "Our Lord, we believe, so forgive us and have mercy on us. You are the best of those who show mercy.", "Ae hamare Rab, ham imaan laaye, pas hamein bakhsh de aur ham par reham farma, aur Tu sab se behtar reham karne wala hai."),
        ("25:65-66 · Turn away the punishment of Hell", [Q(25, 65, 2), Q(25, 66, 0)], "Rabbanaṣrif `annā `adhāba jahannam, inna `adhābahā kāna gharāmā, innahā sā'at mustaqarran wa muqāmā.", "Our Lord, turn away from us the punishment of Hell. Its punishment is lasting torment; it is a terrible place to stay and to live.", "Ae hamare Rab, jahannam ka azaab ham se pher de, beshak us ka azaab chimat jaane wala hai, beshak woh bura thikana aur buri jagah hai."),
        ("25:74 · A happy family", Q(25, 74, 2), "Rabbanā hab lanā min azwājinā wa dhurriyyātinā qurrata a`yunin waj`alnā lil-muttaqīna imāmā.", "Our Lord, grant us from our spouses and our children the coolness of our eyes, and make us leaders for the righteous.", "Ae hamare Rab, hamein hamare jeewan saathiyon aur aulad se aankhon ki thandak ata farma, aur hamein parhezgaron ka imam bana."),
        ("40:7 · The angels' dua for the believers", Q(40, 7, 13), "Rabbanā wasi`ta kulla shay'in raḥmatan wa `ilman faghfir lil-ladhīna tābū wattaba`ū sabīlaka wa qihim `adhābal-jaḥīm.", "Our Lord, You embrace all things in mercy and knowledge, so forgive those who repent and follow Your way, and protect them from the punishment of Hellfire.", "Ae hamare Rab, Tu ne har cheez ko rehmat aur ilm mein gher rakha hai, pas un ko bakhsh de jinhon ne tauba ki aur Tere raaste par chale, aur unhein jahannam ke azaab se bacha."),
        ("40:8 · Admit them to the Gardens of Eden", Q(40, 8, 0), "Rabbanā wa adkhilhum jannāti `adninil-latī wa`attahum wa man ṣalaḥa min ābā'ihim wa azwājihim wa dhurriyyātihim, innaka antal-`azīzul-ḥakīm.", "Our Lord, admit them into the Gardens of Eden You promised them, along with the righteous among their parents, spouses and children. You are the Mighty, the Wise.", "Ae hamare Rab, unhein hamesha rehne wali jannaton mein daakhil farma jin ka Tu ne un se waada kiya, aur un ke baap daada, biwiyon aur aulad mein se nek logon ko bhi. Beshak Tu ghalib, hikmat wala hai."),
        ("40:9 · Protect them from evil deeds", Q(40, 9, 0), "Wa qihimus-sayyi'āt, wa man taqis-sayyi'āti yawma'idhin faqad raḥimtah, wa dhālika huwal-fawzul-`aẓīm.", "And protect them from evil deeds. Whoever You protect from evil on that Day, You have truly shown mercy, and that is the great success.", "Aur unhein buraiyon se bacha. Jise Tu us din buraiyon se bacha le us par Tu ne reham farmaya, aur yahi bari kaamyabi hai."),
        ("59:10 · For the believers before us", Q(59, 10, 5, 11), "Rabbanaghfir lanā wa li-ikhwāninal-ladhīna sabaqūnā bil-īmān.", "Our Lord, forgive us and our brothers who came before us in faith.", "Ae hamare Rab, hamein aur hamare un bhaiyon ko bakhsh de jo ham se pehle imaan laaye."),
        ("59:10 · No ill feeling in our hearts", Q(59, 10, 12), "Wa lā taj`al fī qulūbinā ghillan lil-ladhīna āmanū, rabbanā innaka ra'ūfur-raḥīm.", "And do not put any ill feeling in our hearts towards those who believe. Our Lord, You are Kind and Merciful.", "Aur hamare dilon mein imaan walon ke liye koi keena na rakh. Ae hamare Rab, beshak Tu bahut shafqat wala, reham wala hai."),
        ("60:4 · Upon You we rely", Q(60, 4, 45), "Rabbanā `alayka tawakkalnā wa ilayka anabnā wa ilaykal-maṣīr.", "Our Lord, in You we put our trust, to You we turn, and to You is the final return.", "Ae hamare Rab, ham ne Tujh par bharosa kiya, Teri taraf rujoo kiya aur Teri hi taraf laut kar jaana hai."),
        ("60:5 · Do not make us a trial for disbelievers", Q(60, 5, 0), "Rabbanā lā taj`alnā fitnatan lil-ladhīna kafarū waghfir lanā rabbanā, innaka antal-`azīzul-ḥakīm.", "Our Lord, do not make us a trial for those who disbelieve, and forgive us, our Lord. You are the Mighty, the Wise.", "Ae hamare Rab, hamein kafiron ke liye aazmaish na bana aur hamein bakhsh de, ae hamare Rab. Beshak Tu ghalib, hikmat wala hai."),
        ("66:8 · Complete our light", Q(66, 8, 34), "Rabbanā atmim lanā nūranā waghfir lanā, innaka `alā kulli shay'in qadīr.", "Our Lord, complete our light for us and forgive us. You have power over all things.", "Ae hamare Rab, hamara noor hamare liye poora kar de aur hamein bakhsh de, beshak Tu har cheez par qadir hai."),
    ]
    rabbana = [(w, ar, tr, en, ur, "", "Quran " + w.split(" ·")[0]) for (w, ar, tr, en, ur) in R]
    rabbi = [it for it in PAGES[p]["items"] if it[6] in ("Quran 17:24", "Quran 20:25-28", "Quran 20:114", "Quran 23:118", "Quran 28:24")]
    rabbi = [("Rabbi · " + it[0], *it[1:]) for it in rabbi]
    PAGES[p]["items"] = rabbana + rabbi
    PAGES[p]["title"] = "40 Rabbana Duas from the Quran with Meaning (English & Urdu)"
    PAGES[p]["desc"] = "All 40 Rabbana duas from the Quran in Arabic (Uthmani text) with transliteration, meaning in English and Roman Urdu, and the surah and ayah, plus the Rabbi duas of the Prophets."
    PAGES[p]["h1"] = '40 Rabbana Duas <span class="gold">from the Quran</span>'
    PAGES[p]["card"] = "All 40 Rabbana duas, plus the Rabbi duas of the Prophets."

    # ---------------- NEW PAGES ----------------
    PAGES["sleeping-duas"] = dict(
        title="Duas Before Sleeping (Sone ki Dua) with Meaning",
        desc="Every authentic dua and dhikr before sleeping: the 3 Quls, Ayatul Kursi, the last two verses of Al-Baqarah, Bismika Allahumma and more, with meaning in English and Roman Urdu.",
        h1='Duas Before <span class="gold">Sleeping</span>', ar_title="أَذْكَارُ النَّوْم", eyebrow="A Peaceful Night", card="The 3 Quls, Ayatul Kursi, Bismika Allahumma and more.",
        intro="The Prophet, peace be upon him, never went to sleep without remembering Allah. These are the authentic duas and azkar he taught for bedtime. Make wudu, lie on your right side and read as many as you can. Children can start with Bismika Allahumma and the 3 Quls.",
        items=[
            ("Blow the 3 Quls into your hands (3 times)", QULS, "Cup your hands, blow lightly into them, recite Al-Ikhlas, Al-Falaq and An-Nas, then wipe your hands over as much of your body as you can, starting with your head and face. Do this three times.",
             "The Prophet, peace be upon him, did this every night before sleeping.", "Nabi ﷺ har raat sone se pehle aisa karte: haath jod kar un mein halka phoonkte, teenon Qul parhte, phir haath sar, chehre aur jism par pherte. Teen baar.", "3", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 99)"),
            ("Ayatul Kursi", Q(2, 255, 0), "Allāhu lā ilāha illā huwal-ḥayyul-qayyūm... (see full text on our Ayatul Kursi page)",
             "Whoever reads Ayatul Kursi when going to bed will have a guardian from Allah all night, and no devil will come near them until morning.",
             "Jo sote waqt Ayatul Kursi parhe us par Allah ki taraf se saari raat ek nigehbaan rehta hai aur subah tak Shaitan us ke qareeb nahin aata.", "1", "Sahih al-Bukhari (Hisn al-Muslim 100)"),
            ("The last two verses of Surah Al-Baqarah", [Q(2, 285, 0), Q(2, 286, 0)], "Āmanar-rasūlu bimā unzila ilayhi mir-rabbihī wal-mu'minūn... (to the end of the surah)",
             "Whoever recites the last two verses of Surah Al-Baqarah at night, they will be enough for them.",
             "Jo raat ko Surah Baqarah ki aakhri do aayatein parhe, woh us ke liye kaafi ho jaati hain.", "1", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 101)"),
            ("In Your name I lie down", "بِاسْمِكَ رَبِّي وَضَعْتُ جَنْبِي، وَبِكَ أَرْفَعُهُ، فَإِن أَمْسَكْتَ نَفْسِي فارْحَمْهَا، وَإِنْ أَرْسَلْتَهَا فَاحْفَظْهَا بِمَا تَحْفَظُ بِهِ عِبَادَكَ الصَّالِحِينَ",
             "Bismika rabbī waḍa`tu janbī wa bika arfa`uh, fa-in amsakta nafsī farḥamhā, wa in arsaltahā faḥfaẓhā bimā taḥfaẓu bihī `ibādakaṣ-ṣāliḥīn.",
             "In Your name, my Lord, I lie down and in Your name I rise. If You take my soul, have mercy on it, and if You send it back, protect it as You protect Your righteous servants.",
             "Ae mere Rab, Tere naam se main ne apna pehlu rakha aur Tere hi naam se use uthaunga. Agar Tu meri rooh rok le to us par reham farma, aur agar wapas bhej de to us ki aise hifazat farma jaise Tu apne nek bandon ki hifazat karta hai.", "", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 102)"),
            ("You created my soul", "اللَّهُمَّ إِنَّكَ خَلَقْتَ نَفْسِي وَأَنْتَ تَوَفَّاهَا، لَكَ مَمَاتُهَا وَمَحْياهَا، إِنْ أَحْيَيْتَهَا فَاحْفَظْهَا، وَإِنْ أَمَتَّهَا فَاغْفِرْ لَهَا. اللَّهُمَّ إِنِّي أَسْأَلُكَ العَافِيَةَ",
             "Allāhumma innaka khalaqta nafsī wa anta tawaffāhā, laka mamātuhā wa maḥyāhā, in aḥyaytahā faḥfaẓhā, wa in amattahā faghfir lahā. Allāhumma innī as'alukal-`āfiyah.",
             "O Allah, You created my soul and You will take it. Its death and its life belong to You. If You keep it alive, protect it, and if You cause it to die, forgive it. O Allah, I ask You for wellbeing.",
             "Ae Allah, Tu ne meri jaan paida ki aur Tu hi use wafaat dega, us ki maut aur zindagi Tere hi liye hai. Agar Tu use zinda rakhe to us ki hifazat farma, aur agar maut de to use bakhsh de. Ae Allah, main Tujh se aafiyat mangta hoon.", "", "Sahih Muslim (Hisn al-Muslim 103)"),
            ("Save me from Your punishment", "اللّهُمَّ قِني عَذابَكَ يَوْمَ تَبْعَثُ عِبادَك", "Allāhumma qinī `adhābaka yawma tab`athu `ibādak.",
             "O Allah, save me from Your punishment on the Day You raise up Your servants. The Prophet, peace be upon him, said this three times with his right hand under his cheek.",
             "Ae Allah, mujhe us din apne azaab se bacha jis din Tu apne bandon ko uthayega. Nabi ﷺ daayan haath rukhsar ke neeche rakh kar teen baar yeh kehte.", "3", "Abu Dawud; At-Tirmidhi (Hisn al-Muslim 104)"),
            ("Bismika Allahumma", "بِاسْمِكَ اللّهُمَّ أَموتُ وَأَحْيا", "Bismika Allāhumma amūtu wa aḥyā.",
             "In Your name, O Allah, I die and I live.", "Ae Allah, Tere hi naam ke saath main marta (sota) hoon aur jeeta (jaagta) hoon.", "", "Sahih al-Bukhari (Hisn al-Muslim 105)"),
            ("Tasbih before sleeping (33, 33, 34)", ("STEPS", [
                ("سُبْحَانَ اللَّهِ", "SubḥānAllāh", "Glory be to Allah", "Allah paak hai", 33),
                ("وَالْحَمْدُ لِلَّهِ", "Alḥamdulillāh", "All praise is for Allah", "Tamam tareef Allah ke liye hai", 33),
                ("وَاللَّهُ أَكْبَرُ", "Allāhu Akbar", "Allah is the Greatest", "Allah sab se bara hai", 34)]),
             "", "The Prophet, peace be upon him, taught this to Fatimah and Ali instead of a servant: SubhanAllah 33, Alhamdulillah 33 and Allahu Akbar 34 before sleeping.",
             "Nabi ﷺ ne Hazrat Fatima aur Hazrat Ali (RA) ko khadim ke bajaye yeh sikhaya: sone se pehle SubhanAllah 33, Alhamdulillah 33 aur Allahu Akbar 34 baar.", "100", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 106)"),
            ("Lord of the seven heavens", "اللّهُمَّ رَبَّ السّمواتِ السَّبْعِ وَرَبَّ العَرْشِ العَظيم رَبَّنا وَرَبَّ كُلِّ شَيء فالِقَ الحَبِّ وَالنَّوى وَمُنَزِّلَ التَّوْراةِ وَالإنْجيل والفُرْقان أَعوذُ بِكَ مِن شَرِّ كُلِّ شَيءٍ أَنْتَ آخِذٌ بِناصِيَتِه اللّهُمَّ أَنْتَ الأوَّلُ فَلَيسَ قَبْلَكَ شَيء وَأَنْتَ الآخِرُ فَلَيسَ بَعْدَكَ شَيء وَأَنْتَ الظّاهِرُ فَلَيْسَ فَوْقَكَ شَيء وَأَنْتَ الْباطِنُ فَلَيْسَ دونَكَ شَيء اقْضِ عَنّا الدَّيْنَ وَأَغْنِنا مِنَ الفَقْر",
             "Allāhumma rabbas-samāwātis-sab`i wa rabbal-`arshil-`aẓīm, rabbanā wa rabba kulli shay', fāliqal-ḥabbi wan-nawā, wa munzilat-tawrāti wal-injīli wal-furqān, a`ūdhu bika min sharri kulli shay'in anta ākhidhun bināṣiyatih. Allāhumma antal-awwalu falaysa qablaka shay', wa antal-ākhiru falaysa ba`daka shay', wa antaẓ-ẓāhiru falaysa fawqaka shay', wa antal-bāṭinu falaysa dūnaka shay', iqḍi `annad-dayna wa aghninā minal-faqr.",
             "O Allah, Lord of the seven heavens and Lord of the Mighty Throne, our Lord and Lord of everything, who splits the seed and the date stone, who sent down the Torah, the Injeel and the Quran: I seek Your protection from the evil of everything You hold by the forelock. O Allah, You are the First, nothing is before You; You are the Last, nothing is after You; You are the Most High, nothing is above You; You are the Most Near, nothing is closer than You. Settle our debts for us and free us from poverty.",
             "Ae Allah, saat aasmanon ke Rab aur Arsh-e-Azeem ke Rab, hamare Rab aur har cheez ke Rab, daane aur guthli ko phaarne wale, Taurat, Injeel aur Furqan utaarne wale, main har us cheez ki buraai se Teri panah mangta hoon jis ki peshani Tere haath mein hai. Ae Allah, Tu awwal hai, Tujh se pehle kuch nahin; Tu aakhir hai, Tere baad kuch nahin; Tu zaahir hai, Tere upar kuch nahin; Tu baatin hai, Tujh se qareeb kuch nahin. Hamara qarz ada kar de aur hamein mohtaaji se be-niyaz kar de.", "", "Sahih Muslim (Hisn al-Muslim 107)"),
            ("Gratitude for food and a home", "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا، وَكَفَانَا، وَآوَانَا، فَكَمْ مِمَّنْ لاَ كَافِيَ لَهُ وَلاَ مُؤْوِيَ",
             "Alḥamdu lillāhil-ladhī aṭ`amanā wa saqānā wa kafānā wa āwānā, fakam mimman lā kāfiya lahū wa lā mu'wī.",
             "All praise is for Allah, who fed us, gave us drink, took care of our needs and gave us a home, for how many people have no one to care for them and no home.",
             "Tamam tareefein Allah ke liye hain jis ne hamein khilaya, pilaya, hamari zarooratein poori keen aur hamein thikana diya, kitne hi log hain jin ka na koi sahara hai na thikana.", "", "Sahih Muslim (Hisn al-Muslim 108)"),
            ("Knower of the unseen", "اللّهُمَّ عالِمَ الغَيْبِ وَالشّهادَةِ فاطِرَ السّماواتِ وَالأرْضِ رَبَّ كلِّ شَيءٍ وَمَليكَه أَشْهَدُ أَنْ لا إِلهَ إِلاّ أَنْت أَعوذُ بِكَ مِن شَرِّ نَفْسي وَمِن شَرِّ الشَّيْطانِ وَشِرْكِه وَأَنْ أَقْتَرِفَ عَلى نَفْسي سوءاً أَوْ أَجُرَّهُ إِلى مُسْلِم",
             "Allāhumma `ālimal-ghaybi wash-shahādah, fāṭiras-samāwāti wal-arḍ, rabba kulli shay'in wa malīkah, ash-hadu an lā ilāha illā ant, a`ūdhu bika min sharri nafsī wa min sharrish-shayṭāni wa shirkih, wa an aqtarifa `alā nafsī sū'an aw ajurrahū ilā muslim.",
             "O Allah, Knower of the unseen and the seen, Creator of the heavens and the earth, Lord and Owner of everything, I bear witness that there is no god but You. I seek Your protection from the evil of my own self, from the evil of Shaytan and his call to shirk, and from doing wrong to myself or bringing it upon any Muslim.",
             "Ae Allah, ghaib aur zaahir ke jaanne wale, aasmanon aur zameen ke paida karne wale, har cheez ke Rab aur Malik, main gawahi deta hoon ke Tere siwa koi mabood nahin. Main apne nafs ki buraai se, Shaitan ki buraai aur us ke shirk se, aur apne aap par koi buraai karne ya kisi Musalman ki taraf us ko le jaane se Teri panah mangta hoon.", "", "Abu Dawud; At-Tirmidhi (Hisn al-Muslim 109)"),
            ("The last words before sleep", "اللّهُمَّ أَسْلَمْتُ نَفْسي إِلَيْكَ، وَفَوَّضْتُ أَمْري إِلَيْكَ، وَوَجَّهْتُ وَجْهي إِلَيْكَ، وَأَلْجَأْتُ ظَهري إِلَيْكَ، رَغْبَةً وَرَهْبَةً إِلَيْكَ، لا مَلْجَأَ وَلا مَنْجا مِنْكَ إِلاّ إِلَيْكَ، آمَنْتُ بِكِتابِكَ الّذي أَنْزَلْتَ وَبِنَبِيِّكَ الّذي أَرْسَلْت",
             "Allāhumma aslamtu nafsī ilayk, wa fawwaḍtu amrī ilayk, wa wajjahtu wajhī ilayk, wa alja'tu ẓahrī ilayk, raghbatan wa rahbatan ilayk, lā malja'a wa lā manjā minka illā ilayk, āmantu bikitābikal-ladhī anzalt, wa binabiyyikal-ladhī arsalt.",
             "O Allah, I submit myself to You, I entrust my affairs to You, I turn my face to You and I rely on You completely, with hope and fear of You. There is no refuge and no escape from You except to You. I believe in Your Book that You sent down and Your Prophet whom You sent. The Prophet, peace be upon him, said to make these your last words before sleep.",
             "Ae Allah, main ne apne aap ko Tere supurd kiya, apna har kaam Tere hawale kiya, apna rukh Teri taraf kiya aur apni pusht Tera sahara li, Teri raghbat aur Tere khauf ke saath. Tujh se bach kar koi panah aur nijaat ki jagah nahin magar Teri hi taraf. Main Teri us kitaab par imaan laaya jo Tu ne utaari aur Tere us Nabi par jise Tu ne bheja. (Nabi ﷺ ne farmaya ise sone se pehle aakhri kalimaat banao.)", "", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 111)"),
        ],
        faqs=[("What is the dua before sleeping?", "The shortest is \"Bismika Allahumma amutu wa ahya\" - In Your name, O Allah, I die and I live (Sahih al-Bukhari). The Prophet, peace be upon him, also recited the 3 Quls and Ayatul Kursi every night."),
              ("Which surahs should I read before sleeping?", "The 3 Quls (blown into the hands three times), Ayatul Kursi and the last two verses of Surah Al-Baqarah are all authentic bedtime recitations."),
              ("What should children say before sleeping?", "Start with Bismika Allahumma amutu wa ahya and the 3 Quls. Our <a href=\"../../online-duas-course/\" class=\"in-link\">duas course</a> teaches them step by step.")])

    PAGES["travel-dua"] = dict(
        title="Travel Dua (Safar ki Dua) with Meaning | Duas for a Journey",
        desc="The authentic travel dua (safar ki dua) for starting a journey, returning home, entering a town, saying goodbye and more, with Arabic, transliteration and meaning in English and Roman Urdu.",
        h1='Travel Dua <span class="gold">(Safar ki Dua)</span>', ar_title="دُعَاءُ السَّفَر", eyebrow="Safe Journeys", card="Safar ki dua, returning home, goodbyes and more.",
        intro="Whether it is the school run, a flight to visit family or Umrah, the Prophet, peace be upon him, taught us to begin every journey with Allah's name. Here are the authentic travel duas from the Sunnah with their meaning in English and Roman Urdu.",
        items=[
            ("When getting into a car, plane or bus", "بِسْمِ اللهِ", "Bismillāh.", "In the name of Allah.", "Allah ke naam se.", "", "Abu Dawud (Hisn al-Muslim 210)"),
            ("The travel dua (safar ki dua)", "اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، ﴿سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ * وَإِنَّا إِلَى رَبِّنَا لَمُنقَلِبُونَ﴾ اللَّهُمَّ إِنّا نَسْأَلُكَ فِي سَفَرِنَا هَذَا البِرَّ وَالتَّقْوَى، وَمِنَ الْعَمَلِ مَا تَرْضَى، اللَّهُمَّ هَوِّنْ عَلَيْنَا سَفَرَنَا هَذَا وَاطْوِ عَنَّا بُعْدَهُ، اللَّهُمَّ أَنْتَ الصَّاحِبُ فِي السَّفَرِ، وَالْخَليفَةُ فِي الْأَهْلِ، اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ وَعْثَاءِ السَّفَرِ، وَكَآبَةِ الْمَنْظَرِ، وَسُوءِ الْمُنْقَلَبِ فِي الْمَالِ وَالْأَهْلِ",
             "Allāhu akbar, Allāhu akbar, Allāhu akbar. Subḥānal-ladhī sakhkhara lanā hādhā wa mā kunnā lahū muqrinīn, wa innā ilā rabbinā lamunqalibūn. Allāhumma innā nas'aluka fī safarinā hādhal-birra wat-taqwā, wa minal-`amali mā tarḍā. Allāhumma hawwin `alaynā safaranā hādhā waṭwi `annā bu`dah. Allāhumma antaṣ-ṣāḥibu fis-safar, wal-khalīfatu fil-ahl. Allāhumma innī a`ūdhu bika min wa`thā'is-safar, wa ka'ābatil-manẓar, wa sū'il-munqalabi fil-māli wal-ahl.",
             "Allah is the Greatest (3 times). Glory be to the One who has made this subject to us, which we could never have done ourselves, and to our Lord we will surely return. O Allah, we ask You on this journey for goodness and piety, and for deeds that please You. O Allah, make this journey easy for us and shorten its distance. O Allah, You are our Companion on the journey and the Guardian of our family. O Allah, I seek Your protection from the hardships of travel, from sad sights, and from finding harm in our wealth and family when we return.",
             "Allah sab se bara hai (teen baar). Paak hai woh zaat jis ne is (sawari) ko hamare tabe kar diya, warna hum ise qaabu mein na la sakte the, aur beshak hum apne Rab ki taraf laut kar jaane wale hain. Ae Allah, hum is safar mein Tujh se neki aur taqwa mangte hain aur woh amal jo Tujhe pasand ho. Ae Allah, hamare is safar ko aasaan kar de aur is ki doori ko samait de. Ae Allah, Tu safar mein hamara saathi aur ghar walon ka nigehbaan hai. Ae Allah, main safar ki mushqat, buray manzar aur maal aur ghar walon mein bure anjaam se Teri panah mangta hoon.", "", "Sahih Muslim (Hisn al-Muslim 207)"),
            ("When returning from a journey", "آيِبُونَ، تَائِبُونَ، عَابِدُونَ، لِرَبِّنا حَامِدُونَ",
             "Āyibūna tā'ibūna `ābidūna lirabbinā ḥāmidūn.",
             "Say the travel dua again and add: We return, repenting, worshipping and praising our Lord.",
             "Wapsi par safar ki dua dobara parhein aur yeh izafa karein: Hum laut kar aane wale hain, tauba karne wale, ibadat karne wale aur apne Rab ki tareef karne wale.", "", "Sahih Muslim (Hisn al-Muslim 207)"),
            ("When entering a town or city", "اللّهُمَّ رَبَّ السَّمواتِ السّبْعِ وَما أَظْلَلَن، وَرَبَّ الأَراضينَ السّبْعِ وَما أقْلَلْن، وَرَبَّ الشَّياطينِ وَما أَضْلَلْن، وَرَبَّ الرِّياحِ وَما ذَرَيْن، أَسْأَلُكَ خَيْرَ هذهِ الْقَرْيَةِ وَخَيْرَ أَهْلِها، وَخَيْرَ ما فيها، وَأَعوذُ بِكَ مِنْ شَرِّها وَشَرِّ أَهْلِها، وَشَرِّ ما فيها",
             "Allāhumma rabbas-samāwātis-sab`i wa mā aẓlalna, wa rabbal-araḍīnas-sab`i wa mā aqlalna, wa rabbash-shayāṭīni wa mā aḍlalna, wa rabbar-riyāḥi wa mā dharayna, as'aluka khayra hādhihil-qaryati wa khayra ahlihā wa khayra mā fīhā, wa a`ūdhu bika min sharrihā wa sharri ahlihā wa sharri mā fīhā.",
             "O Allah, Lord of the seven heavens and all they shade, Lord of the seven earths and all they carry, Lord of the devils and all they mislead, Lord of the winds and all they scatter: I ask You for the good of this town, the good of its people and the good of all that is in it, and I seek Your protection from its evil, the evil of its people and the evil of all that is in it.",
             "Ae Allah, saat aasmanon ke Rab aur jin par woh saaya karte hain, saat zameenon ke Rab aur jo woh uthaati hain, shaitanon ke Rab aur jinhein woh gumraah karte hain, hawaon ke Rab aur jo woh urati hain: main Tujh se is basti ki bhalai, is ke logon ki bhalai aur jo is mein hai us ki bhalai mangta hoon, aur is ki buraai, is ke logon ki buraai aur jo is mein hai us ki buraai se Teri panah mangta hoon.", "", "Al-Hakim, graded authentic (Hisn al-Muslim 208)"),
            ("When stopping somewhere on a journey", "أَعوذُ بِكَلِماتِ اللّهِ التّامّاتِ مِنْ شَرِّ ما خَلَق", "A`ūdhu bikalimātillāhit-tāmmāti min sharri mā khalaq.",
             "I seek protection in the perfect words of Allah from the evil of what He has created. Nothing will harm you until you leave that place.",
             "Main Allah ke mukammal kalimaat ki panah mangta hoon har us cheez ki buraai se jo Us ne paida ki. Jab tak aap wahan se rawana na hon koi cheez nuqsan nahin pohnchayegi.", "", "Sahih Muslim (Hisn al-Muslim 216)"),
            ("The traveller's goodbye to family", "أَسْتَوْدِعُكُمُ اللَّهَ الَّذي لا تَضيعُ وَدائِعُه", "Astawdi`ukumullāhal-ladhī lā taḍī`u wadā'i`uh.",
             "I leave you in the care of Allah, whose trusts are never lost.", "Main tumhein us Allah ke supurd karta hoon jis ke supurd ki hui amanatein kabhi zaaya nahin hoteen.", "", "Ahmad; Ibn Majah (Hisn al-Muslim 211)"),
            ("Saying goodbye to a traveller", "أَسْتَوْدِعُ اللَّهَ دينَكَ وَأَمانَتَكَ، وَخَواتيمَ عَمَلِك", "Astawdi`ullāha dīnaka wa amānataka wa khawātīma `amalik.",
             "I leave your faith, your trust and the last of your deeds in the care of Allah.", "Main tumhara deen, tumhari amanat aur tumhare aakhri amal Allah ke supurd karta hoon.", "", "Ahmad; At-Tirmidhi (Hisn al-Muslim 212)"),
            ("A dua for the traveller", "زَوَّدَكَ اللَّهُ التقْوى، وَغَفَرَ ذَنْبَكَ، وَيَسَّرَ لَكَ الخَيْرَ حَيْثُما كُنْت", "Zawwadakallāhut-taqwā, wa ghafara dhanbak, wa yassara lakal-khayra ḥaythumā kunt.",
             "May Allah give you piety as your provision, forgive your sins and make good easy for you wherever you are.", "Allah tumhein taqwa ka zaad-e-raah de, tumhare gunah maaf kare aur tum jahan bhi ho tumhare liye bhalai aasaan kare.", "", "At-Tirmidhi (Hisn al-Muslim 213)"),
        ],
        faqs=[("What is the dua for travelling?", "Say Bismillah when getting on, then the travel dua beginning with Allahu Akbar three times and \"Subhanal-ladhi sakhkhara lana hadha...\" (Sahih Muslim), shown above."),
              ("Is there a dua for flying or driving?", "The same travel dua is said for any journey, whether by car, bus, train or plane."),
              ("What do I say when I come home?", "Say the travel dua again and add \"Ayibuna, ta'ibuna, 'abiduna, li rabbina hamidun\".")])

    PAGES["wudu-and-masjid-duas"] = dict(
        title="Wudu Dua and Masjid Duas (Entering & Leaving the Mosque)",
        desc="Authentic duas for wudu (before and after ablution) and for going to, entering and leaving the masjid, with Arabic, transliteration and meaning in English and Roman Urdu.",
        h1='Wudu and <span class="gold">Masjid Duas</span>', ar_title="الوُضُوء وَالمَسْجِد", eyebrow="Purity and Prayer", card="Before and after wudu, entering and leaving the masjid.",
        intro="Wudu washes away sins, and the walk to the masjid is full of reward. These short authentic duas, taught by the Prophet, peace be upon him, turn both into acts of remembrance. They are perfect for children learning to pray.",
        items=[
            ("Before wudu", "بِسْمِ الله", "Bismillāh.", "In the name of Allah.", "Allah ke naam se.", "", "Abu Dawud; Ibn Majah (Hisn al-Muslim 12)"),
            ("After wudu: the shahada", "أَشْهَدُ أَنْ لا إِلَهَ إِلاّ اللهُ وَحْدَهُ لا شَريكَ لَهُ وَأَشْهَدُ أَنَّ مُحَمّداً عَبْدُهُ وَرَسولُه", "Ash-hadu an lā ilāha illallāhu waḥdahu lā sharīka lah, wa ash-hadu anna Muḥammadan `abduhū wa rasūluh.",
             "I bear witness that there is no god but Allah alone, with no partner, and I bear witness that Muhammad is His servant and Messenger. The eight gates of Paradise are opened for whoever says this after wudu.",
             "Main gawahi deta hoon ke Allah ke siwa koi mabood nahin, woh akela hai, Us ka koi shareek nahin, aur main gawahi deta hoon ke Muhammad ﷺ Us ke bande aur Rasool hain. Jo wudu ke baad yeh kahe us ke liye jannat ke aathon darwaze khol diye jaate hain.", "", "Sahih Muslim (Hisn al-Muslim 13)"),
            ("After wudu: make me among the pure", "اللّهُمَّ اجْعَلني مِنَ التَّوّابينَ وَاجْعَلْني مِنَ المتَطَهّرين", "Allāhummaj`alnī minat-tawwābīna waj`alnī minal-mutaṭahhirīn.",
             "O Allah, make me among those who turn to You in repentance and make me among those who purify themselves.", "Ae Allah, mujhe tauba karne walon mein se bana aur mujhe paak saaf rehne walon mein se bana.", "", "At-Tirmidhi (Hisn al-Muslim 14)"),
            ("After wudu: glory to You", "سُبْحانَكَ اللّهُمَّ وَبِحَمدِك أَشْهَدُ أَنْ لا إِلهَ إِلاّ أَنْتَ أَسْتَغْفِرُكَ وَأَتوبُ إِلَيْك", "Subḥānaka Allāhumma wa biḥamdik, ash-hadu an lā ilāha illā ant, astaghfiruka wa atūbu ilayk.",
             "Glory be to You, O Allah, and all praise is Yours. I bear witness that there is no god but You. I ask Your forgiveness and turn to You in repentance.", "Ae Allah, Tu paak hai aur tamam tareef Teri hai. Main gawahi deta hoon ke Tere siwa koi mabood nahin. Main Tujh se maghfirat mangta hoon aur Teri taraf tauba karta hoon.", "", "An-Nasa'i (Hisn al-Muslim 15)"),
            ("When leaving home for the masjid", "بِسْمِ اللهِ ، تَوَكَّلْتُ عَلى اللهِ وَلا حَوْلَ وَلا قُوَّةَ إِلاّ بِالله", "Bismillāhi, tawakkaltu `alallāhi, wa lā ḥawla wa lā quwwata illā billāh.",
             "In the name of Allah, I put my trust in Allah, and there is no power and no strength except with Allah.", "Allah ke naam se, main ne Allah par bharosa kiya, aur Allah ke siwa na koi taaqat hai na quwwat.", "", "Abu Dawud; At-Tirmidhi (Hisn al-Muslim 16)"),
            ("Walking to the masjid: the dua of light", "اللّهُمَّ اجْعَلْ فِي قَلْبي نُوراً ، وَفي لِسَانِي نُوراً، وَفِي سَمْعِي نُوراً, وَفِي بَصَرِي نُوراً, وَمِنْ فَوْقِي نُوراً , وَمِنْ تَحْتِي نُوراً, وَعَنْ يَمِينِي نُوراً, وعَنْ شِمَالِي نُوراً, وَمِنْ أَمَامِي نُوراً, وَمِنْ خَلْفِي نُوراً, واجْعَلْ فِي نَفْسِي نُوراً, وأَعْظِمْ لِي نُوراً",
             "Allāhummaj`al fī qalbī nūrā, wa fī lisānī nūrā, wa fī sam`ī nūrā, wa fī baṣarī nūrā, wa min fawqī nūrā, wa min taḥtī nūrā, wa `an yamīnī nūrā, wa `an shimālī nūrā, wa min amāmī nūrā, wa min khalfī nūrā, waj`al fī nafsī nūrā, wa a`ẓim lī nūrā.",
             "O Allah, place light in my heart and light on my tongue, light in my hearing and light in my sight, light above me and light below me, light on my right and light on my left, light in front of me and light behind me. Place light in my soul and make my light great.",
             "Ae Allah, mere dil mein noor daal de, meri zabaan mein noor, meri sunne mein noor, meri nazar mein noor, mere upar noor, mere neeche noor, mere daayen noor, mere baayen noor, mere aage noor, mere peeche noor, meri jaan mein noor daal de aur mere noor ko bara kar de.", "", "Sahih al-Bukhari; Sahih Muslim (Hisn al-Muslim 19)"),
            ("When entering the masjid", "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ", "Allāhummaftaḥ lī abwāba raḥmatik.",
             "O Allah, open for me the doors of Your mercy. Enter with your right foot first.", "Ae Allah, mere liye apni rehmat ke darwaze khol de. (Daayan paaon pehle andar rakhein.)", "", "Sahih Muslim 713 (Hisn al-Muslim 20)"),
            ("When leaving the masjid", "بِسمِ الله وَالصّلاةُ وَالسّلامُ عَلى رَسولِ الله، اللّهُمَّ إِنّي أَسْأَلُكَ مِنْ فَضْلِك، اللّهُمَّ اعصِمْني مِنَ الشَّيْطانِ الرَّجيم",
             "Bismillāhi waṣ-ṣalātu was-salāmu `alā rasūlillāh. Allāhumma innī as'aluka min faḍlik. Allāhumma`ṣimnī minash-shayṭānir-rajīm.",
             "In the name of Allah, and blessings and peace be upon the Messenger of Allah. O Allah, I ask You for Your bounty. O Allah, protect me from Shaytan the rejected. Leave with your left foot first.",
             "Allah ke naam se, aur Allah ke Rasool par durood o salam ho. Ae Allah, main Tujh se Tera fazl mangta hoon. Ae Allah, mujhe mardood Shaitan se bacha. (Baayan paaon pehle bahar rakhein.)", "", "Ibn Majah (Hisn al-Muslim 21)"),
        ],
        faqs=[("What is the dua after wudu?", "\"Ash-hadu an la ilaha illallahu wahdahu la sharika lah, wa ash-hadu anna Muhammadan 'abduhu wa rasuluh\". The Prophet, peace be upon him, said the eight gates of Paradise are opened for whoever says it (Sahih Muslim)."),
              ("What is the dua for entering the masjid?", "\"Allahummaftah li abwaba rahmatik\" - O Allah, open for me the doors of Your mercy (Sahih Muslim 713). Enter with the right foot."),
              ("Can my child learn wudu and salah online?", "Yes. Our <a href=\"../../online-salah-classes/\" class=\"in-link\">online salah classes</a> teach wudu and salah step by step with a female teacher.")])

    for s in ("sleeping-duas", "travel-dua", "wudu-and-masjid-duas"):
        if s not in ORDER:
            ORDER.insert(3 if s == "sleeping-duas" else len(ORDER) - 1, s)
