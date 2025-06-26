from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)

URL= "https://api.npoint.io/c790b4d5cab58020d391"
content = requests.get(url=URL).json()
blogs = []
for i in content:
    new_obj = Post(i['id'],i['title'],i['subtitle'],i['body'])
    blogs.append(new_obj)

@app.route('/')
def home():
    return render_template("index.html", all_blogs=blogs)

@app.route('/post/<int:id_no>')
def post_content(id_no):
    required_post = None
    for blog in blogs:
        if blog.id_no == id_no:
            required_post = blog
    return render_template("post.html",post = required_post)

if __name__ == "__main__":
    app.run(debug=True)
