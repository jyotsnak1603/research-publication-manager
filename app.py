import streamlit as st
import pandas as pd
import plotly.express as px
from db_utils import fetch_dataframe, add_publication, assign_author
from streamlit_lottie import st_lottie
import json, os

# --- Load Lottie Files ---
def load_lottie(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        st.warning(f"Lottie animation not found: {path}")
        return None

anim_dashboard = load_lottie("lottie-dashboard.json")
anim_add = load_lottie("lottie-add-publication.json")
anim_faculty = load_lottie("lottie-faculty.json")
anim_recent = load_lottie("lottie-recent.json")

# --- Custom CSS Styling ---
def local_css(css_text):
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)

custom_style = """
    .reportview-container {
        background: linear-gradient(to right, #f0f2f6, #dfe9f3);
    }
    .stButton>button {
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        padding: 6px 12px;
    }
"""
local_css(custom_style)

st.set_page_config(layout="wide")
st.title("📚 Research Project & Publication Manager")

# --- User Role (optional simulation) ---
role = st.sidebar.selectbox("Select Role", ["Admin", "Faculty", "Student"])
if role == "Student":
    st.warning("🔒 Restricted features are hidden in Student View")

menu = st.sidebar.radio("Navigation", ["Dashboard", "Add Publication", "Faculty Insights", "Recent Activity"])

# --- Dashboard Page ---
if menu == "Dashboard":

    tab1, tab2, tab3 = st.tabs(["📈 Yearly Trends", "📊 Category Distribution", "📁 Type Distribution"])

    with tab1:
        df = fetch_dataframe("SELECT * FROM publications_by_year")
        st.subheader("Year-wise Publications")
        fig = px.bar(df, x='PUBLICATION_YEAR', y='PUBLICATION_COUNT', text='PUBLICATION_COUNT',
                     color='PUBLICATION_YEAR', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Yearly Report", csv, "yearly_report.csv", "text/csv")

    with tab2:
        df2 = fetch_dataframe("""
            SELECT category, COUNT(*) AS count
            FROM publication
            GROUP BY category
            ORDER BY count DESC FETCH FIRST 5 ROWS WITH TIES
        """)
        st.subheader("Top 5 Categories")
        fig = px.pie(df2, names='CATEGORY', values='COUNT', title="Publication Categories")
        st.plotly_chart(fig)

    with tab3:
        df3 = fetch_dataframe("""
            SELECT publication_type, COUNT(*) AS count 
            FROM publication 
            GROUP BY publication_type
        """)
        fig = px.pie(df3, names='PUBLICATION_TYPE', values='COUNT', hole=0.5,
                     title="Publication Type (Donut)")
        st.plotly_chart(fig)

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Publications", int(df['PUBLICATION_COUNT'].sum()))
    col2.metric("Top Category", df2['CATEGORY'][0])
    top_faculty_df = fetch_dataframe("SELECT * FROM top_contributing_faculty")
    col3.metric("Top Faculty", top_faculty_df['FACULTY_NAME'][0])

    if anim_dashboard:
        st_lottie(anim_dashboard, height=180, key="dash_anim")

# --- Add Publication Page ---
elif menu == "Add Publication" and role != "Student":
    st.subheader("➕ Add a New Publication")
    with st.form("pub_form"):
        pub_id = st.text_input("Publication ID")
        title = st.text_input("Title")
        summary = st.text_area("Summary")
        category = st.text_input("Category")
        pub_type = st.selectbox("Type", ["Journal", "Conference", "Workshop"])
        pub_date = st.date_input("Published Date")
        status = st.selectbox("Status", ["Draft", "Accepted", "Published"])

        author_type = st.selectbox("Author Type", ["faculty", "student"])
        if author_type == "faculty":
            authors_df = fetch_dataframe("SELECT faculty_id AS id, name FROM faculty")
        else:
            authors_df = fetch_dataframe("SELECT student_id AS id, name FROM student")

        author_name = st.selectbox("Select Author", authors_df['NAME'])
        author_id = authors_df[authors_df['NAME'] == author_name]['ID'].values[0]

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not pub_id or not title:
                st.warning("⚠️ Please fill in all required fields.")
            else:
                result = add_publication(pub_id, title, summary, category, pub_type, pub_date, status)
                if result == True:
                    assign_result = assign_author(pub_id, int(author_id), author_type)
                    if assign_result == True:
                        st.success("✅ Publication added and author assigned successfully!")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ Publication added, but author assignment failed: {assign_result}")
                else:
                    st.error(f"❌ Failed to add publication: {result}")

    if anim_add:
        st_lottie(anim_add, height=180, key="add_anim")

# --- Faculty Insights Page ---
elif menu == "Faculty Insights":
    if anim_faculty:
        st_lottie(anim_faculty, height=180, key="faculty_anim")

    st.subheader("🏆 Top Contributing Faculty")
    df3 = fetch_dataframe("SELECT * FROM top_contributing_faculty")
    st.dataframe(df3, use_container_width=True)

    fig2 = px.bar(df3, x='TOTAL_PUBLICATIONS', y='FACULTY_NAME', orientation='h', color='TOTAL_PUBLICATIONS',
                  color_continuous_scale='Bluered')
    st.plotly_chart(fig2)

# --- Recent Activity Page ---
elif menu == "Recent Activity":
    st.subheader("🕒 Recently Updated Publications")
    df4 = fetch_dataframe("SELECT * FROM recent_publications")
    st.dataframe(df4, use_container_width=True)

    if anim_recent:
        st_lottie(anim_recent, height=180, key="recent_anim")
