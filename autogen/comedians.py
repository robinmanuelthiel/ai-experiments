import os
import asyncio
import agentops
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat

async def main() -> None:
  openai_model_client = OpenAIChatCompletionClient(
      model="gpt-4o",
  )

  ollama_model_client = OpenAIChatCompletionClient(
      model="phi3",
      base_url="http://127.0.0.1:11434/v1",
  )

  # Start logging with logger_type and the filename to log to
  # logging_session_id = autogen.runtime_logging.start(logger_type="sqlite", config={"dbname": "logs.db"})
  # print("Logging session ID: " + str(logging_session_id))

  # agentops.init(api_key=os.environ.get("AGENTOPS_API_KEY"), tags=["simple-autogen-example"])
  # agentops.start_session(tags=["autogen-tool-example"])

  cathy = AssistantAgent(
      name="cathy",
      system_message="Your name is Cathy and you are a part of a duo of comedians.",
      model_client=openai_model_client
  )

  joe = AssistantAgent(
      name="joe",
      system_message="Your name is Joe and you are a part of a duo of comedians and you like dad jokes.",
      model_client=ollama_model_client
  )

  group_chat = RoundRobinGroupChat([cathy, joe], max_turns=4)
  stream = group_chat.run_stream(task="Cathy, tell me a joke about progamming")
  await Console(stream)

  # agentops.end_session("Success")
  # autogen.runtime_logging.stop()


asyncio.run(main())

