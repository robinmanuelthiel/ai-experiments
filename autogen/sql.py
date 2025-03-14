import os
import asyncio
from typing import Any
import agentops
import sqlite3
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination

# Start tracing
# agentops.init(api_key=os.environ.get("AGENTOPS_API_KEY"), tags=["simple-autogen-example"])

# Init database connection
connection = sqlite3.connect("demo.db", check_same_thread=False)

# Seeding
# cursor = connection.cursor()
# cursor.execute("DROP TABLE IF EXISTS cars")
# cursor.execute("DROP TABLE IF EXISTS orders")
# cursor.execute("DROP TABLE IF EXISTS users")
# cursor.execute("CREATE TABLE cars (id INTEGER PRIMARY KEY, make TEXT, model TEXT)")
# cursor.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, car_id INTEGER)")
# cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, country_code TEXT)")
# cursor.execute("INSERT INTO users (name, age, country_code) VALUES ('Linda', 30, 'US')")
# cursor.execute("INSERT INTO users (name, age, country_code) VALUES ('Peter', 25, 'US')")
# cursor.execute("INSERT INTO users (name, age, country_code) VALUES ('Alice', 27, 'US')")
# cursor.execute("INSERT INTO users (name, age, country_code) VALUES ('Robin-Manuel', 33, 'DE')")
# connection.commit()


def get_tables() -> list[str]:
  """
  Returns the list of tables in the database.

  Returns:
    list[str]: The list of tables in the database.
  """

  cursor = connection.cursor()
  result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
  return result.fetchall()

def run_query(sql: str) -> list[Any]:
  """
  Executes the given SQL query and returns a list of results.

  Args:
    sql (str): The SQL query to be executed.

  Returns:
    list[dict]: A list of results.
  """
  print(f"Running query: {sql}")
  cursor = connection.cursor()
  result = cursor.execute(sql)
  return result.fetchall()

# Let's first define the assistant agent that suggests tool calls.
agent = AssistantAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. You can help with simple questions about the dataset. Return 'TERMINATE' when the task is done.",
    model_client=OpenAIChatCompletionClient(model="gpt-4o"),
    tools=[get_tables, run_query],
)

# Run the agent and stream the messages to the console.
async def main() -> None:
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(10)
    group_chat = RoundRobinGroupChat([agent], termination_condition=termination)
    stream = group_chat.run_stream(task="How many users are from Germany?")
    await Console(stream)
    # Stop tracing
    # agentops.end_session("Success")

# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
asyncio.run(main())
