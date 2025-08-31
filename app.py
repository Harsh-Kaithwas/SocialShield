import streamlit as st

st.set_page_config(page_title="SocialShield", layout="wide")
st.title("SocialShield – Social Media Impact Assessment (Prototype)")
st.write("Prototype Dashboard: 4 Dimensions Placeholder")

# 4 columns for 4 dimensions
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Mental Stress & Addiction")
    st.metric(label="Score", value="--", delta="--")

with col2:
    st.subheader("Fake News & Misinformation")
    st.metric(label="Score", value="--", delta="--")

with col3:
    st.subheader("Privacy & Data Risk")
    st.metric(label="Score", value="--", delta="--")

with col4:
    st.subheader("Reputation / Cancel Culture")
    st.metric(label="Score", value="--", delta="--")

st.write("Status: Placeholders only. Scores will appear after integration.")
