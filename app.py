from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64
from typing import List, Dict, Any
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Batik Classification API",
    description="API untuk klasifikasi pola batik menggunakan model deep learning",
    version="1.0.0"
)

# Add CORS middleware for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store the loaded model
model = None
class_names = []

def load_model():
    """Load the trained model and class names"""
    global model, class_names
    try:
        model = tf.keras.models.load_model('mainModel.keras')
        
        # Load class names from labels.txt
        try:
            with open('labels.txt', 'r', encoding='utf-8') as f:
                class_names = [line.strip() for line in f.readlines() if line.strip()]
            print(f"Loaded {len(class_names)} class names from labels.txt")
        except Exception as e:
            print(f"Warning: Could not load labels.txt: {e}")
            # Fallback to generic names
            class_names = [f"Batik Pattern {i+1}" for i in range(60)]
        
        return True
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

def preprocess_image(image_bytes: bytes, target_size=(224, 224)) -> np.ndarray:
    """Preprocess image for model prediction"""
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Resize image
        image = image.resize(target_size)
        
        # Convert to array and normalize
        img_array = np.array(image)
        
        # Convert to RGB if grayscale
        if len(img_array.shape) == 2:
            img_array = np.stack((img_array,) * 3, axis=-1)
        
        # Normalize pixel values
        img_array = img_array.astype('float32') / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error preprocessing image: {str(e)}")

def get_top_predictions(predictions: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
    """Get top k predictions with their probabilities"""
    try:
        # Get indices of top k predictions
        top_indices = np.argsort(predictions[0])[-top_k:][::-1]
        
        # Create list of predictions
        top_predictions = []
        for i, idx in enumerate(top_indices):
            # Use actual class names from labels.txt
            if idx < len(class_names):
                class_name = class_names[idx]
            else:
                class_name = f"Batik Pattern {idx + 1}"  # Fallback
            
            probability = float(predictions[0][idx])
            confidence_percentage = probability * 100
            
            top_predictions.append({
                "rank": i + 1,
                "class_name": class_name,
                "class_id": int(idx),
                "probability": probability,
                "confidence_percentage": round(confidence_percentage, 2)
            })
        
        return top_predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing predictions: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    print("Loading model...")
    if load_model():
        print("✅ Model loaded successfully!")
    else:
        print("❌ Failed to load model!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Batik Classification API",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": model is not None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.get("/model-info")
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": "MobileNetV2 Transfer Learning",
        "input_shape": model.input_shape,
        "output_shape": model.output_shape,
        "total_parameters": model.count_params(),
        "framework": "TensorFlow/Keras",
        "total_classes": len(class_names),
        "available_classes": class_names
    }

@app.post("/predict")
async def predict_batik(file: UploadFile = File(...)):
    """
    Predict batik pattern from uploaded image
    
    Args:
        file: Image file (PNG, JPG, JPEG)
    
    Returns:
        JSON with prediction results
    """
    # Check if model is loaded
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read file content
    try:
        image_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    
    # Preprocess image
    processed_image = preprocess_image(image_bytes)
    
    # Make prediction
    try:
        predictions = model.predict(processed_image, verbose=0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")
    
    # Get top predictions
    top_predictions = get_top_predictions(predictions, top_k=5)
    
    # Prepare response
    response = {
        "filename": file.filename,
        "file_size": len(image_bytes),
        "content_type": file.content_type,
        "predictions": top_predictions,
        "top_prediction": top_predictions[0] if top_predictions else None,
        "processing_time": "N/A"  # You can add timing if needed
    }
    
    return JSONResponse(content=response)

@app.post("/predict-batch")
async def predict_batik_batch(files: List[UploadFile] = File(...)):
    """
    Predict batik patterns from multiple uploaded images
    
    Args:
        files: List of image files
    
    Returns:
        JSON with prediction results for all images
    """
    # Check if model is loaded
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed per batch")
    
    results = []
    
    for file in files:
        # Validate file type
        if not file.content_type.startswith('image/'):
            results.append({
                "filename": file.filename,
                "error": "File must be an image"
            })
            continue
        
        try:
            # Read file content
            image_bytes = await file.read()
            
            # Preprocess image
            processed_image = preprocess_image(image_bytes)
            
            # Make prediction
            predictions = model.predict(processed_image, verbose=0)
            
            # Get top predictions
            top_predictions = get_top_predictions(predictions, top_k=3)
            
            results.append({
                "filename": file.filename,
                "file_size": len(image_bytes),
                "content_type": file.content_type,
                "predictions": top_predictions,
                "top_prediction": top_predictions[0] if top_predictions else None
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return JSONResponse(content={
        "total_files": len(files),
        "processed_files": len([r for r in results if "error" not in r]),
        "results": results
    })

@app.get("/api-docs")
async def get_api_docs():
    """Get API documentation"""
    return {
        "endpoints": {
            "GET /": "Root endpoint with API info",
            "GET /health": "Health check endpoint",
            "GET /model-info": "Get model information",
            "POST /predict": "Predict single image",
            "POST /predict-batch": "Predict multiple images",
            "GET /api-docs": "This documentation"
        },
        "usage": {
            "single_prediction": "POST /predict with image file",
            "batch_prediction": "POST /predict-batch with multiple image files",
            "supported_formats": ["PNG", "JPG", "JPEG"],
            "max_batch_size": 10
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 