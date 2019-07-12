# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'gfU7Lj7r3E'

app.config['MYSQL_HOST'] = 'sql10.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql10295050'
app.config['MYSQL_PASSWORD'] = 'lBShTY5uYZ'
app.config['MYSQL_DB'] = 'sql10295050'

mysql = MySQL(app)

@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html", msg='')

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        name = str(request.form["Nome"])
        email = str(request.form["Email"])
        password = str(request.form["Senha"])

        if name and email:
            cur.execute('''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''', (name, email, password))
            mysql.connection.commit()    

    return redirect(url_for('index'))

@app.route("/perfil",  methods=['GET', 'POST'])
def perfil():
    msg = ''

    if request.method == 'POST' and 'Email' in request.form and 'Senha' in request.form and 'TipoUsuario' in request.form:
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        email = str(request.form["Email"])
        senha = str(request.form["Senha"])
<<<<<<< HEAD
<<<<<<< HEAD
        tipo = request.form["TipoUsuario"]

        if tipo == '1':
            cur.execute('''SELECT * FROM users WHERE email = %s AND password = %s''',(email, senha))
            account = cur.fetchone()
        
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['name'] = account['name']

                cur.execute('''SELECT doctor_id FROM users WHERE email = %s''',[email])
                doctor_id = cur.fetchone()
                
                if (doctor_id != None):
                    cur.execute('''SELECT name FROM doctors WHERE (id = %s)''',[doctor_id])
                    doctor_name = cur.fetchone()
                else:
                    doctor_name = None

                return render_template("usertouser.html")
            else:
                return render_template("index_erro.html", msg = 'Senha incorreta.')
        else:
            cur.execute('''SELECT * FROM doctors WHERE email = %s AND password = %s''',(email, senha))
            account = cur.fetchone()
        
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['name'] = account['name']
                session['crm'] = account['crm']

                return render_template("doctortodoctor.html")
            else:
                return render_template("index_erro.html", msg = 'Senha incorreta.')
    else:
        return render_template("index_erro.html", msg = 'Favor preencher todos os campos.')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('name', None)
   session.pop('crm', None)
   
   return redirect(url_for('index'))
=======
=======
        tipo = request.form["TipoUsuario"]
>>>>>>> 444fcebda501f8dead13715fdb16cd08fd57ad41

        if tipo == '1':
            cur.execute('''SELECT * FROM users WHERE email = %s AND password = %s''',(email, senha))
            account = cur.fetchone()
        
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['name'] = account['name']

                cur.execute('''SELECT doctor_id FROM users WHERE email = %s''',[email])
                doctor_id = cur.fetchone()
                
                if (doctor_id != None):
                    cur.execute('''SELECT name FROM doctors WHERE (id = %s)''',[doctor_id])
                    doctor_name = cur.fetchone()
                else:
                    doctor_name = None

                return render_template("usertouser.html")
            else:
                return render_template("index_erro.html", msg = 'Senha incorreta.')
        else:
            cur.execute('''SELECT * FROM doctors WHERE email = %s AND password = %s''',(email, senha))
            account = cur.fetchone()
        
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['name'] = account['name']
                session['crm'] = account['crm']

                return render_template("doctortodoctor.html")
            else:
                return render_template("index_erro.html", msg = 'Senha incorreta.')
    else:
        return render_template("index_erro.html", msg = 'Favor preencher todos os campos.')
>>>>>>> 75670cab031053a065ac00026d59d876a42f7665

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('name', None)
   session.pop('crm', None)
   
   return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=8085)

