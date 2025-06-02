import streamlit as st
import joblib
import pandas as pd

# تحميل النموذج
model = joblib.load('best_xgb_model.pkl')

st.title("🚗 تنبؤ بسعر السيارات المستعملة")
st.write("أدخل معلومات السيارة، وسنخبرك بالسعر المتوقع 💰")

# --- إدخال البيانات الأساسية
year = st.number_input("📅 سنة الصنع", 1990, 2025, 2015)
odometer = st.number_input("📍 عدد الأميال", 0, 300000, 60000)
cylinders = st.selectbox("🔧 عدد السلندرات", [4, 6, 8])

# --- خصائص السيارة الإضافية حسب النموذج
manufacturer = st.selectbox("🏭 الشركة المصنعة", [
    'ford', 'chevrolet', 'toyota', 'honda', 'nissan', 'jeep', 'hyundai', 'gmc', 'ram', 'bmw',
    'volkswagen', 'subaru', 'kia', 'dodge', 'mercedes-benz', 'cadillac', 'mazda', 'chrysler',
    'lexus', 'buick', 'infiniti', 'acura', 'lincoln', 'volvo', 'mini', 'mitsubishi', 'audi',
    'pontiac', 'mercury', 'saturn', 'jaguar', 'porsche', 'tesla', 'land rover', 'fiat',
    'harley-davidson', 'alfa-romeo', 'aston-martin', 'ferrari', 'datsun', 'rover'
])

model_clean = st.selectbox("🚘 موديل السيارة", [
    'corolla', 'camry', 'civic', 'accord', 'f150', 'f-150', 'silverado', 'mustang',
    'altima', 'cr-v', 'escape', 'fusion', 'malibu', 'impala', 'wrangler', 'tacoma',
    'prius', 'sentra', 'elantra', 'sonata', 'equator', 'odyssey', 'grand cherokee',
    'explorer', 'jetta', 'focus', 'rav4', 'tahoe', 'sierra', '4runner', 'outback', 'other'
])

condition = st.selectbox("🛠️ حالة السيارة", ['new', 'like new', 'good', 'fair', 'salvage'])

fuel = st.selectbox("⛽ نوع الوقود", ['gas', 'diesel', 'electric', 'hybrid', 'other'])

transmission = st.selectbox("⚙️ نوع الجير", ['automatic', 'manual', 'other'])

drive = st.selectbox("🛞 نظام الدفع", ['fwd', 'rwd', '4wd'])

car_type = st.selectbox("🚙 نوع السيارة", [
    'sedan', 'SUV', 'truck', 'coupe', 'hatchback', 'wagon', 'mini-van', 'van',
    'convertible', 'pickup', 'offroad', 'bus', 'other'
])

paint_color = st.selectbox("🎨 لون الطلاء", [
    'white', 'black', 'silver', 'blue', 'red', 'grey', 'green', 'custom', 'brown',
    'orange', 'yellow', 'purple'
])

state = st.selectbox("📍 الولاية", [
    'ca', 'ny', 'tx', 'fl', 'pa', 'oh', 'il', 'ga', 'nc', 'mi', 'nj', 'va', 'wa', 'az',
    'ma', 'in', 'tn', 'mo', 'md', 'wi', 'co', 'mn', 'sc', 'al', 'la', 'ky', 'or', 'ok',
    'ct', 'ut', 'ia', 'nv', 'ar', 'ms', 'ks', 'nm', 'ne', 'wv', 'id', 'hi', 'nh', 'me',
    'ri', 'mt', 'de', 'sd', 'nd', 'ak', 'vt', 'dc', 'wy'
])

# --- بناء DataFrame
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

# تعبئة باقي الأعمدة الناقصة بالقيمة 0
expected_columns = model.get_booster().feature_names
for col in expected_columns:
    if col not in input_df.columns:
        input_df[col] = 0

# ترتيب الأعمدة
input_df = input_df[expected_columns]

# --- تنبؤ بالسعر
if st.button("🔍 تنبأ بالسعر"):
    price = model.predict(input_df)[0]
    st.success(f"🚘 السعر المتوقع للسيارة هو: ${round(price, 2)}")