from flask import Flask, render_template, request, session, jsonify
import random
import os

app = Flask(__name__)
app.secret_key = 'dota2_ranker_secret'

HEROES = [
    {"id": 1, "name": "Anti-Mage", "img": "static/assets/heroes/antimage.png"},
    {"id": 2, "name": "Bane", "img": "static/assets/heroes/bane.png"},
    {"id": 3, "name": "Brewmaster", "img": "static/assets/heroes/brewmaster.png"},
    {"id": 4, "name": "Centaur", "img": "static/assets/heroes/centaur.png"},
    {"id": 5, "name": "Dawnbreaker", "img": "static/assets/heroes/dawnbreaker.png"},
    {"id": 6, "name": "Faceless Void", "img": "static/assets/heroes/faceless_void.png"},
    {"id": 7, "name": "Huskar", "img": "static/assets/heroes/huskar.png"},
    {"id": 8, "name": "Juggernaut", "img": "static/assets/heroes/juggernut.png"},
    {"id": 9, "name": "Kez", "img": "static/assets/heroes/kez.png"},
    {"id": 10, "name": "Lion", "img": "static/assets/heroes/lion.png"},
    {"id": 11, "name": "Lone Druid", "img": "static/assets/heroes/lone_druid.png"},
    {"id": 12, "name": "Mars", "img": "static/assets/heroes/mars.png"},
    {"id": 13, "name": "Meepo", "img": "static/assets/heroes/meepo.png"},
    {"id": 14, "name": "Phantom Lancer", "img": "static/assets/heroes/phantom_lancer.png"},
    {"id": 15, "name": "Slardar", "img": "static/assets/heroes/slardar.png"},
    {"id": 16, "name": "Sniper", "img": "static/assets/heroes/sniper.png"},
    {"id": 17, "name": "Storm Spirit", "img": "static/assets/heroes/storm_spirit.png"},
    {"id": 18, "name": "Sven", "img": "static/assets/heroes/sven.png"},
    {"id": 19, "name": "Tinker", "img": "static/assets/heroes/tinker.png"},
    {"id": 20, "name": "Underlord", "img": "static/assets/heroes/underlord.png"},
    {"id": 21, "name": "Undying", "img": "static/assets/heroes/undying.png"},
    {"id": 22, "name": "Zeus", "img": "static/assets/heroes/zuus.png"},
]

def init_tournament():
    heroes = HEROES.copy()
    random.shuffle(heroes)
    session['hero_a'] = heroes[0]
    session['hero_b'] = heroes[1]
    session['remaining'] = heroes[2:]
    session['matches_completed'] = 0
    session['total_matches'] = len(heroes) - 1
    session['finished'] = False

@app.route('/')
def index():
    init_tournament()
    return render_template('index.html')

@app.route('/state', methods=['GET'])
def get_state():
    if 'hero_a' not in session:
        init_tournament()
    
    if session['finished']:
        # The winner is the one who survived the last match
        return jsonify({
            'finished': True,
            'winner': session['last_winner']
        })

    return jsonify({
        'finished': False,
        'hero_a': session['hero_a'],
        'hero_b': session['hero_b'],
        'match': session['matches_completed'] + 1,
        'total': session['total_matches'],
        'progress': (session['matches_completed'] / session['total_matches']) * 100 if session['total_matches'] > 0 else 0
    })

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    winner_id = data.get('winner_id')
    
    hero_a = session['hero_a']
    hero_b = session['hero_b']
    remaining = session['remaining']
    
    # Determine which hero won and which one to replace
    if hero_a['id'] == winner_id:
        winner = hero_a
        # Keep hero_a, replace hero_b
        if not remaining:
            session['finished'] = True
            session['last_winner'] = winner
        else:
            session['hero_b'] = remaining.pop(0)
    else:
        winner = hero_b
        # Keep hero_b, replace hero_a
        if not remaining:
            session['finished'] = True
            session['last_winner'] = winner
        else:
            session['hero_a'] = remaining.pop(0)
    
    session['remaining'] = remaining
    session['matches_completed'] += 1
    session.modified = True
    
    return get_state()

@app.route('/restart', methods=['POST'])
def restart():
    init_tournament()
    return get_state()

if __name__ == '__main__':
    # Слушаем на 0.0.0.0, чтобы сервер был доступен в сети
    app.run(host='0.0.0.0', port=5000)
