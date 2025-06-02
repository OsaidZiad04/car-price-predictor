import streamlit as st
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('best_xgb_model.pkl')

# Language selection
lang = st.sidebar.selectbox("🌐 Select Language / اختر اللغة", ["English", "العربية"])

# Texts for both languages
texts = {
    "English": {
        "title": "🚗 Used Car Price Prediction",
        "subtitle": "Enter the car details and we'll predict the expected price 💰",
        "year": "📅 Year of Manufacture",
        "odometer": "📍 Odometer (miles)",
        "cylinders": "🔧 Number of Cylinders",
        "manufacturer": "🏭 Manufacturer",
        "model": "🚘 Car Model",
        "condition": "🛠️ Condition",
        "fuel": "⛽ Fuel Type",
        "transmission": "⚙️ Transmission",
        "drive": "🛞 Drive Type",
        "car_type": "🚙 Car Type",
        "paint_color": "🎨 Paint Color",
        "state": "📍 State",
        "predict": "🔍 Predict Price",
        "result": "🚘 The estimated price of the car is: ${}"
    },
    "العربية": {
        "title": "🚗 تنبؤ بسعر السيارات المستعملة",
        "subtitle": "أدخل معلومات السيارة، وسنخبرك بالسعر المتوقع 💰",
        "year": "📅 سنة الصنع",
        "odometer": "📍 عدد الأميال",
        "cylinders": "🔧 عدد السلندرات",
        "manufacturer": "🏭 الشركة المصنعة",
        "model": "🚘 موديل السيارة",
        "condition": "🛠️ حالة السيارة",
        "fuel": "⛽ نوع الوقود",
        "transmission": "⚙️ نوع الجير",
        "drive": "🛞 نظام الدفع",
        "car_type": "🚙 نوع السيارة",
        "paint_color": "🎨 لون الطلاء",
        "state": "📍 الولاية",
        "predict": "🔍 تنبأ بالسعر",
        "result": "🚘 السعر المتوقع للسيارة هو: ${}"
    }
}

t = texts[lang]  # Active language dictionary

# UI Header
st.title(t["title"])
st.write(t["subtitle"])

# Inputs
year = st.number_input(t["year"], 1990, 2025, 2015)
odometer = st.number_input(t["odometer"], 0, 300000, 60000)
cylinders = st.selectbox(t["cylinders"], [4, 6, 8])

manufacturer = st.selectbox(t["manufacturer"], [
    'ford', 'chevrolet', 'toyota', 'honda', 'nissan', 'jeep', 'hyundai', 'gmc', 'ram', 'bmw',
    'volkswagen', 'subaru', 'kia', 'dodge', 'mercedes-benz', 'cadillac', 'mazda', 'chrysler',
    'lexus', 'buick', 'infiniti', 'acura', 'lincoln', 'volvo', 'mini', 'mitsubishi', 'audi',
    'pontiac', 'mercury', 'saturn', 'jaguar', 'porsche', 'tesla', 'land rover', 'fiat',
    'harley-davidson', 'alfa-romeo', 'aston-martin', 'ferrari', 'datsun', 'rover'
])

model_clean = st.selectbox(t["model"], [
    'corolla', 'camry', 'civic', 'accord', 'f150', 'f-150', 'silverado', 'mustang',
    'altima', 'cr-v', 'escape', 'fusion', 'malibu', 'impala', 'wrangler', 'tacoma',
    'prius', 'sentra', 'elantra', 'sonata', 'equator', 'odyssey', 'grand cherokee',
    'explorer', 'jetta', 'focus', 'rav4', 'tahoe', 'sierra', '4runner', 'outback', 'other'
])

condition = st.selectbox(t["condition"], ['new', 'like new', 'good', 'fair', 'salvage'])
fuel = st.selectbox(t["fuel"], ['gas', 'diesel', 'electric', 'hybrid', 'other'])
transmission = st.selectbox(t["transmission"], ['automatic', 'manual', 'other'])
drive = st.selectbox(t["drive"], ['fwd', 'rwd', '4wd'])

car_type = st.selectbox(t["car_type"], [
    'sedan', 'SUV', 'truck', 'coupe', 'hatchback', 'wagon', 'mini-van', 'van',
    'convertible', 'pickup', 'offroad', 'bus', 'other'
])

paint_color = st.selectbox(t["paint_color"], [
    'white', 'black', 'silver', 'blue', 'red', 'grey', 'green', 'custom', 'brown',
    'orange', 'yellow', 'purple'
])

state = st.selectbox(t["state"], [
    'ca', 'ny', 'tx', 'fl', 'pa', 'oh', 'il', 'ga', 'nc', 'mi', 'nj', 'va', 'wa', 'az',
    'ma', 'in', 'tn', 'mo', 'md', 'wi', 'co', 'mn', 'sc', 'al', 'la', 'ky', 'or', 'ok',
    'ct', 'ut', 'ia', 'nv', 'ar', 'ms', 'ks', 'nm', 'ne', 'wv', 'id', 'hi', 'nh', 'me',
    'ri', 'mt', 'de', 'sd', 'nd', 'ak', 'vt', 'dc', 'wy'
])

# Build input dictionary
input_dict = {
    'year': year,
    'odometer': odometer,
    'cylinders': cylinders,
    f'manufacturer_{manufacturer}': 1,
    f'model_clean_{model_clean}': 1,
    f'condition_{condition}': 1,
    f'fuel_{fuel}': 1,
    f'transmission_{transmission}': 1,
    f'drive_{drive}': 1,
    f'type_{car_type}': 1,
    f'paint_color_{paint_color}': 1,
    f'state_{state}': 1,
}

input_df = pd.DataFrame([input_dict])

# Fill missing features with 0
expected_columns = model.get_booster().feature_names
for col in expected_columns:
    if col not in input_df.columns:
        input_df[col] = 0

# Reorder columns
input_df = input_df[expected_columns]

# Prediction button
if st.button(t["predict"]):
    price = model.predict(input_df)[0]
    st.success(t["result"].format(round(price, 2)))
