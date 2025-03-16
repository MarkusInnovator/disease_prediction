import "../styles/PredictionResult.css";

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

  const modelPredictions = [
    { name: "Random Forest", value: prediction.rf_model_prediction },
    { name: "Naive Bayes", value: prediction.naive_bayes_prediction },
    { name: "Support Vector Machine", value: prediction.svm_model_prediction },
  ];

  return (
    <div 
      className="prediction-container"
      role="region" 
      aria-label="Disease prediction results"
    >
      {/* Header */}
      <div className="header">
        <h2 className="title">
          Diagnostic Predictions
        </h2>
      </div>

      {/* Model Predictions */}
      <div className="content">
        <div className="model-predictions">
          {modelPredictions.map((model) => (
            <div 
              key={model.name}
              className="model-prediction"
            >
              <div className="model-name">
                {model.name}
              </div>
              <div className="model-value">
                {model.value}
              </div>
            </div>
          ))}
        </div>

        {/* Final Prediction */}
        <div className="final-prediction">
          <div className="final-prediction-content">
            <span className="final-prediction-title">
              Final Diagnosis
            </span>
            <span 
              className="final-prediction-value"
              aria-label={`Final diagnosis: ${prediction.final_prediction}`}
            >
              {prediction.final_prediction}
            </span>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="disclaimer">
        <p className="disclaimer-text">
          This prediction is based on machine learning models and should be confirmed by a healthcare professional.
        </p>
      </div>
    </div>
  );
}