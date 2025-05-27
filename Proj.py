import tkinter as tk
from tkinter import messagebox, simpledialog
import statistics
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

materias = {}

materia_selecionada = None

def adicionar_materia():
    global materia_selecionada
    nome = simpledialog.askstring("Adicionar Matéria", "Nome da matéria:")
    if nome:
        if nome in materias:
            messagebox.showerror("Erro", "Matéria já existe.")
        else:
            materias[nome] = []
            materia_selecionada = nome
            atualizar_lista_materias()
            atualizar_lista_alunos()

def editar_materia():
    global materia_selecionada
    if not materia_selecionada:
        return
    novo_nome = simpledialog.askstring("Editar Matéria", "Novo nome da matéria:", initialvalue=materia_selecionada)
    if novo_nome and novo_nome != materia_selecionada:
        materias[novo_nome] = materias.pop(materia_selecionada)
        materia_selecionada = novo_nome
        atualizar_lista_materias()
        atualizar_lista_alunos()

def excluir_materia():
    global materia_selecionada
    if not materia_selecionada:
        return
    if messagebox.askyesno("Confirmar", f"Excluir matéria '{materia_selecionada}'?"):
        materias.pop(materia_selecionada)
        materia_selecionada = None
        atualizar_lista_materias()
        atualizar_lista_alunos()

def selecionar_materia(evt):
    global materia_selecionada
    sel = lista_materias.curselection()
    if sel:
        materia_selecionada = lista_materias.get(sel[0])
        atualizar_lista_alunos()

# CRUD alunos e notas
def adicionar_aluno():
    if not materia_selecionada:
        messagebox.showerror("Erro", "Selecione uma matéria.")
        return
    nome = simpledialog.askstring("Aluno", "Nome do aluno:")
    if nome:
        try:
            nota = float(simpledialog.askstring("Nota", "Nota de 0 a 10:"))
            if 0 <= nota <= 10:
                materias[materia_selecionada].append({"aluno": nome, "nota": nota})
                atualizar_lista_alunos()
            else:
                messagebox.showerror("Erro", "A nota deve estar entre 0 e 10.")
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida.")

def editar_aluno():
    if not materia_selecionada:
        return
    idx = lista_alunos.curselection()
    if not idx:
        return
    index = idx[0]
    try:
        nova_nota = float(simpledialog.askstring("Editar Nota", "Nova nota de 0 a 10:"))
        if 0 <= nova_nota <= 10:
            materias[materia_selecionada][index]['nota'] = nova_nota
            atualizar_lista_alunos()
        else:
            messagebox.showerror("Erro", "A nota deve estar entre 0 e 10.")
    except ValueError:
        messagebox.showerror("Erro", "Nota inválida.")

def excluir_aluno():
    if not materia_selecionada:
        return
    idx = lista_alunos.curselection()
    if not idx:
        return
    index = idx[0]
    materias[materia_selecionada].pop(index)
    atualizar_lista_alunos()

def gerar_estatisticas():
    if not materias:
        return "Nenhuma matéria registrada."

    texto = f"RELATÓRIO GERADO EM: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    for mat, avaliacoes in materias.items():
        notas = [a['nota'] for a in avaliacoes]
        if not notas:
            continue
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

        texto += f"""
\n--- MATÉRIA: {mat} ---
Alunos:
"""
        for a in avaliacoes:
            texto += f"- {a['aluno']} (Nota: {a['nota']})\n"

        texto += f"""
Estatísticas:
Média: {media:.2f}, Mediana: {mediana:.2f}, Moda: {moda}, Desvio Padrão: {stdev:.2f}, Variância: {variancia:.2f}
Total de avaliações: {len(notas)}, Clientes satisfeitos (nota ≥ 7): {len(satisfeitos)} ({percentual_satisfeitos:.1f}%)
Nota mínima: {min(notas)}, Nota máxima: {max(notas)}
"""
    return texto

def salvar_relatorio():
    texto = gerar_estatisticas()
    with open("relatorio.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    messagebox.showinfo("Relatório", "Relatório salvo em 'relatorio.txt'")

def mostrar_estatisticas():
    texto = gerar_estatisticas()
    messagebox.showinfo("Estatísticas e KPIs", texto)

def mostrar_grafico():
    if not materia_selecionada:
        return
    avaliacoes = materias[materia_selecionada]
    if not avaliacoes:
        return
    notas = [a['nota'] for a in avaliacoes]
    freq = {n: notas.count(n) for n in sorted(set(notas))}

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(freq.keys(), freq.values(), color='skyblue')
    ax.set_title(f"Frequência das Notas - {materia_selecionada}")
    ax.set_xlabel("Nota")
    ax.set_ylabel("Frequência")
    ax.set_xticks(list(freq.keys()))

    grafico_win = tk.Toplevel(janela)
    grafico_win.title("Gráfico de Frequência")
    canvas = FigureCanvasTkAgg(fig, master=grafico_win)
    canvas.draw()
    canvas.get_tk_widget().pack()

def mostrar_grafico_comparativo():
    if not materias:
        messagebox.showinfo("Aviso", "Nenhuma matéria cadastrada.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    materias_nomes = list(materias.keys())
    largura = 0.35
    posicoes = list(range(len(materias_nomes)))

    for i, mat in enumerate(materias_nomes):
        alunos = materias[mat]
        notas = [a['nota'] for a in alunos]
        nomes = [a['aluno'] for a in alunos]

        if notas:
            media = statistics.mean(notas)
            ax.bar([i - largura/2], [media], width=largura, label=f"Média - {mat}", color='gray')
            for j, nota in enumerate(notas):
                ax.bar([i + (j+1)*largura/(len(notas)+1)], [nota], width=largura/(len(notas)+1), label=nomes[j] if i == 0 else "")

    ax.set_xticks(posicoes)
    ax.set_xticklabels(materias_nomes)
    ax.set_ylabel("Nota")
    ax.set_title("Notas por Matéria e Médias")
    ax.legend()

    grafico_win = tk.Toplevel(janela)
    grafico_win.title("Gráfico Comparativo Geral")
    canvas = FigureCanvasTkAgg(fig, master=grafico_win)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Atualizações de interface
def atualizar_lista_materias():
    lista_materias.delete(0, tk.END)
    for m in materias:
        lista_materias.insert(tk.END, m)

def atualizar_lista_alunos():
    lista_alunos.delete(0, tk.END)
    if materia_selecionada:
        for a in materias[materia_selecionada]:
            lista_alunos.insert(tk.END, f"{a['aluno']} - Nota: {a['nota']}")

# GUI
janela = tk.Tk()
janela.title("Sistema de Avaliações por Matéria")
janela.geometry("800x550")

frame_materias = tk.Frame(janela)
frame_materias.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(frame_materias, text="Matérias").pack()
lista_materias = tk.Listbox(frame_materias, width=30)
lista_materias.pack()
lista_materias.bind('<<ListboxSelect>>', selecionar_materia)

botoes_materias = tk.Frame(frame_materias)
botoes_materias.pack(pady=5)

tk.Button(botoes_materias, text="Adicionar", command=adicionar_materia).grid(row=0, column=0, padx=2)
tk.Button(botoes_materias, text="Editar", command=editar_materia).grid(row=0, column=1, padx=2)
tk.Button(botoes_materias, text="Excluir", command=excluir_materia).grid(row=0, column=2, padx=2)

frame_alunos = tk.Frame(janela)
frame_alunos.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(frame_alunos, text="Alunos").pack()
lista_alunos = tk.Listbox(frame_alunos, width=50)
lista_alunos.pack()

botoes_alunos = tk.Frame(frame_alunos)
botoes_alunos.pack(pady=5)

tk.Button(botoes_alunos, text="Adicionar", command=adicionar_aluno).grid(row=0, column=0, padx=2)
tk.Button(botoes_alunos, text="Editar", command=editar_aluno).grid(row=0, column=1, padx=2)
tk.Button(botoes_alunos, text="Excluir", command=excluir_aluno).grid(row=0, column=2, padx=2)

botoes_gerais = tk.Frame(janela)
botoes_gerais.pack(pady=10)

tk.Button(botoes_gerais, text="Estatísticas", command=mostrar_estatisticas).grid(row=0, column=0, padx=5)
tk.Button(botoes_gerais, text="Salvar Relatório", command=salvar_relatorio).grid(row=0, column=1, padx=5)
tk.Button(botoes_gerais, text="Mostrar Gráfico", command=mostrar_grafico).grid(row=0, column=2, padx=5)
tk.Button(botoes_gerais, text="Gráfico Geral", command=mostrar_grafico_comparativo).grid(row=0, column=3, padx=5)

janela.mainloop()