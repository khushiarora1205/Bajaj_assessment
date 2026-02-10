import os
import math
from functools import reduce
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Global constant
OFFICIAL_EMAIL = "khushi3860.beai23@chitkara.edu.in"

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Input size limits for security
MAX_ARRAY_SIZE = 1000
MAX_FIBONACCI_N = 1000
MAX_AI_STRING_LENGTH = 5000


# ==================== HELPER FUNCTIONS ====================

def generate_fibonacci(n):
    """Generate first N Fibonacci numbers starting from 0."""
    if n == 0:
        return []
    elif n == 1:
        return [0]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    
    return fib_sequence[:n]


def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True


def filter_primes(numbers):
    """Filter and return only prime numbers from array."""
    return [num for num in numbers if is_prime(num)]


def calculate_gcd(a, b):
    """Calculate GCD of two numbers."""
    while b:
        a, b = b, a % b
    return abs(a)


def calculate_hcf(numbers):
    """Calculate HCF (GCD) of all numbers in array."""
    return reduce(calculate_gcd, numbers)


def calculate_lcm_two(a, b):
    """Calculate LCM of two numbers."""
    return abs(a * b) // calculate_gcd(a, b)


def calculate_lcm(numbers):
    """Calculate LCM of all numbers in array."""
    return reduce(calculate_lcm_two, numbers)


def get_gemini_response(query):
    """Get single-word response from Gemini API."""
    try:
        if not GEMINI_API_KEY:
            return {"error": "Gemini API key not configured", "status": 500}
        
        model = genai.GenerativeModel('models/gemma-3-12b-it')
        prompt = f"Answer the following question with ONLY ONE WORD, no punctuation, no explanation: {query}"
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return {"error": "No response from AI service", "status": 500}
        
        # Clean response - remove punctuation and whitespace
        answer = response.text.strip().strip('.,!?;:"\'-')
        
        # Extract first word if multiple words returned
        answer = answer.split()[0] if answer.split() else answer
        
        return {"data": answer}
    
    except Exception as e:
        return {"error": f"AI service error: {str(e)}", "status": 500}


def create_success_response(data):
    """Create standardized success response."""
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL,
        "data": data
    })


def create_error_response(error_message, status_code=400):
    """Create standardized error response."""
    return jsonify({
        "is_success": False,
        "official_email": OFFICIAL_EMAIL,
        "error": error_message
    }), status_code


# ==================== ROUTES ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }), 200


@app.route('/bfhl', methods=['POST'])
def bfhl():
    """Main endpoint for fibonacci, prime, lcm, hcf, and AI operations."""
    try:
        # Validate Content-Type
        if not request.is_json:
            return create_error_response("Content-Type must be application/json", 400)
        
        # Get request body
        data = request.get_json()
        
        # Validate body exists
        if not data:
            return create_error_response("Request body is required", 400)
        
        # Validate exactly one key
        if len(data) != 1:
            return create_error_response("Request must contain exactly one key", 400)
        
        # Get the operation key
        operation = list(data.keys())[0]
        value = data[operation]
        
        # Validate allowed operations
        allowed_operations = ["fibonacci", "prime", "lcm", "hcf", "AI"]
        if operation not in allowed_operations:
            return create_error_response(
                f"Invalid operation. Allowed: {', '.join(allowed_operations)}", 
                400
            )
        
        # ========== FIBONACCI ==========
        if operation == "fibonacci":
            # Validate type
            if not isinstance(value, int):
                return create_error_response("fibonacci requires an integer", 422)
            
            # Validate range
            if value < 0:
                return create_error_response("fibonacci requires a non-negative integer", 422)
            
            # Security limit
            if value > MAX_FIBONACCI_N:
                return create_error_response(f"fibonacci N must be <= {MAX_FIBONACCI_N}", 422)
            
            result = generate_fibonacci(value)
            return create_success_response(result)
        
        # ========== PRIME ==========
        elif operation == "prime":
            # Validate type
            if not isinstance(value, list):
                return create_error_response("prime requires an array", 422)
            
            # Validate non-empty
            if len(value) == 0:
                return create_error_response("prime requires a non-empty array", 422)
            
            # Security limit
            if len(value) > MAX_ARRAY_SIZE:
                return create_error_response(f"Array size must be <= {MAX_ARRAY_SIZE}", 422)
            
            # Validate all elements are integers
            if not all(isinstance(x, int) for x in value):
                return create_error_response("prime array must contain only integers", 422)
            
            result = filter_primes(value)
            return create_success_response(result)
        
        # ========== LCM ==========
        elif operation == "lcm":
            # Validate type
            if not isinstance(value, list):
                return create_error_response("lcm requires an array", 422)
            
            # Validate non-empty
            if len(value) == 0:
                return create_error_response("lcm requires a non-empty array", 422)
            
            # Security limit
            if len(value) > MAX_ARRAY_SIZE:
                return create_error_response(f"Array size must be <= {MAX_ARRAY_SIZE}", 422)
            
            # Validate all elements are integers
            if not all(isinstance(x, int) for x in value):
                return create_error_response("lcm array must contain only integers", 422)
            
            # Validate no zeros (LCM undefined for zero)
            if 0 in value:
                return create_error_response("lcm cannot be calculated with zero values", 422)
            
            result = calculate_lcm(value)
            return create_success_response(result)
        
        # ========== HCF ==========
        elif operation == "hcf":
            # Validate type
            if not isinstance(value, list):
                return create_error_response("hcf requires an array", 422)
            
            # Validate non-empty
            if len(value) == 0:
                return create_error_response("hcf requires a non-empty array", 422)
            
            # Security limit
            if len(value) > MAX_ARRAY_SIZE:
                return create_error_response(f"Array size must be <= {MAX_ARRAY_SIZE}", 422)
            
            # Validate all elements are integers
            if not all(isinstance(x, int) for x in value):
                return create_error_response("hcf array must contain only integers", 422)
            
            result = calculate_hcf(value)
            return create_success_response(result)
        
        # ========== AI ==========
        elif operation == "AI":
            # Validate type
            if not isinstance(value, str):
                return create_error_response("AI requires a string", 422)
            
            # Validate non-empty
            if len(value.strip()) == 0:
                return create_error_response("AI requires a non-empty string", 422)
            
            # Security limit
            if len(value) > MAX_AI_STRING_LENGTH:
                return create_error_response(f"AI string must be <= {MAX_AI_STRING_LENGTH} characters", 422)
            
            ai_result = get_gemini_response(value)
            
            if "error" in ai_result:
                return create_error_response(ai_result["error"], ai_result.get("status", 500))
            
            return create_success_response(ai_result["data"])
    
    except Exception as e:
        # Unexpected server error
        return create_error_response(f"Internal server error: {str(e)}", 500)


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return create_error_response("Endpoint not found", 404)


@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 errors."""
    return create_error_response("Method not allowed", 405)


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return create_error_response("Internal server error", 500)


if __name__ == '__main__':
    app.run(debug=False)
