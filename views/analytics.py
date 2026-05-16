import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    try:
        return pd.read_csv('dataset.csv')
    except:
        return pd.DataFrame()

def render():
    st.markdown("<h2 class='title-text'>📈 Global Healthcare Analytics</h2>", unsafe_allow_html=True)
    df = load_data()
    
    if df.empty:
        st.error("No dataset available.")
        return
        
    # Top metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Average Global Treatment Cost", f"${df['Treatment_Cost'].mean():,.0f}")
    c2.metric("Most Popular Destination", df['Country'].mode()[0])
    c3.metric("Highest Request Disease", df['Disease'].mode()[0])
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Patient Count by Country")
        fig1 = px.bar(df['Country'].value_counts().reset_index(), x='Country', y='count', color='Country')
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Cost Distribution by Disease")
        fig2 = px.box(df, x='Disease', y='Total_Cost', color='Disease')
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Cost Heatmap: Stay Days vs Cost")
    # Simplify scatter for performance
    fig3 = px.scatter(df.sample(2000), x='Stay_Days', y='Total_Cost', color='Hospital_Type', size='Treatment_Cost', hover_data=['Country'])
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
