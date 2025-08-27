"""
Prompt Optimizer Flask Backend
Main application server providing API endpoints for prompt optimization
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import os

from config import Config
from optimizer import PromptOptimizer

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, origins=Config.CORS_ORIGINS)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize optimizer
try:
    optimizer = PromptOptimizer()
    logger.info("Prompt Optimizer initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Prompt Optimizer: {e}")
    optimizer = None

# Rate limiting storage (simple in-memory for demo)
request_counts = {}

def check_rate_limit(client_ip: str) -> bool:
    """Simple rate limiting check"""
    current_time = datetime.now()
    current_minute = current_time.replace(second=0, microsecond=0)
    
    if client_ip not in request_counts:
        request_counts[client_ip] = {}
    
    if current_minute not in request_counts[client_ip]:
        request_counts[client_ip][current_minute] = 0
    
    request_counts[client_ip][current_minute] += 1
    
    # Clean old entries
    old_entries = [k for k in request_counts[client_ip].keys() 
                   if (current_time - k).total_seconds() > 60]
    for old_key in old_entries:
        del request_counts[client_ip][old_key]
    
    return request_counts[client_ip][current_minute] <= Config.REQUESTS_PER_MINUTE

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "service": "Prompt Optimizer",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health():
    """Comprehensive health check including DeepSeek API"""
    if not optimizer:
        logger.error("Optimizer validation endpoint called but optimizer not initialized")
        return jsonify({
            "error": "Prompt Optimizer not initialized"
        }), 503

    health_status = optimizer.health_check()
    status_code = 200 if health_status["status"] == "healthy" else 500
    
    return jsonify(health_status), status_code

@app.route('/optimize', methods=['POST'])
def optimize_prompt():
    """Main endpoint for prompt optimization"""
    client_ip = request.remote_addr
    
    # Rate limiting
    if not check_rate_limit(client_ip):
        return jsonify({
            "error": True,
            "message": "Rate limit exceeded. Please try again later."
        }), 429
    
    # Validate optimizer is initialized
    if not optimizer:
        return jsonify({
            "error": True,
            "message": "Service temporarily unavailable"
        }), 503
    
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": True,
                "message": "No JSON data provided"
            }), 400
        
        # Validate required fields
        required_fields = ["raw_prompt", "prompt_style", "target_ai"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": True,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Validate field values
        # Extract required fields
        raw_prompt = data.get('raw_prompt', '').strip()
        prompt_style = data.get('prompt_style', 'BASIC').upper()
        target_ai = data.get('target_ai', 'ChatGPT')
        clarifications = data.get('clarifications', '').strip() or None
        
        if not raw_prompt:
            return jsonify({
                "error": True,
                "message": "raw_prompt cannot be empty"
            }), 400
        
        if prompt_style not in ["BASIC", "DETAIL"]:
            return jsonify({
                "error": True,
                "message": "prompt_style must be 'BASIC' or 'DETAIL'"
            }), 400
        
        if target_ai not in ["ChatGPT", "Claude", "Gemini", "Other"]:
            return jsonify({
                "error": True,
                "message": "target_ai must be one of: ChatGPT, Claude, Gemini, Other"
            }), 400
        
        # Log the optimization request
        logger.info(f"Optimization request from {client_ip}: style={prompt_style}, target={target_ai}")
        
        # Perform optimization (may return questions for DETAIL mode)
        result = optimizer.optimize_prompt(raw_prompt, prompt_style, target_ai, clarifications)
        
        if result.get("error"):
            logger.error(f"Optimization failed: {result.get('message')}")
            return jsonify(result), 500
        
        # Log successful optimization
        logger.info(f"Optimization completed successfully for {client_ip}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in optimize_prompt: {str(e)}")
        return jsonify({
            "error": True,
            "message": "An unexpected error occurred. Please try again."
        }), 500

@app.route('/validate', methods=['POST'])
def validate_input():
    """Endpoint to validate input before optimization"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"valid": False, "message": "No data provided"})
        
        raw_prompt = data.get("raw_prompt", "").strip()
        
        if not raw_prompt:
            return jsonify({"valid": False, "message": "Prompt cannot be empty"})
        
        if len(raw_prompt) < 10:
            return jsonify({"valid": False, "message": "Prompt too short (minimum 10 characters)"})
        
        if len(raw_prompt) > 5000:
            return jsonify({"valid": False, "message": "Prompt too long (maximum 5000 characters)"})
        
        return jsonify({"valid": True, "message": "Input is valid"})
        
    except Exception as e:
        logger.error(f"Error in validate_input: {str(e)}")
        return jsonify({"valid": False, "message": "Validation error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": True,
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": True,
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    # Validate configuration before starting
    try:
        Config.validate_config()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        exit(1)
    
    # Start the Flask development server
    port = int(os.environ.get('PORT', 8000))
    debug = Config.FLASK_ENV == 'development'
    
    logger.info(f"Starting Prompt Optimizer on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
