from flask import Flask, request, render_template, url_for, redirect

from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql10.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql10295050'
app.config['MYSQL_PASSWORD'] = 'lBShTY5uYZ'
app.config['MYSQL_DB'] = 'sql10295050'
mysql = MySQL(app)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET','POST'])
def cadastro():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        name = request.form.get("Nome")
        email = request.form.get("Email")
        password = request.form.get("Senha")

        if name and email:
            cur.execute('''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''', (name, email, password))
            mysql.connection.commit()    

    return redirect(url_for('index'))

@app.route("/perfil")
def perfil():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        email = request.values.get("Email")
        senha = request.values.get("Senha")

        cur.execute('''SELECT id FROM users WHERE (email = '%s')''',(email))
        id = cur.fetchone()
    
    if(id != None):
        cur.execute('''SELECT name FROM users WHERE (id = %s)''',[id])
        name = cur.fetchone()
        cur.execute('''SELECT doctor_id FROM users WHERE (id = %s)''',[id])
        doctor_id = cur.fetchone()

        if (doctor_id != None):
            cur.execute('''SELECT name FROM doctors WHERE (id = %s)''',[doctor_id])
            doctor_name = cur.fetchone()
        else: 
            doctor_name = None

        return render_template("calendario.html",id=id, name=name, doctor_id=doctor_id,doctor_name=doctor_name)
    
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=8085)

