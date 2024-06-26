from tkinter import *

placas = []
contador = 0
tempo_saida = 5

root = Tk()
root.title("Sensores Forno de placas")
root.resizable(width=False, height=False)

def adicionar_placa():
    global contador, botao_emperramento
    contador += 1
    placas.append({"numero": contador, "stuck": False})  # Adiciona um dicionário representando a nova placa à lista placas
    entrada(placas[-1])  # Chama a função entrada com a última placa adicionada
    botao_emperramento = Button(frame_registro, text=f"Emperrar Placa {contador}", command=lambda p=placas[-1]: simular_emperramento(p))  # Cria um botão para simular emperramento
    botao_emperramento.pack(pady=2)  # Mostra o botão na interface

def entrada(placa_info):
    placa_num = placa_info["numero"]
    texto_registro.insert(END, f"Placa {placa_num} entrou\n")  # Insere no registro que a placa entrou
    texto_registro.see(END)  # Garante que o registro esteja visível
    if placa_info["stuck"]:
        texto_registro.insert(END, f"Placa {placa_num} está emperrada e precisa de atenção!\n")  # Informa se a placa está emperrada
        texto_registro.see(END)
    else:
        root.after(int(entrada_temposaida.get()) * 1000, lambda: saida(placa_info))  # Programa a saída da placa após o tempo especificado

def saida(placa_info):
    placa_num = placa_info["numero"]
    if not placa_info["stuck"]:
        texto_registro.insert(END, f"Placa {placa_num} saiu\n")  # Informa que a placa saiu
        texto_registro.see(END)
    else:
        texto_registro.insert(END, f"Placa {placa_num} não foi detectada como saída após o tempo de espera!\n")  # Informa se a placa emperrada não saiu
        texto_registro.see(END)

def simular_emperramento(placa_info):
    global botao_emperramento
    placa_info["stuck"] = True  # Simula que a placa está emperrada
    placa_num = placa_info["numero"]
    texto_registro.see(END)
    botao_emperramento = Button(frame_registro, text=f"Placa {placa_num} Emperrada", state=DISABLED)  # Cria um botão desativado para a placa emperrada
    botao_emperramento.pack_forget()  # Remove o botão após algum tempo
    root.after(int(entrada_temposaida.get()) * 1000, lambda: esconder_botao(botao_emperramento))  # Programa a remoção do botão após o tempo especificado

def esconder_botao(botao):
    botao.pack_forget()  # Remove o botão da interface

def limpar_lista():
    global placas, contador
    placas.clear()  # Limpa a lista de placas
    contador = 0  # Reinicia o contador de placas
    texto_registro.delete(1.0, END)  # Limpa o texto do registro
    texto_registro.insert(END, "Lista de placas limpa!\n")  # Informa que a lista de placas foi limpa
    texto_registro.see(END)  # Garante que a mensagem de limpeza esteja visível
    for widget in frame_registro.winfo_children():
        widget.pack_forget()  # Remove todos os widgets do frame de registro

frame_controles = Frame(root)
frame_controles.pack(padx=10, pady=10)

Button(frame_controles, text="Adicionar Placa", command=adicionar_placa).grid(row=0, column=0, padx=5, pady=5)
Button(frame_controles, text="Limpar Lista", command=limpar_lista).grid(row=0, column=1, padx=5, pady=5)

Label(frame_controles, text="Tempo de saída (s):").grid(row=0, column=2, padx=5, pady=5)

entrada_temposaida = Entry(frame_controles)
entrada_temposaida.grid(row=0, column=3, padx=5, pady=5)
entrada_temposaida.insert(END, str(tempo_saida))

frame_registro = Frame(root)
frame_registro.pack(padx=10, pady=10)

frame_list = Frame(root)
frame_list.pack(padx=10, pady=10)

Label(frame_list, text="Registro de Movimentos:").pack()

scrollbar = Scrollbar(frame_list)
scrollbar.pack(side=RIGHT, fill=Y)

texto_registro = Text(frame_list, height=10, width=60, yscrollcommand=scrollbar.set)
texto_registro.pack()

scrollbar.config(command=texto_registro.yview)

root.mainloop()