import { useState } from "react";

interface Props {
  onPredict: (symptoms: string[]) => void;
  loading: boolean;
}

export default function PredictionForm({ onPredict, loading }: Props) {
  const [symptoms, setSymptoms] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onPredict(symptoms.split(",").map(s => s.trim()));
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded shadow">
      <input
        type="text"
        placeholder="Enter symptoms, separated by commas"
        value={symptoms}
        onChange={(e) => setSymptoms(e.target.value)}
        className="border p-2 w-full rounded"
      />
      <button
        type="submit"
        className="mt-4 bg-blue-500 text-white p-2 w-full rounded hover:bg-blue-700"
        disabled={loading}
      >
        {loading ? "Loading..." : "Get Prediction"}
      </button>
    </form>
  );
}
