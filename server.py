import json
import time
from flask import Flask, jsonify
from flask_cors import CORS
import news_fetcher
import gpt4_summarizer

app = Flask(__name__)
CORS(app)

def update_news_data():
    news_items = news_fetcher.get_top_stories()
    summarized_items = gpt4_summarizer.process_news_items(news_items)

    with open('news_data.json', 'w') as outfile:
        json.dump(summarized_items, outfile)

@app.route('/get_news', methods=['GET'])
def get_news():
    with open('news_data.json', 'r') as infile:
        news_data = json.load(infile)
    return jsonify(news_data)

if __name__ == '__main__':
    app.run(debug=True)
