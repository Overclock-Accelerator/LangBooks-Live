# LangBooks-Live (RightBookAI)

RightBookAI is an intelligent, conversational book concierge designed to help users discover their next favorite read. Built with Python and LangChain, it adopts the persona of a polite and knowledgeable British concierge to provide personalized recommendations, answer specific book queries, and build curated book bundles within a budget.

## Features

- **Personalized Recommendations**: Suggests books based on user interests, genres, and preferences using the `book_recommender` tool.
- **Specific Book Queries**: Answers questions about specific books (title or author) using the `answer_book_question` tool.
- **Smart Order Building**: Creates a curated list of books that fit within a specified budget while maximizing value using the `order_builder` tool.
- **Conversational Interface**: Engaging, persona-driven chat interface that maintains context throughout the conversation.

## Prerequisites

- Python 3.8+
- An OpenAI API Key

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

To start the concierge agent, run the `agent.py` script:

```bash
python agent.py
```

Once running, you can interact with RightBookAI by typing your questions or requests. 

**Example interactions:**
- "Can you recommend a good mystery novel?"
- "I have $50 to spend on sci-fi books. What can I get?"
- "Do you have 'The Great Gatsby'?"

Type `exit` or `quit` to end the session.

## Project Structure

- `agent.py`: The main entry point. Sets up the LangChain agent, tools, and runs the chat loop.
- `storedata.json`: A JSON database containing the catalog of available books.
- `tools/`: Directory containing the custom tools used by the agent.
  - `book_tools.py`: Contains `answer_book_question` for specific book lookups.
  - `recommendation_tools.py`: Contains `book_recommender` for interest-based suggestions.
  - `order_tools.py`: Contains `order_builder` for budget-constrained book selection.
- `requirements.txt`: List of Python dependencies.

## Customization

You can modify `storedata.json` to add or remove books from the catalog. The agent will automatically use the updated data.
