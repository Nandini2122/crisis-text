# 🚨 Crisis Text — From Text to Timely Action

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.0-black?style=flat-square&logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> An AI-powered disaster message analysis platform that converts unstructured crisis text into structured emergency insights — instantly.

🌐 **Live Demo:** [https://crisis-text.onrender.com](https://crisis-text.onrender.com)

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Model Performance](#model-performance)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Team](#team)

---

## 📖 About the Project

During disasters, thousands of people post urgent messages on social media and messaging platforms requesting immediate help. These messages are **unstructured, scattered, and difficult to prioritize** — making it nearly impossible for emergency responders to manually read and route hundreds of messages under extreme time pressure.

**Crisis Text** solves this problem by automatically analyzing incoming disaster messages using Natural Language Processing and Machine Learning. The system:

- Predicts the **emergency severity level** (High / Medium)
- Detects the **location** mentioned in the message
- Identifies the **type of help required**
- Recommends the correct **disaster helpline number**

All in real time — converting raw, chaotic text into structured, actionable emergency intelligence.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌊 **Disaster Message Analysis** | Processes raw unstructured crisis messages using NLP |
| ⚠️ **Emergency Severity Detection** | Classifies messages as High or Medium severity |
| 📍 **Location Extraction** | Matches 801 Indian districts and cities |
| 📞 **Helpline Recommendation** | Routes to correct state SDMA helpline from 84 verified numbers |
| 📊 **Analytics Dashboard** | Visual charts showing disaster trends and patterns |
| 🎨 **Modern AI UI** | Dark theme dashboard with smooth animations |

---

## 🎬 Demo

### Analyze Page
Enter any disaster message and click **Analyze Crisis**

```
Input:  "Flood in Mumbai people trapped on rooftop need rescue immediately"

Output:
  Emergency Level  →  HIGH (84% confidence)
  Location         →  Mumbai
  Disaster Type    →  Flood
  Help Needed      →  Rescue
  Helpline         →  1070 (Maharashtra SDMA)
```

---

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Plus Jakarta Sans + JetBrains Mono fonts
- Custom dark AI dashboard UI

### Backend
- **Python 3.12**
- **Flask 3.1** — Web framework
- **pandas** — Data handling
- **openpyxl** — Excel file reading

### Machine Learning & NLP
- **scikit-learn** — Random Forest Classifier
- **TF-IDF Vectorizer** — Text feature extraction
- **NLTK** — Stopword removal, lemmatization
- **rapidfuzz** — Fuzzy location matching

### Deployment
- **GitHub** — Source code hosting
- **Render** — Free cloud deployment

---

## 📊 Dataset

| File | Description | Records |
|---|---|---|
| `dataset_1disasters.xlsx` | Historical disaster records 2000–2025 | 520 |
| `dataset_2messages.xlsx` | Labeled disaster messages | 520 |
| `dataset_3helplines.xlsx` | Verified helpline numbers | 84 |
| `states_districts.xlsx` | Indian districts for location lookup | 733 |
| `union_territories_cities.xlsx` | UT cities for location lookup | 68 |

### Disaster Types Covered
`Flood` `Storm` `Earthquake` `Landslide` `Fire` `Drought` `Heatwave` `Transport` `Industrial`

### Help Categories
`Rescue` `Ambulance` `Shelter` `Fire Brigade` `Hazmat` `Relief` `Medical`

---

## 📈 Model Performance

| Metric | Score |
|---|---|
| Accuracy | 78.8% |
| Precision | 78% |
| Recall | 79% |
| F1 Score | 78% |

**Model:** Random Forest Classifier (200 estimators)  
**Vectorizer:** TF-IDF (5000 max features)  
**Split:** 80% train / 20% test  

---

## 📁 Project Structure

```
crisis-text/
│
├── app.py                          # Flask backend
├── retrain.py                      # Model retraining script
├── requirements.txt                # Python dependencies
├── Procfile                        # Render deployment config
│
├── crisis_model.pkl                # Trained Random Forest model
├── tfidf_vectorizer.pkl            # Fitted TF-IDF vectorizer
│
├── dataset_1disasters.xlsx         # Historical disasters dataset
├── dataset_2messages.xlsx          # Crisis messages dataset
├── dataset_3helplines.xlsx         # Helplines database
├── states_districts.xlsx           # Indian districts lookup
├── union_territories_cities.xlsx   # UT cities lookup
│
├── templates/
│   └── index.html                  # Frontend (all 5 pages)
│
└── static/                         # Static assets (if any)
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/Nandini2122/crisis-text.git
cd crisis-text
```

**2. Create virtual environment**
```bash
python -m venv venv
```

**3. Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Download NLTK data**
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
```

**6. Retrain the model (first time only)**
```bash
python retrain.py
```

**7. Run the application**
```bash
python app.py
```

**8. Open in browser**
```
http://127.0.0.1:5000
```

---

## 🚀 Usage

**Home Page**
- Overview of the platform and key features

**Analyze Page**
- Enter any disaster-related message
- Click example pills to load sample messages
- Click **Analyze Crisis** to get results

**Results Page**
- View Emergency Level, Location, Disaster Type, Help Needed, Helpline Number

**Dashboard Page**
- View charts: Disaster Type Distribution, Emergency Level, Help Type, Word Cloud

**About Page**
- Project information, NLP techniques, model performance, team credits

---

## 👥 Team

| Role | Name |
|---|---|
| 👩‍💻 Development & System Implementation | Nandini Singh |
| 👩‍🔬 Data Collection & Research | Sakshi Sonawane |
| 👩‍📚 Documentation & Reporting | Vaishnavi Pawar |

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- National Disaster Management Authority (NDMA) India
- State Disaster Management Authorities (SDMA) across India
- scikit-learn and NLTK open source communities

---

<div align="center">
  <p>Made with ❤️ for disaster response in India</p>
  <p>© 2025 Crisis Text — From Text to Timely Action</p>
</div>
