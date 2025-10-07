#!/usr/bin/env python3
"""
Simple test server for frontend development
"""
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, 
            template_folder='frontend/templates', 
            static_folder='frontend/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('frontend/static', filename)

if __name__ == "__main__":
    print("Starting test server on http://localhost:5002")
    print("Open your browser and go to: http://localhost:5002")
    app.run(debug=True, port=5002) 