import streamlit as st
import json

# Load mock data
with open("mock_data.json") as f:
    data = json.load(f)

# Simple score calculations
mental_score = int(min(data["daily_usage_hours"]/6*100,100))
fake_news_score = int(sum([1 for p in data["posts"] if not p["verified"]])/len(data["posts"])*100)
privacy_score = 100 if data["profile_public"] else 0
reputation_score = int(data["negative_comments"]/sum([p["comments"] for p in data["posts"]])*100)

# Dashboard
st.title("SocialShield – Social Media Impact Assessment")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader("Mental Stress & Addiction")
    st.metric(label="Score", value=mental_score, delta="--")
with col2:
    st.subheader("Fake News & Misinformation")
    st.metric(label="Score", value=fake_news_score, delta="--")
with col3:
    st.subheader("Privacy & Data Risk")
    st.metric(label="Score", value=privacy_score, delta="--")
with col4:
    st.subheader("Reputation / Cancel Culture")
    st.metric(label="Score", value=reputation_score, delta="--")
