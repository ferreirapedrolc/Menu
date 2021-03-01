from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from main import dbcolumns, winetree
import sqlite3
import pandas as pd




app = Flask(__name__)
app.config['SECRET_KEY'] = 'marujo'
dbfile = 'registros.db'
tabelaregistros = 'registros'
tabelabebidas = 'bebidas'



class FormBebidas(FlaskForm):
    for i in dbcolumns(dbfile,tabelabebidas):
        i = StringField(f"{i}")





@app.route('/')
def home():
    return render_template('menu.html')

@app.route('/bebidas', methods=['GET'])
def teste():
    formtest = FormBebidas()
    colunas = dbcolumns(dbfile, tabelabebidas)
    return render_template('formbebidas.html', formtest=formtest, colunas=colunas)

@app.route('/bebidas', methods=['POST'])
def bebidasreg():
    colunas = dbcolumns(dbfile, tabelabebidas)
    connection = sqlite3.connect(dbfile)
    cursor = connection.cursor()
    query2 = f"INSERT INTO {tabelabebidas} VALUES ("
    for c in colunas:
        c = request.form[f'{c}']
        query2 = query2 + f"'{c}', "
    query2 = query2[:-2]+")"
    cursor.execute(query2)
    connection.commit()
    return redirect('/teste')

@app.route('/prev')
def prev():
    connection = sqlite3.connect('registros.db')
    cursor = connection.cursor()
    dados = cursor.execute("SELECT * FROM registros")
    dados = cursor.fetchall()
    categorias = []
    for i in dados:
        if i[3] in categorias:
            pass
        else:
            categorias.append(i[3])
    teste = "<h1>PEDRO</h1>"
    return render_template('prev.html', dados=dados, categorias=categorias)

@app.route('/winelist')
def winelist():
    def select(cols=None, conds=None, dis=False, order=False, **vals):
        fststm = "SELECT * FROM bebidas"
        if cols is not None:
            x = ", ".join(cols) if len(cols) > 1 else cols[0]
            fststm = ''.join(("SELECT ", x, " FROM bebidas"))
        if conds is not None:
            w = ''
            for n in range(len(conds)): w += (conds[n] + ("='") + vals['vals'][n] + ("' and "))
            w = w[:-5]
            frase = ''.join((fststm, " WHERE ", w))
        else:
            frase = fststm
        if dis == True:
            frase = frase[:7] + "DISTINCT " + frase[7:]
        if order == True:
            frase = frase + ' ORDER by ' + cols[0]
        conn = sqlite3.connect('registros.db')
        c = conn.cursor()
        c.execute(frase)
        temp = {}
        resultado = []
        for a in c.fetchall():
            for b, c in enumerate(a):
                temp[cols[b]] = c
            resultado.append(temp.copy())
        return resultado
    return render_template('winelist.html', select=select)



@app.route('/form', methods=["GET"])
def form():
    connection = sqlite3.connect('registros.db')
    cursor = connection.cursor()
    dados = cursor.execute("SELECT * FROM registros")
    dados = cursor.fetchall()
    return render_template('form.html', dados = dados)


@app.route('/form', methods=["POST"])
def register():
    connection = sqlite3.connect('registros.db')
    cursor = connection.cursor()
    prod = request.form['produto']
    descr = request.form['desc']
    preco = request.form['preco']
    cat = request.form['cat']
    query1 = f"INSERT INTO registros VALUES ('{prod}', '{descr}', '{preco}', '{cat}')"
    cursor.execute(query1)
    connection.commit()
    return redirect('/form')


app.run(port=5200, debug=True)
