import os
import sys
from dotenv import load_dotenv
from langchain.agents import create_agent

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
            "that you cannot answer the question."
        )
        agent = create_agent(
            model="gpt-4o-mini",
            tools=[], # No tools for now
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
