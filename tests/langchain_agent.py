from langchain.tools import Tool
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from groqllm import LLM
from langchain.agents import initialize_agent,AgentType
import sys


class RagAgent():
    def __init__(self,api_key):
        llm_instance=LLM(api_key)


        time_tool=Tool(
            name="time_tool",
            func = lambda _:datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            description="This tool returns date and time"
        )

        def get_weather(city:str) -> str:
            load_dotenv()
            API_KEY=os.getenv("OPEN_WEATHER_API_KEY")
            if not API_KEY:
                print("No API key found")
                raise ValueError
            api_endpoint=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&unit=metric"
            try:
                response=requests.get(api_endpoint).json()
                if response.get("cod")!=200:
                    print (response.get("message","Error fetching datat"))
                    
                else:
                    weather=response["weather"][0]["main"]
                    return f"Weather in {city} is {weather}"
                    
            except Exception as e:
                print(f"An error occurred: {e}")

        weather_tool=Tool(
            name="weather_tool",
            func=get_weather,
            description="Retruns current weather in a given city.Input should be the city name."
        )


        tools=[time_tool,weather_tool]
        memory=llm_instance.memory
        prompt=llm_instance.prompt
        self.agent=initialize_agent(
            llm=llm_instance.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            tools=tools,
            prompt=prompt,
            verbose=True,
            memory=memory,
            max_iterations=5
        )
    def agent_run(self,query:str):
        try:
            return self.agent.invoke({"input": query})["output"]
        except Exception as e:
            return f"Error: {e}"


if __name__ =="__main__":
    load_dotenv()
    api_key=os.getenv("GROQ_API_KEY")
    if not api_key:
        print("No API key found!!")
    agent=RagAgent(api_key=api_key)

    print("Whoosh:Hi Woosh here,how can I help you.")

    try:

        while True:
            query = input("Enter your query: ")
            if query.lower() in ["quit","exit","goodbye"]:
                print("Goodbye")
                sys.exit(0)
            
            response = agent.agent_run(query)
            print(response)
    except KeyboardInterrupt:
            print("Goodbye!")
            sys.exit(0)