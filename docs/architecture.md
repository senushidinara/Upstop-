# NeuroGuard AI Architecture (MVP)

## Data Flow
1. User uploads EEG CSV from frontend.
2. Backend validates schema.
3. Aggregated feature vector is generated.
4. Risk score inference runs in model layer.
5. SHAP-style explanation summary is produced.
6. Frontend displays risk + explanation list.

## Next Steps (Production)
- Replace heuristic model with trained CNN-Transformer checkpoint.
- Add real SHAP integration (e.g., shap.DeepExplainer with PyTorch model).
- Add authentication + patient profile storage.
- Add longitudinal charting with PostgreSQL/Firebase.
- Add clinician report export (PDF).