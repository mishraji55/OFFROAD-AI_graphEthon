## 🌐 API Documentation

### Endpoints Overview

```
GET  /              - Web interface
GET  /health        - Health check
POST /predict-image - Analyze single image
POST /predict-video - Analyze video frames
```

---

## 📡 Detailed Endpoints

### 1️⃣ GET `/`
**Main web interface**

```
URL: http://localhost:10000
Method: GET
Response: HTML page
```

---

### 2️⃣ GET `/health`
**Health check for monitoring**

```
URL: http://localhost:10000/health
Method: GET
Response: 
{
  "status": "ok"
}
Status: 200 OK
```

---

### 3️⃣ POST `/predict-image`
**Analyze a single image for terrain classification and segmentation**

#### Request
```
URL: http://localhost:10000/predict-image
Method: POST
Content-Type: multipart/form-data

Parameters:
- file (required): Image file (JPG, PNG, GIF, BMP)
  Max size: 10MB
```

#### cURL Example
```bash
curl -X POST -F "file=@terrain.jpg" \
  http://localhost:10000/predict-image
```

#### JavaScript Example
```javascript
let formData = new FormData();
formData.append("file", imageFile);

fetch("http://localhost:10000/predict-image", {
  method: "POST",
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

#### Python Example
```python
import requests

with open("terrain.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:10000/predict-image",
        files=files
    )
    print(response.json())
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "terrain": "Easy",
  "confidence": 94.2,
  "decision": "✓ GO STRAIGHT",
  "mask": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}
```

#### Error Response (400/500)
```json
{
  "success": false,
  "error": "Invalid file type. Use: JPG, PNG, GIF"
}
```

#### Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Request succeeded |
| terrain | string | Terrain difficulty: "Easy", "Moderate", "Rough", "Very Rough" |
| confidence | float | Confidence percentage (0-100) |
| decision | string | Navigation command with emoji |
| mask | string | Base64-encoded PNG segmentation mask |
| error | string | Error message (only on failure) |

---

### 4️⃣ POST `/predict-video`
**Analyze multiple frames from a video**

#### Request
```
URL: http://localhost:10000/predict-video
Method: POST
Content-Type: multipart/form-data

Parameters:
- file (required): Video file (MP4, AVI, MOV, etc.)
```

#### Success Response
```json
{
  "success": true,
  "frame_predictions": [
    "✓ GO STRAIGHT",
    "← TURN LEFT",
    "✓ GO STRAIGHT"
  ],
  "final_decision": "✓ GO STRAIGHT"
}
```

---

## 🎨 Response Format Details

### Terrain Classes
```
"Easy"       - Open terrain, safe to traverse
"Moderate"   - Some obstacles, proceed with caution
"Rough"      - Many obstacles, difficult
"Very Rough" - Extremely challenging, should avoid
```

### Navigation Decisions
```
"✓ GO STRAIGHT"  - Safe to proceed forward
"← TURN LEFT"    - Recommend turning left
"→ TURN RIGHT"   - Recommend turning right
"🛑 STOP"        - Dangerous, do not proceed
```

### Segmentation Mask
- Base64-encoded PNG image
- Same size as input (resized internally)
- Binary mask: 1 = traversable, 0 = obstacle
- Decode in frontend: `data:image/png;base64,{mask}`

---

## 🔄 Request/Response Flow

```
Client             Server
  |                  |
  |-- POST image --> |
  |                  | Load model (if first time)
  |                  | Classify terrain
  |                  | Generate segmentation
  |                  | Compute decision
  |<- JSON response--|
  |                  |
  Display results
```

---

## ⚙️ Integration Examples

### React Component
```jsx
const [loading, setLoading] = useState(false);
const [result, setResult] = useState(null);

const uploadImage = async (file) => {
  setLoading(true);
  const formData = new FormData();
  formData.append("file", file);
  
  const res = await fetch("http://localhost:10000/predict-image", {
    method: "POST",
    body: formData
  });
  
  const data = await res.json();
  setResult(data);
  setLoading(false);
};
```

### Vue Components
```vue
<script>
export default {
  methods: {
    async predictImage(file) {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('http://localhost:10000/predict-image', {
        method: 'POST',
        body: formData
      });
      
      this.prediction = await response.json();
    }
  }
}
</script>
```

### Django Integration
```python
import requests

def analyze_terrain(image_file):
    url = "http://localhost:10000/predict-image"
    files = {"file": image_file}
    response = requests.post(url, files=files)
    return response.json()
```

---

## 🛡️ Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 400 - "No file provided" | Missing file | Include file in request |
| 400 - "Invalid file type" | Wrong format | Use JPG, PNG, GIF |
| 400 - "Empty filename" | Empty file | Upload actual file |
| 500 - "Classifier model failed" | Model not loaded | Restart server |
| 500 - "UNet model failed" | Model load error | Check dependencies |
| 500 - "Model file not found" | Missing `.pth` file | Ensure model in root |

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| First Request | 5-10 sec (model load) |
| Subsequent | 2-3 sec (CPU) |
| Memory Usage | ~1.5GB peak |
| Model Size | ~50MB |
| Typical Image Size | <5MB |

---

## 🔐 API Constraints

- **Max file size:** 10MB
- **Timeout:** 30 seconds per request
- **Concurrent requests:** Limited by system memory
- **Rate limiting:** None (add if needed)
- **Authentication:** None required (add if needed)

---

## 🚀 Production Deployment

For production, add:

```python
# Rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

# Authentication
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# Logging
import logging
logging.basicConfig(level=logging.INFO)

# HTTPS
# Use gunicorn with SSL certificates
# gunicorn --certfile=cert.pem --keyfile=key.pem app:app
```

---

**All endpoints are ready for integration! 🎉**
