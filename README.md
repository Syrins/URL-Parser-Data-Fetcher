# URL Parser & Data Fetcher

![Application Screenshot](screenshot.png)

## 📝 Tanım

URL Parser & Data Fetcher, API istekleri yapmak, yanıtları görüntülemek ve kaydetmek için geliştirilmiş bir masaüstü uygulamasıdır. Kullanıcı dostu arayüzü sayesinde:

- API endpoint'lerine istek gönderebilir
- Gelen yanıtları formatlı bir şekilde görüntüleyebilir
- Yanıtları otomatik olarak organize edilmiş şekilde kaydedebilir
- Daha önce kaydedilmiş yanıtları görüntüleyebilir ve analiz edebilirsiniz

## ✨ Özellikler

- **Modern ve Kullanıcı Dostu Arayüz**: CustomTkinter ile oluşturulmuş, koyu/açık tema desteği
- **Çoklu İstek Metodları**: GET, POST, PUT, DELETE, PATCH desteği
- **Otomatik URL Parsing**: URL'den parametreleri otomatik çıkarma
- **JSON Görüntüleyici**: Syntax highlighting ile gelişmiş JSON görüntüleme
- **Otomatik Kayıt Sistemi**: Yanıtları domain/path yapısına göre otomatik kaydetme
- **Log Kayıtları**: Tüm işlemlerin detaylı log kaydı
- **Veri Yönetimi**: Kaydedilmiş yanıtları tarih ve konum bilgisiyle listeleme

## 🛠 Kurulum

1. Gereksinimleri yükleyin:

```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:

```bash
python main.py
```

## 📂 Klasör Yapısı

```
.
├── config/               # Konfigürasyon dosyaları
│   └── settings.py       # Uygulama ayarları
├── ui/                   # Kullanıcı arayüzü dosyaları
│   ├── main_window.py    # Ana pencere
│   ├── request_tab.py    # İstek sekmesi
│   └── data_viewer_tab.py# Veri görüntüleyici sekme
├── utils/                # Yardımcı araçlar
│   ├── file_manager.py   # Dosya yönetimi
│   ├── logger.py         # Log sistemi
│   └── request_handler.py# İstek işleyici
├── veriler/              # Kaydedilmiş yanıtlar (otomatik oluşturulur)
├── logs/                 # Log dosyaları (otomatik oluşturulur)
├── main.py               # Uygulama giriş noktası
└── requirements.txt      # Bağımlılıklar
```

## 🎨 Temalar

Uygulama 3 farklı tema modunu destekler:

- Light (Açık)
- Dark (Koyu) - Varsayılan
- System (Sistem teması)

Sağ üst köşedeki menüden tema değiştirilebilir.

## 📊 Kayıtlı Verileri Görüntüleme

1. "Data Viewer" sekmesine geçin
2. Sol tarafta kayıtlı yanıtların listesi görünecektir
3. Bir kayıt seçtiğinizde, sağ tarafta JSON içeriği syntax highlighting ile görüntülenecektir
4. "↻" butonu ile listeyi yenileyebilirsiniz

## 📜 Log Sistemi

Uygulamanın alt kısmında tüm işlemlerin log kayıtları görüntülenir. Loglar ayrıca `logs/` dizininde tarih bazlı dosyalara kaydedilir.

## ⚙️ Ayarlar

`config/settings.py` dosyasından aşağıdaki ayarları değiştirebilirsiniz:

- Varsayılan pencere boyutu
- Renk teması
- Varsayılan HTTP başlıkları
- Request timeout süresi
- Log dosyası boyutu ve sayısı

## 📄 Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Detaylar için LICENSE dosyasına bakınız.

---

**Not**: Bu uygulama geliştirme aşamasındadır. Öneri ve katkılarınızı bekliyoruz!
