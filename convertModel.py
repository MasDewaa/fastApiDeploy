# JALANKAN SKRIP INI DI LINGKUNGAN TRAINING ASLI ANDA
import tensorflow as tf

try:
    # Langkah 1: Muat model lama (ini akan berhasil di sini)
    print("Memuat model dari format .keras...")
    model = tf.keras.models.load_model("mainModel.keras")
    print("Model berhasil dimuat.")

    # Langkah 2: Simpan bobotnya saja ke format .h5
    print("Menyimpan bobot ke format .h5...")
    model.save_weights("model_weights.h5")

    print("\n✅ Berhasil! File 'model_weights.h5' telah dibuat.")
    print("Sekarang, pindahkan file 'model_weights.h5' ini ke mesin deployment Anda.")

except Exception as e:
    print(f"\n❌ Terjadi error: {e}")
    print("Pastikan Anda menjalankan skrip ini di lingkungan yang sama dengan saat Anda membuat model.")