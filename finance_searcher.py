from agents import Agent, WebSearchTool, ModelSettings

INSTRUCTIONS = """You are a Financial Data Extractor. 
Summarize search results into concise, data-heavy paragraphs. 
Focus on Revenue, EBITDA, Risks, and Market Share. Ignore fluff."""

finance_searcher = Agent(
    name="Finance Searcher",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)