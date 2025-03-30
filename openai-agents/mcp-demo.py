import os
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import asyncio
from dotenv import load_dotenv

load_dotenv()

github_server = MCPServerStdio(
  params={
    "command": "docker",
    "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "mcp/github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "")
    }
  }
)

agent = Agent(
    name="Developer Assistant",
    instructions="You provide help with programming related questions.",
    mcp_servers=[github_server]
)

async def main():
    async with github_server:
        prompt = "Summarize the latest commit of the " \
                 "robinmanuelthiel/local-calendar-sync repository."

        result = await Runner.run(agent, prompt)
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
