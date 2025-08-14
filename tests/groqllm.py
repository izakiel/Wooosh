#Langchain 
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="C:/Users/basil/Documents/Python/Woosh/.env")

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("No API Key")

chat_history=[{"role":"system","content":"Your name is Whoosh"}]

def llmchat(input):
    llm=ChatGroq(model_name="llama-3.1-8b-instant",
                 groq_api_key=GROQ_API_KEY,
                 temperature=0.7,
                 max_tokens=100
                 )
    chat_history.append({"role":"user","content":input})
    response=llm.invoke(chat_history) 
    chat_history.append({"role":"assistant","content":response.content})
    return response.content
    





if __name__ == "__main__":

    print("Whoosh:Hi,how can I help you today?")

    while True:
        prompt=input("User:")
        if prompt not in ['quit','exit','bye']:
            response=llmchat(prompt)
            print(f"Whoosh:{response}")
        else:
            print("Whoosh:Goodbye!")
            break
    
    







