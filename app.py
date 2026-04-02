from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
import torchvision.transforms as T
import torch.nn.functional as F
import numpy as np
from PIL import Image
import tempfile
import io
import base64
import os
from pathlib import Path

from video import sample_video_frames

app = Flask(__name__)
CORS(app)

# ================= CONFIG =================

CLASSES = ["Easy", "Moderate", "Rough", "Very Rough"]

clf_tf = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor()
])

seg_tf = T.Compose([
    T.Resize((256, 256)),
    T.ToTensor(),
    T.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ================= LAZY LOAD MODELS =================

clf_model = None
unet_model = None
model_load_error = None


def load_classifier():
    global clf_model, model_load_error

    if clf_model is None:
        try:
            import torchvision.models as models

            clf_model = models.resnet18(weights=None)
            clf_model.fc = torch.nn.Linear(clf_model.fc.in_features, 4)

            model_path = "terrain_classifier.pth"
            if not os.path.exists(model_path):
                model_load_error = f"Model file not found: {model_path}"
                return None

            clf_model.load_state_dict(
                torch.load(model_path, map_location="cpu")
            )
            clf_model.eval()
        except Exception as e:
            model_load_error = str(e)
            clf_model = None
            return None

    return clf_model


def load_unet():
    global unet_model, model_load_error

    if unet_model is None:
        try:
            import segmentation_models_pytorch as smp

            unet_model = smp.Unet(
                encoder_name="mobilenet_v2",
                encoder_weights="imagenet",
                in_channels=3,
                classes=1,
                activation=None
            )
            unet_model.eval()
        except Exception as e:
            model_load_error = str(e)
            unet_model = None
            return None

    return unet_model


# ================= CORE LOGIC =================

def classify_terrain(img):
    model = load_classifier()
    if model is None:
        raise Exception("Classifier model failed to load")

    x = clf_tf(img).unsqueeze(0)

    with torch.no_grad():
        probs = F.softmax(model(x), dim=1)[0]
        idx = torch.argmax(probs).item()

    return CLASSES[idx], float(probs[idx] * 100)


def unet_segment(img):
    model = load_unet()
    if model is None:
        raise Exception("UNet model failed to load")

    x = seg_tf(img).unsqueeze(0)

    with torch.no_grad():
        logits = model(x)
        probs = torch.sigmoid(logits)
        probs = probs.squeeze().cpu().numpy()

    mask = (probs > 0.5).astype(np.uint8)
    return mask



def split_zones(mask):
    h, w = mask.shape
    return (
        mask[:, :w//3],
        mask[:, w//3:2*w//3],
        mask[:, 2*w//3:]
    )


def free_ratio(zone):
    total = zone.size
    if total == 0:
        return 0
    return np.sum(zone == 1) / total


def navigation_decision(mask, terrain_label):
    left, front, right = split_zones(mask)
    lf, ff, rf = free_ratio(left), free_ratio(front), free_ratio(right)

    if terrain_label == "Very Rough":
        decision = "🛑 STOP"
    elif ff < 0.3:
        decision = "← TURN LEFT" if lf > rf else "→ TURN RIGHT"
    else:
        decision = "✓ GO STRAIGHT"

    return decision


# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


@app.route("/predict-image", methods=["POST"])
def predict_image():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        # Validate file
        allowed_ext = {"jpg", "jpeg", "png", "gif", "bmp"}
        if not any(file.filename.lower().endswith(ext) for ext in allowed_ext):
            return jsonify({"error": "Invalid file type. Use: JPG, PNG, GIF"}), 400

        img = Image.open(file).convert("RGB")

        # Run predictions
        terrain, conf = classify_terrain(img)
        mask = unet_segment(img)
        decision = navigation_decision(mask, terrain)

        # Convert mask to base64
        mask_img = Image.fromarray(mask * 255)
        buffered = io.BytesIO()
        mask_img.save(buffered, format="PNG")
        mask_base64 = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            "success": True,
            "terrain": terrain,
            "confidence": round(conf, 2),
            "decision": decision,
            "mask": mask_base64
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route("/predict-video", methods=["POST"])
def predict_video():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file.save(temp.name)
            frames = sample_video_frames(temp.name)

            if not frames:
                return jsonify({"error": "No frames extracted from video"}), 400

            decisions = []
            for frame in frames:
                terrain, _ = classify_terrain(frame)
                mask = unet_segment(frame)
                decision = navigation_decision(mask, terrain)
                decisions.append(decision)

            final_decision = max(set(decisions), key=decisions.count)

            return jsonify({
                "success": True,
                "frame_predictions": decisions,
                "final_decision": final_decision
            })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
