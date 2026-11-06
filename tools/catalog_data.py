# -*- coding: utf-8 -*-
"""Structure of the library: courses, sections and documents (RO + RU metadata).

`src` paths are matched against the source folders ignoring diacritics/case, so
"instructia tragerii/Cartuse.ppt" finds "instrucția tragerii/Cartuse.ppt".

kind:  slides (presentation) | doc (Word document) | pdf (text PDF) | scan (scanned PDF)
type:  key in TYPES below (label shown on cards)
mode:  default view in the reader: slides | text | pages
"""

SITE = {
    'title': {'ro': 'Grupa 131 · Inițiere în Ofițer', 'ru': 'Группа 131 · Initiere în Ofițer'},
    'program': {'ro': 'Cursul de formare inițială a ofițerilor', 'ru': 'Курс первоначальной подготовки офицеров'},
}

TYPES = {
    'presentation': {'ro': 'Prezentare', 'ru': 'Презентация', 'icon': 'i-slides'},
    'lecture':      {'ro': 'Suport de curs', 'ru': 'Конспект', 'icon': 'i-book'},
    'lesson':       {'ro': 'Proiect de lecție', 'ru': 'План занятия', 'icon': 'i-doc'},
    'instruction':  {'ro': 'Instrucțiune', 'ru': 'Инструкция', 'icon': 'i-doc'},
    'law':          {'ro': 'Lege', 'ru': 'Закон', 'icon': 'i-law'},
    'order':        {'ro': 'Ordin MAI', 'ru': 'Приказ МВД', 'icon': 'i-law'},
    'hg':           {'ro': 'Hotărâre de Guvern', 'ru': 'Постановление Правительства', 'icon': 'i-law'},
    'regulation':   {'ro': 'Regulament', 'ru': 'Устав / Положение', 'icon': 'i-law'},
    'manual':       {'ro': 'Manual', 'ru': 'Учебник', 'icon': 'i-book'},
    'guide':        {'ro': 'Ghid', 'ru': 'Руководство', 'icon': 'i-book'},
}

SECTION_TITLES = {
    'teme':       {'ro': 'Teme', 'ru': 'Темы'},
    'studiu':     {'ro': 'Materiale de studiu', 'ru': 'Учебные материалы'},
    'prezentari': {'ro': 'Prezentări', 'ru': 'Презентации'},
    'suporturi':  {'ro': 'Suporturi de curs și manuale', 'ru': 'Конспекты и учебники'},
    'acte':       {'ro': 'Regulamente și acte normative', 'ru': 'Уставы и нормативные акты'},
}

COURSES = [
    {
        'id': 'front', 'icon': 'c-front', 'color': '#2f62d0', 'code': None,
        'title': {'ro': 'Instrucția de front', 'ru': 'Строевая подготовка'},
        'short': {'ro': 'Poziții, întoarceri, deplasare, salut, formații și portul uniformei.',
                  'ru': 'Стойки, повороты, передвижение, воинское приветствие, строи и ношение формы.'},
        'desc': {'ro': 'Normele de conduită și regulile instrucției de front: pozițiile de bază, întoarcerile, deplasarea și pasul de defilare, '
                       'salutul militar, formațiile, precum și regulile de port al uniformei.',
                 'ru': 'Нормы поведения и правила строевой подготовки: основные стойки, повороты, передвижение и строевой шаг, '
                       'воинское приветствие, строи, а также правила ношения форменной одежды.'},
        'sections': [
            ('studiu', ['front-prezentare', 'front-pas-defilare']),
            ('acte', ['front-regulament', 'front-ordin-493', 'front-ordin-54', 'front-hg-676']),
        ],
        'related': [],
    },
    {
        'id': 'arop', 'icon': 'c-arop', 'color': '#b7791f', 'code': 'AROP',
        'title': {'ro': 'AROP', 'ru': 'AROP'},
        'subtitle': {'ro': 'Asigurarea și restabilirea ordinii publice', 'ru': 'Обеспечение и восстановление общественного порядка'},
        'short': {'ro': 'Menținerea, asigurarea și restabilirea ordinii publice: noțiuni, dispozitive și procedee.',
                  'ru': 'Поддержание, обеспечение и восстановление общественного порядка: понятия, построения, приёмы.'},
        'desc': {'ro': 'Menținerea, asigurarea și restabilirea ordinii publice: noțiuni și principii, dispozitivele de asigurare '
                       '(cordoane, coridoare, posturi, baraje) și procedeele de restabilire a ordinii publice.',
                 'ru': 'Поддержание, обеспечение и восстановление общественного порядка: понятия и принципы, построения для '
                       'обеспечения порядка (оцепления, коридоры, посты, заграждения) и приёмы восстановления порядка.'},
        'sections': [
            ('teme', ['arop-tema-1', 'arop-tema-2', 'arop-tema-3']),
        ],
        'related': ['trg-legea-218', 'trg-ordin-311'],
    },
    {
        'id': 'tragere', 'icon': 'c-tragere', 'color': '#c0392b', 'code': None,
        'title': {'ro': 'Instrucția tragerii', 'ru': 'Огневая подготовка'},
        'short': {'ro': 'Măsuri de siguranță, codificări de alertă, balistică, cartușe, armament și legislație.',
                  'ru': 'Меры безопасности, коды тревоги, баллистика, патроны, оружие и законодательство.'},
        'desc': {'ro': 'Cadrul normativ al instrucției tragerii, măsurile de siguranță și codificările de alertă, balistica, cartușele, '
                       'construcția armamentului (PM, AK-74) și legislația privind aplicarea armei de foc.',
                 'ru': 'Нормативная база огневой подготовки, меры безопасности и коды тревоги, баллистика, патроны, '
                       'устройство оружия (ПМ, АК-74) и законодательство о применении огнестрельного оружия.'},
        'sections': [
            ('prezentari', ['trg-regulament-222', 'trg-masuri-siguranta', 'trg-masuri-222-311', 'trg-cps-311',
                            'trg-codificari', 'trg-legea-218-prez', 'trg-balistica', 'trg-cartuse']),
            ('suporturi', ['trg-tema-1-coercitive', 'trg-masuri-securitate', 'trg-suport-curs']),
            ('acte', ['trg-ordin-222', 'trg-regulament-nou', 'trg-ordin-311', 'trg-legea-218', 'trg-legea-130',
                      'trg-regim-armament', 'trg-ghid-interventie']),
        ],
        'related': [],
    },
    {
        'id': 'prim-ajutor', 'icon': 'c-prim', 'color': '#15803d', 'code': None,
        'title': {'ro': 'Prim ajutor', 'ru': 'Первая помощь'},
        'short': {'ro': 'Suport vital bazal, evaluarea victimei, etapele primului ajutor și Serviciul 112.',
                  'ru': 'Базовая реанимация, оценка пострадавшего, этапы первой помощи и Служба 112.'},
        'desc': {'ro': 'Suportul vital bazal la adult, evaluarea victimei, principiile și etapele acordării primului ajutor, '
                       'manualul european de prim ajutor și activitatea Serviciului 112.',
                 'ru': 'Базовая сердечно-лёгочная реанимация у взрослых, оценка состояния пострадавшего, принципы и этапы '
                       'оказания первой помощи, европейское руководство по первой помощи и работа Службы 112.'},
        'sections': [
            ('prezentari', ['pa-svb', 'pa-112']),
            ('suporturi', ['pa-sinteza', 'pa-ipssm', 'pa-manual']),
        ],
        'related': [],
    },
    {
        'id': 'tip', 'icon': 'c-tip', 'color': '#5b3cc4', 'code': 'TIP',
        'title': {'ro': 'TIP', 'ru': 'TIP'},
        'subtitle': {'ro': 'Tactica intervenției profesionale', 'ru': 'Тактика профессионального вмешательства'},
        'short': {'ro': 'Intervenția graduală, legitimarea, controlul corporal, aplicarea forței și a mijloacelor speciale.',
                  'ru': 'Поэтапное вмешательство, проверка документов, досмотр, применение силы и спецсредств.'},
        'desc': {'ro': 'Tactica intervenției profesionale: noțiuni și principii, intervenția graduală, contactarea și legitimarea persoanei, '
                       'controlul corporal și percheziția, aplicarea forței fizice și a mijloacelor speciale.',
                 'ru': 'Тактика профессионального вмешательства: понятия и принципы, поэтапное вмешательство, контакт и проверка '
                       'документов, личный досмотр и обыск, применение физической силы и специальных средств.'},
        'sections': [
            ('teme', ['tip-tema-1', 'tip-tema-2', 'tip-tema-3', 'tip-tema-4', 'tip-tema-5']),
        ],
        'related': ['trg-ordin-311', 'trg-ghid-interventie', 'trg-legea-218'],
    },
]

# Materials that are not tied to one discipline (shown on the home / about pages).
GENERAL = ['info-formare-initiala']

DOCS = {
    # ------------------------------------------------------------------ INSTRUCȚIA DE FRONT
    'front-prezentare': dict(
        src='instructia front/instructia de front.pptx', kind='slides', type='presentation',
        kicker={'ro': 'Noțiuni de bază', 'ru': 'Основы'},
        title={'ro': 'Instrucția de front pentru funcționarii publici cu statut special din cadrul MAI',
               'ru': 'Строевая подготовка служащих с особым статусом МВД'},
        summary={'ro': 'Definiția și rolul instrucției de front, disciplina și ordinea, executarea comenzilor, elementele formației, '
                       'pozițiile „Drepți” și „Pe loc repaus”, întoarcerile pe loc și salutul de front.',
                 'ru': 'Определение и роль строевой подготовки, дисциплина и порядок, выполнение команд, элементы строя, '
                       'стойки «Смирно» и «Вольно», повороты на месте и воинское приветствие.'},
        points={'ro': ['Instrucția de front este ansamblul de reguli, metode și exerciții prin care se formează deprinderea de a acționa organizat, disciplinat și coordonat în formație.',
                       'Elementele formației: frontul, flancul, intervalul (distanța laterală), distanța (în adâncime), rândul și coloana.',
                       'Tipurile de formații: în linie (ceremonii, prezentări), în coloană (deplasări), pe două rânduri (efectiv numeros, spațiu limitat).',
                       'Poziția „Drepți” este poziția de bază: corpul drept și nemișcat, călcâiele apropiate, privirea înainte, liniște și atenție.',
                       '„Pe loc repaus” permite relaxarea temporară fără părăsirea locului în formație; la comanda „Drepți” se revine imediat.',
                       'Întoarcerile pe loc — la dreapta, la stânga, împrejur — se execută rapid și precis, fără a pierde alinierea.'],
                'ru': ['Строевая подготовка — совокупность правил, методов и упражнений, формирующих умение действовать организованно, дисциплинированно и слаженно в строю.',
                       'Элементы строя: фронт, фланг, интервал (расстояние по фронту), дистанция (в глубину), шеренга и колонна.',
                       'Виды строя: развёрнутый (церемонии, смотры), походный — колонна (передвижение), двухшереножный (большой состав на ограниченной площади).',
                       'Стойка «Смирно» — основная: корпус прямо и неподвижно, пятки вместе, взгляд вперёд, тишина и внимание.',
                       '«Вольно» позволяет временно расслабиться, не покидая места в строю; по команде «Смирно» — сразу принять строевую стойку.',
                       'Повороты на месте — направо, налево, кругом — выполняются быстро и чётко, без нарушения равнения.']},
    ),
    'front-pas-defilare': dict(
        src='instructia front/Instructiune Metodica pasul nou1.doc', kind='doc', type='instruction', mode='text',
        kicker={'ro': 'Instrucțiune metodică', 'ru': 'Методическая инструкция'},
        title={'ro': 'Antrenarea mișcării mâinii și a pasului de defilare',
               'ru': 'Отработка движения рук и строевого шага'},
        summary={'ro': 'Metodica antrenării în trei etape (pe elemente, în complex, în cadrul formației) a mișcării mâinilor, '
                       'pasului pe loc și pasului de defilare — fiecare executat în patru mișcări.',
                 'ru': 'Методика обучения в три этапа (по элементам, в комплексе, в составе строя) движению рук, шагу на месте '
                       'и строевому шагу — каждое упражнение выполняется в четыре движения.'},
        points={'ro': ['Etapa I — pe elemente, la comanda: „…la patru numere începeți! Faceți UNU, faceți DOI, faceți TREI, faceți PATRU”.',
                       'Etapa a II-a — fiecare mișcare în complex: „…începeți! UNU, DOI, TREI, PATRU”.',
                       'Etapa a III-a — toate mișcările în complex, din mers, în cadrul rândului sau al formației.',
                       'Mișcarea mâinii: brațul drept, cu pumnul strâns, se ridică înainte până la înălțimea umărului, revine, apoi se duce înapoi cât permite articulația umărului.',
                       'Pasul pe loc: piciorul se ridică la 15–20 cm, talpa paralelă cu solul, brațele se mișcă în ritmul pasului.'],
                'ru': ['Этап I — по элементам, по команде: «…на четыре счёта начинай! Делай РАЗ, делай ДВА, делай ТРИ, делай ЧЕТЫРЕ».',
                       'Этап II — каждое движение в комплексе: «…начинай! РАЗ, ДВА, ТРИ, ЧЕТЫРЕ».',
                       'Этап III — все движения в комплексе, в движении, в составе шеренги или строя.',
                       'Движение руки: правая рука, сжатая в кулак, выносится вперёд до высоты плеча, возвращается, затем отводится назад до упора в плечевом суставе.',
                       'Шаг на месте: нога поднимается на 15–20 см, ступня параллельна земле, руки двигаются в такт шагу.']},
    ),
    'front-regulament': dict(
        src='instructia front/Regulamentul Instructiei de frontF. modificari2 (5).doc', kind='doc', type='regulation', mode='text',
        kicker={'ro': 'Regulament', 'ru': 'Устав'},
        title={'ro': 'Regulamentul instrucției de front al Forțelor Armate ale Republicii Moldova',
               'ru': 'Строевой устав Вооружённых сил Республики Молдова'},
        summary={'ro': 'Regulamentul de bază al instrucției de front: formațiile și conducerea lor, exercițiile de front fără armă și cu arma, '
                       'salutul militar, ieșirea și întoarcerea în formație, formațiile subunităților, revista de front și drapelul de luptă.',
                 'ru': 'Основной строевой устав: строи и управление ими, строевые приёмы без оружия и с оружием, воинское приветствие, '
                       'выход из строя и возвращение в строй, строи подразделений, строевой смотр и Боевое знамя.'},
        points={'ro': ['Titlul I — formațiile și obligațiile militarilor înainte de adunare și în formație.',
                       'Titlul II — exercițiile de front și deplasarea fără armă și cu arma: poziția „drepți”, întoarcerile de pe loc, deplasarea, întoarcerile din mers, mânuirile armei.',
                       'Titlul III — executarea salutului (onorului) militar de pe loc și din mers, ieșirea din formație și întoarcerea în formație, prezentarea în fața comandantului.',
                       'Titlurile IV–V — formațiile grupei, plutonului, companiei, batalionului și brigăzii, pe jos și pe mașini.',
                       'Titlurile VI–VII — revista de front a subunităților și locul drapelului de luptă în formație.'],
                'ru': ['Раздел I — строи и обязанности военнослужащих перед построением и в строю.',
                       'Раздел II — строевые приёмы и движение без оружия и с оружием: стойка «смирно», повороты на месте, движение, повороты в движении, приёмы с оружием.',
                       'Раздел III — выполнение воинского приветствия на месте и в движении, выход из строя и возвращение в строй, подход к начальнику и отход от него.',
                       'Разделы IV–V — строи отделения, взвода, роты, батальона и бригады в пешем порядке и на машинах.',
                       'Разделы VI–VII — строевой смотр подразделений и место Боевого знамени в строю.']},
    ),
    'front-ordin-493': dict(
        src='instructia front/130 13.09.2024.pdf', kind='scan', type='order', mode='pages',
        kicker={'ro': 'Ordinul MAI nr. 493 din 14.09.2024', 'ru': 'Приказ МВД № 493 от 14.09.2024'},
        title={'ro': 'Instrucțiunea privind normele de conduită, relaționare și elementele instrucției de front',
               'ru': 'Инструкция о нормах поведения, взаимоотношений и элементах строевой подготовки'},
        summary={'ro': 'Instituie reguli unice pentru funcționarii publici cu statut special ai MAI privind conduita, aspectul exterior, '
                       'relaționarea, disciplina, eticheta de serviciu, portul uniformei și elementele instrucției de front.',
                 'ru': 'Устанавливает единые правила для служащих с особым статусом МВД: поведение, внешний вид, взаимоотношения, '
                       'дисциплина, служебный этикет, ношение формы и элементы строевой подготовки.'},
        points={'ro': ['Se aplică funcționarilor publici cu statut special, inclusiv elevilor și studenților cu statut special, din toate subdiviziunile MAI.',
                       'Normele de conduită se respectă atât în serviciu, cât și în afara acestuia, inclusiv în relațiile cu cetățenii.',
                       'Activitatea se desfășoară în baza principiilor profesionalismului, integrității, loialității, imparțialității, transparenței și subordonării ierarhice.',
                       'Încălcarea Instrucțiunii poate atrage răspunderea disciplinară, civilă, contravențională sau penală.'],
                'ru': ['Распространяется на служащих с особым статусом, в том числе учащихся и студентов с особым статусом, во всех подразделениях МВД.',
                       'Нормы поведения соблюдаются как на службе, так и вне её, в том числе в отношениях с гражданами.',
                       'Деятельность основывается на принципах профессионализма, неподкупности, лояльности, беспристрастности, прозрачности и иерархической подчинённости.',
                       'Нарушение Инструкции может повлечь дисциплинарную, гражданскую, административную (контравенционную) или уголовную ответственность.']},
    ),
    'front-ordin-54': dict(
        src='instructia front/25 29.01.2024.pdf', kind='scan', type='order', mode='pages',
        kicker={'ro': 'Ordinul MAI nr. 54 din 29.01.2024', 'ru': 'Приказ МВД № 54 от 29.01.2024'},
        title={'ro': 'Regulile de port a uniformei și a însemnelor distinctive',
               'ru': 'Правила ношения форменной одежды и знаков различия'},
        summary={'ro': 'Aprobă Regulile de port a uniformei și a însemnelor distinctive pentru funcționarii publici cu statut special din cadrul MAI, '
                       'obligatorii atât în timpul serviciului, cât și în afara orelor de serviciu.',
                 'ru': 'Утверждает Правила ношения формы и знаков различия служащими с особым статусом МВД — '
                       'обязательны как во время службы, так и вне её.'},
        points={'ro': ['Funcționarii sunt obligați să cunoască tipurile de uniformă și să respecte regulile de port.',
                       'Conducătorii subdiviziunilor asigură respectarea Regulilor de către personalul din subordine.',
                       'Folosirea altor uniforme sau însemne decât cele aprobate reprezintă încălcarea modului de folosire a simbolurilor publice și atrage răspundere.',
                       'Ordinul este emis în temeiul HG nr. 676/2023 privind uniforma funcționarului public cu statut special din cadrul MAI.'],
                'ru': ['Служащие обязаны знать виды формы одежды и соблюдать правила её ношения.',
                       'Руководители подразделений обеспечивают соблюдение Правил подчинённым личным составом.',
                       'Использование иной формы или знаков различия, кроме утверждённых, является нарушением порядка использования публичной символики и влечёт ответственность.',
                       'Приказ издан на основании Постановления Правительства № 676/2023 о форме служащего с особым статусом МВД.']},
    ),
    'front-hg-676': dict(
        src='instructia front/139672.pdf', kind='pdf', type='hg', mode='text',
        kicker={'ro': 'HG nr. 676 din 13.09.2023', 'ru': 'ПП № 676 от 13.09.2023'},
        title={'ro': 'Normele, descrierea și modelul uniformei funcționarului public cu statut special din cadrul MAI',
               'ru': 'Нормы, описание и образец формы служащего с особым статусом МВД'},
        summary={'ro': 'Hotărârea Guvernului care aprobă normele de asigurare, descrierea și modelul uniformei funcționarului public cu statut special '
                       'din cadrul MAI (Monitorul Oficial nr. 404-407 din 31.10.2023).',
                 'ru': 'Постановление Правительства, утверждающее нормы обеспечения, описание и образец формы служащего с особым статусом МВД '
                       '(Официальный монитор № 404-407 от 31.10.2023).'},
        points={'ro': ['Adoptată în temeiul art. 64 alin. (2) din Legea nr. 288/2016 privind funcționarul public cu statut special din cadrul MAI.',
                       'Stabilește normele, descrierea și modelul uniformei.',
                       'Constituie temeiul pentru Regulile de port a uniformei aprobate prin Ordinul MAI nr. 54/2024.'],
                'ru': ['Принято на основании ч. (2) ст. 64 Закона № 288/2016 о государственном служащем с особым статусом МВД.',
                       'Устанавливает нормы, описание и образец форменной одежды.',
                       'Является основанием для Правил ношения формы, утверждённых Приказом МВД № 54/2024.']},
    ),

    # ------------------------------------------------------------------ AROP
    'arop-tema-1': dict(
        src='AROP/Tema1 Actiuni la Mentinere AROP.pptx', kind='slides', type='presentation',
        kicker={'ro': 'Tema 1', 'ru': 'Тема 1'},
        title={'ro': 'Acțiuni la menținerea, asigurarea și restabilirea ordinii publice',
               'ru': 'Действия по поддержанию, обеспечению и восстановлению общественного порядка'},
        summary={'ro': 'Vocabularul specific, clasificarea evenimentelor publice, principiile de acțiune și conduita angajaților MAI '
                       'pe timpul misiunilor de menținere, asigurare și restabilire a ordinii publice.',
                 'ru': 'Специальная терминология, классификация публичных мероприятий, принципы действий и правила поведения '
                       'сотрудников МВД при поддержании, обеспечении и восстановлении общественного порядка.'},
        points={'ro': ['Menținerea ordinii publice — măsuri cotidiene; asigurarea — măsuri preventive pentru ca un eveniment public să se desfășoare fără tulburări; restabilirea — măsuri de intervenție, cu folosirea forței, pentru dispersarea unei mulțimi violente.',
                       'Evenimentele publice se clasifică după caracter, modul de declanșare, numărul participanților (mică — până la 100, medie — 100–1000, mare — peste 1000), durată, mod de desfășurare, grad de risc și mod de acțiune.',
                       'Eveniment public cu grad sporit de risc — cu risc iminent de tulburări sau cu peste 1000 de participanți.',
                       'Principii: legalitate, umanism, nediscriminare, evitarea surprinderii, suficiență–gradualitate–proporționalitate, riscul minim, colaborarea cu comunitatea, confidențialitatea.',
                       'Conduita: prudență și tact, neutralitate totală, evitarea conflictelor, acțiune numai după avertizările și somațiile legale.'],
                'ru': ['Поддержание порядка — повседневные меры; обеспечение — превентивные меры, чтобы мероприятие прошло без нарушений; восстановление — меры вмешательства с применением силы для рассеивания агрессивной толпы.',
                       'Публичные мероприятия классифицируются по характеру, способу возникновения, числу участников (малые — до 100, средние — 100–1000, крупные — свыше 1000), продолжительности, форме проведения, степени риска и характеру действий.',
                       'Мероприятие повышенного риска — с непосредственной угрозой беспорядков или с участием свыше 1000 человек.',
                       'Принципы: законность, гуманизм, недискриминация, недопущение внезапности, достаточность–постепенность–соразмерность, минимальный риск, сотрудничество с обществом, конфиденциальность.',
                       'Поведение: осторожность и такт, полный нейтралитет, избегание конфликтов, действия только после законных предупреждений и требований.']},
    ),
    'arop-tema-2': dict(
        src='AROP/Tema2.Asigurarea OP.pptx', kind='slides', type='presentation',
        kicker={'ro': 'Tema 2', 'ru': 'Тема 2'},
        title={'ro': 'Asigurarea ordinii publice', 'ru': 'Обеспечение общественного порядка'},
        summary={'ro': 'Dispozitivele utilizate la asigurarea ordinii publice: cordonul de ordine, cordonul de jaloneri, coridorul de trecere, '
                       'postul și barajul — compunere, misiuni și dotare.',
                 'ru': 'Построения для обеспечения общественного порядка: оцепление, цепь жалонёров, коридор прохода, пост и заграждение — '
                       'состав, задачи и оснащение.'},
        points={'ro': ['Cordonul de ordine — menține libertatea de mișcare pe un itinerar sau protejează manifestanții; fix (simplu, dublu în adâncime, dublu opus) sau mobil (simplu, dublu, în formă de unghi).',
                       'Distanța față de manifestanți peste 5 m: picioarele la lățimea umerilor, mâinile la spate; sub 5 m: mâinile în față, încrucișate.',
                       'Cordonul de jaloneri — la întâmpinarea delegațiilor oficiale; polițiștii dispuși în șah, la 45° în întâmpinarea coloanei.',
                       'Coridorul de trecere (simplu sau dublu) — pentru deplasarea persoanelor VIP, artiștilor etc.',
                       'Postul — protecția temporară a unui punct (element fix, mobil și de rezervă); barajul — interzicerea accesului unei mulțimi într-un spațiu (BOFI, baraj de direcționare, intermitent, filtrant).'],
                'ru': ['Оцепление — обеспечивает свободу движения по маршруту или защиту участников; неподвижное (одинарное, двойное в глубину, двойное встречное) или подвижное (одинарное, двойное, углом).',
                       'При расстоянии до участников более 5 м: ноги на ширине плеч, руки за спиной; менее 5 м: руки скрещены впереди.',
                       'Цепь жалонёров — при встрече официальных делегаций; полицейские в шахматном порядке, под углом 45° навстречу колонне.',
                       'Коридор прохода (одинарный или двойной) — для прохода VIP-персон, артистов и т. п.',
                       'Пост — временная охрана объекта (постоянный, подвижный и резервный элементы); заграждение — запрет доступа толпы на определённую территорию (BOFI, направляющее, прерывистое, фильтрующее).']},
    ),
    'arop-tema-3': dict(
        src='AROP/tema3 Restabilirea OP.pptx', kind='slides', type='presentation',
        kicker={'ro': 'Tema 3', 'ru': 'Тема 3'},
        title={'ro': 'Restabilirea ordinii publice', 'ru': 'Восстановление общественного порядка'},
        summary={'ro': 'Dispozitivul de acțiune și elementele sale, binomul scutier — agent de siguranță, pregătirea acțiunii și procedeele de restabilire: '
                       'saltul ofensiv, șarja, trecerea baricadelor, reținerea capilor instigatori, retragerea.',
                 'ru': 'Боевой порядок и его элементы, двойка «щитоносец — страхующий», подготовка действий и приёмы восстановления порядка: '
                       'наступательный рывок, атака (шарж), преодоление баррикад, задержание зачинщиков, отход.'},
        points={'ro': ['Forme de acțiune: non-violente (dialog cu liderii) și în forță — numai după epuizarea mijloacelor pașnice.',
                       'Elementul de bază al dispozitivului este binomul: scutierul (în față, cu scut) și agentul de siguranță (în spate).',
                       'Elementele dispozitivului: de contact, de flancare, grupa de intervenție mobilă (GIM), elementul de sprijin, monitorizare, escortă, documentare, punct de comandă, rezervă.',
                       'Saltul ofensiv — maximum 10 m, pentru crearea spațiului de manevră; nu este destinat câștigării de teren.',
                       'Șarja — procedeu ofensiv pentru dispersarea definitivă a mulțimii, executat numai după avertizările și somațiile prevăzute de art. 16 al Legii nr. 218/2012.'],
                'ru': ['Формы действий: ненасильственные (диалог с лидерами) и силовые — только после исчерпания мирных средств.',
                       'Основной элемент боевого порядка — двойка (бином): щитоносец (впереди, со щитом) и страхующий (сзади).',
                       'Элементы построения: контактный, фланговые, мобильная группа вмешательства (GIM), группа поддержки, наблюдения, конвоя, документирования, командный пункт, резерв.',
                       'Наступательный рывок — не более 10 м, для создания пространства для манёвра; не предназначен для захвата территории.',
                       'Шарж (атака) — наступательный приём для окончательного рассеивания толпы, только после предупреждений, предусмотренных ст. 16 Закона № 218/2012.']},
    ),

    # ------------------------------------------------------------------ INSTRUCȚIA TRAGERII
    'trg-regulament-222': dict(
        src='instructia tragerii/Regulamentul de tragere.ppt', kind='slides', type='presentation',
        kicker={'ro': 'Ordinul MAI nr. 222/2017', 'ru': 'Приказ МВД № 222/2017'},
        title={'ro': 'Regulamentul cu privire la instrucția tragerii în cadrul MAI',
               'ru': 'Положение об огневой подготовке в МВД'},
        summary={'ro': 'Principiile instrucției tragerii și categoriile de solicitare a angajaților MAI (ordinară, avansată, specială) '
                       'conform Regulamentului aprobat prin Ordinul MAI nr. 222 din 20.07.2017.',
                 'ru': 'Принципы огневой подготовки и категории нагрузки сотрудников МВД (обычная, продвинутая, специальная) '
                       'согласно Положению, утверждённому Приказом МВД № 222 от 20.07.2017.'},
        points={'ro': ['Principii: centralizare, orientarea spre necesitățile de instruire, autonomie.',
                       'Categoria ordinară — exerciții inițiale cu pistolul și pistolul-mitralieră, cel puțin 3 trageri anual.',
                       'Categoria avansată — angajații din urmărire penală, investigații și ordine publică: cel puțin o tragere lunar.',
                       'Categoria specială — subdiviziunile de intervenție și destinație specială: exerciții specifice și integrate.'],
                'ru': ['Принципы: централизация, ориентация на потребности обучения, автономия.',
                       'Обычная категория — начальные упражнения с пистолетом и автоматом, не менее 3 стрельб в год.',
                       'Продвинутая категория — уголовное преследование, расследования, общественный порядок: не менее одной стрельбы в месяц.',
                       'Специальная категория — подразделения вмешательства и специального назначения: специальные и комплексные упражнения.']},
    ),
    'trg-masuri-siguranta': dict(
        src='instructia tragerii/Masuri de siguranta.ppt', kind='slides', type='presentation',
        kicker={'ro': 'Măsuri de siguranță', 'ru': 'Меры безопасности'},
        title={'ro': 'Măsuri de siguranță la ședințele de tragere',
               'ru': 'Меры безопасности на стрельбах'},
        summary={'ro': 'Cerințele Ordinului MAI nr. 222/2017, organizarea tragerilor, regulile fundamentale de securitate, cazurile de încetare a focului, '
                       'interdicțiile și măsurile de siguranță la curățarea și ungerea armei.',
                 'ru': 'Требования Приказа МВД № 222/2017, организация стрельб, основные правила безопасности, случаи прекращения огня, '
                       'запреты и меры безопасности при чистке и смазке оружия.'},
        points={'ro': ['Orice armă se consideră și se manipulează întotdeauna ca și cum ar fi încărcată.',
                       'Țeava nu se îndreaptă spre țintă până nu a fost indicată de conducătorul tragerii; degetul nu se pune pe trăgaci până la comanda de deschidere a focului.',
                       'Orice manipulare (alimentare, încărcare, descărcare, verificare) se execută numai într-o direcție nepericuloasă.',
                       'Focul încetează imediat la apariția oamenilor sau animalelor în poligon, la ridicarea fanionului alb, la izbucnirea incendiului, la pierderea orientării.',
                       'Înainte de curățare, angajatul se asigură că în camera cartușului nu sunt cartușe.'],
                'ru': ['Любое оружие всегда считается заряженным и обращаться с ним нужно соответственно.',
                       'Ствол не направляется на цель, пока её не указал руководитель стрельбы; палец не кладётся на спусковой крючок до команды «огонь».',
                       'Любые манипуляции (снаряжение, заряжание, разряжание, проверка) — только в безопасном направлении.',
                       'Огонь немедленно прекращается при появлении людей или животных на стрельбище, подъёме белого флажка, пожаре, потере ориентации.',
                       'Перед чисткой сотрудник убеждается, что в патроннике нет патрона.']},
    ),
    'trg-masuri-222-311': dict(
        src='instructia tragerii/Masuri Regulamentul 222.ppt', kind='slides', type='presentation',
        kicker={'ro': 'Ord. 222/2017 și Ord. 311/2015', 'ru': 'Приказы № 222/2017 и № 311/2015'},
        title={'ro': 'Regulile de securitate conform ordinelor MAI nr. 222 și nr. 311',
               'ru': 'Правила безопасности по приказам МВД № 222 и № 311'},
        summary={'ro': 'Compararea regulilor fundamentale de securitate din Regulamentul instrucției tragerii (Ord. 222) și din '
                       'Regulamentul intervenției profesionale (Ord. 311), măsurile în timpul tragerilor și interdicțiile.',
                 'ru': 'Сравнение основных правил безопасности по Положению об огневой подготовке (Приказ 222) и '
                       'Положению о профессиональном вмешательстве (Приказ 311), меры при стрельбах и запреты.'},
        points={'ro': ['Ord. 222: țeava se îndreaptă spre țintă doar dacă aceasta a fost indicată de conducătorul tragerii.',
                       'Ord. 311: țeava se îndreaptă spre adversar doar dacă viața și sănătatea angajatului sau a altor persoane este pusă în pericol și adversarul este identificat și izolat de terți.',
                       'În caz de rateu sau blocare, trăgătorul păstrează poziția, nu manipulează arma, ridică mâna reactivă și așteaptă ordinele.',
                       'Încărcătorul nu se introduce cu forța; armele se păstrează în toc.'],
                'ru': ['Приказ 222: ствол направляется на цель, только если её указал руководитель стрельбы.',
                       'Приказ 311: ствол направляется на противника, только если жизни и здоровью сотрудника или других лиц угрожает опасность, а противник опознан и изолирован от третьих лиц.',
                       'При осечке или задержке стрелок сохраняет положение, не трогает оружие, поднимает свободную руку и ждёт команды.',
                       'Магазин не вставляется с силой; оружие хранится в кобуре.']},
    ),
    'trg-cps-311': dict(
        src='instructia tragerii/Masuri de siguranta Ord 311 NEW.ppt', kind='slides', type='presentation',
        kicker={'ro': 'Ordinul MAI nr. 311/2015', 'ru': 'Приказ МВД № 311/2015'},
        title={'ro': 'Măsurile de siguranță: controlul personal de securitate (CPS)',
               'ru': 'Меры безопасности: личная проверка безопасности оружия (CPS)'},
        summary={'ro': 'Pas cu pas, în fotografii: controlul personal de securitate al pistolului (CPS) și controlul la alimentare (CPS+A), '
                       'pentru prevenirea accidentelor la primirea, predarea și mânuirea armei.',
                 'ru': 'Пошагово, в фотографиях: личная проверка безопасности пистолета (CPS) и проверка при снаряжении (CPS+A) '
                       'для предотвращения несчастных случаев при получении, сдаче и обращении с оружием.'},
        points={'ro': ['Se identifică o direcție nepericuloasă (sau lada cu nisip) și se scoate arma din toc.',
                       'Se demontează încărcătorul și se ține între degetul mic și inelar.',
                       'Se dezasigură arma, manșonul-închizător se trage înapoi și se fixează pe piedică.',
                       'Camera cartușului se verifică vizual și tactil; apoi manșonul se eliberează, cocoșul se dezarmează, arma se asigură.',
                       'Se montează încărcătorul până la țăcănitură și arma se introduce în toc.'],
                'ru': ['Определяется безопасное направление (или ящик с песком), оружие извлекается из кобуры.',
                       'Магазин отделяется и удерживается между мизинцем и безымянным пальцем.',
                       'Оружие снимается с предохранителя, затвор отводится назад и ставится на затворную задержку.',
                       'Патронник проверяется визуально и на ощупь; затем затвор освобождается, курок спускается, оружие ставится на предохранитель.',
                       'Магазин вставляется до характерного щелчка, оружие убирается в кобуру.']},
    ),
    'trg-codificari': dict(
        src='instructia tragerii/Codificari de alerta.ppt', kind='slides', type='presentation',
        kicker={'ro': 'Ordinul MAI nr. 311/2015', 'ru': 'Приказ МВД № 311/2015'},
        title={'ro': 'Codificările de alertă', 'ru': 'Коды тревоги (готовности оружия)'},
        summary={'ro': 'Modul de păstrare și port al armei în funcție de misiune și de pericol: codul alb, galben, orange, roșu și roșu-foc.',
                 'ru': 'Порядок хранения и ношения оружия в зависимости от задачи и угрозы: белый, жёлтый, оранжевый, красный и «красный — огонь».'},
        points={'ro': ['Codul alb — arma în rastel, încărcătorul nealimentat, fără cartuș pe țeavă, arma asigurată.',
                       'Codul galben — arma în toc (sau la umăr), încărcătoarele alimentate, fără cartuș în camera cartușului, arma asigurată.',
                       'Codul orange — amenințare prezumtivă: arma dezasigurată, mâna pe mânerul armei, indexul în prelungirea gărzii trăgaciului.',
                       'Codul roșu — amenințare actuală identificată: cartuș în camera cartușului, arma sub orizontala privirii, indexul în prelungirea gărzii.',
                       'Codul roșu-foc — agresiune actuală: indexul pe trăgaci, se execută „foc”.'],
                'ru': ['Белый код — оружие в пирамиде, магазин не снаряжён, патрона в патроннике нет, оружие на предохранителе.',
                       'Жёлтый код — оружие в кобуре (или на плече), магазины снаряжены, патрона в патроннике нет, на предохранителе.',
                       'Оранжевый код — предполагаемая угроза: оружие снято с предохранителя, рука на рукоятке, указательный палец вдоль спусковой скобы.',
                       'Красный код — реальная опознанная угроза: патрон в патроннике, оружие ниже линии взгляда, палец вдоль спусковой скобы.',
                       '«Красный — огонь» — реальное нападение: палец на спусковом крючке, производится выстрел.']},
    ),
    'trg-legea-218-prez': dict(
        src='instructia tragerii/Legea 218.ppt', kind='slides', type='presentation',
        kicker={'ro': 'Legea nr. 218/2012', 'ru': 'Закон № 218/2012'},
        title={'ro': 'Aplicarea forței fizice, a mijloacelor speciale și a armelor de foc (prezentare)',
               'ru': 'Применение физической силы, специальных средств и огнестрельного оружия (презентация)'},
        summary={'ro': 'Noțiunile, condițiile și limitele aplicării armei de foc conform Legii nr. 218 din 19.10.2012, obligațiile subiecților legii '
                       'și principiul proporționalității.',
                 'ru': 'Понятия, условия и пределы применения огнестрельного оружия по Закону № 218 от 19.10.2012, обязанности субъектов закона '
                       'и принцип соразмерности.'},
        points={'ro': ['Aplicarea armei de foc înseamnă efectuarea unei împușcături asupra țintei.',
                       'Forța, mijloacele speciale și armele de foc se aplică în legitimă apărare, în stare de extremă necesitate sau la reținerea persoanelor.',
                       'Principiul proporționalității: utilizare adecvată, necesară și corespunzătoare scopului urmărit.',
                       'Obligatoriu: avertizarea despre intenția de a recurge la forță, cu timp suficient pentru conformare (cu excepțiile prevăzute de lege).'],
                'ru': ['Применение огнестрельного оружия — производство выстрела по цели.',
                       'Сила, спецсредства и оружие применяются при необходимой обороне, крайней необходимости или задержании лиц.',
                       'Принцип соразмерности: применение должно быть адекватным, необходимым и соответствующим цели.',
                       'Обязательно предупреждение о намерении применить силу с предоставлением времени для выполнения требований (с исключениями, предусмотренными законом).']},
    ),
    'trg-balistica': dict(
        src='instructia tragerii/BALISTICA INTERNA SI EXTERNA.pptx', kind='slides', type='presentation',
        kicker={'ro': 'Balistica', 'ru': 'Баллистика'},
        title={'ro': 'Balistica internă și externă', 'ru': 'Внутренняя и внешняя баллистика'},
        summary={'ro': 'Fenomenul tragerii, perioadele tragerii, viteza inițială, reculul, traiectoria glonțului și factorii care o influențează.',
                 'ru': 'Явление выстрела, периоды выстрела, начальная скорость, отдача, траектория пули и влияющие на неё факторы.'},
        points={'ro': ['Balistica internă studiază procesele din momentul tragerii, mișcarea glonțului în canalul țevii; balistica externă — mișcarea glonțului după ieșirea din țeavă.',
                       'Fenomenul tragerii: percutorul lovește capsa, se aprinde pulberea, presiunea gazelor aruncă glonțul (presiune maximă 2800–2900 kg/cm²).',
                       'Perioadele tragerii: prealabilă, prima (de bază), a doua și a treia (acțiunea gazelor).',
                       'Rateu — capsa nu se aprinde; foc întârziat — ieșirea cu întârziere a glonțului (închizătorul nu se deschide imediat!).',
                       'Doar 25–35% din energia pulberii se consumă pentru imprimarea vitezei glonțului.'],
                'ru': ['Внутренняя баллистика изучает процессы при выстреле и движение пули в канале ствола; внешняя — движение пули после вылета из ствола.',
                       'Явление выстрела: боёк бьёт по капсюлю, воспламеняется порох, давление газов выбрасывает пулю (максимальное давление 2800–2900 кг/см²).',
                       'Периоды выстрела: предварительный, первый (основной), второй и третий (последействие газов).',
                       'Осечка — капсюль не воспламенился; затяжной выстрел — запоздалый вылет пули (затвор сразу не открывать!).',
                       'Лишь 25–35% энергии пороха расходуется на сообщение пуле скорости.']},
    ),
    'trg-cartuse': dict(
        src='instructia tragerii/Cartuse.ppt', kind='slides', type='presentation',
        kicker={'ro': 'Tema: Examinarea cartușelor', 'ru': 'Тема: Изучение патронов'},
        title={'ro': 'Cartușele de calibrul 5,45 × 39 mm', 'ru': 'Патроны калибра 5,45 × 39 мм'},
        summary={'ro': 'Tipurile de cartușe pentru pistolul-mitralieră 5,45 mm și caracteristicile lor: obișnuit, perforant, antiblindaj, trasor, '
                       'cu viteză redusă, cu ricoșare redusă, de manevră și de instruire.',
                 'ru': 'Виды патронов 5,45 мм для автомата и их характеристики: обычный, повышенной пробиваемости, бронебойный, трассирующий, '
                       'уменьшенной скорости, с пониженной рикошетирующей способностью, холостой и учебный.'},
        points={'ro': ['Cartușul obișnuit 5,45 mm: masa 10,5 g, glonțul 3,4 g, viteza inițială 890 m/s.',
                       'Glonțul trasor: masa 3,2 g, distanța de zbor a trasorului — 800 m (TM modernizat — 850 m).',
                       'Glonț cu viteză redusă (US): viteza inițială 300 m/s.',
                       'Cartușul de manevră (orb) și cartușul de instruire (UC) nu conțin glonț de luptă.'],
                'ru': ['Обычный патрон 5,45 мм: масса 10,5 г, пуля 3,4 г, начальная скорость 890 м/с.',
                       'Трассирующая пуля: масса 3,2 г, дальность трассирования — 800 м (модернизированная ТМ — 850 м).',
                       'Пуля уменьшенной скорости (УС): начальная скорость 300 м/с.',
                       'Холостой и учебный (УЧ) патроны не содержат боевой пули.']},
    ),
    'trg-tema-1-coercitive': dict(
        src='instructia tragerii/Tema 1 Masuri corcitive cu aplicarea armei de foc.doc', kind='doc', type='lesson', mode='text',
        kicker={'ro': 'Tema 1 · Proiect de lecție', 'ru': 'Тема 1 · План занятия'},
        title={'ro': 'Măsurile coercitive cu aplicarea armei de foc',
               'ru': 'Принудительные меры с применением огнестрельного оружия'},
        summary={'ro': 'Proiect de lecție practică (180 min): particularitățile dominării cu armă a adversarului, reguli și măsuri de siguranță, '
                       'reguli și procedee de tragere, codificările de alertă.',
                 'ru': 'План практического занятия (180 мин): особенности контроля противника с оружием, правила и меры безопасности, '
                       'правила и приёмы стрельбы, коды тревоги.'},
        points={'ro': ['Subiectul 1 — particularitățile dominării cu armă a adversarului.',
                       'Subiectul 2 — reguli și măsuri de siguranță.',
                       'Subiectul 3 — reguli și procedee de tragere.',
                       'Subiectul 4 — codificările de alertă (Ordinul MAI nr. 311).'],
                'ru': ['Вопрос 1 — особенности контроля (доминирования) над противником с оружием.',
                       'Вопрос 2 — правила и меры безопасности.',
                       'Вопрос 3 — правила и приёмы стрельбы.',
                       'Вопрос 4 — коды тревоги (Приказ МВД № 311).']},
    ),
    'trg-masuri-securitate': dict(
        src='instructia tragerii/Masuri de securitate.pdf', kind='pdf', type='lecture', mode='text',
        kicker={'ro': 'Suport de curs', 'ru': 'Конспект'},
        title={'ro': 'Măsurile de siguranță la mânuirea armei', 'ru': 'Меры безопасности при обращении с оружием'},
        summary={'ro': 'Măsurile de securitate, măsurile la ședințele de tragere de antrenament și de luptă, la curățarea armelor și examinarea cartușelor.',
                 'ru': 'Меры безопасности, меры на тренировочных и боевых стрельбах, при чистке оружия и осмотре патронов.'},
        points={'ro': ['Persoanele care nu au însușit măsurile de siguranță și partea materială a armamentului nu sunt admise la trageri.',
                       'În timpul tragerii — fără grabă și nervozitate; arma permanent în direcția țintei; dezasigurarea numai după luarea poziției și comanda „FOC!”.',
                       'Curățarea armei se face sub supraveghere, în locuri special amenajate, după verificarea camerei cartușului.',
                       'Cartușele se examinează înainte de tragere.'],
                'ru': ['Лица, не усвоившие меры безопасности и материальную часть оружия, к стрельбам не допускаются.',
                       'Во время стрельбы — без спешки и нервозности; оружие постоянно направлено в сторону мишени; снятие с предохранителя — только после изготовки и команды «ОГОНЬ!».',
                       'Чистка оружия — под наблюдением, в специально оборудованных местах, после проверки патронника.',
                       'Патроны осматриваются перед стрельбой.']},
    ),
    'trg-suport-curs': dict(
        src='instructia tragerii/Ofiteri.docx', kind='doc', type='lecture', mode='text',
        kicker={'ro': 'Suport de curs', 'ru': 'Конспект'},
        title={'ro': 'Balistica, regulile tragerii, măsurile de siguranță, pistolul Makarov și AK-74',
               'ru': 'Баллистика, правила стрельбы, меры безопасности, пистолет Макарова и АК-74'},
        summary={'ro': 'Suport teoretic complet: balistica internă și externă, noțiuni despre trageri și ochire, reguli și măsuri de siguranță, '
                       'construcția, demontarea și montarea pistolului Makarov (PM) și a pistolului-mitralieră AKM/AK-74.',
                 'ru': 'Полный теоретический конспект: внутренняя и внешняя баллистика, понятия о стрельбе и прицеливании, правила и меры безопасности, '
                       'устройство, разборка и сборка пистолета Макарова (ПМ) и автомата АКМ/АК-74.'},
        points={'ro': ['Viteza inițială depinde de lungimea țevii, greutatea glonțului, temperatura și umiditatea încărcăturii.',
                       'Noțiuni despre trageri și ochire: traiectoria glonțului, distanța loviturii directe, împrăștierea gloanțelor.',
                       'Pistolul Makarov (PM) de 9 mm: calitățile de luptă, piesele și mecanismele principale, demontarea parțială și completă.',
                       'AKM / AK-74: construcția, ordinea demontării incomplete și a montării.'],
                'ru': ['Начальная скорость зависит от длины ствола, массы пули, температуры и влажности заряда.',
                       'Понятия о стрельбе и прицеливании: траектория пули, дальность прямого выстрела, рассеивание пуль.',
                       '9-мм пистолет Макарова (ПМ): боевые свойства, основные части и механизмы, неполная и полная разборка.',
                       'АКМ / АК-74: устройство, порядок неполной разборки и сборки.']},
    ),
    'trg-ordin-222': dict(
        src='instructia tragerii/ord.222-17 Instructia trageri in cadrul MAI.pdf', kind='scan', type='order', mode='pages',
        kicker={'ro': 'Ordinul MAI nr. 222 din 20.07.2017', 'ru': 'Приказ МВД № 222 от 20.07.2017'},
        title={'ro': 'Regulamentul cu privire la instrucția tragerii în cadrul MAI (ordinul scanat)',
               'ru': 'Положение об огневой подготовке в МВД (скан приказа)'},
        summary={'ro': 'Ordinul de aprobare a Regulamentului instrucției tragerii în cadrul MAI (abrogă Ordinul MAI nr. 223/2004), '
                       'cu anexele — documentul original scanat.',
                 'ru': 'Приказ об утверждении Положения об огневой подготовке в МВД (отменяет Приказ МВД № 223/2004) '
                       'с приложениями — оригинальный отсканированный документ.'},
        points={'ro': ['Emis în temeiul Legii nr. 288/2016 și al Legii nr. 218/2012.',
                       'Conducătorii subdiviziunilor asigură implementarea Regulamentului.',
                       'Textul regulamentului în format editabil — vezi „Regulamentul cu privire la instrucția tragerii (redacție nouă)”.'],
                'ru': ['Издан на основании Закона № 288/2016 и Закона № 218/2012.',
                       'Руководители подразделений обеспечивают внедрение Положения.',
                       'Текст положения в текстовом виде — см. «Положение об огневой подготовке (новая редакция)».']},
    ),
    'trg-regulament-nou': dict(
        src='instructia tragerii/ordin/ORIGINAL final regiulametnul privind instructia tragerii..doc', kind='doc', type='regulation', mode='text',
        kicker={'ro': 'Regulament · redacție nouă (proiect)', 'ru': 'Положение · новая редакция (проект)'},
        title={'ro': 'Regulamentul cu privire la instrucția tragerii în cadrul MAI',
               'ru': 'Положение об огневой подготовке в МВД'},
        summary={'ro': 'Proiectul noii redacții a Regulamentului instrucției tragerii (prevede abrogarea Ordinului nr. 222/2017): '
                       'organizarea instruirii, exercițiile de tragere, normativele și măsurile de siguranță.',
                 'ru': 'Проект новой редакции Положения об огневой подготовке (предусматривает отмену Приказа № 222/2017): '
                       'организация обучения, стрелковые упражнения, нормативы и меры безопасности.'},
        points={'ro': ['Stabilește sistemul complex de activități de instruire a tragerii pentru angajații MAI.',
                       'Cuprinde organizarea ședințelor, condițiile exercițiilor și normativele de control.',
                       'Document în format text — se poate căuta și citi comod pe telefon.'],
                'ru': ['Устанавливает комплексную систему мероприятий по огневой подготовке сотрудников МВД.',
                       'Включает организацию занятий, условия упражнений и контрольные нормативы.',
                       'Текстовый документ — удобно искать и читать с телефона.']},
    ),
    'trg-ordin-311': dict(
        src='instructia tragerii/ordin/ord.311-15.docx', kind='doc', type='order', mode='text',
        kicker={'ro': 'Ordinul MAI nr. 311 din 17.11.2015', 'ru': 'Приказ МВД № 311 от 17.11.2015'},
        title={'ro': 'Regulamentul cu privire la intervenția profesională a angajaților cu statut special din cadrul MAI',
               'ru': 'Положение о профессиональном вмешательстве сотрудников с особым статусом МВД'},
        summary={'ro': 'Actul de bază al intervenției profesionale: noțiuni, obiective și principii, avertizarea și somarea, intervenția graduală, '
                       'zonele de protecție, codificările de alertă și măsurile de siguranță la mânuirea armei.',
                 'ru': 'Основной акт о профессиональном вмешательстве: понятия, цели и принципы, предупреждение и требование, поэтапное вмешательство, '
                       'зоны защиты, коды тревоги и меры безопасности при обращении с оружием.'},
        points={'ro': ['Abrogă Ordinul MAI nr. 40/2006 privind tactica specială a măsurilor de intervenție.',
                       'Definește noțiunile: adversar, distanță de protecție (2–3 pași), dispozitiv de control, element de control și de sprijin.',
                       'Stabilește fazele intervenției graduale și regulile de avertizare/somare.',
                       'Prevede codificările de alertă (alb, galben, orange, roșu, roșu-foc) și controlul personal de securitate.'],
                'ru': ['Отменяет Приказ МВД № 40/2006 о специальной тактике мер вмешательства.',
                       'Определяет понятия: противник, дистанция защиты (2–3 шага), контрольное построение, контролирующий и страхующий элементы.',
                       'Устанавливает фазы поэтапного вмешательства и правила предупреждения/требования.',
                       'Предусматривает коды тревоги (белый, жёлтый, оранжевый, красный, «красный — огонь») и личную проверку безопасности оружия.']},
    ),
    'trg-legea-218': dict(
        src='instructia tragerii/ordin/legea 218.docx', kind='doc', type='law', mode='text',
        kicker={'ro': 'Legea nr. 218 din 19.10.2012', 'ru': 'Закон № 218 от 19.10.2012'},
        title={'ro': 'Legea privind modul de aplicare a forței fizice, a mijloacelor speciale și a armelor de foc',
               'ru': 'Закон о порядке применения физической силы, специальных средств и огнестрельного оружия'},
        summary={'ro': 'Temeiurile, condițiile și limitele aplicării forței fizice, a mijloacelor speciale și a armelor de foc; '
                       'avertizarea, garanțiile și răspunderea subiecților legii.',
                 'ru': 'Основания, условия и пределы применения физической силы, специальных средств и огнестрельного оружия; '
                       'предупреждение, гарантии и ответственность субъектов закона.'},
        points={'ro': ['Aplicarea forței este o acțiune de constrângere administrativă, admisă doar în condițiile și limitele legii.',
                       'Noțiuni-cheie: rezistență armată, atac armat, pericolul aplicării armei de foc, principiul proporționalității.',
                       'Avertizarea prealabilă este obligatorie, cu excepțiile prevăzute de lege.',
                       'Art. 12: se interzice aplicarea armei de foc împotriva minorilor (vârsta evidentă sau cunoscută), femeilor, persoanelor în etate și celor cu semne vizibile de invaliditate — cu excepția atacului în grup sau cu utilizarea armelor.'],
                'ru': ['Применение силы — мера административного принуждения, допустимая только в условиях и пределах закона.',
                       'Ключевые понятия: вооружённое сопротивление, вооружённое нападение, угроза применения оружия, принцип соразмерности.',
                       'Предварительное предупреждение обязательно, за исключениями, предусмотренными законом.',
                       'Ст. 12: запрещено применять оружие против несовершеннолетних (возраст очевиден или известен), женщин, пожилых и лиц с явными признаками инвалидности — кроме случаев группового или вооружённого нападения.']},
    ),
    'trg-legea-130': dict(
        src='instructia tragerii/ordin/LEGE 130.docx', kind='doc', type='law', mode='text',
        kicker={'ro': 'Legea nr. 130 din 08.06.2012', 'ru': 'Закон № 130 от 08.06.2012'},
        title={'ro': 'Legea privind regimul armelor și al munițiilor cu destinație civilă',
               'ru': 'Закон о режиме оружия и боеприпасов гражданского назначения'},
        summary={'ro': 'Categoriile de arme și muniții cu destinație civilă, condițiile de procurare, deținere, port și folosire, '
                       'licențele și permisele, evidența și controlul armelor.',
                 'ru': 'Категории гражданского оружия и боеприпасов, условия приобретения, хранения, ношения и использования, '
                       'лицензии и разрешения, учёт и контроль оружия.'},
        points={'ro': ['Nu se extinde asupra armelor militare din dotarea autorităților de apărare, securitate și ordine publică.',
                       'Art. 2 definește noțiunile de bază: armă, armă letală/neletală, muniție, permis de armă etc.',
                       'Stabilește categoriile de arme și operațiunile permise pe teritoriul Republicii Moldova.'],
                'ru': ['Не распространяется на боевое оружие органов обороны, безопасности и общественного порядка.',
                       'Ст. 2 определяет основные понятия: оружие, летальное/нелетальное оружие, боеприпасы, разрешение на оружие и др.',
                       'Устанавливает категории оружия и разрешённые операции на территории Республики Молдова.']},
    ),
    'trg-regim-armament': dict(
        src='instructia tragerii/ordin/Anexa nr146 ordinul.doc', kind='doc', type='regulation', mode='text',
        kicker={'ro': 'Anexa la Ordinul MAI nr. 146', 'ru': 'Приложение к Приказу МВД № 146'},
        title={'ro': 'Regulamentul cu privire la regimul juridic al armamentului și mijloacelor speciale',
               'ru': 'Положение о правовом режиме вооружения и специальных средств'},
        summary={'ro': 'Evidența, inventarierea, circulația, păstrarea (la depozit și în subdiviziuni), mentenanța, casarea și controlul '
                       'armamentului și mijloacelor speciale din cadrul MAI.',
                 'ru': 'Учёт, инвентаризация, движение, хранение (на складе и в подразделениях), обслуживание, списание и контроль '
                       'вооружения и специальных средств МВД.'},
        points={'ro': ['Capitolul I — dispoziții generale.',
                       'Capitolul II — evidența și inventarierea, circulația și păstrarea, mentenanța și casarea, controlul armamentului.',
                       'Anexe — formularele actelor de evidență și termenele de păstrare.'],
                'ru': ['Глава I — общие положения.',
                       'Глава II — учёт и инвентаризация, движение и хранение, обслуживание и списание, контроль вооружения.',
                       'Приложения — формы учётных документов и сроки хранения.']},
    ),
    'trg-ghid-interventie': dict(
        src='instructia tragerii/ordin/ghid_privind_interventia_profesionala_in_exercitiul_functiei (1).pdf', kind='pdf', type='guide', mode='pages',
        kicker={'ro': 'Ghid', 'ru': 'Руководство'},
        title={'ro': 'Ghid privind intervenția profesională în exercițiul funcției',
               'ru': 'Руководство по профессиональному вмешательству при исполнении служебных обязанностей'},
        summary={'ro': 'Ghid ilustrat care uniformizează practicile și tehnicile de intervenție: zonele de percuție și traumatism, părțile corpului, '
                       'pozițiile, avertizarea, contactarea, legitimarea, controlul corporal, imobilizarea și încătușarea.',
                 'ru': 'Иллюстрированное руководство, унифицирующее практику и приёмы вмешательства: зоны поражения и травматизма, части тела, '
                       'стойки, предупреждение, контакт, проверка документов, досмотр, обездвиживание и надевание наручников.'},
        points={'ro': ['Scopul — uniformizarea practicilor, procedeelor și tehnicilor de intervenție profesională.',
                       'Zonele de percuție și traumatism — suprafețele corpului unde loviturile sunt permise sau interzise.',
                       'Partea cu arma și partea reactivă a corpului; atitudinea persoanei (cooperantă sau agresivă).',
                       'Recomandat pentru citire în modul „Original” — conține multe ilustrații.'],
                'ru': ['Цель — унификация практики, приёмов и техник профессионального вмешательства.',
                       'Зоны поражения и травматизма — участки тела, удары по которым разрешены или запрещены.',
                       'Сторона с оружием и «реактивная» сторона тела; поведение лица (сотрудничающее или агрессивное).',
                       'Рекомендуется читать в режиме «Оригинал» — много иллюстраций.']},
    ),

    # ------------------------------------------------------------------ PRIM AJUTOR
    'pa-svb': dict(
        src='Prim ajutor/SVB la adult.pptx', kind='slides', type='presentation',
        kicker={'ro': 'Serviciul Medical al MAI', 'ru': 'Медицинская служба МВД'},
        title={'ro': 'Suport vital bazal la adult', 'ru': 'Базовая сердечно-лёгочная реанимация у взрослых'},
        summary={'ro': 'Analiza situației și măsurile de siguranță, lanțul supraviețuirii, evaluarea victimei (piele, ochi, respirație, puls), '
                       'resuscitarea cardiopulmonară și utilizarea defibrilatorului automat extern.',
                 'ru': 'Оценка обстановки и меры безопасности, цепочка выживания, оценка пострадавшего (кожа, глаза, дыхание, пульс), '
                       'сердечно-лёгочная реанимация и использование автоматического наружного дефибриллятора.'},
        points={'ro': ['Primul ajutor acordat la momentul potrivit poate salva vieți — este o abilitate pe care trebuie să o aibă oricine.',
                       'Lanțul supraviețuirii: recunoașterea precoce și apelarea ajutorului, RCP precoce, defibrilarea precoce, îngrijirea post-resuscitare.',
                       'Orice persoană areactivă, cu respirație anormală sau absentă, se suspectează de stop cardiorespirator.',
                       'Evaluarea victimei: culoarea pielii (paliditate, cianoză, hiperemie, icter), pupilele, respirația, pulsul.',
                       'Dispecerul medical ghidează martorii pentru RCP prin telefon până la sosirea echipajului.'],
                'ru': ['Своевременно оказанная первая помощь спасает жизни — этим навыком должен владеть каждый.',
                       'Цепочка выживания: раннее распознавание и вызов помощи, ранняя СЛР, ранняя дефибрилляция, постреанимационная помощь.',
                       'При отсутствии реакции и ненормальном или отсутствующем дыхании подозревают остановку сердца.',
                       'Оценка пострадавшего: цвет кожи (бледность, цианоз, гиперемия, желтуха), зрачки, дыхание, пульс.',
                       'Диспетчер скорой помощи руководит свидетелями при СЛР по телефону до прибытия бригады.']},
    ),
    'pa-112': dict(
        src='Prim ajutor/Dirijarea_operationala_in_procesul_receptionarii_informatiei.pptx', kind='slides', type='presentation',
        kicker={'ro': 'Serviciul 112', 'ru': 'Служба 112'},
        title={'ro': 'Dirijarea operațională în procesul recepționării informației',
               'ru': 'Оперативное управление при приёме информации'},
        summary={'ro': 'Serviciul național unic pentru apelurile de urgență 112: misiune, cadru normativ, funcții, organizare, competențele operatorilor, '
                       'preluarea și procesarea apelurilor, fișa apelului, eCall și conferința cu dispecerii serviciilor specializate.',
                 'ru': 'Национальная единая служба экстренных вызовов 112: миссия, нормативная база, функции, структура, компетенции операторов, '
                       'приём и обработка вызовов, карточка вызова, eCall и конференц-связь с диспетчерами экстренных служб.'},
        points={'ro': ['Serviciul 112 — creat prin HG nr. 243/2016, subordonat MAI; funcționează 24/7, apel gratuit de pe orice telefon, inclusiv SMS.',
                       'Cadrul normativ: Legea nr. 174/2014, HG nr. 647/2018, HG nr. 243/2016.',
                       'Funcții: preluarea apelurilor, interogarea apelantului, localizarea, alertarea serviciilor specializate de urgență (SSU).',
                       'Două centre de preluare a apelurilor în Chișinău, care se rezervă reciproc.',
                       'Pentru persoanele cu dizabilități de auz și vorbire — serviciul SMS și aplicația 112MD.'],
                'ru': ['Служба 112 создана Постановлением Правительства № 243/2016, подчинена МВД; работает 24/7, звонок бесплатный с любого телефона, есть SMS.',
                       'Нормативная база: Закон № 174/2014, ПП № 647/2018, ПП № 243/2016.',
                       'Функции: приём вызовов, опрос заявителя, определение местоположения, оповещение специализированных экстренных служб (SSU).',
                       'Два центра приёма вызовов в Кишинёве, резервирующие друг друга.',
                       'Для людей с нарушениями слуха и речи — SMS-сервис и приложение 112MD.']},
        media='video',  # embed the video; call recordings (audio) are not published
    ),
    'pa-sinteza': dict(
        src='Prim ajutor/SINTEZA GENERALITATI 1 ajutor medical.pdf', kind='pdf', type='lecture', mode='text',
        kicker={'ro': 'Sinteză', 'ru': 'Конспект'},
        title={'ro': 'Bazele cunoștințelor medicale: generalități despre primul ajutor',
               'ru': 'Основы медицинских знаний: общие сведения о первой помощи'},
        summary={'ro': 'Principiile de bază ale primului ajutor, sprijinul emoțional al victimei, concepțiile greșite care împiedică intervenția '
                       'și cele patru etape principale ale acordării primului ajutor.',
                 'ru': 'Основные принципы первой помощи, эмоциональная поддержка пострадавшего, ошибочные убеждения, мешающие помочь, '
                       'и четыре основных этапа оказания первой помощи.'},
        points={'ro': ['Începem întotdeauna cu întrebarea „Ce observi?” — evaluarea situației și a pericolelor.',
                       'Oferă victimei sprijin emoțional; gândește-te și la propriile reacții după intervenție.',
                       'Concepții greșite: „nu poate fi atât de grav”, „altcineva va ajuta”, „nu sunt obligat să ajut”, „mă tem să nu mă infectez”.',
                       'Patru etape principale: siguranța, evaluarea, alertarea serviciilor de urgență, acordarea primului ajutor.'],
                'ru': ['Всегда начинаем с вопроса «Что ты видишь?» — оценка ситуации и опасностей.',
                       'Окажи пострадавшему эмоциональную поддержку; подумай и о своих реакциях после помощи.',
                       'Ошибочные убеждения: «не может быть так серьёзно», «кто-то другой поможет», «я не обязан помогать», «боюсь заразиться».',
                       'Четыре основных этапа: безопасность, оценка, вызов экстренных служб, оказание первой помощи.']},
    ),
    'pa-ipssm': dict(
        src='Prim ajutor/IPSSM 15 -2020 Prim-ajutor.pdf', kind='pdf', type='instruction', mode='text',
        kicker={'ro': 'IPSSM cod 15/2020', 'ru': 'Инструкция ОТ № 15/2020'},
        title={'ro': 'Instrucțiuni proprii SSM pentru acordarea primului ajutor',
               'ru': 'Инструкция по охране труда по оказанию первой помощи'},
        summary={'ro': 'Procedeele de acordare a primului ajutor: stopul respirator, șocul, leșinul, pansamentele și bandajele, transportul accidentaților, '
                       'arsurile, fracturile, plăgile, hemoragiile, electrocutarea, leziunile ochiului și otrăvirile, plus procedura practică la locul accidentului.',
                 'ru': 'Приёмы первой помощи: остановка дыхания, шок, обморок, повязки и бинтование, транспортировка пострадавших, '
                       'ожоги, переломы, раны, кровотечения, электротравма, травмы глаз и отравления, а также порядок действий на месте происшествия.'},
        points={'ro': ['Scop: însușirea procedeelor de acordare a primului ajutor în diverse situații.',
                       'Procedura la locul accidentului: 1) victima nu respiră și nu are puls; 2) nu respiră, dar are puls; 3) respiră și are puls.',
                       'Primul ajutor se acordă rapid, fără a pune în pericol salvatorul.'],
                'ru': ['Цель: освоение приёмов оказания первой помощи в различных ситуациях.',
                       'Порядок на месте происшествия: 1) пострадавший не дышит и нет пульса; 2) не дышит, но есть пульс; 3) дышит и есть пульс.',
                       'Помощь оказывается быстро, не подвергая опасности спасателя.']},
    ),
    'pa-manual': dict(
        src='Prim ajutor/Manual-de-prim-ajutor-Crucea-Rosie.pdf', kind='pdf', type='manual', mode='pages',
        kicker={'ro': 'Crucea Roșie', 'ru': 'Красный Крест'},
        title={'ro': 'Manual european de prim ajutor', 'ru': 'Европейское руководство по первой помощи'},
        summary={'ro': 'Manual ilustrat: principiile de bază, etapele principale ale acordării primului ajutor, suportul vital de bază și '
                       'defibrilarea externă automată, primul ajutor în traumatisme, hemoragii, arsuri, intoxicații și alte urgențe.',
                 'ru': 'Иллюстрированное руководство: основные принципы, этапы оказания первой помощи, базовая реанимация и '
                       'автоматическая наружная дефибрилляция, помощь при травмах, кровотечениях, ожогах, отравлениях и других неотложных состояниях.'},
        points={'ro': ['Principiile de bază și etapele principale ale acordării primului ajutor.',
                       'Suport vital de bază și defibrilare externă automată (DEA).',
                       'Hemoragii, plăgi, arsuri, fracturi, intoxicații și alte urgențe.',
                       'Recomandat pentru citire în modul „Original” — conține multe ilustrații.'],
                'ru': ['Основные принципы и этапы оказания первой помощи.',
                       'Базовая реанимация и автоматическая наружная дефибрилляция (АНД).',
                       'Кровотечения, раны, ожоги, переломы, отравления и другие неотложные состояния.',
                       'Рекомендуется читать в режиме «Оригинал» — много иллюстраций.']},
    ),

    # ------------------------------------------------------------------ TIP
    'tip-tema-1': dict(
        src='TIP/Tema 1 Actiuni tactice a masurilor de interventie.pdf', kind='pdf', type='lecture', mode='text',
        kicker={'ro': 'Tema 1', 'ru': 'Тема 1'},
        title={'ro': 'Acțiuni tactice ale măsurilor de intervenție', 'ru': 'Тактические действия при мерах вмешательства'},
        summary={'ro': 'Noțiunile generale ale intervenției profesionale, obiectivele și principiile care stau la baza acesteia.',
                 'ru': 'Основные понятия профессионального вмешательства, его цели и принципы.'},
        points={'ro': ['Noțiuni: acțiuni coercitive, adversar, direcție nepericuloasă, distanța de protecție (2–3 pași), dispozitiv de control, element de control și de sprijin, imobilizare, triunghi de agresiune.',
                       'Obiective: dominarea adversarului prin negociere, descurajare și nivelul de forță strict necesar; promovarea imaginii pozitive a MAI.',
                       'Principii: legalitatea, inviolabilitatea persoanei, egalitatea și nediscriminarea, profesionalismul, confidențialitatea.'],
                'ru': ['Понятия: принудительные действия, противник, безопасное направление, дистанция защиты (2–3 шага), контрольное построение, контролирующий и страхующий элементы, обездвиживание, треугольник агрессии.',
                       'Цели: подчинение противника путём переговоров, сдерживания и строго необходимого уровня силы; позитивный имидж МВД.',
                       'Принципы: законность, неприкосновенность личности, равенство и недискриминация, профессионализм, конфиденциальность.']},
    ),
    'tip-tema-2': dict(
        src='TIP/Tema 2 Formarea generala in inerventia profesionala.pdf', kind='pdf', type='lecture', mode='text',
        kicker={'ro': 'Tema 2', 'ru': 'Тема 2'},
        title={'ro': 'Formarea generală în intervenția profesională', 'ru': 'Общая подготовка в профессиональном вмешательстве'},
        summary={'ro': 'Avertizarea și somarea, nivelurile de agresivitate, intervenția graduală, zonele și distanțele de protecție, zonele de percuție, '
                       'pozițiile de gardă, plasările de securitate și tehnicile de comunicare în situații de criză.',
                 'ru': 'Предупреждение и требование (окрик), уровни агрессивности, поэтапное вмешательство, зоны и дистанции защиты, зоны поражения, '
                       'защитные стойки, расположение для безопасности и техники общения в кризисных ситуациях.'},
        points={'ro': ['Avertizarea atenționează persoana despre acțiunile legale în caz de nesupunere; somarea este o cerință imperativă (ordin). Se efectuează în limba de stat.',
                       'Somația la aplicarea armei: „STAI! POLIȚIA!”, apoi „STAI CĂ TRAG!”, apoi foc în plan vertical (în încăperi — interzis).',
                       'Comportamentul persoanei: cooperant, agresivitate redusă, medie, sporită.',
                       'Intervenția graduală — patru faze, de la acțiuni preventive nonviolente până la aplicarea forței, mijloacelor speciale și a armei de foc.'],
                'ru': ['Предупреждение сообщает лицу о законных мерах в случае неподчинения; требование (окрик) — императивный приказ. Выполняются на государственном языке.',
                       'Окрик при применении оружия: «СТОЙ! ПОЛИЦИЯ!», затем «СТОЙ, СТРЕЛЯЮ!», затем выстрел вверх (в помещениях — запрещено).',
                       'Поведение лица: сотрудничающее, низкая, средняя, повышенная агрессивность.',
                       'Поэтапное вмешательство — четыре фазы: от ненасильственных превентивных действий до применения силы, спецсредств и оружия.']},
    ),
    'tip-tema-3': dict(
        src='TIP/Tema 3 Actiuni tactice in timpul contactari si legitimarii persoanei.pdf', kind='pdf', type='lecture', mode='text',
        kicker={'ro': 'Tema 3', 'ru': 'Тема 3'},
        title={'ro': 'Acțiuni tactice în timpul contactării și legitimării persoanei',
               'ru': 'Тактические действия при контакте и проверке документов'},
        summary={'ro': 'Regulile tactice la contactarea persoanei, legitimarea și stabilirea identității, situațiile neprevăzute și '
                       'legitimarea persoanei aflate în mijlocul de transport.',
                 'ru': 'Тактические правила при контакте с лицом, проверка документов и установление личности, непредвиденные ситуации и '
                       'проверка лица, находящегося в транспортном средстве.'},
        points={'ro': ['Contactarea persoanei — primul pas al intervenției, cu respectarea distanței de protecție și a plasării de securitate.',
                       'Legitimarea și stabilirea identității persoanelor — temeiuri și reguli tactice.',
                       'Situații neprevăzute în timpul legitimării și modul lor de rezolvare.',
                       'Reguli tactice la legitimarea persoanei aflate în mijlocul de transport.'],
                'ru': ['Контакт с лицом — первый шаг вмешательства, с соблюдением дистанции защиты и безопасного расположения.',
                       'Проверка документов и установление личности — основания и тактические правила.',
                       'Непредвиденные ситуации при проверке документов и способы их разрешения.',
                       'Тактические правила при проверке лица, находящегося в транспортном средстве.']},
    ),
    'tip-tema-4': dict(
        src='TIP/Tema 4 Masuri de interventie la controlul corporal preventiv,bagajelor,perchezitia..pdf', kind='pdf', type='lecture', mode='text',
        kicker={'ro': 'Tema 4', 'ru': 'Тема 4'},
        title={'ro': 'Măsuri de intervenție la controlul corporal, controlul bagajelor și percheziția corporală',
               'ru': 'Меры вмешательства при личном досмотре, досмотре багажа и личном обыске'},
        summary={'ro': 'Controlul corporal preventiv și regulile tactice, controlul bagajelor, percheziția corporală și regulile tactice în timpul percheziției.',
                 'ru': 'Превентивный личный досмотр и тактические правила, досмотр багажа, личный обыск и тактические правила при обыске.'},
        points={'ro': ['Controlul corporal preventiv — măsură de siguranță pentru depistarea obiectelor periculoase.',
                       'Regulile tactice: poziția persoanei, plasarea elementului de control și a celui de sprijin.',
                       'Controlul bagajelor se efectuează cu respectarea măsurilor de siguranță.',
                       'Percheziția corporală este de două feluri: sumară (incompletă) și amănunțită (completă).'],
                'ru': ['Превентивный личный досмотр — мера безопасности для обнаружения опасных предметов.',
                       'Тактические правила: положение лица, расположение контролирующего и страхующего элементов.',
                       'Досмотр багажа проводится с соблюдением мер безопасности.',
                       'Личный обыск бывает двух видов: поверхностный (неполный) и тщательный (полный).']},
    ),
    'tip-tema-5': dict(
        src='TIP/Tema 5 Masurile de interventie la aplicarea fortei fizice si a mij speciale.pdf', kind='pdf', type='lecture', mode='text',
        kicker={'ro': 'Tema 5', 'ru': 'Тема 5'},
        title={'ro': 'Măsuri de intervenție la aplicarea forței fizice și a mijloacelor speciale',
               'ru': 'Меры вмешательства при применении физической силы и специальных средств'},
        summary={'ro': 'Invitarea și aducerea persoanelor la sediul poliției (pe jos și cu transportul auto), procedeele de imobilizare și aducere prin forță, '
                       'aplicarea forței fizice și a mijloacelor speciale, utilizarea mijloacelor de imobilizare și a câinilor de serviciu.',
                 'ru': 'Приглашение и доставление лиц в полицию (пешком и автотранспортом), приёмы обездвиживания и доставления с применением силы, '
                       'применение физической силы и спецсредств, использование средств обездвиживания и служебных собак.'},
        points={'ro': ['Aducerea persoanelor la sediul poliției — pe jos sau cu mijloace de transport; cu autoturismul se aduc cel mult două persoane.',
                       'Procedeele de imobilizare și aducerea prin folosirea forței.',
                       'Utilizarea mijloacelor de imobilizare (cătușe etc.).',
                       'Câinii de serviciu: cu botniță și fără lesă, fără botniță și în lesă, fără botniță și fără lesă — în situațiile prevăzute.'],
                'ru': ['Доставление в полицию — пешком или транспортом; легковым автомобилем доставляется не более двух человек.',
                       'Приёмы обездвиживания и доставление с применением силы.',
                       'Использование средств обездвиживания (наручники и др.).',
                       'Служебные собаки: в наморднике без поводка, без намордника на поводке, без намордника и без поводка — в предусмотренных случаях.']},
    ),

    # ------------------------------------------------------------------ GENERAL
    'info-formare-initiala': dict(
        src='instructia tragerii/prezentarea Formarea initiala.pptx', kind='slides', type='presentation',
        kicker={'ro': 'Despre curs', 'ru': 'О курсе'},
        title={'ro': 'Formarea inițială a ofițerilor — prezentarea cursului',
               'ru': 'Первоначальная подготовка офицеров — презентация курса'},
        summary={'ro': 'Ce este formarea inițială, actele normative, programul de studii (module și ore), stagiul de practică, '
                       'evaluarea finală, obligațiile cursanților și cazurile de excludere.',
                 'ru': 'Что такое первоначальная подготовка, нормативные акты, учебная программа (модули и часы), практика, '
                       'итоговая аттестация, обязанности слушателей и основания для отчисления.'},
        points={'ro': ['Durata: 16 săptămâni — 11 săptămâni de studii, 3 săptămâni de stagiu de practică, 2 săptămâni de sinteză și evaluare finală.',
                       'Competențe generale — 280 de ore (module I–VII), inclusiv „Intervenția profesională” (68 ore) și „Pregătirea tactică” (42 ore).',
                       'Competențe specifice (specializare) — 160 de ore.',
                       'Evaluarea finală: partea teoretică și partea practică, în fața Comisiei de evaluare.',
                       'Cursanții sunt obligați să frecventeze orele, să studieze tematica și să respecte regulamentele instituției.'],
                'ru': ['Продолжительность: 16 недель — 11 недель обучения, 3 недели практики, 2 недели обобщения и итоговой аттестации.',
                       'Общие компетенции — 280 часов (модули I–VII), в том числе «Профессиональное вмешательство» (68 ч) и «Тактическая подготовка» (42 ч).',
                       'Специальные компетенции (специализация) — 160 часов.',
                       'Итоговая аттестация: теоретическая и практическая части перед аттестационной комиссией.',
                       'Слушатели обязаны посещать занятия, изучать темы и соблюдать внутренний распорядок учебного заведения.']},
        redact_re=[r'(?<!\d)0\d{8}(?!\d)'],  # personal phone numbers (slide 2) are covered on images and text
    ),
}
