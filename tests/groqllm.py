#Langchain 
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import sys



class LLM():
    def __init__(self,api_key,model_name="llama-3.1-8b-instant",temperature=0.7,max_tokens=100):
        self.llm=ChatGroq(
            model_name=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
    
        self.memory= ConversationSummaryBufferMemory(
                llm=self.llm,
                max_token_limit=1000,
                memory_key="chat_history",
                return_messages=True
            )
        self.custom_template = """
You are Whoosh, an AI assistant. 
When the user asks for multiple pieces of information (e.g., time and weather), use all relevant tools.
Always return a single final answer combining the results.
Do not continue thinking after the tools are used.
{chat_history}
User: {input}
Whoosh:"""
        self.prompt=PromptTemplate(
        input_variables=["chat_history","input"],
        template=self.custom_template
        )
        self.conversation=ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
            )
    
    def llmchat(self,input):
        try:    
            response=self.conversation.predict(input=input)         
            return response
        except Exception as e:
            print(f"Error: {e}")
        





if __name__ == "__main__":

    load_dotenv()
    api_key=os.getenv("GROQ_API_KEY")
    if not api_key:
        print("API key not found")
        sys.exit(1)

    print("Whoosh:Hi,how can I help you today?")
    LLM=LLM(api_key=api_key)
    try:

        while True:
            prompt=input("User:")
            if prompt.lower() in {"quit","bye","exit"} :
                print("Whoosh:Goodbye!")
                sys.exit(0)
            response=LLM.llmchat(prompt)
            print(f"Whoosh:{response}")
    except KeyboardInterrupt:
        print("\n Whoosh:Goodbye!")
    
    







