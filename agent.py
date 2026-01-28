import os
import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from tools.book_tools import answer_book_question
from tools.recommendation_tools import book_recommender
from tools.order_tools import order_builder

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
            "If the user asks about multiple books *specifically by name*, you must call the 'answer_book_question' tool separately for each book. "
            "However, if you are providing recommendations using 'book_recommender' or building an order with 'order_builder', "
            "use the detailed information returned by those tools to describe the books. "
            "Do NOT call 'answer_book_question' for books returned by the recommender or order builder, as those tools provide sufficient details."
        )
        
        tools = [answer_book_question, book_recommender, order_builder]
        
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

    # Initialize conversation history
    chat_history = []

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue

            # Add user message to history
            chat_history.append({"role": "user", "content": user_input})

            # Invoke the agent with the full conversation history
            result = agent.invoke({
                "messages": chat_history
            })
            
            # Check for tool calls in the conversation history of this turn
            for msg in result["messages"]:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    # Avoid duplicate logging if we are re-processing history, 
                    # but here result["messages"] is the output of this specific invoke call 
                    # which includes the new steps taken.
                    # However, create_agent returns the FULL state including input messages.
                    # We only want to log new tool calls.
                    # A simple heuristic: if the message index is greater than the length of our previous history.
                    pass 

            # Actually, let's just log tool calls from the *new* messages generated in this turn.
            # The result["messages"] includes everything.
            # We know how many messages we sent in (len(chat_history)).
            new_messages = result["messages"][len(chat_history):]

            for msg in new_messages:
                 if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        print(f"[I used the {tool_call['name']} tool]")

            # The result contains the full state.
            # We extract the last message, which is the agent's response.
            latest_message = result["messages"][-1]
            print(f"Agent: {latest_message.content}")
            print("-" * 50)
            
            # Update chat history with the new messages from the agent (including tool calls/outputs)
            # We extend our history with all the new messages generated during this turn
            chat_history.extend(new_messages)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_chat()
