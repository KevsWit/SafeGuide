# 🧭 SafeGuide

**SafeGuide** is an interactive travel guide designed to help people understand the status of tourist destinations in Ecuador by incorporating crime data, hazardous events, and tourist site information. The platform provides clear visualizations and a smart assistant to help travelers make safer, data-driven decisions.

---

## 📌 Project Overview

The main idea of SafeGuide is to develop a web-based application that provides reliable and up-to-date information about tourist destinations using a generative AI (Gemini) and official datasets. Travelers can use the app to:

- Explore Ecuador's safest and most interesting destinations.
- Identify areas with higher risk due to crime or dangerous events.
- Get personalized recommendations using a conversational chatbot.

---

### 🔐 Safety and Prevention

- **Crime maps and dangerous zones**: Visualize provinces and cantons with high crime rates, based on homicide data.
- **Disaster and event tracking**: A dashboard based on SGR data shows past incidents like mass disturbances and intoxications.
- **Real-time alerts (planned)**: Integrate up-to-date alerts using official data sources.

---

### 📍 Places to Visit

- **Interactive maps**: See markers for tourist attractions and dangerous events.
- **Customized suggestions**: Based on travel profiles (family, cultural, adventurous, etc.).
- **Conversational AI**: Ask about the best places to visit, safety considerations, or travel ideas.

---

## 💻 Current Features

### 📊 Dashboards

Built with Dash and Folium, the app includes:

#### 🔎 Homicide Dashboard
- Filter data by **province** and **type of death**.
- View histograms segmented by weapon and gender.

#### ⚠️ Hazardous Events Dashboard (SGR)
- Filter by **event type** (e.g., “Intoxicación”, “Perturbación en eventos masivos”).
- Histogram showing event frequency by province and canton.

#### 🗺️ Interactive Maps
- **Tourist attractions**: Displayed in green.
- **Dangerous events**: Displayed in red, filtered by type.
- Easy navigation for visual risk assessment and planning.

---

### 🤖 AI Chatbot (Integrated with Gemini AI)

- Built into the Dash app interface.
- Responds to user questions about:
  - Safety of cities or provinces
  - Travel suggestions by location
  - Most common dangerous events in the area
- Available in both **Spanish and English**.
- Auto-blocks unrelated questions: responds with
  > "Estoy enfocado en la guía turística, para otra consulta puedes utilizar otra herramienta"

---

## 🛠️ Technologies Used

- [Python](https://www.python.org/)
- [Dash (Plotly)](https://dash.plotly.com/)
- [Folium](https://python-visualization.github.io/folium/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [LangChain](https://www.langchain.com/)
- [Gemini AI](https://ai.google.dev/)
- [Google Generative AI API](https://ai.google.dev/)

---

## 📁 Project Structure

```
SafeGuide/
│
├── app.py                           # Main dashboard + chatbot UI (Dash + Folium + Gemini)
├── mdi_homicidiosintencionales...  # Homicide dataset (CSV)
├── SGR_EventosPeligrosos_...xlsx    # Hazardous events dataset (Excel)
├── atractivos_tur.csv               # Tourist attraction dataset
├── .env                             # API key for Gemini AI
└── README.md                        # This file
```

---

## 🚀 How to Run the App

### 1. Install dependencies
```bash
pip install dash pandas plotly folium python-dotenv langchain langchain-google-genai google-generativeai
```

### 2. Create a `.env` file
Inside your project folder:
```
API_KEY_GEMINI=your_api_key_here
```

### 3. Run the app
```bash
python app.py
```

Then open [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

---

## 🔮 Planned Features

- Itinerary planner with estimated time, distance, and safety scores.
- Heatmaps with crime and danger density.
- User-authenticated profiles to store preferences.
- Language selection and offline support for chatbot responses.

---

## 🛡️ Privacy & Ethics

- Respects user privacy and does not store personal data.
- Built with transparency and avoids bias in suggestions.
- Uses only open and verifiable datasets.

---

## 👥 Authors

Developed by Computer Science students as a final project focused on:
- Public safety
- Generative AI
- Data visualization
- Smart tourism

---

**SafeGuide** is more than just a travel app — it's your smart, safe companion to explore Ecuador.
