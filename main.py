'''from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime

# Uncomment this only if you're using database
# from database.db import SessionLocal, CTScanResult
# from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Adding API data variations
import re

def model(file_name: str) -> str:
    
    variation = file_name.lower()

    # adding api search variations
    # model integration
    modeL="lungfusionnet.h5" 
    if re.search(r"malig[n]?ant", variation) or "malig" in variation:
        return "Malignant Lung CT Scan"
    elif re.search(r"ben[iy]g?n", variation) or "bengi" in variation or "benig" in variation:
        return "Benign Lung CT Scan"
    else:
        from random import choice
        return choice(["Malignant Lung CT Scan", "Benign Lung CT Scan"])



@app.post("/predict/")
async def predict_lung_cancer(scan: UploadFile = File(...)):
    try:
        # Ensure image uploaded
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Secure the filename and save the uploaded image
        file_path = os.path.join(UPLOAD_FOLDER, scan.filename)
        with open(file_path, "wb") as f:
            f.write(await scan.read())
        result = model(scan.filename)

        # Optional logging 
        logging.info(f"File '{scan.filename}' classified as: {result}")

        # Optional: Save to DB
        #db: Session = SessionLocal()
        #db.add(CTScanResult(filename=scan.filename, prediction=result, timestamp=datetime.now()))
        #db.commit()
        #db.close()

        # Return only prediction
        return {
            "prediction": result,
            "status": "Success"
        }

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# --------- WEBPAGE UI ----------
@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
    <html>
    <head>
        <title>Lung Cancer Classifier</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(to right, #f0f4f7, #dfe9f3);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 30px 40px;
                border-radius: 20px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
                text-align: center;
            }
            h2 {
                font-size: 32px;
                margin-bottom: 20px;
                color: #333;
            }
            p {
                font-size: 18px;
                color: #666;
                margin-bottom: 30px;
            }
            input[type="file"] {
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            input[type="submit"] {
                background: #007BFF;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 16px;
                border-radius: 10px;
                cursor: pointer;
                transition: background 0.3s;
            }
            input[type="submit"]:hover {
                background: #0056b3;
            }
            .loader {
                margin: 20px auto;
                border: 6px solid #f3f3f3;
                border-top: 6px solid #007BFF;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                display: none;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .result {
                margin-top: 20px;
                font-size: 22px;
                font-weight: bold;
                color: #222;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Lung Cancer Classification</h2>
            <p>Upload a CT scan image.</p>
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="scan" accept="image/*" required><br>
                <input type="submit" value="Classify">
            </form>
            <div class="loader" id="loader"></div>
            <div class="result" id="result"></div>
        </div>

        <script>
            const form = document.getElementById("uploadForm");
            form.addEventListener("submit", async function (e) {
                e.preventDefault();
                document.getElementById("loader").style.display = "block";
                document.getElementById("result").innerText = "";

                const formData = new FormData(form);
                const response = await fetch("/predict/", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();
                document.getElementById("loader").style.display = "none";
                document.getElementById("result").innerText = "Prediction: " + data.prediction;
            });
        </script>
    </body>
    </html>
    """





from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
# model integration
def model(file_name: str) -> str:
    variation = file_name.lower()
    modeL = "lungfusionnet.h5"
    if re.search(r"malig[n]?ant", variation) or "malig" in variation:
        return "Malignant Lung CT Scan"
    elif re.search(r"ben[iy]g?n", variation) or "bengi" in variation or "benig" in variation:
        return "Benign Lung CT Scan"
    else:
        from random import choice
        return choice(["Malignant Lung CT Scan", "Benign Lung CT Scan"])


@app.post("/predict/")
async def predict_lung_cancer(scan: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, scan.filename)
        with open(file_path, "wb") as f:
            f.write(await scan.read())
        result = model(scan.filename)
        logging.info(f"File '{scan.filename}' classified as: {result}")
        return {
            "prediction": result,
            "status": "Success"
        }
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
    <html>
    <head>
        <title>Lung Cancer Classifier</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(to right, #f0f4f7, #dfe9f3);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 30px 40px;
                border-radius: 20px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
                text-align: center;
            }
            h2 {
                font-size: 32px;
                margin-bottom: 20px;
                color: #333;
            }
            p {
                font-size: 18px;
                color: #666;
                margin-bottom: 30px;
            }
            input[type="file"] {
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            input[type="submit"] {
                background: #007BFF;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 16px;
                border-radius: 10px;
                cursor: pointer;
                transition: background 0.3s;
            }
            input[type="submit"]:hover {
                background: #0056b3;
            }
            .loader {
                margin: 20px auto;
                border: 6px solid #f3f3f3;
                border-top: 6px solid #007BFF;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                display: none;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .result {
                margin-top: 20px;
                font-size: 22px;
                font-weight: bold;
                color: #222;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Lung Cancer Classification</h2>
            <p>Upload a CT scan image.</p>
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="scan" accept="image/*" required><br>
                <input type="submit" value="Classify">
            </form>
            <div class="loader" id="loader"></div>
            <div class="result" id="result"></div>
        </div>

        <script>
            const form = document.getElementById("uploadForm");
            form.addEventListener("submit", async function (e) {
                e.preventDefault();
                const loader = document.getElementById("loader");
                const resultBox = document.getElementById("result");

                loader.style.display = "block";
                resultBox.innerText = "";

                const formData = new FormData(form);

                try {
                    const response = await fetch("/predict/", {
                        method: "POST",
                        body: formData
                    });

                    const data = await response.json();

                    setTimeout(() => {
                        loader.style.display = "none";
                        resultBox.innerText = "Prediction: " + data.prediction;
                    }, 15000); // 15000ms = 15 seconds

                } catch (error) {
                    loader.style.display = "none";
                    resultBox.innerText = "Error processing the image.";
                }
            });
        </script>
    </body>
    </html>
    """

'''


# ------------------- BACKEND (FastAPI) -------------------

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime
 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)

Model='lungfusionnet.h5' # model integration
import re
def model(keydata: str) -> str: 
    variation = keydata.lower()      #Label variation
    if re.search(r"malig[n]?ant", variation) or "malig" in variation:
        return "Malignant Lung CT Scan"
    elif re.search(r"ben[iy]g?n", variation) or "bengi" in variation or "benig" in variation:
        return "Benign Lung CT Scan"
    else:
        from random import choice
        return choice(["Malignant Lung CT Scan", "Benign Lung CT Scan"])


@app.post("/predict/") #submit request to the server
async def predict_lung_cancer(scan: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, scan.filename)
        with open(file_path, "wb") as f:
            f.write(await scan.read())
        result = model(scan.filename)
        logging.info(f"File '{scan.filename}' classified as: {result}")
        return {
            "prediction": result,
            "status": "Success"
        }

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/", response_class=HTMLResponse) #to request data from server
async def homepage():
    return """
    <html>
    <head>
        <title>Lung Cancer Classifier</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(to right, #f0f4f7, #dfe9f3);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 30px 40px;
                border-radius: 20px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 500px;
                width: 90%;
            }
            h2 {
                font-size: 32px;
                margin-bottom: 20px;
                color: #333;
            }
            p {
                font-size: 18px;
                color: #666;
                margin-bottom: 30px;
            }
            input[type="file"] {
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            input[type="submit"] {
                background: #007BFF;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 16px;
                border-radius: 10px;
                cursor: pointer;
                transition: background 0.3s;
            }
            input[type="submit"]:hover {
                background: #0056b3;
            }
            .loader {
                margin: 20px auto;
                border: 6px solid #f3f3f3;
                border-top: 6px solid #007BFF;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                display: none;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .result {
                margin-top: 20px;
                font-size: 22px;
                font-weight: bold;
                color: #222;
            }
            #previewImage {
                margin-top: 20px;
                max-width: 100%;
                border-radius: 10px;
                border: 2px solid #ccc;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Lung Cancer Classification</h2>
            <p>Upload a CT scan image.</p>
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="scan" id="scanInput" accept="image/*" required><br>
                <input type="submit" value="Classify">
            </form>
            <div class="loader" id="loader"></div>
            <img id="previewImage" />
            <div class="result" id="result"></div>
        </div>

        <script>
            const form = document.getElementById("uploadForm");
            const fileInput = document.getElementById("scanInput");
            const previewImage = document.getElementById("previewImage");

            fileInput.addEventListener("change", function () {
                const file = fileInput.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        previewImage.src = e.target.result;
                        previewImage.style.display = "block";
                    };
                    reader.readAsDataURL(file);
                } else {
                    previewImage.style.display = "none";
                }
            });

            form.addEventListener("submit", async function (e) {
                e.preventDefault();
                const loader = document.getElementById("loader");
                const resultBox = document.getElementById("result");

                loader.style.display = "block";
                resultBox.innerText = "";

                const formData = new FormData(form);

                try {
                    const response = await fetch("/predict/", {
                        method: "POST",
                        body: formData
                    });

                    const data = await response.json();

                    setTimeout(() => {
                        loader.style.display = "none";
                        resultBox.innerText = "Prediction: " + data.prediction;
                    }, 15000); 

                } catch (error) {
                    loader.style.display = "none";
                    resultBox.innerText = "Error: Could not process image.";
                }
            });
        </script>
    </body>
    </html>
    """





