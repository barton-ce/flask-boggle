from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET KEY"] = "secretKey123"
app.secret_key = "secret?"

boggle_game = Boggle()


@app.route("/")
def homepage():

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    return render_template("index.html", board=board, highscore=highscore, numplays=numplays)


@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({"result": response})


@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json['score']
    highscore = session.get('highschore', 0)
    numplays = session.get('numplays', 0)

    session['numplays'] = numplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newRecord=score > highscore)
