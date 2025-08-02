# 🚀 Quick Start Guide - Batik Classification API

## 📋 Prerequisites
- Docker installed and running
- File `mainModel.keras` (18MB) - model yang sudah dilatih
- File `labels.txt` - daftar nama kelas batik

## ⚡ Deployment Cepat

### 1. Deploy dengan Script Otomatis
```bash
# Jalankan deployment script
./deploy.sh
```

### 2. Deploy Manual dengan Docker
```bash
# Build image
docker build -t batik-classification-api .

# Run container
docker run -d --name batik-api -p 8000:8000 batik-classification-api
```

### 3. Deploy dengan Docker Compose
```bash
docker-compose up -d
```

## 🔍 Testing API

### Test dengan Script Python
```bash
python test_api.py
```

### Test dengan Browser
Buka file `test_frontend.html` di browser

### Test dengan cURL
```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model-info

# Prediction (dengan file gambar)
curl -X POST -F "file=@your_image.jpg" http://localhost:8000/predict
```

## 📊 Endpoint API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Info API |
| `/health` | GET | Health check |
| `/model-info` | GET | Info model & kelas |
| `/predict` | POST | Prediksi 1 gambar |
| `/predict-batch` | POST | Prediksi multiple gambar |
| `/api-docs` | GET | Dokumentasi API |

## 🎨 Kelas Batik yang Dikenali

Model dapat mengenali 60 jenis pola batik:
- Arumdalu, Brendhi, Cakar Ayam
- Cinde Wilis, Gedhangan, Jayakirana
- Jayakusuma, Kawung Nitik, Kemukus
- Klampok Arum, Krawitan, Kuncup Kanthil
- Manggar, Mawur, Rengganis
- Sari Mulat, Sekar Andhong, Sekar Blimbing
- Dan 42 pola batik lainnya...

## 🌐 Integrasi dengan Website

### JavaScript Example
```javascript
async function predictBatik(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log('Prediction:', result.top_prediction.class_name);
}
```

## 🛠️ Management Commands

```bash
# Status container
./deploy.sh status

# View logs
./deploy.sh logs

# Restart container
./deploy.sh restart

# Stop container
./deploy.sh stop

# Test API
./deploy.sh test
```

## 📁 File Structure
```
batik-deploy-last/
├── app.py                 # FastAPI application
├── mainModel.keras        # Trained model (18MB)
├── labels.txt            # Class names (60 batik patterns)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker compose
├── deploy.sh             # Deployment script
├── test_api.py           # API test script
├── test_frontend.html    # Frontend test page
└── README.md            # Full documentation
```

## 🔧 Troubleshooting

### Model tidak ter-load
```bash
# Cek log container
docker logs batik-classification-api

# Pastikan file ada
ls -la mainModel.keras labels.txt
```

### Port sudah digunakan
```bash
# Cek port yang digunakan
netstat -tulpn | grep 8000

# Ganti port di docker run
docker run -p 8001:8000 batik-classification-api
```

### Memory issues
```bash
# Tambah memory limit
docker run --memory=2g -p 8000:8000 batik-classification-api
```

## 📞 Support

Untuk bantuan lebih lanjut, lihat `README.md` untuk dokumentasi lengkap.

---

**🎉 API siap digunakan untuk klasifikasi pola batik!** 