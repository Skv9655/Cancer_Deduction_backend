# Cancer Deduction Backend

This is the backend API for the Cancer Deduction AI project. It uses FastAPI to serve a trained XGBoost machine learning model that predicts whether a breast cancer tumor is Malignant or Benign based on 15 core features.

## Tech Stack
- **Python 3**
- **FastAPI**: High-performance web framework.
- **Uvicorn**: ASGI server.
- **XGBoost & Scikit-learn**: Machine learning model and preprocessing.
- **Pandas**: Data handling.

## Installation & Setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the API server using Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### `POST /predict`
Accepts a JSON payload containing the 15 tumor features and returns a prediction.
- If features are omitted, the API uses predefined mean values.
- **Returns**: A JSON object containing the `prediction` (Malignant/Benign), `prediction_code` (1/0), and confidence `probability`.
