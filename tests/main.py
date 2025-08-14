#Main code#
from groqllm import llmchat


def main():
    
    print("Woosh:Hi,whoosh here how can I help you today?")

    while True:
        query=input("You:")
        if query.lower() not in ["bye","quit","exit"]:
            response=llmchat(query)
            print(f"Woosh:{response}")
        else:
            print("Woosh:Bye,see you later!")
            break

if __name__ == "__main__":
    main()


              
        
