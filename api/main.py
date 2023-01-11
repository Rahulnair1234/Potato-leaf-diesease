from fastapi import FastAPI,File,UploadFile
import uvicorn 
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins=["http://localhost","http://localhost:3000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    
)

MODEL=tf.keras.models.load_model("./saved_models/1")
CLASS_NAMES=["Early Blight","Late Blight","Healthy"]

@app.get("/ping")

async def ping():
    return "Hello I am Alive"

def read_file_as_image(data)->np.ndarray:
    image=np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")

async def predict(file: UploadFile=File(...)):
    image=read_file_as_image(await file.read())
    img_batch=np.expand_dims(image,0)

    prediction=MODEL.predict(img_batch)
    index=np.argmax(prediction[0])
    predicted_class=CLASS_NAMES[index]
    confidence=np.max(prediction[0])
    return{
        'class':predicted_class,
        'confidence':float(confidence)
    }

if __name__=="__main__":
    uvicorn.run("main:app",host="localhost",port=8000,reload=True)