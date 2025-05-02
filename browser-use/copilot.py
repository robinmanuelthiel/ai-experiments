from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
import asyncio
from dotenv import load_dotenv

load_dotenv()

browser = Browser(
    config=BrowserConfig(
        browser_binary_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    )
)

async def main():
    agent = Agent(
        task=(
            "Open Microsoft Teams at https://teams.microsoft.com/. "
            "If required, login with my @microsoft.com account. "
            "Enter the following prompt as a message: "
            "'What emails should be on my radar? Focus on those that seem urgent, important or are from my manager.' "
            "Send the message and wait for the response. "
            "Take a screenshot of the response."
        ),
        browser=browser,
        llm=ChatOpenAI(model="gpt-4.1"),
    )
    await agent.run()

asyncio.run(main())
