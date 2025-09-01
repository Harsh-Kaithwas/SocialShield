import streamlit as st
import pandas as pd
import json
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="SocialShield Dashboard", layout="wide")
st.title("SocialShield – Social Media Impact Dashboard")
st.markdown("Analyze social media posts/users and visualize overall impact.")

# Load mock data
with open("mock_data.json") as f:
    data = json.load(f)

users_list = [u["username"] for u in data["users"]]

# ---- Sidebar Removed, Single Input Field ----
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

toxicity_map = {"Low": 30, "Medium": 60, "High": 85}

def get_color(score):
    if score < 40:
        return "#9AE6B4"
    elif score < 70:
        return "#FBD38D"
    else:
        return "#FC8181"

# ---- Analysis on Button Click ----
if analyze_btn:
    result = dummy_analysis(user_input)
    
    st.subheader(f"Analysis Report: '{result['username']}'")
    
    # ---- Top Metrics Cards ----
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
    
    # ---- Bar Chart: Users vs Risk ----
    st.subheader("Bar Chart: Users vs Risk Score")
    df_users = pd.DataFrame({
        "Username": [u["username"] for u in data["users"]],
        "Risk Score": [u["risk_score"] for u in data["users"]]
    })
    st.bar_chart(df_users.set_index("Username"))
    
    # ---- Pie Chart: Sentiment Distribution ----
    st.subheader("Pie Chart: Sentiment Distribution")
    sentiments = [u["sentiment"] for u in data["users"]]
    sentiment_counts = pd.Series(sentiments).value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=['#9AE6B4','#FBD38D','#FC8181'])
    ax1.axis('equal')
    st.pyplot(fig1)
    
    # ---- Average Metrics Summary ----
    avg_risk = int(sum([u["risk_score"] for u in data["users"]])/len(data["users"]))
    avg_fake_news = int(sum([u["fake_news_prob"] for u in data["users"]])/len(data["users"]))
    avg_toxicity = int(sum([toxicity_map[u["toxicity"]] for u in data["users"]])/len(data["users"]))
    
    st.subheader("Overall Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Risk Score", avg_risk)
    with col2:
        st.metric("Average Fake News %", f"{avg_fake_news}%")
    with col3:
        st.metric("Average Toxicity", avg_toxicity)
    
    st.markdown("---")
    
    # ---- Explainable Insight ----
    st.subheader("Explainable AI Insights")
    insight_list = [
        "This caption contains indicators of negative sentiment.",
        "Low toxicity detected, content seems safe.",
        "High fake news probability due to unverified sources.",
        "Engagement may lead to reputational risk.",
        "Post appears neutral but hashtags may amplify reach."
    ]
    st.info(random.choice(insight_list))
