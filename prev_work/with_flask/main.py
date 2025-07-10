import os
import smtplib
import requests
from dotenv import load_dotenv
from flask import Flask, render_template,request


load_dotenv()
my_email = os.environ['EMAIL']
password = os.environ['PASSWORD']

app = Flask(__name__)

def create_mail(user_email, write_data):
    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=my_email,password=password)
        connection.sendmail(
            from_addr = my_email,
            to_addrs= user_email,
            msg = f"Subject:NEW CONNECTION!!!\n\n{write_data}"
        )


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

@app.route('/contact', methods=['POST','GET'])
def form_entry():
    if request.method == 'POST':
        heading = "Your message has been successfully sent!!"
        data = request.form
        write_data = f'Name:{data["name"]}\n Email:{data["email"]}\n Phone:{data["phone"]}\n Message:{data["message"]}'
        create_mail(data["email"],write_data)
        return render_template('contact.html',msg_sent=True)
    else:
        return render_template('contact.html',msg_sent=False)

@app.route('/post/<int:id_no>')
def post_content(id_no):
    for post in posts:
        if post['id']== id_no:
            return render_template('post.html',content=post)

if __name__ == "__main__":
    app.run(debug=True)