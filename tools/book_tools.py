import json
import os
from langchain.tools import tool

def load_store_data():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to root
    root_dir = os.path.dirname(current_dir)
    data_path = os.path.join(root_dir, 'storedata.json')
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"books": []}

@tool
def answer_book_question(query: str) -> str:
    """
    Useful for answering specific questions about a book. 
    Input should be the title of the book or the author's name.
    """
    data = load_store_data()
    books = data.get("books", [])
    
    query_lower = query.lower().strip()
    found_books = []
    
    # First pass: Exact title match (case-insensitive)
    for book in books:
        if book['title'].lower() == query_lower:
            found_books.append(book)
            
    # Second pass: Title contained in query (if query is longer, e.g. "The Correspondent by Virginia Evans")
    # OR Query contained in title (partial match)
    if not found_books:
        for book in books:
            book_title_lower = book['title'].lower()
            # Check if book title is inside the query (e.g. query="price of The Hobbit")
            if book_title_lower in query_lower and len(book_title_lower) > 3:
                found_books.append(book)
            # Check if query is inside book title (e.g. query="Harry Potter")
            elif query_lower in book_title_lower and len(query_lower) > 3:
                found_books.append(book)
                
    # Third pass: Author match
    if not found_books:
        for book in books:
            if query_lower in book['author'].lower():
                found_books.append(book)

    if not found_books:
        return "I could not find any book matching that title or author in our store."
        
    # Remove duplicates if any (based on id)
    seen_ids = set()
    unique_books = []
    for b in found_books:
        if b['id'] not in seen_ids:
            unique_books.append(b)
            seen_ids.add(b['id'])

    return json.dumps(unique_books)
