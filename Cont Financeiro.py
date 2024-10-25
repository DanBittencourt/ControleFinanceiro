import datetime
import tkinter as tk
from tkinter import messagebox
import pickle

# Classe para representar uma transação financeira
class Transacao:
    def __init__(self, data, descricao, valor, tipo):
        self.data = data
        self.descricao = descricao
        self.valor = valor
        self.tipo = tipo

# Variáveis globais
transacoes = []
saldo_label = None
lista_transacoes = None
descricao_entry = None
valor_entry = None
periodo_inicio_entry = None
periodo_fim_entry = None

# Função para adicionar uma nova transação
def adicionar_transacao():
    global descricao_entry, valor_entry

    descricao = descricao_entry.get()
    valor = float(valor_entry.get())
    tipo = tipo_var.get()

    if descricao and valor:
        data = datetime.datetime.now()
        transacao = Transacao(data, descricao, valor, tipo)
        transacoes.append(transacao)
        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
        atualizar_lista_transacoes()
        atualizar_saldo()
        descricao_entry.delete(0, tk.END)
        valor_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos.")

# Função para exibir as transações
def atualizar_lista_transacoes():
    global lista_transacoes

    lista_transacoes.delete(0, tk.END)
    for transacao in transacoes:
        item = f"{transacao.data.strftime('%d/%m/%Y %H:%M:%S')} - {transacao.descricao}: R${transacao.valor:.2f} ({transacao.tipo})"
        lista_transacoes.insert(tk.END, item)

# Função para calcular o saldo
def atualizar_saldo():
    global saldo_label

    saldo = 0
    for transacao in transacoes:
        if transacao.tipo == 'receita':
            saldo += transacao.valor
        elif transacao.tipo == 'despesa':
            saldo -= transacao.valor
    saldo_label.config(text=f"Saldo atual: R${saldo:.2f}")

# Função para gerar o relatório com base no período especificado
def gerar_relatorio():
    global periodo_inicio_entry, periodo_fim_entry

    periodo_inicio = datetime.datetime.strptime(periodo_inicio_entry.get(), "%d/%m/%Y")
    periodo_fim = datetime.datetime.strptime(periodo_fim_entry.get(), "%d/%m/%Y")

    relatorio = []
    for transacao in transacoes:
        if periodo_inicio <= transacao.data <= periodo_fim:
            item = f"{transacao.data.strftime('%d/%m/%Y %H:%M:%S')} - {transacao.descricao}: R${transacao.valor:.2f} ({transacao.tipo})"
            relatorio.append(item)

    messagebox.showinfo("Relatório", "\n".join(relatorio))

# Função para salvar as transações em um arquivo
def salvar_transacoes():
    with open("transacoes.pkl", "wb") as file:
        pickle.dump(transacoes, file)
    messagebox.showinfo("Sucesso", "As transações foram salvas!")

# Função para carregar as transações de um arquivo
def carregar_transacoes():
    global transacoes

    try:
        with open("transacoes.pkl", "rb") as file:
            transacoes = pickle.load(file)
        atualizar_lista_transacoes()
        atualizar_saldo()
        messagebox.showinfo("Sucesso", "As transações foram carregadas!")
    except FileNotFoundError:
        messagebox.showwarning("Erro", "O arquivo de transações não foi encontrado.")

# Função principal
def main():
    global saldo_label, lista_transacoes, descricao_entry, valor_entry, periodo_inicio_entry, periodo_fim_entry

    root = tk.Tk()
    root.title("Controle Financeiro")
    root.geometry("500x500")

    # Frame para adicionar transações
    adicionar_frame = tk.LabelFrame(root, text="Adicionar Transação")
    adicionar_frame.pack(padx=10, pady=10)

    descricao_label = tk.Label(adicionar_frame, text="Descrição:")
    descricao_label.grid(row=0, column=0, sticky=tk.W)
    descricao_entry = tk.Entry(adicionar_frame, width=30)
    descricao_entry.grid(row=0, column=1, padx=5, pady=5)

    valor_label = tk.Label(adicionar_frame, text="Valor:")
    valor_label.grid(row=1, column=0, sticky=tk.W)
    valor_entry = tk.Entry(adicionar_frame, width=10)
    valor_entry.grid(row=1, column=1, padx=5, pady=5)

    tipo_label = tk.Label(adicionar_frame, text="Tipo:")
    tipo_label.grid(row=2, column=0, sticky=tk.W)
    global tipo_var
    tipo_var = tk.StringVar()
    tipo_receita = tk.Radiobutton(adicionar_frame, text="Receita", variable=tipo_var, value="receita")
    tipo_receita.grid(row=2, column=1, sticky=tk.W)
    tipo_despesa = tk.Radiobutton(adicionar_frame, text="Despesa", variable=tipo_var, value="despesa")
    tipo_despesa.grid(row=2, column=1, sticky=tk.E)

    adicionar_button = tk.Button(adicionar_frame, text="Adicionar", command=adicionar_transacao)
    adicionar_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Frame para exibir transações
    transacoes_frame = tk.LabelFrame(root, text="Transações")
    transacoes_frame.pack(padx=10, pady=10)

    lista_transacoes = tk.Listbox(transacoes_frame, width=50)
    lista_transacoes.pack()

    # Frame para gerar o relatório
    relatorio_frame = tk.LabelFrame(root, text="Relatório")
    relatorio_frame.pack(padx=10, pady=10)

    periodo_inicio_label = tk.Label(relatorio_frame, text="Período de início (dd/mm/yyyy):")
    periodo_inicio_label.grid(row=0, column=0, sticky=tk.W)
    periodo_inicio_entry = tk.Entry(relatorio_frame, width=12)
    periodo_inicio_entry.grid(row=0, column=1, padx=5, pady=5)

    periodo_fim_label = tk.Label(relatorio_frame, text="Período de fim (dd/mm/yyyy):")
    periodo_fim_label.grid(row=1, column=0, sticky=tk.W)
    periodo_fim_entry = tk.Entry(relatorio_frame, width=12)
    periodo_fim_entry.grid(row=1, column=1, padx=5, pady=5)

    relatorio_button = tk.Button(relatorio_frame, text="Gerar Relatório", command=gerar_relatorio)
    relatorio_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Frame para exibir o saldo
    saldo_frame = tk.Frame(root)
    saldo_frame.pack(padx=10, pady=10)

    saldo_label = tk.Label(saldo_frame, text="Saldo atual: R$0.00")
    saldo_label.pack()

    # Frame para salvar e carregar as transações
    salvar_carregar_frame = tk.Frame(root)
    salvar_carregar_frame.pack(padx=10, pady=10)

    salvar_button = tk.Button(salvar_carregar_frame, text="Salvar Transações", command=salvar_transacoes)
    salvar_button.grid(row=0, column=0, padx=5, pady=5)

    carregar_button = tk.Button(salvar_carregar_frame, text="Carregar Transações", command=carregar_transacoes)
    carregar_button.grid(row=0, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
