import sqlite3
import pandas as pd


def dbcolumns(db, table):
    conn = sqlite3.connect(f'{db}')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = []
    for x in cursor.fetchall(): columns.append(x[1])
    return columns



def winetree():
    connw = sqlite3.connect('registros.db')
    connw.cursor()
    wine = pd.read_sql_query("SELECT * FROM bebidas", connw)
    lista = []
    estilos = wine.estilo.unique()
    estilos.sort()
    for e in estilos:
        estilo = wine.loc[wine['estilo'] == e]
        paises = estilo.pais.unique()
        paises.sort()
        for p in paises:
            pais = estilo.loc[estilo['pais'] == p]
            regioes = pais.regiao.unique()
            regioes.sort()
            for r in regioes:
                regiao = pais.loc[pais['regiao'] == r]
                lista.append(regiao)
    return lista, wine

class WineList:

    def __init__(self, estilo, pais, regiao, uva, preco):
        self.estilo = estilo
        self.pais = pais
        self.regiao = regiao
        self.uva = uva
        self.preco = preco





