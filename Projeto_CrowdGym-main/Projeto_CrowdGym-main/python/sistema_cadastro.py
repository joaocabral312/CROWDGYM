import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost', # Endereço do servidor MySQL  
            user='root', # Usuário do MySQL  
            password='', # Senha do MySQL 
            database='academia' # Nome do banco de dados
        )
        if conexao.is_connected():
            cursor = conexao.cursor()
            return conexao, cursor
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None, None

# Função para encerrar a conexão
def fechar_conexao(conexao, cursor):
    if conexao.is_connected():
        cursor.close()
        conexao.close()

# Função para inserir alunos no banco de dados
def inserir_aluno(cpf, nome, status):
    conexao, cursor = conectar_banco()
    if conexao:
        try:
            query = "INSERT INTO alunos (cpf, nome, status) VALUES (%s, %s, %s)"
            cursor.execute(query, (cpf, nome, status))
            conexao.commit()
            messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado com sucesso!")
        except Error as e:
            print(f"Erro ao inserir aluno: {e}")
            messagebox.showerror("Erro", f"Erro ao cadastrar aluno: {e}")
        finally:
            fechar_conexao(conexao, cursor)

# Função para validar o CPF
def validar_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

# Função para processar o cadastro de um novo aluno
def cadastrar_aluno():
    nome = entrada_nome.get()
    cpf = entrada_cpf.get()
    status = var_status.get()

    if not nome or not cpf:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido. Deve conter 11 dígitos.")
        return

    inserir_aluno(cpf, nome, status)

# Interface gráfica para cadastro de alunos
root = tk.Tk()
root.title("Sistema de Cadastro de Alunos")

# Labels e campos de entrada
label_nome = tk.Label(root, text="Nome do Aluno:", font=("Helvetica", 14))
label_nome.pack(pady=10)

entrada_nome = tk.Entry(root, font=("Helvetica", 14))
entrada_nome.pack(pady=10)

label_cpf = tk.Label(root, text="CPF do Aluno (11 dígitos):", font=("Helvetica", 14))
label_cpf.pack(pady=10)

entrada_cpf = tk.Entry(root, font=("Helvetica", 14))
entrada_cpf.pack(pady=10)

# Menu para selecionar o status do aluno (Ativo/Inativo)
label_status = tk.Label(root, text="Status do Aluno:", font=("Helvetica", 14))
label_status.pack(pady=10)

var_status = tk.StringVar(value="Ativo")  # Valor padrão
menu_status = tk.OptionMenu(root, var_status, "Ativo", "Inativo")
menu_status.config(font=("Helvetica", 14))
menu_status.pack(pady=10)

# Botão para cadastrar aluno
botao_cadastrar = tk.Button(root, text="Cadastrar Aluno", command=cadastrar_aluno, font=("Helvetica", 14))
botao_cadastrar.pack(pady=20)

root.mainloop()
