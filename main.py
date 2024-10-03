""" This script run the flask app"""
from flask import Flask, jsonify
from src.utils import create_short_url, get_one_url, get_all_urls


app = Flask(__name__)


@app.route('/get_all_urls', methods=['GET'])
def all_urls():
    """This function returns all the url stored in the database"""
    return jsonify(get_all_urls())


@app.route('/urls/<string:url_id>', methods=['GET'])
def one_url(url_id):
    """This function only returns on url stored in the database using the url id"""
    # Call the function and return the result
    return jsonify(get_one_url(url_id))


@app.route('/urls', methods=['POST'])
def short_url():
    """ This function return short url when posted with a url"""
    return jsonify(create_short_url())


if __name__ == '__main__':
    app.run(debug=True)
