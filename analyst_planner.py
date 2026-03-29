from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """You are an expert SEBI-registered Research Analyst. 
For an Indian stock, generate 5 search queries focusing on:
1. Latest Annual Report and Quarter Results (from NSE/BSE or Company Investor Relations).
2. Management Commentary/Concall transcripts from platforms like Screener.in or Trendlyne.
3. Industry analysis (e.g., PLI schemes, RBI policy impact, or sectoral tailwinds).
4. Shareholding pattern (Promoter pledging and FII/DII inflows).
5. Peer comparison with other Indian listed companies (e.g., if analyzing HDFC, compare with ICICI)."""

class SearchItem(BaseModel):
    reason: str = Field(description="Why this data is needed.")
    query: str = Field(description="The search term.")

class FinancePlan(BaseModel):
    searches: list[SearchItem]

analyst_planner = Agent(
    name="Analyst Planner",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=FinancePlan
)