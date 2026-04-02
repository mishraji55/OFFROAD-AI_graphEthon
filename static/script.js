let selectedFile = null;

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultsSection = document.getElementById("resultsSection");
const metricsSection = document.getElementById("metricsSection");
const errorBox = document.getElementById("errorBox");
const loadingState = document.getElementById("loadingState");

// File input handling
fileInput.addEventListener("change", (e) => {
    selectedFile = e.target.files[0];
    handleFileSelect(selectedFile);
});

// Drop zone handling
dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
        selectedFile = file;
        handleFileSelect(file);
    } else {
        showError("Please drop an image file");
    }
});

// Handle file selection
function handleFileSelect(file) {
    // Validate file
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        showError("File size must be less than 10MB");
        return;
    }

    if (!file.type.startsWith("image/")) {
        showError("Please select a valid image file");
        return;
    }

    // Preview
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById("preview").src = e.target.result;
        analyzeBtn.style.display = "inline-block";
        errorBox.style.display = "none";
    };
    reader.readAsDataURL(file);
}

// Show error message
function showError(message) {
    errorBox.textContent = "❌ " + message;
    errorBox.style.display = "block";
    analyzeBtn.style.display = "none";
}

// Show loading state
function setLoading(isLoading) {
    loadingState.style.display = isLoading ? "block" : "none";
    analyzeBtn.disabled = isLoading;
    if (isLoading) {
        analyzeBtn.textContent = "Processing...";
    } else {
        analyzeBtn.textContent = "Analyze Terrain";
    }
}

// Predict function
async function predict() {
    if (!selectedFile) {
        showError("Please select an image first");
        return;
    }

    setLoading(true);
    errorBox.style.display = "none";

    try {
        const formData = new FormData();
        formData.append("file", selectedFile);

        const response = await fetch("/predict-image", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || "Prediction failed");
        }

        // Display results
        displayResults(data);

    } catch (error) {
        showError(error.message || "Error processing image. Please try again.");
        console.error("Prediction error:", error);
    } finally {
        setLoading(false);
    }
}

// Display results
function displayResults(data) {
    // Show mask image
    if (data.mask) {
        document.getElementById("maskPreview").src = "data:image/png;base64," + data.mask;
    }

    // Update metrics
    document.getElementById("terrain").textContent = data.terrain || "--";
    document.getElementById("confidence").textContent = (data.confidence || 0) + "%";
    document.getElementById("decision").textContent = data.decision || "--";

    // Show sections
    resultsSection.style.display = "block";
    metricsSection.style.display = "block";

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }, 100);
}