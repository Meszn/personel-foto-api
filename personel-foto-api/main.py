from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles  # YENİ: Dosyaları dışarı açmak için
import shutil
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = Path("uploads/personel_fotograflari")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# YENİ: Klasörü '/fotograflar' endpoint'i altından dışarıya (frontend'e) açıyoruz
app.mount("/fotograflar", StaticFiles(directory=UPLOAD_DIR), name="fotograflar")

@app.post("/upload-foto/")
async def receive_personel_foto(
    sicil_no: int = Form(...),
    file: UploadFile = File(...)
):
    try:
        file_extension = Path(file.filename).suffix
        new_filename = f"{sicil_no}{file_extension}"
        file_path = UPLOAD_DIR / new_filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # YENİ: Frontend'in ve Veritabanının kullanacağı erişilebilir URL
        # IP adresini kendi IP'n ile sabitle
        foto_url = f"http://<SUNUCU_IP_ADRESI>:8001/fotograflar/{new_filename}"

        return {
            "status": "success",
            "message": "Fotoğraf başarıyla kaydedildi.",
            "sicil_no": sicil_no,
            "foto_url": foto_url  # PostgreSQL'e yazılacak olan alan
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")