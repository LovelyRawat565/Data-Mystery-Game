import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Page config
st.set_page_config(page_title="Data Mystery Room", page_icon="🕵️‍♂️", layout="wide")

# Title and Story
st.title("🕵️‍♂️ The Great Diamond Heist: A Data Mystery")
st.markdown("""
---
### 🚨 THE CASE FILE:
Yesterday at **17:15 PM**, the famous *Star of India* diamond was stolen from the royal showroom safe. 
The security systems recorded every single movement. As the **Lead Data Detective**, your job is to upload the raw security CSV logs, analyze the charts, and catch the thief!

⏱️ **🚨 NEW TWIST:** The thief is trying to erase the backup servers! You only have **60 seconds** to lock your answer once the data is uploaded. Hurry up!
---
""")

# Initialize session state for timer
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# File Uploader
uploaded_file = st.file_uploader("Upload 'security_logs.csv' to unlock the clues", type=["csv"])

if uploaded_file is not None:
    # Set start time when file is first uploaded
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
        
    # Calculate time remaining
    elapsed_time = time.time() - st.session_state.start_time
    time_remaining = int(60 - elapsed_time)
    
    if time_remaining <= 0:
        st.error("🚨 TIME'S UP! The thief successfully wiped the servers and escaped! 🏃‍♂️💨")
        
        # Naya Restart Button
        if st.button("🔄 Restart Game"):
            st.session_state.start_time = None
            st.rerun()
            
        st.stop()
    else:
        # Show a warning and a progress bar for the timer
        st.warning(f"⏳ **Time Remaining to solve the case: {time_remaining} seconds!**")
        st.progress(max(0, min(time_remaining / 60, 1.0)))
        
        # Add a quick rerun button to refresh the timer screen manually if needed
        if st.button("🔄 Refresh Timer Clock"):
            st.rerun()

    df = pd.read_csv(uploaded_file)
    st.success("📁 Security logs loaded successfully! Analyze the patterns below quickly!")
    
    # Layout with Columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Room Access Frequency")
        fig1 = px.bar(df, x="Location", color="Employee_Name", title="Who was hanging around where?", barmode="group")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.subheader("🔒 Access Card Status (Authorized vs Denied)")
        fig2 = px.histogram(df, x="Employee_Name", color="Card_Status", title="Any suspicious Denied access?")
        st.plotly_chart(fig2, use_container_width=True)

    # Raw Data View with filter
    st.subheader("🔍 Filter Logs by Employee")
    selected_emp = st.selectbox("Select a suspect to track their steps:", ["All"] + list(df["Employee_Name"].unique()))
    
    if selected_emp != "All":
        filtered_df = df[df["Employee_Name"] == selected_emp]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
        
    # Solution Zone
    st.markdown("---")
    st.subheader("🎯 Lock Your Final Answer")
    
    thief_guess = st.selectbox("Who do you think stole the diamond?", ["Select Suspect", "Rohan Sharma", "Amit Verma", "Priya Patel", "Vikram Singh"])
    
    if thief_guess == "Vikram Singh":
        st.balloons()
        st.success(f"🎉 EXCELLENT WORK DETECTIVE! You caught Vikram Singh with {time_remaining} seconds left! Case Closed! 🏆")
        # Reset timer after winning
        st.session_state.start_time = None
    elif thief_guess != "Select Suspect":
        st.error("❌ Wrong Suspect! Look closely at the 'Card_Status' graph. Time is ticking! Try again!")

else:
    # Clear timer state if file is removed
    st.session_state.start_time = None
    st.info("💡 Awaiting security log file. Please upload 'security_logs.csv' to begin the investigation.")