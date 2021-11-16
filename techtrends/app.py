import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
import sys

# Function to get a database connection.
# This function connects to database with the name `database.db`

conn_counter = 0

def get_db_connection():
    global conn_counter

    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    conn_counter += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
       
      ## About page retrieved
        app.logger.info("Non-Existing Article")
        logger.info("404 - Article does not exists")
        logger.addHandler(h1)
        logger.addHandler(h2)
        return render_template('404.html'), 404
    else:
        ## About page retrieved
        app.logger.info('Article \"' +post['title']+ '\" retrieved!')  
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
     ## About page retrieved
    app.logger.info("/About Request Succesfully")
    logger.info("About Us")
    logger.addHandler(h1)
    logger.addHandler(h2)
    return render_template('about.html')

@app.route('/healthz')
def status():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )

    ## log line
    app.logger.info('Status request successfull')

    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    response = app.response_class(
        response=json.dumps({"status": "success", "code": 0, "data": {"db_connection_count": conn_counter, "post_count": len(posts)}}),
        status=200,
        mimetype='application/json'
    )

    ## log line
    app.logger.info('Metrics request successfull')

    return response

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            ## Title created
            app.logger.info("Article Created")
            logger.info(f"Article {title} created")
            logger.addHandler(h1)
            logger.addHandler(h2)

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
    ## stream logs to app.log file
    logger = logging.getLogger("__name__")
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    h1 = logging.StreamHandler(sys.stdout)
    h1.setLevel(logging.DEBUG)
    h2 = logging.StreamHandler(sys.stderr)
    h2.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port='3111')
