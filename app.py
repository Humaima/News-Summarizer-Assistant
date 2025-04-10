# Add this at the very top
import asyncio
import sys
import os

# Fix for Streamlit on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Workaround for PyTorch issues
os.environ["STREAMLIT_PYTHON_LOG_LEVEL"] = "ERROR"
import torch
torch._C._set_grad_enabled(False)

import streamlit as st
from news_fetcher import NewsFetcher
from vector_db import VectorDB
from summarizer import NewsSummarizer
from config import Config
import time

# Initialize components
@st.cache_resource
def init_components():
    try:
        return {
            "fetcher": NewsFetcher(),
            "vector_db": VectorDB(),
            "summarizer": NewsSummarizer()
        }
    except Exception as e:
        st.error(f"Initialization failed: {str(e)}")
        st.stop()

# App layout
st.set_page_config(
    page_title="News Summarizer Assistant",
    page_icon="📰",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .stTextInput input {
        font-size: 18px;
        padding: 10px;
    }
    .stButton button {
        width: 100%;
        padding: 10px;
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
    }
    .stMarkdown h1 {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# Main header
st.title("📰 Personalized News Summarizer")
st.markdown("Enter any topic you're interested in below")

# Initialize components
components = init_components()

# Search form
with st.form("news_search_form"):
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        user_query = st.text_input(
            "What news are you looking for?", 
            placeholder="e.g., artificial intelligence, climate change, sports"
        )
    
    with col2:
        lang = st.selectbox("Language", ["en", "es", "fr", "de", "it"], index=0)
    
    with col3:
        country = st.selectbox("Country", ["us", "gb", "in", "ca", "au"], index=0)
    
    search_button = st.form_submit_button("Get News Summaries")

# Display results
if search_button:
    if not user_query.strip():
        st.warning("Please enter a search term")
        st.stop()
    
    with st.spinner(f"Finding the latest news about '{user_query}'..."):
        try:
            # Fetch news based on user query
            articles = components["fetcher"].fetch_news(
                query=user_query,
                lang=lang,
                country=country,
                max_results=5
            )
            
            if not articles:
                st.warning(f"No articles found about '{user_query}'. Try different search terms.")
                st.stop()
                
            # Process articles
            documents = [f"{article['title']}\n{article['description']}" for article in articles]
            components["vector_db"].create_db(documents)
            
            # Display results
            st.success(f"Showing {len(articles)} results for: {user_query}")
            
            for i, article in enumerate(articles):
                with st.container():
                    # Article header
                    st.subheader(f"{article['title']}")
                    
                    # Columns for content
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.caption(f"📅 {article['publishedAt']}")
                        st.markdown(f"🔗 [Read full article]({article['url']})")
                        
                        # Show summary
                        with st.expander("✨ AI Summary"):
                            content = f"{article['title']}\n{article['description']}\n{article.get('content', '')}"
                            summary = components["summarizer"].summarize(content)
                            st.write(summary)
                    
                    with col_b:
                        if article.get('image'):
                            st.image(article['image'], width=150)
                    
                    # Show similar articles
                    similar = components["vector_db"].search(article['title'])
                    if similar:
                        with st.expander("🔍 Related articles"):
                            for sim_article in similar[:2]:
                                st.write(sim_article.split('\n')[0])
                    
                    st.divider()
                    
        except Exception as e:
            st.error(f"Error processing news: {str(e)}")