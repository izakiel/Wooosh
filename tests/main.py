#Main code#
from  memory_class import Memory
import os
from dotenv import load_dotenv
import sys
from langchain_groq import ChatGroq


def main():
    #Loading environement variables
    load_dotenv()
    api_key=os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Api Key Not Found")
        raise ValueError
        sys.exit(1)
    
    #Loading LLM and Memory LLM
    llm=ChatGroq(api_key=api_key,model_name="llama-3.1-8b-instant",temperature=0.6,max_tokens=1000)
    Whoosh=Memory(llm=llm)

    while True:

        user_id=input("Enter your user id:")
        print("Woosh:Hi,whoosh here how can I help you today?")
        

        while True:
            try:
                query=input("You:")
                if query.lower() not in ["bye","quit","exit"]:
                    response=Whoosh.chat_with_memory(query,user_id)
                    print(f"Woosh:{response.content}")
                else:
                    print("Woosh:Bye,see you later!")
                    break
            except KeyboardInterrupt:
                print("Goodbye!")
                sys.exit(0)


if __name__ == "__main__":
    main()


              
        
