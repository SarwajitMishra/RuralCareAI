"""
Offline Healthcare Knowledge Repository for RuralCareAI.

Structured medical information (disease description, precautions,
first aid, referral guidance, emergency warning signs) used to
ground the RAG pipeline and the Local LLM clinical summary.

This is general public-health guidance only and does not replace
professional medical diagnosis or treatment.

Author: Sarwajit Kumar Mishra
"""

from __future__ import annotations

DISEASE_KNOWLEDGE = {

    "(vertigo) Paroymsal  Positional Vertigo": {
        "hindi": "स्थिति बदलने पर चक्कर आना",
        "description": "A condition causing dizziness or spinning sensation when changing head position.",
        "risk": 45,
        "precautions": [
            "Sit or lie down immediately when dizziness begins",
            "Avoid sudden head movements",
            "Avoid driving or operating machinery during episodes",
        ],
        "first_aid": [
            "Help the patient sit or lie down in a safe position",
            "Keep the surroundings well lit and clear of obstacles",
        ],
        "when_to_consult": "If episodes are frequent, prolonged, or accompanied by hearing loss.",
        "emergency_signs": [
            "Sudden severe headache with dizziness",
            "Slurred speech or weakness on one side",
            "Loss of consciousness",
        ],
    },

    "AIDS": {
        "hindi": "एड्स",
        "description": "A chronic disease caused by HIV that weakens the immune system.",
        "risk": 95,
        "precautions": [
            "Practice safe sex and avoid sharing needles",
            "Maintain a nutritious diet and good hygiene",
            "Adhere strictly to prescribed antiretroviral therapy",
        ],
        "first_aid": [
            "No first aid applicable; requires specialist medical management",
        ],
        "when_to_consult": "Immediately, for confirmatory testing and specialist referral.",
        "emergency_signs": [
            "High fever with severe weight loss",
            "Persistent diarrhoea or difficulty breathing",
            "Signs of opportunistic infection",
        ],
    },

    "Acne": {
        "hindi": "मुंहासे",
        "description": "A common skin condition causing pimples and inflammation.",
        "risk": 10,
        "precautions": [
            "Wash the face gently twice a day",
            "Avoid squeezing or picking at pimples",
            "Use non-comedogenic skin products",
        ],
        "first_aid": [
            "Keep the affected area clean and dry",
        ],
        "when_to_consult": "If acne is severe, painful, or leaves scarring.",
        "emergency_signs": [
            "Signs of spreading skin infection (fever, pus, redness spreading)",
        ],
    },

    "Alcoholic hepatitis": {
        "hindi": "अल्कोहलिक हेपेटाइटिस",
        "description": "Inflammation of the liver caused by excessive alcohol consumption.",
        "risk": 70,
        "precautions": [
            "Stop alcohol consumption completely",
            "Maintain a balanced, low-fat diet",
            "Avoid over-the-counter drugs that stress the liver (e.g. paracetamol overuse)",
        ],
        "first_aid": [
            "No specific first aid; seek medical evaluation",
        ],
        "when_to_consult": "Promptly, especially if jaundice, confusion, or abdominal swelling develop.",
        "emergency_signs": [
            "Yellowing of skin/eyes with confusion",
            "Vomiting blood or black stools",
            "Severe abdominal swelling",
        ],
    },

    "Allergy": {
        "hindi": "एलर्जी",
        "description": "An immune reaction to normally harmless substances.",
        "risk": 15,
        "precautions": [
            "Identify and avoid known allergens",
            "Keep antihistamines available if prescribed",
            "Keep living areas clean and dust-free",
        ],
        "first_aid": [
            "Move away from the suspected allergen",
            "Take an antihistamine if previously advised by a doctor",
        ],
        "when_to_consult": "If reactions are recurrent or worsening.",
        "emergency_signs": [
            "Swelling of face, lips, or throat",
            "Difficulty breathing",
            "Widespread hives with dizziness (possible anaphylaxis)",
        ],
    },

    "Arthritis": {
        "hindi": "गठिया",
        "description": "Inflammation of joints causing pain and stiffness.",
        "risk": 40,
        "precautions": [
            "Maintain a healthy weight to reduce joint stress",
            "Stay physically active with low-impact exercise",
            "Apply warm or cold compresses for symptom relief",
        ],
        "first_aid": [
            "Rest the affected joint",
            "Apply a cold compress to reduce swelling",
        ],
        "when_to_consult": "If joint pain persists, worsens, or limits daily activity.",
        "emergency_signs": [
            "Sudden severe joint swelling with fever",
            "Inability to move the joint at all",
        ],
    },

    "Bronchial Asthma": {
        "hindi": "दमा / अस्थमा",
        "description": "A chronic respiratory disease causing breathing difficulty.",
        "risk": 40,
        "precautions": [
            "Avoid known triggers (dust, smoke, pollen, cold air)",
            "Keep a rescue inhaler accessible at all times",
            "Follow the prescribed asthma action plan",
        ],
        "first_aid": [
            "Help the patient sit upright",
            "Use a rescue inhaler if available",
            "Encourage slow, steady breathing",
        ],
        "when_to_consult": "If attacks are frequent or the inhaler gives insufficient relief.",
        "emergency_signs": [
            "Severe breathlessness at rest",
            "Bluish lips or fingertips",
            "Inability to speak full sentences due to breathlessness",
        ],
    },

    "Cervical spondylosis": {
        "hindi": "गर्दन की स्पॉन्डिलोसिस",
        "description": "Age-related degeneration of the cervical spine.",
        "risk": 35,
        "precautions": [
            "Maintain good posture, especially while using screens",
            "Use a supportive pillow while sleeping",
            "Do gentle neck stretching exercises",
        ],
        "first_aid": [
            "Rest the neck and avoid sudden movements",
            "Apply a warm compress to ease stiffness",
        ],
        "when_to_consult": "If pain radiates to the arms or is accompanied by numbness.",
        "emergency_signs": [
            "Loss of bladder/bowel control",
            "Weakness or numbness spreading to limbs",
        ],
    },

    "Chicken pox": {
        "hindi": "चेचक",
        "description": "A contagious viral infection causing itchy blisters.",
        "risk": 35,
        "precautions": [
            "Isolate the patient to prevent spread",
            "Keep fingernails trimmed to avoid scratching",
            "Maintain hydration and rest",
        ],
        "first_aid": [
            "Apply calamine lotion to relieve itching",
            "Give lukewarm baths with baking soda or oatmeal",
        ],
        "when_to_consult": "If fever is high, or blisters show signs of bacterial infection.",
        "emergency_signs": [
            "Difficulty breathing",
            "Persistent high fever with confusion",
            "Signs of severe skin infection (spreading redness, pus)",
        ],
    },

    "Chronic cholestasis": {
        "hindi": "दीर्घकालिक पित्त अवरोध",
        "description": "A condition where bile flow from the liver is reduced.",
        "risk": 65,
        "precautions": [
            "Follow a low-fat diet as advised",
            "Avoid alcohol and unnecessary medications",
            "Monitor for worsening jaundice",
        ],
        "first_aid": [
            "No specific first aid; requires medical evaluation",
        ],
        "when_to_consult": "Promptly for liver function evaluation.",
        "emergency_signs": [
            "Severe abdominal pain with fever",
            "Vomiting blood or black stools",
        ],
    },

    "Common Cold": {
        "hindi": "साधारण सर्दी",
        "description": "A viral infection affecting the upper respiratory tract.",
        "risk": 20,
        "precautions": [
            "Rest and stay well hydrated",
            "Cover mouth and nose while coughing or sneezing",
            "Wash hands frequently",
        ],
        "first_aid": [
            "Steam inhalation to ease congestion",
            "Warm fluids such as soup or herbal tea",
        ],
        "when_to_consult": "If symptoms persist beyond 10 days or worsen.",
        "emergency_signs": [
            "High fever with breathing difficulty",
            "Severe chest pain",
        ],
    },

    "Dengue": {
        "hindi": "डेंगू",
        "description": "A mosquito-borne viral infection causing fever and body pain.",
        "risk": 75,
        "precautions": [
            "Use mosquito nets and repellents",
            "Eliminate stagnant water near living areas",
            "Avoid aspirin/ibuprofen; use only paracetamol if advised",
        ],
        "first_aid": [
            "Ensure adequate fluid intake",
            "Monitor temperature and rest",
        ],
        "when_to_consult": "Promptly for blood platelet monitoring, especially with high fever.",
        "emergency_signs": [
            "Bleeding from gums or nose",
            "Severe abdominal pain with vomiting",
            "Cold, clammy skin or restlessness (possible shock)",
        ],
    },

    "Diabetes ": {
        "hindi": "मधुमेह",
        "description": "A disease characterized by elevated blood sugar levels.",
        "risk": 55,
        "precautions": [
            "Follow a balanced, low-sugar diet",
            "Exercise regularly and monitor blood sugar",
            "Take prescribed medication/insulin on schedule",
        ],
        "first_aid": [
            "If unusually weak or shaky, check blood sugar if a glucometer is available",
        ],
        "when_to_consult": "Regularly for monitoring; promptly if sugar levels are erratic.",
        "emergency_signs": [
            "Confusion or loss of consciousness",
            "Fruity-smelling breath with rapid breathing",
            "Very high or very low blood sugar readings",
        ],
    },

    "Dimorphic hemmorhoids(piles)": {
        "hindi": "बवासीर",
        "description": "Swollen veins in the lower rectum and anus.",
        "risk": 35,
        "precautions": [
            "Increase dietary fibre and fluid intake",
            "Avoid straining during bowel movements",
            "Avoid prolonged sitting",
        ],
        "first_aid": [
            "Warm sitz baths for relief",
            "Use over-the-counter topical relief if previously advised",
        ],
        "when_to_consult": "If bleeding is persistent or pain is severe.",
        "emergency_signs": [
            "Heavy rectal bleeding",
            "Severe pain with swelling",
        ],
    },

    "Drug Reaction": {
        "hindi": "दवा प्रतिक्रिया",
        "description": "An adverse response to a medication.",
        "risk": 45,
        "precautions": [
            "Stop the suspected medication immediately",
            "Inform healthcare workers of known drug allergies",
            "Keep a record of medications that caused reactions",
        ],
        "first_aid": [
            "Stop the medication and monitor closely",
            "Take an antihistamine if previously advised for mild reactions",
        ],
        "when_to_consult": "Promptly, and always before restarting any suspected medication.",
        "emergency_signs": [
            "Swelling of face, lips, or throat",
            "Difficulty breathing",
            "Widespread rash with dizziness or fainting",
        ],
    },

    "Fungal infection": {
        "hindi": "फंगल संक्रमण",
        "description": "An infection caused by fungi affecting various body parts.",
        "risk": 20,
        "precautions": [
            "Keep the affected area clean and dry",
            "Avoid sharing towels or clothing",
            "Wear breathable, loose-fitting clothing",
        ],
        "first_aid": [
            "Wash and dry the area thoroughly",
            "Apply antifungal powder/cream if previously advised",
        ],
        "when_to_consult": "If the infection spreads or does not improve with basic hygiene care.",
        "emergency_signs": [
            "Spreading redness with fever",
            "Signs of secondary bacterial infection",
        ],
    },

    "GERD": {
        "hindi": "एसिड रिफ्लक्स / अम्लता",
        "description": "A digestive disorder where stomach acid flows back into the food pipe.",
        "risk": 35,
        "precautions": [
            "Avoid spicy, oily, and acidic foods",
            "Eat smaller meals and avoid lying down right after eating",
            "Avoid smoking and excess caffeine",
        ],
        "first_aid": [
            "Sit upright and avoid further food intake temporarily",
        ],
        "when_to_consult": "If symptoms are frequent or affect swallowing.",
        "emergency_signs": [
            "Chest pain resembling a heart attack",
            "Vomiting blood or black stools",
            "Difficulty swallowing",
        ],
    },

    "Gastroenteritis": {
        "hindi": "पेट और आंत का संक्रमण",
        "description": "Inflammation of the stomach and intestines.",
        "risk": 50,
        "precautions": [
            "Drink safe, clean water and maintain hygiene",
            "Wash hands before eating and after using the toilet",
            "Avoid street food during outbreaks",
        ],
        "first_aid": [
            "Give oral rehydration solution (ORS) frequently",
            "Encourage rest and light, easily digestible food",
        ],
        "when_to_consult": "If diarrhoea/vomiting persists beyond 2 days or dehydration signs appear.",
        "emergency_signs": [
            "Signs of severe dehydration (sunken eyes, no urination, lethargy)",
            "Blood in stool or vomit",
            "High fever with severe abdominal pain",
        ],
    },

    "Heart attack": {
        "hindi": "हृदयाघात",
        "description": "A medical emergency caused by blockage of blood flow to the heart.",
        "risk": 95,
        "precautions": [
            "Manage blood pressure, cholesterol, and blood sugar",
            "Avoid smoking and maintain a heart-healthy diet",
            "Stay physically active as advised by a doctor",
        ],
        "first_aid": [
            "Call emergency medical services immediately",
            "Help the patient sit in a comfortable, upright position",
            "Give aspirin only if not allergic and already advised by a doctor",
        ],
        "when_to_consult": "This is a medical emergency — seek immediate care.",
        "emergency_signs": [
            "Crushing chest pain radiating to arm/jaw",
            "Severe breathlessness or sweating",
            "Loss of consciousness",
        ],
    },

    "Hepatitis B": {
        "hindi": "हेपेटाइटिस बी",
        "description": "A viral infection affecting the liver.",
        "risk": 80,
        "precautions": [
            "Get vaccinated where available",
            "Avoid sharing needles or personal items like razors",
            "Practice safe sex",
        ],
        "first_aid": [
            "No specific first aid; requires medical evaluation",
        ],
        "when_to_consult": "Promptly for liver function tests and specialist care.",
        "emergency_signs": [
            "Severe jaundice with confusion",
            "Vomiting blood or black stools",
        ],
    },

    "Hepatitis C": {
        "hindi": "हेपेटाइटिस सी",
        "description": "A liver infection caused by the Hepatitis C virus.",
        "risk": 80,
        "precautions": [
            "Avoid sharing needles or personal items like razors",
            "Avoid alcohol consumption",
            "Get tested if exposure risk is suspected",
        ],
        "first_aid": [
            "No specific first aid; requires medical evaluation",
        ],
        "when_to_consult": "Promptly for liver function tests and specialist care.",
        "emergency_signs": [
            "Severe jaundice with confusion",
            "Vomiting blood or black stools",
        ],
    },

    "Hepatitis D": {
        "hindi": "हेपेटाइटिस डी",
        "description": "A serious liver infection occurring with Hepatitis B.",
        "risk": 85,
        "precautions": [
            "Get vaccinated against Hepatitis B (prevents Hepatitis D)",
            "Avoid sharing needles or personal items",
            "Avoid alcohol consumption",
        ],
        "first_aid": [
            "No specific first aid; requires urgent medical evaluation",
        ],
        "when_to_consult": "Urgently, given the risk of rapid liver damage.",
        "emergency_signs": [
            "Severe jaundice with confusion",
            "Vomiting blood or black stools",
        ],
    },

    "Hepatitis E": {
        "hindi": "हेपेटाइटिस ई",
        "description": "A viral liver infection commonly spread through contaminated water.",
        "risk": 75,
        "precautions": [
            "Drink safe, clean, boiled or filtered water",
            "Maintain good food and water hygiene",
            "Avoid alcohol during recovery",
        ],
        "first_aid": [
            "Rest and maintain hydration",
        ],
        "when_to_consult": "Promptly, especially in pregnant patients given higher risk.",
        "emergency_signs": [
            "Severe jaundice with confusion",
            "Vomiting blood or black stools",
        ],
    },

    "Hypertension ": {
        "hindi": "उच्च रक्तचाप",
        "description": "Persistently elevated blood pressure.",
        "risk": 60,
        "precautions": [
            "Reduce salt intake and maintain a healthy weight",
            "Exercise regularly and manage stress",
            "Take prescribed medication consistently",
        ],
        "first_aid": [
            "Help the patient rest in a calm, seated position",
            "Check blood pressure if a monitor is available",
        ],
        "when_to_consult": "Regularly for monitoring; promptly if readings are very high.",
        "emergency_signs": [
            "Severe headache with vision changes",
            "Chest pain or breathlessness",
            "Confusion or slurred speech",
        ],
    },

    "Hyperthyroidism": {
        "hindi": "अतिसक्रिय थायरॉइड",
        "description": "A condition where the thyroid gland produces excess hormones.",
        "risk": 45,
        "precautions": [
            "Follow prescribed medication regularly",
            "Avoid excess iodine intake unless advised",
            "Manage stress and get adequate rest",
        ],
        "first_aid": [
            "No specific first aid; requires medical evaluation",
        ],
        "when_to_consult": "If symptoms such as rapid heartbeat, tremors, or weight loss appear.",
        "emergency_signs": [
            "Very rapid or irregular heartbeat",
            "High fever with confusion (possible thyroid storm)",
        ],
    },

    "Hypoglycemia": {
        "hindi": "निम्न रक्त शर्करा",
        "description": "A condition where blood sugar falls below normal levels.",
        "risk": 55,
        "precautions": [
            "Do not skip meals, especially if on diabetes medication",
            "Carry a fast-acting sugar source at all times",
            "Monitor blood sugar regularly if diabetic",
        ],
        "first_aid": [
            "Give sugar, juice, or a glucose tablet immediately",
            "Recheck symptoms after 15 minutes; repeat if needed",
        ],
        "when_to_consult": "If episodes are frequent or the patient loses consciousness.",
        "emergency_signs": [
            "Loss of consciousness",
            "Seizures",
            "Inability to swallow safely",
        ],
    },

    "Hypothyroidism": {
        "hindi": "अल्पसक्रिय थायरॉइड",
        "description": "A condition where the thyroid gland produces insufficient hormones.",
        "risk": 45,
        "precautions": [
            "Take prescribed thyroid medication consistently",
            "Maintain a balanced diet",
            "Get regular thyroid function monitoring",
        ],
        "first_aid": [
            "No specific first aid; requires medical evaluation",
        ],
        "when_to_consult": "If fatigue, weight gain, or cold intolerance persist.",
        "emergency_signs": [
            "Severe lethargy or confusion",
            "Very slow heart rate with low body temperature",
        ],
    },

    "Impetigo": {
        "hindi": "त्वचा का जीवाणु संक्रमण",
        "description": "A contagious bacterial skin infection.",
        "risk": 25,
        "precautions": [
            "Keep the affected area clean and covered",
            "Avoid sharing towels, clothing, or bedding",
            "Wash hands frequently",
        ],
        "first_aid": [
            "Gently clean the area with soap and water",
            "Avoid scratching or touching the sores",
        ],
        "when_to_consult": "If sores spread, worsen, or do not heal with basic hygiene care.",
        "emergency_signs": [
            "Fever with spreading redness",
            "Signs of deeper tissue infection",
        ],
    },

    "Jaundice": {
        "hindi": "पीलिया",
        "description": "Yellowing of skin and eyes due to liver dysfunction.",
        "risk": 65,
        "precautions": [
            "Avoid alcohol and unnecessary medications",
            "Maintain a low-fat, nutritious diet",
            "Stay well hydrated",
        ],
        "first_aid": [
            "Rest and maintain hydration",
        ],
        "when_to_consult": "Promptly for evaluation of the underlying cause.",
        "emergency_signs": [
            "Confusion or drowsiness",
            "Vomiting blood or black stools",
            "Severe abdominal pain",
        ],
    },

    "Malaria": {
        "hindi": "मलेरिया",
        "description": "A mosquito-borne parasitic disease.",
        "risk": 75,
        "precautions": [
            "Use mosquito nets and repellents",
            "Eliminate stagnant water near living areas",
            "Complete the full course of antimalarial treatment if prescribed",
        ],
        "first_aid": [
            "Rest and maintain hydration",
            "Manage fever with paracetamol if advised",
        ],
        "when_to_consult": "Promptly for blood testing and antimalarial treatment.",
        "emergency_signs": [
            "Confusion or seizures",
            "Very high fever with chills and rigors",
            "Yellowing of eyes or dark urine",
        ],
    },

    "Migraine": {
        "hindi": "आधे सिर का तेज दर्द",
        "description": "A neurological condition causing recurring severe headaches.",
        "risk": 45,
        "precautions": [
            "Identify and avoid personal triggers (light, stress, certain foods)",
            "Maintain regular sleep and meal schedules",
            "Stay hydrated",
        ],
        "first_aid": [
            "Rest in a quiet, dark room",
            "Apply a cold compress to the forehead",
        ],
        "when_to_consult": "If headaches are frequent, severe, or disrupt daily life.",
        "emergency_signs": [
            "Sudden 'worst headache of life'",
            "Headache with weakness, confusion, or vision loss",
            "Headache following a head injury",
        ],
    },

    "Osteoarthristis": {
        "hindi": "ऑस्टियोआर्थराइटिस",
        "description": "Degeneration of joint cartilage causing pain and stiffness.",
        "risk": 40,
        "precautions": [
            "Maintain a healthy weight",
            "Engage in low-impact exercise regularly",
            "Use supportive footwear",
        ],
        "first_aid": [
            "Rest the joint and apply a warm or cold compress",
        ],
        "when_to_consult": "If pain limits mobility or daily activities.",
        "emergency_signs": [
            "Sudden severe swelling with fever",
            "Inability to bear weight on the joint",
        ],
    },

    "Paralysis (brain hemorrhage)": {
        "hindi": "लकवा (मस्तिष्क रक्तस्राव)",
        "description": "Loss of muscle function due to bleeding in the brain.",
        "risk": 95,
        "precautions": [
            "Manage blood pressure and avoid smoking",
            "Regular health checkups for at-risk patients",
        ],
        "first_aid": [
            "Call emergency medical services immediately",
            "Keep the patient still, note the time symptoms started",
            "Do not give food or water if swallowing is impaired",
        ],
        "when_to_consult": "This is a medical emergency — seek immediate care.",
        "emergency_signs": [
            "Sudden weakness or numbness on one side",
            "Slurred speech or facial drooping",
            "Sudden severe headache or loss of consciousness",
        ],
    },

    "Peptic ulcer diseae": {
        "hindi": "पेप्टिक अल्सर",
        "description": "Painful sores in the stomach lining.",
        "risk": 55,
        "precautions": [
            "Avoid spicy, oily foods, alcohol, and smoking",
            "Avoid unnecessary use of painkillers (NSAIDs)",
            "Eat smaller, regular meals",
        ],
        "first_aid": [
            "Avoid further irritant foods until evaluated",
        ],
        "when_to_consult": "If pain is persistent or associated with weight loss.",
        "emergency_signs": [
            "Vomiting blood or black, tarry stools",
            "Sudden severe abdominal pain",
        ],
    },

    "Pneumonia": {
        "hindi": "फेफड़ों का संक्रमण",
        "description": "An infection causing inflammation of the lungs.",
        "risk": 85,
        "precautions": [
            "Get vaccinated where recommended (children, elderly)",
            "Avoid smoking and exposure to smoke",
            "Maintain good hand hygiene",
        ],
        "first_aid": [
            "Help the patient rest in a comfortable, upright position",
            "Encourage fluid intake",
        ],
        "when_to_consult": "Promptly, especially in children, the elderly, or with high fever.",
        "emergency_signs": [
            "Severe breathlessness or bluish lips",
            "High fever with confusion",
            "Chest pain worsening with breathing",
        ],
    },

    "Psoriasis": {
        "hindi": "सोरायसिस",
        "description": "A chronic autoimmune skin disease.",
        "risk": 30,
        "precautions": [
            "Moisturize skin regularly",
            "Avoid known triggers (stress, skin injury, certain medications)",
            "Avoid excessive alcohol and smoking",
        ],
        "first_aid": [
            "Keep skin moisturized and avoid scratching",
        ],
        "when_to_consult": "If patches spread, worsen, or affect joints.",
        "emergency_signs": [
            "Widespread skin redness with fever",
            "Signs of skin infection",
        ],
    },

    "Tuberculosis": {
        "hindi": "क्षय रोग (टीबी)",
        "description": "A bacterial infection primarily affecting the lungs.",
        "risk": 90,
        "precautions": [
            "Complete the full course of prescribed anti-TB medication",
            "Cover mouth while coughing and ensure good ventilation",
            "Maintain good nutrition",
        ],
        "first_aid": [
            "No specific first aid; requires medical evaluation and treatment",
        ],
        "when_to_consult": "Promptly for testing and treatment; TB is treatable but requires supervision.",
        "emergency_signs": [
            "Coughing up blood",
            "Severe breathlessness",
            "High fever with significant weight loss",
        ],
    },

    "Typhoid": {
        "hindi": "टाइफाइड बुखार",
        "description": "A bacterial infection spread through contaminated food and water.",
        "risk": 65,
        "precautions": [
            "Drink safe, clean, boiled or filtered water",
            "Maintain good food hygiene",
            "Complete the full course of prescribed antibiotics",
        ],
        "first_aid": [
            "Rest and maintain hydration with ORS",
            "Manage fever with paracetamol if advised",
        ],
        "when_to_consult": "Promptly for testing and antibiotic treatment.",
        "emergency_signs": [
            "Severe abdominal pain with rigidity",
            "Confusion or persistent high fever",
            "Blood in stool",
        ],
    },

    "Urinary tract infection": {
        "hindi": "मूत्र मार्ग संक्रमण",
        "description": "An infection affecting the urinary system.",
        "risk": 45,
        "precautions": [
            "Drink plenty of water",
            "Maintain good personal hygiene",
            "Urinate regularly, do not hold urine for long periods",
        ],
        "first_aid": [
            "Increase fluid intake",
        ],
        "when_to_consult": "If symptoms persist beyond 2 days or fever develops.",
        "emergency_signs": [
            "High fever with back/flank pain",
            "Blood in urine",
            "Confusion (especially in elderly patients)",
        ],
    },

    "Varicose veins": {
        "hindi": "वैरिकोज वेन्स",
        "description": "Enlarged and twisted veins commonly affecting the legs.",
        "risk": 35,
        "precautions": [
            "Avoid prolonged standing or sitting",
            "Elevate legs when resting",
            "Maintain a healthy weight and stay active",
        ],
        "first_aid": [
            "Rest with legs elevated",
        ],
        "when_to_consult": "If veins become painful, swollen, or skin changes appear.",
        "emergency_signs": [
            "Sudden painful swelling in the leg (possible clot)",
            "Skin ulceration or bleeding from the vein",
        ],
    },

    # ----------------------------------------------------------
    # Skin-image (CNN) classes - HAM10000 dermatological lesion
    # types. Keys must match models/image_class_mapping.json
    # exactly, so the fusion engine's image-override path (see
    # src/ml/fusion_engine.py) resolves to a real, matching entry
    # instead of falling through to an unrelated ChromaDB semantic
    # match when the predicted disease is an image-only class.
    # ----------------------------------------------------------

    "Actinic_Keratosis": {
        "hindi": "एक्टिनिक केराटोसिस",
        "description": "A rough, scaly patch on sun-exposed skin caused by years of UV exposure; considered a precancerous lesion.",
        "risk": 55,
        "precautions": [
            "Avoid direct sun exposure, especially during peak hours",
            "Use broad-spectrum sunscreen and wear protective clothing",
            "Do not scratch, pick, or attempt to remove the patch",
        ],
        "first_aid": [
            "Protect the affected area from further sun exposure",
        ],
        "when_to_consult": "For any new, rough, or scaly patch on sun-exposed skin - a dermatologist should evaluate it to rule out progression.",
        "emergency_signs": [
            "Rapid growth, bleeding, or ulceration of the patch",
        ],
    },

    "Basal_Cell_Carcinoma": {
        "hindi": "बेसल सेल कार्सिनोमा",
        "description": "The most common type of skin cancer - slow-growing and rarely spreads internally, but locally destructive if left untreated.",
        "risk": 70,
        "precautions": [
            "Use sun protection and avoid prolonged direct sun exposure",
            "Perform regular skin self-examinations",
            "Avoid trauma or scratching of the lesion",
        ],
        "first_aid": [
            "Keep the area clean and protected from further sun exposure",
        ],
        "when_to_consult": "Promptly, for any new pearly or waxy bump, or a sore that does not heal or bleeds easily.",
        "emergency_signs": [
            "Rapid growth, significant bleeding, or signs of spreading infection",
        ],
    },

    "Benign_Keratosis": {
        "hindi": "बिनाइन केराटोसिस",
        "description": "A common, non-cancerous skin growth (such as a seborrheic keratosis) that can sometimes resemble a cancerous lesion.",
        "risk": 15,
        "precautions": [
            "Monitor the growth for changes in size, color, or shape",
            "Avoid picking, scratching, or irritating the area",
        ],
        "first_aid": [
            "Keep the area clean and dry",
        ],
        "when_to_consult": "If the growth changes rapidly, becomes painful, bleeds, or looks different from surrounding moles.",
        "emergency_signs": [
            "Rapid change in appearance, bleeding, or ulceration",
        ],
    },

    "Dermatofibroma": {
        "hindi": "डर्मेटोफाइब्रोमा",
        "description": "A benign, firm skin nodule (often on the legs) that is harmless but can occasionally be itchy or tender.",
        "risk": 10,
        "precautions": [
            "Avoid trauma or repeated friction to the area",
            "Do not attempt to remove the nodule at home",
        ],
        "first_aid": [
            "Keep the area clean; avoid scratching",
        ],
        "when_to_consult": "If the nodule grows rapidly, becomes painful, or changes color or shape.",
        "emergency_signs": [
            "Rapid growth, ulceration, or bleeding",
        ],
    },

    "Melanocytic_Nevus": {
        "hindi": "तिल (मेलानोसाइटिक नीवस)",
        "description": "A common mole, usually benign, but should be monitored for changes that could indicate melanoma risk.",
        "risk": 20,
        "precautions": [
            "Use sun protection and avoid excessive sun exposure",
            "Self-examine moles periodically using the ABCDE rule (Asymmetry, Border, Color, Diameter, Evolving)",
        ],
        "first_aid": [
            "No first aid needed for a stable, unchanged mole",
        ],
        "when_to_consult": "If the mole changes in size, shape, or color, becomes itchy, or bleeds.",
        "emergency_signs": [
            "Rapid change in mole appearance, new bleeding, or ulceration",
        ],
    },

    "Melanoma": {
        "hindi": "मेलानोमा",
        "description": "The most dangerous form of skin cancer; can spread rapidly to other organs if not detected and treated early.",
        "risk": 90,
        "precautions": [
            "Use sun protection and avoid tanning beds",
            "Perform regular skin checks using the ABCDE rule",
            "Seek prompt evaluation of any suspicious mole or lesion",
        ],
        "first_aid": [
            "No first aid applicable at home; avoid further sun exposure to the area",
        ],
        "when_to_consult": "Urgently - any suspicious mole or lesion with ABCDE warning features needs immediate dermatologist evaluation.",
        "emergency_signs": [
            "Rapid growth, bleeding, ulceration, satellite lesions, or swollen nearby lymph nodes",
        ],
    },

    "Vascular_Lesion": {
        "hindi": "वैस्कुलर लीजन",
        "description": "An abnormality of blood vessels in or under the skin (such as a hemangioma or cherry angioma), usually benign.",
        "risk": 15,
        "precautions": [
            "Protect the lesion from trauma or injury that could cause bleeding",
            "Monitor for changes in size or appearance",
        ],
        "first_aid": [
            "Apply gentle pressure if the lesion bleeds from a minor injury",
        ],
        "when_to_consult": "If the lesion grows rapidly, bleeds frequently, or becomes cosmetically or functionally concerning.",
        "emergency_signs": [
            "Uncontrolled bleeding, rapid growth, or signs of infection",
        ],
    },
}

DEFAULT_KNOWLEDGE = {
    "hindi": "",
    "description": "General health condition requiring clinical evaluation.",
    "risk": 50,
    "precautions": [
        "Maintain good hygiene and rest",
        "Stay hydrated and monitor symptoms",
    ],
    "first_aid": [
        "Provide basic supportive care and monitor the patient",
    ],
    "when_to_consult": "If symptoms persist, worsen, or cause concern.",
    "emergency_signs": [
        "Severe pain, breathlessness, or loss of consciousness",
    ],
}


def get_disease_knowledge(disease: str) -> dict:
    """
    Return the structured knowledge entry for a disease,
    falling back to a generic entry if not curated.
    """
    return DISEASE_KNOWLEDGE.get(disease, DEFAULT_KNOWLEDGE)
