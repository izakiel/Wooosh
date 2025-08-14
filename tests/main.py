#Main code#


def main():
    
    print("Woosh:Hi,whoosh here how can I help you today?")

    while True:
        query=input("You:")
        if query.lower() not in ["bye","quit"]:
            print(f"Woosh:You said '{query}'")
        else:
            print("Woosh:Bye,see you later!")
            break

if __name__ == "__main__":
    main()


              
        
