from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
import asyncio
from dotenv import load_dotenv

load_dotenv()

controller = Controller()
browser = Browser(
    config=BrowserConfig(
        # Use my own chrome browser
        browser_binary_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    )
)

@controller.action('Ask user for information')
def ask_human(question: str) -> str:
    answer = input(f'\n{question}\nInput: ')
    return ActionResult(extracted_content=answer)

async def main():
    agent = Agent(
        task=(
            "Open LinkedIn. "
            "Search for Gustav Galata. Send him a message. Ask the user for the message content. "
        ),
        # browser=browser,
        llm=ChatOpenAI(model="gpt-4.1"),
        controller=controller
    )
    await agent.run()

asyncio.run(main())
