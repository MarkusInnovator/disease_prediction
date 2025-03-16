export const fetchPrediction = async (symptoms: string[]) => {
  const requestBody = JSON.stringify({ symptoms });  // ✅ Ensures correct format
  
  console.log("Sending request:", requestBody);  // 🔍 Debugging step

  const response = await fetch("http://localhost:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: requestBody,  // ✅ Correct JSON structure
    mode: "cors",
  });

  if (!response.ok) {
    throw new Error("Error fetching prediction");
  }

  return response.json();
};

export const fetchSymptoms = async () => {
  const response = await fetch("http://localhost:8000/symptoms", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    mode: "cors",
  });

  if (!response.ok) {
    throw new Error("Error fetching symptoms");
  }

  return response.json();
};