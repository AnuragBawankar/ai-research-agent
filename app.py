import streamlit as st
from dotenv import load_dotenv
from tavily import TavilyClient
from openai import OpenAI
import os

load_dotenv()

# API Clients
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="AI Research Agent")
st.title("🔎 AI Research Agent")

topic = st.text_input(
    "Enter a research topic:",
    placeholder="AI Chatbots for Healthcare Clinics"
)

if st.button("Generate Research Report"):

    if not topic:
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("Researching..."):

        # Search web
        search_results = tavily.search(
            query=topic,
            search_depth="advanced",
            max_results=5
        )

        content = ""

        for result in search_results["results"]:
            content += f"""
Title: {result['title']}
URL: {result['url']}
Content: {result['content']}

"""

        # Generate report
        prompt = f"""
You are a professional market research analyst.

Create a detailed report on:

{topic}

Using the research below.

Research:
{content}

Structure the report as:

1. Executive Summary
2. Key Trends
3. Major Players
4. Opportunities
5. Risks
6. Recommendations
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert business analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        report = response.choices[0].message.content

        st.subheader("Research Report")
        st.markdown(report)

        st.subheader("Sources")

        for result in search_results["results"]:
            st.markdown(
                f"- [{result['title']}]({result['url']})"
            )