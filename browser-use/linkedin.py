from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, Controller
import asyncio
from dotenv import load_dotenv

load_dotenv()

controller = Controller()
browser = Browser(
    config=BrowserConfig(
        browser_binary_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",

        # Chrome's Security Features don't allow remote debugging to be enabled when the browser is
        # using the default user data directory. In this workaroung, a remote-debug-profile gets created.
        # This profile will not have any of your existing cookies or logins, but will store them across
        # sessions. You can delete the remote-debug-profile directory to clear the cookies.
        extra_browser_args=[
            "--user-data-dir=remote-debug-profile",
        ],
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
            "Search for Satya Nadella. Send him a message. Ask the user for the message content. "
        ),
        browser=browser,
        llm=ChatOpenAI(model="gpt-4.1"),
        controller=controller
    )
    await agent.run()

asyncio.run(main())
