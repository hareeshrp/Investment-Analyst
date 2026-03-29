import asyncio
from sys import exception
from agents import Runner, trace, gen_trace_id
from analyst_planner import analyst_planner
from finance_searcher import finance_searcher
from report_writer import report_writer, InvestmentMemo
from email_agent import email_agent
class FinanceManager:
    async def run(self, query: str):
        trace_id = gen_trace_id()
        # Initial status update for Gradio
        yield f"🚀 Starting Market Analysis for: {query}... (Trace: {trace_id})"
        
        with trace("Finance Analysis", trace_id=trace_id):
            # 1. PLAN: Generate the 5-step research plan
            # We append 'Indian Stock Market' to the query to force context
            plan_input = f"Analyze the Indian company: {query}"
            res = await Runner.run(analyst_planner, plan_input)
            plan = res.final_output
            yield "📅 Research plan generated. Identifying key Indian financial metrics..."

            # 2. PARALLEL SEARCH: Execute searches across NSE/BSE sources
            # We add 'NSE India' to each query to ensure we don't get US data
            tasks = [
                Runner.run(finance_searcher, f"{s.query} NSE India") 
                for s in plan.searches
            ]
            
            search_results = []
            num_completed = 0
            
            # Using as_completed to update Gradio in real-time as each search finishes
            for task in asyncio.as_completed(tasks):
                result = await task
                if result and result.final_output:
                    search_results.append(str(result.final_output))
                num_completed += 1
                yield f"🔍 Search progress: {num_completed}/{len(tasks)} completed..."

            # 3. WRITE: Synthesize the final Investment Memo
            yield "✍️ Search complete. Report Writer is synthesizing the thesis..."
            
            # Prepare the rich context for the writer
            writer_input = (
                f"Original Company: {query}\n"
                f"Market: Indian Stock Market (NSE/BSE)\n"
                f"Research Data: {' '.join(search_results)}"
            )
            
            final_res = await Runner.run(report_writer, writer_input)
            
            # Use the output_type we defined in report_writer.py
            report = final_res.final_output_as(InvestmentMemo)

            #4. Send email
            yield "Sending report via email"
            email_input = (f"Subject: Investment Analysis for {query}\n"
            f"Content: {report.markdown_report}")

            try:
                await Runner.run(email_agent, email_input)
                yield "Report sent to email successfully!!"

            except Exception as e:
                yield f"Email failed: {str(e)}"
                
            # We yield the markdown_report which Gradio will render
            yield report.markdown_report