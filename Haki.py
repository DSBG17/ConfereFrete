from calculos.calculadora import*
from servicos.varreduranf import*
from servicos.varreduracte import*
from servicos.atualizarcte import*
from servicos.atualizarnf import*
from servicos.extratoCte import *

from tkinter import *
from PIL import Image, ImageTk

# Configuração da Janela
janela = Tk()
janela.geometry('400x350')

# Tirar o botão de maximizar
janela.resizable(False, False)

# Imagem de fundo
imagem = Image.open('imagens/fator.png')
imagem = imagem.resize((400, 350), Image.Resampling.LANCZOS)
bg_img = ImageTk.PhotoImage(imagem)

bg_label = Label(janela, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#Criar espaçamento

janela.title('Haki')

# Função para centralizar os botões com grid
def configurar_botao(botao, linha):
    botao.grid(row=linha, column=0, padx=10, pady=10, sticky="n")

# Botões
verificarcte = Button(janela, text="Verificar Cte", width=20, height=2, command=varreduracte)
verificarnf = Button(janela, text="Verificar NFs", width=20, height=2, command=varreduranf)
calcular = Button(janela, text="Calcular frete", width=20, height=2, command=calculos)
relatoriobd = Button(janela, text="Extrato calculos", width=20, height=2, command=relatorio)

# Configurar a grid
for i, botao in enumerate([verificarcte, verificarnf, calcular,  relatoriobd]):
    configurar_botao(botao, i)

# Centralizar a grid
janela.grid_columnconfigure(0, weight=1)

janela.mainloop()
