import tkinter as tk
from tkinter import messagebox, simpledialog
import statistics
import datetime

avaliacoes = []

# Funções estatísticas e KPIs
def gerar_estatisticas():
    notas = [a['nota'] for a in avaliacoes]
    if not notas:
        return "Nenhuma avaliação registrada."

    try:
        media = statistics.mean(notas)
        mediana = statistics.median(notas)
        moda = statistics.mode(notas)
        stdev = statistics.stdev(notas) if len(notas) > 1 else 0
        variancia = statistics.variance(notas) if len(notas) > 1 else 0
    except statistics.StatisticsError:
        moda = "N/A"

    freq = {n: notas.count(n) for n in sorted(set(notas))}
    satisfeitos = [n for n in notas if n >= 7]
    percentual_satisfeitos = (len(satisfeitos) / len(notas)) * 100

    texto = f"""
    RELATÓRIO GERADO EM: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

    --- ESTATÍSTICAS ---
    Média: {media:.2f}
    Mediana: {mediana:.2f}
    Moda: {moda}
    Desvio Padrão: {stdev:.2f}
    Variância: {variancia:.2f}
    Frequência: {freq}

    --- KPIs ---
    Total de avaliações: {len(notas)}
    Clientes satisfeitos (nota ≥ 7): {len(satisfeitos)} ({percentual_satisfeitos:.1f}%)
    Nota mínima: {min(notas)}
    Nota máxima: {max(notas)}
    """
    return texto

def salvar_relatorio():
    texto = gerar_estatisticas()
    with open("relatorio.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    messagebox.showinfo("Relatório", "Relatório salvo em 'relatorio.txt'")

# Funções CRUD
def adicionar():
    nome = simpledialog.askstring("Cliente", "Nome do cliente:")
    if nome:
        try:
            nota = float(simpledialog.askstring("Nota", "Nota de 0 a 10:"))
            if 0 <= nota <= 10:
                avaliacoes.append({"cliente": nome, "nota": nota})
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "A nota deve estar entre 0 e 10.")
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida.")

def editar():
    idx = lista.curselection()
    if not idx:
        return
    index = idx[0]
    try:
        nova_nota = float(simpledialog.askstring("Editar Nota", "Nova nota de 0 a 10:"))
        if 0 <= nova_nota <= 10:
            avaliacoes[index]['nota'] = nova_nota
            atualizar_lista()
        else:
            messagebox.showerror("Erro", "A nota deve estar entre 0 e 10.")
    except ValueError:
        messagebox.showerror("Erro", "Nota inválida.")

def excluir():
    idx = lista.curselection()
    if not idx:
        return
    index = idx[0]
    avaliacoes.pop(index)
    atualizar_lista()

def atualizar_lista():
    lista.delete(0, tk.END)
    for a in avaliacoes:
        lista.insert(tk.END, f"{a['cliente']} - Nota: {a['nota']}")

def mostrar_estatisticas():
    texto = gerar_estatisticas()
    messagebox.showinfo("Estatísticas e KPIs", texto)

# Interface Gráfica
janela = tk.Tk()
janela.title("Sistema de Avaliações")
janela.geometry("500x400")

frame = tk.Frame(janela)
frame.pack(pady=10)

lista = tk.Listbox(frame, width=50)
lista.pack()

botoes_frame = tk.Frame(janela)
botoes_frame.pack(pady=10)

tk.Button(botoes_frame, text="Adicionar", width=10, command=adicionar).grid(row=0, column=0, padx=5)
tk.Button(botoes_frame, text="Editar", width=10, command=editar).grid(row=0, column=1, padx=5)
tk.Button(botoes_frame, text="Excluir", width=10, command=excluir).grid(row=0, column=2, padx=5)
tk.Button(botoes_frame, text="Estatísticas", width=12, command=mostrar_estatisticas).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(botoes_frame, text="Salvar Relatório", width=15, command=salvar_relatorio).grid(row=1, column=2, pady=5)

atualizar_lista()
janela.mainloop()
