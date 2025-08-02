# 🎨 Batik Classification API

API untuk klasifikasi pola batik menggunakan model deep learning berbasis MobileNetV2 dengan Transfer Learning.

## 📋 Deskripsi

Aplikasi ini menggunakan model deep learning yang telah dilatih untuk mengklasifikasikan 60 jenis pola batik berbeda. Model menggunakan arsitektur MobileNetV2 dengan Transfer Learning untuk performa yang optimal.

## 🚀 Fitur

- **FastAPI Framework**: REST API yang cepat dan modern
- **Transfer Learning**: Menggunakan MobileNetV2 sebagai base model
- **Multi-file Upload**: Mendukung upload batch hingga 10 gambar
- **CORS Support**: Siap untuk integrasi dengan website frontend
- **Health Check**: Monitoring kesehatan aplikasi
- **Docker Ready**: Siap untuk deployment dengan Docker

## 📦 Endpoint API

### 1. Root Endpoint
```
GET /
```
Informasi dasar API

### 2. Health Check
```
GET /health
```
Status kesehatan aplikasi dan model

### 3. Model Information
```
GET /model-info
```
Informasi detail tentang model yang digunakan

### 4. Single Prediction
```
POST /predict
```
Prediksi untuk satu gambar

**Request:**
- Content-Type: `multipart/form-data`
- Body: File gambar (PNG, JPG, JPEG)

**Response:**
```json
{
  "filename": "batik.jpg",
  "file_size": 12345,
  "content_type": "image/jpeg",
  "predictions": [
    {
      "rank": 1,
      "class_name": "Batik Pattern 1",
      "class_id": 0,
      "probability": 0.95,
      "confidence_percentage": 95.0
    }
  ],
  "top_prediction": {...},
  "processing_time": "N/A"
}
```

### 5. Batch Prediction
```
POST /predict-batch
```
Prediksi untuk multiple gambar (maksimal 10 file)

### 6. API Documentation
```
GET /api-docs
```
Dokumentasi lengkap endpoint

## 🐳 Deployment dengan Docker

### 1. Build Docker Image
```bash
docker build -t batik-classification-api .
```

### 2. Run Container
```bash
docker run -d \
  --name batik-api \
  -p 8000:8000 \
  batik-classification-api
```

### 3. Docker Compose (Opsional)
Buat file `docker-compose.yml`:
```yaml
version: '3.8'
services:
  batik-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Lalu jalankan:
```bash
docker-compose up -d
```

## 🔧 Deployment Manual

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python app.py
```

Atau dengan uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 🌐 Integrasi dengan Website

### Contoh JavaScript untuk Frontend

```javascript
// Upload single image
async function predictBatik(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  try {
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    console.log('Prediction:', result);
    return result;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Upload multiple images
async function predictBatch(imageFiles) {
  const formData = new FormData();
  
  for (let file of imageFiles) {
    formData.append('files', file);
  }
  
  try {
    const response = await fetch('http://localhost:8000/predict-batch', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    console.log('Batch Prediction:', result);
    return result;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Contoh HTML Form

```html
<!DOCTYPE html>
<html>
<head>
    <title>Batik Classification</title>
</head>
<body>
    <h1>🎨 Batik Classification</h1>
    
    <form id="uploadForm">
        <input type="file" id="imageInput" accept="image/*" required>
        <button type="submit">Predict Batik</button>
    </form>
    
    <div id="result"></div>
    
    <script>
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const file = document.getElementById('imageInput').files[0];
            const result = await predictBatik(file);
            
            if (result.top_prediction) {
                document.getElementById('result').innerHTML = `
                    <h3>Prediction: ${result.top_prediction.class_name}</h3>
                    <p>Confidence: ${result.top_prediction.confidence_percentage}%</p>
                `;
            }
        });
    </script>
</body>
</html>
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Model Info
```bash
curl http://localhost:8000/model-info
```

## 🔒 Production Considerations

1. **CORS Configuration**: Sesuaikan `allow_origins` di `app.py` untuk production
2. **Rate Limiting**: Tambahkan rate limiting untuk mencegah abuse
3. **Authentication**: Implementasikan authentication jika diperlukan
4. **Logging**: Tambahkan logging untuk monitoring
5. **SSL/TLS**: Gunakan HTTPS untuk production
6. **Load Balancer**: Gunakan load balancer untuk high availability

## 📁 Struktur File

```
batik-deploy-last/
├── app.py                 # FastAPI application
├── mainModel.keras        # Trained model file
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore file
└── README.md            # This file
```

## 🛠️ Troubleshooting

### Model tidak ter-load
- Pastikan file `mainModel.keras` ada di direktori yang sama
- Cek log container: `docker logs batik-api`

### Port sudah digunakan
- Ganti port di Dockerfile dan docker run command
- Atau hentikan service yang menggunakan port 8000

### Memory issues
- Tambahkan memory limit: `docker run --memory=2g ...`
- Atau gunakan model yang lebih kecil

## 📞 Support

Untuk pertanyaan atau masalah, silakan buat issue di repository ini.

---

**Dibuat dengan ❤️ menggunakan FastAPI dan TensorFlow** 