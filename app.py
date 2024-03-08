from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

# Memuat model
model = load_model('D:/FastApiTA/ModelTerbaru.h5')

# Membuat dictionary untuk mapping class prediksi ke nama penyakit
class_names = {
    0: "Blight",
    1: "Common Rust",
    2: "Gray Leaf Spot",
    3: "Healthy"
}

@app.post("/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    pil_image = Image.open(BytesIO(contents)).convert('RGB')
    img = pil_image.resize((224, 224))

    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    img_preprocessed = img_array_expanded_dims / 255.0  # Normalisasi

    # Lakukan prediksi
    prediction = model.predict(img_preprocessed)

    # Mengambil kelas dengan probabilitas tertinggi
    predicted_class = np.argmax(prediction, axis=1)
    predicted_class_name = class_names[int(predicted_class[0])]  # Menggunakan dictionary untuk mendapatkan nama penyakit

    return {"predicted_class": predicted_class_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
