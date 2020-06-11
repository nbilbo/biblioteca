from tkinter import *
from tkinter import ttk


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
        style = ttk.Style()
        style.configure(
            "TLabel",
            font = default.font,
            background = default.background,
            foreground = "white"
        )
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
        
        style = ttk.Style()
        style.configure("TButton", font = (None, 12))
        self.pack(side = "left", fill = "x", expand = True, padx = 5)


class FrameCategoria(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent,  *args, **kwargs),0
        
        default = Default()
        style = ttk.Style()
        style.configure("Categoria.Treeview", font = (None, 12), rowheight = 25)
        style.configure("Categoria.Treeview.Heading", font = (None, 11, "bold"))
        self.configure(
            height = 250,
            background = default.background
        )
        
        self.tree = ttk.Treeview(self, style = "Categoria.Treeview")
        scroll = Scrollbar(self, command = self.tree.yview)
        self.tree.configure(yscrollcommand = scroll.set)
        
        self.tree["columns"] = ("categorias")
        self.tree.heading("categorias", text = "Categorias")
        self.tree.column("#0", width = 0, stretch = False)
        
        self.pack(fill = "x", padx = 5, pady = 5)
        self.pack_propagate(False)
        self.tree.pack(side = "left", fill = "both", expand = True)
        scroll.pack(side = "left", fill = "y")
    
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
        self.title("Toplevel")
        self.geometry("{}+550+20".format(default.geometry))
        self.configure(background = default.background)
       
        style = ttk.Style()
        style.configure("TButton", font = (None, 12))
        
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
        
        self.button.configure(
            text = "Atualizar"
        )
    
    def buttonClick(self):
        print("Atualizar")
        print(self.getValues())
    
#----------------------------------------------#        
        

def main():
    root = Tk()
    root.geometry("500x500+0+0")
    
    tela = TelaAtualizarLivro(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()