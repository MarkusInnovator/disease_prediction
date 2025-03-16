import { useState, useEffect } from "react";
import { fetchSymptoms } from "../services/api";
import "../styles/PredictionForm.css";

interface Props {
  onPredict: (symptoms: string[]) => void;
  loading: boolean;
}

export default function PredictionForm({ onPredict, loading }: Props) {
  const [symptoms, setSymptoms] = useState<string[]>([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getSymptoms = async () => {
      try {
        const data = await fetchSymptoms();
        setSymptoms(data.symptoms);
      } catch {
        setError("Error fetching symptoms");
      }
    };

    getSymptoms();
  }, []);

  const handleSymptomChange = (symptom: string) => {
    setSelectedSymptoms((prevSelectedSymptoms) =>
      prevSelectedSymptoms.includes(symptom)
        ? prevSelectedSymptoms.filter((s) => s !== symptom)
        : [...prevSelectedSymptoms, symptom]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (selectedSymptoms.length === 0) {
      setError("Please select at least one symptom.");
      return;
    }

    setError(null);
    onPredict(selectedSymptoms);
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} aria-label="Health Symptom Prediction Form">
        <div className="space-y-6">
          <label htmlFor="symptoms-input" className="form-title">
            Please Select Your Symptoms:
          </label>
          <div className="symptoms-list">
            {symptoms.map((symptom) => (
              <label key={symptom} className="symptom-item">
                <input
                  type="checkbox"
                  value={symptom}
                  onChange={() => handleSymptomChange(symptom)}
                  className="symptom-checkbox"
                />
                {symptom}
              </label>
            ))}
          </div>
          {error && (
            <p id="error-message" className="error-message">
              {error}
            </p>
          )}
        </div>
        <button
          type="submit"
          className="submit-button"
          disabled={loading}
        >
          {loading ? (
            <span className="loading-spinner">
              <svg
                className="animate-spin h-6 w-6 mr-2"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Processing...
            </span>
          ) : (
            "Predict Health Condition"
          )}
        </button>
      </form>
    </div>
  );
}