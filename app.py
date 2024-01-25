import tkinter as tk
import Banco as dados
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import os
from datetime import datetime, date
from maskedentry import*
from tkcalendar import DateEntry
from operator import neg
import calendario





        
 
def load_frame2(email, password):
    
    
    def agenda():
        appp = tk.Toplevel()
        appp.title("Forma de Pagamento")
        x = appp.winfo_screenwidth() // 8
        y = int(appp.winfo_screenheight() * 0.1)
        appp.geometry('900x600+' + str(x) + '+' + str(y) )
        appp.configure(background="#b4918f")
        
        s = dados.db_listar_saida2()
        events = {}
        for x in s:
            events.setdefault(x['data'][:10], []).append(( x['descricao'] + ' ' + str(f"{x['valor_total']:.2f}"),'reminder'))
       
  
        agenda = calendario.Agenda(appp, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy',firstweekday="sunday")
        
        for k in events.keys():
            date=datetime.strptime(k,"%Y-%m-%d").date()
            for v in range(len(events[k])):
                agenda.calevent_create(date, events[k][v][0], events[k][v][1])
    
    
        

        agenda.tag_config('reminder', background="#8B0000", foreground='white')
        agenda.pack(fill="both", expand=True)
         
    
    
            
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
            lb_data.set (d[1])
            
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
        
     
    def saida():
        
        def editar_salvar():
            try:
                itemS = tvs.selection()[0]
                valores = tvs.item(itemS,"value")
                _data = "{}/{}/{}".format(valores[1][8:10],valores[1][5:7],valores[1][:4])
                
                app = tk.Toplevel()
                app.title("Editar Saída")
                x = app.winfo_screenwidth() // 10
                y = int(app.winfo_screenheight() * 0.03)
                app.geometry('800x400+' + str(x) + '+' + str(y) )
                app.configure(background="#b4918f")
                
                
                quandro3 = tk.LabelFrame(app, text = "Registrar Saída", background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12, 'bold'))
                quandro3.pack()
                
                def validate_entry(text, P):
                    if len(P) > 10:
                        return False
                    
                    if (
                    all(char in "0123456789." for char in text) and  # all characters are valid
                    "-" not in text[1:] and # "-" is the first character or not present
                    text.count(".") <= 1): # only 0 or 1 periods
                        return True
                    else:   
                        return False
                
                
                def alterar_saida():
                    msg = messagebox.askquestion("?","Deseja Excluir o Atendimento do Cliente {0} do dia {1}".format(valores[2], valores[1]) )
                    if msg == "yes":
                        d = pNome.get()
                        if d == "" or descricao.get() == "" or valor.get() == "" or obs.get() == "":
                            return messagebox.showinfo(title=False, message="Preencha todos os campos")
                            
                        else:
                            dados.db_atualizar_saida(valores[0],datetime.strptime(d, "%d/%m/%Y"),descricao.get(),valor.get(), obs.get())
                            messagebox.showinfo(title=False, message="Cadastro feito com sucesso")       
                            app.destroy()
                        

                dataLabel = tk.Label(
                quandro3,
                text="Data",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 10, 'bold'),
                )
                dataLabel.grid(row=0,column=0, sticky='w', padx=5, pady=(5))
                
                
                pNome =DateEntry(quandro3, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
                pNome.grid(row=0,column=1, sticky='ew', padx=5, pady=(5))
                
                descricaoLabel = tk.Label(
                quandro3,
                text="Descrição",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 10, 'bold'),
                )
                
                descricaoLabel.grid(row=1,column=0, sticky='w', padx=5, pady=(5))
                    
                descricao = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10))
                descricao.grid(row=1,column=1, sticky='ew', padx=5, pady=(5), columnspan=2)
                
                
                tk.Label(
                quandro3,
                text="Valor",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 10, 'bold'),
                ).grid(row=2,column=0, sticky='w', padx=5, pady=(5))
                
                
                vn = quandro3.register(validate_entry)
                valor = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10), validate="key", validatecommand=(vn ,"%S","%P"))
                valor.grid(row=2,column=1, sticky='ew', padx=5, pady=(5))
                
                
                
                tk.Label(
                quandro3,
                text="Observação",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 10),
                ).grid(row=3,column=0, sticky='w', padx=5, pady=(5))
                    
                obs = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10))
                obs.grid(row=3,column=1, sticky='ew', padx=5, pady=(5), columnspan=2)
                
                
                tk.Button(
                quandro3,
                text=("Registrar Saída"),
                font=('TkMenuFont', 10),
                bg="#28393a",
                fg="white",
                cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                bd = 5,
                
                command=lambda:  alterar_saida()).grid(row=4,column=1, sticky='w', padx=5, pady=(5))
                
                
                pNome.set_date(_data) 
                descricao.insert(0,valores[2])
                valor.insert(0,valores[3])
                obs.insert(0,valores[4])
                    
                app.transient(root)
                app.focus_force()
                app.grab_set() 
                
                    
                
            except:
                messagebox.showerror("ERRO!", "Precisa Selecionar um item")
            
           
            
                
               
        
        def popular():
            tvs.delete(*tvs.get_children())
            saida = dados.db_listar_saida2()
            
            
            for s in saida:
                tvs.insert("","end", values=(s['id_saida'],s["data"],s['descricao'],"%.2f" %s['valor_total'],s['observacao']))        

        def pesquisaCliente():
            tvs.delete(*tvs.get_children())
            saida = dados.db_listar_saida(datetime.strptime(pNome.get(), "%d/%m/%Y"))
            
            for s in saida:
                tvs.insert("","end", values=(s['id_saida'],s["data"],s['descricao'],"%.2f" %s['valor_total'],s['observacao']))
                
                
        app = tk.Toplevel()
        app.title("Fluxo de Caixa")
        x = app.winfo_screenwidth() // 10
        y = int(app.winfo_screenheight() * 0.03)
        app.geometry('1000x690+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")
        
        
        quandro3 = tk.LabelFrame(app, text = "Registrar Saída", background="#b4918f", fg="white", bd=5, height=1000, font=('TkMenuFont', 12, 'bold'))
        quandro3.grid(row=0, column=0, rowspan=2, sticky='w', padx=25, pady=25 )
         
        def validate_entry(text, P):
            if len(P) > 10:
                return False
            
            if (
            all(char in "0123456789." for char in text) and  # all characters are valid
            "-" not in text[1:] and # "-" is the first character or not present
            text.count(".") <= 1): # only 0 or 1 periods
                return True
            else:   
                return False
        
        
        def criar_saida():
            d = pNome.get()
            if d == "" or descricao.get() == "" or valor.get() == "" or obs.get() == "":
                return messagebox.showinfo(title=False, message="Preencha todos os campos")
                
            else:
                dados.db_criar_saida(datetime.strptime(d, "%d/%m/%Y"),descricao.get().strip(" "),valor.get().strip(" "), obs.get().strip(" "))
                messagebox.showinfo(title=False, message="Cadastro feito com sucesso")       
                descricao.delete(0,tk.END)
                valor.delete(0,tk.END)
                obs.delete(0,tk.END)
                

        dataLabel = tk.Label(
        quandro3,
        text="Data",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 10, 'bold'),
        )
        dataLabel.grid(row=0,column=0, sticky='w', padx=5, pady=(5))
        
        
        pNome =DateEntry(quandro3, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
        pNome.grid(row=0,column=1, sticky='ew', padx=5, pady=(5))
        
        descricaoLabel = tk.Label(
        quandro3,
        text="Descrição",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 10, 'bold'),
        )
        
        descricaoLabel.grid(row=1,column=0, sticky='w', padx=5, pady=(5))
            
        descricao = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10))
        descricao.grid(row=1,column=1, sticky='ew', padx=5, pady=(5), columnspan=2)
        
        
        tk.Label(
        quandro3,
        text="Valor",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 10, 'bold'),
        ).grid(row=2,column=0, sticky='w', padx=5, pady=(5))
        
        
        vn = quandro3.register(validate_entry)
        valor = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10), validate="key", validatecommand=(vn ,"%S","%P"))
        valor.grid(row=2,column=1, sticky='ew', padx=5, pady=(5))
        
        
        
        tk.Label(
        quandro3,
        text="Observação",
        bg="#b4918f",
        fg="white",
        font=('TkMenuFont', 10),
        ).grid(row=3,column=0, sticky='w', padx=5, pady=(5))
            
        obs = tk.Entry(quandro3, width=10, font=('TkMenuFont', 10))
        obs.grid(row=3,column=1, sticky='ew', padx=5, pady=(5), columnspan=2)
        

                   
        tk.Button(
        quandro3,
        text=("Registrar Saída"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda:  criar_saida()).grid(row=4,column=1, sticky='w', padx=5, pady=(5))

                
        quadroGridSaida = tk.LabelFrame(app, text="Saídas", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 14))
        quadroGridSaida.grid(row=0, column=1)
        
        tvs = ttk.Treeview(quadroGridSaida, columns=("id","Data","Nome","Valor_Pago", "forma"), show="headings",)
        
        tvs.column("id",minwidth=0,width=30, anchor=tk.W, )
        tvs.column("Data",minwidth=15,width=70, anchor=tk.W)
        tvs.column("Nome",minwidth=15,width=150, anchor=tk.W)
       
        tvs.column("Valor_Pago",minwidth=0,width=100, anchor=tk.W)
        tvs.column("forma",minwidth=0,width=100, anchor=tk.W)
        tvs.heading("id", text="ID", anchor=tk.W)
        tvs.heading("Data", text="DATA", anchor=tk.W)
        tvs.heading("Nome", text="DESCRIÇÃO", anchor=tk.W)
       
        tvs.heading("Valor_Pago", text="VALOR PAGO", anchor=tk.W)
        tvs.heading("forma", text="OBSERVAÇÃO.", anchor=tk.W)
        tvs.pack()
        popular()
        
        
        
        
        quandro2 = tk.LabelFrame(app, text = "Pesquisar Clientes",  background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 12))
        quandro2.configure(height=1)
        quandro2.grid(row=1, column=1, columnspan=2)

            
        pNome1 =tk.Entry(quandro2)
        pNome1.bind('<Return>',(lambda event: pesquisaCliente()))
        pNome1.pack(side="left",padx=10)
        
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
        
        
        tk.Button(
        quandro2,
        text=("Editar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: editar_salvar()).pack(side="left",padx=10)
        
        app.transient(root)
        app.focus_force()
        app.grab_set() 
      
           
        
    def pesquisarEntrada():
        
        def switch_case(mes,y):
            if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                soma = dados.db_listar_saida_mes_ano((y, mes, 1), (y, mes, 31))
                return float(soma[0]['tt']) * -1 if soma[0]['tt'] != None else f"{0:.2f}"
            
            elif mes == 2:
                if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
                    soma = dados.db_listar_saida_mes_ano((y, mes, 1), (y, mes, 29))
                    return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"
                else:
                    soma = dados.db_listar_saida_mes_ano((y, mes, 1), (y, mes, 28))
                    return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"
                
            else:
                soma = dados.db_listar_saida_mes_ano((y, mes, 1), (y, mes, 30))
                return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"
            
            
        def switch_case_entrada(mes,y):
            if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                soma = dados.db_historico_entrada_saida((y, mes, 1), (y, mes, 31))
                return float(soma[0]['tt']) if soma[0]['tt'] != None else f"{0:.2f}"
            
            elif mes == 2:
                if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
                    soma = dados.db_historico_entrada_saida((y, mes, 1), (y, mes, 29))
                    return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"
                else:
                    soma = dados.db_historico_entrada_saida((y, mes, 1), (y, mes, 28))
                    return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"
                
            else:
                soma = dados.db_historico_entrada_saida((y, mes, 1), (y, mes, 30))
                return f"{soma[0]['tt']:.2f}" if soma[0]['tt'] != None else f"{0:.2f}"
        
                
        def buscarAtendimento2():
            tv.delete(*tv.get_children())
            tvs.delete(*tvs.get_children())
            historico = dados.db_trazer_historico_atendimento(datetime.strptime(pNome.get(), "%d/%m/%Y"))
            historicoConsulta = dados.db_historico_entrada(datetime.strptime(pNome.get(), "%d/%m/%Y"))
            todosSaida = dados.db_listar_saida(datetime.strptime(pNome.get(), "%d/%m/%Y"))
            somaSaida = dados.db_historico_saida(datetime.strptime(pNome.get(), "%d/%m/%Y"))
            
            
            if somaSaida[0]['tt'] == None:
                saida = f"{0:.2f}"
            else:
                saida = f"{somaSaida[0]['tt']:.2f}"
                
           
            if historicoConsulta[0]['tt'] == None:
                entrada = f"{0:.2f}"
            else:
                entrada = f"{historicoConsulta[0]['tt']:.2f}"

            string_variable1.set(saida)
            string_variable.set(entrada) 
            
            corLabel = f"{float(string_variable.get()) - float(string_variable1.get()):.2f}"
            
            if float(corLabel) < 0:
                totalEntradas.configure(foreground="#800000")
            else:
                totalEntradas.configure(foreground="#00008B")
            subtracao.set(corLabel)
            
                       
            for s in todosSaida:
                tvs.insert("","end", values=(s['id_saida'],s["data"],s['descricao'],"%.2f" %s['valor_total'],s['observacao'])) 
              
            for c in historico:
                tv.insert("","end", values=(c['id_atendimento'],c["data"],c['nome'],"%.2f" %c['valor_total'],c['forma_pagamento']))

            d = pNome.get().split("/")
            res = [ele.lstrip('0') for ele in d] 
            comboxMeses.current(int(res[1]))
           
            
            corLabelMes = switch_case(int(res[1]), int(pNome.get()[6:]))
            LabelEntradaMes = float(switch_case_entrada(int(res[1]), int(pNome.get()[6:])))
        
           
            ts = float(corLabelMes)
            somaMes.set(f"{ts:.2f}")
            somaEntradasMes.set(f"{LabelEntradaMes:.2f}")
            
        def atualizar():
            app.destroy()
            pesquisarEntrada()
            
            
        def popular():
            tv.delete(*tv.get_children())
            tvs.delete(*tvs.get_children())
            saida = dados.db_listar_saida(pNome.get())
            cliente = dados.cosultaEntrada(pNome.get())
            t = dados.db_historico_entrada(pNome.get())
            
            for s in saida:
                tvs.insert("","end", values=(s['id_saida'],s["data"],s['descricao'],"%.2f" %s['valor_total'],s['observacao']))        

            for c in cliente:
                tv.insert("","end", values=(c['id_atendimento'],c["data"],c['nome'],"%.2f" %c['valor_total'],c['forma_pagamento']))        

            
                
        app = tk.Toplevel()
        app.title("Fluxo de Caixa")
        x = app.winfo_screenwidth() // 10
        y = int(app.winfo_screenheight() * 0.03)
        app.geometry('1000x690+' + str(x) + '+' + str(y) )
        app.configure(background="#b4918f")
        
        
        
        quadroGrid = tk.LabelFrame(app, text="Entradas", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 14))
        quadroGrid.grid(column=0, row=1, padx=15, pady=10)
        
        tv = ttk.Treeview(quadroGrid, columns=("id","Data","Nome","Valor_Pago", "forma"), show="headings",)
        
        tv.column("id",minwidth=0,width=30, anchor=tk.W, )
        tv.column("Data",minwidth=15,width=70, anchor=tk.W)
        tv.column("Nome",minwidth=15,width=150, anchor=tk.W)
       
        tv.column("Valor_Pago",minwidth=0,width=100, anchor=tk.W)
        tv.column("forma",minwidth=0,width=100, anchor=tk.W)
        tv.heading("id", text="ID", anchor=tk.W)
        tv.heading("Data", text="DATA", anchor=tk.W)
        tv.heading("Nome", text="NOME", anchor=tk.W)
       
        tv.heading("Valor_Pago", text="VALOR PAGO", anchor=tk.W)
        tv.heading("forma", text="FORMA DE PAGAMENTO.", anchor=tk.W)
        tv.pack()
        #popular()
        
       
        
        
        
        quandro2 = tk.LabelFrame(app, text = "Buscar Data",  background="#b4918f", fg="white", bd=5, font=('TkMenuFont', 12, 'bold'))
        quandro2.grid(column=0, row=0, ipady=15, columnspan=2)

      
            
        pNome =DateEntry(quandro2, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
        pNome.bind('<Return>',(lambda event: buscarAtendimento2()))
        pNome.pack(side="left",padx=10)
        
        tk.Button(
        quandro2,
        text=("Buscar "),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: buscarAtendimento2()).pack(side="left",padx=10)
        
        


        tk.Button(
        quandro2,
        text=("Atualizar"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: atualizar()).pack(side="left",padx=10)
        
        
        tk.Button(
        quandro2,
        text=("Registrar Saída"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5,
        
        command=lambda: saida()).pack(side="left",padx=10)
        
        
        
        
        
        
        
        quadroGridSaida = tk.LabelFrame(app, text="Saídas", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 14))
        quadroGridSaida.grid(column=1, row=1, padx=20, pady=10)
        
        tvs = ttk.Treeview(quadroGridSaida, columns=("id","Data","Nome","Valor_Pago", "forma"), show="headings",)
        
        tvs.column("id",minwidth=0,width=30, anchor=tk.W, )
        tvs.column("Data",minwidth=15,width=70, anchor=tk.W)
        tvs.column("Nome",minwidth=15,width=150, anchor=tk.W)
       
        tvs.column("Valor_Pago",minwidth=0,width=100, anchor=tk.W)
        tvs.column("forma",minwidth=0,width=100, anchor=tk.W)
        tvs.heading("id", text="ID", anchor=tk.W)
        tvs.heading("Data", text="DATA", anchor=tk.W)
        tvs.heading("Nome", text="DESCRIÇÃO", anchor=tk.W)
       
        tvs.heading("Valor_Pago", text="VALOR PAGO", anchor=tk.W)
        tvs.heading("forma", text="OBSERVAÇÃO.", anchor=tk.W)
        tvs.pack()
        popular()
        
        
        labelEntradas = tk.Label(quadroGridSaida, text="Total de Saídas ", fg="#696969", background="#b4918f", font=('TkMenuFont', 12, 'bold'))
        labelEntradas.pack(side="left", padx=10)
        
        
        cliente3 = dados.db_historico_saida(pNome.get())
        
        if cliente3[0]['tt'] == None:
            saida1 = f"{0:.2f}"
            
        else:
            saida1 = f"{cliente3[0]['tt']:.2f}"
        
        string_variable1 = tk.StringVar() # Create the variable 
        string_variable1.set(saida1)
        
        totalsaida = tk.Label(quadroGridSaida, textvariable=string_variable1, bd=5, background="#b4918f", fg="#ADD8E6", font=('TkMenuFont', 12, 'bold'))
        totalsaida.pack(side="left")
        

        
        cliente2 = dados.db_historico_entrada(pNome.get())
    
        if cliente2[0]['tt'] == None:
            entrada = f"{0:.2f}"
        else:
            entrada = f"{cliente2[0]['tt']:.2f}"
            
            
            
        
        labelEntrada = tk.Label(quadroGrid, text="Total de Entradas", fg="#696969", background="#b4918f", font=('TkMenuFont', 12, 'bold'))
        labelEntrada.pack(side="left", padx=10)
        
        string_variable = tk.StringVar() # Create the variable 
        string_variable.set(entrada) 
        
        totalEntrada = tk.Label(quadroGrid, textvariable=string_variable, bd=5, background="#b4918f", fg="#ADD8E6", font=('TkMenuFont', 12, 'bold'))
        totalEntrada.pack(side="left")
        
    
        
        subtracao = tk.StringVar()
        corLabel = f"{float(string_variable.get()) - float(string_variable1.get()):.2f}"
        
        if float(corLabel) < 0:
            fgc = "#800000"
        else:
            fgc = "#00008B"
        subtracao.set(corLabel)
        
        totalEntradasaida = tk.Label(app, text='Fluxo do dia', bd=5, background="#b4918f", fg="#ADD8E6", font=('TkMenuFont', 25, 'bold'))
        totalEntradasaida.grid(column=1, row=2, padx=25, pady=1, sticky='w')
        
        totalEntradas = tk.Label(app, textvariable=subtracao, bd=5, background="#b4918f", fg=fgc, font=('TkMenuFont', 25, 'bold'))
        totalEntradas.grid(column=1, row=2, padx=25, pady=1, sticky='e')
        
        meses = ('Selecione o Mês','Janeiro',  
                          'Fevereiro', 
                          'Março', 
                          'Abril', 
                          'Maio', 
                          'Junho',  
                          'Julho',  
                          'Agosto',  
                          'Setembro',  
                          'Outubro',  
                          'Novembro',  
                          'Dezembro')
        
     
        mes_do_Ano = datetime.today()
        
        quadroFluxo = tk.LabelFrame(app, text="Fluxo Total do Mês", background="#b4918f",fg="white", bd=5, font=('TkMenuFont', 14))
        quadroFluxo.grid(column=0, row=3, padx=15, pady=1, sticky='ew')
        
        totalEntradasMes = tk.Label(quadroFluxo, text="Meses: ", bd=5, background="#b4918f", fg=fgc, font=('TkMenuFont', 12, 'bold'))
        totalEntradasMes.grid(row = 0, column = 1)
        
        current_var = tk.StringVar()
        k = current_var.get()
        comboxMeses = ttk.Combobox(quadroFluxo,textvariable=k, state='readonly')
        comboxMeses['values'] = meses
        comboxMeses.current(mes_do_Ano.month)
        comboxMeses.grid(column = 2, row = 0)
        
        
         
        somaMes = tk.StringVar()
        corLabelMes = switch_case(mes_do_Ano.month, mes_do_Ano.year)
        
        
        if float(corLabelMes) < 0:
            fgcm = "#800000"
        else:  
            fgcm = "#00008B"
        somaMes.set(f"{corLabelMes:.2f}")
        
        totalEntradasaida1 = tk.Label(quadroFluxo, text='Total de Saída Mês', bd=5, background="#b4918f", fg=fgcm, font=('TkMenuFont', 12, 'bold'))
        totalEntradasaida1.grid(column=0, row=1, padx=2, pady=1, sticky='w')
        
        totalEntradas1 = tk.Label(quadroFluxo, textvariable=somaMes, bd=5, background="#b4918f", fg=fgcm, font=('TkMenuFont', 12, 'bold'))
        totalEntradas1.grid(column=1, row=1, padx=2, pady=1, sticky='e') 
        
        
        
        somaEntradasMes = tk.StringVar()
        somaEntradasMes.set(f"{switch_case_entrada(mes_do_Ano.month, mes_do_Ano.year):.2f}")
        
        totalEntradasaida2 = tk.Label(quadroFluxo, text='Total de Entradas Mês', bd=5, background="#b4918f", fg=fgcm, font=('TkMenuFont', 12, 'bold'))
        totalEntradasaida2.grid(column=0, row=2, padx=2, pady=1, sticky='w')
        
        totalSaidas_ = tk.Label(quadroFluxo, textvariable=somaEntradasMes, bd=5, background="#b4918f", fg=fgcm, font=('TkMenuFont', 12, 'bold'))
        totalSaidas_.grid(column=1, row=2, padx=2, pady=1, sticky='e') 

        app.transient(root)
        app.focus_force()
        app.grab_set()
        
        
    def novoAtendimento():  
        
        options = []
        formaPag = []
        
                        
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
                
                
        def criar_atendimento():
            
            try:    
                descricoItem = ""
                for j in options:
                    descricoItem += "Quan. {},{}, V. unitario: {}\n".format(j[0],j[1],j[2])
                for i in formaPag:
                    descricoItem += "Valor-{}, Pagamento-{}\n".format(i[0],i[1])        
                items = tv.selection()[0]
                id = tv.item(items,"value")
                desconto= desc.get()
                v = float(desc.get()) + float(valorTotal.get())
                vt = valorTotal.get()
                dataR = datetime.strptime(d, "%d/%m/%Y")
                descricao= descricoItem
                formaPagamento = formaPag
                for f in dados.db_listar_forma_pagamento():
                    if f["nome"] == formaPag[0][1]:
                        formaPagamento = f["id_forma_pagamento"]
                
                if v == "" or vt == "" or dataR == "" or descricao == "" or formaPagamento == "":
                    
                    messagebox.showerror("ERRO!", "Preencha todos os Campos")
                    
                    
                else:
                    msg = messagebox.askquestion("?","Deseja Finalizar o Atendimento?" )
                    
                    if msg == "yes": 
                                  
                        dados.criar_atendimento(id[0],v,desconto, vt, formaPagamento, descricao, dataR)
                        
                        messagebox.showinfo(title=False, message="Atendimento Adicionado com sucesso")
                        app.after(500, app.destroy)
                        novoAtendimento()
                        
                        
            except:
                messagebox.showerror("ERRO!", "Precisa Selecionar um Cliente")
                
                
        def formaPagamento():
            def fechar():
                appp.destroy()
            
            def adicionarForma():
                id = 0
                listaF = [forma1.get(), comboBox.get()]
                formaPag.append(listaF)
                formaPagmanemto = dados.db_listar_forma_pagamento()
                for f in formaPagmanemto:
                    if comboBox.get() == f["nome"]:
                        id = f["id_forma_pagamento"]
                     
                tvc.insert("","end", values=(id,forma1.get(), comboBox.get()))
                segundaFo.set(forma3.get())
                primeiraF.set("0.00")
                
                
                
            def calcForma(e):
            
                segundaF.set(float(segundaFo.get()) - float(forma1.get()))
            
            
            appp = tk.Toplevel()
            appp.title("Forma de Pagamento")
            x = appp.winfo_screenwidth() // 8
            y = int(appp.winfo_screenheight() * 0.1)
            appp.geometry('800x400+' + str(x) + '+' + str(y) )
            appp.configure(background="#b4918f")
            
            
           
            
            tvc = ttk.Treeview(appp, columns=("id","valor","forma de pagamento"), show="headings",)
            tvc.column("id",minwidth=0,width=50, anchor=tk.CENTER)
            tvc.column("valor",minwidth=0,width=250, anchor=tk.CENTER)
            tvc.column("forma de pagamento",minwidth=0,width=100, anchor=tk.CENTER)
            tvc.heading("id", text="ID")
            tvc.heading("valor", text="VALOR")
            tvc.heading("forma de pagamento", text="FORMA DE PAGAMENTO")
            tvc.configure(height=4)
            tvc.pack(fill="both",expand="no", padx=2,pady=10,)
            
            
            tk.Label(
                appp,
                text="Valor Total",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left")
            segundaFo = tk.DoubleVar()
        
            forma2 =tk.Entry(appp, width=8, textvariable=segundaFo, validate="key", validatecommand=(vcmd,  "%P"))
            forma2.pack(side="left",padx=10)
            
            #comboBox = ttk.Combobox(app, values=lista, width=10)
            #comboBox.pack(side="left",padx=10)
            segundaFo.set(valorTotal.get())
            
            
            formaPagamneto = dados.db_listar_forma_pagamento()
            lista = []
            for f in formaPagamneto:
                lista.append(f['nome'])
                
            tk.Label(
                    appp,
                    text="Valor Parcial",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left")
            
            primeiraF = tk.DoubleVar()
        
            forma1 =tk.Entry(appp, width=8, textvariable=primeiraF, validate="key", validatecommand=(vcmd,  "%P"))
            forma1.pack(side="left",padx=10)
            forma1.bind("<KeyRelease>", calcForma)
            
           
            tk.Label(
                    appp,
                    text="Valor Restante",
                    bg="#b4918f",
                    fg="white",
                    font=('TkMenuFont', 9)
                    ).pack(side="left")
            
            segundaF = tk.DoubleVar()
        
            forma3 =tk.Entry(appp, width=8, textvariable=segundaF, validate="key", validatecommand=(vcmd,  "%P"))
            forma3.pack(side="left",padx=10)
            
            tk.Label(
                appp,
                text="Forma de Pagamento",
                bg="#b4918f",
                fg="white",
                font=('TkMenuFont', 9)
                ).pack(side="left")
            
            
            comboBox = ttk.Combobox(appp, values=lista, width=10)
            comboBox.pack(side="left",padx=10)
            
            tk.Button(
            appp,
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
            appp,
            text=("Finalizar "),
            font=('TkMenuFont', 10),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            bd = 5, 
            
            command=lambda: fechar()).place(x=300, y=300)
        
            
            
            
            appp.transient(root)
            appp.focus_force()
            appp.grab_set()
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
        x = app.winfo_screenwidth() // 10
        y = int(app.winfo_screenheight() * 0.03)
        app.geometry('1000x690+' + str(x) + '+' + str(y) )
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
        
        

        
        data = DateEntry(quadroGrid2, selectmode='day',locale='pt_br', date_pattern='dd/MM/yyyy')
        
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
        text=("Adicionar Forma Pagamento"),
        font=('TkMenuFont', 10),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        bd = 5, 
        
        command=lambda: formaPagamento()).pack(side="left")
        
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
            
            command=lambda: criar_atendimento()).pack(side="left")
        
        
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
        
        
        relatorioMenu = tk.Menu(barraMenu, tearoff=0)
        relatorioMenu.add_command(label="Entrada", command=pesquisarEntrada)
        relatorioMenu.add_command(label="Fluxo De Caixa")
        barraMenu.add_cascade(label="Fluxo de caixa", menu=relatorioMenu)
        
        
        AgendaMenu = tk.Menu(barraMenu, tearoff=0)
        AgendaMenu.add_command(label="Agendamento", command=agenda)
        barraMenu.add_cascade(label="Agenda", menu=AgendaMenu)


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
root.attributes('-fullscreen',True)
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
