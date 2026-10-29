const form = document.getElementById("prediction-form");
const predictButton = document.getElementById("predict-button");
const emptyResult = document.getElementById("empty-result");
const resultContent = document.getElementById("result-content");
const errorBox = document.getElementById("error-box");
let predictionCount = 0;

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  window.setTimeout(() => toast.classList.remove("show"), 2800);
}

async function refreshHealth() {
  const topStatus = document.getElementById("top-status");
  const apiMetric = document.getElementById("api-metric");
  const modelMetric = document.getElementById("model-metric");
  const apiDetail = document.getElementById("api-detail");
  const modelDetail = document.getElementById("model-detail");
  const apiDot = document.getElementById("api-dot");
  const modelDot = document.getElementById("model-dot");
  const backendState = document.getElementById("backend-state");
  const savedModelState = document.getElementById("saved-model-state");
  try {
    const response = await fetch("/health", { cache: "no-store" });
    if (!response.ok) throw new Error(`Health endpoint returned ${response.status}`);
    const data = await response.json();
    topStatus.textContent = "API connected";
    document.querySelector(".pulse").classList.add("online");
    apiMetric.textContent = "Online";
    apiDetail.textContent = "FastAPI responding";
    apiDot.className = "status-dot good";
    backendState.textContent = "Online";
    backendState.className = "system-state good";
    const ready = Boolean(data.model_ready);
    modelMetric.textContent = ready ? "Ready" : "Missing";
    modelDetail.textContent = ready ? "Saved model detected" : "Train the model first";
    modelDot.className = `status-dot ${ready ? "good" : "bad"}`;
    savedModelState.textContent = ready ? "Ready" : "Missing";
    savedModelState.className = `system-state ${ready ? "good" : "bad"}`;
  } catch (error) {
    topStatus.textContent = "API unavailable";
    document.querySelector(".pulse").classList.remove("online");
    apiMetric.textContent = "Offline";
    apiDetail.textContent = "Start the FastAPI server";
    apiDot.className = "status-dot bad";
    modelMetric.textContent = "Unknown";
    modelDetail.textContent = "API could not be reached";
    modelDot.className = "status-dot bad";
    backendState.textContent = "Offline";
    backendState.className = "system-state bad";
    savedModelState.textContent = "Unknown";
    savedModelState.className = "system-state";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.classList.add("hidden");
  const formData = new FormData(form);
  const payload = {
    tenure: Number(formData.get("tenure")),
    monthly_charges: Number(formData.get("monthly_charges")),
    total_charges: Number(formData.get("total_charges")),
    contract: formData.get("contract"),
    internet_service: formData.get("internet_service"),
    tech_support: formData.get("tech_support"),
    online_security: formData.get("online_security"),
    payment_method: formData.get("payment_method"),
    paperless_billing: formData.get("paperless_billing"),
    senior_citizen: Number(formData.get("senior_citizen")),
    partner: formData.get("partner"),
    dependents: formData.get("dependents")
  };

  predictButton.disabled = true;
  predictButton.innerHTML = '<span class="button-spark">◌</span> Predicting…';
  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) {
      const detail = typeof result.detail === "string" ? result.detail : JSON.stringify(result.detail || result);
      throw new Error(detail || `Request failed (${response.status})`);
    }
    renderResult(result);
    predictionCount += 1;
    document.getElementById("prediction-count").textContent = String(predictionCount);
    document.getElementById("last-risk").textContent = result.risk_level;
    document.getElementById("last-risk-detail").textContent = `${(Number(result.churn_probability) * 100).toFixed(1)}% probability`;
    showToast("Prediction completed successfully.");
  } catch (error) {
    emptyResult.classList.add("hidden");
    resultContent.classList.add("hidden");
    errorBox.textContent = `Could not generate prediction: ${error.message}. Check that the API is running and the saved model exists.`;
    errorBox.classList.remove("hidden");
    showToast("Prediction failed. Check the error message.");
  } finally {
    predictButton.disabled = false;
    predictButton.innerHTML = '<span class="button-spark">✦</span> Predict churn <span class="button-arrow">→</span>';
  }
});

function renderResult(result) {
  const prediction = String(result.churn_prediction || "Unknown");
  const probability = Math.max(0, Math.min(1, Number(result.churn_probability) || 0));
  const risk = String(result.risk_level || "Unknown");
  emptyResult.classList.add("hidden");
  errorBox.classList.add("hidden");
  resultContent.classList.remove("hidden");
  const word = document.getElementById("prediction-word");
  word.textContent = prediction;
  word.className = `prediction-word ${prediction.toLowerCase() === "yes" ? "yes" : "no"}`;
  document.getElementById("prediction-caption").textContent =
    prediction.toLowerCase() === "yes" ? "This customer is predicted to churn." : "This customer is not predicted to churn.";
  document.getElementById("probability-number").textContent = `${(probability * 100).toFixed(1)}%`;
  document.getElementById("probability-bar").style.width = `${probability * 100}%`;
  document.getElementById("risk-level").textContent = `${risk} risk`;
  document.getElementById("risk-pill").textContent = risk;
  const riskBox = document.getElementById("risk-box");
  riskBox.className = `risk-box ${risk.toLowerCase()}`;
}

document.getElementById("refresh-status").addEventListener("click", async () => {
  await refreshHealth();
  showToast("System status refreshed.");
});
document.getElementById("reset-button").addEventListener("click", () => {
  window.setTimeout(() => showToast("Form reset to its default values."), 0);
});
refreshHealth();
