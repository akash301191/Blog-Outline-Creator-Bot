import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_blog_outline_inputs():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Topic & Audience
    with col1:
        st.subheader("🧠 Topic & Audience")
        topic = st.text_input("Blog Topic*", placeholder="e.g., How to build healthy habits")
        audience = st.text_input("Target Audience*", placeholder="e.g., Busy professionals in their 30s")
        domain = st.selectbox(
            "Industry/Domain (optional)",
            ["General", "Health", "Technology", "Education", "Finance", "Travel", "Lifestyle", "Marketing", "Other"]
        )

    # Column 2: Style & Intent
    with col2:
        st.subheader("✍️ Style & Intent")
        tone = st.selectbox(
            "Desired Tone*",
            ["Informative", "Conversational", "Persuasive", "Professional", "Witty", "Inspirational"]
        )
        point_of_view = st.selectbox(
            "Point of View",
            ["First-person (I/we)", "Second-person (you)", "Third-person (they)", "No preference"]
        )
        intent = st.selectbox(
            "Primary Intent*",
            ["Educate", "Drive traffic", "Promote a product", "Engage audience", "Establish authority"]
        )

    # Column 3: Format & Notes (simplified to 3 select/text fields)
    with col3:
        st.subheader("📐 Format & Notes")
        word_count = st.selectbox(
            "Preferred Word Count*",
            ["500–800", "800–1200", "1200–1500", "1500+"]
        )
        include_faq = st.selectbox(
            "Include FAQ Section?",
            ["Yes", "No"]
        )
        notes = st.text_input("Key Subtopics or Notes (optional)", placeholder="e.g., Mention habit-building apps")

    # Compile user blog input profile
    blog_outline_preferences = f"""
**Topic & Audience:**
- Blog Topic: {topic}
- Target Audience: {audience}
- Industry/Domain: {domain}

**Style & Intent:**
- Tone: {tone}
- Point of View: {point_of_view}
- Purpose: {intent}

**Format Preferences:**
- Word Count: {word_count}
- Include FAQ: {include_faq}
- Notes: {notes if notes.strip() else "None"}
"""

    return blog_outline_preferences

def generate_blog_outline(user_blog_preferences: str) -> str:
    # Step 1: Run Blog Researcher Agent
    research_agent = Agent(
        name="Blog Researcher",
        role="Finds high-performing blog examples and article structures based on the user’s topic, tone, and audience.",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a blog research expert. Your job is to help writers plan strong blog outlines by analyzing top-ranking posts.
            Using the user’s topic, tone, audience, and format preferences, generate a focused blog search query, search the web, and extract article links that reflect good structure, headings, and flow.
        """),
        instructions=[
            "Carefully read the user's blog preferences to understand the topic, audience, tone, and intent.",
            "Generate ONE specific search query (e.g., 'best blog articles on morning routines for busy professionals').",
            "Avoid generic or broad queries. Focus on the core topic and audience.",
            "Use `search_google` with your query.",
            "From the results, extract 8–10 high-quality links to real blog articles, preferably from SEO-rich or trusted platforms like HubSpot, Medium, Backlinko, Neil Patel, Ahrefs, Buffer, etc.",
            "Only return real URLs or article titles. Do NOT generate or invent sample blogs.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    )

    research_response = research_agent.run(user_blog_preferences)
    research_results = research_response.content

    # Step 2: Run Blog Outliner Agent
    outliner_agent = Agent(
        name="Blog Outliner",
        role="Generates a structured blog outline based on user preferences and real article formats found online.",
        model=OpenAIChat(id='o3-mini', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a blog planning assistant. Your job is to generate a blog outline using:
            1. The user's blog preferences (topic, tone, audience, length, structure).
            2. A list of reference articles from top-performing blog content.

            You must return a clear section-wise outline with brief descriptions and suggested headings.
        """),
        instructions=[
            "Review the user's preferences in detail: topic, audience, tone, format, purpose, and any specific notes.",
            "Explore the reference URLs provided from the research agent.",
            "Extract useful section formats and apply them creatively to the new outline.",
            "Ensure that the outline is well-paced, logically structured, and tailored to the audience/tone.",
            "Use the following format for each section:\n"
            "### [Section Title]\n"
            "*Description of what goes in this section in 4–5 bullet points*",
            "Include 6–10 sections depending on preferred length.",
            "If the user requested FAQ, include a final section titled 'Frequently Asked Questions'.",
            "Do not include actual article text from the links. Only extract ideas or structure.",
            "Start directly with '## 📝 Blog Outline' as the header — no intro or closing remarks.",
            "Ensure the outline is clear, practical, and aligned with blog-writing best practices.",
        ],
        add_datetime_to_instructions=True,
    )

    outliner_input = f"""
User's Blog Preferences:
{user_blog_preferences}

Research Results:
{research_results}

Use these details to generate a structured blog outline.
"""

    outliner_response = outliner_agent.run(outliner_input)
    outline_report = outliner_response.content

    return outline_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Blog Outline Creator Bot", page_icon="📝", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>📝 Blog Outline Creator Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Blog Outline Creator Bot — an intelligent blog-planning assistant that analyzes top-ranking articles and transforms your idea into a structured, high-impact blog blueprint tailored to your audience and goals.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_blog_preferences = render_blog_outline_inputs()
    
    st.markdown("---")

    if st.button("📝 Generate Blog Outline"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Drafting a structured outline for your blog..."):
                blog_outline = generate_blog_outline(user_blog_preferences)
                st.session_state.blog_outline = blog_outline

    if "blog_outline" in st.session_state:
        st.markdown(st.session_state.blog_outline, unsafe_allow_html=True)
        st.markdown("---")

        st.download_button(
            label="📥 Download Blog Outline",
            data=st.session_state.blog_outline,
            file_name="blog_outline.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()