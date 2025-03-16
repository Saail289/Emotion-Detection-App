from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
import numpy as np
import cv2

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect-emotion")
async def detect_emotion(file: UploadFile = File(...)):
    # Read the image file
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect emotions using DeepFace
    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    dominant_emotion = result[0]['dominant_emotion']
    confidence = result[0]['emotion'][dominant_emotion]

    return {"emotion": dominant_emotion, "confidence": confidence}

# Add this block to ensure the app works with Gunicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)  # Use port 10000 for Render