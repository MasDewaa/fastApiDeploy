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

# 2️⃣ Global variables
model = None
labels = []

# 2.5️⃣ Model validation function
def validate_model(model):
    """Validate that the loaded model can make predictions"""
    try:
        # Create a dummy input to test the model
        dummy_input = np.random.random((1, 160, 160, 3))
        prediction = model.predict(dummy_input, verbose=0)
        print(f"✅ Model validation successful. Output shape: {prediction.shape}")
        return True
    except Exception as e:
        print(f"❌ Model validation failed: {e}")
        return False

# 2.6️⃣ Custom model loading function for dense layer issues
def load_model_with_dense_fix(model_path):
    """Load model with specific handling for dense layer input issues"""
    try:
        # Try to load the model configuration first
        model_config = tf.keras.models.model_from_json(
            tf.keras.models.load_model(model_path, compile=False).to_json()
        )
        
        # Load weights separately
        original_model = tf.keras.models.load_model(model_path, compile=False)
        model_config.set_weights(original_model.get_weights())
        
        # Compile the model
        model_config.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Model loaded with dense layer fix")
        return model_config
    except Exception as e:
        print(f"❌ Dense layer fix failed: {e}")
        return None

# 3️⃣ Load model and labels function
def load_model_and_labels():
    global model, labels
    
    # Load model with multiple fallback strategies
    model_loaded = False
    
    # Strategy 1: Try loading with custom_objects and compile=False
    try:
        model = tf.keras.models.load_model("mymodel.keras", compile=False, custom_objects=None)
        print("✅ Model loaded successfully with compile=False")
        model_loaded = True
    except Exception as e:
        print(f"❌ Strategy 1 failed: {e}")
    
    # Strategy 2: Try loading with different TensorFlow version compatibility
    if not model_loaded:
        try:
            # Try loading with legacy format support
            model = tf.keras.models.load_model("mymodel.keras", compile=False, options=tf.saved_model.LoadOptions(experimental_io_device='/job:localhost'))
            print("✅ Model loaded successfully with legacy format support")
            model_loaded = True
        except Exception as e:
            print(f"❌ Strategy 2 failed: {e}")
    
    # Strategy 3: Try loading mainModel.keras as fallback
    if not model_loaded:
        try:
            model = tf.keras.models.load_model("mainModel.keras", compile=False)
            print("✅ Fallback model (mainModel.keras) loaded successfully")
            model_loaded = True
        except Exception as e:
            print(f"❌ Strategy 3 failed: {e}")
    
    # Strategy 4: Try to fix the dense layer issue by recreating the model
    if not model_loaded:
        try:
            # Load the model architecture without weights first
            model = tf.keras.models.load_model("mymodel.keras", compile=False, custom_objects=None)
            
            # If we get here, the model loaded but might have the dense layer issue
            # Try to fix by recompiling the model
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            print("✅ Model loaded and recompiled successfully")
            model_loaded = True
        except Exception as e:
            print(f"❌ Strategy 4 failed: {e}")
    
    # Strategy 5: Try custom dense layer fix
    if not model_loaded:
        try:
            model = load_model_with_dense_fix("mymodel.keras")
            if model is not None:
                print("✅ Model loaded with custom dense layer fix")
                model_loaded = True
        except Exception as e:
            print(f"❌ Strategy 5 failed: {e}")
    
    if not model_loaded:
        print("❌ All loading strategies failed. Model could not be loaded.")
        return False
    
    # Validate the loaded model
    if not validate_model(model):
        print("❌ Model validation failed after loading")
        return False
    
    # Load labels
    try:
        with open("labels.txt") as f:
            labels = [line.strip() for line in f]
        print(f"✅ Loaded {len(labels)} labels")
    except Exception as e:
        print(f"❌ Error loading labels: {e}")
        labels = [f"Batik Pattern {i+1}" for i in range(60)]
    
    return True

# 4️⃣ Load on startup
load_model_and_labels()

# 5️⃣ Ukuran input gambar
IMAGE_SIZE = (160, 160)

# 6️⃣ Endpoint root
@app.get("/")
def read_root():
    return {
        "message": "FastAPI Batik Classifier is running!",
        "model_loaded": model is not None,
        "total_classes": len(labels)
    }

# 7️⃣ Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "total_classes": len(labels)
    }

# 8️⃣ Model info endpoint
@app.get("/model-info")
def model_info():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": "MobileNetV2 Transfer Learning",
        "input_shape": str(model.input_shape),
        "output_shape": str(model.output_shape),
        "total_parameters": model.count_params(),
        "total_classes": len(labels),
        "available_classes": labels
    }

# 9️⃣ Endpoint prediksi (upload image)
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Check if model is loaded
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
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