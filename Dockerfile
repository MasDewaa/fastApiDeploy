# Tahap 1: Builder - Bertugas menginstal semua dependensi
# Menggunakan -slim sudah cukup untuk mengurangi ukuran awal
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Upgrade pip dan install dependensi ke dalam virtual environment
# Ini membuat proses penyalinan ke tahap selanjutnya lebih bersih dan terisolasi
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Tahap 2: Final - Image akhir yang akan dijalankan di produksi
# Kita mulai lagi dari base image yang bersih dan ramping
FROM python:3.12-slim

# Buat user non-root untuk keamanan
RUN useradd --create-home appuser
WORKDIR /home/appuser/app

# Install HANYA dependensi sistem yang dibutuhkan saat runtime
# --no-install-recommends mencegah instalasi paket yang tidak perlu
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    curl \
    # Membersihkan cache dalam satu layer yang sama untuk efisiensi
    && rm -rf /var/lib/apt/lists/*

# Salin virtual environment yang berisi paket Python dari tahap builder
COPY --from=builder /opt/venv /opt/venv

# Salin file aplikasi
COPY app.py .
COPY labels.txt .
COPY mainModel.keras .

# Berikan kepemilikan file kepada user non-root
RUN chown -R appuser:appuser /home/appuser/app

# Ganti ke user non-root
USER appuser

# Aktifkan virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Expose port untuk FastAPI
EXPOSE 8000

# Health check untuk monitoring
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Jalankan aplikasi FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
