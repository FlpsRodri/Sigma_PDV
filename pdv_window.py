from tkinter import *
from tkinter import messagebox, ttk
from main_config import config

class PdvWindow(config):
    def __init__(self, master=None):
        self.root = Tk()
        #self.root.state("zoomed")        
        #self.root.overrideredirect(True) # Uncomment to remove title bar
        self.prod_in_list =[{"name":"arroz", "price":"9,5", "qnt":1}, 
                            {"name":"feijão", "price":"7,5", "qnt":1},
                            {"name":"macarrão", "price":"4,5", "qnt":1},
                            {"name":"carne", "price":"20,0", "qnt":1.5}]
        self.load_config(master=self.root)
        self.window()
        
        self.root.mainloop()
        
    def anotations(self):
        #adiconar funcao nas configuraçoes de produtos, seja selecionavel a opção de produto comulativo ou não
        #adicionar opção de pagamento, se é dinheiro ou cartão
        pass
        
    def window(self):
        def frames():
            master = self.root
            
            right_frame = Frame(master, bg=self.main_bg, width=200)
            right_frame.pack(side=RIGHT, fill=Y, padx=10, pady=10)
            right_frame.config(bg="yellow")
            
            self.itens_frame = Frame(master, bg=master.cget("bg"))
            self.itens_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
            
            self.preview_frame = Frame(right_frame, bg=self.main_bg, width=400, height=300)
            self.preview_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
            self.preview_frame.config(bg="blue")
            
            self.entry_frame = Frame(right_frame, bg=self.main_bg, height=300)
            self.entry_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
            self.entry_frame.config(bg="green")
        
        def update_prod():
            for prod in self.prod_in_list:
                prod["name"] = prod["name"].capitalize()
                prod["price"] = prod["price"].replace(",", ".")
                prod["price"] = format(float(prod["price"]), ".2f")
                prod["price"] = prod["price"].replace(".", ",")
                prod["qnt"] = format(float(prod["qnt"]), ".3f")
                prod["qnt"] = prod["qnt"].replace(".", ",")
                name, qnt, price = prod["name"], prod["qnt"], prod["price"]
                self.list_prod.insert("", "end", values=(name, qnt, price))
            
        
        def remove_prod(event):
            selected_item = self.list_prod.selection()
            if selected_item:
                item_index = self.list_prod.index(selected_item)
                
                if messagebox.askyesno("Remover Produto", "Você tem certeza que deseja remover este produto?\n "+ self.prod_in_list[item_index]["name"]):
                    # Remove the item from the listbox and the product list
                    self.list_prod.delete(selected_item)
                    del self.prod_in_list[item_index]
        
        def itens_widgets():
            
            list_prod_frame = LabelFrame(self.itens_frame, text="Produtos", bg="#fff89b", font=self.main_font, width=400, height=500)
            list_prod_frame.pack(side=TOP, fill=BOTH, expand=True)
            btns_frame = LabelFrame(self.itens_frame, bg=self.main_bg, height=100)
            btns_frame.pack(side=TOP, fill=X, expand=True)
            
            columns = ("name", "qnt", "price")
            width_lim = {"name": 210, "qnt": 50, "price": 90}
            self.list_prod = ttk.Treeview(list_prod_frame, columns=("name", "qnt", "price"), show="headings")
            
            for col in columns:
                self.list_prod.heading(col, text=col.capitalize())
                self.list_prod.column(col, width=width_lim[col], minwidth=width_lim[col], stretch=False)
            
            update_prod()
            
            self.list_prod.pack(side=TOP, fill=BOTH, expand=True)
            self.list_prod.bind("<Delete>", remove_prod)
                
            
        def preview_widgets():
            pass
        def entry_widgets():
            pass
        
        frames()
        itens_widgets()
        preview_widgets()
        entry_widgets()
    

if __name__ == "__main__":
    
    pdv_window = PdvWindow()
    
    