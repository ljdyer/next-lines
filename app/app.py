from flask import Flask, request, jsonify, render_template

from next_lines import answer_question
from text_assets import title, blurb

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "iogfvosupo"


# ====================
@app.route('/')
def index():
    """Render index.html on app launch"""

    return render_template('index.html')


# ====================
@app.route("/get_answer", methods=["POST"])
def get_answer():

    input_line = request.data
    answer = answer_question(str(input_line))

    return jsonify(answer)


# ====================
if __name__ == "__main__":

    app.run(debug=True)
