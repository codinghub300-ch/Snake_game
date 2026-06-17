import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="wide"
)

st.title("🐍 Snake Game")
st.write("Built by Coding Hub")

with open("snake.html", "r", encoding="utf-8") as f:
    html = f.read()

components.html(html, height=750)
