from flask import Flask, request, jsonify, render_template
from datetime import datetime 

class Comment:
    def __init__(self, content, author, timestamp):
        self.content = content
        self.author = author
        self.timestamp = timestamp

class CommentManager:
    def __init__(self):
        self.comments = []

    def add_comment(self, content, author):
        new_comment = Comment(content, author, datetime.now())
        self.comments.append(new_comment)

    def get_comments(self):
        return self.comments

comments_manager = CommentManager()  # Singleton instance

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", comments=comments_manager.get_comments())

@app.route("/submit_comment", methods=["POST"])
def submit_comment():
    content = request.form.get('content')
    author = request.form.get('author', 'NoOne')
    
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400

    # Escape content and author to prevent XSS -- without escape() for now 
    escaped_content = content
    escaped_author = author

    comments_manager.add_comment(escaped_content, escaped_author)
    return render_template('index.html', comments=comments_manager.get_comments())

@app.route("/forest_comment", methods=["GET"])
def forest_comment():
    return render_template('index.html', comments=comments_manager.get_comments())

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("q")
    else:
        query = request.args.get("q")
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Escape query to prevent XSS
    escaped_query = escape(query)
    
    return jsonify({"message": f"You searched for: {escaped_query}!"})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
