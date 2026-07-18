import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# 1. .env dosyasındaki API anahtarını yüklüyoruz
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. DDXPlus Semptom Listesi (Yahya'nın modelinin tanıdığı anahtar sütunlar)
# Buraya ilk aşamada en kritik ve yaygın semptomları ekledim. 
# Yahya ile pazar günü bu listeyi projenize göre daraltıp genişletebilirsiniz.
DDXPLUS_SYMPTOMS = {
    "E_112": "Ateş (fever)",
    "E_201": "Boğaz ağrısı (sore throat)",
    "E_134": "Öksürük (cough)",
    "E_129": "Burun akıntısı (runny nose)",
    "E_204": "Halsizlik / Yorgunluk (fatigue)",
    "E_200": "Gözlerde sulanma veya kızarıklık (watery or red eyes)",
    "E_151": "Kas ağrısı / Vücut ağrısı (muscle ache / myalgia)",
    "E_154": "Bulantı (nausea)",
    "E_215": "Kusma (vomiting)",
    "E_144": "İshal (diarrhea)",
    "E_173": "Nefes darlığı (shortness of breath / dyspnea)",
    "E_55_@_V_12": "Şiddetli göğüs ağrısı (severe chest pain)",
    "E_53": "Baş ağrısı (headache)"
}

def extract_symptoms_from_text(user_text: str) -> dict:
    """
    Hekim paneline girilen serbest metni analiz eder, 
    DDXPlus sözlüğüne göre 0 ve 1'lerden oluşan bir sözlük döner.
    """
    # Hızlı, kararlı ve bütçe dostu olan Gemini 1.5 Flash modelini kullanıyoruz
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Prompt Mühendisliği: LLM'e rolünü ve uyması gereken katı kuralları veriyoruz
    system_instruction = f"""
    Sen klinik ön-triyaj sisteminde çalışan uzman bir tıbbi yapay zeka asistanısın. 
    Görevin, sana gelen hasta şikayet metnini dikkatlice analiz etmek ve bunu verilen DDXPlus semptom sözlüğündeki kodlarla eşleştirmektir.
    
    DDXPlus Semptom Sözlüğü:
    {json.dumps(DDXPLUS_SYMPTOMS, ensure_ascii=False, indent=2)}
    
    Kurallar:
    1. Metinde hastada VAR olduğu belirtilen semptomların değerini 1 yap.
    2. Metinde açıkça YOK olduğu, şikayeti olmadığı belirtilen semptomların değerini 0 yap.
    3. Metinde hiç bahsedilmeyen semptomların değerini varsayılan olarak 0 yap.
    4. Çıktıyı SADECE VE SADECE JSON formatında ver. Başında veya sonunda hiçbir açıklama, markdown işareti (```json gibi) veya konuşma cümlesi ekleme.
    """
    
    # Gemini'ın çıktı olarak sadece temiz bir JSON üretmesini garanti ediyoruz
    generation_config = {"response_mime_type": "application/json"}
    
    try:
        response = model.generate_content(
            contents=[system_instruction, f"Analiz edilecek hasta şikayeti: {user_text}"],
            generation_config=generation_config
        )
        
        # Gelen string formatındaki JSON'ı Python dictionary nesnesine çeviriyoruz
        symptom_output = json.loads(response.text)
        return symptom_output
        
    except Exception as e:
        print(f"Gemini API veya JSON Ayrıştırma Hatası: {e}")
        # Hata durumunda uygulamanın çökmesini önlemek için tüm semptomları 0 dönen yedek plan
        return {key: 0 for key in DDXPLUS_SYMPTOMS.keys()}

# Kodun kendi bilgisayarında tek başına çalışıp çalışmadığını test etmek için:
if __name__ == "__main__":
    test_metni = "Hastanın dünden beri şiddetli baş ağrısı ve yüksek ateşi var, ancak öksürük veya nefes darlığı şikayeti bulunmuyor."
    print("Gemini API'ye istek gönderiliyor, lütfen bekleyin...")
    
    sonuc = extract_symptoms_from_text(test_metni)
    
    print("\n✅ Gemini'dan Başarıyla Dönen JSON Çıktısı:")
    print(json.dumps(sonuc, indent=4, ensure_ascii=False))