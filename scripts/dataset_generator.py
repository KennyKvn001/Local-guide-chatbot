import pandas as pd
import random
from faker import Faker

# Initialize tools
fake = Faker()
random.seed(42)

# 1. Enhanced Q&A Template with Seasonal Variations
qa_templates = {
    "tourism": [
        ("Best place to see mountain gorillas?", "Volcanoes National Park in Musanze offers gorilla trekking."),
        ("What's special about Nyungwe Forest?", "Home to chimpanzees and East Africa's only canopy walk (160m long)."),
        ("Can I do a safari in Rwanda?", "Yes, Akagera National Park has lions, elephants and 500+ bird species."),
        ("Top cultural village to visit?", "Iby'Iwacu Cultural Village near Volcanoes NP shows traditional Rwandan life."),
        ("Where to see traditional Intore dance?", "At the Kandt House Museum in Kigali or during festivals."),
        ("Best time to visit Rwanda?", "June-September (dry season) for gorilla trekking and hiking."),
        ("Entry fee for Volcanoes National Park?", "$100 for foreigners, 15,000 RWF for Rwandans (2025 rates)."),
        ("How long is gorilla trekking?", "2-8 hours depending on gorilla family location."),
        ("Can kids do gorilla trekking?", "Minimum age is 15 for gorilla permits."),
        ("What to pack for Nyungwe canopy walk?", "Sturdy shoes, rain jacket, and camera - it's 70m above ground!"),
        ("Where to see golden monkeys?", "Also in Volcanoes National Park - cheaper than gorilla permits."),
        ("Best hiking trail near Kigali?", "Mount Kigali Trail offers great city views (2-3 hour hike).")
    ],
    "education": [
        ("Top university in Rwanda?", "University of Rwanda is the largest and highest-ranked."),
        ("Where to study computer science?", "University of Rwanda's College of Science and Technology in Nyarugenge."),
        ("Best coding bootcamp?", "ALX Rwanda offers 12-month software engineering programs."),
        ("International schools in Kigali?", "Green Hills Academy, Kigali International Community School, and École Belge."),
        ("Is education free in Rwanda?", "Primary education is free in public schools."),
        ("Where to learn Kinyarwanda?", "University of Rwanda's Language Centre offers courses."),
        ("Technical schools in Rwanda?", "IPRCs (Integrated Polytechnic Regional Colleges) across the country."),
        ("Scholarships for Rwandan students?", "Mastercard Foundation Scholars Program at UR and Kepler."),
        ("Best medical school?", "University of Rwanda's College of Medicine and Health Sciences."),
        ("Where to study hospitality?", "Akilah Institute for Women offers diploma programs."),
        ("Public vs private universities?", "UR is public; AUCA, CMU are private options."),
        ("STEM programs for girls?", "Girls in ICT initiative by RDB and Andela Rwanda.")
    ],
    "healthcare": [
        ("Best hospital in Kigali?", "King Faisal Hospital is the top private facility."),
        ("Public hospitals in Rwanda?", "CHUK (Central Hospital Kigali) and district hospitals."),
        ("Emergency number?", "Dial 112 for police, 912 for medical emergencies."),
        ("Where to get COVID vaccine?", "All district hospitals and health centers."),
        ("Malaria risk in Rwanda?", "Present - use prophylaxis and mosquito nets, especially in rural areas."),
        ("24-hour pharmacy in Kigali?", "King Faisal Hospital pharmacy operates 24/7."),
        ("Dental clinics in Kigali?", "Kigali Dental Clinic in Kimihurura is recommended."),
        ("Mental health services?", "Ndera Neuropsychiatric Hospital specializes in mental health."),
        ("Pediatric hospitals?", "KFH and CHUK both have pediatric wings."),
        ("Health insurance requirements?", "Mandatory for foreigners - RAMA or private insurance."),
        ("Vaccinations needed?", "Yellow fever mandatory; hepatitis A/B, typhoid recommended."),
        ("Where to buy prescription drugs?", "Pharmacies like KIM Pharmacy require doctor's prescription.")
    ],
    "accommodation": [
        ("Budget hostels in Kigali?", "Discover Rwanda Youth Hostel from $10/night."),
        ("Luxury hotels in Kigali?", "Kigali Marriott ($200+) and Serena Hotel ($150+)."),
        ("Best area to stay in Kigali?", "Kimihurura for restaurants, Kiyovu for quiet luxury."),
        ("Eco-lodges near Volcanoes NP?", "Bisate Lodge (luxury) or Red Rocks Rwanda (budget)."),
        ("Lake Kivu resorts?", "Lake Kivu Serena Hotel in Rubavu has lake views."),
        ("Airbnb availability?", "Yes, 300+ listings in Kigali from $20/night."),
        ("Camping in Akagera?", "Yes, Ruzizi Tented Lodge and campsites inside park."),
        ("Hostels near bus stations?", "Okapi Hotel is 5min from Nyabugogo Bus Park."),
        ("Pet-friendly hotels?", "Kigali Marriott allows pets with prior notice."),
        ("Hotels with pools?", "Radisson Blu and Serena both have outdoor pools."),
        ("Long-term apartment rentals?", "Check Kigali Heights or KBC area for 1-3 month leases."),
        ("Guesthouses in Musanze?", "Fatima Guesthouse and La Palme Hotel are popular.")
    ],
    "transport": [
        ("Bus from Kigali to Musanze?", "Volcano Express takes 2.5hrs (~3000 RWF)."),
        ("How to use Tap&Go?", "Buy card at stations, load money for bus fares."),
        ("Moto-taxi safety tips?", "Always wear helmet, agree on fare first (~500-2000 RWF)."),
        ("Car rental companies?", "Europcar, Avis and local companies like Rwanda Car Rentals."),
        ("Kigali airport to city?", "Taxi costs ~10,000 RWF (20min), no Uber available."),
        ("Speed limits in Rwanda?", "50km/h cities, 80km/h highways, strictly enforced."),
        ("Cross-border buses?", "Jaguar Coaches to Kampala, Trinity to Bujumbura."),
        ("Domestic flights?", "Akol Aviation flies Kigali-Kamembe (Lake Kivu)."),
        ("Bicycle rentals?", "Available in Nyamirambo and near Kimironko Market."),
        ("Night buses?", "No intercity buses operate after 8pm typically."),
        ("Parking in Kigali?", "Malls (Kigali Heights, Union Trade Centre) have secure parking."),
        ("Fuel prices?", "~1,300 RWF/liter for petrol (2025 rates).")
    ],
    "business": [
        ("Where to register a company?", "Rwanda Development Board (RDB) One Stop Center."),
        ("Top industries in Rwanda?", "ICT, tourism, agriculture and manufacturing."),
        ("Co-working spaces?", "Norrsken House Kigali and The Office."),
        ("Business license cost?", "Depends on sector - from 50,000 RWF for small business."),
        ("Mobile money usage?", "90% penetration - MTN MoMo and Airtel Money dominate."),
        ("Major banks?", "Bank of Kigali, Equity Bank, and Access Bank."),
        ("Import taxes?", "Varies by product - check RRA (Rwanda Revenue Authority)."),
        ("Top local companies?", "MTN Rwanda, Bralirwa, and Crystal Ventures Ltd."),
        ("Business incubators?", "kLab and Impact Hub Kigali support startups."),
        ("E-commerce platforms?", "Jumia Rwanda and Kasha are most popular."),
        ("Stock exchange?", "Rwanda Stock Exchange has 10+ listed companies."),
        ("Corporate tax rate?", "30% for large companies, 0-20% for small businesses.")
    ],
    "history": [
        ("Pre-colonial kingdoms?", "Kingdom of Rwanda ruled from 15th century to 1961."),
        ("1994 Genocide memorials?", "Kigali Genocide Memorial is main site (Gisozi)."),
        ("First president?", "Grégoire Kayibanda (1962-1973)."),
        ("Traditional courts?", "Gacaca courts tried genocide cases 2001-2012."),
        ("Ancient Rwandan currency?", "Used barter system; later cowrie shells and hoes."),
        ("Colonial periods?", "German (1897-1916) then Belgian rule until 1962 independence."),
        ("Royal palace location?", "Nyanza was historic seat of Rwandan kings."),
        ("Umuganura festival?", "Traditional harvest festival celebrated August 1st."),
        ("Rwandan Patriotic Front?", "Political party that ended genocide in 1994."),
        ("Oldest building?", "Kandt House Museum (1907) in Kigali."),
        ("Traditional kingdoms?", "Rwanda and neighboring Burundi were linked kingdoms."),
        ("Independence date?", "July 1, 1962 from Belgium.")
    ],
    "sports": [
        ("National stadium?", "Amahoro Stadium hosts football matches (25,000 capacity)."),
        ("Rwanda Premier League teams?", "APR FC, Rayon Sports and Kiyovu SC are top clubs."),
        ("Golf courses?", "Kigali Golf Club (18 holes) and Gorilla Golf Club in Musanze."),
        ("Cycling routes?", "Kigali to Musanze (90km) is popular challenge route."),
        ("Basketball teams?", "Patriots BBC represents Rwanda in FIBA Africa."),
        ("Volcano hiking?", "Mount Bisoke (3,711m) is 3-5 hour hike from base."),
        ("Running clubs?", "Kigali Running Club meets Saturdays at 6am in Kimihurura."),
        ("Swimming pools?", "Kigali Serena and Cercle Sportif have public pools."),
        ("Traditional sports?", "High jump (gusimbuka) was historic royal sport."),
        ("Marathons?", "Kigali International Peace Marathon every May."),
        ("Football academies?", "APR FC Academy trains youth players."),
        ("Where to watch sports?", "Pili Pili Bar screens Premier League matches.")
    ],
    "language": [
        ("Hello in Kinyarwanda?", "Muraho (formal) or Bite (informal)."),
        ("Thank you?", "Murakoze (singular) or Murakoze cyane (many thanks)."),
        ("How are you?", "Amakuru? (response: Ni meza)"),
        ("Numbers 1-5?", "Rimwe, kabiri, gatatu, kane, gatanu."),
        ("Where is...?", "He...? (e.g., He hoteli? = Where is the hotel?)"),
        ("How much?", "Ni bangahe?"),
        ("I don't understand", "Sinumva."),
        ("Goodbye", "Murabeho (formal) or Reka (informal)."),
        ("Please", "Nyamuneka."),
        ("Sorry", "Mbabarira."),
        ("Yes/No", "Yego/Oya"),
        ("What's your name?", "Witwa nde?")
    ],
    "services": [
        ("SIM card for tourists?", "MTN or Airtel - need passport at airport or shops."),
        ("Post offices?", "Main one in Kigali City Tower, others in each district."),
        ("Where to recycle?", "COPED in Nyarugenge takes plastics and electronics."),
        ("Laundry services?", "Many guesthouses offer or try Washry in Kimihurura."),
        ("Visa extensions?", "At Directorate General of Immigration in Kimihurura."),
        ("Police stations?", "Each sector has one - main is in Remera, Kigali."),
        ("Where to print documents?", "Copy shops near universities and business districts."),
        ("International shipping?", "DHL has office in Kigali City Tower."),
        ("Lost property?", "Check with local authorities or establishment last visited."),
        ("Tourist police?", "Call 112 or visit nearest tourism office."),
        ("Where to pay bills?", "At banks, online via Irembo, or mobile money."),
        ("Public toilets?", "In shopping malls and petrol stations - carry tissues.")
    ],
    "hyperlocal": [
        ("Best chapati in Nyamirambo?", "Café de Nyamirambo makes fluffy chapatis for 500 RWF."),
        ("Where to buy authentic Agaseke baskets?", "Cooperative des Tresses in Gisozi village."),
        ("Cheapest brochettes in Kigali?", "Brochetterie du Quartier in Kimironko (800 RWF)."),
        ("Best place for Rwandan coffee?", "Question Coffee Café in Kacyiru."),
        ("Where locals buy fabric?", "Sopetrade in Nyabugogo Market has best kitenge selection."),
        ("Hidden gem restaurant?", "Taj Mahal in Remera for Indian-Rwandan fusion."),
        ("Best view of Kigali?", "Top floor of Kigali City Tower observation deck."),
        ("Where to hear live Rwandan music?", "Repub Lounge in Kimihurura on weekends."),
        ("Best place to watch sunsets?", "Rooftop of The Hut in Kiyovu."),
        ("Local hair braiding salon?", "Beauté Noire in Nyamirambo for traditional styles."),
        ("Where to buy fresh passion fruit?", "Early morning at Kimironko Market stalls."),
        ("Best milk bar?", "Inyange Shop near Remera Taxi Park.")
    ],
    
    # Recent developments (2024-2025)
    "new_developments": [
        ("What is Kigali Innovation City?", "Tech hub under construction in Gasaro, will host Carnegie Mellon Africa."),
        ("Newest museum in Rwanda?", "Rwanda Art Museum relocated to former presidential palace in 2024."),
        ("Recent transport upgrades?", "New electric buses launched on Kigali-Gasabo route in 2025."),
        ("Latest tech campus?", "Norrsken Kigali House expansion completed 2024."),
        ("New national park?", "Gishwati-Mukura designated as 4th national park in 2020."),
        ("Recent sports facility?", "Nyamirambo Stadium renovated in 2024 for WNBA Africa Games."),
        ("New border crossing?", "Rusumo One-Stop Border Post with Tanzania opened 2023."),
        ("Latest hotel opening?", "Radisson Blu Kigali Convention Center opened 2025."),
        ("New university programs?", "UR launched AI degree program in 2024."),
        ("Recent infrastructure project?", "Kigali Central Station modernized in 2025."),
        ("New tourism initiative?", "'Visit Rwanda' now includes community-based tourism trails."),
        ("Latest startup hub?", "kLab moved to new larger premises in 2025.")
    ],
    
    # Carefully handled sensitive topics
    "history_sensitive": [
        ("How is the 1994 Genocide taught?", "In schools through official curriculum emphasizing unity and reconciliation."),
        ("Where to learn about genocide history?", "Kigali Genocide Memorial provides comprehensive education."),
        ("Are genocide memorials appropriate for children?", "Main memorial recommends age 12+ for underground exhibits."),
        ("How has Rwanda achieved reconciliation?", "Through Gacaca courts, unity policies, and community initiatives."),
        ("Can I visit genocide sites?", "Yes, with respect - Nyamata and Murambi are preserved memorials."),
        ("Current relations with neighbors?", "Rwanda maintains diplomatic relations with all neighboring countries."),
        ("How to discuss genocide respectfully?", "Avoid graphic details; focus on resilience and rebuilding."),
        ("Are there survivor organizations?", "IBUKA and AERG support survivors through various programs."),
        ("What caused the genocide?", "Complex colonial legacy and political extremism led to the tragedy."),
        ("How long did the genocide last?", "Approximately 100 days from April-July 1994."),
        ("International response during genocide?", "UN peacekeeping mission was present but under-resourced."),
        ("Post-genocide justice process?", "Used Gacaca community courts to try 1.9 million cases.")
    ],
    
    "seasonal": [
        ("Best time to visit Volcanoes NP?", "Dry seasons (Jun-Sep & Dec-Feb) for easier hiking."),
        ("Rainy season trekking tips?", "Pack waterproof gear - trails get muddy Mar-May & Oct-Nov."),
        ("Umbrella or rain jacket?", "Both - sudden downpours common in rainy season."),
        ("Road conditions during rains?", "Some rural roads flood - check with locals before trips."),
        ("Seasonal festivals?", "Umuganura (Aug) - harvest, Kwita Izina (Sep) - gorilla naming."),
        ("Best rainy season activity?", "Museum visits in Kigali or hot springs at Lake Kivu."),
        ("Temperature range December?", "Kigali: 18-28°C; higher altitudes cooler at night."),
        ("When are gorillas easiest to spot?", "Dry season when they stay lower in the forests."),
        ("Seasonal price changes?", "Hotels 20-30% cheaper in rainy season (Mar-May)."),
        ("Nyungwe Forest in April?", "Lush but leeches present - wear leech socks."),
        ("Lake Kivu best season?", "June-August for calm waters and swimming."),
        ("When to see migratory birds?", "November-April in Akagera National Park.")
    ]
}

# 2. Data Generation Function
def generate_qa_dataset(target_rows=500):
    """Generate comprehensive Q&A dataset with balanced domain coverage"""
    rows = []
    
    # Calculate distribution
    main_domains = [d for d in qa_templates.keys() if d not in ["history_sensitive"]]
    sensitive_count = min(int(target_rows * 0.05), len(qa_templates["history_sensitive"]))  # 5% sensitive questions or max available
    
    # Generate main questions
    for domain in main_domains:
        for q, a in qa_templates[domain]:
            for _ in range(2):  # Generate 2 variations per question
                rows.append({
                    "domain": domain,
                    "question": add_variation(q, is_question=True),
                    "answer": add_variation(a, is_question=False)
                })
    
    # Add sensitive questions
    for q, a in random.sample(qa_templates["history_sensitive"], k=sensitive_count):
        rows.append({
            "domain": "history",
            "question": q,
            "answer": a
        })
    
    # Convert to DataFrame and clean
    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["question"])
    
    # Ensure we have exactly target_rows
    if len(df) > target_rows:
        df = df.sample(target_rows)
    elif len(df) < target_rows:
        # Add more variations if needed
        additional = target_rows - len(df)
        extra_rows = pd.DataFrame([create_variation(row) for _, row in df.sample(additional).iterrows()])
        df = pd.concat([df, extra_rows])
    
    return df.reset_index(drop=True)

def add_variation(text, is_question):
    """Add natural language variations to questions/answers"""
    if is_question:
        variations = [
            text,
            text.replace("?", random.choice([" in Rwanda?", " in Kigali?", "?"])),
            f"Can you tell me {text.lower()}",
            f"Where would I find {text.split('?')[0].lower()}?"
        ]
    else:
        variations = [
            text,
            f"{text} (2025 info)",
            f"In Rwanda, {text.lower()}",
            f"Location: {text.split('.')[0]}. Details: {text}"
        ]
    return random.choice(variations)

def create_variation(row):
    """Create a new variation from an existing row"""
    new_row = row.copy()
    new_row["question"] = add_variation(row["question"], is_question=True)
    new_row["answer"] = add_variation(row["answer"], is_question=False)
    return new_row

# Generate and save dataset
df = generate_qa_dataset(520)
df.to_csv("rwanda_qa_comprehensive.csv", index=False)

print(f"✅ Generated {len(df)} Q&A pairs")
print("Sample data:")
print(df.sample(5).to_string(index=False))