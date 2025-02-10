import streamlit as st
import json
import os
from datetime import datetime

def display_feedback_tab():
    st.header("User Feedback Comments")
    
    # Load CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Path ke file JSON
    feedback_file = 'dataset/user_feedbacks.json'
    
    # Cek apakah file ada
    if not os.path.exists(feedback_file):
        st.warning("No feedback data available.")
        return
    
    # Baca file JSON
    with open(feedback_file, 'r') as file:
        feedback_data = json.load(file)
    
    # Tampilkan komentar
    if not feedback_data:
        st.info("No feedback comments to display.")
    else:
        for feedback in feedback_data:
            # Format timestamp agar lebih mudah dibaca
            timestamp = feedback.get("timestamp", "")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    formatted_time = timestamp
            else:
                formatted_time = "No timestamp"
            
            # Tampilkan feedback dalam card
            st.markdown(
                f"""
                <div class="feedback-card">
                    <h4>{feedback.get('name', 'Anonymous🐦‍🔥')}</h4>
                    <p class="timestamp">{formatted_time}</p>
                    <p><strong>Email:</strong> {feedback.get('email', 'No email provided')}</p>
                    <p class="rating">Rating: {feedback.get('rating', 'No rating')} ⭐</p>
                    <p class="category">Category: {feedback.get('category', 'No category')}</p>
                    <p><strong>Feedback:</strong> {feedback.get('feedback_text', 'No feedback text')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )