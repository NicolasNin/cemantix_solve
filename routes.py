from flask import Blueprint, jsonify, request,current_app,render_template
from api_score import *
main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Basic form for testing
    return render_template('index.html', strategy='external')
@main.route('/send_word', methods=['POST'])
def send_word():
    word = request.form['word']
    solver = current_app.config['SOLVER']
    try:
        result = solver.send_word(word)
        if "score" in result:
            result["score"] = round(float(result["score"]),4)
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@main.route('/analyze')
def analyze():
    return "Analysis route"

@main.route('/random_word', methods=['GET'])
def random_word():
    try:
        solver = current_app.config['SOLVER']
        word = solver.get_random_word()
        return jsonify({"status": "success", "word": word})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    
@main.route('/find_similar', methods=['POST'])
def find_similar():
    try:
        word = request.form['word']
        score = float(request.form['score'])  # Convert string to float
        solver = current_app.config['SOLVER']
        similar_words = solver.get_possible_words_from_score(word, score)
        return jsonify({"status": "success", "words": similar_words})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@main.route('/switch_strategy', methods=['POST'])
def switch_strategy():
    try:
        strategy_type = request.form['strategy']
        solver = current_app.config['SOLVER']
        print(strategy_type)
        if strategy_type == 'local':
            game = current_app.config['GAME']  # Get existing game instance
            solver.set_score_strategy(LocalGameStrategy(game))
        else:  # external
            solver.set_score_strategy(ExternalAPIStrategy())
            
        return jsonify({"status": "success", "strategy": strategy_type})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    
@main.route('/local')
def local():
    # Switch to local strategy first
    solver = current_app.config['SOLVER']
    game = current_app.config['GAME']
    solver.set_score_strategy(LocalGameStrategy(game))
    return render_template('index.html', strategy='local')

@main.route('/new_game', methods=['POST'])
def new_game():
    try:
        game = current_app.config['GAME']
        game.init_random_word()
        solver = current_app.config['SOLVER']
        solver.reset()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400