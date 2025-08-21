from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_groq import ChatGroq
from sqlalchemy import create_engine, Column, String, Integer, desc
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------- DB SETUP ----------------
Base = declarative_base()
engine = create_engine("sqlite:///chat1.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    message = Column(String, nullable=False)
    role=Column(String,nullable=False)

Base.metadata.create_all(engine)

# ---------------- MEMORY CLASS ----------------
class Memory():
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate([
            ("system", "you are Whoosh, a helpful assistant"),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{user_input}")
        ])
        self.store = {} 
        self.setup()

    # Pull last 20 messages from DB
    def load_history_from_db(self, session_id: str):
        msgs = session.query(Message)\
            .filter_by(user_id=session_id)\
            .order_by(desc(Message.id))\
            .limit(20).all()
        return [(m.message,m.role) for m in reversed(msgs)]

    # Get or initialize memory
    def get_history(self, session_id: str):
        if session_id not in self.store:
            history = InMemoryChatMessageHistory()
            
            # Load past messages from DB into memory
            for msg, role in self.load_history_from_db(session_id):
                if role == 'user':
                    history.add_user_message(msg)  # assuming all are user messages; could adjust if roles exist
                else:
                    history.add_ai_message(msg)            
            self.store[session_id] = history
        return self.store[session_id]

    # Trim memory to last 20
    def trim_history(self, history, limit=20):
        if len(history.messages) > limit:
            history.messages = history.messages[-limit:]

    # Setup the chain with memory
    def setup(self):
        chain = self.prompt | self.llm
        self.with_memory = RunnableWithMessageHistory(
            chain,
            get_session_history=self.get_history,
            input_messages_key="user_input",
            history_messages_key="history"
        )

    # Call chain with user input and session_id
    def chat_with_memory(self, input_text, session_id):
        try:
            # invoke chain
            response = self.with_memory.invoke(
                {"user_input": input_text},
                config={"configurable": {"session_id": session_id}}
            )
            session.add_all([
                Message(user_id=session_id,role='user',message=input_text),
                Message(user_id=session_id,role='llm',message=response.content)
            ])

            session.commit()


            # Trim in-memory history
            history = self.store[session_id]
            
            self.trim_history(history, limit=5)

            return response

        except Exception as e:
            print(f"Error: {e}")

if __name__=="__main__":

    import os
    import sys
    from langchain_groq import ChatGroq
    from dotenv import load_dotenv

    load_dotenv()

    api_key=os.getenv("GROQ_API_KEY")

    if not api_key:
        print("No API Key")
        sys.exit(1)

    llm=ChatGroq(api_key=api_key,model_name="llama-3.1-8b-instant")
    whoosh=Memory(llm=llm)

    while True:
        session_id=input("Enter your id")
        print("whoosh:Hey Whoosh here how can i help you.")

        

        while True:

            try:

                query=input("User:")

                if query not in ['bye','quit','exit']:

                    response=whoosh.chat_with_memory(input_text=query,session_id=session_id)
                    

                    print(f"Whoosh:{response.content}")
                    
                else:
                    print("Gooodbye!")
                    break
            except KeyboardInterrupt:
                print("Goodbye forever!")
                sys.exit(0)

