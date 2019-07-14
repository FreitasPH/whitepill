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
    return render_template("pre_cadastro.html")

@app.route("/tipousuario", methods=['GET', 'POST'])
def tipousuario():
    if request.method == "POST":
        option = request.form["Tipo"]
        session['tipo'] = option

        if option == '1':
            return render_template("cadastro.html")
        else:
            return render_template("cadastromedico.html")

@app.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        name = str(request.form["Nome"])
        email = str(request.form["Email"])
        
        if name and email:
            
            if session['tipo'] == '1':
                password = str(request.form["Senha"])
                cur.execute('''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''', (name, email, password))
                
            else:
                crm = str(request.form["CRM"])
                cur.execute('''INSERT INTO doctors (name, email, crm) VALUES (%s, %s, %s)''', (name, email, crm))
                
            mysql.connection.commit()    

    return redirect(url_for('index'))

@app.route("/event", methods=['GET', 'POST'])
def event():
    cur = mysql.connection.cursor()
    id = session['id']

    if 'Day' in request.form:
        day = request.form["Day"]
        session['day'] = day

    day = session['day']

    cur.execute('''SELECT * FROM day_status WHERE user_id = %s AND date = %s''', (id, day))
    status = cur.fetchone()
    cur.execute('''SELECT * FROM events WHERE user_id = %s AND date = %s''', (id, day))
    events = cur.fetchall()

    if status or events:
        msg_sintomas = "Você não apresenta sintomas nesse dia."
        msg_status = "Você naõ registrou como foi o seu dia."
        if events:
            msg_sintomas = ""
            for row in events:
                msg_sintomas = msg_sintomas + str(row[2]) + "\n" 
        if status:
            if status[3] == 1:
                msg_status = "Seu dia foi muito ruim"
            if status[3] == 2:
                msg_status = "Seu dia foi ruim"
            if status[3] == 3:
                msg_status = "Seu dia foi neutro"
            if status[3] == 4:
                msg_status = "Seu dia foi bom"
            if status[3] == 5:
                msg_status = "Seu dia foi muito bom" 
        return render_template("newevent.html", msg_sintomas=msg_sintomas, msg_status=msg_status)
    else:
        return render_template("event.html", day=day)

@app.route("/insertevent", methods=['GET', 'POST'])
def insertevent():
    cur =  mysql.connection.cursor()
    user_id = session['id']
    day = session['day']

    if request.method == 'POST':
        if 'Status' in request.form:
            status = request.form["Status"]

            cur.execute('''SELECT * FROM day_status WHERE user_id = %s AND date = %s''', (user_id, day))
            line = cur.fetchone()
            
            if line:
                cur.execute('''UPDATE day_status SET status = %s WHERE user_id = %s AND date = %s''',(status, user_id, day))
                
            else:
                cur.execute('''INSERT INTO day_status (user_id, date, status) VALUES (%s, %s, %s)''', (user_id, day, status))

            mysql.connection.commit()    

        if 'Sintoma' in request.form:
            symptom = request.form["Sintoma"]

            if len(symptom) > 0:
                cur.execute('''INSERT INTO events (user_id, symptom, date) VALUES (%s, %s, %s)''', (user_id, symptom, day))
                mysql.connection.commit()

    return redirect(url_for('event'))


@app.route("/userpage", methods=['GET', 'POST'])
def userpage():
    cur = mysql.connection.cursor()

    id = session['id']

    cur.execute('''SELECT * FROM medicine WHERE status='A' AND user_id=%s''', [id])
    medicamentos = cur.fetchall()

    msg_remedios = "Remédios em uso:\n"
    if medicamentos:
        for row in medicamentos:
            msg_remedios = msg_remedios + str(row[3]) + ", " + str(row[4]) + "mg\n"
    else:
        msg_remedios = msg_remedios +"Nenhum"


    return render_template("calendario.html", msg_remedios=msg_remedios)

@app.route("/medicamento", methods=['GET', 'POST'])
def medicamento():
    id = session['id']

    cur = mysql.connection.cursor()

    cur.execute('''SELECT * FROM historic WHERE user_id = %s''', [id])
    historico = cur.fetchall()

    msg_historico = "Não existem registros anteriores"

    if historico:
        msg_historico = "Histórico:\n\n"
        for row in historico:
            medicine_id = row[8]
            cur.execute('''SELECT * from medicine WHERE id = %s''',[medicine_id])
            medicine = cur.fetchone()
            if row[3] == 'I':
                acao = 'Inicio do uso do medicamento'
            else:
                acao = 'Fim do uso do medicamento'

            msg_historico = msg_historico + "Medicamento: "+str(medicine[3])+"\nQuantidade: "+str(medicine[4])+"\n"+acao+"\nDia da alteração: "+str(row[4])+"\nResumo:"+str(row[5])+"\nRazão: "+str(row[6])+"\nObservação: "+str(row[7])+"\n\n"
    
    return render_template("medicamentos.html", msg_historico=msg_historico)

@app.route("/altermedicine", methods=['GET','POST'])
def altermedicine():
    id = session['id']
    cur = mysql.connection.cursor()

    if "Tipo" in request.form:
        tipo = request.form["Tipo"]
        if tipo == '1':
            nome = request.form["Nome"]
            quant = request.form["Quant"]
            dia = request.form["Dia"]
            crm = request.form["CRM"]
            resumo = request.form["Resumo"]
            motivo = request.form["Motivo"]
            obs = request.form["Obs"]

            if len(nome) > 0 and len(quant) > 0 and len(crm) > 0 and len(dia) > 0:
                cur.execute('''SELECT * FROM doctors WHERE crm=%s''',[crm])
                doctor = cur.fetchone()
                doctor_id = doctor[0]

                cur.execute('''INSERT INTO medicine (user_id, doctor_id, name, quant, status) VALUES (%s, %s, %s, %s, 'A')''', (id,doctor_id,nome,quant))
                mysql.connection.commit()

                cur.execute('''SELECT * FROM medicine WHERE status = 'A' AND user_id = %s AND quant = %s AND name = %s''',(id, quant, nome))            
                med = cur.fetchone()
                med_id = med[0]

                cur.execute('''INSERT INTO historic (user_id, doctor_id, acao, date, resume, reason, obs, medicine_id) VALUES (%s, %s,'I', %s, %s, %s, %s, %s)''', (id, doctor_id, dia, resumo, motivo, obs, med_id))
                mysql.connection.commit()
        else:
            nome = request.form["Nome"]
            dia = request.form["Dia"]
            crm = request.form["CRM"]
            resumo = request.form["Resumo"]
            motivo = request.form["Motivo"]
            obs = request.form["Obs"]

            if len(nome) > 0 and len(crm) > 0 and len(dia) > 0:
                cur.execute('''SELECT * FROM medicine WHERE status = 'A' AND user_id = %s AND name = %s''',(id, nome))                        
                med = cur.fetchone()
                
                if med:
                    med_id = med[0]

                    cur.execute('''SELECT * FROM doctors WHERE crm=%s''',[crm])
                    doctor = cur.fetchone()
                    doctor_id = doctor[0]

                    cur.execute('''UPDATE medicine SET status = 'I' WHERE user_id = %s AND name = %s''',(id, nome))
                    mysql.connection.commit()
                    
                    cur.execute('''INSERT INTO historic (user_id, doctor_id, acao, date, resume, reason, obs, medicine_id) VALUES (%s, %s, 'R', %s, %s, %s, %s, %s)''',(id, doctor_id, dia, resumo, motivo, obs, med_id))
                    mysql.connection.commit()

    return redirect(url_for('medicamento'))

@app.route("/perfil",  methods=['GET', 'POST'])
def perfil():
    msg = ''

    if request.method == 'POST' and 'Email' in request.form and 'Senha' in request.form:
        
        cur = mysql.connection.cursor()
        
        email = str(request.form["Email"])
        senha = str(request.form["Senha"])
        
        cur.execute('''SELECT * FROM users WHERE email = %s AND password = %s''',(email, senha))
        account = cur.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['name'] = account[1]

            cur.execute('''SELECT doctor_id FROM users WHERE email = %s''',[email])
            doctor_id = cur.fetchone()
                
            if (doctor_id != None):
                cur.execute('''SELECT name FROM doctors WHERE (id = %s)''',[doctor_id])
                doctor_name = cur.fetchone()
                session['doctor_name'] = doctor_name
                session['has_doctor'] = True
            else:
                doctor_name = None
                session['has_doctor'] = False

            return redirect(url_for('userpage'))
        else:
            return render_template("index_erro.html", msg = 'Senha incorreta.')
    
    else:
        return render_template("index_erro.html", msg = 'Favor preencher todos os campos.')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('name', None)
   session.pop('crm', None)
   session.pop('day', None)
   
   return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=8085)

