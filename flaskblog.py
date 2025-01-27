from flask import Flask, render_template, request

from main import main

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    search_query = request.args.get('search')
    search_type = request.args.get('search_type')
    filter_type = request.args.get('filter')
    filter_search = request.args.get('filter_search')
    papers = main(search_query.lower(), search_type.lower(), filter_type, filter_search.lower())  # Convert to lowercase before sending
    try:
        return render_template('search.html', papers=papers)
    except Exception as e:
        print(f"Template rendering error: {e}")

# Enable debugging mode during development
if __name__ == '__main__':
    app.run(debug=False)