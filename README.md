# AI Integrity Shield: Fake News & Deepfake Detection Platform

A complete, lightweight, and functional full-featured application designed for multi-modal verification of news text and visual media. Built for AI/ML security research, academic demonstrations, and journalistic media forensics.

![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
![Framework](https://img.shields.io/badge/framework-Streamlit-red)
![ML Core](https://img.shields.io/badge/ML-Scikit--Learn%20%7C%20FFT%20Forensics-green)

---

## 🌟 Modules & Features

### 1. 📰 Fake News & Misinformation Detection Module
* **NLP Classification Pipeline**: TF-IDF (1-2 ngrams) + calibrated Logistic Regression model.
* **Linguistic Heuristic Analyzer**: Scans for clickbait vocabulary (*"shocking"*, *"secret"*, *"miracle"*), uppercase shouting ratios, and emotional punctuation.
* **Interactive Token Highlighting**: Color-codes text directly in the UI (🔴 red for sensationalist terms, 🟢 green for credibility anchors, 🟠 orange for excessive capitalization).
* **Exportable Reports**: Generate instant downloadable JSON and formatted printable HTML audit reports.

### 2. 🔍 Deepfake & Image Manipulation Forensics Module
* **Error Level Analysis (ELA)**: Detects localized compression variances and copy-move splices, outputting an ELA heatmap.
* **2D Fast Fourier Transform (FFT)**: Performs frequency spectrum decomposition to detect generative lattice artifacts typical of diffusion and GAN models.
* **EXIF & Header Integrity Audit**: Inspects camera hardware tags vs editing software signatures (Photoshop, Canva, Midjourney, etc.).
* **Laplacian Noise Analysis**: Measures edge variance to identify synthetic blurring or deepfake skin smoothing.
* **Exportable Reports**: Download structured forensic reports in JSON and HTML.

### 3. 🌐 Multi-Modal Unified Check Module
* Cross-examines textual claims together with attached lead images.
* Produces a unified **Holistic Media Integrity Score (0-100)** and a synthesized cross-modal risk assessment.

### 4. ⚡ Live Model Retraining Suite
* Retrain or fine-tune the classifier directly from the browser using custom CSV datasets.
* Includes downloadable template CSV format.

---

## 📁 Project Directory Structure

```text
Fake News and Deepfake -AIML/
│
├── app.py                     # Streamlit frontend & interactive dashboard
├── nlp_detector.py            # TF-IDF + Logistic Regression NLP classification & token highlighter
├── deepfake_detector.py       # ELA, 2D FFT, and metadata forensic image analysis engine
├── report_generator.py        # Export engine for JSON and HTML audit reports
├── requirements.txt           # Project dependencies
├── generate_samples.py        # Sample generator script for instant testing
├── test_modules.py            # Unit test suite verifying all modules
│
└── samples/                   # Pre-bundled test snippets and images
    ├── sample_articles.json   # Sample credible & fake news test snippets
    ├── authentic_sample.jpg   # Sample authentic photograph with EXIF
    ├── manipulated_sample.jpg # Sample spliced image with editing software tag
    └── synthetic_sample.jpg   # Sample synthetic pattern with Fourier artifacts
```

---

## 🚀 Quickstart Guide

### 1. Activate Environment & Run
```bash
# Activate virtual environment
source venv/bin/activate

# Launch the Streamlit application
streamlit run app.py --server.port=8505
```

Open your browser at `http://localhost:8505`.

### 2. Run Automated Tests
```bash
source venv/bin/activate
python test_modules.py
```
*(All tests verify NLP accuracy, forensic metrics, and error handling for corrupt inputs)*
