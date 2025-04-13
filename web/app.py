from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="movies",
        user="postgres",
        password="postgres"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, movie FROM reviews ORDER BY id DESC")
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', reviews=reviews)



@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    movie = request.form['movie']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO reviews (name, movie) VALUES (%s, %s)", (name, movie))
    conn.commit()
    cur.close()
    conn.close()

    return render_template('result.html', name=name, movie=movie)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
