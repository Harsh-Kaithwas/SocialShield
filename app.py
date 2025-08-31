import streamlit as st
import pandas as pd
import json
from transformers import pipeline

# Page setup
st.set_page_config(page_title="SocialShield", layout="wide")
st.title("SocialShield – Social Media Impact Assessment (Prototype)")
st.write("Dashboard: 4 Dimensions with color-coded scores and chart")

# Load mock data
with open("mock_data.json") as f:
    data = json.load(f)

# Initialize sentiment analysis pipeline (HuggingFace)
sentiment_pipeline = pipeline("sentiment-analysis")

# ---- Calculate Mental Stress Score ----
negative_posts = 0
for post in data["posts"]:
    result = sentiment_pipeline(post["text"])[0]
    if result["label"] == "NEGATIVE":
        negative_posts += 1
mental_score = int(negative_posts / max(1, len(data["posts"])) * 100)

# ---- Fake News Score (mock logic: unverified posts) ----
fake_news_score = int(sum([1 for p in data["posts"] if not p["verified"]])/len(data["posts"])*100)

# ---- Privacy Risk ----
privacy_score = 100 if data["profile_public"] else 0

# ---- Reputation / Cancel Culture Score (mock: negative comments) ----
total_comments = sum([p["comments"] for p in data["posts"]])
reputation_score = int(data["negative_comments"]/max(1,total_comments)*100)

# ---- Color function ----
def get_color(score):
    if score < 40:
        return "green"
    elif score < 70:
        return "yellow"
    else:
        return "red"

# ---- Display 4 metrics with color ----
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader("Mental Stress & Addiction")
    st.markdown(f"<h3 style='color:{get_color(mental_score)}'>{mental_score}</h3>", unsafe_allow_html=True)
with col2:
    st.subheader("Fake News & Misinformation")
    st.markdown(f"<h3 style='color:{get_color(fake_news_score)}'>{fake_news_score}</h3>", unsafe_allow_html=True)
with col3:
    st.subheader("Privacy & Data Risk")
    st.markdown(f"<h3 style='color:{get_color(privacy_score)}'>{privacy_score}</h3>", unsafe_allow_html=True)
with col4:
    st.subheader("Reputation / Cancel Culture")
    st.markdown(f"<h3 style='color:{get_color(reputation_score)}'>{reputation_score}</h3>", unsafe_allow_html=True)

# ---- Bar Chart ----
scores = {
    "Dimension": ["Mental Stress", "Fake News", "Privacy Risk", "Reputation Risk"],
    "Score": [mental_score, fake_news_score, privacy_score, reputation_score]
}
df = pd.DataFrame(scores)
st.subheader("Overall Impact Chart")
st.bar_chart(df.set_index("Dimension"))
