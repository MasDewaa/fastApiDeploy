# 🎨 Batik Classification API

FastAPI untuk klasifikasi pola batik menggunakan model deep learning MobileNetV2.

## 🚀 Quick Deploy

```bash
# Deploy dengan script otomatis
./deploy.sh

# Atau manual
docker build -t batik-classification-api .
docker run -d --name batik-api -p 8000:8000 batik-classification-api
```

## 📋 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Info API |
| `/health` | GET | Health check |
| `/model-info` | GET | Info model & kelas |
| `/predict` | POST | Prediksi gambar |

## 🧪 Test API

```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model-info

# Predict (dengan file gambar)
curl -X POST -F "file=@your_image.jpg" http://localhost:8000/predict
```

## 📁 Files

- `app.py` - FastAPI application
- `mainModel.keras` - Trained model (18MB)
- `labels.txt` - 60 nama kelas batik
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration
- `deploy.sh` - Deployment script

## 🎨 Kelas Batik

Model dapat mengenali 60 jenis pola batik:
- Arumdalu, Brendhi, Cakar Ayam
- Cinde Wilis, Gedhangan, Jayakirana
- Jayakusuma, Kawung Nitik, Kemukus
- Dan 53 pola batik lainnya...

## 🔧 Management

```bash
# View logs
docker logs batik-api

# Stop container
docker stop batik-api

# Restart container
docker restart batik-api
```

## 🌐 Frontend Integration

```javascript
// Upload image untuk prediksi
async function predictBatik(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  return result;
}
```

---

**🎉 API siap untuk deployment!** 