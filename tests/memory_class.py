from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_groq import ChatGroq

#Creating a memory class

class Memory():
    def __init__(self,llm):
        self.llm=llm
        self.prompt=ChatPromptTemplate([
            ("system","you are Whoosh an helpfull assistant"),
            MessagesPlaceholder(variable_name="history"),
            ("user","{user_input}")
        
        ])
        self.store={} 
        self.setup()
    #For getting the sesion-id or user id    
    
    def get_history(self,session_id:str):
        if session_id not in self.store:
            self.store[session_id]=InMemoryChatMessageHistory()
        return self.store[session_id]
    
    #Creating a chian for memory
    def setup(self):
        chain=self.prompt | self.llm
        self.with_memory=RunnableWithMessageHistory(
            chain,
            get_session_history=self.get_history,
            input_messages_key="user_input",
            history_messages_key="history"

        )
    #Calling the chain with user input and session_id
    def chat_with_memory(self,input,session_id):
        try:
            return self.with_memory.invoke(
                {"user_input":input},
                config={"configurable":{"session_id":session_id}}
            )
        except Exception as e:
            print(f"Error: {e}")
    
        
    
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    import sys

    load_dotenv()
    api_key=os.getenv("GROQ_API_KEY")
    if  not api_key:
        print("Please set GROK_API_KEY in your .env file")
        sys.exit(1)
    llm=ChatGroq(model_name="llama-3.1-8b-instant",api_key=api_key)
    whoosh=Memory(llm=llm)
    print("Whoosh:Hey Whoosh here,how can I help you")
    while True:
        
        try:
            user_input=input("You:")
        
            response=whoosh.chat_with_memory(user_input,"session_1")

            print(f"Woosh:{response.content}")
            
        except KeyboardInterrupt:
            print("Goodbye!")
            sys.exit(0)
    