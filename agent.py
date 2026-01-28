import os
import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from tools.book_tools import answer_book_question

# Load environment variables
load_dotenv()

def run_chat():
    # Initialize the model
    # Ensure you have OPENAI_API_KEY set in your environment or .env file
    try:
        # We use create_agent to build the agent runtime.
        # Even without tools, this sets up the graph-based agent structure.
        system_prompt = (
            "You are RightBookAI, a dedicated book concierge. "
            "Your purpose is to help users discover books they will truly enjoy. "
            "You must adopt the persona of a proper, polite, and knowledgeable British concierge. "
            "Speak with elegance, use British spelling (e.g., 'colour', 'favourite'), and be helpful and courteous at all times. "
            "If the user asks questions unrelated to books or the bookstore, you must regrettably inform them "
            "that you cannot answer the question. "
            "If the user asks about multiple books, you must call the 'answer_book_question' tool separately for each book "
            "to ensure you have the correct details for all of them."
        )
        
        tools = [answer_book_question]
        
        agent = create_agent(
            model="gpt-4o-mini",
            tools=tools,
            system_prompt=system_prompt
        )
    except Exception as e:
        print(f"Error initializing agent: {e}")
        print("Make sure you have set the OPENAI_API_KEY environment variable.")
        return

    print("Agent is ready! Type 'exit' or 'quit' to stop.")
    print("-" * 50)

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue

            # Invoke the agent with the user's message
            result = agent.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            
            # Check for tool calls in the conversation history of this turn
            # result["messages"] contains the full history. We want to see if any tools were called in the recent turn.
            # A simple way is to check if any message in the result is a ToolMessage or AIMessage with tool_calls
            
            # For debugging/confirmation purposes, let's print if a tool was used.
            for msg in result["messages"]:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        print(f"[I used the {tool_call['name']} tool]")

            # The result contains the full state, including the conversation history.
            # We extract the last message, which is the agent's response.
            latest_message = result["messages"][-1]
            print(f"Agent: {latest_message.content}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_chat()
