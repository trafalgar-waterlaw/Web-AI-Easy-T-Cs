from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import sqlite3
import os
import logging
from waitress import serve

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={
    r"/summarize": {"origins": "*"},
    r"/feedback": {"origins": "*"}
})


try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn",
    device="cpu",
    torch_dtype="float32"
    )
    logger.info("Model loaded successfully")
except Exception as e:
    logger.critical(f"Model loading failed: {str(e)}")
    raise


DATABASE = os.path.join(os.path.dirname(__file__), "feedback.db")

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL") # Enable Write-Ahead Logging
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

def init_db():
    try:
        with get_db_connection() as conn:
            conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
            comments TEXT DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
            logger.info("Database initialized")
    except Exception as e:
        logger.critical(f"Database initialization failed: {str(e)}")
        raise


@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            logger.warning("Invalid request format")
            return jsonify({"error": "Missing 'text' in request"}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({"error": "Empty text provided"}), 400
        logger.info(f"Processing text (length: {len(text)} chars)")

        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)

        return jsonify({
            "summary": summary[0]['summary_text'],
            "original_length": len(text)
        })
    
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        return jsonify({"error": "Processing failed"}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        required_fields = ['summary', 'rating']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO feedback (summary, rating, comments) VALUES (?, ?, ?)',
                (data['summary'], int(data['rating']), data.get('comments', ''))
            )
            
            return jsonify({"message": "Feedback saved"})

    except ValueError:
        return jsonify({"error": "Invalid rating value"}), 400

    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        return jsonify({"error": "Database error"}), 500
    


if __name__ == '__main__':
    init_db()

    serve(
        app,
        host='0.0.0.0',
        port=5000,
        threads=4,
        channel_timeout=60
    )