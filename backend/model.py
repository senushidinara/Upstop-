import math

def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

def predict_risk(features: dict):
    """
    Lightweight proxy model for MVP demo.
    Replace with trained CNN-Transformer inference in production.
    """
    z = (
        1.2 * features["theta_power"]
        - 1.0 * features["alpha_power"]
        + 1.1 * features["spectral_entropy"]
        + 0.8 * features["signal_variance"]
        + 0.4 * features["delta_power"]
        + 0.3 * features["beta_power"]
        - 1.5
    )

    risk_score = _sigmoid(z)

    if risk_score < 0.35:
        risk_level = "Low"
    elif risk_score < 0.65:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    return risk_score, risk_level