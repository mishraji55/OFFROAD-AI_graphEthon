# ⚡ Quick Start Guide

## 🚀 In 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Model File
Make sure `terrain_classifier.pth` is in the project root folder

### Step 3: Run the App

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
bash run.sh
```

**Or manually:**
```bash
python app.py
```

---

## 🌐 Open Web App
Once running, open your browser and go to:
```
http://localhost:10000
```

---

## 📋 What Should Happen

✅ Flask server starts and listens on port 10000  
✅ Models load on first request (5-10 seconds)  
✅ Web interface loads at http://localhost:10000  
✅ You can upload images and get predictions  

---

## ❌ If Something Goes Wrong

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "terrain_classifier.pth not found"
- Download/check if the model file exists in project root
- Check file name exactly matches

### "Port 10000 already in use"
- Edit `app.py` line 163: change `port=10000` to any free port
- Or kill the process using port 10000

### App is very slow on first request
- First request loads models (~5-10 seconds) - this is normal
- Subsequent requests are faster

---

## ✨ Features

✅ Drag-and-drop image upload  
✅ Real-time terrain classification  
✅ Semantic segmentation mask  
✅ Navigation decision  
✅ Confidence scores  
✅ Error handling  
✅ Mobile responsive  

---

## 📦 Files Structure

```
project-root/
├── app.py                    # Flask backend
├── video.py                  # Video processing
├── requirements.txt          # Dependencies
├── terrain_classifier.pth    # Pre-trained model
├── run.bat                   # Windows startup
├── run.sh                    # Linux/Mac startup
├── DEPLOY.md                 # Deployment guide
├── QUICKSTART.md             # This file
├── templates/
│   └── index.html            # Web interface
└── static/
    ├── script.js             # Frontend logic
    └── style.css             # Styling
```

---

## 🔧 System Requirements

- **CPU:** Any modern processor
- **RAM:** 4GB minimum
- **Storage:** 500MB
- **OS:** Windows, Linux, or Mac
- **Python:** 3.8+

---

## 🎯 Next Steps

1. ✅ Get the app running locally
2. 📸 Test with sample images
3. 🔍 Check output quality
4. 🚀 Deploy to production (see DEPLOY.md)

---

## 📞 Troubleshooting Resources

- **DEPLOY.md** - Advanced deployment options
- **README.md** - Project overview
- **app.py** - Backend code with comments

---

**Ready? Run `python app.py` and start analyzing terrain! 🚀**
