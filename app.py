import streamlit as st
import google.generativeai as genai

# Configure Gemini AI API (Replace with your actual API key)
API_KEY = "AIzaSyBa5WZHnfs5OZ4_roPGR6jcMM5N9waVqH8"
genai.configure(api_key=API_KEY)

# Use a valid Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

def get_conversion_result(query):
    try:
        response = model.generate_content(query)
        return response.text if response else "No response received."
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.set_page_config(page_title="🔄 Smart Unit Converter", page_icon="📏", layout="wide")
    
    st.title("🚀 Smart Unit Converter")
    st.markdown("### Convert Length, Weight, Temperature, Time, Speed, and Data Units with Ease!")
    
    with st.sidebar:
        st.header("⚙️ Settings")
        reset_button = st.button("🔄 Reset All")
        if reset_button:
            st.session_state.clear()
        
        st.header("🤖 Gemini AI Conversion")
        user_query = st.text_input("💬 Enter your conversion query (e.g., '10 km to miles'):")
        if st.button("✨ Ask Gemini"):
            if user_query:
                result = get_conversion_result(user_query)
                if any(unit in user_query.lower() for unit in ["km", "miles", "kg", "grams", "celsius", "fahrenheit"]):
                    st.success(f"✅ Result: {result}")
                else:
                    st.warning("⚠️ Please ask only about unit conversions.")
            else:
                st.warning("⚠️ Please enter a conversion query.")
    
    conversion_type = st.radio("📌 Choose Conversion Type", [
        "Length Converter", "Weight Converter", "Temperature Converter", 
        "Time Converter", "Speed Converter", "Data Converter"
    ])
    
    options = {
        "Length Converter": ["Kilometers to Miles", "Miles to Kilometers", "Meters to Feet", "Feet to Meters"],
        "Weight Converter": ["Kilograms to Pounds", "Pounds to Kilograms", "Grams to Ounces", "Ounces to Grams"],
        "Temperature Converter": ["Celsius to Fahrenheit", "Fahrenheit to Celsius"],
        "Time Converter": ["Hours to Minutes", "Minutes to Seconds", "Seconds to Milliseconds", "Milliseconds to Seconds"],
        "Speed Converter": ["Kilometers per Hour to Miles per Hour", "Miles per Hour to Kilometers per Hour"],
        "Data Converter": ["Megabytes to Gigabytes", "Gigabytes to Terabytes", "Kilobytes to Megabytes", "Bytes to Kilobytes"]
    }
    
    result = ""  # Default value to prevent errors
    
    choice = st.radio("🔽 Select Conversion", options[conversion_type])
    value = st.number_input("✏️ Enter Value", min_value=0.0, format="%.4f")
    
    conversions = {
        "Kilometers to Miles": value * 0.621371,
        "Miles to Kilometers": value * 1.60934,
        "Meters to Feet": value * 3.28084,
        "Feet to Meters": value * 0.3048,
        "Kilograms to Pounds": value * 2.20462,
        "Pounds to Kilograms": value * 0.453592,
        "Grams to Ounces": value * 0.035274,
        "Ounces to Grams": value * 28.3495,
        "Celsius to Fahrenheit": (value * 9/5) + 32,
        "Fahrenheit to Celsius": (value - 32) * 5/9,
        "Hours to Minutes": value * 60,
        "Minutes to Seconds": value * 60,
        "Seconds to Milliseconds": value * 1000,
        "Milliseconds to Seconds": value / 1000,
        "Kilometers per Hour to Miles per Hour": value * 0.621371,
        "Miles per Hour to Kilometers per Hour": value * 1.60934,
        "Megabytes to Gigabytes": value / 1024,
        "Gigabytes to Terabytes": value / 1024,
        "Kilobytes to Megabytes": value / 1024,
        "Bytes to Kilobytes": value / 1024
    }
    
    if choice in conversions:
        result = f"🎯 {value} {choice.split()[0]} = {conversions[choice]:.4f} {choice.split()[-1]}"
        st.success(result)
    
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    if st.button("💾 Add to History") and result:
        st.session_state['history'].append(result)
    
    if st.session_state['history']:
        st.subheader("📜 Conversion History")
        for i, entry in enumerate(st.session_state['history'], 1):
            st.write(f"{i}. {entry}")
    
    if st.button("🗑️ Clear History"):
        st.session_state['history'] = []
        st.success("🧹 History cleared!")
    
if __name__ == "__main__":
    main()
