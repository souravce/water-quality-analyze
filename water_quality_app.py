import streamlit as st
import matplotlib.pyplot as plt

def categorize_water(color, turbidity, viscosity, ph):
    color = color.lower()
    categories = {
        "clear": ("Toxin Free", "No action needed."),
        "yellow": ("Less Harmful", "Possible chlorine presence; consider aeration or activated carbon filtration."),
        "cloudy": ("Moderate Risk", "Sedimentation or microbial contamination; try filtration and boiling."),
        "green": ("Harmful", "Possible algal growth; use UV treatment or chlorination."),
        "reddish brown": ("Toxic", "High iron content; consider aeration and iron removal filters."),
        "black": ("Highly Toxic", "Possible sewage contamination; avoid use, requires extensive treatment.")
    }

    turbidity_level = "Low" if turbidity < 5 else "Medium" if turbidity < 50 else "High"
    viscosity_level = "Low" if viscosity < 10 else "Medium" if viscosity < 50 else "High"

    if ph < 7:
        ph_status = "Acidic"
        ph_color = "red"
    elif ph == 7:
        ph_status = "Neutral"
        ph_color = "green"
    else:
        ph_status = "Alkaline"
        ph_color = "blue"

    category, suggestion = categories.get(color, ("Unknown", "No data available for this color."))
    return category, suggestion, turbidity_level, viscosity_level, ph_status, ph_color

# Streamlit App Config
st.set_page_config(page_title="AquaScan", layout="wide")

# Elegant Background & Component Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to right, #e0f7fa, #ffffff);
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
    }
    .block-container {
        padding: 2rem 3rem;
    }
    .stSidebar {
        background-color: #1e1e1e !important;
        color: white;
    }
    .stSlider > div[data-baseweb="slider"] {
        margin-top: 10px;
    }
    .stSelectbox label, .stSlider label {
        color: white !important;
        font-weight: 600;
    }
    .stButton button {
        background-color: #007acc;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #005f99;
    }
    .result-card {
        background-color: rgba(255,255,255,0.85);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("🌊 Water Quality Analyzer")
st.markdown("Analyze water samples based on **color**, **turbidity**, **viscosity**, and **pH level**.")

# Sidebar
with st.sidebar:
    st.header("Input Parameters")
    color = st.selectbox("Water Color", ["clear", "yellow", "cloudy", "green", "reddish brown", "black"])
    turbidity = st.slider("Turbidity (NTU)", 0, 1000, 10)
    viscosity = st.slider("Viscosity Index", 5, 110, 15)
    ph = st.slider("pH Level", 0.0, 14.0, 7.0, step=0.1)

# Analysis and Result Display
if st.button("Analyze Sample"):
    category, suggestion, turbidity_level, viscosity_level, ph_status, ph_color = categorize_water(
        color, turbidity, viscosity, ph
    )

    st.subheader("Results")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='result-card'>
        <h4>Category:</h4>
        <span style='color: {"red" if "Toxic" in category else "orange" if "Harmful" in category else "green"}'>
        {category}</span><br><br>

        <h4>Suggestion:</h4>
        {suggestion}<br><br>

        <h4>pH Status:</h4>
        <span style='color:{ph_color}; font-weight:bold'>{ph_status}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig, ax = plt.subplots()
        params = ["Turbidity", "Viscosity", "pH"]
        values = [turbidity, viscosity, ph]
        colors = ["#1f77b4", "#ff7f0e", ph_color]
        bars = ax.bar(params, values, color=colors)
        ax.set_title("Parameter Comparison")
        ax.set_ylabel("Value")
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height, f'{height:.1f}', ha='center', va='bottom')
        st.pyplot(fig)

    if color == "black":
        st.error("🚨 Immediate action required! Possible sewage contamination.")
    elif color == "clear" and turbidity < 1 and viscosity < 5:
        st.success("✅ This is clean, safe water.")
