import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="YouTube Creator Dashboard", page_icon="📊", layout="wide")

# Title of the dashboard
st.title("📊 YouTube Creator Analytics Dashboard")
st.markdown("Track your channel's performance, engagement, and growth in real-time.")
st.markdown("---")

# 1. Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("youtube_data.csv")
    return df

df = load_data()

# 2. Sidebar Filter Section
st.sidebar.header("🎯 Filter Options")

# Category filter (Multi-select)
all_categories = df["Category"].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Select Video Category:",
    options=all_categories,
    default=all_categories
)

# Filtering the dataframe based on selection
filtered_df = df[df["Category"].isin(selected_categories)]

# Show raw data checkbox in sidebar
if st.sidebar.checkbox("Show Raw Dataset", False):
    st.subheader("📁 Raw Analytics Data")
    st.dataframe(filtered_df)

# 3. KPI Metrics Section (Summary Cards)
st.subheader("📈 Channel Performance Overview")

total_views = int(filtered_df["Views"].sum())
total_likes = int(filtered_df["Likes"].sum())
total_comments = int(filtered_df["Comments"].sum())
total_watch_time = int(filtered_df["Watch_Time_Hours"].sum())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Views 👁️", value=f"{total_views:,}")

with col2:
    st.metric(label="Total Likes 👍", value=f"{total_likes:,}")

with col3:
    st.metric(label="Total Comments 💬", value=f"{total_comments:,}")

with col4:
    st.metric(label="Watch Time (Hrs) ⏱️", value=f"{total_watch_time:,}")

st.markdown("---")

# 4. Charts Section
st.subheader("📊 Visualizing Video Performance")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### 🚀 Views per Video")
    # UPDATED: Added height and margin to fix the top video cutoff bug
    fig_bar = px.bar(
        filtered_df,
        x="Views",
        y="Video_Title",
        orientation="h",
        color="Category",
        text="Views",
        labels={"Video_Title": "Video Title", "Views": "Total Views"},
        template="plotly_dark"
    )
    fig_bar.update_layout(
        yaxis={'categoryorder':'total ascending'},
        height=500,  # Isse gap badhega aur top video sahi dikhegi
        margin=dict(l=200, r=20, t=40, b=40)  # Left margin bade names ke liye
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.markdown("### 💡 Engagement by Category (Likes)")
    fig_pie = px.pie(
        filtered_df,
        values="Likes",
        names="Category",
        hole=0.4,
        template="plotly_dark"
    )
    fig_pie.update_layout(height=500)
    st.plotly_chart(fig_pie, use_container_width=True)

# 5. Advanced Data Insights Section
st.markdown("---")
st.subheader("🎯 Smart Creator Insights")

if not filtered_df.empty:
    top_video = filtered_df.loc[filtered_df["Views"].idxmax()]
    st.info(f"🏆 **Top Performing Content:** '{top_video['Video_Title']}' is currently your best performing video in the selected categories with **{top_video['Views']:,} views**!")
else:
    st.warning("Please select at least one category to see insights.")