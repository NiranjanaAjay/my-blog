from flask import Flask, render_template
import requests

app = Flask(__name__)

URL = "https://api.npoint.io/aaa4e12f25ec12eb7d77"
posts = requests.get(url=URL).json()


@app.route('/')
def home_page():
    return render_template('index.html',all_posts=posts)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/post/<int:id_no>')
def post_content(id_no):
    for post in posts:
        if post['id']== id_no:
            return render_template('post.html',content=post)

if __name__ == "__main__":
    app.run(debug=True)