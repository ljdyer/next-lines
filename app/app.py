from flask import Flask, request, session

from next_lines import answer_question
from text_assets import title, blurb

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "iogfvosupo"


# ====================
@app.route("/", methods=["GET", "POST"])
def adder_page():
    # Set up session variable to store dialogue history
    if "dialogue" not in session:
        session["dialogue"] = []
    if request.method == "POST":
        question = str(request.form["this_line"])
        # If the question field is not empty, add the question and response
        # to the dialogue history
        if question:
            answer = answer_question(question)
            session["dialogue"].append(f'{question.strip(".")}...<br>' +
                                       f"...{answer['next_line']}<br>" +
                                       f"{answer['song_name']} by {answer['artist_name']}<br>")
            if len(session["dialogue"]) > 5:
                session["dialogue"] = session["dialogue"][-5:]
            session.modified = True
    return f'''
        <html>
            <head>
                <link rel="stylesheet" link href="/static/css/base.css">
            </head>
            <body onLoad="document.getElementById('this_line').focus();">
                <pre>{title}</pre>
                <p>{blurb}</p>
                <form method="post" action=".">
                    <div class="row" style="width: 100%">
                        <input name="this_line" id="this_line" />
                        <input type="submit" value="Ask" id="ask" />
                    </div>
                    <p>{'<br><br>'.join(session["dialogue"])}</p>
                </form>
            </body>
            ''' + '''
            <script>
            if ( window.history.replaceState ) {
              window.history.replaceState( null, null, window.location.href );
            }
            </script>
        </html>
    '''


# ====================
if __name__ == "__main__":

    app.run(debug=True)