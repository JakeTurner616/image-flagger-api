import os
import sqlite3
import logging
from flask import Flask, request, jsonify, g
from dotenv import load_dotenv

# To copy the database file from the container to your local machine, run:
#docker cp <container_id>:/app/flags.db /path/on/your/local/machine/flags.db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up environment variables
API_KEY = os.getenv('API_KEY')
DATABASE = 'flags.db'  # SQLite database file

if not API_KEY:
    logger.error("API_KEY is not set in environment variables.")
    raise EnvironmentError("API_KEY is required for production.")

# Open a database connection before each request
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, check_same_thread=False)
        g.db.execute('PRAGMA journal_mode=WAL;')  # Enable WAL mode for better concurrency
    return g.db

# Close the database connection after each request
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Route to process image parameters and save to SQLite
@app.route('/flag-image', methods=['POST'])
def flag_image():
    # Authenticate request using API Key
    if request.headers.get('Authorization') != f"Bearer {API_KEY}":
        logger.warning("Unauthorized access attempt detected.")
        return jsonify({"error": "Unauthorized"}), 403

    # Parse JSON data
    data = request.get_json()
    required_fields = [
        "image_prompt", "steps", "sampler",
        "cfg_scale", "seed", "size", "model_hash", "model_name",
        "seed_resize_from", "denoising_strength"
    ]

    # Validate required fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.warning(f"Missing fields: {missing_fields}")
        return jsonify({"error": "Missing required fields", "missing_fields": missing_fields}), 400

    # Extract parameters
    image_prompt = data["image_prompt"]
    steps = data["steps"]
    sampler = data["sampler"]
    cfg_scale = data["cfg_scale"]
    seed = data["seed"]
    size = data["size"]
    model_hash = data["model_hash"]
    model_name = data["model_name"]
    seed_resize_from = data["seed_resize_from"]
    denoising_strength = data["denoising_strength"]
    logger.info(f"Seed parameter: {seed}")  # Log the seed parameter specifically
    
    # Insert data into the database
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO flagged_images (
                image_prompt, steps, sampler, cfg_scale,
                seed, size, model_hash, model_name, seed_resize_from, denoising_strength
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (image_prompt, steps, sampler, cfg_scale,
            seed, size, model_hash, model_name, seed_resize_from, denoising_strength))
        db.commit()

        logger.info(f"Flagged image data saved for prompt '{image_prompt}'.")

        return jsonify({
            "status": "success",
            "message": "Image flagged and saved successfully."
        }), 200
    except Exception as e:
        logger.error(f"Error saving flagged image: {e}")
        return jsonify({"error": "Failed to save flag"}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # For production, use a WSGI server like Gunicorn to serve the app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)