/* Orarul Plutonului 131 — transcris după orarele săptămânale aprobate (fotografiile din folderul Orar).
   Editare: fiecare lecție este [interval, disciplină, profesori]; intervalele sunt în `slots`,
   disciplinele în `subjects`. Săptămânile încep luni (`start`), zilele merg luni → vineri. */
window.LIB_ORAR = {
  group: 'Plutonul 131',
  updated: '2026-11-12',
  program: {
    ro: 'Instruirea inițială a ofițerilor debutanți de nivel B03 · competențe profesionale generale',
    ru: 'Первоначальная подготовка начинающих офицеров уровня B03 · общие профессиональные компетенции'
  },
  // a–e: intervalele obișnuite; x: examen (orar indicat doar ora de început)
  slots: {
    a: ['08:30', '10:00'], b: ['10:10', '11:40'], c: ['11:50', '13:20'],
    d: ['14:30', '16:00'], e: ['16:10', '17:40'], x: ['16:10', null]
  },
  // modulele programului de formare inițială (ore conform programului de studii)
  modules: {
    I:   { color: '#475569', hours: 22, ro: 'Încadrarea profesională în cadrul sistemului MAI', ru: 'Профессиональная интеграция в систему МВД' },
    II:  { color: '#0e7490', hours: 20, ro: 'Protecția juridică a drepturilor omului. Egalitatea de gen și prevenirea discriminării', ru: 'Правовая защита прав человека. Гендерное равенство и предотвращение дискриминации' },
    III: { color: '#7c3aed', hours: 42, ro: 'Integritatea și deontologia profesională. Tehnici de comunicare și aspecte psihologice în activitatea profesională', ru: 'Неподкупность и профессиональная деонтология. Техники общения и психологические аспекты профессиональной деятельности' },
    IV:  { color: '#dc2626', hours: 68, ro: 'Intervenția profesională', ru: 'Профессиональное вмешательство' },
    V:   { color: '#2563eb', hours: 42, ro: 'Pregătirea tactică', ru: 'Тактическая подготовка' },
    VI:  { color: '#b45309', hours: 46, ro: 'Instrumente de examinare și reglementare a faptelor penale', ru: 'Инструменты рассмотрения и регулирования уголовно наказуемых деяний' },
    VII: { color: '#15803d', hours: 40, ro: 'Rolul subdiviziunilor specializate ale MAI în cooperare cu societatea privind prevenirea faptelor ilicite', ru: 'Роль специализированных подразделений МВД во взаимодействии с обществом по предупреждению противоправных деяний' },
    '':  { color: '#64748b', hours: null, ro: 'Alte discipline', ru: 'Другие дисциплины' }
  },
  // m: modulul · t: tema din modul (VII.2–VII.5) · link: materialele din bibliotecă (curs:<id> sau doc:<id>)
  subjects: {
    cadru:       { m: 'I',   ro: 'Cadrul juridic și sfera de reglementare a activității MAI', ru: 'Правовая база и сфера регулирования деятельности МВД' },
    drepturi:    { m: 'II',  ro: 'Protecția juridică a drepturilor omului', ru: 'Правовая защита прав человека' },
    etica:       { m: 'III', ro: 'Normele de etică și deontologie profesională', ru: 'Нормы этики и профессиональной деонтологии' },
    integritate: { m: 'III', ro: 'Integritate instituțională', ru: 'Институциональная неподкупность', link: 'doc:integritate-fpss' },
    comunicare:  { m: 'III', ro: 'Comunicarea profesională', ru: 'Профессиональная коммуникация' },
    psihologie:  { m: 'III', ro: 'Psihologia judiciară', ru: 'Судебная психология' },
    tip:         { m: 'IV',  ro: 'Tactica intervenției profesionale', ru: 'Тактика профессионального вмешательства', link: 'curs:tip' },
    tragere:     { m: 'IV',  ro: 'Instrucția tragerii', ru: 'Огневая подготовка', link: 'curs:tragere' },
    autoaparare: { m: 'IV',  ro: 'Procedee tactice de luptă și autoapărare', ru: 'Тактические приёмы борьбы и самообороны' },
    medicale:    { m: 'IV',  ro: 'Bazele cunoștințelor medicale', ru: 'Основы медицинских знаний', link: 'curs:prim-ajutor' },
    front:       { m: 'V',   ro: 'Instrucția de front', ru: 'Строевая подготовка', link: 'curs:front' },
    arop:        { m: 'V',   ro: 'Tactica intervenției polițienești la asigurarea și restabilirea ordinii publice', ru: 'Тактика полицейского вмешательства при обеспечении и восстановлении общественного порядка', link: 'curs:arop' },
    tetra:       { m: 'V',   ro: 'Sistemul de comunicații speciale TETRA', ru: 'Система специальной связи TETRA' },
    drone:       { m: 'V',   ro: 'Utilizarea aeronavelor fără pilot la bord în activitatea MAI', ru: 'Использование беспилотных летательных аппаратов в деятельности МВД' },
    civila:      { m: 'V',   ro: 'Protecția civilă', ru: 'Гражданская защита' },
    calificare:  { m: 'VI',  ro: 'Calificarea faptelor prejudiciabile', ru: 'Квалификация общественно опасных деяний' },
    sesizari:    { m: 'VI',  ro: 'Procedura de examinare a sesizărilor cu privire la faptele ilegale', ru: 'Порядок рассмотрения сообщений о противоправных деяниях' },
    prevenire:   { m: 'VI',  ro: 'Prevenirea și combaterea criminalității', ru: 'Предупреждение преступности и борьба с ней' },
    cercetare:   { m: 'VI',  ro: 'Aspecte procesuale și de tactică-criminalistică la cercetarea la fața locului', ru: 'Процессуальные и криминалистико-тактические аспекты осмотра места происшествия' },
    expertize:   { m: 'VI',  ro: 'Constatarea tehnico-științifică și medico-legală', ru: 'Технико-научная и судебно-медицинская констатация' },
    comunitar:   { m: 'VII', t: 2, ro: 'Activitatea polițienească comunitară și rolul subdiviziunilor specializate a MAI în prevenirea faptelor ilegale', ru: 'Общинная полицейская деятельность и роль специализированных подразделений МВД в предупреждении противоправных деяний' },
    violenta:    { m: 'VII', t: 3, ro: 'Rolul subdiviziunilor specializate a MAI privind prevenirea și documentarea cazurilor de violență în familie', ru: 'Роль специализированных подразделений МВД в предупреждении и документировании случаев насилия в семье' },
    copii:       { m: 'VII', t: 4, ro: 'Rolul subdiviziunilor specializate a MAI în activitatea de siguranță a copiilor. Intervenția profesională în cazul delicvenței juvenile', ru: 'Роль специализированных подразделений МВД в обеспечении безопасности детей. Профессиональное вмешательство при подростковой преступности' },
    intruniri:   { m: 'VII', t: 5, ro: 'Rolul subdiviziunilor specializate a MAI privind respectarea drepturilor fundamentale ale omului în cadrul întrunirilor, menținerea, restabilirea și asigurarea ordinii publice', ru: 'Роль специализированных подразделений МВД в соблюдении основных прав человека во время собраний, поддержании, восстановлении и обеспечении общественного порядка' },
    dirijare:    { m: 'VII', ro: 'Dirijarea operațională în procesul recepționării informației', ru: 'Оперативное управление при приёме информации', link: 'doc:pa-112' },
    analiza:     { m: '',    ro: 'Analiza informațiilor', ru: 'Анализ информации' },
    straini:     { m: '',    ro: 'Regimul străinilor în Republica Moldova', ru: 'Режим иностранцев в Республике Молдова' },
    // examene (ora 16:10)
    'ex-I':   { m: 'I',   exam: true, ro: 'Încadrarea profesională în cadrul sistemului MAI', ru: 'Профессиональная интеграция в систему МВД' },
    'ex-II':  { m: 'II',  exam: true, ro: 'Protecția juridică a drepturilor omului. Egalitatea de gen și prevenirea discriminării', ru: 'Правовая защита прав человека. Гендерное равенство и предотвращение дискриминации' },
    'ex-III': { m: 'III', exam: true, ro: 'Etica și deontologia profesională. Integritatea instituțională și prevenirea corupției. Comunicarea profesională. Sănătatea mentală', ru: 'Этика и профессиональная деонтология. Институциональная неподкупность и предупреждение коррупции. Профессиональная коммуникация. Психическое здоровье' },
    'ex-IV':  { m: 'IV',  exam: true, ro: 'Intervenția profesională', ru: 'Профессиональное вмешательство' },
    'ex-V':   { m: 'V',   exam: true, ro: 'Pregătirea tactică', ru: 'Тактическая подготовка' },
    'ex-VI':  { m: 'VI',  exam: true, ro: 'Instrumente de examinare și reglementare a faptelor ilegale', ru: 'Инструменты рассмотрения и регулирования противоправных деяний' },
    'ex-VII': { m: 'VII', exam: true, ro: 'Rolul subdiviziunilor specializate ale MAI în cooperare cu societatea privind prevenirea faptelor ilicite', ru: 'Роль специализированных подразделений МВД во взаимодействии с обществом по предупреждению противоправных деяний' }
  },
  weeks: [
    { start: '2026-11-09', days: [
      [['a', 'cadru', 'I. Mitriuc'], ['b', 'tip', 'V. Buzdugan, N. Gulceac'], ['c', 'integritate', 'E. Șevciuc'], ['d', 'tragere', 'P. Diuvenji, N. Gulceac'], ['e', 'autoaparare', 'S. Remarenco, M. Taran']],
      [['a', 'etica', 'I. Mitriuc'], ['b', 'tip', 'V. Buzdugan, N. Gulceac'], ['c', 'tragere', 'P. Diuvenji, N. Gulceac'], ['d', 'autoaparare', 'S. Remarenco, M. Taran']],
      [['a', 'tetra', 'I. Botnari'], ['b', 'tetra', 'I. Botnari'], ['c', 'medicale', 'I. Vaculin'], ['d', 'medicale', 'I. Vaculin']],
      [['a', 'tip', 'V. Buzdugan, N. Gulceac'], ['b', 'front', 'V. Buzdugan, M. Frunze'], ['c', 'drepturi', 'Ig. Șevcenco']],
      [['a', 'tip', 'V. Buzdugan, N. Gulceac'], ['b', 'front', 'V. Buzdugan, M. Frunze'], ['c', 'tragere', 'P. Diuvenji, N. Gulceac'], ['d', 'tragere', 'P. Diuvenji, N. Gulceac']]
    ] },
    { start: '2026-11-16', days: [
      [['a', 'front', 'V. Buzdugan, M. Frunze'], ['b', 'cadru', 'I. Mitriuc'], ['c', 'tragere', 'P. Diuvenji, N. Gulceac'], ['d', 'tragere', 'P. Diuvenji, N. Gulceac']],
      [['a', 'front', 'V. Buzdugan, M. Frunze'], ['b', 'etica', 'I. Mitriuc'], ['c', 'tragere', 'P. Diuvenji, N. Gulceac'], ['d', 'autoaparare', 'S. Remarenco, M. Taran']],
      [['a', 'tip', 'V. Buzdugan, N. Gulceac'], ['b', 'tip', 'V. Buzdugan, N. Gulceac'], ['c', 'calificare', 'I. Rotaru'], ['d', 'calificare', 'I. Rotaru']],
      [['a', 'tip', 'V. Buzdugan, N. Gulceac'], ['b', 'tip', 'V. Buzdugan, N. Gulceac'], ['c', 'tragere', 'P. Diuvenji, N. Gulceac'], ['d', 'autoaparare', 'S. Remarenco, M. Taran']],
      [['a', 'sesizari', 'A. Andronache'], ['b', 'sesizari', 'A. Andronache'], ['c', 'integritate', 'E. Șevciuc'], ['d', 'drepturi', 'Ig. Șevcenco']]
    ] },
    { start: '2026-11-23', days: [
      [['a', 'arop', 'V. Buzdugan'], ['b', 'cadru', 'I. Mitriuc'], ['c', 'etica', 'I. Mitriuc'], ['d', 'drepturi', 'Ig. Șevcenco']],
      [['a', 'drone', 'V. Munteanu'], ['b', 'drone', 'V. Munteanu'], ['c', 'calificare', 'I. Rotaru'], ['d', 'autoaparare', 'S. Remarenco, M. Taran']],
      [['a', 'arop', 'V. Buzdugan, N. Gulceac'], ['b', 'arop', 'V. Buzdugan, N. Gulceac'], ['c', 'medicale', 'I. Vaculin'], ['d', 'medicale', 'I. Vaculin']],
      [['a', 'arop', 'V. Buzdugan, N. Gulceac'], ['b', 'comunicare', 'N. Rusu'], ['c', 'comunicare', 'N. Rusu'], ['d', 'autoaparare', 'S. Remarenco, M. Taran']],
      [['a', 'prevenire', 'S. Zavtur'], ['b', 'prevenire', 'S. Zavtur'], ['c', 'sesizari', 'D. Ostavciuc, A. Andronache'], ['d', 'sesizari', 'D. Ostavciuc, A. Andronache']]
    ] },
    { start: '2026-11-30', days: [
      [['a', 'cercetare', 'A. Lisov'], ['b', 'cercetare', 'A. Lisov'], ['c', 'expertize', 'A. Lisov'], ['d', 'expertize', 'A. Lisov']],
      [['a', 'psihologie', 'O. Chirița'], ['b', 'psihologie', 'O. Chirița'], ['c', 'cadru', 'I. Mitriuc'], ['d', 'autoaparare', 'S. Remarenco, M. Taran']],
      [['a', 'arop', 'V. Buzdugan, N. Gulceac'], ['b', 'arop', 'V. Buzdugan, N. Gulceac'], ['c', 'comunicare', 'N. Rusu'], ['d', 'comunicare', 'N. Rusu']],
      [['a', 'drone', 'V. Muntean'], ['b', 'drone', 'V. Muntean'], ['c', 'drepturi', 'Ig. Șevcenco'], ['d', 'autoaparare', 'S. Remarenco, M. Taran']],
      [['a', 'prevenire', 'S. Zavtur'], ['b', 'prevenire', 'S. Zavtur'], ['c', 'sesizari', 'D. Ostavciuc, A. Andronache'], ['d', 'sesizari', 'D. Ostavciuc, A. Andronache']]
    ] },
    { start: '2026-12-07', days: [
      [['a', 'civila', 'V. Buzdugan'], ['b', 'comunicare', 'N. Rusu'], ['c', 'comunicare', 'N. Rusu'], ['d', 'cadru', 'I. Mitriuc']],
      [['a', 'violenta', 'M. Maxian'], ['b', 'copii', 'M. Maxian'], ['c', 'intruniri', 'M. Maxian'], ['d', 'autoaparare', 'S. Remarenco, M. Taran'], ['x', 'ex-I', 'I. Mitriuc']],
      [['a', 'arop', 'V. Buzdugan, N. Gulceac'], ['b', 'arop', 'V. Buzdugan, N. Gulceac'], ['c', 'etica', 'I. Mitriuc'], ['d', 'drepturi', 'Ig. Șevcenco']],
      [['a', 'arop', 'V. Buzdugan, N. Gulceac'], ['b', 'civila', 'V. Buzdugan, N. Gulceac'], ['c', 'psihologie', 'O. Chirița'], ['d', 'autoaparare', 'S. Remarenco, M. Taran'], ['x', 'ex-III', 'I. Mitriuc']],
      [['a', 'straini', 'M. Vodă'], ['b', 'prevenire', 'S. Zavtur'], ['c', 'prevenire', 'S. Zavtur'], ['d', 'drepturi', 'I. Șevcenco'], ['x', 'ex-II', 'I. Șevcenco']]
    ] },
    { start: '2026-12-14', days: [
      [['a', 'violenta', 'M. Maxian'], ['b', 'copii', 'M. Maxian'], ['c', 'intruniri', 'M. Maxian'], ['d', 'straini', 'M. Vodă'], ['x', 'ex-IV', 'V. Buzdugan, P. Diuvenji, N. Gulceac, S. Remarenco, M. Taran']],
      [['a', 'analiza', 'I. Botnari'], ['b', 'analiza', 'I. Botnari'], ['c', 'comunitar', 'A. Boubătrîn'], ['d', 'comunitar', 'A. Boubătrîn'], ['x', 'ex-V', 'V. Buzdugan, N. Gulceac']],
      [['a', 'dirijare', 'T. Untilă, Specialist 112'], ['b', 'dirijare', 'T. Untilă, Specialist 112'], ['c', 'dirijare', 'T. Untilă, Specialist 112'], ['d', 'comunitar', 'A. Boubătrîn'], ['x', 'ex-VI', 'A. Andronachi, S. Zavtur']],
      [['a', 'analiza', 'I. Botnari'], ['b', 'analiza', 'I. Botnari'], ['c', 'violenta', 'M. Maxian'], ['d', 'violenta', 'M. Maxian']],
      [['a', 'copii', 'M. Maxian'], ['b', 'copii', 'M. Maxian'], ['c', 'intruniri', 'M. Maxian'], ['d', 'straini', 'M. Vodă'], ['x', 'ex-VII', 'M. Maxian, M. Vodă']]
    ] }
  ]
};
