import pandas as pd
import streamlit as st
import joblib

class EnergyConsumptionApp:
    def __init__(self):
        # Page configuration
        st.set_page_config(
            page_title="Energy Consumption Prediction",
            page_icon="🔋",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.setup_styles()
        self.load_resources()
    def setup_styles(self):
        # Updated styles for input features and blue sliders
        st.markdown(
            """
            <style>
            /* Global Styles */
            .stApp {
                background: radial-gradient(circle, #2C3E50, #4CA1AF);
                font-family: 'Poppins', sans-serif;
                color: #E8EAED;
            }

            /* Header Style */
            .header {
                text-align: center;
                color: #FFFFFF;
                background: linear-gradient(to right, #43C6AC, #191654);
                padding: 30px 10px;
                border-radius: 12px;
                font-size: 36px;
                font-weight: 700;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
            }

            /* Sidebar Style */
            .sidebar {
                padding: 15px;
                background-color: #333A46;
                border-radius: 10px;
                color: #E8EAED;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            }

            .sidebar h4 {
                color: #43C6AC;
            }

            /* Input Features Style */
            .stSlider > div > div > div > div {
                background-color: #43C6AC !important;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }

            .stSlider > div > div > div > div > div {
                background-color: #1D4ED8 !important;
            }

            .stDateInput > div, .stTimeInput > div {
                background: linear-gradient(to right, #43C6AC, #191654);
                color: white;
                border-radius: 8px;
                padding: 5px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
            }

            .stDateInput > div:hover, .stTimeInput > div:hover {
                box-shadow: 0 6px 10px rgba(0, 0, 0, 0.5);
            }

            /* Card Style for Predictions */
            .card {
                background: linear-gradient(to bottom, #283E51, #4B79A1);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
                color: #F1F1F1;
                margin: 20px 0;
                text-align: center;
            }

            .card h3 {
                color: #FFD700;
            }

            .disclaimer {
                background-color: #444B59;
                color: #B0C4DE;
                padding: 20px;
                border-radius: 12px;
                font-size: 14px;
                margin-top: 30px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            }

            /* Buttons */
            .stButton>button {
                background: linear-gradient(to right, #FF7F50, #FF4500);
                color: white;
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                transition: 0.3s ease-in-out;
            }

            .stButton>button:hover {
                background: linear-gradient(to right, #FF6347, #FF4500);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    def load_resources(self):
        # Load models and features
        try:
            self.linear_model = joblib.load("linear_model.pkl")
            self.ridge_model = joblib.load("ridge_model.pkl")
            self.feature_names = joblib.load("feature_names.pkl")
            st.sidebar.success("✅ Models loaded successfully!")
        except Exception as e:
            st.sidebar.error(f"⚠️ Error loading resources: {e}")

    def run(self):
        # Header
        st.markdown("<div class='header'>🔋 Energy Consumption Prediction</div>", unsafe_allow_html=True)

        # Sidebar inputs
        st.sidebar.markdown("<div class='sidebar'><h4>🔧 Input Features</h4></div>", unsafe_allow_html=True)

        voltage = st.sidebar.slider("Voltage (V)", 220.0, 255.0, 240.0)
        global_intensity = st.sidebar.slider("Global Intensity (A)", 0.0, 20.0, 4.63)
        sub_metering_1 = st.sidebar.slider("Sub Metering 1 (Wh)", 0.0, 50.0, 1.12)
        sub_metering_2 = st.sidebar.slider("Sub Metering 2 (Wh)", 0.0, 50.0, 1.30)
        sub_metering_3 = st.sidebar.slider("Sub Metering 3 (Wh)", 0.0, 50.0, 6.46)

        date = st.sidebar.date_input("Select Date", value=pd.Timestamp("2024-11-28"))
        time = st.sidebar.time_input("Select Time", value=pd.Timestamp("2024-11-28 12:00:00").time())

        # Features and predictions
        date_time = pd.Timestamp.combine(date, time)
        year, month, day, hour, minute = date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute
        weekday = date_time.weekday()
        is_holiday, light = 0, 1

        input_data = pd.DataFrame({
            "Global_reactive_power": [0.0],
            "Voltage": [voltage],
            "Global_intensity": [global_intensity],
            "Sub_metering_1": [sub_metering_1],
            "Sub_metering_2": [sub_metering_2],
            "Sub_metering_3": [sub_metering_3],
            "Year": [year],
            "Month": [month],
            "Day": [day],
            "Hour": [hour],
            "Minute": [minute],
            "Is_holiday": [is_holiday],
            "Light": [light],
            "Weekday": [weekday]
        })[self.feature_names]

        try:
            linear_pred = self.linear_model.predict(input_data)[0]
            ridge_pred = self.ridge_model.predict(input_data)[0]

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                f"<h3>Linear Regression</h3><p>{linear_pred:.2f} kW</p>"
                f"<h3>Ridge Regression</h3><p>{ridge_pred:.2f} kW</p>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
        except ValueError as e:
            st.error(f"⚠️ Prediction Error: {e}")

        # Disclaimer
        st.markdown(
            "<div class='disclaimer'>"
            "<strong>Note:</strong> Results are based on predictive models. For accuracy, seek expert consultation."
            "</div>",
            unsafe_allow_html=True
        )

# Run app
def main():
    app = EnergyConsumptionApp()
    app.run()

if __name__ == "__main__":
    main()

