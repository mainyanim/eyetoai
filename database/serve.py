from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)



@app.route("/", methods=['POST'])
def notes_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        condition = str(request.data.get('condition'))
        findings = request.data.get('findings')
        return condition,, status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]



if __name__ == "__main__":
    app.run(debug=True)