#handle a POST request
from flask import Flask, request, jsonify, abort
import easyocr
import re

app = Flask(__name__)

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    reader = easyocr.Reader(['en'])
    r = re.compile("^[0-9]{5,6}$")
    path = request.get_json(force=True)["path"]
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    text = reader.readtext(path)
    text = [x[-2] for x in text]
    accession_no = list(filter(r.match, text))
    print(accession_no)
    if(len(accession_no) > 0):
        return accession_no[0]
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)