from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import string
import random
import os
from dotenv import load_dotenv
from datetime import datetime


# Load all environment variable
load_dotenv()

# MongoDB connection  and initialization
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)

# Creation of the database and collection
db = client['shortit_db']
urls_collection = db['urls']

# Accessing the environment variables
BASE_URL = os.getenv('BASE_URL', 'https://shortit/')

def generate_short_url():
    """Generate a random 6-character string for short URL"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))
def get_all_urls():
    """Retrieve all URLs from the database"""
    try:
        urls = list(urls_collection.find())
        formatted_urls = []
        for url in urls:
            formatted_urls.append({
                'id': str(url['_id']),
                'originalUrl': url['originalUrl'],
                'shortUrl': f"{BASE_URL}{url['shortUrl']}",
                'createdAt': url['createdAt'].isoformat()
            })
        return jsonify(formatted_urls), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_one_url(url_identifier):
    """Retrieve a single URL by its short URL or original URL"""
    try:
        # Try to find the URL by short URL first
        url=urls_collection.find_one({'shortUrl': url_identifier})

        # If not found, try to find by original URL
        if not url:
            url=urls_collection.find_one({'originalUrl': url_identifier})

        if url:
            formatted_url={
                'id': str(url['_id']),
                'originalUrl': url['originalUrl'],
                'shortUrl': f"{BASE_URL}{url['shortUrl']}",
                'createdAt': url['createdAt'].isoformat()
            }
            return jsonify(formatted_url), 200
        return jsonify({'error': 'URL not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_short_url():
    """Create a new short url when a long url is posted by the user """
    try:
        data = request.json
        original_url = data.get('originalUrl')
        custom_name = data.get('customName')

        # Get the original URL and custom name from the request data
        if not original_url:
            return jsonify({'error': 'Original URL is required'}), 400

        # Check if the original URL already exists
        existing_url = urls_collection.find_one({'originalUrl': original_url})
        if existing_url:
            formatted_url = {
                'id': str(existing_url['_id']),
                'originalUrl': existing_url['originalUrl'],
                'shortUrl': f"{BASE_URL}{existing_url['shortUrl']}",
                'createdAt': existing_url['createdAt'].isoformat()
            }
            return jsonify({'message': 'URL already exists', 'url': formatted_url}), 200

        # Generate a short URL if no custom name is provided
        if custom_name:
            existing_url = urls_collection.find_one({'shortUrl': custom_name})
            if existing_url:
                return jsonify({'error': 'Custom name already exists'}), 400
            short_url = custom_name
        else:
            short_url = generate_short_url()

        # Create a new URL document
        new_url = {
            'originalUrl': original_url,
            'shortUrl': short_url,
            'createdAt': datetime.utcnow()
        }

        # Insert the new URL document into the database
        result = urls_collection.insert_one(new_url)

        # Format the newly inserted URL document
        formatted_new_url = {
            'id': str(result.inserted_id),
            'originalUrl': new_url['originalUrl'],
            'shortUrl': f"{BASE_URL}{new_url['shortUrl']}",
            'createdAt': new_url['createdAt'].isoformat()
        }

        # Return a JSON response with the formatted URL object and a success status code
        return jsonify(formatted_new_url), 201
    except Exception as e:
        # Handle exceptions and return a JSON response with an error message and a 500 status code
        return jsonify({'error': str(e)}), 500