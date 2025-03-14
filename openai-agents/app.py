from sys import api_version
from openai import AsyncAzureOpenAI
from agents import Agent, Runner, enable_verbose_stdout_logging, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client
import asyncio

from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor

# Set up console tracing
console_exporter = ConsoleSpanExporter()
console_processor = BatchTraceProcessor(exporter=console_exporter)


# Create OpenAI client using Azure OpenAI
openai_client = AsyncAzureOpenAI(
    api_key="3PWJdtWMOShZMA82XHhkmf13aA0GOLKJHJ1hwltiMnH7Yazf6lnOJQQJ99ALACHYHv6XJ3w3AAAAACOGDGEE",
    api_version="2024-08-01-preview",
    azure_endpoint="https://rothie-eastus2-ai-services.openai.azure.com/",
    azure_deployment="gpt-4o"
)

# Set the default OpenAI client for the Agents SDK
set_default_openai_client(openai_client)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
)

async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?", max_turns=5)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
