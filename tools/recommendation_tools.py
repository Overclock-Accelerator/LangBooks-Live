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
def book_recommender(user_interests: str) -> str:
    """
    Useful for providing book recommendations or suggestions based on user interests, genre preferences, or specific book properties.
    Input should be a description of the user's interests or what they are looking for.
    """
    data = load_store_data()
    books = data.get("books", [])
    
    interests_lower = user_interests.lower()
    
    # Simple keyword matching for scoring
    scored_books = []
    
    for book in books:
        score = 0
        # Check genre
        if book['genre'].lower() in interests_lower:
            score += 5
        
        # Check description
        if any(word in book['description'].lower() for word in interests_lower.split()):
            score += 3
            
        # Check title
        if any(word in book['title'].lower() for word in interests_lower.split()):
            score += 2
            
        # Bonus for high rating
        if book['rating'] >= 4.5:
            score += 1
            
        # Bonus for being featured
        if book['isFeatured']:
            score += 1

        # Bonus for being on sale
        if book['onSale']:
            score += 1
            
        if score > 0:
            scored_books.append((score, book))
            
    # Sort by score descending
    scored_books.sort(key=lambda x: x[0], reverse=True)
    
    # Take top 3 recommendations
    top_recommendations = scored_books[:3]
    
    if not top_recommendations:
        # Fallback: just pick some highly rated books if no matches found
        highly_rated = [b for b in books if b['rating'] >= 4.7]
        top_recommendations = [(0, b) for b in random.sample(highly_rated, min(3, len(highly_rated)))]
        
    response_parts = []
    
    for _, book in top_recommendations:
        # Build a selling description
        desc = f"Title: {book['title']} by {book['author']}\n"
        desc += f"Genre: {book['genre']}\n"
        desc += f"Description: {book['description']}\n"
        desc += f"Why it fits: "
        
        reasons = []
        if book['rating'] >= 4.5:
            reasons.append(f"It has an excellent rating of {book['rating']}/5.")
        if book['reviewCount'] > 10000:
            reasons.append(f"It is incredibly popular with {book['reviewCount']:,} reviews!")
        if book['isFeatured']:
            reasons.append("It is currently one of our featured selections.")
        if book['onSale']:
            reasons.append(f"It is currently ON SALE for ${book.get('salePrice', book['price'])} (originally ${book['price']})!")
        if book['year'] >= 2024:
            reasons.append("It is a very recent release!")
            
        desc += " ".join(reasons)
        response_parts.append(desc)
        
    return "\n\n".join(response_parts)
