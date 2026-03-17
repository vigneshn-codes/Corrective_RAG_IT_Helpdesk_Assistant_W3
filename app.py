import streamlit as st
import requests

st.title("🛠️ IT Helpdesk Assistant (CRAG)")

user_input = st.text_input("Describe your technical issue:")

if st.button("Get Help"):
    if user_input:
        with st.spinner("Checking internal docs and external sources..."):
            response = requests.post("http://localhost:8000/ask", json={"prompt": user_input})
            if response.status_code == 200:
                data = response.json()
                st.subheader(f"Source: {data['source']}")
                st.write(data['answer'])
            else:
                st.error("Failed to connect to the backend.")