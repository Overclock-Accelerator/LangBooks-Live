import json
import os
import random
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
def order_builder(budget: float, criteria: str) -> str:
    """
    Useful for building a book order or bundle within a specific budget.
    The tool selects a set of books that match the user's criteria (e.g., genre, recency, popularity)
    while ensuring the total cost is within the provided budget.
    It aims to maximize the total value of the order within the budget.
    Input should be the budget amount and a description of the criteria.
    """
    data = load_store_data()
    books = data.get("books", [])
    
    criteria_lower = criteria.lower()
    
    # Filter books based on criteria
    eligible_books = []
    for book in books:
        score = 0
        # Check genre
        if book['genre'].lower() in criteria_lower:
            score += 5
        # Check description
        if any(word in book['description'].lower() for word in criteria_lower.split()):
            score += 3
        # Check title
        if any(word in book['title'].lower() for word in criteria_lower.split()):
            score += 2
        
        # Check recency (e.g., "recent" in criteria)
        if "recent" in criteria_lower and book['year'] >= 2020:
            score += 3
            
        if score > 0:
            eligible_books.append((score, book))
            
    # Sort by score descending
    eligible_books.sort(key=lambda x: x[0], reverse=True)
    
    # If no matches, fallback to highly rated books
    if not eligible_books:
        eligible_books = [(0, b) for b in books if b['rating'] >= 4.5]
        random.shuffle(eligible_books)
        
    selected_books = []
    current_total = 0.0
    
    # Greedy selection: Try to fit high-scoring books first
    for _, book in eligible_books:
        price = book.get('salePrice', book['price'])
        if current_total + price <= budget:
            selected_books.append(book)
            current_total += price
            
    # If we have room, try to fill the gap with other books (even if lower score) to maximize budget usage
    remaining_budget = budget - current_total
    if remaining_budget > 5: # If we have at least $5 left
        # Look for books that fit in the remaining budget, prioritizing criteria match then rating
        potential_fillers = [b for b in books if b not in selected_books]
        # Sort potential fillers by price descending to fill budget efficiently, or rating
        potential_fillers.sort(key=lambda b: b.get('salePrice', b['price']), reverse=True)
        
        for book in potential_fillers:
            price = book.get('salePrice', book['price'])
            if price <= remaining_budget:
                 selected_books.append(book)
                 current_total += price
                 remaining_budget -= price
    
    if not selected_books:
        return f"I'm sorry, but I couldn't find any books matching your criteria that fit within your budget of ${budget:.2f}."

    # Format output
    response = "Certainly. Here’s a recommended bundle.\n\n"
    total_price = 0.0
    
    for book in selected_books:
        price = book.get('salePrice', book['price'])
        total_price += price
        response += f"{book['title']} ({book['year']}): ${price:.2f}\n"
        
    response += f"\nOrder Total: ${total_price:.2f}"
    
    return response
