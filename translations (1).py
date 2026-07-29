"""
src/utils/translations.py
İngilizce DDXPlus çıktılarını Türkçe'ye çeviren sözlükler ve yardımcı fonksiyonlar.

Kullanım:
    from src.utils.translations import translate_pathology, translate_symptom

Sözlükte olmayan kelimeler hata vermez; orijinal İngilizce metin geri döner.
"""

# ── 49 DDXPlus Hastalığı: İngilizce → Türkçe ─────────────────────────────────
PATHOLOGY_TR: dict[str, str] = {
    "Acute COPD exacerbation / infection":      "Akut KOAH Alevlenmesi / Enfeksiyonu",
    "Acute dystonic reactions":                 "Akut Distonik Reaksiyonlar",
    "Acute laryngitis":                         "Akut Larenjiit",
    "Acute otitis media":                       "Akut Orta Kulak İltihabı",
    "Acute pulmonary edema":                    "Akut Akciğer Ödemi",
    "Acute rhinosinusitis":                     "Akut Rinosinüzit",
    "Allergic sinusitis":                       "Alerjik Sinüzit",
    "Anaphylaxis":                              "Anafilaksi",
    "Anemia":                                   "Anemi (Kansızlık)",
    "Atrial fibrillation":                      "Atriyal Fibrilasyon",
    "Boerhaave":                                "Boerhaave Sendromu (Özofagus Rüptürü)",
    "Bronchiectasis":                           "Bronşiektazi",
    "Bronchiolitis":                            "Bronşiolit",
    "Bronchitis":                               "Bronşit",
    "Bronchospasm / acute asthma exacerbation": "Bronkospazm / Akut Astım Atağı",
    "Chagas":                                   "Chagas Hastalığı",
    "Chronic rhinosinusitis":                   "Kronik Rinosinüzit",
    "Cluster headache":                         "Küme Baş Ağrısı",
    "Croup":                                    "Krup (Yalancı Kuşpalazı)",
    "Ebola":                                    "Ebola Virüsü Hastalığı",
    "Epiglottitis":                             "Epiglotit",
    "GERD":                                     "Gastroözofageal Reflü Hastalığı (GÖRH)",
    "Guillain-Barré syndrome":                  "Guillain-Barré Sendromu",
    "HIV (initial infection)":                  "HIV (Başlangıç Enfeksiyonu)",
    "Influenza":                                "İnfluenza (Grip)",
    "Inguinal hernia":                          "Kasık Fıtığı",
    "Larygospasm":                              "Larenks Spazmı",
    "Localized edema":                          "Lokalize Ödem",
    "Myasthenia gravis":                        "Miyastenia Gravis",
    "Myocarditis":                              "Miyokardit",
    "PSVT":                                     "PSVT (Paroksismal Supraventriküler Taşikardi)",
    "Pancreatic neoplasm":                      "Pankreas Tümörü",
    "Panic attack":                             "Panik Atak",
    "Pericarditis":                             "Perikardit",
    "Pneumonia":                                "Pnömoni (Zatürre)",
    "Possible NSTEMI / STEMI":                  "Olası Kalp Krizi (NSTEMI / STEMI)",
    "Pulmonary embolism":                       "Pulmoner Emboli (Akciğer Pıhtısı)",
    "Pulmonary neoplasm":                       "Akciğer Tümörü",
    "SLE":                                      "Sistemik Lupus Eritematozus (SLE)",
    "Sarcoidosis":                              "Sarkoidoz",
    "Scombroid food poisoning":                 "Scombroid Gıda Zehirlenmesi",
    "Spontaneous pneumothorax":                 "Spontan Pnömotoraks (Akciğer Çökmesi)",
    "Spontaneous rib fracture":                 "Spontan Kaburga Kırığı",
    "Stable angina":                            "Stabil Anjina (Kararlı Göğüs Ağrısı)",
    "Tuberculosis":                             "Tüberküloz (Verem)",
    "URTI":                                     "Üst Solunum Yolu Enfeksiyonu",
    "Unstable angina":                          "Unstabil Anjina (Kararsız Göğüs Ağrısı)",
    "Viral pharyngitis":                        "Viral Farenjit (Boğaz İltihabı)",
    "Whooping cough":                           "Boğmaca",
}

# ── Semptom Terimleri: İngilizce → Türkçe (LLM çıktısında geçen kalıplar) ────
# LLM, extract_symptoms fonksiyonuyla her semptomu İngilizce atomik cümle
# üretir (örn. "Fever is present.", "Chest pain is absent.").
# Bu sözlük, o cümlelerdeki tıbbi terimleri anahtar kelime bazında değiştirir.
SYMPTOM_TERMS_TR: dict[str, str] = {
    # Kalıp ifadeler (önce bunlar işlenir)
    " is present":       " mevcut",
    " is absent":        " yok",
    " are present":      " mevcut",
    " are absent":       " yok",
    "Patient has ":      "Hastada ",
    "Patient reports ":  "Hasta bildiriyor: ",
    "Symptoms followed": "Semptomlar şu durumun ardından gelişti:",

    # Ağrı ve his
    "Chest pain":           "Göğüs ağrısı",
    "chest pain":           "göğüs ağrısı",
    "Abdominal pain":       "Karın ağrısı",
    "abdominal pain":       "karın ağrısı",
    "Back pain":            "Sırt ağrısı",
    "back pain":            "sırt ağrısı",
    "Headache":             "Baş ağrısı",
    "headache":             "baş ağrısı",
    "Neck pain":            "Boyun ağrısı",
    "neck pain":            "boyun ağrısı",
    "Knee pain":            "Diz ağrısı",
    "knee pain":            "diz ağrısı",
    "Joint pain":           "Eklem ağrısı",
    "joint pain":           "eklem ağrısı",
    "Muscle pain":          "Kas ağrısı",
    "muscle pain":          "kas ağrısı",
    "Throat pain":          "Boğaz ağrısı",
    "throat pain":          "boğaz ağrısı",
    "Shoulder pain":        "Omuz ağrısı",
    "shoulder pain":        "omuz ağrısı",
    "Flank pain":           "Yan ağrısı",
    "flank pain":           "yan ağrısı",
    "Pelvic pain":          "Pelvik ağrı",
    "pelvic pain":          "pelvik ağrı",
    "Burning pain":         "Yanıcı ağrı",
    "burning pain":         "yanıcı ağrı",
    "Sharp pain":           "Keskin ağrı",
    "sharp pain":           "keskin ağrı",
    "Dull pain":            "Künt ağrı",
    "dull pain":            "künt ağrı",
    "Radiating pain":       "Yayılan ağrı",
    "radiating pain":       "yayılan ağrı",

    # Solunum
    "Shortness of breath":  "Nefes darlığı",
    "shortness of breath":  "nefes darlığı",
    "Dyspnea":              "Dispne (nefes darlığı)",
    "dyspnea":              "dispne",
    "Cough":                "Öksürük",
    "cough":                "öksürük",
    "Dry cough":            "Kuru öksürük",
    "dry cough":            "kuru öksürük",
    "Productive cough":     "Balgamlı öksürük",
    "productive cough":     "balgamlı öksürük",
    "Wheezing":             "Hırıltılı nefes",
    "wheezing":             "hırıltılı nefes",
    "Stridor":              "Stridor (solunumda ıslık sesi)",
    "stridor":              "stridor",
    "Hemoptysis":           "Hemoptizi (kan öksürme)",
    "hemoptysis":           "hemoptizi",

    # Ateş ve enfeksiyon
    "Fever":                "Ateş",
    "fever":                "ateş",
    "Chills":               "Titreme / üşüme",
    "chills":               "titreme / üşüme",
    "Sweating":             "Terleme",
    "sweating":             "terleme",
    "Night sweats":         "Gece terlemesi",
    "night sweats":         "gece terlemesi",

    # Sindirim
    "Nausea":               "Bulantı",
    "nausea":               "bulantı",
    "Vomiting":             "Kusma",
    "vomiting":             "kusma",
    "Diarrhea":             "İshal",
    "diarrhea":             "ishal",
    "Constipation":         "Kabızlık",
    "constipation":         "kabızlık",
    "Heartburn":            "Mide yanması",
    "heartburn":            "mide yanması",
    "Regurgitation":        "Regürjitasyon (mide içeriğinin geri gelmesi)",
    "regurgitation":        "regürjitasyon",
    "Bloating":             "Şişkinlik",
    "bloating":             "şişkinlik",
    "Loss of appetite":     "İştah kaybı",
    "loss of appetite":     "iştah kaybı",
    "Dysphagia":            "Yutma güçlüğü",
    "dysphagia":            "yutma güçlüğü",

    # Nörolojik
    "Dizziness":            "Baş dönmesi",
    "dizziness":            "baş dönmesi",
    "Syncope":              "Senkop (bayılma)",
    "syncope":              "senkop",
    "Weakness":             "Halsizlik / güçsüzlük",
    "weakness":             "halsizlik",
    "Numbness":             "Uyuşma",
    "numbness":             "uyuşma",
    "Tingling":             "Karıncalanma",
    "tingling":             "karıncalanma",
    "Confusion":            "Konfüzyon (zihin bulanıklığı)",
    "confusion":            "konfüzyon",
    "Seizure":              "Nöbet",
    "seizure":              "nöbet",
    "Vision changes":       "Görme değişiklikleri",
    "vision changes":       "görme değişiklikleri",

    # Kardiyovasküler
    "Palpitations":         "Çarpıntı",
    "palpitations":         "çarpıntı",
    "Tachycardia":          "Taşikardi (hızlı kalp atışı)",
    "tachycardia":          "taşikardi",
    "Edema":                "Ödem",
    "edema":                "ödem",
    "Swelling":             "Şişlik",
    "swelling":             "şişlik",

    # Diğer
    "Fatigue":              "Yorgunluk / bitkinlik",
    "fatigue":              "yorgunluk",
    "Rash":                 "Döküntü",
    "rash":                 "döküntü",
    "Itching":              "Kaşıntı",
    "itching":              "kaşıntı",
    "Hoarseness":           "Ses kısıklığı",
    "hoarseness":           "ses kısıklığı",
    "Runny nose":           "Burun akıntısı",
    "runny nose":           "burun akıntısı",
    "Nasal congestion":     "Burun tıkanıklığı",
    "nasal congestion":     "burun tıkanıklığı",
    "Sore throat":          "Boğaz ağrısı",
    "sore throat":          "boğaz ağrısı",
    "Ear pain":             "Kulak ağrısı",
    "ear pain":             "kulak ağrısı",
    "Ear discharge":        "Kulak akıntısı",
    "ear discharge":        "kulak akıntısı",
    "Weight loss":          "Kilo kaybı",
    "weight loss":          "kilo kaybı",
    "Urinary symptoms":     "İdrar yolu semptomları",
    "urinary symptoms":     "idrar yolu semptomları",
    "Hematuria":            "Hematüri (idrarda kan)",
    "hematuria":            "hematüri",
    "a fall":               "düşme",
    "a fall.":              "düşme.",

    # Yön ve konum
    "Right ":               "Sağ ",
    "right ":               "sağ ",
    "Left ":                "Sol ",
    "left ":                "sol ",
    "Upper ":               "Üst ",
    "upper ":               "üst ",
    "Lower ":               "Alt ",
    "lower ":               "alt ",
    "Bilateral ":           "İki taraflı ",
    "bilateral ":           "iki taraflı ",

    # Vücut bölgeleri (bağımsız kelime olarak geçenler)
    " knee":                " diz",
    " ankle":               " ayak bileği",
    " wrist":               " bilek",
    " elbow":               " dirsek",
    " hip":                 " kalça",
    " arm":                 " kol",
    " leg":                 " bacak",
    " foot":                " ayak",
    " hand":                " el",
    " finger":              " parmak",
    " toe":                 " ayak parmağı",
    " eye":                 " göz",
    " ear":                 " kulak",
    " nose":                " burun",
    " throat":              " boğaz",
    " neck":                " boyun",
    " chest":               " göğüs",
    " abdomen":             " karın",
    " groin":               " kasık",
    " side":                " yan",
    " back":                " sırt",

    # Süre / şiddet niteleyicileri
    "has been present for":         "süredir mevcut:",
    "has been present since":       "tarihinden beri mevcut:",
    "aggravated by":                "şu durumla kötüleşiyor:",
    "relieved by":                  "şu durumla hafifliyor:",
    "at rest":                      "istirahatte",
    "on exertion":                  "eforla",
    "exertion":                     "efor",
    "progressively":                "giderek artan şekilde",
    "suddenly":                     "aniden",
    "gradually":                    "yavaş yavaş",
    "intermittently":               "aralıklı olarak",
    "constantly":                   "sürekli olarak",
    "Severe ":                      "Şiddetli ",
    "mild ":                        "hafif ",
    "Mild ":                        "Hafif ",
    "moderate ":                    "orta şiddette ",
    "Moderate ":                    "Orta şiddette ",
    "severe ":                      "şiddetli ",
    "acute ":                       "akut ",
    "Acute ":                       "Akut ",
    "chronic ":                     "kronik ",
    "Chronic ":                     "Kronik ",

    # "pain" tek başına (diğer "X pain" kalıpları yukarıda uzun eşleşmeyle yakalanır)
    " pain":                        " ağrısı",
}


def translate_pathology(name: str) -> str:
    """
    DDXPlus hastalık adını Türkçe'ye çevirir.
    Sözlükte yoksa orijinal İngilizce adı döndürür.
    """
    return PATHOLOGY_TR.get(name, name)


def translate_symptom(statement: str) -> str:
    """
    LLM'in ürettiği İngilizce atomik semptom cümlesini Türkçe'ye çevirir.
    Bilinen terimleri sözlük üzerinden değiştirir; tanınmayan kısımlar
    orijinal haliyle kalır (hata vermez).

    Not: Daha uzun/özgün ifadeler (örn. "Dry cough") daha kısa olanlardan
    (örn. "cough") önce işlenir; böylece kısmi eşleşmeler çakışmaz.
    """
    result = statement
    # Anahtar uzunluğuna göre azalan sırayla işle (özgün önce)
    for en in sorted(SYMPTOM_TERMS_TR, key=len, reverse=True):
        result = result.replace(en, SYMPTOM_TERMS_TR[en])
    # Baş harfini büyüt
    if result and result[0].islower():
        result = result[0].upper() + result[1:]
    return result
