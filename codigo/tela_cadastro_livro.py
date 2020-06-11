#-*- coding: utf-8 -*-

try:
    from Tkinter import *
    import ttk
    print("python 2x")

except ImportError:
    from tkinter import *
    from tkinter import ttk
    print("python 3x")



#----------------------------------------------#


class Default(object):
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        
        self.background = "#282828"
        self.geometry = "500x500"
        self.font = (None, 12, "bold")


class LabelDefault(ttk.Label):
    def __init__(self, *args, **kwargs):
        ttk.Label.__init__(self, *args, **kwargs)
        
        default = Default()
        
       
        self.configure(
            foreground = "white",
            background = default.background, 
            width = 15
        )
        self.pack(side = "left", anchor = "nw", padx = 1, pady = 1)


class EntryDefault(ttk.Entry):
    def __init__(self, *args, **kwargs):
        ttk.Entry.__init__(self, *args, **kwargs)
        
        default = Default()
        self.configure(
            font = default.font
        )
        self.pack(side = "left", fill = "x", expand = True, padx = 1, pady = 1)


class FrameEntry(Frame):
    def __init__(self, parent, label_text, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        default = Default()
        self.configure(
            background = default.background
        )
        self.label = LabelDefault(self, text = label_text)
        self.entry = EntryDefault(self)
        self.pack(fill = "x", padx = 5, pady = 5)
        
        self.label.bind("<Button-1>", lambda event: self.entry.focus())
        self.entry.bind("<Key>", lambda event: self.setBackground(default.background))
    
    def getEntry(self):
        return self.entry.get()
    
    def setEntry(self, text):
        self.entry.insert("end", text)
    
    def setBackground(self, background):
        self.label.configure(background = background)


class ButtonCategoria(ttk.Button):
    def __init__(self, *args, **kwargs):
        ttk.Button.__init__(self, *args, **kwargs)
        self.pack(side = "left", fill = "x", expand = True, padx = 5)


class FrameCategoria(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent,  *args, **kwargs),0
        
        default = Default()
        self.configure(
            background = default.background
        )
        
        #criando os widgets
        self.tree = ttk.Treeview(self)
        scroll = Scrollbar(self, command = self.tree.yview)
        self.tree.configure(yscrollcommand = scroll.set)
        
        self.tree["columns"] = ("categorias")
        self.tree.heading("categorias", text = "Categorias")
        self.tree.column("#0", width = 0, stretch = False)
        
        #posicionando
        self.pack(fill = "both", expand = True, padx = 5, pady = 5)
        self.pack_propagate(False)
        self.tree.pack(side = "left", fill = "both", expand = True)
        scroll.pack(side = "left", fill = "y")

        #comandos

        #-testes-#
       
        #-fim testes-#

    def getCategoriaItem(self, categoria):
        #retornar o item de uma categoria de self.tree
        for item in self.tree.get_children(""):
            if (self.tree.item(item)["values"][0]) == categoria:
                return item
        return None
        
    def setCategoria(self, *categorias):
        #selecionar as categorias 
        itens = []
        for categoria in categorias:
            item = self.getCategoriaItem(categoria)
            if item:
                itens.append(item)
        self.tree.selection_set(*itens)
        
    def addCategoria(self, categoria):
        #adicionar uma categoria em self.tree
        self.tree.insert("", "end", values = (categoria))
        
    def getSelection(self):
        #retornar os valores que estão selecionados na coluna categoria
        values = [self.tree.item(categoria)["values"][0] for categoria in self.tree.selection()]
        return values
    

        
class FrameDisponibilidade(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        default = Default()
        self.configure(
            background = default.background
        )
        
        label = LabelDefault(self, text = "Disponibilidade")
        self.intCheck = IntVar(value = 1)
        checkButton = Checkbutton(self, variable = self.intCheck)
        checkButton.configure(
            background = default.background
        )
        
        self.pack(fill = "x", padx = 5, pady = 5)
        label.pack(side = "left", padx = 1, pady = 1)
        checkButton.pack(side = "left", padx = 1, pady = 1)
        
        label.bind("<Button-1>", self.labelClick)
    
    def labelClick(self, event):
        if self.intCheck.get():
            self.intCheck.set(0)
        else:
            self.intCheck.set(1)
     
class TelaCadastroLivro(Toplevel):
    def __init__(self, parent, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        
        default = Default()
        self.title("Toplevel novo livro")
        self.geometry("{}+550+20".format(default.geometry))
        self.configure(background = default.background)
        
        #criandos os widgets
        self.frameTitulo = FrameEntry(self, "Título")
        self.frameAutor = FrameEntry(self, "Autor")
        self.framePaginas = FrameEntry(self, "Páginas")
        self.frameCategoria = FrameCategoria(self)
        self.frameDisponibilidade = FrameDisponibilidade(self)
        
        #o botão de confirmação
        self.button = ttk.Button(self, text = "Confirmar")
        self.button.pack(padx = 5, pady = 5)
        self.button["command"] = lambda: self.buttonClick()
        
    def getValues(self):
        values = {}
        values["titulo"] = self.frameTitulo.getEntry().strip()
        values["autor"] = self.frameAutor.getEntry().strip()
        values["paginas"] = self.framePaginas.getEntry().strip()
        values["categoria"] = self.frameCategoria.getSelection() 
        return values
       
    def buttonClick(self):
        print("Cadastro")
        print(self.getValues())


class TelaAtualizarLivro(TelaCadastroLivro):
    def __init__(self, parent, *args, **kwargs):
        TelaCadastroLivro.__init__(self, parent, *args, **kwargs)
        self.title("Toplevel atualizar")
        self.button.configure(
            text = "Atualizar"
        )
    
    def buttonClick(self):
        print("Atualizar")
        print(self.getValues())

class TelaLivro(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        #cor de fundo
        default = Default()
        self.configure(
            background = default.background
        )
    
        #instanciando os widgets
        self.criarTree()
        self.criarButton(default)

        #chamando o método pack no momento da criação.
        self.pack(fill = "both", expand = True, padx = 5, pady = 5)
        self.pack_propagate(False)

    def criarTree(self):

        frame = Frame(self)
        self.tree = ttk.Treeview(frame)
        scrollX = Scrollbar(frame, command = self.tree.xview, orient = "horizont", width = 16 )
        scrollY = Scrollbar(frame, command = self.tree.yview, orient = "vertical", width = 16)
        self.tree.configure(
            xscrollcommand = scrollX.set,
            yscrollcommand = scrollY.set
        )

        self.tree["columns"] = ("idlivro", "titulo", "autor", "paginas", "categoria", "disponibilidade")
        self.tree.heading("idlivro", text = "id")
        self.tree.heading("titulo", text = "Título")
        self.tree.heading("autor", text = "Autor")
        self.tree.heading("paginas", text = "Páginas")
        self.tree.heading("categoria", text = "Categoria")
        self.tree.heading("disponibilidade", text = "Disponibilidade")

        self.tree.column("#0", width = 0, stretch = False)
        self.tree.column("idlivro", width = 50, minwidth = 50, stretch = False)
        self.tree.column("titulo", width  = 350)
        self.tree.column("autor", width = 250)
        self.tree.column("paginas", width = 100)
        self.tree.column("categoria", width = 150)
        self.tree.column("disponibilidade", width = 200, minwidth = 150)

        self.tree.tag_configure('disponivel', background = "green")
        self.tree.tag_configure("naodisponivel", background = "red")

        frame.pack(fill = "both", expand = True)
        frame.pack_propagate(False)
        scrollX.pack(side = "bottom", fill = "x")
        self.tree.pack(side = "left", fill = "both", expand = True)
        scrollY.pack(side = "left", fill = "y")

        #--apenas p/ testes--#
        self.tree.insert("", "end", values = (1 , "herry poter", "j.k rowling", 433, "fantasia", "Sim"), tag = 'disponivel')
        self.tree.insert("", "end", values = (2 , "herry poter", "j.k rowling", 433, "fantasia", "Não"), tag = 'naodisponivel')
        #--------------------#
    
    def criarButton(self, instancia_de_default):
        frame = Frame(self)
        frame.configure(
            background = instancia_de_default.background
        )
        buttonAdd = ttk.Button(frame, text = "+", width = 10)
        buttonRemove = ttk.Button(frame, text = "-", width = 10)

        frame.pack(fill = "x", padx = 5, pady = 5)
        buttonAdd.pack(side = "left", padx = 1, pady = 1)
        buttonRemove.pack(side = "right", padx = 1, pady = 1)
        
        #comandos
        buttonAdd["command"] = lambda: self.abrirFormularioNovoLivro()
        buttonRemove["command"] = lambda: self.removerLivro()
        self.tree.bind("<Double-Button-1>", lambda event: self.abrirFormularioAtualizarLivro(event))
    
    def abrirFormularioNovoLivro(self):
        TelaCadastroLivro(self)

    def abrirFormularioAtualizarLivro(self, event):
        itemSelecionado = self.tree.selection()
        if itemSelecionado:
            #obtendo os valores atuais 
            itemSelecionado = self.tree.item(self.tree.selection()[0])
            values = itemSelecionado["values"]
            idlivro = values[0]
            titulo = values[1]
            autor = values[2]
            paginas = values[3]
            disponibilidade = {"Sim": 1, "Não": 0}[values[5]]

            #instanciando TelaAtulizarLivro e definindo os valores dos campos
            telaAtualizar = TelaAtualizarLivro(self)
            telaAtualizar.frameTitulo.setEntry(titulo)
            telaAtualizar.frameAutor.setEntry(autor)
            telaAtualizar.framePaginas.setEntry(paginas)
            telaAtualizar.frameDisponibilidade.intCheck.set(disponibilidade)

    def removerLivro(self):
        print("removerlivro chamado")

        
#----------------------------------------------#        
        

def main():
    root = Tk()
    print(root.tk.call('info', 'patchlevel'))
    root.geometry("900x500+0+0")

    default = Default()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font = (None, 14, "bold"), rowheight = 25, fieldbackground = default.background)
    style.configure("Treeview.Heading", font = (None, 16, "bold"))
    style.configure(
            "TLabel",
            font = default.font,
            background = default.background,
            foreground = "white"
        )
    style.configure("TButton", font = (None, 12, "bold"))
  
    
    tela = TelaLivro(root)
    #tela = TelaCadastroLivro(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
