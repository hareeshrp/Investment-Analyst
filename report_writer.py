from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """You are a Senior Fund Manager at an Indian AMC. 
Write a detailed investment memo in Markdown. 
Requirements:
1. Use ₹ (INR) and Crores/Lakhs for all currency values.
2. Include a section on 'Promoter Quality & Pledging'.
3. Mention specific Indian macro factors (GST impact, Monsoon, Budget/Tax changes).
4. Provide a Bull vs Bear case and a Rating (BUY/HOLD/SELL).
Use tables for P/E, Price/Book, and Dividend Yield."""

class InvestmentMemo(BaseModel):
    recommendation: str = Field(description="BUY, HOLD, or SELL")
    markdown_report: str = Field(description="The full report in Markdown")

report_writer = Agent(
    name="Report Writer",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=InvestmentMemo
)