def generate_explanations(features: dict, risk_score: float):
    """
    SHAP-style explanation mock for MVP.
    Returns directional contribution estimate per feature.
    """
    baseline = {
        "delta_power": 0.5,
        "theta_power": 0.5,
        "alpha_power": 0.5,
        "beta_power": 0.5,
        "signal_variance": 0.5,
        "spectral_entropy": 0.5,
    }

    weights = {
        "delta_power": 0.4,
        "theta_power": 1.2,
        "alpha_power": -1.0,
        "beta_power": 0.3,
        "signal_variance": 0.8,
        "spectral_entropy": 1.1,
    }

    explanations = []
    for key, value in features.items():
        contribution = (value - baseline[key]) * weights[key]
        direction = "increases risk" if contribution >= 0 else "reduces risk"
        explanations.append({
            "feature": key,
            "value": round(float(value), 4),
            "contribution": round(float(contribution), 4),
            "interpretation": direction
        })

    explanations.sort(key=lambda x: abs(x["contribution"]), reverse=True)

    summary = {
        "model_output_risk_score": round(float(risk_score), 4),
        "top_factors": explanations[:3],
        "all_factors": explanations
    }
    return summary