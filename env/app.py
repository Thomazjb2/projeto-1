import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Configurações de tema
tema_claro = {
    "bg": "white",
    "fg": "black",
    "insertbackground": "black",
    "menu_bg": "lightgray",
    "menu_fg": "black"
}

tema_escuro = {
    "bg": "#1e1e1e",
    "fg": "white",
    "insertbackground": "white",
    "menu_bg": "#2e2e2e",
    "menu_fg": "white"
}

tema_atual = tema_claro
arquivo_salvo = ""
conteudo_original = ""

def aplicar_tema(tema):
    text_area.config(bg=tema["bg"], fg=tema["fg"], insertbackground=tema["insertbackground"])
    menu_bar.config(bg=tema["menu_bg"], fg=tema["menu_fg"])
    contador_label.config(bg=tema["bg"], fg=tema["fg"])
    preview_lateral.config(bg=tema["bg"], fg=tema["fg"])
    for menu in menu_bar.winfo_children():
        menu.config(bg=tema["menu_bg"], fg=tema["menu_fg"])

def atualizar_contador(event=None):
    texto = text_area.get(1.0, tk.END)
    palavras = len(texto.split())
    caracteres = len(texto) - 1
    contador_label.config(text=f"Palavras: {palavras} | Caracteres: {caracteres}")
    atualizar_preview()

def novo_arquivo(event=None):
    global arquivo_salvo, conteudo_original
    if verificar_alteracao():
        if not confirmar_perda():
            return
    text_area.delete(1.0, tk.END)
    arquivo_salvo = ""
    conteudo_original = ""

def abrir_arquivo(event=None):
    global arquivo_salvo, conteudo_original
    caminho = filedialog.askopenfilename(defaultextension=".txt",
                                          filetypes=[("Textos", "*.txt *.md *.html"), ("Todos os arquivos", "*.*")])
    if caminho:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, conteudo)
            arquivo_salvo = caminho
            conteudo_original = conteudo
        atualizar_contador()

def salvar_arquivo(event=None):
    global arquivo_salvo, conteudo_original
    if not arquivo_salvo:
        arquivo_salvo = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Textos", "*.txt *.md *.html"), ("Todos os arquivos", "*.*")])
    if arquivo_salvo:
        with open(arquivo_salvo, "w", encoding="utf-8") as arquivo:
            conteudo = text_area.get(1.0, tk.END)
            arquivo.write(conteudo)
            conteudo_original = conteudo
        messagebox.showinfo("Salvo", f"Arquivo salvo: {os.path.basename(arquivo_salvo)}")

def verificar_alteracao():
    texto_atual = text_area.get(1.0, tk.END)
    return texto_atual.strip() != conteudo_original.strip()

def confirmar_perda():
    return messagebox.askyesno("Alterações não salvas", "Você tem alterações não salvas. Deseja descartá-las?")

def ao_fechar():
    if verificar_alteracao():
        if not messagebox.askyesno("Sair sem salvar?", "Há alterações não salvas. Deseja sair mesmo assim?"):
            return
    janela.destroy()

def mudar_para_tema_claro():
    global tema_atual
    tema_atual = tema_claro
    aplicar_tema(tema_atual)

def mudar_para_tema_escuro():
    global tema_atual
    tema_atual = tema_escuro
    aplicar_tema(tema_atual)

def atualizar_preview():
    texto = text_area.get(1.0, tk.END)
    linhas = texto.strip().split("\n")
    preview = "\n".join(linhas[:20])  # Mostra até 20 linhas
    preview_lateral.delete(1.0, tk.END)
    preview_lateral.insert(tk.END, preview)

# Janela principal
janela = tk.Tk()
janela.title("Bloco de Notas PRO 📝")
janela.geometry("800x500")
janela.protocol("WM_DELETE_WINDOW", ao_fechar)

# Menu
menu_bar = tk.Menu(janela)
arquivo_menu = tk.Menu(menu_bar, tearoff=0)
arquivo_menu.add_command(label="Novo (Ctrl+N)", command=novo_arquivo)
arquivo_menu.add_command(label="Abrir (Ctrl+O)", command=abrir_arquivo)
arquivo_menu.add_command(label="Salvar (Ctrl+S)", command=salvar_arquivo)
arquivo_menu.add_separator()
arquivo_menu.add_command(label="Sair", command=ao_fechar)
menu_bar.add_cascade(label="Arquivo", menu=arquivo_menu)

tema_menu = tk.Menu(menu_bar, tearoff=0)
tema_menu.add_command(label="Tema Claro", command=mudar_para_tema_claro)
tema_menu.add_command(label="Tema Escuro", command=mudar_para_tema_escuro)
menu_bar.add_cascade(label="Tema", menu=tema_menu)

janela.config(menu=menu_bar)

# Frame principal
frame = tk.Frame(janela)
frame.pack(fill="both", expand=True)

# Área de texto principal
text_area = tk.Text(frame, font=("Arial", 12), wrap="word")
text_area.pack(side="left", fill="both", expand=True)
text_area.bind("<KeyRelease>", atualizar_contador)

# Preview lateral (mini mapa de conteúdo)
preview_lateral = tk.Text(frame, font=("Arial", 9), width=30, state="normal")
preview_lateral.pack(side="right", fill="y")
preview_lateral.insert(tk.END, "")
preview_lateral.config(state="disabled")

# Contador
contador_label = tk.Label(janela, text="Palavras: 0 | Caracteres: 0", anchor="w", padx=10)
contador_label.pack(fill="x")

# Atalhos
janela.bind("<Control-n>", novo_arquivo)
janela.bind("<Control-o>", abrir_arquivo)
janela.bind("<Control-s>", salvar_arquivo)

# Tema inicial
aplicar_tema(tema_atual)

janela.mainloop()
