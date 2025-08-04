# 🚂 Railway Deployment Guide

## 📋 Files untuk Railway

Pastikan file berikut ada di repository Anda:

```
├── app.py                 # FastAPI application
├── mainModel.keras        # Trained model (18MB)
├── labels.txt            # Class names
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── railway.json          # Railway configuration
└── .railwayignore        # Files to ignore
```

## 🚀 Deployment Steps

### 1. Push ke GitHub
```bash
git add .
git commit -m "Add batik classification API"
git push origin main
```

### 2. Connect ke Railway
1. Buka [Railway.app](https://railway.app)
2. Login dengan GitHub
3. Klik "New Project"
4. Pilih "Deploy from GitHub repo"
5. Pilih repository Anda

### 3. Railway akan otomatis:
- ✅ Membaca `Dockerfile`
- ✅ Build Docker image
- ✅ Deploy aplikasi
- ✅ Memberikan URL publik

## 🌐 Environment Variables

Railway akan otomatis set:
- `PORT` - Port yang digunakan (biasanya 8000)
- `RAILWAY_STATIC_URL` - URL untuk static files

## 📊 Monitoring

Setelah deploy, Anda bisa:
- View logs di Railway dashboard
- Monitor health check di `/health`
- Test API di URL yang diberikan Railway

## 🧪 Test API

```bash
# Ganti YOUR_RAILWAY_URL dengan URL dari Railway
curl https://YOUR_RAILWAY_URL.railway.app/health
curl https://YOUR_RAILWAY_URL.railway.app/model-info
```

## 🔧 Troubleshooting

### Jika build gagal:
1. Cek logs di Railway dashboard
2. Pastikan semua file ada di repository
3. Pastikan `mainModel.keras` tidak corrupt

### Jika API tidak respond:
1. Cek health check: `/health`
2. View logs di Railway dashboard
3. Restart deployment jika perlu

## 🌐 Frontend Integration

```javascript
// Ganti dengan URL Railway Anda
const API_URL = 'https://YOUR_RAILWAY_URL.railway.app';

async function predictBatik(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  return result;
}
```

---

**🎉 Railway akan handle semua deployment secara otomatis!** 