import tkinter as tk
from tkinter import messagebox

# Função para verificar login e senha
def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    # Verificar se as credenciais estão corretas
    if usuario == "admin" and senha == "senha123":
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo ao sistema!")
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")

# Janela principal
janela = tk.Tk()
janela.title("Tela de Login")

# Configurar o layout
label_usuario = tk.Label(janela, text="Usuário:")
label_usuario.pack(pady=5)

entry_usuario = tk.Entry(janela, width=30)
entry_usuario.pack(pady=5)

label_senha = tk.Label(janela, text="Senha:")
label_senha.pack(pady=5)

entry_senha = tk.Entry(janela, width=30, show="*")  # A senha será mostrada como asteriscos
entry_senha.pack(pady=5)

# Botão para realizar o login
botao_login = tk.Button(janela, text="Login", command=verificar_login)
botao_login.pack(pady=20)

# Rodar a interface
janela.mainloop()
