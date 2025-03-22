Aquí tienes tu `README.md` actualizado con las nuevas funcionalidades:

---

```markdown
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

## 🧭 Current Functionality (Dash App)

This version, built using Dash + Folium, includes:

### 🔍 Homicide Dashboard

- Filter data by **province** and **type of death**.
- Visualize weapon usage with a histogram chart, segmented by gender.

### ⚠️ Dangerous Events Dashboard (SGR)

- Filter by **type of event** (e.g., “Intoxicación”, “Perturbación en eventos masivos”).
- View reported cases by **province and canton** in a histogram chart.

### 🗺️ Interactive Map

- Displays **tourist attractions** with green markers using Folium.
- Includes name, category, and type of each attraction.
- The map loads quickly and only focuses on core tourist data for now.

---

## 🛠️ Technologies Used

- [Python](https://www.python.org/)
- [Dash (Plotly)](https://dash.plotly.com/)
- [Folium](https://python-visualization.github.io/folium/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

---

## 📁 Project Structure

```
SafeGuide/
│
├── app.py                           # Main dashboard script
├── mdi_homicidiosintencionales...  # Homicide data (Ecuador)
├── SGR_EventosPeligrosos_...xlsx    # Hazardous events dataset (SGR)
├── atractivos_tur.csv               # Tourist attraction dataset
└── README.md                        # This file
```

---

## 🚀 How to Run

1. Install required packages:

```bash
pip install dash pandas plotly folium
```

2. Place the CSV and Excel files in the same directory as `app.py`.

3. Run the application:

```bash
python app.py
```

4. Open your browser and go to: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## 🔮 Planned Features (Using Generative AI)

- Smart itinerary generation with estimated travel times, costs, and schedules.
- AI-based chatbot that answers questions like:
  - “What are the safest places to visit at night?”
  - “What is the best route to avoid traffic?”
- Recommendations that improve with user feedback and behavior.
- Real-time data updates from government, media, tourism platforms, and social networks.

---

## 🛡️ Privacy & Ethics

- Complies with data protection laws and ensures responsible data handling.
- AI models will be transparent and explainable.
- Avoids discriminatory bias in recommendations or safety scoring.

---

## 👥 Authors

- Developed by students of Computer Science as part of a project focused on data science, public safety, and smart tourism.

---

**SafeGuide** is more than a travel tool — it's your trusted companion for safe, smart, and informed exploration.
