import sqlite3 as sql

def acessaDB(local, banco):
    con = sql.connect(local+banco)
    return con

def criaTabela(cursor, tabela):
    cursor.execute('CREATE TABLE IF NOT EXISTS '+tabela+''' (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    acertos INTEGER NOT NULL,
    erros INTEGER NOT NULL,
    total INTEGER NOT NULL
    );
    ''')


def verificaJogador(cursor, jogador, tabela):
    usuario = cursor.execute('SELECT nome FROM '+tabela+''' 
    WHERE nome=:nome''', {"nome": jogador}
    )
    return usuario


def adicionaJogador(cursor, jogador, tabela):
    cursor.execute('INSERT INTO '+tabela+' (nome, acertos, erros, total) VALUES(?, ?, ?, ?)',
                   (jogador[0], jogador[1], jogador[2], jogador[3]))


def obterJogador(cursor, jogador, tabela):
    usuario = cursor.execute('SELECT * FROM ' + tabela + ''' 
        WHERE nome=:nome''', {"nome": jogador}
                             )
    return usuario


def atualizaJogador(cursor, jogador, tabela):
    cursor.execute('UPDATE '+tabela+''' 
    SET acertos = ?, erros = ?, total = ? WHERE nome = ?
    ''', (jogador[1], jogador[2], jogador[3], jogador[0])
    )