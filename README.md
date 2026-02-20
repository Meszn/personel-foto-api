#  Personel Yönetim Sistemi - Medya Mikroservisi (Media Service)

Bu depo, Personel Yönetim Sistemi mimarisinde personellerin profil fotoğraflarının güvenli bir şekilde sunucuya yüklenmesi, disk üzerinde depolanması ve istemci (Frontend/React) tarafına statik olarak sunulması işlemlerini üstlenen bağımsız bir FastAPI mikroservisidir. 

Proje, ana Backend (FastAPI & PostgreSQL) mimarisi üzerindeki dosya I/O yükünü hafifletmek ve medya sunumunu izole etmek amacıyla tasarlanmıştır.

##  Temel Özellikler

* **Asenkron Dosya İşleme:** `UploadFile` ve `shutil.copyfileobj` kullanılarak, gelen medya dosyaları RAM'i (belleği) şişirmeden "chunking" yöntemiyle akış (stream) olarak diske yazılır.
* **Statik Dosya Sunumu (Media Server):** FastAPI'nin `StaticFiles` modülü kullanılarak, yüklenen görseller `/fotograflar` rotası üzerinden Frontend uygulamasına anında ve doğrudan servis edilir.
* **Güvenli Dosya İsimlendirme:** Kullanıcıdan gelen orijinal dosya isimleri yerine, personelin eşsiz `sicil_no` değeri referans alınarak isimlendirme yapılır (Örn: `10542.jpg`). Bu sayede dosya çakışmaları ve zararlı dosya ismi açıkları önlenir.
* **Otomatik Dizin Yönetimi:** `pathlib` kütüphanesi ile sistem, başlangıçta `uploads/personel_fotograflari` dizinini kontrol eder ve yoksa otomatik olarak oluşturur.

## 🛠️ Teknoloji Yığını (Tech Stack)

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Sunucu (ASGI):** Uvicorn
* **Veri İletim Formatı:** `multipart/form-data`
* **Standart Kütüphaneler:** `shutil`, `pathlib`

## ⚙️ Kurulum ve Çalıştırma

Mikroservisi yerel ortamınızda ayağa kaldırmak için aşağıdaki adımları izleyiniz.

### 1. Gereksinimlerin Yüklenmesi
Uygulamanın çalışması için gerekli kütüphaneleri sanal ortamınıza (venv) kurun:

```bash
pip install fastapi uvicorn python-multipart
```
### 2. IP Adresi Konfigürasyonu (Önemli)
Ana API'nin ve Frontend'in bu servise erişebilmesi için main.py içerisindeki foto_url değişkenini, servisin çalışacağı makinenin (veya sunucunun) IP adresi ile güncelleyin:

#### main.py içerisindeki ilgili satır:
```bash
foto_url = f"http://<SUNUCU_IP_ADRESI>:8001/fotograflar/{new_filename}"
```

### 3. Servisi Başlatma
Diğer servislerle port çakışması yaşamamak adına servisi 8001 portundan ve ağdaki tüm isteklere açık (0.0.0.0) şekilde başlatın:
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```
## 📡 API Uç Noktaları (Endpoints)
### 1. Fotoğraf Yükleme (POST /upload-foto/)
Ana API üzerinden yönlendirilen multipart/form-data paketlerini karşılar.

#### İstek (Request):

- sicil_no (Form Data - Integer): Personelin sicil numarası.
- file (Form Data - File): Yüklenen görsel dosyası (.jpg, .png vb.)

Başarılı Yanıt (Response - 200 OK):
```bash
{
  "status": "success",
  "message": "Fotoğraf başarıyla kaydedildi.",
  "sicil_no": 10542,
  "foto_url": "[http://<SUNUCU_IP_ADRESI>:8001/fotograflar/10542.jpg](http://<SUNUCU_IP_ADRESI>:8001/fotograflar/10542.jpg)"
}
```
(Dönen foto_url değeri, ana veritabanında saklanmak üzere tasarlanmıştır.)

### 2. Medya Sunumu (GET /fotograflar/{dosya_adi})
Bu endpoint sayesinde kaydedilen fotoğraflar tarayıcı veya Frontend üzerinden <img> etiketleri ile doğrudan görüntülenebilir.

## 🏗️ Mimari İş Akışı

- Frontend (React) kullanıcısı görseli seçer ve Ana API'ye iletir.
- Ana API, görseli ve personel sicil numarasını alarak bu Mikroservise (Medya Servisi) fırlatır.
- Medya Servisi, görseli uploads/personel_fotograflari klasörüne kaydeder ve oluşturduğu tam erişilebilir URL'i Ana API'ye geri döner.
- Ana API, gelen bu URL'i PostgreSQL veritabanına kaydeder.
