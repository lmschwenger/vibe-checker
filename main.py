from flask import Flask, request, render_template, jsonify
from my_code.my_code import Analyzer
import uuid

app = Flask(__name__)

# Temporary storage for analysis results
results = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    analyzer = Analyzer()

    highlighted_html = analyzer.analyze_website(url)

    # Generate a unique ID for this result
    result_id = str(uuid.uuid4())
    results[result_id] = highlighted_html

    return jsonify({'result_id': result_id})


@app.route('/result/<result_id>')
def result(result_id):
    highlighted_html = results.get(result_id, "No result found.")

    return render_template('result.html', highlighted_html=highlighted_html)


if __name__ == '__main__':
    app.run(debug=True)
