# Part 2: Prediction with User Input (Models stored in the "model" folder)
import numpy as np
import joblib
import pickle
import statistics

# Load the saved models from the "model" folder
final_svm_model = joblib.load("train_model/final_svm_model.pkl")
final_nb_model = joblib.load("train_model/final_nb_model.pkl")
final_rf_model = joblib.load("train_model/final_rf_model.pkl")

# Load the data dictionary from the "model" folder
with open("train_model/data_dict.pkl", "rb") as f:
    data_dict = pickle.load(f)

def predictDisease(symptoms):
    # Split the input string by commas and remove extra spaces
    symptoms = [s.strip() for s in symptoms.split(",")]
    
    # Create the input vector (initialize all values to 0, then set 1 at the positions of the input symptoms)
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        # Format the symptom, e.g., "fever" -> "Fever"
        formatted_symptom = " ".join([word.capitalize() for word in symptom.split()])
        if formatted_symptom in data_dict["symptom_index"]:
            index = data_dict["symptom_index"][formatted_symptom]
            input_data[index] = 1
        else:
            print(f"Symptom '{symptom}' not recognized.")
    
    input_data = np.array(input_data).reshape(1, -1)
    
    # Make predictions using the individual models
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]
    
    # Final prediction based on majority voting (mode)
    final_prediction = statistics.mode([rf_prediction, nb_prediction, svm_prediction])
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
    }
    return predictions

# Interactive user input for symptoms
if __name__ == "__main__":
    print("Welcome to the Disease Prediction System!")
    user_symptoms = input("Please enter the symptoms (comma-separated): ")
    result = predictDisease(user_symptoms)
    
    print("\nPredictions:")
    for key, value in result.items():
        print(f"{key}: {value}")
