"""
Flask Web Interface for the Python Translator
Run with: python app.py
Access at: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from googletrans import Translator
import os
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
translator = Translator()

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'hi': 'Hindi',
    'ar': 'Arabic',
    'tr': 'Turkish',
}


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', languages=SUPPORTED_LANGUAGES)


@app.route('/api/translate', methods=['POST'])
def translate_api():
    """API endpoint for translation"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400
        
        text = data.get('text', '').strip() if data.get('text') else ''
        src_lang = data.get('source_lang', 'auto')
        dest_lang = data.get('dest_lang', 'en')
        
        if not text:
            return jsonify({'success': False, 'error': 'Text cannot be empty'}), 400
        
        if not src_lang or not dest_lang:
            return jsonify({'success': False, 'error': 'Source and destination languages must be specified'}), 400
        
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        
        return jsonify({
            'success': True,
            'original': text,
            'translated': result.text,
            'source_lang': src_lang,
            'dest_lang': dest_lang,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Translation error: {str(e)}'}), 500


@app.route('/api/detect', methods=['POST'])
def detect_api():
    """API endpoint for language detection"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400
        
        text = data.get('text', '').strip() if data.get('text') else ''
        
        if not text:
            return jsonify({'success': False, 'error': 'Text cannot be empty'}), 400
        
        detection = translator.detect(text)
        lang_code = detection.lang
        lang_name = SUPPORTED_LANGUAGES.get(lang_code, 'Unknown')
        confidence = detection.confidence if detection.confidence else 0.0
        
        return jsonify({
            'success': True,
            'text': text,
            'language': lang_name,
            'code': lang_code,
            'confidence': float(confidence) if confidence else 0.0,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Detection error: {str(e)}'}), 500


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """API endpoint to get supported languages"""
    return jsonify({
        'success': True,
        'languages': SUPPORTED_LANGUAGES,
        'total': len(SUPPORTED_LANGUAGES)
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'Python Translator API',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("="*60)
    print("  Starting Python Translator Flask Server")
    print("="*60)
    print("\n📡 API Endpoints:")
    print("  POST   /api/translate - Translate text")
    print("  POST   /api/detect    - Detect language")
    print("  GET    /api/languages - Get supported languages")
    print("  GET    /api/health    - Health check")
    print("\n🌐 Web Interface:")
    print("  http://localhost:5000")
    print("\n" + "="*60)
    app.run(debug=True, port=5000, use_reloader=False)

