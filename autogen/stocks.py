import asyncio
import os
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
import agentops

async def main() -> None:
  # agentops.init(api_key=os.environ.get("AGENTOPS_API_KEY"), tags=["simple-autogen-example"])

  assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant. Write all code in python. Reply only 'TERMINATE' if the task is done.",
    model_client=OpenAIChatCompletionClient(model="gpt-4o")
  )

  code_executor = CodeExecutorAgent(
      name="code_executor",
      code_executor=LocalCommandLineCodeExecutor(work_dir="coding"),
  )

  # The termination condition is a combination of text termination and max message termination, either of which will cause the chat to terminate.
  termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(10)

  # The group chat will alternate between the assistant and the code executor.
  group_chat = RoundRobinGroupChat([assistant, code_executor], termination_condition=termination)

  # `run_stream` returns an async generator to stream the intermediate messages.
  stream = group_chat.run_stream(task="Plot a chart of NVDA and TESLA stock price change YTD.'")
  # `Console` is a simple UI to display the stream.
  await Console(stream)

asyncio.run(main())

# # Start the chat
# result = user_proxy.initiate_chat(
#     assistant,
#     message="Plot a chart of NVDA and TESLA stock price change YTD.",
# )

# print(result)
# agentops.end_session("Success")
