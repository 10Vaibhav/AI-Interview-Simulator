from openai import OpenAI
import streamlit as st 

st.set_page_config(page_title="AI Interview Simulator", page_icon="💬")

st.title("AI Interview Simulator!")

client = OpenAI(api_key= st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"