interface Prediction {
    rf_model_prediction: string;
    naive_bayes_prediction: string;
    svm_model_prediction: string;
    final_prediction: string;
  }
  
  interface Props {
    prediction: Prediction | null;
  }
  
  export default function PredictionResult({ prediction }: Props) {
    if (!prediction) return null;
  
    return (
      <div className="mt-4 p-3 border rounded">
        <h2 className="font-bold">Predictions:</h2>
        <p>Random Forest: {prediction.rf_model_prediction}</p>
        <p>Naive Bayes: {prediction.naive_bayes_prediction}</p>
        <p>SVM: {prediction.svm_model_prediction}</p>
        <p className="font-bold">Final Diagnosis: {prediction.final_prediction}</p>
      </div>
    );
  }
  