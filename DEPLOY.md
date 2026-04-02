# 🚀 Deployment Guide - Offroad AI Web App

## Quick Start (Local Machine)

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Ensure Model Files Exist**
- `terrain_classifier.pth` - Must be in project root
- This file is loaded lazily on first request

### 3. **Run the App**
```bash
python app.py
```

**The app will be live at:** `http://localhost:10000`

---

## Deployment Options

### Option A: **Local CPU (Recommended for Testing)**

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

✅ Runs on CPU without GPU  
✅ Works on Windows, Linux, Mac  
✅ No additional setup needed

---

### Option B: **Google Colab (Free GPU)**

```python
# In Colab notebook:

# 1. Clone repo (if using git)
# !git clone <your-repo-url>
# %cd OFFROAD-AI_graphEthon

# 2. Install dependencies
!pip install -r requirements.txt

# 3. Run Flask with ngrok tunnel
!pip install pyngrok
from pyngrok import ngrok
ngrok.connect(10000)

# 4. Run app
!python app.py
```

---

### Option C: **Heroku Deployment**

1. **Create `Procfile`:**
```
web: gunicorn app:app
```

2. **Update `requirements.txt` (done ✅)**

3. **Deploy:**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

---

### Option D: **Docker Container**

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["python", "app.py"]
```

Build & Run:
```bash
docker build -t offroad-ai .
docker run -p 10000:10000 offroad-ai
```

---

## ✅ Deployment Checklist

- [ ] `terrain_classifier.pth` exists in project root
- [ ] `requirements.txt` is up-to-date
- [ ] `app.py` runs without errors
- [ ] Flask is listening on `0.0.0.0:10000`
- [ ] Frontend loads at `http://localhost:10000`
- [ ] Image upload works
- [ ] Predictions complete without errors

---

## Troubleshooting

### "terrain_classifier.pth not found"
- Ensure the model file is in the project root directory
- Check file path matches exactly

### Port 10000 already in use
```bash
# Change port in app.py:
app.run(host="0.0.0.0", port=5000)  # or any free port
```

### CORS errors
- CORS is already enabled in `app.py`
- Should work for all origins

### Model too slow
- Using MobileNetV2 encoder (lightweight)
- CPU inference ~2-3 seconds per image
- GPU deployment would be faster

---

## Performance Notes

- **Model Load Time:** ~5-10 seconds (first request only, then cached)
- **Inference Time:** ~2-3 seconds per image (CPU)
- **Memory Usage:** ~1.5GB during inference
- **Best on:** CPU with 4GB RAM minimum

---

## API Endpoints

### `GET /` 
Main web interface

### `GET /health`
Health check
```json
{"status": "ok"}
```

### `POST /predict-image`
Analyze single image

**Request:**
```
Content-Type: multipart/form-data
file: <image_file>
```

**Response:**
```json
{
  "success": true,
  "terrain": "Easy",
  "confidence": 94.2,
  "decision": "✓ GO STRAIGHT",
  "mask": "<base64_encoded_image>"
}
```

### `POST /predict-video`
Analyze video frames

---

## Environment Variables

Optional (already set in code):
```
FLASK_ENV=production
FLASK_DEBUG=False
```

---

**Need help?** Check the main README.md for project details.
