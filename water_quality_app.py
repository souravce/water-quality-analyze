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

# --- Streamlit App ---
st.set_page_config(page_title="AquaScan", layout="wide")

# Custom Background Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to right, #f0f9ff, #ffffff);
        font-family: 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌊 Water Quality Analyzer")
st.markdown("Analyze water samples based on color, turbidity, viscosity, and pH level.")

# Sidebar Inputs
with st.sidebar:
    st.header("Input Parameters")
    color = st.selectbox("Water Color", ["clear", "yellow", "cloudy", "green", "reddish brown", "black"])
    turbidity = st.slider("Turbidity (NTU)", 0, 1000, 10)
    viscosity = st.slider("Viscosity Index", 5, 110, 15)
    ph = st.slider("pH Level", 0.0, 14.0, 7.0, step=0.1)

if st.button("Analyze Sample"):
    category, suggestion, turbidity_level, viscosity_level, ph_status, ph_color = categorize_water(
        color, turbidity, viscosity, ph
    )

    st.subheader("Results")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Category:**  
        <span style='color: {"red" if "Toxic" in category else "orange" if "Harmful" in category else "green"}'>
        {category}</span><br><br>
        
        **Suggestion:**  
        {suggestion}<br><br>
        
        **pH Status:**  
        <span style='color:{ph_color}'>{ph_status}</span>
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
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom')
        st.pyplot(fig)

    if color == "black":
        st.error("🚨 Immediate action required! Possible sewage contamination.")
    elif color == "clear" and turbidity < 1 and viscosity < 5:
        st.success("✅ This is clean, safe water.")
