import os
from typing import Dict
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = Email("hareeshkanna2002@gmail.com")  # put your verified sender here
    to_email = To("hareeshkanna2002@gmail.com")  # put your recipient here
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return "success"


INSTRUCTIONS = """You take a Markdown investment report and convert it into a 
clean, professional HTML email. Use standard HTML tags (<h1>, <p>, <li>). 
Make the 'BUY/HOLD/SELL' recommendation bold and prominent. 
Send exactly one email with a subject line like 'Investment Research: [Ticker Symbol]'."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
