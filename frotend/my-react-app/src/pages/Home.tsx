import { useState } from "react";
import PredictionForm from "../components/PredictionForm";
import PredictionResult from "../components/PredictionResult";
import { fetchPrediction } from "../services/api";

export default function Home() {
  
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async (symptoms: string[]) => {
    
    setLoading(true);
    setError(null);
    setPrediction(null);
    
    try {
      const data = await fetchPrediction(symptoms);
      setPrediction(data);
    } catch (err) {
      setError((err as Error).message);
    }

    setLoading(false);
  };

  return (
    <div className="max-w-lg mx-auto p-4 shadow-lg rounded-xl bg-white mt-10">
        <PredictionForm onPredict={handlePredict} loading={loading} />
      {error && <p className="text-red-500 mt-2">{error}</p>}
      <PredictionResult prediction={prediction} />
    </div>
  );
}
