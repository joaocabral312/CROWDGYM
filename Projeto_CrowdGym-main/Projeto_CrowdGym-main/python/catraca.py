import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

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
        except Error as e:
            print(f"Erro ao inserir aluno: {e}")
        finally:
            fechar_conexao(conexao, cursor)

# Função para buscar um aluno no banco de dados pelo CPF
def buscar_aluno(cpf):
    conexao, cursor = conectar_banco()
    if conexao:
        try:
            query = "SELECT * FROM alunos WHERE cpf = %s"
            cursor.execute(query, (cpf,))
            aluno = cursor.fetchone()
            return aluno
        except Error as e:
            print(f"Erro ao buscar aluno: {e}")
        finally:
            fechar_conexao(conexao, cursor)
    return None

# Função para atualizar a presença do aluno no banco de dados
def atualizar_presenca(cpf, presenca):
    conexao, cursor = conectar_banco()
    if conexao:
        try:
            query = "UPDATE alunos SET presenca = %s WHERE cpf = %s"
            cursor.execute(query, (presenca, cpf))
            conexao.commit()
        except Error as e:
            print(f"Erro ao atualizar presença: {e}")
        finally:
            fechar_conexao(conexao, cursor)

# Função para registrar o histórico no banco de dados
def registrar_historico(cpf, nome, acao):
    conexao, cursor = conectar_banco()
    if conexao:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query = "INSERT INTO historico (cpf, nome, acao, timestamp) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (cpf, nome, acao, timestamp))
            conexao.commit()
        except Error as e:
            print(f"Erro ao registrar histórico: {e}")
        finally:
            fechar_conexao(conexao, cursor)

# Função para validar o CPF (apenas checagem simples para esta versão)
def validar_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

# Função para simular a entrada de um aluno
def entrada_aluno():
    global total_alunos
    cpf = entrada_cpf.get()

    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido. Verifique o formato.")
        return

    aluno = buscar_aluno(cpf)
    
    if aluno:
        nome, status, presenca = aluno[1], aluno[2], aluno[3]
        
        if status == "Ativo":
            if presenca == 0:
                total_alunos += 1
                atualizar_presenca(cpf, 1)
                atualizar_tela(f"{nome} entrou.", total_alunos)
                registrar_historico(cpf, nome, "entrou")
            else:
                atualizar_tela(f"{nome} já está dentro.", total_alunos)
        else:
            atualizar_tela(f"{nome} não pode entrar (matrícula inativa).", total_alunos)
    else:
        messagebox.showerror("Erro", "CPF não encontrado.")

# Função para simular a saída de um aluno
def saida_aluno():
    global total_alunos
    cpf = entrada_cpf.get()

    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido. Verifique o formato.")
        return

    aluno = buscar_aluno(cpf)
    
    if aluno:
        nome, status, presenca = aluno[1], aluno[2], aluno[3]
        
        if presenca == 1:
            total_alunos -= 1
            atualizar_presenca(cpf, 0)
            atualizar_tela(f"{nome} saiu.", total_alunos)
            registrar_historico(cpf, nome, "saiu")
        else:
            atualizar_tela(f"{nome} não está dentro.", total_alunos)
    else:
        messagebox.showerror("Erro", "CPF não encontrado.")

# Função para exibir na tela a contagem e status
def atualizar_tela(mensagem, total_alunos):
    label_mensagem.config(text=mensagem)
    label_contagem.config(text=f"Total de alunos dentro: {total_alunos}")

# Variáveis globais
total_alunos = 0

# Interface gráfica
root = tk.Tk()
root.title("Sistema de Controle de Catraca")

# Label para mostrar a contagem de alunos
label_contagem = tk.Label(root, text="Total de alunos dentro: 0", font=("Helvetica", 18))
label_contagem.pack(pady=10)

# Label para mostrar mensagens
label_mensagem = tk.Label(root, text="", font=("Helvetica", 18))
label_mensagem.pack(pady=10)

# Campo de entrada para CPF (para entradas e saídas)
label_cpf = tk.Label(root, text="Digite o CPF para entrada/saída:", font=("Helvetica", 16))
label_cpf.pack(pady=10)

entrada_cpf = tk.Entry(root, font=("Helvetica", 16))
entrada_cpf.pack(pady=10)

# Botão para simular a entrada de um aluno
botao_entrada = tk.Button(root, text="Entrada", command=entrada_aluno, font=("Helvetica", 16))
botao_entrada.pack(pady=10)

# Botão para simular a saída de um aluno
botao_saida = tk.Button(root, text="Saída", command=saida_aluno, font=("Helvetica", 16))
botao_saida.pack(pady=10)


root.mainloop()

