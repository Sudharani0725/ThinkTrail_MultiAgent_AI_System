# ThinkTrail – From Questions to Insights

**ThinkTrail** is an AI-powered research assistant that automates web research through a four-stage AI pipeline. It searches the web for relevant information, extracts content from selected webpages, generates structured research reports, and evaluates the generated reports using an AI-powered critic.

Built using Python, LangChain, Google Gemini, Tavily, and Streamlit, ThinkTrail transforms research questions into organized insights.

---

## Problem Statement

Researching a topic often requires searching multiple websites, reading lengthy articles, collecting relevant information, and organizing findings into a structured report. This process can be time-consuming and requires considerable manual effort.

ThinkTrail addresses this challenge by automating these activities through AI-powered agents and LLM chains, making research more efficient and organized.

## Objectives

- Automate web research using AI-powered agents.
- Retrieve relevant information from web sources.
- Extract useful content from selected webpages.
- Generate structured and informative research reports.
- Evaluate generated reports using an AI-powered critic.
- Provide an interactive interface for conducting research.

## Key Features

- **Automated Web Search:** Retrieves up to five search results using Tavily, including titles, URLs, and content snippets.
- **Web Content Extraction:** Extracts readable webpage content using Requests and BeautifulSoup.
- **AI-Powered Report Generation:** Generates structured research reports using Google Gemini.
- **AI-Based Evaluation:** Reviews generated reports and provides scores, strengths, improvement suggestions, and an overall verdict.
- **Source Collection:** Displays URLs identified during the research process.
- **Interactive Dashboard:** Provides a Streamlit interface with a four-stage progress tracker.
- **Research Results:** Displays reports, critic feedback, sources, search results, and scraped content in separate tabs.
- **Report Download:** Allows users to download generated reports in Markdown format.
- **Scraping Fallback:** Attempts alternative URLs when the Reader Agent cannot successfully scrape content in the Streamlit workflow.

## System Architecture

ThinkTrail follows a four-stage AI research pipeline consisting of **two tool-using agents and two LLM chains**.

### 1. Search Agent

- Built using LangChain's `create_agent`.
- Uses the custom `web_search` tool.
- Integrates Tavily to retrieve relevant web search results.
- Returns titles, URLs, and content snippets.

### 2. Reader Agent

- Built using LangChain's `create_agent`.
- Uses the custom `scrape_url` tool.
- Integrates Requests and BeautifulSoup for webpage extraction.
- Removes unnecessary HTML elements such as scripts, styles, navigation, and footers.
- Extracts readable text from selected webpages.

### 3. Writer Chain

- Built using LangChain Expression Language (LCEL).
- Uses `ChatPromptTemplate` and Google Gemini.
- Combines search results and extracted webpage content.
- Generates a structured report containing:
  - Introduction
  - Key Findings
  - Conclusion
  - Sources

### 4. Critic Chain

- Built using LangChain Expression Language (LCEL).
- Reviews the generated research report using Google Gemini.
- Provides a score out of 10.
- Identifies strengths and areas for improvement.
- Generates an overall verdict.

## Workflow

1. User enters a research topic through the Streamlit interface.
2. Search Agent searches the web using Tavily.
3. Reader Agent selects a relevant URL and extracts webpage content.
4. Writer Chain combines the collected information and generates a structured research report.
5. Critic Chain evaluates the generated report.
6. Streamlit displays the report, evaluation, sources, search results, and scraped content.
7. User can download the generated report as a Markdown file.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM | Google Gemini |
| AI Framework | LangChain |
| Agent Creation | LangChain `create_agent` |
| Prompt Engineering | ChatPromptTemplate |
| Chain Composition | LangChain Expression Language (LCEL) |
| Output Parsing | StrOutputParser |
| Web Search | Tavily API |
| Web Scraping | Requests, BeautifulSoup4, lxml |
| Frontend | Streamlit |
| Environment Management | uv, Python Virtual Environment |
| Configuration | python-dotenv |
| Data Validation | Pydantic |
| Terminal Formatting | Rich |

## Project Structure

```text
ThinkTrail_MultiAgent_AI_System/
│
├── app.py                 # Streamlit application
├── agents.py              # Agent and LLM chain definitions
├── pipeline.py            # Research pipeline orchestration
├── tools.py               # Web search and scraping tools
├── requirements.txt       # Project dependencies
├── .env                   # API keys (not uploaded to GitHub)
├── .gitignore              # Git ignored files
└── README.md              # Project documentation
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- uv package manager
- Google Gemini API key
- Tavily API key

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ThinkTrail_MultiAgent_AI_System
```

### 2. Create a Virtual Environment

```bash
uv venv .venv
```

### 3. Activate the Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your API keys:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholders with your actual API keys.

**Important:** Never upload your `.env` file to GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser.

### Alternative: Run Through the Terminal

You can also execute the command-line research pipeline:

```bash
python pipeline.py
```

Enter your research topic when prompted.

## Application Screenshots

Screenshots of the ThinkTrail application will be added here.

<!-- Add screenshots of the dashboard, generated report, and critic feedback here. -->

## Testing and Validation

ThinkTrail was tested using three different research scenarios:

| Test | Research Topic | Outcome |
|---|---|---|
| Test 01 | Multi-agent AI systems in software development and automation | Successful execution; report generated and critic feedback received |
| Test 02 | RAG vs. Fine-Tuning in Large Language Models | Successful execution; technical report and evaluation generated |
| Test 03 | Exact number of AI-powered software engineering startups founded in Bidar during October 2026 | Pipeline executed, but the generated numerical conclusion was not sufficiently supported by evidence |

Testing demonstrated that the complete research pipeline works end to end. It also identified opportunities to improve source reliability, factual verification, and uncertainty handling.

## Limitations

- Search results may contain unreliable or outdated information.
- Only selected webpages are scraped for deeper research.
- Some websites may block automated scraping.
- Generated reports may contain unsupported factual claims.
- The critic may not identify every factual error.
- The current pipeline does not perform independent verification of every generated claim.
- Research quality depends on the relevance and reliability of retrieved information.

## Future Enhancements

- Retrieve and analyze multiple relevant webpages.
- Implement source-based citations for individual claims.
- Introduce evidence-based factual verification.
- Improve critic evaluation and reliability.
- Add an explicit insufficient-evidence response for unverifiable queries.
- Improve search result filtering and source selection.
- Add research history and report management.
- Deploy the application for public access.

## Author

**Sudharani**

- GitHub: [Sudharani0725](https://github.com/Sudharani0725)
- LinkedIn: [Sudharani](https://www.linkedin.com/in/sudharani-014933318/)

---

*ThinkTrail – From Questions to Insights.*