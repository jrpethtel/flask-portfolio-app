from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

#Establishes a db connection to the sqlite db file.
def get_db_connection():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	return conn

#Gets a post based on id.
def get_post(post_id):
	conn = get_db_connection()
	post = conn.execute('SELECT * FROM posts WHERE id = ?',
						(post_id,)).fetchone()
	conn.close()
	if post is None:
		abort(404)
	return post

#Initializes the app.
app = Flask(__name__)
#Establishes a secret for the app in order to utilize session for flash messages.
app.config['SECRET_KEY'] = '123456'

#Home route.  Returns a list of all posts from the sqlite db.
@app.route('/')
def index():
	conn = get_db_connection()
	posts = conn.execute('SELECT * FROM posts').fetchall()
	conn.close()
	return render_template('index.html', posts=posts)

#About route.  Takes user to a simple About template.
@app.route('/about', methods=('GET',))
def about():
	return render_template('about.html')

#Post route. Returns a single post from the sqlite db.
@app.route('/<int:post_id>')
def post(post_id):
	post = get_post(post_id)
	return render_template('post.html', post=post)

#Create route. Provides create form for User to create a new post.
@app.route('/create', methods=('GET','POST'))
def create():
	
	if request.method == 'GET':
		return render_template('create.html')

	if request.method == 'POST':
		title = request.form['title']
		summary = request.form['summary']
		sourceLink = request.form['sourceLink']
		appLink = request.form['appLink']

		if not title:
			flash('Title is required! Cannot create Post.')
			return redirect(url_for('index'))

		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO posts (title, summary, sourceLink, appLink) VALUES (?,?,?,?)',
					(title, summary, sourceLink, appLink))
			conn.commit()
			conn.close()
			return redirect(url_for('index'))

#Edit route. Gets a single post and provides edit form for User.
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        sourceLink = request.form['sourceLink']
        appLink = request.form['appLink']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, summary = ?, sourceLink = ?, appLink = ?'
                         ' WHERE id = ?',
                         (title, summary, sourceLink, appLink, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

#Delete route.  Accepts a single post id and deletes it from sqlite db.
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
	post = get_post(id)

	conn = get_db_connection()
	conn.execute('DELETE FROM posts WHERE id = ?', (id,))
	conn.commit()
	conn.close()
	flash ('{} was successfully deleted!'.format(post['title']))
	return redirect(url_for('index'))









