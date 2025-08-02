from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import uvicorn

# 1️⃣ Inisialisasi FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # atau ganti dengan ["http://localhost:5173"] untuk lebih aman
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2️⃣ Load model Keras dengan error handling
model = tf.keras.models.load_model("mainModel.keras", compile=False)
print("✅ Model loaded successfully")

# 3️⃣ Load labels dari file
try:
    with open("labels.txt") as f:
        labels = [line.strip() for line in f]
    print(f"✅ Loaded {len(labels)} labels")
except Exception as e:
    print(f"❌ Error loading labels: {e}")
    labels = [f"Batik Pattern {i+1}" for i in range(60)]

# 4️⃣ Ukuran input gambar (sesuai dengan model!)
IMAGE_SIZE = (224, 224)  # Sesuai dengan input shape model yang ter-load

# 5️⃣ Endpoint root
@app.get("/")
def read_root():
    return {
        "message": "FastAPI Batik Classifier is running!",
        "model_loaded": model is not None,
        "total_classes": len(labels)
    }

# 6️⃣ Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "total_classes": len(labels)
    }

# 7️⃣ Model info endpoint
@app.get("/model-info")
def model_info():
    return {
        "model_type": "MobileNetV2 Transfer Learning",
        "input_shape": str(model.input_shape),
        "output_shape": str(model.output_shape),
        "total_parameters": model.count_params(),
        "total_classes": len(labels),
        "available_classes": labels
    }

# 6️⃣ Endpoint prediksi (upload image)
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize(IMAGE_SIZE)
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        # Make prediction
        predictions = model.predict(image_array, verbose=0)[0]
        
        # Create prediction list
        prediction_list = [
            {"label": labels[i], "confidence": float(pred)}
            for i, pred in enumerate(predictions)
        ]
        prediction_list.sort(key=lambda x: x["confidence"], reverse=True)
        top_predictions = prediction_list[:5]
        top_prediction = top_predictions[0]

        return {
            "success": True,
            "filename": file.filename,
            "file_size": len(image_bytes),
            "data": {
                "class_name": top_prediction["label"],
                "confidence": top_prediction["confidence"],
                "probabilities": {
                    p["label"]: p["confidence"] for p in top_predictions
                },
                "top_predictions": top_predictions
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# 8️⃣ Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)