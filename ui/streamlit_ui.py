import streamlit as st
from orchestrators.calendar_orchestrator import calendar_orchestrator
from orchestrators.blog_orchestrator import blog_orchestrator

st.set_page_config("LLM Workflow Demo")
st.title("🚀 LLM Workflow Demo")

tab1, tab2 = st.tabs(["Calendar", "Blog"])

with tab1:
    text = st.text_input("Calendar request")
    if st.button("Run"):
        st.success(calendar_orchestrator(text))

with tab2:
    topic = st.text_input("Blog topic")
    if st.button("Generate"):
        st.markdown(blog_orchestrator(topic))
