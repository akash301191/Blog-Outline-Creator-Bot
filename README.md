# Blog Outline Creator Bot

Blog Outline Creator Bot is an intelligent blog-planning assistant that helps bloggers and content marketers craft structured, SEO-informed blog outlines based on their topic, audience, tone, and goals. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot analyzes top-ranking web content and transforms your idea into a high-impact, ready-to-write blog blueprint.

## Folder Structure

```
Blog-Outline-Creator-Bot/
├── blog-outline-creator-bot.py
├── README.md
└── requirements.txt
```

* **blog-outline-creator-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Blog Preferences Input**
  Capture blog topic, target audience, tone, purpose, word count, and structure preferences.

* **Web-Based Article Research**
  The Blog Researcher agent performs a focused Google search to find high-performing articles that inform real-world structure and style.

* **AI-Powered Outline Generator**
  The Blog Outliner agent analyzes the best content formats and transforms your idea into a section-wise outline tailored to your goals.

* **Structured Markdown Output**
  The outline is rendered in clean, sectioned Markdown with brief descriptions under each heading, suitable for direct drafting.

* **Download Option**
  Download the outline as a `.txt` file to start writing your blog right away.

* **Intuitive Streamlit UI**
  Built using Streamlit for a clean, responsive, and minimal interface.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Blog-Outline-Creator-Bot.git
   cd Blog-Outline-Creator-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run blog-outline-creator-bot.py
   ```

2. **In your browser**:

   * Enter your OpenAI and SerpAPI keys in the sidebar.
   * Fill in your blog topic, audience, tone, and format preferences.
   * Click **📝 Generate Blog Outline**.
   * View your AI-generated outline and download it for use.

3. **Download Option**
   Use the **📥 Download Blog Outline** button to save your outline as a `.txt` file.

## Code Overview

* **`render_blog_outline_inputs()`**: Captures user inputs like topic, tone, audience, word count, and optional notes.
* **`render_sidebar()`**: Collects OpenAI and SerpAPI credentials via Streamlit sidebar.
* **`generate_blog_outline()`**:

  * Uses the **Blog Researcher** agent to find article structures from trusted web sources.
  * Passes results to the **Blog Outliner** agent to generate a clear, section-wise blog plan.
* **`main()`**: Lays out the UI, processes the input, and manages the overall flow from input to download.

## Contributions

Contributions are welcome! Feel free to fork the repo, report bugs, suggest features, or open a pull request. Make sure your updates are clean, well-documented, and align with the app’s purpose.