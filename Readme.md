# 🩺 Akıllı Ön-Triyaj ve Doktor Karar Destek Paneli
### 🚀 YZTA Bootcamp 2026 - Grup 131 Proje Prototipi (MVP Phase 1)

Bu proje, **Yapay Zeka ve Teknoloji Akademisi (YZTA) Bootcamp 2026 - 5. Akademi Dönemi** kapsamında, Grup 131 tarafından geliştirilen yapay zeka destekli bir ön-triyaj ve klinik karar destek sistemi prototipidir. 

Projenin temel amacı; hastaların randevu öncesinde şikâyetlerini doğal dilde ifade edebileceği kontrollü bir arayüz sunmak, bu şikâyetleri yapılandırılmış verilere dönüştürerek klasik makine öğrenmesi modelleriyle olası branş ve aciliyet skorunu tahmin etmek ve hekime muayene öncesinde hazırlık şansı tanıyan dinamik bir özet panel üretmektir.

---

## 🎯 Temel Özellikler (MVP Kapsamı)
* **Yapay Zeka Destekli Metin Analizi:** Google Gemini API kullanılarak hastanın doğal dildeki şikayetinden tıbbi semptomların sıfır hata ile JSON formatında ayıklanması.
* **Akıllı Branş ve Aciliyet Tahmini:** `scikit-learn` (Random Forest / XGBoost) modelleriyle semptomlar üzerinden poliklinik yönlendirmesi ve 1-10 arası aciliyet skoru üretimi.
* **Hafif ve Hızlı Arayüz (Streamlit):** Hem hasta giriş ekranını hem de hekim karar destek panelini tek bir Python ekosisteminde birleştiren kullanıcı dostu arayüz.
* **Etik Yapay Zeka Yaklaşımı:** Kesinlikle tanı koymayan, "ön bilgilendirme amaçlı karar destek verisidir" uyarısı barındıran klinik sınır koruması.

---

## 🏗️ Proje Klasör Mimarisi

```text
SmartTriage_Grup131/
│
├── data/                   # Kaggle'dan edinilen ham ve işlenmiş veri setleri (.csv)
├── notebooks/              # Keşifçi Veri Analizi (EDA) ve Model Eğitim Jupyter Notebook'ları
├── models/                 # Eğitilmiş makine öğrenmesi modelleri (.pkl / .joblib)
├── src/                    # Ana Kaynak Kod Klasörü
│   ├── ml/                 # Model yükleme ve tahmin (predict) fonksiyonları
│   ├── llm/                # Gemini API entegrasyonu ve prompt mühendisliği katmanı
│   └── ui/                 # Streamlit arayüz kodları (app.py)
├── assets/                 # README dökümantasyonunda kullanılan ekran görüntüleri
├── .env                    # API Anahtarları ve gizli değişkenler (Git'e pushlanmaz!)
├── .gitignore              # Proje dışı tutulacak dosya filtreleri
├── requirements.txt        # Proje bağımlılıkları ve Python paketleri
└── README.md               # Proje ana dökümantasyonu
```

## Uygulama Arayüzü ve Ekran Görüntüleri
### 1. Karşılama Ekranı & Genel Bakış
Sistemin çalışma mantığının, hasta istatistiklerinin ve demo branş dağılım grafiklerinin yer aldığı ana karşılama arayüzü:
![alt text](assets/app_SS_1.jpeg)

###  2. Hasta Ön-Triyaj Giriş Paneli
Hastanın yaş, şikayet süresi, şiddeti ve doğal dildeki tıbbi durumunu girdiğinde arkada Gemini API ve ML modelini tetikleyen kullanıcı veri giriş formu:
![alt text](assets/app_SS_2.jpeg)

###  3. Hekim Karar Destek Paneli (Detaylı Özet ve Filtreleme)
Hekimlerin randevudan önce hastanın durumunu analiz etmesini sağlayan, risk faktörlerini listeleyen ve Gemini API tarafından üretilen "Yapay Zeka Özeti" modülünü içeren akıllı panel
![alt text](assets/app_SS_3.jpeg)

Filtreleme mekanizması sayesinde aciliyet seviyesine ve poliklinik branşına göre hasta listesi dinamik olarak daraltılabilmektedir:
![alt text](assets/app_SS_4.jpeg)

### 4. Genel İstatistikler ve Klinik Analiz Paneli
Klinik yönetiminin günlük hasta trendini, aciliyet dağılımlarını ve branş bazlı yoğunlukları izleyebileceği veri görselleştirme alanı:
![alt text](assets/app_SS_5.jpeg)

## 🔄 Scrum Süreci ve Sprint Yönetimi
Projemiz, Scrum metodolojisine uygun olarak yönetilmektedir. İş takibi, backlog yönetimi ve sprint tahtası için ClickUp kullanılmıştır.

## 📅 Sprint 1 (İlk Aşama Teslimi - 5 Temmuz)
**Hedef:** Hızlı prototipleme amacıyla Streamlit üzerinde uçtan uca çalışan (End-to-End) MVP'nin ayağa kaldırılması, LLM JSON entegrasyonunun tamamlanması ve temel ML modelinin arayüze bağlanması.

![alt text](assets/Clickup_Board.png)

## 👥 Ekip ve Görev Dağılımı (Grup 131)

- <b>Kadriye HARMANCI:</b> Scrum Master / Yapay Zeka Geliştiricisi (ClickUp Sprint Board yönetimi, veri akış entegrasyonu).
- <b>Yahya Fuat GÖKKUŞ:</b> Product Owner / Veri Analizcisi (Gemini API Entegrasyonu, Prompt Tasarımı ve Scikit-Learn Model Eğitimi).
- <b>Meryem AKBABA:</b> Developer / Dokümantasyon Sorumlusu (Slack/Git süreçlerinin yönetimi, Streamlit UI tasarımı,dosya hiyerarşisinin takibi ve teknik dökümantasyon).

## ⚠️ Etik Not ve Sorumluluk Reddi
Bu sistem kesinlikle bir tanı koyma aracı değildir. Sistem tarafından üretilen branş önerileri ve aciliyet skorları, yalnızca hastanın randevu öncesinde durumunu özetlemek ve hekime klinik karar destek mekanizması sunmak amacıyla geliştirilmiş deneysel bir prototiptir. Nihai tıbbi karar ve teşhis yetkisi tamamen uzman hekime aittir.