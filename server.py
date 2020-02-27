from flask import Flask, render_template, redirect, request, session
from mysqlconnection import connectToMySQL 



app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
		mysql = connectToMySQL()
		query = "INSERT INTO users (name, username, password) VALUES (%(name)s, %(username)s, %(password)s);"
		data = {
				"name": request.form['name'],
				"username": request.form['username'],
				"password": request.form['password'],
		}
		user = mysql.query_db(query, data)

		session['is_logged_in'] = True
		session['name'] = request.form['name']
		session['user_id'] = user

		return redirect("/")

@app.route('/display')
def display():
	mysql = connectToMySQL()
	users = mysql.query_db('SELECT * FROM users;') 
	return render_template("display.html", users = users)


@app.route('/delete', methods=['POST'])
def delete():
	mysql = connectToMySQL()
	query = "DELETE FROM users WHERE id = %(id)s;" 
	data = {
			"id": request.form['id'],
		}
	mysql.query_db(query, data)
	return redirect("/display")

@app.route('/edit', methods=['POST'])
def edit():
	mysql = connectToMySQL()
	query = "SELECT * FROM users WHERE id = %(id)s;" 
	data = {
			"id": request.form['id'],
		}
	user = mysql.query_db(query, data)
	return render_template("edit.html", user = user)

@app.route('/update', methods=['POST'])
def update():
	mysql = connectToMySQL()
	query = "UPDATE users SET name =  %(name)s, username = %(username)s, password = %(password)s  WHERE id =  %(id)s;" 
	data = {
			"id": request.form['id'],
			"name": request.form['name'],
			"username": request.form['username'],
			"password": request.form['password'],
		}
	mysql.query_db(query, data)
	return redirect("/display")


if __name__=="__main__":
    app.run(debug=True)
