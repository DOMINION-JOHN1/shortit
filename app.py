from flask import Flask, jsonify
from src.utils import create_short_url, get_one_url, get_all_urls


app = Flask(__name__)


@app.route('/get_all_urls', methods=['GET'])
def get_all_urls():
    return jsonify(get_all_urls())


@app.route('/urls/<string:url_id>', methods=['GET'])
def get_one_url(url_id):
    # Call the function and return the result
    return jsonify(get_one_url(url_id))


@app.route('/urls', methods=['POST'])
def create_short_url():
    return jsonify(create_short_url())


if __name__ == '__main__':
    app.run(debug=True)
