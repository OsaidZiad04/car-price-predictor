# 🚗 Used Car Price Prediction with XGBoost and Streamlit

This is a web-based machine learning project that predicts the price of used cars based on various input features using a pre-trained XGBoost model. The web interface is built with Streamlit and allows users to input car details such as year, mileage, manufacturer, model, condition, and more to estimate the expected price.

---

## 📊 Dataset

The model was trained using the publicly available **[Craigslist Cars and Trucks Dataset](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data)** from Kaggle. The dataset includes over 400,000 vehicle listings across various U.S. states.

---

## 🔧 Features Used in the Model

- Year of manufacturing  
- Odometer (mileage)  
- Number of cylinders  
- Fuel type  
- Transmission type  
- Manufacturer  
- Model  
- Condition  
- Drive type  
- Car body type  
- Paint color  
- U.S. state  

All categorical features were one-hot encoded before training.

---

## 🚀 How to Run the App

1. **Clone the repository:**
   ```bash
   git clone https://github.com/OsaidZiad04/car-price-predictor
   cd car-price-predictor
