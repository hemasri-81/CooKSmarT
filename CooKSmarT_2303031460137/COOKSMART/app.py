# app.py
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from models import db
from graphs import build_substitution_graph, build_inverted_index
from engine import suggest_recipes

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    # DB file placed next to this file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cooksmart.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # simple in-memory cache for graphs; rebuild if DB changes (restart server)
    app.sub_graph = None
    app.inv_index = None

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/suggest', methods=['POST'])
    def api_suggest():
        payload = request.get_json() or {}
        available = payload.get('available_ingredients', [])
        if not isinstance(available, list):
            return jsonify({'error': 'available_ingredients should be a list'}), 400

        # lazy build
        if app.sub_graph is None:
            app.sub_graph = build_substitution_graph(db.session)
        if app.inv_index is None:
            app.inv_index = build_inverted_index(db.session)

        suggestions = suggest_recipes(db.session, app.sub_graph, app.inv_index, available)
        return jsonify({'suggestions': suggestions})

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host='0.0.0.0', port=5000)
