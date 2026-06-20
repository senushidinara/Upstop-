const API_BASE = window.API_BASE || "http://127.0.0.1:8000"; // override via window.API_BASE in production

const fileInput = document.getElementById("fileInput");
const predictBtn = document.getElementById("predictBtn");
const statusEl = document.getElementById("status");

const resultCard = document.getElementById("resultCard");
const explainCard = document.getElementById("explainCard");
const riskScoreEl = document.getElementById("riskScore");
const riskLevelEl = document.getElementById("riskLevel");
const explanationsEl = document.getElementById("explanations");

predictBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    statusEl.textContent = "Please select a CSV file first.";
    return;
  }

  statusEl.textContent = "Uploading and predicting...";
  resultCard.hidden = true;
  explainCard.hidden = true;
  explanationsEl.innerHTML = "";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Prediction failed.");
    }

    riskScoreEl.textContent = data.risk_score;
    riskLevelEl.textContent = data.risk_level;

    const factors = data.explanations?.all_factors || [];
    for (const f of factors) {
      const li = document.createElement("li");
      li.textContent = `${f.feature}: contribution ${f.contribution} (${f.interpretation})`;
      explanationsEl.appendChild(li);
    }

    resultCard.hidden = false;
    explainCard.hidden = false;
    statusEl.textContent = "Prediction completed successfully.";
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
  }
});