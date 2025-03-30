import os
from agents import Agent, function_tool, Runner
import asyncio

@function_tool
def calculator(a: int, b: int, operator: str) -> int:
    """
    Perform a basic arithmetic operation on two integers.

    Args:
      a (int): The first operand.
      b (int): The second operand.
      operator (str): The arithmetic operator, which can be one of the following:
              "+" for addition,
              "-" for subtraction,
              "*" for multiplication,
              "/" for division.

    Returns:
      int: The result of the arithmetic operation.

    Raises:
      ValueError: If the operator is not one of the supported values.
    """
    print(f"Calculator called with a={a}, b={b}, operator={operator}")
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions=(
      "You provide help with math problems. "
      "When doing mathematic operations, use the calculator tool. "
      "Explain your reasoning at each step and include examples"
    ),
    tools=[calculator]
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent]
)

async def main():
    result = await Runner.run(triage_agent, "What is 3+5?", max_turns=5)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
