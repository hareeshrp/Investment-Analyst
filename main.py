import gradio as gr
import asyncio
from dotenv import load_dotenv
from finance_manager import FinanceManager

load_dotenv(override=True)

async def analyze(query):
    async for status in FinanceManager().run(query):
        yield status

with gr.Blocks(theme=gr.themes.Soft()) as ui:
    gr.Markdown("# 📈 Multi-Agent Investment Analyst")
    ticker = gr.Textbox(label="Enter Company or Ticker")
    btn = gr.Button("Analyze", variant="primary")
    output = gr.Markdown()
    
    btn.click(fn=analyze, inputs=ticker, outputs=output)

if __name__ == "__main__":
    ui.launch()