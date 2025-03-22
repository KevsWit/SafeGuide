# 🧭 SafeGuide

**SafeGuide** is an interactive travel guide designed to help people understand the status of tourist destinations by incorporating crime data, dangerous zones, crowded areas, and must-visit locations. The platform provides clear and useful visualizations to help travelers make safer, data-driven decisions.

---

## 📌 Project Overview

The main idea of SafeGuide is to develop a mobile application that provides reliable and up-to-date information about tourist destinations using a generative AI capable of processing large volumes of data. Anyone planning a trip can consult the app and gain insight into the real situation of the place they want to visit, with a focus on:

---

### 🔐 Safety and Prevention

- **Crime maps and dangerous zones**: The app visually highlights areas with higher crime incidence, allowing users to avoid high-risk areas and choose safer routes.
- **Disaster and incident tracking**: A dashboard based on government emergency data (SGR) shows hazardous events like intoxications, natural disasters, or mass disturbances.
- **Real-time alerts**: By integrating open data and local sources, the app will notify users of recent incidents or unsafe events.

---

### 🛣️ Infrastructure and Access

- Stay informed about busy zones and optimal access routes.

---

### 📍 Places to Visit

- **Personalized recommendations**: Using generative AI, the app suggests historic sites, museums, parks, and local gastronomy tailored to user interests (e.g., family, adventure, cultural tourism).
- **User reviews and summaries**: AI will generate short summaries from reviews posted on social media, websites, and travel platforms to highlight the reputation and key features of each place.

---

## 🧭 Current Functionality

### 💻 Dash App (Data Visualization)

This version, built using Dash + Folium, includes:

#### 🔍 Homicide Dashboard
- Filter data by **province** and **type of death**.
- Visualize weapon usage with a histogram chart, segmented by gender.

#### ⚠️ Dangerous Events Dashboard (SGR)
- Filter by **type of event** (e.g., “Intoxicación”, “Perturbación en eventos masivos”).
- View reported cases by **province and canton** in a histogram chart.

#### 🗺️ Interactive Map
- Displays **tourist attractions** with green markers using Folium.
- Includes name, category, and type of each attraction.
- The map loads quickly and only focuses on core tourist data for now.

### 🤖 SafeGuide Chatbot (Gemini AI)

- A conversational assistant built with **Gemini 1.5 Flash** using LangChain.
- Accepts questions about:
  - What places are safe or risky to visit
  - Where to travel based on interests
  - What tourist sites exist in specific provinces or cities
- Responds in **Spanish or English** depending on user input.
- Automatically blocks questions outside tourism-related topics in Ecuador.

---

## 🛠️ Technologies Used

- [Python](https://www.python.org/)
- [Dash (Plotly)](https://dash.plotly.com/)
- [Folium](https://python-visualization.github.io/folium/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [LangChain](https://www.langchain.com/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)

---

## 📁 Project Structure

```
SafeGuide/
│
├── app.py                           # Main dashboard script (Dash + Folium)
├── chatbot.py                       # Conversational AI (Gemini + LangChain)
├── mdi_homicidiosintencionales...  # Homicide data (Ecuador)
├── SGR_EventosPeligrosos_...xlsx    # Hazardous events dataset (SGR)
├── atractivos_tur.csv               # Tourist attraction dataset
├── .env                             # API key file for Gemini
└── README.md                        # This file
```

---

## 🚀 How to Run

### For the Dashboard:

1. Install required packages:
```bash
pip install dash pandas plotly folium
```
2. Place the data files in the same directory as `app.py`
3. Run the application:
```bash
python app.py
```
4. Open your browser at: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

### For the Chatbot:

1. Install required packages:
```bash
pip install python-dotenv pandas langchain langchain-google-genai google-generativeai
```
2. Create a `.env` file with your Gemini API key:
```
API_KEY_GEMINI=your_api_key_here
```
3. Run the chatbot:
```bash
python chatbot.py
```

---

## 🔮 Planned Features (Future)

- Smart itinerary generation with estimated travel times, costs, and schedules.
- Enhanced AI chatbot with live data retrieval and contextual memory.
- Visual heatmaps of high-risk areas and top-rated attractions.
- User profile-based recommendations.

---

## 🛡️ Privacy & Ethics

- Complies with data protection laws and ensures responsible data handling.
- AI models are transparent and explainable.
- Avoids bias in recommendations or safety scoring.

---

## 👥 Authors

- Developed by students of Computer Science as part of a project focused on data science, public safety, and smart tourism.

---

**SafeGuide** is more than a travel tool — it's your trusted companion for safe, smart, and informed exploration.
