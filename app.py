import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import os
from datetime import datetime, timedelta
from maskedentry import*







        
 
def load_frame2(email, password):
    
    
            
    def deletarAtendimento():
        
        def deletar():
            try:
                itemS = tv.selection()[0]
                valores = tv.item(itemS,"value")
                msg = messagebox.askquestion("?","Deseja Excluir o Atendimento do Cliente {0} do dia {1}".format(valores[2], valores[1]) )
                if msg == "yes":
                    dados.db_deletar_atendimento(valores[0])
                    messagebox.showinfo("Sucesso", "Cadastro foi excluíndo com sucesso")
                    app.destroy()
                    
                
            except:
                messagebox.showerror("ERRO!", "Precisa Selecionar um item")
                
        def buscarAtendimento():
            tv.delete(*tv.get_children())
            historico = dados.db_historico_atendimento(pNome.get())
            pNome.delete(0,tk.END)
            for c in historico:
                tv.insert("","end", values=(c['id_atendimento'],c["data"],c['nome'],"%.2f" %c['valor_unitario'], c['descricao'],"%.2f" %c['desconto'],"%.2f" %c['valor_total'],c['forma_pagamento']))
                
        
        def popular():
            tv.delete(*tv.get_children())
            cliente = dados.db_listar_atendimento()
        
            for c in cliente:
                tv.insert("","end", values=(c['id_atendimento'],c["data"],c['nome'],"%.2f" %c['valor_unitario'], c['descricao'],"%.2f" %c['desconto'],"%.2f" %c['valor_total'],c['forma_pagamento']))        
                
        app = tk.Toplevel()
        app.title("Excluir Atendimento")
        x = app.winfo_screenwidth() // 8
        y = int(app.winfo_screenheight() * 0.1)
        app.geometry('1000x600+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")
        
        
        
        quadroGrid = tk.LabelFrame(app, text="Atendimentos", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
        
        tv = ttk.Treeview(quadroGrid, columns=("id","Data","Nome","Valor", "Descricao", "Desconto","Valor_Pago", "forma"), show="headings",)
        tv.column("id",minwidth=15,width=50)
        tv.column("Data",minwidth=15,width=70)
        tv.column("Nome",minwidth=15,width=250)
        tv.column("Valor",minwidth=15,width=100)
        tv.column("Descricao",minwidth=50,width=250)
        tv.column("Desconto",minwidth=0,width=100)
        tv.column("Valor_Pago",minwidth=0,width=100)
        tv.column("forma",minwidth=0,width=100)
        tv.heading("id", text="ID")
        tv.heading("Data", text="DATA")
        tv.heading("Nome", text="NOME")
        tv.heading("Valor", text="VALOR")
        tv.heading("Descricao", text="DESCRIÇÃO")
        tv.heading("Desconto", text="DESCONTO")
        tv.heading("Valor_Pago", text="VALOR PAGO")
        tv.heading("forma", text="FORMA DE PAGAMENTO")
        tv.pack()
        popular()
         
              
        
        
        quandro2 = tk.LabelFrame(app, text = "Pesquisar Clientes",  background="#b4918f", fg="white",bd=5, font=('TkMenuFont',12))
        quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

            
        pNome =tk.Entry(quandro2)
        pNome.bind('<Return>', (lambda event: buscarAtendimento()))
        pNome.pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Pesquisar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: buscarAtendimento()).pack(side="left",padx=10)
        
        

        tk.Button(
        quandro2,
        text=("Mostrar Todos"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: popular()).pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Excluir Atendimento"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: deletar()).pack(side="left",padx=10)
        app.transient(root)
        app.focus_force()
        app.grab_set()
        
        
        
    def editarAtendimeto(d):
        
        
    
            def salvar():
                msg = messagebox.askquestion("?","Deseja Alterar o Atendimento de {0}".format(d[2]) )
                if msg == "yes":
                    id_forma = ""
                    forma = dados.db_listar_forma_pagamento()
                    for j in forma:
                        if comboBox.get() == j["nome"]:
                            id_forma = j["id_forma_pagamento"]
                    
                    dados.db_editar_atendimento(d[0], id.get(),valor.get(), desc.get(), valorTotal.get(), id_forma, textArea.get("1.0",tk.END), data.get())
                    messagebox.showinfo("Sucesso", "Atendimento foi Alterado com sucesso")
                    
                    #dados.db_editar_atendimento(id_atendimento, id_cliente, valor_unitario, desconto, valor_total, id_forma_pagamento, descricao, data)
                    rootalter.destroy() 
                    pesquisarAtendimento()
                    
                    
            def voltar():
                pesquisarAtendimento()
                rootalter.destroy()                
            
            def calc(e):
                a = float(valor.get()) - float(desc.get())
                text_valor_total.set(a)
            
            def limitar_tamanho(P):
                if P == "": return True
                try:
                    value = float(P)
                except ValueError:
                    return False
                return 0 <= value <= 10000
            
            
            
            rootalter = tk.Toplevel()
            rootalter.title("Alterar Atendimento")
            x = rootalter.winfo_screenwidth() // 8
            y = int(rootalter.winfo_screenheight() * 0.1)
            rootalter.geometry('1000x600+' + str(x) + '+' + str(y) )
            rootalter.configure(background="#b4918f")
            
            quadroNome = tk.LabelFrame(rootalter, text = "Dados do Cadastro", background="#b4918f",foreground="white",bd=5, font=('TkMenuFont', 12))
            quadroNome.pack(fill="both", expand='yes',padx=10, pady=10)
            
        
            tk.Label(
                    quadroNome,
                    text="ID",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left", pady=15)
            
            lb_id = tk.StringVar()   
            id = tk.Entry(quadroNome, width=5, textvariable=lb_id)
            id.pack(side="left",padx=15)
            
            tk.Label(
                    quadroNome,
                    text="NOME",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left", pady=15)
            
            lb_nome = tk.StringVar()   
            c_nome = tk.Entry(quadroNome, width=50, textvariable=lb_nome)
            c_nome.pack(side="left",padx=15)
            
            cliente = dados.db_listar_cliente()
            for c in cliente:
                if c['nome'] == d[2]:
                    lb_id.set(c['id_cliente'])
                    lb_nome.set(c['nome'])
                    
            quadro = tk.LabelFrame(rootalter, text = "Serviço Realizado", background="#b4918f",foreground="white", bd=5, font=('TkMenuFont', 12))
            quadro.pack(fill="both", expand='yes',padx=10, pady=10)
            
            vcmd = rootalter.register(func=limitar_tamanho)
            
            tk.Label(
                    quadro,
                    text="Descrição",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left", pady=10)
            
        
            
            textArea = tk.Text(quadro, width=50, height=4    )
            textArea.pack(side="left",padx=10)
            textArea.insert(tk.END, d[4])
            tk.Label(
                    quadro,
                    text="Data Realizada",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left", pady=10)
            
            lb_data = tk.StringVar()   
            data = MaskedWidget(quadro,'fixed', mask='99/99/9999', width=10, textvariable=lb_data)
            data.pack(side="left",padx=10)
            lb_data.set(d[1])
            
            quandro1 = tk.LabelFrame(rootalter, text = "Alterar Dados da Venda", background="#b4918f", foreground="white", bd=5, font=('TkMenuFont', 12))
            quandro1.pack(fill="both", expand='yes',padx=10, pady=10)
        
            

            tk.Label(
                    quandro1,
                    text="Valor",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left", pady=10,padx=10)
            
            lb_valor = tk.DoubleVar()   
            valor =tk.Entry(quandro1, width=8, textvariable=lb_valor, validate="key", validatecommand=(vcmd, "%P"))
            valor.pack(side="left",padx=10)
            lb_valor.set(float(d[3]))
            
            tk.Label(
                    quandro1,
                    text="Desconto Reais",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left")
            
            text_desc = tk.DoubleVar()    
            desc =tk.Entry(quandro1, width=6, textvariable=text_desc, validate="key", validatecommand=(vcmd,  "%P"))
            desc.pack(side="left",padx=10)
            desc.bind("<KeyRelease>", calc)
            text_desc.set(float(d[5]))
            tk.Label(
                    quandro1,
                    text="Valor Total",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left")
            
            text_valor_total = tk.DoubleVar()
            
            valorTotal =tk.Entry(quandro1, width=8, textvariable=text_valor_total, validate="key", validatecommand=(vcmd,  "%P"))
            text_valor_total.set(d[6])
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
            comboBox.set(d[7])
            comboBox.pack(side="left",padx=10)
            
            
            tk.Button(
            quandro1,
            text=("Salvar Altereção"),
            font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd = 5, 
            
            command=lambda: salvar()).pack(side="left")
            
            tk.Button(
            quandro1,
            text=("Voltar"),
            font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd = 5, 
            
            command=lambda: voltar()).pack(side="left")
            
            rootalter.transient(root)
            rootalter.focus_force()
            rootalter.grab_set()
                
            
                
        
    def pesquisarAtendimento():
        
        
            
            
              
        def alterar():
            try:
                items = tv.selection()[0]
                d = tv.item(items,"value")
                editarAtendimeto(d)    
                app.destroy()
            except:
                messagebox.showerror("ERRO!", "Escolha um Atendimento")
                
        def buscarAtendimento():
            tv.delete(*tv.get_children())
            historico = dados.db_historico_atendimento(pNome.get())
            pNome.delete(0,tk.END)
            for c in historico:
                tv.insert("","end", values=(c['id_atendimento'],c["data"],c['nome'],"%.2f" %c['valor_unitario'], c['descricao'],"%.2f" %c['desconto'],"%.2f" %c['valor_total'],c['forma_pagamento']))
                
        
        def popular():
            tv.delete(*tv.get_children())
            cliente = dados.db_listar_atendimento()
        
            for c in cliente:
                tv.insert("","end", values=(c['id_atendimento'],c["data"],c['nome'],"%.2f" %c['valor_unitario'], c['descricao'],"%.2f" %c['desconto'],"%.2f" %c['valor_total'],c['forma_pagamento']))        
                
        app = tk.Toplevel()
        app.title("Pesquisar Atendimento")
        x = app.winfo_screenwidth() // 8
        y = int(app.winfo_screenheight() * 0.1)
        app.geometry('1000x600+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")
        
        
        
        quadroGrid = tk.LabelFrame(app, text="Atendimentos", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
        quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
        
        tv = ttk.Treeview(quadroGrid, columns=("id","Data","Nome","Valor", "Descricao", "Desconto","Valor_Pago", "forma"), show="headings",)
        
        tv.column("id",minwidth=0,width=30, anchor=tk.W, )
        tv.column("Data",minwidth=15,width=70, anchor=tk.W)
        tv.column("Nome",minwidth=15,width=150, anchor=tk.W)
        tv.column("Valor",minwidth=15,width=60, anchor=tk.W)
        tv.column("Descricao",minwidth=0,width=400, anchor=tk.W)
        tv.column("Desconto",minwidth=0,width=70, anchor=tk.W)
        tv.column("Valor_Pago",minwidth=0,width=100, anchor=tk.W)
        tv.column("forma",minwidth=0,width=100, anchor=tk.W)
        tv.heading("id", text="ID", anchor=tk.W)
        tv.heading("Data", text="DATA", anchor=tk.W)
        tv.heading("Nome", text="NOME", anchor=tk.W)
        tv.heading("Valor", text="VALOR", anchor=tk.W)
        tv.heading("Descricao", text="DESCRIÇÃO", anchor=tk.W)
        tv.heading("Desconto", text="DESCONTO", anchor=tk.W)
        tv.heading("Valor_Pago", text="VALOR PAGO", anchor=tk.W)
        tv.heading("forma", text="FORMA DE PAG.", anchor=tk.W)
        tv.pack()
        popular()
        
        
        
        
        
        quandro2 = tk.LabelFrame(app, text = "Pesquisar Clientes",  background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

            
        pNome =tk.Entry(quandro2)
        pNome.bind('<Return>',(lambda event: buscarAtendimento()))
        pNome.pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Pesquisar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: buscarAtendimento()).pack(side="left",padx=10)
        
        

        tk.Button(
        quandro2,
        text=("Mostrar Todos"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: popular()).pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Ver Detalhes"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: alterar()).pack(side="left",padx=10)
        app.transient(root)
        app.focus_force()
        app.grab_set()
        
    def novoAtendimento():  
        options = []
        formaPag = []
        def criar_atendimento(comboBox):
            try :
                descricoItem = ""
                for j in options:
                    descricoItem += "Quan. {},{}, V. unitario {}\n".format(j[0],j[1],j[2])
                    
                items = tv.selection()[0]
                id = tv.item(items,"value")
                desconto= desc.get()
                v = float(desc.get()) + float(valorTotal.get())
                vt = valorTotal.get()
                dataR = data.get()
                descricao= descricoItem
                formaPagamento = comboBox
                if v == "" or vt == "" or dataR == "" or descricao == "" or formaPagamento == "":
                    messagebox.showerror("ERRO!", "Preencha todos os Campos")
                   
                    
                else:
                    msg = messagebox.askquestion("?","Deseja Finalizar o Atendimento?" )
                    
                    if msg == "yes":
                        lista = dados.db_listar_forma_pagamento()
                        id_forma_pagamento = 0
                        for i in lista:
                            if formaPagamento == i["nome"]:
                                id_forma_pagamento = i["id_forma_pagamento"]
                        
                        dados.criar_atendimento(id[0],v,desconto, vt, id_forma_pagamento, descricao, dataR)
                       
                        messagebox.showinfo(title=False, message="Atendimento Adicionado com sucesso")
                        app.after(500, app.destroy)
                        novoAtendimento()
                        
                        
            except:
                messagebox.showerror("ERRO!", "Precisa Selecionar um Cliente")
                
                
        
        def popular():
            tv.delete(*tv.get_children())
            cliente = dados.db_listar_cliente()
        
            for c in cliente:
                tv.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
                
        
            
                    
        def calc(e):
            soma = 0
            for i in options:
                soma += int(i[0]) * float(i[2])
            a = soma - float(desc.get())
            
            text_valor_total.set(a)
            
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
                
        def formaPagamento():
            
            def adicionarForma():
                listaF = [forma1.get(), comboBox.get()]
                formaPag.append(listaF)
               
                     
                tv.insert("","end", values=(1,forma1.get(), comboBox.get()))
                
                
                
            def calcForma(e):
            
                segundaF.set(float(valorTotal.get()) - float(forma1.get()))
            
            
            app = tk.Toplevel()
            app.title("Forma de Pagamento")
            x = app.winfo_screenwidth() // 4
            y = int(app.winfo_screenheight() * 0.1)
            app.geometry('600x400+' + str(x) + '+' + str(y) )
            app.configure(background="#b4918f")
            
            
           
            
            tv = ttk.Treeview(app, columns=("id","valor","forma de pagamento"), show="headings",)
            tv.column("id",minwidth=0,width=50, anchor=tk.CENTER)
            tv.column("valor",minwidth=0,width=250, anchor=tk.CENTER)
            tv.column("forma de pagamento",minwidth=0,width=100, anchor=tk.CENTER)
            tv.heading("id", text="ID")
            tv.heading("valor", text="VALOR")
            tv.heading("forma de pagamento", text="FORMA DE PAGAMENTO")
            tv.configure(height=4)
            tv.pack(fill="both",expand="no", padx=2,pady=10,)
            
            
            tk.Label(
                app,
                text="Valor Total",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left")
            segundaFo = tk.DoubleVar()
        
            forma2 =tk.Entry(app, width=8, textvariable=segundaFo, validate="key", validatecommand=(vcmd,  "%P"))
            forma2.pack(side="left",padx=10)
            
            #comboBox = ttk.Combobox(app, values=lista, width=10)
            #comboBox.pack(side="left",padx=10)
            segundaFo.set(valorTotal.get())
            
            
            formaPagamneto = dados.db_listar_forma_pagamento()
            lista = []
            for f in formaPagamneto:
                lista.append(f['nome'])
                
            tk.Label(
                    app,
                    text="Forma de Pagamento",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left")
            
            primeiraF = tk.DoubleVar()
        
            forma1 =tk.Entry(app, width=8, textvariable=primeiraF, validate="key", validatecommand=(vcmd,  "%P"))
            forma1.pack(side="left",padx=10)
            forma1.bind("<KeyRelease>", calcForma)
            
           
            
            
            segundaF = tk.DoubleVar()
        
            forma3 =tk.Entry(app, width=8, textvariable=segundaF, validate="key", validatecommand=(vcmd,  "%P"))
            forma3.pack(side="left",padx=10)
            
            
            
            comboBox = ttk.Combobox(app, values=lista, width=10)
            comboBox.pack(side="left",padx=10)
            
            tk.Button(
            app,
            text=("Adicionar"),
            font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd = 5, 
            
            command=lambda: adicionarForma()).pack(side="left")
            
            tk.Button(
            app,
            text=("Finalizar"),
            font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd = 5, 
            
            command=lambda: criar_atendimento(comboBox.get())).place(x=250, y=300)
        
            
            
            
            app.transient(root)
            app.focus_force()
            app.grab_set()
            forma2.focus()
                
        def adicionarServico():
            if qta.get() == "" or textArea.get() == "" or valor.get() == "0.0":
                messagebox.showinfo("ERRO", "Digite Todos os Dados")
                return
            items =[qta.get(),textArea.get(), valor.get()]
            options.append(items)
            total = int(qta.get()) * float(valor.get())
            tv2.insert("","end", values=(qta.get(),textArea.get(), valor.get(), total))
            colTotal()
            qta.delete(0,tk.END)
            textArea.delete(0,tk.END)
            lb_valor.set(0.0)
            qta.focus()
            
        def deletar():
            try:
                itemSelecionado = tv2.selection()[0]
                valores = tv2.item(itemSelecionado, "value")
                for i in range(len(options)):
                    if options[i][1] == valores[1]:
                        options.pop(i)
                        
                        colTotal()
                tv2.delete(itemSelecionado)
                
            except:
                messagebox.showinfo("ERRO","Selecione o item a ser deletado")
                
        def colTotal():
            soma = 0
            for i in options:
                soma += int(i[0]) * float(i[2])
            text_valor_total.set(soma)  
            
               
                
                  
            
        app = tk.Toplevel()
        app.title("Novo Atendimento")
        x = app.winfo_screenwidth() // 8
        y = int(app.winfo_screenheight() * 0.0)
        app.geometry('1000x800+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")
        
        vcmd = app.register(func=limitar_tamanho)
        
        quadroGrid = tk.LabelFrame(app, text="Clientes", background="#b4918f", fg="white", bd=5,font=('TkMenuFont', 12))
        quadroGrid.configure(height=3)
        quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
        
        tv = ttk.Treeview(quadroGrid, columns=("id","nome","fone"), show="headings",)
        tv.column("id",minwidth=0,width=50, anchor=tk.CENTER)
        tv.column("nome",minwidth=0,width=250, anchor=tk.CENTER)
        tv.column("fone",minwidth=0,width=100, anchor=tk.CENTER)
        tv.heading("id", text="ID")
        tv.heading("nome", text="NOME")
        tv.heading("fone", text="TELEFONE")
        tv.configure(height=1)
        tv.pack(fill="both",expand="yes", padx=10,pady=10,)
        popular()
        
        quadroGrid2 = tk.LabelFrame(app, text="Adicionar Atendimentos", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
        quadroGrid2.pack(fill="both",expand="yes", padx=10,pady=10)
              
        tv2 = ttk.Treeview(quadroGrid2, columns=("item","Descricao","Valor","Total"), show="headings",)
        tv2.configure(height=2)
        tv2.column("item",minwidth=0,width=80, anchor=tk.CENTER)
        tv2.column("Descricao",minwidth=15,width=250,anchor=tk.CENTER)
        tv2.column("Valor",minwidth=15,width=100,anchor=tk.CENTER)
        tv2.column("Total",minwidth=15,width=100,anchor=tk.CENTER)
        
        
        
        tv2.heading("item", text="QUANTIDADE")
        tv2.heading("Descricao", text="DESCRIÇÃO")
        tv2.heading("Valor", text="VALOR")
        tv2.heading("Total", text="TOTAL")
        
        tv2.pack(fill="both",expand="yes", padx=10,pady=10)
        
        quadro = tk.LabelFrame(app, text = "Serviço Realizado", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
        quadro.configure(height=2)
        quadro.pack(fill="both", expand='yes',padx=10, pady=10)
        
        tk.Label(
                quadroGrid2,
                text="Data Realizada",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left", pady=10)
        
        lb_data = tk.StringVar()   
        data = MaskedWidget(quadroGrid2,'fixed', mask='99/99/9999', width=10, textvariable=lb_data)
        data.pack(side="left",padx=10)
        
       
        
        tk.Label(
                quadroGrid2,
                text="Quantidade",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left", pady=10)
        
       
        
        qta = tk.Entry(quadroGrid2)
        qta.pack(side="left",padx=10)
        
        tk.Label(
            quadroGrid2,
            text="Descrição",
            bg="#b4918f",
            fg="white",
            font=('TkMenuFont', 9)
            ).pack(side="left", pady=10)
    
    
    
        textArea = tk.Entry(quadroGrid2)
        textArea.pack(side="left",padx=10)
        
        
        
        #quandro1 = tk.LabelFrame(app, text = "Inserir Dados da Venda", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        #quandro1.pack(fill="both", expand='yes',padx=10, pady=10)
       
        

        tk.Label(
                quadroGrid2,
                text="Valor",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left", pady=10,padx=10)
        
        lb_valor = tk.DoubleVar()   
        valor =tk.Entry(quadroGrid2, width=8, textvariable=lb_valor, validate="key", validatecommand=(vcmd, "%P"))
        valor.pack(side="left",padx=10)
        
        
        
        tk.Button(
        quadroGrid2,
        text=("Inserir"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5, 
        
        command=lambda: adicionarServico()).pack(side="left") 
        
        tk.Button(
        quadroGrid2,
        text=("Deletar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5, 
        
        command=lambda: deletar()).pack(side="left") 
        
       
        
        qta.focus()
        
        tk.Label(
                quadro,
                text="Desconto Reais",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left")
        
        text_desc = tk.DoubleVar()    
        desc =tk.Entry(quadro, width=6, textvariable=text_desc, validate="key", validatecommand=(vcmd,  "%P"))
        desc.pack(side="left",padx=10)
        desc.bind("<KeyRelease>", calc)
        tk.Label(
                quadro,
                text="Valor Total",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left")
        
        text_valor_total = tk.DoubleVar()
        
        valorTotal =tk.Entry(quadro, width=8, textvariable=text_valor_total, validate="key", validatecommand=(vcmd,  "%P"))
        valorTotal.pack(side="left",padx=10)
        
        
                      
        
        
        
        
        tk.Button(
        quadro,
        text=("Finalizar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5, 
        
        command=lambda: formaPagamento()).pack(side="left")
        
        
        
        quandro2 = tk.LabelFrame(app, text = "Pesquisar Clientes",  background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
        quandro2.configure(height=1)
        quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

            
        pNome =tk.Entry(quandro2)
        pNome.bind('<Return>',(lambda event: pesquisaCliente()))
        pNome.pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Pesquisar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: pesquisaCliente()).pack(side="left",padx=10)
        
        

        tk.Button(
        quandro2,
        text=("Mostrar Todos"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: popular()).pack(side="left",padx=10)
        
        app.transient(root)
        app.focus_force()
        app.grab_set()
            
    def deleteCliente():
        
        def deletar():
            try:
                itemS = tve.selection()[0]
                valores = tve.item(itemS,"value")
                msg = messagebox.askquestion("?","Deseja Excluir o Cadastro de {0}".format(valores[1]) )
                if msg == "yes":
                    dados.apagar_cliente(valores[0],valores[1])
                    messagebox.showinfo("Sucesso", "Cadastro foi excluíndo com sucesso")
                    historicoCliente()
                
            except:
                messagebox.showerror("ERRO!", "Precisa Selecionar um item")
                
        
        def historicoCliente():
            tve.delete(*tve.get_children())
            apCliente = dados.db_historico_cliente(nome_cliente.get())
            for c in apCliente:
                tve.insert("","end", values=(c["id_cliente"],c['nome'],c['telefone']))
            
                
            
        app = tk.Toplevel()
        app.title("Cadastrar Cliente")
        x = app.winfo_screenwidth() // 4
        y = int(app.winfo_screenheight() * 0.2)
        app.geometry('700x500+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")   
        
          
        
        
        quadroGrid = tk.LabelFrame(app, text="Clientes", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        quadroGrid.pack(fill="both",expand="yes", padx=10,pady=10)
        
        tve = ttk.Treeview(quadroGrid, columns=("id","nome","fone"), show="headings")
        tve.column("id",minwidth=0,width=50)
        tve.column("nome",minwidth=0,width=250)
        tve.column("fone",minwidth=0,width=100)
        tve.heading("id", text="ID")
        tve.heading("nome", text="NOME")
        tve.heading("fone", text="TELEFONE")
        tve.pack()
        
        quandro1 = tk.LabelFrame(app, text = "Excluir Cadastro", background = "#b4918f",fg="white", bd=5, font=('TkMenuFont', 12) )
        quandro1.pack(fill="both", expand='yes',padx=10, pady=10)
        
        tk.Label( 
                quandro1,
                text="Nome cliente",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 12),
                
                ).pack(side="left",pady=(2, 0))
            
        nome_cliente =tk.Entry(quandro1, width=25, font=('TkMenuFont', 10))
        nome_cliente.bind('<Return>',(lambda event: historicoCliente()))
        nome_cliente.pack(side="left", pady=(2,0))
        
        

        tk.Button(
        quandro1,
        text=("Buscar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        command=lambda: historicoCliente()).pack(side="left")
        
        b1 = tk.Button(
        quandro1,
        text=("Excluir"),
        font=('TkMenuFont', 10),
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
                
            ja_existe, c = dados.criar_cliente(nome_cliente.get().strip(" ").capitalize(),Telefone.get().strip(" "))
            if ja_existe != False:
                nome_cliente.delete(0,tk.END)
                Telefone.delete(0,tk.END)
                return messagebox.showinfo(title=False, message="Cliente Já existe")
                
            else:
                messagebox.showinfo(title=False, message="Cadastro feito com sucesso")
                app.destroy()
                
        
        #exec(open(pastaApp+"\\novoCliente.py").read())
        app = tk.Toplevel()
        app.title("Cadastrar Cliente")
        app.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))
        x = app.winfo_screenwidth() // 4
        y = int(app.winfo_screenheight() * 0.2)
        app.geometry('700x500+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")

        tk.Label(
                app,
                text="Nome cliente",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 12),
                bd=5
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
        app.geometry('700x500+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")
        
        quadroGrid = tk.LabelFrame(app, text="Clientes", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
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

        quandro1 = tk.LabelFrame(app, text = "Inserir Novos Clientes", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12))
        quandro1.pack(fill="both", expand='yes',padx=10, pady=10)

        tk.Label(
                quandro1,
                text="Nome cliente",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 12),
                bd=5,
                ).pack(side="left")
            
        nome_cliente =tk.Entry(quandro1)
        nome_cliente.pack(side="left",padx=10)
        
        tk.Label(
                quandro1,
                text="Telefone",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 12),
                ).pack(side="left")
            
        fone =tk.Entry(quandro1)
        fone.pack(side="left",padx=10)
        
        

        tk.Button(
        quandro1,
        text=("Inserir"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5, 
        
        command=lambda: inserir()).pack(side="left",padx=10)
        
        
        
        quandro2 = tk.LabelFrame(app, text = "Pesquisar Clientes",  background="#b4918f", fg="white",bd=5, font=('TkMenuFont', 12))
        quandro2.pack(fill="both", expand='yes',padx=10, pady=10)

            
        pNome =tk.Entry(quandro2)
        pNome.bind('<Return>', (lambda event: pesquisaCliente()))
        pNome.pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Pesquisar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: pesquisaCliente()).pack(side="left",padx=10)
        
        

        tk.Button(
        quandro2,
        text=("Mostrar Todos"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: popular()).pack(side="left",padx=10)
        
        app.transient(root)
        app.focus_force()
        app.grab_set()
        
        
        
        
        
    g = dados.db_fazer_login_admin(email, password)
    
    if g is None:
        messagebox.showerror(title=False, message="Email ou Senha Inválido")
    elif g['email'] == email and g['senha'] == password:
        
        frame1.destroy()
        
       
        image = Image.open("assets/salao-de-beleza.jpeg")
        resize_image = image.resize((1360, 728))
        logo_img = ImageTk.PhotoImage(resize_image)
        
        logo_widget = tk.Label(frame2, image=logo_img)
        logo_widget.image = logo_img
        logo_widget.place(x=0, y=0)
        
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
        menuAtendimento.add_command(label="Pesquisar",command=pesquisarAtendimento)
        menuAtendimento.add_command(label="Deletar",command=deletarAtendimento)
       
        barraMenu.add_cascade(label="Atendimento ",menu=menuAtendimento)


        root.config(menu=barraMenu)
        
         
        
        
            
        
            
        
       
        
    else:
        messagebox.showerror(title=False, message="Email ou Senha Inválido") 
    
    
      
    
    
root = tk.Tk()
root.title("Historico de Atendimento")
root.iconphoto(False, tk.PhotoImage(file='assets/Logo-colorido.png'))

#root.eval("tk::PlaceWindow . center")
x = root.winfo_screenwidth() // 240

y = int(root.winfo_screenheight() * 0.0)
root.geometry('1360x728+' + str(x) + '+' + str(y) )

frame1 = tk.Frame(root, width=1360, height=728, bg="#b4918f")
frame2 = tk.Frame(root, width=1360, height=728, bg="#b4918f")
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
    text="Usuário",
    bg="#b4918f",
    fg="white",
    font=('TkMenuFont', 14),
    padx=15,
    pady=15 
    ).pack()
email = tk.Entry(frame1,width=65, font=('TkMenuFont', 10))
email.place(x=60, y=60)
email.focus()
email.bind('<Return>',(lambda event: load_frame2(email.get(),password.get())))
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
password.bind('<Return>',(lambda event: load_frame2(email.get().strip(" "),password.get().strip(" "))))
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
