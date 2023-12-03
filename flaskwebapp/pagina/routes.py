from pagina import app
from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb.cursors
import os
import pandas as pd
import mysql.connector
import re
import pymysql 
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import MySQLdb




app.secret_key = "1234"
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'arquitectura'

mysql = MySQL(app)


@app.get("/")
def index():
    return render_template("index.html")


@app.route("/secretaria", methods =['GET', 'POST'])
def secretaria():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
 
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT rut_secre, contrasenasec FROM secretaria WHERE correosec = '{email}'")
        user = cur.fetchone()
        cur.close()
 
        if user and password == user[1]:
            session ['correosec'] = user[0]
            return redirect(url_for('pacientes'))
        else:
            return render_template("secretaria.html", error= "Usuario no encontrado")
    return render_template("secretaria.html")

@app.route("/paciente", methods =['GET', 'POST'])
def paciente():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
 
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT rut_paciente, contrasenapac FROM paciente WHERE correopac = '{email}'")
        user = cur.fetchone()
        cur.close()
 
        if user and password == user[1]:
            session['rut_paciente'] = user[0]
            return redirect(url_for('pacienteindiv'))
        else:
            return render_template("paciente.html", error= "Usuario no encontrado")
    return render_template("paciente.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/registro", methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        rut = request.form['rut']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(f"insert into paciente values ('{rut}','{nombre}','{apellido}','{email}','{password}')")
        mysql.connection.commit()
        cur.close()
        return render_template("paciente.html")
    return render_template("registracion.html")



@app.route("/doctors")
def doctors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM agenda_doc WHERE disponible = 1")
    data = cur.fetchall()
    cur.close()
    return render_template("doctors.html", data=data)

@app.route("/pacientes", methods=['GET','POST'])
def pacientes():
    if 'correosec' not in session:
        return redirect(url_for('secretaria'))
    if request.method == 'POST':
        rut = request.form['rut']
        fecha = request.form['fecha']
        correo = request.form['correo']
        disponible = request.form['disponible']

        cur = mysql.connection.cursor()
        cur.execute(f"update agenda_doc set disponible=1, rut_paciente={rut} where fecha='{fecha}' AND rut_doc ='{correo}';")
        mysql.connection.commit()
        cur.close()
        return render_template("pacientes.html")
    return render_template("pacientes.html")

@app.route("/pacienteindiv", methods=['GET','POST'])
def pacienteindiv():
    if request.method == 'POST': 
        fecha = request.form['fecha']
        correo = request.form['correo']
        disponible = request.form['disponible']
        rut_paciente = session.get('rut_paciente')
        if rut_paciente:
            cur = mysql.connection.cursor()
            cur.execute(f"UPDATE agenda_doc SET disponible=1, rut_paciente={rut_paciente} WHERE fecha='{fecha}' AND rut_doc='{correo}';")
            mysql.connection.commit()
            cur.close()
            return render_template("pacienteindiv.html")
        else:
            return "Paciente no está logeado."

    return render_template("pacienteindiv.html")

@app.route("/logoutp")
def logoutp():
    session.clear()
    return redirect(url_for('paciente'))

@app.route("/logouts")
def logouts():
    session.clear()
    return redirect(url_for('secretaria'))