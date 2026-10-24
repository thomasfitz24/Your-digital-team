def build(g):
    page=g['page']; phero=g['phero']; two=g['two']; rows=g['rows']; facts=g['facts']; split=g['split']
    related=g['related']; hublist=g['hublist']; towns=g['towns']; band=g['band']; contact=g['contact']
    guar=g['guar']; quote=g['quote']; ld=g['ld_service']; SERVICES=g['SERVICES']; SEO=g['SEO']; U=g['U']
    ARROW=g['ARROW']
    def L(slug,text=None): return f'<a class="inl" href="/{slug}">{text or SERVICES[slug][0].lower()}</a>'
    def btn(label,href,cls='btn-dark'): return (label,href,cls)
    HUB=('Our services','/our-services')

    SEO.append(('', 'Commercial Cleaning London | Kemp Services Ltd', 'Commercial cleaning company in London with over 30 years\' experience. Contract, office and builders cleaning across London and the UK. Call 020 8983 8593.',
      [U('1581578731548-c64695cc6952',2000),U('1718152421680-d1580e843cc9',900),U('1577412647305-991150c7d163',900),U('1504297050568-910d24c426d3',900),U('1669101602108-fa5ba89507ee',2000)]))

    # ================= CONTRACT CLEANING =================
    page('contract-cleaning','Contract Cleaning Services London | Kemp Services',
      'Bespoke contract cleaning services for offices, retail, warehouses and welfare facilities in London and the Home Counties. DBS checked cleaners.',
      [
      phero('Contract cleaning services for businesses in London and across the UK.',
        'Kemp Services is a professional cleaning company offering superior commercial cleaning services to businesses in London and the surrounding counties. For companies looking for office cleaners or commercial cleaners for their premises, we offer a reliable service. Pass all your cleaning worries and responsibilities to us.',
        '1718152421680-d1580e843cc9','Operative machine-cleaning a commercial floor',crumb=HUB,cta='Book your contract cleaning'),
      two('Clean premises make a huge difference.',[
        '!We professionally clean buildings of all shapes and sizes for customers across the UK, creating a sanitary and healthy environment. A clean and welcoming workspace can result in less sickness and also boost overall morale and productivity.',
        'We can offer contract cleaning services for all types of properties, including office, retail, warehouse, and welfare facilities. What better way to impress visitors, who could be new or potential clients, than to have your premises looking sparkling clean at all times?',
        'We offer a full range of commercial cleaning and janitorial services to businesses in London, Essex, Kent, Surrey, Middlesex and Hertfordshire. Whether you have a small office, a shop, restaurant, or corporate business, we have commercial cleaners to maintain your premises, any time of day. This includes large and small '+L('office-cleaning')+', commercial cleaning services for bars, shops, gyms and restaurants, as well as '+L('welfare-area-cleaning','welfare services')+'; as often as you need them. No request is too small.'],
        side='<ul class="rows plain" style="margin-top:30px"><li>Commercial contract cleaning</li><li>Retail cleaning for businesses</li><li>Public sector contract cleaning</li><li>Welfare facilities cleaning</li></ul>'),
      facts([('Cleaners <b>DBS checked</b>','All cleaners are DBS checked for security.'),
             ('<b>GPS</b> live monitoring','We use GPS App systems for live monitoring of all our cleaners.'),
             ('QA checks <b>every month</b>','Quality assurance checks every month, plus WhatsApp QA checks every Friday.'),
             ('<b>One</b> monthly invoice','We provide all facilities management solutions under one monthly invoice.')]),
      rows('Setting up a professional cleaning contract is easy.',
        'Located in London, Kemp Services is a customer-focused and technology-driven commercial cleaning company. All sizes of premises and industries undertaken.',
        [('Site survey and proposal','After carrying out a comprehensive site survey, we will put together our contract cleaning proposal for your business. We will pay particular attention to your budget and specific requirements to create a fully bespoke cleaning service that offers value for money. Whether you need us in the morning, during the day or evening, it is always our aim to minimise disruption to your business whilst maintaining the highest of standards.'),
         ('Getting started the right way','Prior to commencing the regular cleaning contract, we recommend that you hire us to undertake an initial '+L('deep-cleaning','deep clean')+' of the entire premises from top to bottom, including '+L('window-cleaning-london')+' and specialist '+L('carpet-floor-cleaning','floor cleaning')+', if required. This allows our clients to immediately see the difference our professional cleaning services make. An initial deep clean also increases the likelihood of your premises staying cleaner for longer. For any contract cleaner, it is much easier to maintain a clean environment than one that has never had a professional deep clean.'),
         ('Rapid deployment, competitive cost','Cleaning teams can be rapidly deployed and we are very competitive on cost. We are committed to delivering the highest possible service to all our clients, regardless of contract size.')]),
      split('Building long-lasting relationships.',[
        'At Kemp Services, we want to build a long-term relationship with our clients. This will result in giving you the time to concentrate on running your business, with the peace of mind that you have left the cleaning to us. We achieve this by getting to know you and developing a solid and open relationship.',
        'By building great relationships with our clients, we get to know and adapt to your changing needs thus allowing us to tailor your cleaning contract to suit your specific requirements. We will support and adapt, during these ever-changing times, to comply with any safe working practices you need to implement.',
        'We deliver thorough, ongoing training to ensure our cleaning operatives are up-to-date with the latest innovations in our industry. All our employees are dedicated to ensuring we deliver customer satisfaction without compromise.'],
        '1627905646269-7f034dcc5738','Gloved hands wiping down an office desk',rev=True,buttons=[btn('Our F.A.C.T. Guarantee','/#guarantee','btn-line')]),
      band('Looking for reputable commercial cleaners in London or the Home Counties?','Call us on 020 8983 8593 or book your contract cleaning services with us today.'),
      related(['office-cleaning','welfare-area-cleaning','deep-cleaning']),
      contact('Book your contract cleaning today.','Tell us about your premises and we will arrange a site survey and a free, no obligation contract cleaning quote.'),
      ], ld=ld('Contract cleaning services','Bespoke and flexible contract cleaning for offices, retail, warehouses and welfare facilities in London and across England.','contract-cleaning'), needs_form=True)

    # ================= OFFICE CLEANING =================
    page('office-cleaning','Office Cleaning London | Kemp Services Ltd',
      'Professional office cleaning in London from vetted, trained cleaners. Daily or out-of-hours office cleaning tailored to your budget. Free site survey.',
      [
      phero('Office cleaning in London that makes the right first impression.',
        'A clean office presents a welcoming, positive and professional first impression to your clients right from the outset. Creating a clean and healthier environment for your staff can result in less sickness and also boost overall morale and productivity.',
        '1577412647305-991150c7d163','Clean open-plan office floor',crumb=HUB),
      split('Vetted, trained and supported office cleaners.',[
        'Our professional office cleaning staff are vetted, trained and supported by our experienced management team. Our office cleaning team will work to reducing allergens, dust, and mould, which will make your team healthier and more productive.',
        'After carrying out our comprehensive site survey, we will put together our proposal for your business, paying particular attention to your budget and specific requirements to create a fully bespoke service. It is always our aim to minimise disruption to your business whilst maintaining the highest of standards.',
        'If you would prefer us to clean when your offices are empty, we can work outside of usual business hours. Alternatively, our cleaners can work alongside your staff without disrupting them.'],
        '1781637590564-01c65dbf2039','Cleaner vacuuming a carpeted office floor',buttons=[btn('See our contract cleaning services','/contract-cleaning')]),
      rows('Where an office needs cleaning most.',
        'Office cleaning usually happens overnight. Bacteria counts are lower at the start of the workday, but a University of Arizona study found contamination can spread through an office within two to four hours. These are the office hotspots.',
        ['Lift buttons, doorknobs and hand railings','Kitchens: spillages, cupboards and fridges','Bathrooms','Shared office equipment: copiers, franking machines, water coolers and vending machines','Individual desks, phones, keyboards and mice'],white=False,plain=True,cols=True),
      two('Leave the office cleaning to us.',[
        '!At Kemp Services, we want to build a long-term relationship with our clients to ensure you know you can concentrate on running your business and leave the cleaning to us.',
        'By building great relationships with our clients, we get to know and adapt to your changing needs and tailor our service specifically to meet and exceed your expectations.',
        'What you get: peace of mind, a motivated workforce, a positive message to visitors, and high quality cleaning managed by an experienced team. The cost of office cleaning varies with the size of your premises and the hours required for the daily clean, so we quote after a site survey.',
        'Related services: '+L('carpet-floor-cleaning','carpet cleaning')+' and '+L('window-cleaning-london')+'.'],
        side='<a class="btn-dark" href="/contact">Arrange a free site survey'+ARROW+'</a>'),
      related(['contract-cleaning','carpet-floor-cleaning','window-cleaning-london']),
      contact('Get an office cleaning quote.','Tell us about your office, how many staff you have and when you would like us to clean, and we will come back to you with a quote.'),
      ], ld=ld('Office cleaning London','Vetted and trained office cleaners in London, working in or out of hours and tailored to your budget.','office-cleaning'), needs_form=True)

    # ================= CONSTRUCTION HUB =================
    page('construction-cleaning','Post Construction Cleaning London | Kemp Services',
      'Post construction cleaning in London and across the UK: builders cleans, sparkle cleans and welfare area cleaning for construction and fit out firms.',
      [
      phero('Post construction cleaning in London for the construction industry.',
        'We professionally clean buildings of all shapes and sizes for customers across the UK, creating a clean and healthy environment. Builders cleans are one of our core specialities; delivering a safe and professional service working with clients throughout all stages of their projects on time and on budget.',
        '1768321903661-87da7d2962b0','Interior construction site with metal studs and exposed ceiling',crumb=HUB,wash=True),
      hublist('Two services for site teams.','Whether you need the last trade on site before handover, or your welfare facilities kept clean for the duration of the project, we cover both.',
        [('Builders clean','/builders-clean','1504297050568-910d24c426d3','Newly fitted-out office corridor after a builders clean','At the end of any new building, refurbishment or renovation project, the last trade on site before that all-important handover. After builders clean, final clean, sparkle clean or construction site cleaning.',False),
         ('Welfare area cleaning','/welfare-area-cleaning','1772209415876-76ea6cbc2f0c','Operatives working on the floor of a large empty building','When it comes to welfare areas, we can provide cleaning on a one-off ad hoc basis or schedule daily or weekly cleans. From small office accommodation to multi-bay construction site offices.',False)]),
      split('Reliable, flexible, and safe on site.',[
        'We are reliable and flexible and can adapt quickly to changing circumstances or work around trades 24/7, ensuring your deadlines are met whilst delivering quality results; this has led to our excellent track record working with construction, refurbishment, fit out and modular companies.',
        'Health and safety is paramount and the majority of our staff are CSCS qualified and our RAMS are site specific and have been passed by contractors such as Kier, Galliford Try and Willmott Dixon.',
        'We can help if you are tendering for a project or short on time and need a quote off plan, or we can arrange a visit and carry out a comprehensive site survey to ensure a more specific quote.'],
        '1772300164438-f73307d3b645','Large empty building with polished floors after construction',rev=True,white=False,buttons=[btn('Get a quote off plan','/contact')]),
      related(['contract-cleaning','window-cleaning-london','carpet-floor-cleaning'],heading='Also for site teams'),
      contact('Tell us about your project.','Send us the plans or the site address and your handover date, and we will come back with a quote.'),
      ], ld=ld('Post construction cleaning London','Builders cleans and welfare area cleaning for construction, refurbishment, fit out and modular companies in London and across the UK.','construction-cleaning'), needs_form=True)

    # ================= BUILDERS CLEAN =================
    page('builders-clean','Builders Cleaning Services London | Kemp Services',
      'Specialist builders cleaning services: after builders, final and sparkle cleans in London and across the UK. CSCS qualified staff, site-specific RAMS.',
      [
      phero('Builders cleaning services: the last trade on site before handover.',
        'At the end of any new building, refurbishment or renovation project, the last trade on site before that all important handover, is us; your specialist post construction cleaners. After all the planning, project management, hard work and stress, you need a cleaning company you can trust and rely on to ensure your client gets the right first impression when you hand their premises back to them.',
        '1504297050568-910d24c426d3','Newly fitted-out office corridor after a builders clean',crumb=('Construction cleaning','/construction-cleaning'),cta='Get a builders clean quote'),
      facts([('<b>CSCS</b> qualified','The majority of our staff are CSCS qualified.'),
             ('Site-specific <b>RAMS</b>','Our RAMS are site specific and have been passed by contractors such as Kier, Galliford Try and Willmott Dixon.'),
             ('Work around trades <b>24/7</b>','We adapt quickly to changing circumstances to ensure your deadlines are met.'),
             ('Quotes <b>off plan</b>','Tendering or short on time? We can quote off plan or carry out a full site survey.')]),
      two('One of our core specialities.',[
        '!Builders cleans are one of our core specialities; delivering a safe and professional service working with clients throughout all stages of their projects on time and on budget.',
        'We are reliable and flexible and can adapt quickly to changing circumstances or work around trades 24/7, ensuring your deadlines are met whilst delivering quality results; this has led to our excellent track record working with construction, refurbishment, fit out and modular companies.',
        'We have worked on projects of varying sizes in London and across the UK; removing the dust and grime. We can provide professional, quality after builders clean, or final clean, sparkle clean or construction site cleaning.',
        'We can help if you are tendering for a project or short on time and need a quote off plan or we can arrange a visit and carry out a comprehensive site survey to ensure a more specific quote.'],
        side='<a class="btn-dark" href="/contact">Arrange a site survey'+ARROW+'</a><a class="btn-line" href="/construction-cleaning">All construction cleaning'+ARROW+'</a>'),
      rows('Fully customisable builders cleans.','Our builders cleans are fully customisable and we can provide additional services to ensure we are your all-around cleaning provider.',
        ['Window cleaning','Carpet cleaning','Floor scrubbing','High wall and cladding cleaning','Jet washing'],white=False,plain=True,cols=True),
      split('Welfare cleaning for the life of the project.',[
        'We are also experienced and able to provide regular '+L('welfare-area-cleaning','welfare cleaning services')+' to ensure your site facilities comply with Health and Safety regulations.',
        'Call us to see how we can provide you with a hassle-free service on your current or future projects.'],
        '1770838773417-08b18661c62f','Interior construction site with tools and ladders',buttons=[btn('Welfare area cleaning','/welfare-area-cleaning','btn-line')]),
      related(['welfare-area-cleaning','window-cleaning-london','carpet-floor-cleaning']),
      contact('Get a builders clean quote.','Send us the site address, the size of the project and your handover date. We can quote off plan or visit site.'),
      ], ld=ld('Builders cleaning services','After builders, final and sparkle cleans for construction, refurbishment, fit out and modular companies in London and across the UK.','builders-clean'), needs_form=True)

    # ================= WELFARE =================
    page('welfare-area-cleaning','Welfare Cleaning for Construction Sites | Kemp Services',
      'Welfare cleaning for construction sites: ad hoc, daily or weekly cabin and welfare facility cleaning, from small site offices to multi-bay accommodation.',
      [
      phero('Welfare cleaning that keeps your site safe, tidy and compliant.',
        'On any construction site, keeping your welfare facilities clean and hygienic is vital. We offer an excellent, cost effective and consistent building site cabin cleaning service at a frequency to suit your requirements.',
        '1772209415876-76ea6cbc2f0c','Operatives working on the floor of a large empty building',crumb=('Construction cleaning','/construction-cleaning')),
      rows('Cleaning at the frequency your site needs.','Kemp Services have specialist experience working with the construction industry. We focus our efforts on keeping your environment safe and tidy. When it comes to welfare areas, we can provide cleaning on a one-off ad hoc basis or schedule daily or weekly cleans.',
        [('Ad hoc','One-off welfare cleaning when you need it.'),
         ('Daily','Daily welfare cleaning services.'),
         ('Weekly','A weekly welfare cleaning service.')]),
      split('From small site offices to multi-bay accommodation.',[
        'We cover all types of welfare from small office accommodation to multi-bay construction site offices. A clean site will lower the risk of injury and the spread of viruses as well as improve morale as it provides your trades a place to refocus.',
        'We offer excellent and cost-effective welfare cleaning services. We can attend your premises as frequently as you need it; for contractors of all sizes. We also provide '+L('builders-clean','builders cleans')+' at the end of a project, before handover.'],
        '1790156247557-4f4e22b6fca2','Stepladder in a room with bare walls and a concrete floor',rev=True,white=False,buttons=[btn('Get a welfare cleaning quote','/contact')]),
      related(['builders-clean','construction-cleaning','contract-cleaning']),
      contact('Get a welfare cleaning quote.','Tell us how many cabins or welfare units you have, where the site is and how often you want us there.'),
      ], ld=ld('Welfare cleaning','Ad hoc, daily or weekly welfare area and site cabin cleaning for construction sites.','welfare-area-cleaning'), needs_form=True)

    # ================= PROPERTY MANAGEMENT HUB =================
    page('property-management-cleaning','Property Management Cleaning London | Kemp Services',
      'Property management cleaning in London for property managers, landlords and letting agents: communal block cleaning, tenancy cleans, deep cleans and more.',
      [
      phero('Property management cleaning in London for landlords and property managers.',
        'Whether you are a private landlord or manage a local, regional or national property portfolio, Kemp Services have the experience and expertise to ensure your property always makes the right first impression.',
        '1760160134936-14284be2a811','Balconies of a modern apartment building at dusk',crumb=HUB,wash=True),
      two('Over 30 years working with property professionals.',[
        '!We have been working in partnership with property management companies, private landlords and letting agents for over 30 years, providing professional comprehensive and tailored cleaning solutions for all types of residential and commercial tenanted properties.',
        'Our range of services includes pre and post tenancy cleans, regular communal block cleaning, deep cleans, periodic cleaning, carpet and upholstery cleaning, specialist floor cleaning, window cleaning, bin store and car park cleaning and waste and large item removal.']),
      hublist('Two services for your portfolio.','',
        [('Communal block cleaning','/communal-block-cleaning','1635151925996-cf34cc3805d4','Long communal hallway with doors on both sides','Our regular communal block cleaning services ensure that your lobbies, stairwells and corridors remain in top condition and provide you and your residents and visitors with peace of mind.',False),
         ('Pre and post tenancy cleans','/pre-post-tenancy-cleans','1789352844327-765b16a51b9b','Empty carpeted living area opening into a kitchen','As a Letting Agency or Private Landlord, it\'s your duty to provide a property in a clean and well-maintained condition for your tenants.',False)],white=False),
      rows('Everything a tenanted property needs.','',
        ['Pre and post tenancy cleans','Regular communal block cleaning','Deep cleans','Periodic cleaning','Carpet and upholstery cleaning','Specialist floor cleaning','Window cleaning','Bin store and car park cleaning','Waste and large item removal'],plain=True,cols=True),
      related(['deep-cleaning','carpet-floor-cleaning','window-cleaning-london'],heading='Often added to a portfolio contract'),
      contact('Tell us about your portfolio.','Whether it is one block or a national portfolio, tell us what you manage and we will put together a tailored proposal.'),
      ], ld=ld('Property management cleaning London','Cleaning for property management companies, private landlords and letting agents: communal blocks, tenancy cleans, deep cleans and more.','property-management-cleaning'), needs_form=True)

    # ================= COMMUNAL BLOCK =================
    page('communal-block-cleaning','Communal Block Cleaning London | Kemp Services',
      'Regular communal block cleaning for lobbies, stairwells and corridors, plus bin stores, car parks and windows, for housing associations and landlords.',
      [
      phero('Communal block cleaning for lobbies, stairwells and corridors.',
        'Our regular communal block cleaning services ensure that your lobbies, stairwells and corridors remain in top condition and provide you and your residents and visitors with peace of mind.',
        '1635151925996-cf34cc3805d4','Long communal hallway with doors on both sides',crumb=('Property management cleaning','/property-management-cleaning')),
      split('Inside and out.',[
        'We provide communal area cleaning services to housing associations, property management companies and residence associations. We can clean and maintain common areas including staircases, reception areas, post boxes and windows (internally and externally).',
        'Externally, our services also extend to jet washing and disinfecting bin storage areas, large item waste and rubbish removal, car park maintenance and litter picking and window cleaning, making sure your property gives the right first impression.',
        'If you are a landlord or property management company, we carry out communal block cleaning services at competitive rates.'],
        '1765639729104-587942a1e45c','Sunlit communal hallway with a view of buildings',buttons=[btn('Get a quote for your block','/contact')]),
      rows('A flexible schedule, and eyes on your property.','With our flexible approach, we can fully tailor the cleaning schedule you need to ensure minimum disruption to both residents and commercial tenants.',
        [('Regular reports with photos','We will regularly report back, with photos, any property issues we find.'),
         ('Small fixes as we go','We can change smoke alarm batteries and lightbulbs as we go along if required.'),
         ('Periodic specialist cleaning','In addition to the regular cleaning, we can also schedule periodic specialist cleaning for carpets and upholstery, cladding and fascia clean.')],white=False),
      related(['pre-post-tenancy-cleans','window-cleaning-london','carpet-floor-cleaning']),
      contact('Get a communal cleaning quote.','Tell us how many blocks you manage, how many floors and entrances each has, and how often you would like us to attend.'),
      ], ld=ld('Communal block cleaning','Regular cleaning of lobbies, stairwells, corridors, bin stores and car parks for housing associations, landlords and property managers.','communal-block-cleaning'), needs_form=True)

    # ================= TENANCY =================
    page('pre-post-tenancy-cleans','End of Tenancy Cleaning London | Kemp Services',
      'End of tenancy cleaning in London for letting agents and landlords. Thorough pre and post tenancy cleans with before and after photos and a full checklist.',
      [
      phero('End of tenancy cleaning in London for letting agents and landlords.',
        'As a Letting Agency or Private Landlord, it\'s your duty to provide a property in a clean and well-maintained condition for your tenants. Although previous occupants may clean the property before they leave, it\'s unlikely that they will leave it in the same condition as when their rental first commenced; this is where Kemp Services\' years of experience can make all the difference.',
        '1789352844327-765b16a51b9b','Empty carpeted living area opening into a kitchen',crumb=('Property management cleaning','/property-management-cleaning'),cta='Book a tenancy clean'),
      two('A thorough, evidenced clean of every room.',[
        '!Our pre and post tenancy cleaning involves a thorough and professional clean of all rooms, electric appliances, furniture and fittings in your property to the highest standards.',
        'Pre-tenancy cleaning gives the benefit of a clean and fresh start when moving into a new property. The purpose of post-tenancy cleaning is to ensure all rooms are spotless. During the end of tenancy cleaning service all floors are swept and mopped, carpets are hoovered, skirting boards cleaned, all corners and furniture are dusted, and the bathroom and kitchen are thoroughly cleaned and sanitised.',
        'Our cleaners are experienced, vetted and thorough and all our work can be evidenced by before and after photos. Our team will be equipped with all the necessary chemicals, tools and equipment and will work to our own comprehensive checklist, however we can tailor this to your exact requirements.'],
        side='<a class="btn-dark" href="/contact">Book a tenancy clean'+ARROW+'</a>'),
      rows('Additional services you may wish to add.','',
        ['Steam cleaning for carpets and upholstery','Mattress sanitising','Oven cleaning','Window cleaning','External rubbish clearance'],white=False,plain=True,cols=True),
      split('Shown in its best light.',[
        'The cleanliness and maintenance of your property will directly affect the retention of customers, their experience and the duration of their tenancy; Kemp Services can make sure your property is shown in its best light.',
        'For blocks and estates we also provide '+L('communal-block-cleaning')+', and a '+L('deep-cleaning','deep clean')+' where a property needs more than a standard turnaround.'],
        '1753911372198-50b1b254ad4d','Bright empty room with large windows',rev=True,buttons=[btn('Property management cleaning','/property-management-cleaning','btn-line')]),
      related(['communal-block-cleaning','carpet-floor-cleaning','deep-cleaning']),
      contact('Book a pre or post tenancy clean.','Tell us the property address, how many bedrooms it has and the date you need it done by.'),
      ], ld=ld('End of tenancy cleaning London','Pre and post tenancy cleans for letting agents and landlords, with before and after photos and a comprehensive checklist.','pre-post-tenancy-cleans'), needs_form=True)

    # ================= CARPET =================
    page('carpet-floor-cleaning','Commercial Carpet Cleaning London | Kemp Services',
      'Commercial carpet cleaning in London for offices, retail, construction and homes. Bespoke cleaning for any flooring material, restoring tired carpets.',
      [
      phero('Commercial carpet cleaning in London, for any flooring material.',
        'With over 30 years of experience in the cleaning industry, we provide tailored carpet cleaning to both domestic and commercial clients. If you are located within Greater London, we provide services to construction, retailers, homes and offices.',
        '1742483359033-13315b247c74','Operative in protective clothing cleaning a carpet',crumb=HUB),
      split('Keep carpets looking good, and your environment healthy.',[
        'Your home or office carpets and flooring can easily become breeding grounds for bacteria and other undesirable microorganisms. We recommend regular carpet cleaning to keep them not only looking good but keeping your environment fresh and healthy.',
        'Kemp Services provides a bespoke carpet cleaning service, regardless of the fabric your flooring is made from. We can help restore the look of tired and stained carpets. Our carpet cleaners will take care of your flooring and have it looking like new in no time.',
        'Our prices are competitive and tailored to your individual needs, which provides you with better value for money. Carpet and upholstery cleaning has a minimum call out charge of £65 excluding VAT.'],
        '1527515637462-cff94eecc1ac','Vacuum cleaner being used on a carpet',buttons=[btn('Get a carpet cleaning quote','/contact')]),
      two('Part of our other services too.',[
        '!Carpet and floor cleaning is one of the additional services we offer alongside our other cleaning work.',
        'Our '+L('builders-clean','builders cleans')+' are fully customisable and we can provide additional services such as window cleaning, carpet cleaning, floor scrubbing, high wall/cladding and jet washing.',
        'With our '+L('pre-post-tenancy-cleans','pre and post tenancy cleans')+' you may also wish to make use of the additional services we offer such as steam cleaning for carpets and upholstery, mattress sanitising, oven cleaning, window cleaning and external rubbish clearance.',
        'Before a '+L('contract-cleaning','cleaning contract')+' starts, we recommend an initial deep clean of the entire premises, including window cleaning and specialist floor cleaning, if required.'],white=False),
      related(['office-cleaning','deep-cleaning','pre-post-tenancy-cleans']),
      contact('Get a carpet cleaning quote.','Tell us the type of flooring, the approximate floor area and where the premises are.'),
      ], ld=ld('Commercial carpet cleaning London','Bespoke carpet and floor cleaning for offices, retail, construction and homes across Greater London.','carpet-floor-cleaning'), needs_form=True)

    # ================= DEEP =================
    page('deep-cleaning','Deep Cleaning London | Kemp Services Ltd',
      'Professional one-off deep cleaning in London and the Home Counties for commercial and residential properties. Trained, vetted and fully insured cleaners.',
      [
      phero('Professional one-off deep cleaning in London and the Home Counties.',
        'Our cleaners are professionally trained, vetted and fully insured. When the task has become overwhelming, it might be time to book us in for a deep clean.',
        '1740657254989-42fe9c3b8cce','Gloved operative cleaning a hard floor',crumb=HUB,cta='Book a deep clean'),
      two('Why people book a deep clean.',[
        '!The reasons why people choose a deep cleaning service vary. The most common ones include:',
        'When the task of cleaning a residential or commercial property is much but there is a need for an extra clean. Before selling a property, a deep clean can help with a sale. Deep cleaning for visitors, before or after a party, or before the arrival of a new baby. Or when you need an extra clean as an annual spring clean.'],
        side='<ul class="rows plain" style="margin-top:30px"><li>An extra clean</li><li>Before selling a property</li><li>Visitors, parties, a new baby</li><li>An annual spring clean</li></ul>'),
      split('The right start to a cleaning contract.',[
        'Prior to commencing a regular cleaning contract, we recommend that you hire us to undertake an initial deep clean of the entire premises from top to bottom, including '+L('window-cleaning-london')+' and specialist '+L('carpet-floor-cleaning','floor cleaning')+', if required. This allows our clients to immediately see the difference our professional cleaning services make.',
        'An initial deep clean also increases the likelihood of your premises staying cleaner for longer. For any contract cleaner, it is much easier to maintain a clean environment than one that has never had a professional deep clean.'],
        '1585421514284-efb74c2b69ba','Gloved hand wiping a surface clean',rev=True,white=False,buttons=[btn('Contract cleaning services','/contract-cleaning')]),
      related(['contract-cleaning','office-cleaning','carpet-floor-cleaning']),
      contact('Book a deep clean.','Tell us about the property, what needs the most attention and when you need it done.'),
      ], ld=ld('Deep cleaning London','One-off deep cleaning for commercial and residential properties in London and the Home Counties by trained, vetted and fully insured cleaners.','deep-cleaning'), needs_form=True)

    # ================= WINDOW =================
    page('window-cleaning-london','Commercial Window Cleaning London | Kemp Services',
      'Commercial window cleaning in London and across the UK by certified window cleaners. Internal and external window cleaning for all types of business.',
      [
      phero('Commercial window cleaning in London, inside and out.',
        'We provide a commercial window cleaning service throughout London and across the UK. We have worked for many commercial and residential clients to ensure that their windows are sparkling clean.',
        '1482449609509-eae2a7ea42b7','Window cleaner on a platform cleaning a large glass window',crumb=HUB),
      split('Certified professional window cleaners.',[
        'Our certified professional window cleaners are experts in transforming old and dirty windows into gleaming, sparkling pieces of glazing. We clean windows both internally and externally, for all types of businesses.',
        'Window cleaning is available as a one-off, as part of a '+L('contract-cleaning','contract cleaning')+' schedule, or as an add-on to a '+L('builders-clean')+' or '+L('communal-block-cleaning','communal block clean')+'.'],
        '1763026227930-ec2c91d4e7f2','Window cleaner using a squeegee on a shop front',buttons=[btn('Get a window cleaning quote','/contact')]),
      rows('Where we clean windows.','',
        ['Offices','Shops and retail premises','Communal residential blocks','Construction sites before handover','Commercial premises across London and the UK'],white=False,plain=True,cols=True),
      related(['contract-cleaning','communal-block-cleaning','builders-clean']),
      contact('Get a window cleaning quote.','Tell us the address, roughly how many windows there are and whether you need internal, external or both.'),
      ], ld=ld('Commercial window cleaning London','Internal and external window cleaning for businesses throughout London and across the UK by certified window cleaners.','window-cleaning-london'), needs_form=True)

    # ================= OUR SERVICES HUB =================
    page('our-services','Commercial Cleaning Services | Kemp Services Ltd',
      'All our commercial cleaning services: contract, office, construction, builders, welfare, communal, tenancy, carpet, deep and window cleaning.',
      [
      phero('Commercial cleaning services for every type of premises.',
        'We will be your one stop shop for cleaning services offering one-off or regular cleaning. Regardless of the type of property, office, retail, welfare facilities or warehouse, we can help keep your premises looking sparkling clean at all times.',
        '1758448093806-88b2089068ab','Modern office lobby with reception desk and seating',wash=True),
      hublist('Every service we offer.','We professionally clean buildings of all shapes and sizes for customers across the UK, creating a clean and healthy environment.',
        [('Contract cleaning','/contract-cleaning','1718152421680-d1580e843cc9','Operative machine-cleaning a commercial floor','We professionally clean buildings of all shapes and sizes for customers across the UK, creating a clean and healthy environment.',False),
         ('Office cleaning','/office-cleaning','1577412647305-991150c7d163','Clean open-plan office floor','A clean office presents a welcoming, positive and professional first impression to your clients right from the outset.',False),
         ('Construction cleaning','/construction-cleaning','1768321903661-87da7d2962b0','Interior construction site with metal studs','Cleaning services for the construction industry. We professionally clean buildings of all shapes and sizes for customers across the UK.',False),
         ('Builders clean','/builders-clean','1504297050568-910d24c426d3','Newly fitted-out office corridor after a builders clean','At the end of any new building, refurbishment or renovation project, the last trade on site before that all-important handover.','construction cleaning'),
         ('Welfare area cleaning','/welfare-area-cleaning','1772209415876-76ea6cbc2f0c','Operatives working on the floor of a large empty building','When it comes to welfare areas, we can provide cleaning on a one-off ad hoc basis or schedule daily or weekly cleans.','construction cleaning'),
         ('Property management cleaning','/property-management-cleaning','1760160134936-14284be2a811','Balconies of a modern apartment building at dusk','We have been working in partnership with property management companies, private landlords and letting agents for over 30 years.',False),
         ('Communal block cleaning','/communal-block-cleaning','1635151925996-cf34cc3805d4','Long communal hallway with doors on both sides','Our regular communal block cleaning services ensure that your lobbies, stairwells and corridors remain in top condition and provide you and your residents and visitors with peace of mind.','property management cleaning'),
         ('Pre and post tenancy cleans','/pre-post-tenancy-cleans','1789352844327-765b16a51b9b','Empty carpeted living area opening into a kitchen','As a Letting Agency or Private Landlord, it\'s your duty to provide a property in a clean and well-maintained condition for your tenants.','property management cleaning'),
         ('Carpet and floor cleaning','/carpet-floor-cleaning','1742483359033-13315b247c74','Operative in protective clothing cleaning a carpet','With over 30 years of experience in the cleaning industry, we provide tailored carpet cleaning to both domestic and commercial clients.',False),
         ('Deep cleaning','/deep-cleaning','1740657254989-42fe9c3b8cce','Gloved operative cleaning a hard floor','Professional one-off deep cleaning services in London and the Home Counties. Our cleaners are professionally trained, vetted and fully insured.',False),
         ('Window cleaning','/window-cleaning-london','1482449609509-eae2a7ea42b7','Window cleaner on a platform cleaning a large glass window','We provide a commercial window cleaning service throughout London and across the UK. We clean windows both internally and externally.',False)]),
      two('How we work with you.',[
        '!Initially, we will talk through your requirements. We will arrange a site survey to provide you with a free, no obligation, contract cleaning quote. We will tailor our service to meet your budget.',
        'All our cleaning staff are fully vetted. When it comes to working hours and patterns, we offer great flexibility. If you would prefer us to clean when your offices are empty, we can work outside of usual business hours. Alternatively, our cleaners can work alongside your staff without disrupting them.',
        'Our contract cleaning work is covered by our <a class="inl" href="/#guarantee">F.A.C.T. Guarantee</a>.'],white=False,
        side='<ul class="rows plain" style="margin-top:30px"><li>Competitive rates</li><li>Flexible contracts</li><li>Fully insured, trained and vetted staff</li><li>Tailored cleaning schedule</li><li>Regular site inspections</li></ul>'),
      contact(),
      ], needs_form=True)

    # ================= AREAS =================
    compact=g['compact']
    def area_services(featured,heading,white=True):
        return related(featured,heading=heading,four=(len(featured)==4),extra=compact(featured))
    VET='All our cleaning staff are fully vetted. When it comes to working hours and patterns, we offer great flexibility. If you would prefer us to clean when your offices are empty, we can work outside of usual business hours. Alternatively, our cleaners can work alongside your staff without disrupting them.'
    PREM='Clean and presentable premises not only make a difference to the general health and wellbeing of staff, but it also creates a positive first impression to visitors. Regardless of the type of property, office, retail, welfare facilities or warehouse, we can help keep your premises looking sparkling clean at all times.'
    CHECKS='<ul class="rows plain" style="margin-top:30px"><li>Competitive rates</li><li>Flexible contracts</li><li>Fully insured, trained and vetted staff</li><li>Tailored cleaning schedule</li><li>Regular site inspections</li></ul>'

    # LONDON: boroughs first, the Stratford base, four featured services
    page('area-london','Cleaning Contractors London | Kemp Services Ltd',
      'Cleaning contractors in London, from Havering in the east to Ealing in the west. Based in Stratford, covering every London borough.',
      [
      phero('Cleaning contractors in London, from Havering in the east to Ealing in the west.',
        'Kemp Services is a contract cleaning company based in Stratford, east London. For over 30 years we have been offering professional commercial cleaning services. We pride ourselves on being a flexible and responsive London cleaning contractor.',
        '1632897271846-b6e3ca78aded','Red double-decker bus on a busy London street',wash=True,cta='Get a London quote'),
      towns('Every London borough.','We offer our cleaning services to businesses across the whole of London.',
        ['Barking and Dagenham','Barnet','Bexley','Brent','Bromley','Camden','Croydon','Ealing','Enfield','Fulham','Greenwich','Hackney','Haringey','Harrow','Havering','Hillingdon','Hounslow','Islington','Kensington and Chelsea','Kingston upon Thames','Lambeth','Lewisham','Merton','Newham','Redbridge','Richmond upon Thames','Southwark','Sutton','Tower Hamlets','Waltham Forest','Wandsworth','Westminster']),
      split('Based in Stratford, working across the capital.',[PREM,VET],
        '1606757898266-5dcb04600340','People walking between high-rise office buildings in London',white=False,rev=True,buttons=[btn('Our F.A.C.T. Guarantee','/#guarantee')]),
      area_services(['contract-cleaning','office-cleaning','builders-clean','communal-block-cleaning'],'What we clean in London.'),
      band('We also cover Essex, Kent, Surrey and Middlesex.','Most of our customers are based across London and the Home Counties, with contracts in Manchester, Newcastle, Nottingham, Liverpool, Cardiff and Birmingham too.'),
      contact('Get a quote for your London premises.'),
      ], ld=ld('Cleaning contractors London','Contract and commercial cleaning across every London borough from a contractor based in Stratford, east London.','area-london',area='London'), needs_form=True)

    # ESSEX: offices lead, towns in a navy band, services third
    page('contract-cleaning-essex','Office Cleaning Essex | Kemp Services Ltd',
      'Office cleaning in Essex from a contract cleaning company based in Stratford, east London. Vetted cleaners for offices, retail and warehouses across Essex.',
      [
      phero('Office cleaning in Essex, in or out of hours.',
        'Kemp Services is a contract cleaning company based in Stratford, east London. For over 30 years we have been offering professional commercial cleaning services, and we pride ourselves on being a flexible and responsive Essex cleaning contractor.',
        '1746998032579-53288033500d','Buildings along a town street on a sunny day',cta='Get an Essex quote'),
      split('Offices, retail, warehouses and welfare facilities.',[
        'We offer our cleaning services to businesses across the whole of Essex. Regardless of the type of property, office, retail, welfare facilities or warehouse, we can help keep your premises looking sparkling clean at all times.',
        VET],
        '1497366754035-f200968a6e72','Office hallway between glass-panel doors',buttons=[btn('Office cleaning','/office-cleaning'),btn('Our F.A.C.T. Guarantee','/#guarantee','btn-line')]),
      towns('Essex towns we cover.','',['Basildon','Braintree','Brentwood','Chelmsford','Colchester','Grays','Harlow','Kelvedon','Maldon','Romford'],white=False),
      area_services(['office-cleaning','contract-cleaning','welfare-area-cleaning'],'Cleaning services in Essex.'),
      contact('Get a quote for your Essex premises.'),
      ], ld=ld('Office cleaning Essex','Office and commercial cleaning across Essex from a contractor based in Stratford, east London.','contract-cleaning-essex',area='Essex'), needs_form=True)

    # KENT: the guarantee is the unique section, towns in prose order
    page('area-kent','Commercial Cleaning Kent | Kemp Services Ltd',
      'Commercial cleaning across Kent, from Dartford to Dover. Contract, office and builders cleaning from a London contractor with over 30 years\' experience.',
      [
      phero('Commercial cleaning in Kent, from Dartford to Dover.',
        'Kemp Services is a contract cleaning company based in Stratford, east London. We offer our cleaning services to businesses across the whole of Kent, and pride ourselves on being a flexible and responsive Kent cleaning contractor.',
        '1600379877371-091ccbd74267','Brick building under a blue sky',wash=True,cta='Get a Kent quote'),
      two('Thirty years of commercial cleaning.',[
        '!For over 30 years we have been offering professional commercial cleaning services.',
        PREM, VET],side=CHECKS),
      towns('Where we work in Kent.','',['Ashford','Canterbury','Dartford','Dover','Faversham','Gillingham','Hastings','Maidstone','Orpington','Sevenoaks','Tunbridge Wells'],white=False),
      area_services(['contract-cleaning','office-cleaning','builders-clean','welfare-area-cleaning'],'Cleaning services in Kent.'),
      split('Risk free for Kent contract clients.',[
        'We are confident in the services we provide, which is why we make signing up with us a risk free process. If you are not completely satisfied with our service in the first month of your cleaning contract, we will provide you a full refund for that month. Only applies to contract services.'],
        '1612791119418-36f22ce00cd4','Street light beside a brick building',white=False,buttons=[btn('Our F.A.C.T. Guarantee','/#guarantee')]),
      contact('Get a quote for your Kent premises.'),
      ], ld=ld('Commercial cleaning Kent','Contract, office and builders cleaning for businesses across Kent.','area-kent',area='Kent'), needs_form=True)

    # SURREY: the longest town list leads after a white intro; office angle
    page('area-surrey','Office Cleaning Surrey | Kemp Services Ltd',
      'Office cleaning in Surrey from Guildford to Kingston. Flexible, vetted office and commercial cleaners from a contractor with over 30 years\' experience.',
      [
      phero('Office cleaning in Surrey, from Guildford to Kingston.',
        'Kemp Services is a contract cleaning company based in Stratford, east London. For over 30 years we have been offering professional commercial cleaning services, and we pride ourselves on being a flexible and responsive Surrey cleaning contractor.',
        '1581276002303-3c0e4f6bf633','Red bus on a road beside a building',cta='Get a Surrey quote'),
      split('A healthier office for your Surrey team.',[
        'Our '+L('office-cleaning','office cleaning')+' team will work to reducing allergens, dust, and mould, which will make your team healthier and more productive. A clean office presents a welcoming, positive and professional first impression to your clients right from the outset.',
        VET],
        '1771678040129-477a44bd37ea','Modern white office interior with large windows',rev=True,buttons=[btn('Office cleaning','/office-cleaning')]),
      towns('Twenty-seven Surrey towns.','We offer our cleaning services to businesses across the whole of Surrey.',
        ['Aldershot','Chertsey','Coulsdon','Croydon','Dorking','Egham','Epsom','Esher','Farnham','Guildford','Haslemere','Kew','Kingston','Leatherhead','Mitcham','Morden','New Malden','Oxshott','Purley','Redhill','Reigate','Richmond','Staines','Surbiton','Sutton','Weybridge','Woking'],white=False),
      area_services(['office-cleaning','carpet-floor-cleaning','window-cleaning-london','deep-cleaning'],'Office services in Surrey.'),
      contact('Get a quote for your Surrey premises.'),
      ], ld=ld('Office cleaning Surrey','Office and commercial cleaning for businesses across Surrey.','area-surrey',area='Surrey'), needs_form=True)

    # MIDDLESEX: facts strip, then towns, construction and property angle
    page('area-middlesex','Commercial Cleaning Middlesex | Kemp Services Ltd',
      'Commercial cleaning across Middlesex: Harrow, Hounslow, Uxbridge, Wembley and more. Contract, office and builders cleaning from a London contractor.',
      [
      phero('Commercial cleaning in Middlesex, from Wembley to West Drayton.',
        'Kemp Services is a contract cleaning company based in Stratford, east London. We offer our cleaning services to businesses across the whole of Middlesex and pride ourselves on being a flexible and responsive Middlesex cleaning contractor.',
        '1604497853190-dc84f9a3f0bf','People walking between red brick buildings',wash=True,cta='Get a Middlesex quote'),
      facts([('<b>30+</b> years','For over 30 years we have been offering professional commercial cleaning services.'),
             ('Staff <b>fully vetted</b>','All our cleaning staff are fully vetted.'),
             ('In or <b>out of hours</b>','We can work outside of usual business hours, or alongside your staff.'),
             ('<b>F.A.C.T.</b> guaranteed','Our contract cleaning work is covered by our guarantee.')]),
      towns('Middlesex towns we cover.','',['Brentford','Ealing','Edgware','Feltham','Hampton','Harefield','Harrow','Hayes','Hillingdon','Hounslow','Isleworth','Northolt','Northwood','Pinner','Ruislip','Stanmore','Teddington','Twickenham','Uxbridge','Wealdstone','Wembley','West Drayton']),
      area_services(['contract-cleaning','builders-clean','communal-block-cleaning','pre-post-tenancy-cleans'],'Cleaning services in Middlesex.',white=False),
      two('Office, retail, welfare and warehouse premises.',[
        '!'+PREM,
        'If you would prefer us to clean when your offices are empty, we can work outside of usual business hours. Alternatively, our cleaners can work alongside your staff without disrupting them.'],white=False,
        side='<a class="btn-dark" href="/contact">Get a quote'+ARROW+'</a>'),
      contact('Get a quote for your Middlesex premises.'),
      ], ld=ld('Commercial cleaning Middlesex','Contract, office and builders cleaning for businesses across Middlesex.','area-middlesex',area='Middlesex'), needs_form=True)

    # ================= ABOUT =================
    page('about-us','About Us | Contract Cleaning Company London',
      'Kemp Services Ltd is an expert contract cleaning company in London with 30 years\' experience across the Home Counties and the UK. Client focused.',
      [
      phero('An expert contract cleaning company in London.',
        'Welcome to Kemp Services Ltd. Kemp Services has 30 years\' experience providing one-off and contract cleaning services in London and the Home Counties: Essex, Kent, Surrey, Middlesex and Hertfordshire. We also have contracts in Manchester, Newcastle, Nottingham, Liverpool, Cardiff and Birmingham.',
        '1580256081112-e49377338b7f','Housekeeping trolley and vacuum in a carpeted corridor'),
      two('Established, fast-growing, and built on reputation.',[
        '!Based in London, Kemp Services is an established and fast-growing company with a strong foundation and reputation. We meet our customers\' requirements through our knowledge, responsiveness, reliability and our hard-working loyal staff.',
        'We are flexible when the unexpected happens, and our professional cleaning services are tailored to meet the exact needs of our customers. We offer a wide range of commercial cleaning services across all sectors to a myriad of businesses and endeavour to foster long-term relationships with all our customers. We can also provide specific cleaning services, such as '+L('window-cleaning-london')+' and '+L('deep-cleaning','deep cleaning services')+'.',
        'Each customer is different, and your needs may change over time. Our extensive experience in commercial cleaning means that we have the cleaning expertise and knowledge. Regardless of the size of your project, we will deliver a completely bespoke solution to your cleaning requirements. To minimise disruption to your hours of operation, our cleaning operatives can work outside of usual business hours or work alongside your staff without disruption.'],
        side='<ul class="rows plain" style="margin-top:30px"><li>Experienced professional cleaning contractors</li><li>Flexible and friendly approach</li><li>Anticipate and adapt to your needs</li></ul>'),
      split('We are client focused.',[
        'The reputation of Kemp Services has been built on a foundation of delivering professional contract cleaning services, of a high standard, to a wide variety of clients. We offer outstanding customer service, and we continue to improve upon our best.',
        'Our experience as UK cleaning contractors covers a broad range of sectors, including construction, offices, retail outlets, warehouses and welfare facilities. We know how to get the job done to your exact standards, safely, on time and on budget. Your premises need to make the right first impression to your customers and as our customer, we\'ll make sure that happens.'],
        '1437326300822-01d8f13c024f','Cleaner working on a floor beside a white wall',rev=True,white=False),
      rows('Why choose Kemp Services.','',
        ['Customer centric','Over 30 years\' commercial cleaning experience','Flexible and fair business ethos','National coverage, local cleaning operatives','Our contract cleaning work is F.A.C.T. Guaranteed'],plain=True,cols=True),
      two('Your one stop shop for cleaning services.',[
        '!Initially, we will talk through your requirements. We will arrange a site survey to provide you with a free, no obligation, contract cleaning quote. We will tailor our service to meet your budget.',
        'We will be your one stop shop for cleaning services offering one-off or regular cleaning. Our services include '+L('contract-cleaning')+', '+L('office-cleaning')+', '+L('builders-clean')+', '+L('welfare-area-cleaning','welfare clean')+', '+L('communal-block-cleaning')+', '+L('pre-post-tenancy-cleans','pre and post tenancy cleans')+', '+L('carpet-floor-cleaning')+', '+L('deep-cleaning')+' and '+L('window-cleaning-london')+'.'],white=False,
        side='<a class="btn-dark" href="/our-services" style="background:var(--sky);color:var(--navy)">See all our services'+ARROW+'</a>'),
      guar(),
      contact('Talk to us about your premises.'),
      ], needs_guar=True, needs_form=True)

    # ================= CONTACT =================
    page('contact','Contact Kemp Services | Kemp Services Ltd',
      'Contact Kemp Services. Call 020 8983 8593, email info@kempservices.co.uk or send an enquiry. Office hours Monday to Sunday, 7:30am to 7:30pm.',
      [
      phero('Contact Kemp Services.',
        'Are you ready to book your premises a clean and positive atmosphere? We are ready to deliver! Cleaning contractors covering London, the Home Counties and beyond.',
        '1758448500688-3ababa93fd67','Modern lobby with a marble reception desk and plants',cta='Send an enquiry'),
      contact('Get in touch.','Kemp Services is a London-based cleaning contractor based in east London. Most of our customers are based across London, Essex, Kent, Surrey, Middlesex and Hertfordshire. We also have contracts in Manchester, Newcastle, Nottingham, Liverpool, Cardiff and Birmingham. So wherever you are, we have local cleaning teams to take care of your property.',
        extra='<ul class="cinfo"><li><span class="k">Office hours</span><span class="v">Monday to Sunday<br>7:30am to 7:30pm</span></li><li><span class="k">Address</span><span class="v">Kemp Services Ltd<br>Number One, 1 Vicarage Lane<br>Stratford, London E15 4HF</span></li></ul>'),
      two('What our customers say.',[quote()],white=False) if False else f'''<section class="sec white" style="padding-top:0"><div class="w"><h2>What our customers say.</h2>{quote()}</div></section>''',
      towns('Cleaning contractors for London, the Home Counties and beyond.','',['<a class="inl" href="/area-london">London</a>','<a class="inl" href="/contract-cleaning-essex">Essex</a>','<a class="inl" href="/area-kent">Kent</a>','<a class="inl" href="/area-surrey">Surrey</a>','<a class="inl" href="/area-middlesex">Middlesex</a>','Hertfordshire','Manchester','Newcastle','Nottingham','Liverpool','Cardiff','Birmingham'],white=False),
      ], ld='{"@context":"https://schema.org","@type":"ContactPage","name":"Contact Kemp Services Ltd","url":"https://kempservices.co.uk/contact","mainEntity":{"@type":"LocalBusiness","name":"Kemp Services Ltd","telephone":"+442089838593","email":"info@kempservices.co.uk","url":"https://kempservices.co.uk/","openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"07:30","closes":"19:30"}}}', needs_form=True)

    # ================= LEGAL =================
    def legal(slug,title,meta,h1,body_html):
        page(slug,title,meta,[f'''<section class="sec white legal">
  <div class="w">
    <h1>{h1}</h1>
    <p class="stamp">Kemp Services Ltd</p>
    <div class="legal-body" id="ksl-legal-body">{body_html}</div>
  </div>
</section>'''])
    legal('disclaimer','Disclaimer | Kemp Services Ltd','Disclaimer for the Kemp Services Ltd website: content is provided for information only and use of the information on these pages is at your sole risk.','Disclaimer',
      '<p>Content and images on this page are for your information, education and training only. We hope they are valuable and useful to you. Your use of the information contained in these pages, however, is at your sole risk.</p>'
      '<p>Kemp Services Ltd takes reasonable steps to ensure that the information contained in these web pages is accurate and up to date. Our cleaning company does not warrant that the Web site will operate error-free or that this Web site and its server are free of computer viruses and other harmful goods.</p>'
      '<p>All information on these pages is provided "as-is", without any warranty, whether express or implied, of its accuracy, completeness, fitness for a particular purpose, title or non-infringement, and none of the third-party products or information mentioned in the work are authored, recommended, supported or guaranteed by our cleaning agency.</p>'
      '<p>We will not be liable for any damages you may sustain by using this information, whether direct, indirect, special, incidental or consequential, even if it has been advised of the possibility of such damages.</p>')
    legal('privacy-policy','Privacy Policy | Kemp Services Ltd','How Kemp Services Ltd collects, uses and shares your personal information, and your rights under this privacy notice.','Privacy policy',
      '<p>This site is owned and operated by Kemp Services Ltd. Your privacy on the Internet is of the utmost importance to us. We want to make your experience online satisfying and safe.</p>'
      '<p>We take the privacy of your information seriously and we ask that you read this Privacy Notice carefully as it contains important information on: the personal information we collect about you; what we do with your information, and who your information might be shared with.</p>'
      '<p>We won\'t disclose your information to anyone without your consent and prior knowledge, other than as set out in this Privacy Notice and any applicable terms and conditions.</p>')
    legal('terms-conditions','Terms and Conditions | Kemp Services Ltd','Terms and conditions for cleaning services provided by Kemp Services Ltd.','Terms and conditions',
      '')
