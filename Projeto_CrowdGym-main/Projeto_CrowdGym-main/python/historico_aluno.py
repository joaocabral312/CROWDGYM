import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox

# Função para validar CPF com verificação de dígitos verificadores
def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    
    # Cálculo dos dígitos verificadores
    def calc_digito(cpf, pos):
        return sum([int(cpf[i]) * (pos - i) for i in range(pos - 1)]) * 10 % 11 % 10
    
    return calc_digito(cpf, 10) == int(cpf[9]) and calc_digito(cpf, 11) == int(cpf[10])

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
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        messagebox.showerror("Erro", f"Erro ao conectar ao MySQL: {e}")
        return None

# Função para encerrar a conexão
def fechar_conexao(conexao):
    if conexao.is_connected():
        conexao.close()

# Função para buscar o histórico de um aluno específico
def buscar_historico(cpf):
    conexao = conectar_banco()
    if conexao:
        try:
            with conexao.cursor() as cursor:  # Gerenciamento de contexto para o cursor
                query = "SELECT * FROM historico WHERE cpf = %s"
                cursor.execute(query, (cpf,))
                registros = cursor.fetchall()
                return registros
        except Error as e:
            print(f"Erro ao buscar histórico: {e}")
            messagebox.showerror("Erro", f"Erro ao buscar histórico: {e}")
        finally:
            fechar_conexao(conexao)
    return None

# Função para buscar todo o histórico
def buscar_historico_completo():
    conexao = conectar_banco()
    if conexao:
        try:
            with conexao.cursor() as cursor:  # Gerenciamento de contexto para o cursor
                query = "SELECT * FROM historico"
                cursor.execute(query)
                registros = cursor.fetchall()
                return registros
        except Error as e:
            print(f"Erro ao buscar histórico completo: {e}")
            messagebox.showerror("Erro", f"Erro ao buscar histórico completo: {e}")
        finally:
            fechar_conexao(conexao)
    return None

# Função para exibir o histórico de um aluno específico
def exibir_historico_aluno():
    cpf_pesquisa = entrada_cpf.get()

    if not validar_cpf(cpf_pesquisa):
        messagebox.showerror("Erro", "CPF inválido. Verifique o formato.")
        return

    registros = buscar_historico(cpf_pesquisa)
    if registros:
        registros_str = "\n".join([f"{registro[3]} - {registro[2]}" for registro in registros])
        messagebox.showinfo("Histórico de Aluno", registros_str)
    else:
        messagebox.showinfo("Histórico de Aluno", "Nenhum registro encontrado para este CPF.")

# Função para exibir todo o histórico
def exibir_historico_completo():
    registros = buscar_historico_completo()
    if registros:
        registros_str = "\n".join([f"{registro[3]} - {registro[2]}" for registro in registros])
        messagebox.showinfo("Histórico Completo", registros_str)
    else:
        messagebox.showinfo("Histórico Completo", "Nenhum registro encontrado.")

# Interface gráfica para o histórico
root = tk.Tk()
root.title("Sistema de Histórico de Alunos")

# Campo de entrada para CPF de pesquisa
label_cpf = tk.Label(root, text="Digite o CPF para pesquisar histórico:", font=("Helvetica", 14))
label_cpf.pack(pady=10)

entrada_cpf = tk.Entry(root, font=("Helvetica", 14))
entrada_cpf.pack(pady=10)

# Botão para pesquisar o histórico de um aluno
botao_pesquisar = tk.Button(root, text="Pesquisar Histórico de Aluno", command=exibir_historico_aluno, font=("Helvetica", 14))
botao_pesquisar.pack(pady=10)

# Botão para exibir todo o histórico
botao_exibir_completo = tk.Button(root, text="Exibir Histórico Completo", command=exibir_historico_completo, font=("Helvetica", 14))
botao_exibir_completo.pack(pady=10)

root.mainloop()

