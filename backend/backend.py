from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pickle
import statistics

app = FastAPI()

# Enable CORS (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models and data dictionary
final_svm_model = joblib.load("train_model/final_svm_model.pkl")
final_nb_model = joblib.load("train_model/final_nb_model.pkl")
final_rf_model = joblib.load("train_model/final_rf_model.pkl")

with open("train_model/data_dict.pkl", "rb") as f:
    data_dict = pickle.load(f)

# ✅ Define expected request body format
class SymptomsInput(BaseModel):
    symptoms: list[str]  # FastAPI will check this format

# Function to predict disease
def predictDisease(symptoms: list[str]):
    symptoms = [s.strip().capitalize() for s in symptoms]

    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        if symptom in data_dict["symptom_index"]:
            index = data_dict["symptom_index"][symptom]
            input_data[index] = 1

    input_data = np.array(input_data).reshape(1, -1)

    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]

    final_prediction = statistics.mode([rf_prediction, nb_prediction, svm_prediction])

    return {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
    }

# ✅ API endpoint that expects { "symptoms": ["Cough", "Fever"] }
@app.post("/predict")
async def predict(input_data: SymptomsInput):
    result = predictDisease(input_data.symptoms)
    return result
