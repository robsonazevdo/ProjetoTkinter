import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import os
from datetime import datetime, timedelta






pastaApp=os.path.dirname(__file__)


        
 
def load_frame2(email,password):
    
    
            
    def semComando():
        print('deu certo')
        
    def novoAtendimento():  
        def criar_atendimento():
            try :
                items = tv.selection()[0]
                id = tv.item(items,"value")
                desconto= desc.get()
                v = valor.get()
                vt = valorTotal.get()
                dataR = data.get()
                descricao= textArea.get("1.0",tk.END)
                formaPagamento = comboBox.get()
                print("id:",id,"valor Serviço:", v,"Desconto:",desconto, "Valor Total:",vt, "Data:",dataR, "Descrição:",descricao, formaPagamento)
                #dados.criar_atendimento(id,v,desconto, vt, id_forma_pagamento, descricao, dataR)
            except:
                messagebox.showerror("ERRO!", "Precisa Selecionar um Cliente")
                
                
        def inserir():
            if nome_cliente.get() == "" or fone.get() == "": 
               return messagebox.showinfo(title=False, message="Preencha todos os campos")
                
            ja_existe, c = dados.criar_cliente(nome_cliente.get(),fone.get())
            if ja_existe != False:
                nome_cliente.delete(0,tk.END)
                fone.delete(0,tk.END)
                return messagebox.showinfo(title=False, message="Cliente Já existe")
                
            else:
                messagebox.showinfo(title=False, message="Cadastro feito com sucesso")
                nome_cliente.delete(0,tk.END)
                fone.delete(0,tk.END)
                popular()
                return
        
        def popular():
            tv.delete(*tv.get_children())
            cliente = dados.db_listar_cliente()
        
            for c in cliente:
                tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
                
                
        def calc(e):
            a = float(valor.get()) + 2
            valorTotal.insert(0, a)
            
        def limitar_tamanho(P):
            if P == "": return True
            try:
                value = float(P)
            except ValueError:
                return False
            return 0 <= value <= 10000

                
        def pesquisaCliente():
            tv.delete(*tv.get_children())
            historico = dados.db_historico_cliente(pNome.get())
            pNome.delete(0,tk.END)
            for c in historico:
                tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
                
        
        
        app = tk.Toplevel()
        app.title("Novo Atendimento")
        x = app.winfo_screenwidth() // 4
        y = int(app.winfo_screenheight() * 0.1)
        app.geometry('700x500+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")
        
        vcmd = app.register(func=limitar_tamanho)
        
        quadroGrid = tk.LabelFrame(app, text="Clientes", background="#b4918f")
        quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
        
        tv = ttk.Treeview(quadroGrid, columns=("id","nome","fone"), show="headings",)
        tv.column("id",minwidth=0,width=50)
        tv.column("nome",minwidth=0,width=250)
        tv.column("fone",minwidth=0,width=100)
        tv.heading("id", text="ID")
        tv.heading("nome", text="NOME")
        tv.heading("fone", text="TELEFONE")
        tv.pack()
        popular()
        
        quadro = tk.LabelFrame(app, text = "Serviço Realizado", background="#b4918f")
        quadro.pack(fill="both", expand='yes',padx=10, pady=10)
        
        tk.Label(
                quadro,
                text="Descrição",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left", pady=10)
        
       
        
        textArea = tk.Text(quadro, width=40, height=2)
        textArea.pack(side="left",padx=10)
        
        tk.Label(
                quadro,
                text="Data Realizada",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left", pady=10)
        
        lb_data = tk.StringVar()   
        data =tk.Entry(quadro, width=10, textvariable=lb_data)
        data.pack(side="left",padx=10)
        
        
        quandro1 = tk.LabelFrame(app, text = "Inserir Dados da Venda", background="#b4918f")
        quandro1.pack(fill="both", expand='yes',padx=10, pady=10)
       
        

        tk.Label(
                quandro1,
                text="Valor",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left", pady=10,padx=10)
        
        lb_valor = tk.StringVar()   
        valor =tk.Entry(quandro1, width=6, textvariable=lb_valor, validate="key", validatecommand=(vcmd,  "%P"))
        valor.pack(side="left",padx=10)
         
        
        tk.Label(
                quandro1,
                text="Desconto %",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left")
        
        text_desc = tk.StringVar()    
        desc =tk.Entry(quandro1, width=6, textvariable=text_desc)
        desc.pack(side="left",padx=10)
        
        tk.Label(
                quandro1,
                text="Valor Total",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left")
        
        
        text_valor_total = tk.StringVar()
        valorTotal =tk.Entry(quandro1, width=6, textvariable=text_valor_total, validate="key", validatecommand=(vcmd,  "%P"))
        valorTotal.pack(side="left",padx=10)
        
        formaPagamneto = dados.db_listar_forma_pagamento()
        lista = []
        for f in formaPagamneto:
            lista.append(f['nome'])
            
        tk.Label(
                quandro1,
                text="Forma de Pagamento",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left")
        
        comboBox = ttk.Combobox(quandro1, values=lista, width=10)
        comboBox.pack(side="left",padx=10)
        
        
        tk.Button(
        quandro1,
        text=("Inserir"), 
        
        command=lambda: criar_atendimento()).pack(side="left")
        
        
        
        quandro2 = tk.LabelFrame(app, text = "Pesquisar Clientes",  background="#b4918f")
        quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

            
        pNome =tk.Entry(quandro2)
        pNome.pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Pesquisar"),
        
        command=lambda: pesquisaCliente()).pack(side="left",padx=10)
        
        

        tk.Button(
        quandro2,
        text=("Mostrar Todos"),
        
        command=lambda: popular()).pack(side="left",padx=10)
        
        app.transient(root)
        app.focus_force()
        app.grab_set()
            
    def deleteCliente():
        
        def deletar():
            try:
                itemS = tve.selection()[0]
                valores = tve.item(itemS,"value")
                msg = messagebox.askquestion("?","Deseja Apagar o Cadastro de {0}".format(valores[1]) )
                if msg == "yes":
                    dados.apagar_cliente(valores[0],valores[1])
                    messagebox.showinfo("Sucesso", "Cadastro foi excluíndo com sucesso")
                    apagarCliente()
                
            except:
                messagebox.showerror("ERRO!", "Precisa Selecionar um item")
                
        
        def apagarCliente():
            tve.delete(*tve.get_children())
            apCliente = dados.db_historico_cliente(nome_cliente.get())
            for c in apCliente:
                tve.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
            
                
            
        app = tk.Toplevel()
        app.title("Cadastrar Cliente")
        x = app.winfo_screenwidth() // 4
        y = int(app.winfo_screenheight() * 0.2)
        app.geometry('600x450+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")   
        
          
        
        
        quadroGrid = tk.LabelFrame(app, text="Clientes")
        quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
        
        tve = ttk.Treeview(quadroGrid, columns=("id","nome","fone"), show="headings")
        tve.column("id",minwidth=0,width=50)
        tve.column("nome",minwidth=0,width=250)
        tve.column("fone",minwidth=0,width=100)
        tve.heading("id", text="ID")
        tve.heading("nome", text="NOME")
        tve.heading("fone", text="TELEFONE")
        tve.pack()
        
        quandro1 = tk.LabelFrame(app, text = "Deletar Cliente")
        quandro1.pack(fill="both", expand='yes',padx=10, pady=10)
        
        tk.Label( 
                quandro1,
                text="Nome cliente",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 12),
                ).pack(pady=(20, 0))
            
        nome_cliente =tk.Entry(quandro1, width=25, font=('TkMenuFont', 10))
        nome_cliente.pack(side="left", pady=(2,0))
        
        

        tk.Button(
        quandro1,
        text=("Buscar"),
        font=('TkMenuFont', 15),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        command=lambda: apagarCliente()).pack(side="left")
        
        b1 = tk.Button(
        quandro1,
        text=("Deletar"),
        font=('TkMenuFont', 15),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: deletar()).pack(side="left")
        
        
        
        
        
        app.transient(root)
        app.focus_force()
        app.grab_set()    
            
    
    def novoCliente():
        
        def criar_cliente():
            if nome_cliente.get() == "" or Telefone.get() == "":
               return messagebox.showinfo(title=False, message="Preencha todos os campos")
                
            ja_existe, c = dados.criar_cliente(nome_cliente.get(),Telefone.get())
            if ja_existe != False:
                nome_cliente.delete(0,tk.END)
                Telefone.delete(0,tk.END)
                return messagebox.showinfo(title=False, message="Cliente Já existe")
                
            else:
                messagebox.showinfo(title=False, message="Cadastro feito com sucesso")
                app.quit
                return
        
        #exec(open(pastaApp+"\\novoCliente.py").read())
        app = tk.Toplevel()
        app.title("Cadastrar Cliente")
        x = app.winfo_screenwidth() // 4
        y = int(app.winfo_screenheight() * 0.2)
        app.geometry('600x400+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")

        tk.Label(
                app,
                text="Nome cliente",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 12),
                ).pack(pady=(20, 0))
            
        nome_cliente =tk.Entry(app, width=65, font=('TkMenuFont', 10))
        nome_cliente.pack(pady=(20, 0))
        
        
        tk.Label(
        app,
        text="Telefone",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 12),
        ).pack(pady=(40, 0))
            
        Telefone = tk.Entry(app, width=65, font=('TkMenuFont', 10))
        Telefone.pack(pady=(20, 0))
        

        tk.Button(
        app,
        text=("Cadastrar"),
        font=('TkMenuFont', 15),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        command=lambda: criar_cliente()).pack(pady=(8, 0))
        
        app.transient(root)
        app.focus_force()
        app.grab_set()
        
        
    
        
    def pesquisarCliente():
        
        def inserir():
            if nome_cliente.get() == "" or fone.get() == "":
               return messagebox.showinfo(title=False, message="Preencha todos os campos")
                
            ja_existe, c = dados.criar_cliente(nome_cliente.get(),fone.get())
            if ja_existe != False:
                nome_cliente.delete(0,tk.END)
                fone.delete(0,tk.END)
                return messagebox.showinfo(title=False, message="Cliente Já existe")
                
            else:
                messagebox.showinfo(title=False, message="Cadastro feito com sucesso")
                nome_cliente.delete(0,tk.END)
                fone.delete(0,tk.END)
                popular()
                return
        
        def popular():
            tv.delete(*tv.get_children())
            cliente = dados.db_listar_cliente()
        
            for c in cliente:
                tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
                
        def pesquisaCliente():
            tv.delete(*tv.get_children())
            historico = dados.db_historico_cliente(pNome.get())
            pNome.delete(0,tk.END)
            for c in historico:
                tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
                
        
        
        app = tk.Toplevel()
        app.title("Pesquisar Cliente")
        x = app.winfo_screenwidth() // 4
        y = int(app.winfo_screenheight() * 0.1)
        app.geometry('600x450+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")
        
        quadroGrid = tk.LabelFrame(app, text="Clientes", background="#b4918f")
        quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
        
        tv = ttk.Treeview(quadroGrid, columns=("id","nome","fone"), show="headings",)
        tv.column("id",minwidth=0,width=50)
        tv.column("nome",minwidth=0,width=250)
        tv.column("fone",minwidth=0,width=100)
        tv.heading("id", text="ID")
        tv.heading("nome", text="NOME")
        tv.heading("fone", text="TELEFONE")
        tv.pack()
        
        popular()

        quandro1 = tk.LabelFrame(app, text = "Inserir Novos Clientes", background="#b4918f")
        quandro1.pack(fill="both", expand='yes',padx=10, pady=10)

        tk.Label(
                quandro1,
                text="Nome cliente"
                ).pack(side="left")
            
        nome_cliente =tk.Entry(quandro1)
        nome_cliente.pack(side="left",padx=10)
        
        tk.Label(
                quandro1,
                text="Telefone"
                ).pack(side="left")
            
        fone =tk.Entry(quandro1)
        fone.pack(side="left",padx=10)
        
        

        tk.Button(
        quandro1,
        text=("Inserir"), 
        
        command=lambda: inserir()).pack(side="left",padx=10)
        
        
        
        quandro2 = tk.LabelFrame(app, text = "Pesquisar Clientes",  background="#b4918f")
        quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

            
        pNome =tk.Entry(quandro2)
        pNome.pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Pesquisar"),
        
        command=lambda: pesquisaCliente()).pack(side="left",padx=10)
        
        

        tk.Button(
        quandro2,
        text=("Mostrar Todos"),
        
        command=lambda: popular()).pack(side="left",padx=10)
        
        app.transient(root)
        app.focus_force()
        app.grab_set()
        
        
        
        
        
    g = dados.db_fazer_login_admin(email, password)
    
    if g is None:
        messagebox.showerror(title=False, message="Email ou Senha Inválido")
    elif g['email'] == email and g['senha'] == password:
        
        frame1.destroy()
        
       
        image = Image.open("assets/Logo-colorido.png")
        resize_image = image.resize((400, 400))
        logo_img = ImageTk.PhotoImage(resize_image)
        
        logo_widget = tk.Label(frame2, image=logo_img, bg="#b4918f")
        logo_widget.image = logo_img
        logo_widget.place(x=200, y=50)
        
        barraMenu = tk.Menu(frame2)
        menuContatos = tk.Menu(barraMenu, tearoff=0)
        menuContatos.add_command(label="Novo",command=novoCliente)
        menuContatos.add_command(label="Pesquisar",command=pesquisarCliente)
        menuContatos.add_command(label="Deletar",command=deleteCliente)
        menuContatos.add_separator()
        menuContatos.add_command(label="Fechar",command=root.quit)
        barraMenu.add_cascade(label="Cadastro",menu=menuContatos)
        

        menuAtendimento = tk.Menu(barraMenu, tearoff=0)
        menuAtendimento.add_command(label="Novo",command=novoAtendimento)
        menuAtendimento.add_command(label="Pesquisar",command=semComando)
        menuAtendimento.add_command(label="Deletar",command=semComando)
       
        barraMenu.add_cascade(label="Atendimento ",menu=menuAtendimento)


        root.config(menu=barraMenu)
        
         
        
        
            
        
            
        
       
        
    else:
        messagebox.showerror(title=False, message="Email ou Senha Inválido") 
    
    
      
    
    
root = tk.Tk()
root.title("Historico de Atendimento")

#root.eval("tk::PlaceWindow . center")
x = root.winfo_screenwidth() // 5
y = int(root.winfo_screenheight() * 0.05)
root.geometry('800x600+' + str(x) + '+' + str(y) )

frame1 = tk.Frame(root, width=800, height=600, bg="#b4918f")
frame2 = tk.Frame(root, width=800, height=600, bg="#b4918f")
frame1.grid(row=0, column=0)
frame2.grid(row=0, column=1)



frame1.pack_propagate(False)
image = Image.open("assets/Logo-colorido.png")
resize_image = image.resize((200, 200))
logo_img = ImageTk.PhotoImage(resize_image)

logo_widget = tk.Label(frame1, image=logo_img, bg="#b4918f")
logo_widget.image = logo_img
logo_widget.pack()


l1 = tk.Label(
frame1,
text="Logar no Sistema",
bg="#b4918f",
fg="white",
font=('TkMenuFont', 14)
).pack()


tk.Label(
    frame1,
    text="Email",
    bg="#b4918f",
    fg="white",
    font=('TkMenuFont', 14),
    padx=15,
    pady=15 
    ).pack()
email = tk.Entry(frame1,width=65, font=('TkMenuFont', 10))
email.place(x=60, y=60)
email.focus()
email.pack()


tk.Label(
    frame1,
    text="Senha",
    bg="#b4918f",
    fg="white",
    font=('TkMenuFont', 14),
    padx=15,
    pady=15 
    ).pack()
password = tk.Entry(frame1,show="*", width=65, font=('TkMenuFont', 10))
password.place(x=60, y=60)
password.pack()


button = tk.Button(
frame1,
text=("Entrar"),
font=('TkMenuFont', 15),
bg="#28393a",
fg="white",
cursor="hand2",
activebackground="#badee2",
activeforeground="black",
    bd = 5,
command=lambda: load_frame2(email.get(),password.get())
)

button.pack(pady=(80, 0))

    



root.mainloop()
dados.db_inicializar()
