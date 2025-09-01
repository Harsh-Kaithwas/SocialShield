import streamlit as st
import pandas as pd
import json
import random
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="SocialShield", layout="wide")
st.title("SocialShield – Social Media Impact Assessment (Prototype)")
st.write("Analyze a social media post/user for risk, sentiment, toxicity & fake news probability")

# Load mock data
with open("mock_data.json") as f:
    data = json.load(f)

# ---- Sidebar Input ----
st.sidebar.header("Enter Post Details for Analysis")
username = st.sidebar.text_input("Username", "tech_guru")
caption = st.sidebar.text_area("Caption", "I love AI and tech innovations!")
hashtag = st.sidebar.text_input("Hashtags", "#AI #Tech")
url = st.sidebar.text_input("URL", "https://example.com/post1")
analyze_btn = st.sidebar.button("Analyze")

# ---- Dummy Analysis Function ----
def dummy_analysis(input_username, input_caption, input_hashtag, input_url):
    # Check if username exists in mock_data, else generate random
    user_data = next((u for u in data["users"] if u["username"] == input_username), None)
    if not user_data:
        user_data = {
            "username": input_username,
            "caption": input_caption,
            "hashtag": input_hashtag,
            "url": input_url,
            "sentiment": random.choice(["Positive","Neutral","Negative"]),
            "toxicity": random.choice(["Low","Medium","High"]),
            "risk_score": random.randint(10,90),
            "fake_news_prob": random.randint(5,80)
        }
    return user_data

# ---- Color Function ----
def get_color(score):
    if score < 40:
        return "green"
    elif score < 70:
        return "yellow"
    else:
        return "red"

# ---- Display Analysis ----
if analyze_btn:
    result = dummy_analysis(username, caption, hashtag, url)
    
    st.subheader(f"Analysis for @{result['username']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"**Sentiment:** {result['sentiment']}")
    with col2:
        st.markdown(f"**Toxicity:** {result['toxicity']}")
    with col3:
        st.markdown(f"**Risk Score:** <span style='color:{get_color(result['risk_score'])}'>{result['risk_score']}</span>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"**Fake News Probability:** <span style='color:{get_color(result['fake_news_prob'])}'>{result['fake_news_prob']}%</span>", unsafe_allow_html=True)
    
    # ---- Pie Chart ----
    st.subheader("Visual Overview")
    labels = ['Risk Score', 'Fake News Probability', 'Toxicity Level']
    values = [result['risk_score'], result['fake_news_prob'], {"Low":20,"Medium":50,"High":80}[result['toxicity']]]
    
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax1.axis('equal')
    st.pyplot(fig1)
    
    # ---- Bar Chart ----
    st.subheader("Bar Chart Overview")
    df = pd.DataFrame({
        "Metric": ["Risk Score","Fake News","Toxicity"],
        "Value": [result['risk_score'], result['fake_news_prob'], {"Low":20,"Medium":50,"High":80}[result['toxicity']]]
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
