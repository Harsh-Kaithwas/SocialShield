import streamlit as st
import pandas as pd
import json

# Page setup
st.set_page_config(page_title="SocialShield", layout="wide")
st.title("SocialShield – Social Media Impact Assessment (Prototype)")

st.write("Prototype Dashboard: 4 Dimensions with color-coded scores and chart")

# Load mock data
with open("mock_data.json") as f:
    data = json.load(f)

# Simple score calculations
mental_score = int(min(data["daily_usage_hours"]/6*100,100))
fake_news_score = int(sum([1 for p in data["posts"] if not p["verified"]])/len(data["posts"])*100)
privacy_score = 100 if data["profile_public"] else 0
reputation_score = int(data["negative_comments"]/sum([p["comments"] for p in data["posts"]])*100)

# Function to get color based on score
def get_color(score):
    if score < 40:
        return "green"
    elif score < 70:
        return "yellow"
    else:
        return "red"

# Display 4 metrics with color
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Mental Stress & Addiction")
    color = get_color(mental_score)
    st.markdown(f"<h3 style='color:{color}'>{mental_score}</h3>", unsafe_allow_html=True)

with col2:
    st.subheader("Fake News & Misinformation")
    color = get_color(fake_news_score)
    st.markdown(f"<h3 style='color:{color}'>{fake_news_score}</h3>", unsafe_allow_html=True)

with col3:
    st.subheader("Privacy & Data Risk")
    color = get_color(privacy_score)
    st.markdown(f"<h3 style='color:{color}'>{privacy_score}</h3>", unsafe_allow_html=True)

with col4:
    st.subheader("Reputation / Cancel Culture")
    color = get_color(reputation_score)
    st.markdown(f"<h3 style='color:{color}'>{reputation_score}</h3>", unsafe_allow_html=True)

# Bar chart for all 4 dimensions
scores = {
    "Dimension": ["Mental Stress", "Fake News", "Privacy Risk", "Reputation Risk"],
    "Score": [mental_score, fake_news_score, privacy_score, reputation_score]
}

df = pd.DataFrame(scores)
st.subheader("Overall Impact Chart")
st.bar_chart(df.set_index("Dimension"))
