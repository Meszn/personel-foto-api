# 📄 Yazılım Gereksinimleri Belirtimi (SRS)
## Proje: Personel Yönetim Sistemi

---

### 1. Giriş

#### 1.1. Amaç
Bu doküman, "Personel Yönetim Sistemi" projesinin mimari sınırlarını, fonksiyonel ve fonksiyonel olmayan gereksinimlerini, kullanılacak teknoloji yığınını ve veri akış süreçlerini tanımlamayı amaçlamaktadır. Proje, stajyer ekibinin ortak çalışma yetkinliğini artırmak ve modern yazılım geliştirme süreçlerini (Agile/Scrum simülasyonu) pratik etmek amacıyla tasarlanmıştır.

#### 1.2. Kapsam
Sistem, kurum içi personelin kayıt, güncelleme, silme ve listeleme (CRUD) operasyonlarının yönetilmesini, personel profil fotoğraflarının bağımsız bir mikroservis üzerinden güvenli bir şekilde depolanıp sunulmasını ve tüm bu süreçlerin modern bir web arayüzü ile son kullanıcıya yansıtılmasını kapsar.

---

### 2. Genel Tanım

#### 2.1. Ürün Perspektifi
Sistem, üç ana bileşen ve bir veritabanı sunucusundan oluşan dağıtık bir mimari üzerine inşa edilmiştir:

-   **Frontend (İstemci):** Kullanıcı etkileşimlerini yöneten web arayüzü.
-   **Ana API (Backend):** İş mantığını ve veritabanı işlemlerini yürüten merkez servis.
-   **Medya Mikroservisi:** Sadece dosya (fotoğraf) yükleme ve statik sunum işlemlerini üstlenen izole servis.
-   **Veritabanı:** İlişkisel veri saklama katmanı.

#### 2.2. Kullanıcı Sınıfları ve Özellikleri
-   **Sistem Yöneticisi / İK Personeli:** Sistem üzerinden yeni personel ekleyebilir, mevcut personelin verilerini (sicil numarası, fotoğraf, kimlik bilgileri vb.) güncelleyebilir ve silebilir.

#### 2.3. Çalışma Ortamı
-   **Sunucu Altyapısı:** Docker konteynerizasyon teknolojisi destekli herhangi bir Linux/Windows sunucu.
-   **İstemci:** Güncel web tarayıcıları (Chrome, Firefox, Safari vb.).

---

### 3. Teknoloji Yığını ve Altyapı (Tech-Stack)

-   **DevOps & Sanallaştırma:** Docker, Docker Compose
-   **Veritabanı Katmanı:** PostgreSQL, pgAdmin (Konteynerize edilmiş yönetim arayüzü)
-   **Ana Backend (Core API):** Python, FastAPI, SQLAlchemy ORM
-   **Medya Mikroservisi:** Python, FastAPI, Uvicorn, Asenkron dosya işleme (I/O)
-   **Frontend (İstemci):** React, Vite, Tailwind CSS v4, PostCSS, Axios

---

### 4. Sistem Özellikleri ve Fonksiyonel Gereksinimler

#### 4.1. Personel Yönetimi (Core API)
-   **Gereksinim 4.1.1 (Personel Ekleme):** Sistem, yeni personelin sicil numarası, ad, soyad ve diğer özlük bilgileri ile veritabanına kaydedilmesini sağlamalıdır.
-   **Gereksinim 4.1.2 (Personel Listeleme/Okuma):** Sistem, kayıtlı personelleri listeleyebilmeli ve belirli bir `sicil_no` ile filtreleme yapabilmelidir.
-   **Gereksinim 4.1.3 (Personel Güncelleme/Silme):** Yetkili kullanıcılar mevcut personel bilgilerini güncelleyebilmeli veya sistemden silebilmelidir.
-   **Gereksinim 4.1.4 (ORM Entegrasyonu):** Tüm veritabanı etkileşimleri SQLAlchemy ORM üzerinden güvenli bir şekilde (SQL Injection korumalı) gerçekleştirilmelidir.

#### 4.2. Medya ve Fotoğraf Yönetimi (Media Microservice)
-   **Gereksinim 4.2.1 (Fotoğraf Yükleme):** Frontend'den Ana API'ye gönderilen görsel, medya servisine iletilmeli; ram şişmesini önlemek için "chunking" yöntemi ile asenkron olarak diske yazılmalıdır.
-   **Gereksinim 4.2.2 (Güvenli İsimlendirme):** Yüklenen dosyalar, çakışmaları ve zafiyetleri önlemek için personelin eşsiz `sicil_no` değeri ile (Örn: `10542.jpg`) isimlendirilmelidir.
-   **Gereksinim 4.2.3 (Statik Medya Sunumu):** Medya servisi, yüklenen fotoğrafları `/fotograflar` rotası üzerinden Frontend'e doğrudan ve anında servis edebilmelidir.
-   **Gereksinim 4.2.4 (Bağlantı Kaydı):** Medya servisinin oluşturduğu dosya URL'i, ana API tarafından PostgreSQL veritabanındaki ilgili personel kaydına işlenmelidir.

#### 4.3. Kullanıcı Arayüzü (Frontend)
-   **Gereksinim 4.3.1 (Arayüz Tasarımı):** İstemci tarafı Tailwind CSS v4 kullanılarak modern, duyarlı (responsive) ve kullanıcı dostu bir yapıda olmalıdır.
-   **Gereksinim 4.3.2 (Asenkron İletişim):** Arayüz, Axios kütüphanesini kullanarak arka plandaki API uç noktalarına asenkron HTTP istekleri (GET, POST, PUT, DELETE) atmalı ve sayfa yenilenmeden verileri UI üzerinde güncellemelidir.

---

### 5. Fonksiyonel Olmayan Gereksinimler

-   **5.1. Performans:** Medya yükleme işlemlerinin ana API'yi bloklamaması için mimari, bağımsız bir mikroservis ile bölünmüştür. API yanıt süreleri optimize edilmelidir.
-   **5.2. Ölçeklenebilirlik:** Sistem bileşenleri (Veritabanı, Backend, Medya Servisi) Docker ile ayrıştırıldığı için ilerleyen aşamalarda yatay ölçeklemeye (horizontal scaling) uygun olmalıdır.
-   **5.3. Güvenilirlik:** `pathlib` ve `shutil` kütüphaneleri ile dizin kontrolleri otomatik yapılmalı, klasör eksikliklerinde sistem çökmeden klasörleri kendi oluşturmalıdır.
-   **5.4. Bakım Edilebilirlik:** Kod blokları modüler yapıda tutulmalı, uç noktalar OpenAPI (Swagger UI) spesifikasyonları ile otomatik dokümante edilmelidir.
