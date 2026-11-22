# v4: new pairs (Dolo 650, Telma, Thyronorm) and strength variants. Extends data.py / data_more.py in place.
# PRICES for every pair added here are PLACEHOLDERS. CLINICAL TEXT is a draft for pharmacist review.
from data import COMPANIES, SALTS, PAIRS
from data_more import MORE, COMPANY_MORE, AREA_DESC

# ---------------- companies ----------------
COMPANIES.update({
 "micro": dict(name="Micro Labs Ltd", short="Micro Labs", hq="Bengaluru, Karnataka", parent="Independent", founded="1973", listed="Privately held",
     about="Micro Labs is a Bengaluru-based pharmaceutical company with heart, diabetes, eye-care and pain-relief medicines. Dolo is its paracetamol range.",
     areas=["Pain", "Cardiology", "Diabetes", "Ophthalmology"], website="https://www.microlabsltd.com"),
 "ipca": dict(name="Ipca Laboratories Ltd", short="Ipca", hq="Mumbai, Maharashtra", parent="Independent", founded="1949", listed="Listed on NSE and BSE",
     about="Ipca Laboratories is a Mumbai-headquartered company and a leading maker of pain-relief and anti-malarial medicines, with a large export business. Pacimol is its paracetamol range.",
     areas=["Pain", "Anti-malarials", "Cardiology", "Dermatology"], website="https://www.ipca.com"),
 "glenmark": dict(name="Glenmark Pharmaceuticals Ltd", short="Glenmark", hq="Mumbai, Maharashtra", parent="Independent", founded="1977", listed="Listed on NSE and BSE",
     about="Glenmark is a research-led global pharmaceutical company headquartered in Mumbai. Telma is its telmisartan range.",
     areas=["Cardiology", "Respiratory", "Dermatology", "Diabetes"], website="https://www.glenmarkpharma.com"),
 "mankind": dict(name="Mankind Pharma Ltd", short="Mankind", hq="New Delhi, Delhi", parent="Independent", founded="1995", listed="Listed on NSE and BSE",
     about="Mankind Pharma is a New Delhi-based company and one of India's largest drug makers by prescription volume, known for affordable branded medicines. Telmikind is its telmisartan range.",
     areas=["Cardiology", "Anti-infectives", "Women's health", "Dermatology"], website="https://www.mankindpharma.com"),
 "macleods": dict(name="Macleods Pharmaceuticals Ltd", short="Macleods", hq="Mumbai, Maharashtra", parent="Independent", founded="1989", listed="Privately held",
     about="Macleods Pharmaceuticals is a privately held Mumbai-based company with a large presence in thyroid, heart, anti-TB and anti-infective medicines. Thyrox is its levothyroxine range.",
     areas=["Thyroid", "Anti-TB", "Cardiology", "Anti-infectives"], website="https://www.macleodspharma.com"),
})
COMPANIES["abbott"]["about"] += " Thyronorm is its levothyroxine range."
COMPANY_MORE.update({
 "micro": dict(ticker="Unlisted", founder="G. C. Surana", known=["Dolo", "Amlong", "Diapride", "Arbitel"],
     quality="Micro Labs manufactures at several plants in India, some approved by international regulators, under Schedule M good manufacturing practice."),
 "ipca": dict(ticker="NSE: IPCALAB", founder="—", known=["Zerodol", "Pacimol", "HCQS", "Lariago"],
     quality="Ipca makes both active ingredients and finished medicines at multiple Indian plants, several approved by regulators such as the US FDA and WHO."),
 "glenmark": dict(ticker="NSE: GLENMARK", founder="Gracias Saldanha", known=["Telma", "Telma-H", "Telma-AM", "Ascoril", "Candid"],
     quality="Glenmark has manufacturing sites in India and abroad, several approved by regulators such as the US FDA and UK MHRA."),
 "mankind": dict(ticker="NSE: MANKIND", founder="Ramesh Juneja", known=["Manforce", "Telmikind", "Unwanted-72", "Gas-O-Fast"],
     quality="Mankind manufactures at multiple plants across India under Schedule M good manufacturing practice."),
 "macleods": dict(ticker="Unlisted", founder="—", known=["Thyrox", "Macpod"],
     quality="Macleods runs manufacturing plants in India, several approved by regulators such as WHO, under Schedule M good manufacturing practice."),
})
AREA_DESC.update({"Ophthalmology": "Eye drops and medicines for eye conditions.", "Anti-malarials": "Medicines to prevent and treat malaria."})

# ---------------- salts ----------------
SALTS.update({
 "paracetamol": dict(
    name="Paracetamol", alias="Acetaminophen", cls="Analgesic and antipyretic (non-opioid)", therapeutic="Pain & fever", rx=False,
    definition="Paracetamol is a pain reliever and fever reducer. It treats fever, headache, body ache, toothache and period pain, and is the usual first choice for fever in India, including in dengue, where ibuprofen and aspirin are avoided. At the right dose it is gentle on the stomach, but too much can seriously damage the liver.",
    uses=[("Fever", "Including viral fevers such as flu, COVID-19 and dengue."), ("Headache and migraine", "Mild to moderate headaches."),
          ("Body ache and muscle pain", "Aches that come with fever or after exertion."), ("Toothache", "Short-term relief until dental treatment."),
          ("Period pain", "Cramps and lower back pain during periods."), ("Mild joint pain", "Such as osteoarthritis flares.")],
    how="Paracetamol works mainly in the brain and spinal cord, where it reduces prostaglandins, chemicals that signal pain and raise body temperature. It resets the brain's temperature centre to bring fever down. It has little anti-inflammatory effect, which is why it is gentle on the stomach.",
    dosage=[("Fever or pain (adults over 50 kg)", "1 tablet (650 mg) every 4–6 hours if needed", "Up to 3 days for fever, 5 for pain"), ("Maximum dose", "4 g in 24 hours (6 tablets of 650 mg)", "—"),
            ("Liver disease, low body weight or regular alcohol use", "Lower maximum, often 2–3 g a day", "As advised"), ("Children", "Syrup or lower strengths, dosed by body weight", "As advised")],
    side=["Nausea", "Mild stomach upset", "Skin rash (uncommon)", "Allergic reaction (rare)"],
    serious=["Yellow skin or eyes, dark urine or pain in the upper right abdomen (liver damage)", "Red, blistering or peeling skin (rare serious skin reaction)", "Swelling of the face or throat, or difficulty breathing", "Unusual bruising or bleeding (very rare)"],
    avoid=["You are allergic to paracetamol", "You have severe liver disease", "You already take another medicine containing paracetamol (many cold and flu remedies do)", "You drink alcohol heavily every day, unless your doctor advises"],
    safety=dict(alcohol=("unsafe", "Regular or heavy drinking with paracetamol raises the risk of liver damage. Avoid alcohol while taking it."),
                pregnancy=("prescribed", "The most commonly recommended pain and fever medicine in pregnancy. Use the lowest dose for the shortest time."),
                breastfeeding=("safe", "Safe. Only tiny amounts pass into breast milk."),
                driving=("safe", "Does not affect driving."),
                kidney=("caution", "In severe kidney disease, doses may need to be spaced further apart."),
                liver=("caution", "Use lower doses in liver disease and avoid it in severe disease.")),
    interactions=[("Other paracetamol-containing products", "Major", "Taking two together can cause an overdose."), ("Warfarin", "Moderate", "Regular daily use for more than a few days can raise INR and bleeding risk."),
                  ("Carbamazepine, phenytoin, rifampicin", "Moderate", "Can raise the risk of liver damage."), ("Metoclopramide", "Minor", "Makes paracetamol absorb faster.")],
    storage="Store below 30°C in a dry place.",
    tips=["Leave at least 4 hours between doses.", "Check cold, flu and combination painkillers for paracetamol before taking them together.", "Drink plenty of fluids when you have a fever.", "See a doctor if fever lasts more than 3 days or pain more than 5 days.", "In dengue season, use paracetamol rather than ibuprofen or aspirin for fever, and see a doctor."],
    strengths=["500 mg", "650 mg", "1000 mg", "Syrup 125 mg/5 ml", "Syrup 250 mg/5 ml"], forms=["Tablet", "Syrup", "Drops", "Injection"], refs=["acetaminophen"]),
 "telmisartan": dict(
    name="Telmisartan", alias="", cls="Angiotensin II receptor blocker (ARB)", therapeutic="Cardiovascular", rx=True,
    definition="Telmisartan is a blood pressure medicine from the angiotensin receptor blocker (ARB) group. It relaxes blood vessels so blood flows more easily, which lowers blood pressure and eases the strain on the heart. It is taken once a day and is also used to lower the risk of heart attack and stroke in people at high risk.",
    uses=[("High blood pressure (hypertension)", "Lowers blood pressure for 24 hours with one daily dose."), ("Reducing heart attack and stroke risk", "In adults aged 55 or over at high cardiovascular risk."),
          ("Kidney protection in diabetes", "Doctors may use ARBs to slow kidney damage when there is protein in the urine.")],
    how="Angiotensin II is a hormone that narrows blood vessels and makes the body hold on to salt and water. Telmisartan blocks the receptors this hormone acts on, so the blood vessels relax and widen and blood pressure falls. Its long action means one tablet covers a full day.",
    dosage=[("High blood pressure (usual)", "40 mg once a day", "Long term"), ("If blood pressure stays high", "80 mg once a day, or a combination tablet", "Reviewed every 4 weeks"),
            ("Starting dose in some people", "20 mg once a day", "As advised"), ("Heart risk reduction", "80 mg once a day", "Long term")],
    side=["Dizziness, especially when standing up", "Back pain", "Diarrhoea", "Sinus or throat infection", "Tiredness"],
    serious=["Swelling of the face, lips, tongue or throat (angioedema)", "Fainting or very low blood pressure", "Muscle weakness or irregular heartbeat (high potassium)", "Passing much less urine than usual (kidney problems)"],
    avoid=["You are pregnant or planning a pregnancy", "You have severe liver disease or blocked bile ducts", "You have diabetes or kidney disease and take aliskiren", "You are allergic to telmisartan"],
    safety=dict(alcohol=("caution", "Alcohol can lower blood pressure further and cause dizziness. Limit it."),
                pregnancy=("unsafe", "Can harm the unborn baby. Stop and see your doctor as soon as you know you are pregnant."),
                breastfeeding=("consult", "Not recommended; other medicines are usually preferred."),
                driving=("caution", "Can cause dizziness, especially at the start. Do not drive if affected."),
                kidney=("caution", "Kidney function and potassium should be checked. No dose change is usually needed in mild disease."),
                liver=("caution", "Lower doses in mild to moderate liver disease; avoid in severe disease.")),
    interactions=[("Potassium supplements, spironolactone, potassium salt substitutes", "Major", "Can raise potassium to dangerous levels."), ("Aliskiren, ACE inhibitors (ramipril, enalapril)", "Major", "Higher risk of kidney problems, low blood pressure and high potassium."),
                  ("Lithium", "Major", "Lithium levels can rise to toxic levels."), ("Painkillers such as ibuprofen and diclofenac", "Moderate", "Reduce the effect and can harm the kidneys."), ("Digoxin", "Moderate", "Digoxin levels may rise; your doctor may check them.")],
    storage="Store below 30°C. Keep tablets in the strip until use, as they absorb moisture.",
    tips=["Take it at the same time every day, with or without food.", "Stand up slowly to avoid dizziness.", "Keep taking it even when you feel well; high blood pressure usually has no symptoms.", "Check your blood pressure at home and keep a record.", "Do not use potassium-based salt substitutes without advice."],
    strengths=["20 mg", "40 mg", "80 mg"], forms=["Tablet"], refs=["telmisartan"]),
 "levothyroxine": dict(
    name="Levothyroxine", alias="Thyroxine (T4)", cls="Thyroid hormone replacement", therapeutic="Thyroid", rx=True,
    definition="Levothyroxine is a man-made version of thyroxine (T4), the main hormone made by the thyroid gland. It treats an underactive thyroid (hypothyroidism) by replacing the hormone your body is missing. Most people take it once a day on an empty stomach, usually for life, with the dose set by a TSH blood test.",
    uses=[("Hypothyroidism", "Replaces missing thyroid hormone and relieves tiredness, weight gain, feeling cold and low mood."), ("After thyroid surgery or radioactive iodine", "Replaces the hormone when the thyroid has been removed or treated."),
          ("Goitre and thyroid nodules", "Sometimes used to shrink an enlarged thyroid."), ("Hypothyroidism in pregnancy", "Keeps the mother's levels normal, which matters for the baby's brain development.")],
    how="Levothyroxine is identical to the T4 hormone your thyroid normally releases. The body converts it into the active hormone T3, which controls metabolism: how fast your cells use energy. The right daily dose brings hormone levels back to normal over 4–6 weeks.",
    dosage=[("Usual adult start", "About 1.6 mcg per kg body weight once a day (often 50–100 mcg)", "Long term"), ("Older adults or heart disease", "Start low at 12.5–25 mcg a day and increase slowly", "Every 4–6 weeks"),
            ("Pregnancy", "Dose often increased by 25–30%", "As guided by TSH"), ("Dose checks", "TSH blood test 6–8 weeks after any change", "Then every 6–12 months")],
    side=["Usually none at the right dose", "Palpitations or fast heartbeat (dose too high)", "Feeling hot, sweating, anxiety or poor sleep (dose too high)", "Temporary hair thinning in the first months", "Tiredness and weight gain (dose too low)"],
    serious=["Chest pain or an irregular, very fast heartbeat", "Severe headache, shaking or fits", "Swelling of the face or throat (allergy, very rare)"],
    avoid=["You have an untreated overactive thyroid (thyrotoxicosis)", "You have untreated adrenal insufficiency", "You have had a recent heart attack, unless your doctor is managing it", "You want to use it for weight loss: this is dangerous"],
    safety=dict(alcohol=("safe", "No known interaction. Moderate drinking does not affect it."),
                pregnancy=("prescribed", "Safe and essential if you have hypothyroidism. The dose usually needs to go up, so check TSH early."),
                breastfeeding=("safe", "Safe. Only normal hormone levels pass into milk."),
                driving=("safe", "Does not affect driving."),
                kidney=("safe", "No dose change is usually needed."),
                liver=("safe", "No dose change is usually needed.")),
    interactions=[("Calcium, iron, antacids, multivitamins", "Major", "Block absorption. Take them at least 4 hours apart."), ("Pantoprazole, omeprazole and other PPIs", "Moderate", "Can reduce absorption over time; TSH may need checking."),
                  ("Warfarin", "Moderate", "Can increase warfarin's effect; INR needs monitoring when the dose changes."), ("Diabetes medicines and insulin", "Moderate", "Blood sugar may rise as thyroid levels improve."),
                  ("Soy, high-fibre food, coffee", "Minor", "Reduce absorption if taken at the same time.")],
    storage="Store below 25°C in the original bottle, tightly closed, away from light and moisture.",
    tips=["Take it on an empty stomach, 30–60 minutes before breakfast, with water only.", "Keep calcium, iron and antacids at least 4 hours away.", "Stay on one brand, and recheck TSH 6–8 weeks after any brand or dose change.", "Do not stop it when you feel better; most people need it for life.", "Tell your doctor straight away if you become pregnant."],
    strengths=["12.5 mcg", "25 mcg", "50 mcg", "75 mcg", "88 mcg", "100 mcg", "125 mcg", "150 mcg"], forms=["Tablet"], refs=["levothyroxine"]),
})

MORE.update({
 "paracetamol": dict(
  intro="Paracetamol is one of the most widely used medicines in the world. The 650 mg strength is widely used by adults in India for fever and body ache.",
  benefits=[("Brings fever down", "Lowers temperature within 30–60 minutes and makes you feel more comfortable."), ("Relieves everyday pain", "Eases headache, body ache, toothache and period pain."),
            ("Gentle on the stomach", "Unlike ibuprofen or aspirin, it does not usually irritate the stomach, and it is preferred in dengue fever.")],
  how_to_use="Take one tablet with a glass of water, with or without food. Leave at least 4–6 hours between doses. Do not take more than 4 g in 24 hours, counting every product that contains paracetamol.",
  manage=[("Nausea", "Take it after a light snack."), ("Rash", "Stop taking it and speak to a doctor."), ("Fever not settling", "Sponge with lukewarm water, drink fluids and see a doctor if it lasts more than 3 days.")],
  food=["Can be taken with or without food.", "Avoid alcohol while taking it.", "Drink plenty of water, especially when you have a fever."],
  disease=[("Liver disease", "Lower doses are needed; avoid in severe liver disease."), ("Regular heavy drinking", "Higher risk of liver damage even at normal doses."), ("G6PD deficiency", "Rarely, can break down red blood cells. Use as advised.")],
  warnings=["Never take more than the maximum daily dose. Liver damage from an overdose may not cause symptoms for 1–2 days.", "Many cold, flu and combination painkillers also contain paracetamol.", "Fever lasting more than 3 days needs a doctor, especially in dengue or malaria season.", "Keep out of reach of children; accidental overdose is dangerous."],
  lifestyle=["Rest and drink plenty of fluids during a fever.", "Wear light clothing; avoid heavy wrapping during fever.", "For repeated headaches, look at sleep, screen time and water intake.", "Avoid painkillers on more than 10–15 days a month without advice, as this can cause rebound headaches."],
  labs=["Complete blood count (CBC)", "Dengue NS1 antigen", "Malaria test", "Typhoid test", "Liver function test (LFT)"],
  fact=[("Chemical class", "Para-aminophenol derivative"), ("Action class", "Analgesic and antipyretic"), ("Therapeutic class", "Pain & fever"), ("Habit forming", "No"), ("Schedule", "Over the counter (check the pack label)")],
  missed="Paracetamol is usually taken only when needed. If you are on a regular schedule, take the dose when you remember, keeping at least 4 hours from the last one.",
  overdose="A paracetamol overdose is a medical emergency even if you feel well. Go to a hospital at once; the antidote works best within 8 hours.",
  salt_faq=[("Is paracetamol safe to take every day?", "At normal doses for short periods, yes. Daily use for weeks should be discussed with a doctor."),
            ("How long does paracetamol take to work?", "Usually 30–60 minutes. The effect lasts 4–6 hours."),
            ("Can I take paracetamol on an empty stomach?", "Yes. It is gentle on the stomach and can be taken with or without food."),
            ("Is paracetamol the same as acetaminophen?", "Yes. Acetaminophen is the name used in the USA for the same medicine."),
            ("Can I take paracetamol for dengue fever?", "Yes, it is preferred for fever in dengue. Avoid ibuprofen, aspirin and diclofenac, which raise bleeding risk."),
            ("What is the difference between paracetamol 500 mg and 650 mg?", "A 650 mg tablet has 30% more paracetamol. Both are used in adults; follow the dose your doctor or the pack advises."),
            ("Can I take paracetamol with ibuprofen?", "Doctors sometimes advise alternating them for a short time for high fever or pain. Ask your doctor or pharmacist first."),
            ("How many paracetamol 650 mg tablets can I take in a day?", "Most adults should take no more than 4 g a day, which is 6 tablets of 650 mg, at least 4 hours apart. Your doctor may advise less.")]),
 "telmisartan": dict(
  intro="Telmisartan is widely used because one daily tablet controls blood pressure for 24 hours and it rarely causes the dry cough seen with ACE inhibitors.",
  benefits=[("Controls blood pressure all day", "One tablet covers a full 24 hours, including the early morning, when heart attacks are most common."),
            ("Protects the heart, brain and kidneys", "Keeping blood pressure in range lowers the risk of heart attack, stroke and kidney damage."),
            ("Well tolerated", "Unlike ACE inhibitors such as ramipril, it rarely causes a dry cough.")],
  how_to_use="Take one tablet once a day, at the same time each day. Swallow it whole with water, with or without food. Keep the tablet in its strip until you take it.",
  manage=[("Dizziness", "Stand up slowly, sit or lie down if dizzy, and drink enough water."), ("Back or muscle pain", "Usually mild. Tell your doctor if it persists or comes with weakness."),
          ("Diarrhoea", "Drink fluids. Tell your doctor if it is severe, as dehydration can drop blood pressure further.")],
  food=["Can be taken with or without food.", "Keep salt under 5 g a day (about one teaspoon).", "Avoid potassium-based salt substitutes unless your doctor approves.", "Limit alcohol."],
  disease=[("Kidney disease", "Kidney function and potassium need regular checks."), ("Liver disease", "Lower doses; avoid with blocked bile ducts or severe liver disease."),
           ("Narrowed kidney arteries (renal artery stenosis)", "Can cause a sudden drop in kidney function.")],
  warnings=["Do not take it during pregnancy; tell your doctor if you plan to conceive.", "Vomiting, diarrhoea or heavy sweating can cause low blood pressure; ask your doctor whether to pause it.", "Kidney function and potassium may be checked 1–2 weeks after starting or changing the dose.", "Tell the surgeon or anaesthetist you take it before any operation."],
  lifestyle=["Cut down on salt, pickles, papad and packaged snacks.", "Aim for 150 minutes of brisk walking a week.", "Keep a healthy weight and waist size.", "Stop smoking and limit alcohol.", "Check your blood pressure at home and share the log with your doctor."],
  labs=["Blood pressure monitoring", "Kidney function test (creatinine, eGFR)", "Serum potassium", "Lipid profile", "HbA1c", "ECG"],
  fact=[("Chemical class", "Benzimidazole derivative"), ("Action class", "Angiotensin II receptor blocker (ARB)"), ("Therapeutic class", "Cardiovascular (anti-hypertensive)"), ("Habit forming", "No"), ("Schedule", "Schedule H (prescription only)")],
  missed="Take it as soon as you remember the same day. If it is nearly time for the next dose, skip the missed one. Do not take two doses together.",
  overdose="An overdose can cause very low blood pressure, dizziness and a fast or slow heartbeat. Lie down with your legs raised and get medical help.",
  salt_faq=[("What is the best time to take telmisartan?", "Any time of day, as long as it is the same time daily. Many people take it in the morning."),
            ("Can I stop telmisartan once my blood pressure is normal?", "No. Normal readings usually mean the medicine is working. Stopping can make blood pressure rise again."),
            ("Does telmisartan cause cough?", "Rarely. Dry cough is much more common with ACE inhibitors such as ramipril."),
            ("Is telmisartan safe for the kidneys?", "It can protect the kidneys in diabetes and high blood pressure, but kidney function and potassium should be checked regularly."),
            ("How long does telmisartan take to work?", "Blood pressure starts falling within hours, but the full effect takes about 4 weeks."),
            ("What is the difference between telmisartan 40 mg and 80 mg?", "80 mg is twice the dose and lowers blood pressure a little more. Your doctor chooses the strength from your readings."),
            ("Can I take telmisartan with amlodipine?", "Yes. They are often combined, and combination tablets are available."),
            ("Is telmisartan safe in pregnancy?", "No. It can harm the unborn baby. Speak to your doctor before planning a pregnancy.")]),
 "levothyroxine": dict(
  intro="Hypothyroidism is common in India, especially in women. Because the right dose is very precise, levothyroxine comes in many small strength steps.",
  benefits=[("Restores energy and metabolism", "Relieves tiredness, feeling cold, constipation, dry skin and slow thinking caused by low thyroid hormone."),
            ("Helps the heart and cholesterol", "Treating hypothyroidism helps bring cholesterol back to normal and lowers long-term heart risk."),
            ("Supports a healthy pregnancy", "Normal thyroid levels support the baby's brain development and lower the risk of miscarriage.")],
  how_to_use="Take the tablet in the morning on an empty stomach with a glass of water. Wait 30–60 minutes before breakfast, tea or coffee. Take it at the same time every day. Keep calcium, iron and antacids at least 4 hours apart.",
  manage=[("Palpitations or feeling jittery", "Your dose may be too high. Tell your doctor; a TSH test can check."), ("Trouble sleeping", "Take it early in the morning and limit caffeine. Report it if it continues."),
          ("Hair thinning", "Usually temporary in the first few months and settles as levels stabilise.")],
  food=["Take it on an empty stomach, 30–60 minutes before food.", "Keep milk, curd and calcium-rich food away from the dose.", "Tea and coffee reduce absorption; wait at least 30 minutes.", "Use iodised salt as normal; avoid iodine or kelp supplements unless advised."],
  disease=[("Heart disease", "Start with a low dose and increase slowly, as too much can strain the heart."), ("Diabetes", "Sugar control may change as thyroid levels improve; monitor your sugar."), ("Adrenal insufficiency", "Must be treated before starting levothyroxine.")],
  warnings=["Levothyroxine has a narrow dosing range: small changes in dose or brand can change your TSH.", "Never use it for weight loss; high doses can cause serious heart problems.", "Tell your doctor if you become pregnant, as the dose usually needs to rise.", "Older adults are more sensitive to over-treatment, which can affect the heart and bones."],
  lifestyle=["Set a daily alarm so you take it at the same time every morning.", "Eat a balanced diet; cabbage and cauliflower in normal amounts are fine.", "Exercise regularly to help energy and weight.", "Keep a record of your TSH results and doses."],
  labs=["TSH (thyroid stimulating hormone)", "Free T4", "Free T3", "Anti-TPO antibodies", "Lipid profile", "Complete blood count (CBC)"],
  fact=[("Chemical class", "Synthetic thyroid hormone (T4)"), ("Action class", "Thyroid hormone replacement"), ("Therapeutic class", "Thyroid"), ("Habit forming", "No"), ("Schedule", "Schedule H (prescription only)")],
  missed="Take it as soon as you remember the same day. If it is nearly time for the next dose, skip the missed one. Do not double up; missing an occasional dose is not dangerous.",
  overdose="Too much can cause a fast heartbeat, chest pain, shaking, sweating and anxiety. Seek medical help, especially if you have heart disease.",
  switch_note="Levothyroxine has a narrow therapeutic range, so same-strength brands can give slightly different blood levels. A Tablow doctor calls you to guide the switch. Then stay on the new brand and recheck TSH after 6–8 weeks.",
  salt_faq=[("Why must levothyroxine be taken on an empty stomach?", "Food, tea, coffee, milk and many supplements reduce how much is absorbed. An empty stomach gives steady, predictable levels."),
            ("Can I take levothyroxine at night?", "Some doctors allow a bedtime dose, at least 3–4 hours after the last meal. Choose one time and stick to it."),
            ("How long does levothyroxine take to work?", "Many people feel better in 2–3 weeks, but TSH takes 6–8 weeks to settle, which is why tests are done then."),
            ("Will I need levothyroxine for life?", "Most people with hypothyroidism do. Some temporary causes, such as thyroiditis after pregnancy, need it only for a while."),
            ("Does levothyroxine cause weight gain?", "Not at the right dose. Untreated hypothyroidism can cause weight gain. Levothyroxine is not a weight-loss medicine."),
            ("Can I switch levothyroxine brands?", "Yes. A Tablow doctor calls you to guide the switch. Recheck TSH 6–8 weeks after switching, then stay with the same brand."),
            ("Is levothyroxine safe in pregnancy?", "Yes, and it is important. The dose often needs to go up, so tell your doctor as soon as you are pregnant."),
            ("What is the difference between 25, 50 and 100 mcg?", "They are dose steps. Your doctor picks the strength from your weight, age and TSH, and may combine tablets for in-between doses.")]),
})

# ---------------- pairs ----------------
for p, var in zip(PAIRS, ["625 mg", "40 mg", "1 mg + 500 mg", "200/6 mcg", "100 IU/ml 30/70"]):
    p.setdefault("family", p["id"]); p.setdefault("variant", var); p.setdefault("default", True)
PAIRS[4]["variant"] = "40 IU/ml"

def _pair(base, **kw):
    d = {k: v for k, v in base.items() if k not in ("brand_faq", "sub_faq", "brand", "sub")}
    d["default"] = False; d.update(kw); return d

B = {p["id"]: p for p in PAIRS}
NEW = [
 _pair(B["pan"], id="pan20", variant="20 mg", strength="Pantoprazole 20 mg",
       brand=dict(slug="pan-20-tablet", name="Pan 20 Tablet", short="Pan 20", company="alkem", mrp=145.00, price_src="Placeholder"),
       sub=dict(slug="pantop-20-tablet", name="Pantop 20 Tablet", short="Pantop 20", company="aristo", mrp=99.00, price_src="Placeholder")),
 _pair(B["glycomet"], id="glycomet2", variant="2 mg + 500 mg", strength="Glimepiride 2 mg + Metformin 500 mg",
       brand=dict(slug="glycomet-gp-2-tablet", name="Glycomet GP 2 Tablet SR", short="Glycomet GP 2", company="usv", mrp=182.00, price_src="Placeholder"),
       sub=dict(slug="glimisave-m2-tablet", name="Glimisave M2 Tablet SR", short="Glimisave M2", company="eris", mrp=141.00, price_src="Placeholder")),
 _pair(B["foracort"], id="foracort400", variant="400/6 mcg", strength="Budesonide 400 mcg + Formoterol 6 mcg per puff",
       brand=dict(slug="foracort-400-inhaler", name="Foracort 400 Inhaler", short="Foracort 400", company="cipla", mrp=790.00, price_src="Placeholder"),
       sub=dict(slug="budamate-400-inhaler", name="Budamate 400 Inhaler", short="Budamate 400", company="lupin", mrp=640.00, price_src="Placeholder")),
 dict(id="dolo", family="dolo", variant="650 mg", default=True,
      brand=dict(slug="dolo-650-tablet", name="Dolo 650 Tablet", short="Dolo 650", company="micro", mrp=33.60, price_src="Placeholder"),
      sub=dict(slug="pacimol-650-tablet", name="Pacimol 650 Tablet", short="Pacimol 650", company="ipca", mrp=24.00, price_src="Placeholder"),
      salt="paracetamol", strength="Paracetamol 650 mg", form="Tablet", release="Immediate release",
      pack="Strip of 15 tablets", unit="tablet", units=15, icon="strip", category="Pain & fever", rank=None,
      usage=dict(kind="course", qty=1, label="strips per course", note="A 3-day fever course at 3 tablets a day uses about 1 strip.")),
 dict(id="telma", family="telma", variant="40 mg", default=True,
      brand=dict(slug="telma-40-tablet", name="Telma 40 Tablet", short="Telma 40", company="glenmark", mrp=240.00, price_src="Placeholder"),
      sub=dict(slug="telmikind-40-tablet", name="Telmikind 40 Tablet", short="Telmikind 40", company="mankind", mrp=99.00, price_src="Placeholder"),
      salt="telmisartan", strength="Telmisartan 40 mg", form="Tablet", release="Immediate release",
      pack="Strip of 15 tablets", unit="tablet", units=15, icon="strip", category="Heart care", rank=None,
      usage=dict(kind="month", qty=2, label="strips per month", note="One tablet a day uses 2 strips a month.")),
]
NEW.append(_pair(NEW[-1], id="telma80", variant="80 mg", strength="Telmisartan 80 mg",
       brand=dict(slug="telma-80-tablet", name="Telma 80 Tablet", short="Telma 80", company="glenmark", mrp=342.00, price_src="Placeholder"),
       sub=dict(slug="telmikind-80-tablet", name="Telmikind 80 Tablet", short="Telmikind 80", company="mankind", mrp=147.00, price_src="Placeholder")))
THY = dict(family="thyronorm", salt="levothyroxine", form="Tablet", release="Immediate release", pack="Bottle of 120 tablets", unit="tablet", units=120,
           icon="bottle", category="Thyroid", rank=None, usage=dict(kind="year", qty=3, label="bottles a year", note="One tablet a day is 365 tablets, a little over 3 bottles of 120 a year."))
for mcg, bm, sm, dflt in ((25, 160.00, 128.00, False), (50, 198.00, 156.00, True), (100, 236.00, 189.00, False)):
    NEW.append(dict(THY, id=f"thyronorm{mcg}", variant=f"{mcg} mcg", default=dflt, strength=f"Levothyroxine {mcg} mcg",
        brand=dict(slug=f"thyronorm-{mcg}-mcg-tablet", name=f"Thyronorm {mcg} mcg Tablet", short=f"Thyronorm {mcg}", company="abbott", mrp=bm, price_src="Placeholder"),
        sub=dict(slug=f"thyrox-{mcg}-tablet", name=f"Thyrox {mcg} Tablet", short=f"Thyrox {mcg}", company="macleods", mrp=sm, price_src="Placeholder")))

# order: each family together, lowest strength first
_all = PAIRS + NEW
_order = ["augmentin", "pan20", "pan", "glycomet", "glycomet2", "foracort", "foracort400", "mixtard", "dolo", "telma", "telma80", "thyronorm25", "thyronorm50", "thyronorm100"]
PAIRS[:] = [next(p for p in _all if p["id"] == i) for i in _order]

# ---------------- generated FAQs for the new pairs ----------------
def _lc(t): return t if t[:2].isupper() or t[1:2] == "." else t[0].lower() + t[1:]
def _and(xs): return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
def _r(x): return f"₹{x:,.2f}"
def _sent(t, n=2): return " ".join(x.strip() + ("" if x.strip().endswith(".") else ".") for x in t.split(". ")[:n])

def auto_faqs(p):
    b, s = p["brand"], p["sub"]; S = SALTS[p["salt"]]; M = MORE[p["salt"]]
    sc = COMPANIES[s["company"]]; u = p["unit"]
    bu, su = b["mrp"] / p["units"], s["mrp"] / p["units"]; pct = round((b["mrp"] - s["mrp"]) / b["mrp"] * 100)
    F = [x for x in PAIRS if x["family"] == p["family"]]
    note = M.get("switch_note")
    uses = "; ".join(_lc(t) for t, _ in S["uses"][:4])
    rx = (f"Yes. {S['name']} is a prescription medicine. Upload your prescription; a prescription for {b['short']} can be dispensed with a same-salt substitute where the law and your doctor allow."
          if S["rx"] else f"Standard packs of {S['name'].lower()} tablets are sold without a prescription in India. See a doctor if you need it for more than 3 days.")
    bf = [(f"What is the cheaper substitute for {b['short']}?", f"{s['short']} by {sc['short']} contains the same {p['strength']} in the same {p['form'].lower()} form, at {_r(su)} per {u} instead of {_r(bu)}: {pct}% less. Tablow recommends it as the same-salt alternative."),
          (f"Is {s['short']} the same as {b['short']}?", f"Both contain {p['strength']} with the same dosage form and release type, and must meet the same Indian quality standards. Manufacturer, inactive ingredients and price differ. " + (note if note else "After you order, a Tablow doctor calls you to confirm the switch and issue your prescription.")),
          (f"What is {b['short']} used for?", f"It contains {S['name'].lower()} and is used for {uses}."),
          (f"How should I take {b['short']}?", _sent(M["how_to_use"])),
          (f"What is the price of {b['short']}?", f"{b['name']} costs {_r(b['mrp'])} for a {p['pack'].lower()} (MRP), about {_r(bu)} per {u}.")]
    if len(F) > 1:
        fam = b["short"].split()[0]
        o = next(x for x in F if x is not p)
        bf += [(f"Which strengths of {fam} are available?", f"On Tablow you can compare " + _and([f"{x['brand']['short']} ({x['variant']})" for x in F]) + ". Your doctor chooses the strength; do not change it on your own."),
               (f"What is the difference between {b['short']} and {o['brand']['short']}?", f"{b['short']} contains {p['strength']}, and {o['brand']['short']} contains {o['strength']}. They are the same medicine at different doses. Take only the strength your doctor prescribed.")]
    else:
        bf += [(f"Does {b['short']} need a prescription?", rx), (f"Is {b['short']} habit forming?", "No. It is not habit forming.")]
    bf.append((f"Why can't I buy {b['short']} on Tablow?", f"Tablow recommends a branded substitute with the same salt and strength so you pay less. Contact us on WhatsApp if your doctor has said not to substitute."))
    k, q = p["usage"]["kind"], p["usage"]["qty"]
    if k == "course":
        save = (f"How much do I save per course with {s['short']}?", f"{p['usage']['note']} That costs {_r((b['mrp'] - s['mrp']) * q)} less with {s['short']} than with {b['short']}.")
    else:
        yr = (b["mrp"] - s["mrp"]) * q * (1 if k == "year" else 12)
        save = ("How much can I save a year by switching?", f"At {q} {p['usage']['label']}, switching from {b['short']} saves about ₹{yr:,.0f} a year at current prices. Use the calculator on this page for your own dose.")
    sf = [(f"Is {s['short']} a good substitute for {b['short']}?", f"Yes. Both contain {p['strength']} in the same {p['form'].lower()} form. {s['short']} is made by {sc['name']}. " + (note if note else "After you order, a Tablow doctor calls you to confirm the switch and issue your prescription.")),
          (f"What is {s['short']} used for?", f"It is used for {uses}."),
          (f"Who makes {s['short']}?", f"{s['short']} is made by {sc['name']}. " + sc["about"].split(". ")[0] + "."),
          (f"How should I take {s['short']}?", _sent(M["how_to_use"])),
          (f"Do I need a prescription for {s['short']}?", rx), save]
    return bf, sf

for p in PAIRS:
    if "brand_faq" not in p:
        p["brand_faq"], p["sub_faq"] = auto_faqs(p)
