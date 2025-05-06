from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Load projects from JSON
def load_projects():
    with open('data/projects.json', 'r') as f:
        return json.load(f)

# Email config (set your own email env variables)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    projects = load_projects()
    return render_template('projects.html', projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(f"Message from {name}",
                      sender=email,
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = message
        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except:
            flash('Failed to send message. Try again later.', 'danger')
        return redirect('/contact')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
