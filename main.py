from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import re
import uvicorn

app = FastAPI(title="BFHL API", description="REST API for processing arrays")

class RequestData(BaseModel):
    data: List[str]

class ResponseData(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str

USER_INFO = {
    "full_name": "meet_bhuva",
    "birth_date": "01012005",
    "email": "meetpatel0852@gmail.com",
    "roll_number": "22BCE10033"
}

@app.post("/bfhl", response_model=ResponseData, status_code=200)
async def process_data(request: RequestData):
    """
    Process the input array and return categorized data
    """
    try:
        data = request.data
        
        # Initialize arrays
        odd_numbers = []
        even_numbers = []
        alphabets = []
        special_characters = []
        
        # Process each item in the data array
        for item in data:
            if item.isdigit():
                # It's a number
                num = int(item)
                if num % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
            elif item.isalpha():
                #alphabetic (single character or string)
                alphabets.append(item.upper())
            else:
                # Check if contains any alphabetic characters
                if re.search(r'[a-zA-Z]', item):
                    # Mixed alphanumeric or contains letters
                    alphabets.append(item.upper())
                else:
                    #a special character
                    special_characters.append(item)
        
        # Calculate sum
        total_sum = 0
        for item in data:
            if item.isdigit():
                total_sum += int(item)
        
        # Create concatenation string with alternating caps
        # collect all alphabetic characters from all alphabetic items
        all_alpha_chars = []
        for item in data:
            if item.isalpha() or re.search(r'[a-zA-Z]', item):
                for char in item:
                    if char.isalpha():
                        all_alpha_chars.append(char.lower())
        
        all_alpha_chars.reverse()
        
        # Apply alternating caps starting
        concat_string = ""
        for i, char in enumerate(all_alpha_chars):
            if i % 2 == 0:
                concat_string += char.upper()  # Even indices: uppercase
            else:
                concat_string += char.lower()  # Odd indices: lowercase
        
        # Creating response
        response = ResponseData(
            is_success=True,
            user_id=f"{USER_INFO['full_name']}_{USER_INFO['birth_date']}",
            email=USER_INFO["email"],
            roll_number=USER_INFO["roll_number"],
            odd_numbers=odd_numbers,
            even_numbers=even_numbers,
            alphabets=alphabets,
            special_characters=special_characters,
            sum=str(total_sum),
            concat_string=concat_string
        )
        
        return response
        
    except Exception as e:
        # Handle exceptions
        raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")

@app.get("/")
async def root():
    """
    Root endpoint for basic API information
    """
    return {
        "message": "BFHL API is running",
        "endpoints": {
            "POST /bfhl": "Process array data"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found"}

@app.exception_handler(405)
async def method_not_allowed_handler(request, exc):
    return {"error": "Method not allowed"}

if __name__ == "__main__":
    # For local development
    uvicorn.run(app, host="0.0.0.0", port=8000)