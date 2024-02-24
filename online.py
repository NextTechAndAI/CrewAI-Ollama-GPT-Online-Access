import os, sys
from crewai import Agent, Task, Crew, Process

from langchain_community.llms import Ollama
ollama_llm = Ollama(model="openhermes")

from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

user_input = "Hello, world!"
if len(sys.argv) > 1:
  user_input = sys.argv[1]

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal=f'Use the user input provided and fulfill everything that is required in this input. The input is: {user_input}',
  backstory="""You work in a service team.
  Your expertise lies fulfilling input from users.
  Use tools only in case you do not know the answer directly.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  llm=ollama_llm
)

task1 = Task(
  description=f"""Use the human input provided and fulfill everything that is required in this input.
  The input is: {user_input}
  """,
  agent=researcher
)

crew = Crew(
  agents=[researcher],
  tasks=[task1],
  process=Process.sequential,
  verbose=2
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)

