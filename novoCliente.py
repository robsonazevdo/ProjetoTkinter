from tkinter import*
import os
import Banco as dados



def criar_cliente(n,t):
    print(n,t) 
            
            
app = Tk()

app.title("Cadastrar Cliente")
x = app.winfo_screenwidth() // 4
y = int(app.winfo_screenheight() * 0.2)
app.geometry('600x400+' + str(x) + '+' + str(y) )
app.configure(background="#b4918f")


Label(
        app,
        text="Nome cliente",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 12),
        ).pack(pady=(20, 0))
        
nome_cliente = Entry(app, width=65, font=('TkMenuFont', 10))
nome_cliente.pack(pady=(20, 0))
nome =nome_cliente.get()

 
Label(
app,
text="Telefone",
bg="#b4918f",
fg="white",
font=('TkMenuFont', 12),
).pack(pady=(40, 0))
        
Telefone = Entry(app, width=65, font=('TkMenuFont', 10))
Telefone.pack(pady=(20, 0))
tel = Telefone.get()

Button(
app,
text=("Cadastrar"),
font=('TkMenuFont', 15),
bg="#28393a",
fg="white",
cursor="hand2",
activebackground="#badee2",
activeforeground="black",
bd = 5,
command=lambda:  criar_cliente(nome, tel)).pack(pady=(8, 0))




app.mainloop()
