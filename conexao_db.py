import sqlite3
import os
from datetime import datetime
import traceback

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database:
    def __init__(self, db_name="dalvan.db"):
        self.db_path = db_name
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = dict_factory
            self.cursor = self.conn.cursor()
            
            self.criar_tabelas()
            self.criar_tabela_memoria()
            
            print(f"[BANCO] Conectado com sucesso: {os.path.abspath(self.db_path)}")
        except Exception:
            print("[BANCO - ERRO INICIALIZAÇÃO]")
            traceback.print_exc()

    def criar_tabelas(self):
        try:
            # tabelas já existentes
            self.cursor.execute('CREATE TABLE IF NOT EXISTS configuracoes (chave_nome TEXT PRIMARY KEY, valor TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS empresas (id INTEGER PRIMARY KEY AUTOINCREMENT, razao_social TEXT, endereco TEXT, cnpj TEXT, fone TEXT, zap TEXT, local_pagamento TEXT, texto_carne TEXT, texto_os TEXT, logo_path TEXT, data_cadastro TEXT)')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                unidade TEXT,
                referencia TEXT,
                grade TEXT,
                descricao TEXT NOT NULL,
                preco_compra REAL DEFAULT 0.00,
                preco_venda REAL DEFAULT 0.00,
                preco_avista REAL DEFAULT 0.00,
                lucro REAL DEFAULT 0.00,
                margem REAL DEFAULT 0.00,
                grupo TEXT,
                subgrupo TEXT,
                fornecedor TEXT,
                marca TEXT,
                localizacao TEXT,
                validade TEXT,
                data_ultima_compra TEXT,
                observacoes TEXT,
                foto TEXT,
                desativar INTEGER DEFAULT 0,
                estoque REAL DEFAULT 0.00,
                data_cadastro TEXT
            )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                bloqueado INTEGER DEFAULT 0,
                perfil TEXT DEFAULT 'comum',
                ativo INTEGER DEFAULT 1,
                criado_em TEXT,
                data_cadastro TEXT
            )''')

            # novas tabelas para custo e produção
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS materia_prima (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                quantidade_rolos INTEGER,
                metros_totais REAL,
                custo_total REAL,
                data_cadastro TEXT
            )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS producao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_materia_prima INTEGER,
                produto TEXT NOT NULL,
                quantidade_produzida INTEGER,
                consumo_unitario REAL,
                custo_unitario REAL,
                custos_extras REAL,
                custo_final_unitario REAL,
                margem REAL,
                preco_sugerido REAL,
                data_producao TEXT,
                FOREIGN KEY (id_materia_prima) REFERENCES materia_prima(id)
            )''')

            self.conn.commit()
            print("[BANCO] Tabelas verificadas e criadas.")
        except Exception:
            print("[BANCO - ERRO CRÍTICO NA CRIAÇÃO DE TABELAS]:")
            traceback.print_exc()

    def criar_tabela_memoria(self):
        try:
            self.cursor.execute('CREATE TABLE IF NOT EXISTS memoria_aprendizado (id INTEGER PRIMARY KEY AUTOINCREMENT, comando TEXT NOT NULL UNIQUE, resposta TEXT NOT NULL, data_criacao TEXT)')
            self.conn.commit()
        except Exception:
            traceback.print_exc()

    def fechar(self):
        if self.conn:
            self.conn.close()
