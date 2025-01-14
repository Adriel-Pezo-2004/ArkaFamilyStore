from flask import Flask, request, jsonify
from flask_cors import CORS
from database import DatabaseManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia esto por una clave secreta segura

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize database manager
db_manager = DatabaseManager()

@app.route('/api/search', methods=['GET'])
def search_catalog():
    search_term = request.args.get('search', '')
    if not search_term:
        return jsonify({"error": "Missing search term"}), 400

    try:
        results = db_manager.search_catalog(search_term)
        logger.info(f"Search term: {search_term}")
        logger.info(f"Number of results found: {len(results)}")
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        return jsonify({"error": "An error occurred during the search"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)