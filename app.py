import streamlit as st
import pandas as pd
import json
import random
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="SocialShield", layout="wide")
st.title("SocialShield – Social Media Impact Assessment (Prototype)")
st.markdown("Enter any username, URL, or hashtag to generate a social media impact report.")

# Load mock data
with open("mock_data.json") as f:
    data = json.load(f)

# ---- Single Input Field ----
user_input = st.text_input("Enter Username / URL / Hashtag / Caption", "tech_guru")
analyze_btn = st.button("Analyze")

# ---- Dummy Analysis Function ----
def dummy_analysis(input_text):
    user_data = next((u for u in data["users"] if input_text in (u["username"], u["url"], u["hashtag"], u["caption"])), None)
    if not user_data:
        user_data = {
            "username": input_text,
            "caption": input_text,
            "hashtag": input_text,
            "url": "https://example.com/" + input_text,
            "sentiment": random.choice(["Positive","Neutral","Negative"]),
            "toxicity": random.choice(["Low","Medium","High"]),
            "risk_score": random.randint(10,90),
            "fake_news_prob": random.randint(5,80)
        }
    return user_data

# ---- Color Function for Cards ----
def get_color(score):
    if score < 40:
        return "#9AE6B4"  # green
    elif score < 70:
        return "#FBD38D"  # yellow
    else:
        return "#FC8181"  # red

toxicity_map = {"Low": 30, "Medium": 60, "High": 85}

# ---- Display Analysis ----
if analyze_btn:
    result = dummy_analysis(user_input)
    
    st.subheader(f"Analysis Report for '{result['username']}'")
    
    # ---- Metrics Cards ----
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"<div style='background-color:{get_color(toxicity_map[result['toxicity']])};padding:20px;border-radius:10px;text-align:center'><h4>Sentiment</h4><h3>{result['sentiment']}</h3></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='background-color:{get_color(toxicity_map[result['toxicity']])};padding:20px;border-radius:10px;text-align:center'><h4>Toxicity</h4><h3>{result['toxicity']}</h3></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='background-color:{get_color(result['risk_score'])};padding:20px;border-radius:10px;text-align:center'><h4>Risk Score</h4><h3>{result['risk_score']}</h3></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div style='background-color:{get_color(result['fake_news_prob'])};padding:20px;border-radius:10px;text-align:center'><h4>Fake News %</h4><h3>{result['fake_news_prob']}%</h3></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ---- Pie Chart ----
    st.subheader("Visual Overview")
    labels = ['Risk Score', 'Fake News Probability', 'Toxicity Level']
    values = [result['risk_score'], result['fake_news_prob'], toxicity_map[result['toxicity']]]
    
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#FC8181','#66b3ff','#9AE6B4'])
    ax1.axis('equal')
    st.pyplot(fig1)
    
    # ---- Bar Chart ----
    st.subheader("Bar Chart Overview")
    df = pd.DataFrame({
        "Metric": ["Risk Score","Fake News","Toxicity"],
        "Value": [result['risk_score'], result['fake_news_prob'], toxicity_map[result['toxicity']]]
    })
    st.bar_chart(df.set_index("Metric"))
    
    # ---- Explainable Insight ----
    st.subheader("Explainable AI Insight")
    insight_list = [
        "This caption contains indicators of negative sentiment.",
        "Low toxicity detected, content seems safe.",
        "High fake news probability due to unverified sources.",
        "Engagement may lead to reputational risk.",
        "Post appears neutral but hashtags may amplify reach."
    ]
    st.info(random.choice(insight_list))
