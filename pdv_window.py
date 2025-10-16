from tkinter import *
from tkinter import messagebox, ttk, simpledialog
from main_config import config

class PdvWindow(config):
    def __init__(self, master=None):
        self.root = Toplevel(master) if master else Tk()
        #self.root.state("zoomed")        
        #self.root.overrideredirect(True) # Uncomment to remove title bar
        self.prod_in_list =[{"name":"arroz", "price":"9,5", "qnt":1, "EAN":"7891234567890"},
                            {"name":"feijão preto", "price":"8,0", "qnt":1, "EAN":"7891234567891"},
                            {"name":"batata", "price":"3,0", "qnt":2, "EAN":"7891234567892"},
                            {"name":"tomate", "price":"5,0", "qnt":1.5, "EAN":"7891234567893"},
                            {"name":"cenoura", "price":"2,0", "qnt":3, "EAN":"7891234567894"},
                            {"name":"cebola", "price":"1200,5", "qnt":2, "EAN":"7891234567895"}]
        
        self.load_config(master=self.root, shurtcuts=True)
        self.window()
        self.shortcuts_set()
        
        self.root.mainloop()
        
    def shortcuts_set(self):
        def enter():
            widget = self.root.focus_get()
            if isinstance(widget, Button):
                widget.invoke()
        self.shortcuts.add_shortcut("F11", lambda: self.root.wm_attributes("-fullscreen", not self.root.attributes("-fullscreen")), allow_in_input=True)
        self.shortcuts.add_shortcut("F8", lambda: self.FINALIZE_FRAME.lift(), allow_in_input=True)
        self.shortcuts.add_shortcut("F9", lambda: self.PDV_FRAME.lift(), allow_in_input=True)
        self.shortcuts.add_shortcut("i", lambda: self.btn_remove_one.focus_set(), allow_in_input=True)
        self.shortcuts.add_shortcut("Enter", enter, allow_in_input=False)
        
    def anotations(self):
        #adiconar funcao nas configuraçoes de produtos, seja selecionavel a opção de produto comulativo ou não
        #adicionar opção de pagamento, se é dinheiro ou cartão
        pass
        
    def window(self):
        def frames():
            master = Frame(self.root, bg=self.main_bg, width=800, height=600)
            master.pack()
            self.PDV_FRAME = Frame(master, bg=self.main_bg)
            self.PDV_FRAME.place(relwidth=1, relheight=1, relx=0, rely=0)
            self.FINALIZE_FRAME = Frame(master, bg=self.main_bg)
            self.FINALIZE_FRAME.place(relwidth=1, relheight=1, relx=0, rely=0)
            self.PDV_FRAME.lift()
            right_frame = Frame(self.PDV_FRAME, bg=self.main_bg, width=200)
            right_frame.pack(side=RIGHT, fill=Y, padx=10, pady=10)
            right_frame.config(bg=self.main_bg)
            
            self.itens_frame = Frame(self.PDV_FRAME, bg=master.cget("bg"))
            self.itens_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
            
            self.preview_frame = LabelFrame(right_frame, bg=self.main_bg, width=400, height=300)
            self.preview_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
            self.preview_frame.config(bg="#ffffff")
            
            self.entry_frame = LabelFrame(right_frame, bg=self.main_bg, height=300)
            self.entry_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
            self.entry_frame.config(bg="#d1fcf0")
        
        def update_prod(delete_all:bool=False):
            if delete_all == "all":
                self.list_prod.delete(*self.list_prod.get_children())
                
            for i,prod in enumerate(self.prod_in_list):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                
                prod["name"] = prod["name"].capitalize()
                prod["price"] = prod["price"].replace(",", ".")
                prod["price"] = format(float(prod["price"]), ".2f")
                prod["qnt"] = format(float(prod["qnt"]), ".3f")
                name = prod["name"]
                qnt = self.locale.format_string("%.3f",float(prod["qnt"]), grouping=True, monetary=False)
                price = self.locale.format_string("%.2f", float(prod["price"]), grouping=True)
                self.list_prod.insert("", "end", values=(name, qnt, price), tags=(tag,))
        
        def remove_prod(event, amount="one"):
            
            if amount == "one":
                # Remove the selected item from the listbox and the product list
                selected_item = self.list_prod.selection()
                if selected_item:
                    item_index = self.list_prod.index(selected_item)
                    
                    if messagebox.askyesno("Remover Produto", "Você tem certeza que deseja remover este produto?\n "+ self.prod_in_list[item_index]["name"]):
                        # Remove the item from the listbox and the product list
                        del self.prod_in_list[item_index]
                        update_prod(delete_all=True)
                        
                else:
                    # If no item is selected, remove the last item in the list
                    selected_item = self.list_prod.get_children()[-1]
                    item_index = self.list_prod.index(selected_item)
                    if messagebox.askyesno("Remover Produto", "Você tem certeza que deseja remover este produto?\n "+ self.prod_in_list[item_index]["name"]):
                        self.list_prod.delete(selected_item)
                        del self.prod_in_list[item_index]
                
            elif amount == "all":
                if messagebox.askyesno("Remover Todos os Produtos", "Você tem certeza que deseja remover todos os produtos?"):
                    self.list_prod.delete(*self.list_prod.get_children())
                    self.prod_in_list.clear()
                    
        def alter_amount(event):
            selected_item = self.list_prod.selection()
            if selected_item:
                item_index = self.list_prod.index(selected_item)
                self.last_prod_name.set(value=self.prod_in_list[item_index]["name"])
                new_amount = simpledialog.askfloat("Alterar Quantidade", f"Digite a nova quantidade para {self.last_prod_name.get()}:", 
                                                   initialvalue=self.prod_in_list[item_index]["qnt"], parent=self.root)
                if new_amount is not None:
                    self.prod_in_list[item_index]["qnt"] = new_amount
                    self.list_prod.item(selected_item, values=(self.last_prod_name.get(), format(new_amount, ".3f").replace(".", ","), 
                                                                self.prod_in_list[item_index]["price"]))
            else:
                messagebox.showwarning("Nenhum Produto Selecionado", "Por favor, selecione um produto para alterar a quantidade.")
                    
        def itens_widgets():
            # Create the frames
            list_prod_frame = LabelFrame(self.itens_frame, text="Produtos", bg=self.main_bg, font=self.main_font, width=400, height=500)
            list_prod_frame.pack(side=TOP, fill=BOTH, expand=True)
            btns_frame = LabelFrame(self.itens_frame, bg=self.main_bg, height=100, font=self.main_font)
            btns_frame.pack(side=RIGHT, fill=BOTH, expand=True)

            #create the puducts list and treeview
            columns = ("Produto", "qnt", "Preço")
            width_lim = {"Produto": 150, "qnt": 50, "Preço": 90}
            self.list_prod = ttk.Treeview(list_prod_frame, columns=columns, show="headings")
            self.list_prod.tag_configure("evenrow", background="#f0f0f0")
            self.list_prod.tag_configure("oddrow", background="#ffffff")
            
            for col in columns:
                self.list_prod.heading(col, text=col.capitalize())
                self.list_prod.column(col, width=width_lim[col], minwidth=width_lim[col], stretch=False)
                if not col == "Produto":
                    self.list_prod.column(col, anchor=E)
            
            # Create a scrollbar for the list
            scrollbar = ttk.Scrollbar(list_prod_frame, orient=VERTICAL, command=self.list_prod.yview)
            self.list_prod.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=RIGHT, fill=Y)
            self.list_prod.pack(side=LEFT, fill=BOTH, expand=True)
            
            update_prod()
            self.list_prod.bind("<Delete>", remove_prod)
            
            #Buttons
            btn_list_prod_frame = LabelFrame(btns_frame, bg=self.main_bg, font=self.main_font)
            btn_list_prod_frame.pack(side=TOP, fill=BOTH, expand=True)
            self.btn_remove_one = Button(btn_list_prod_frame, text="Remover Produto", command=lambda: remove_prod(None), bg="#f0e10e", font=self.main_font)   
            self.btn_remove_one.pack(side=LEFT, padx=5, pady=5)
            btn_remove_all = Button(btn_list_prod_frame, text="Remover Todos", command=lambda: remove_prod(None, "all"), bg="#ff2424", font=self.main_font)
            btn_remove_all.pack(side=LEFT, padx=5, pady=5)
            
            bnt_alter_amount = Button(btns_frame, text="Alterar Quantidade", command=lambda: alter_amount(None), bg="#ffffff", font=self.main_font)
            bnt_alter_amount.pack(side=LEFT, padx=5, pady=5)
            btn_sorch = Button(btns_frame, text="Buscar Produto", command=lambda: self.PDV_FRAME.lift(), bg="#ffffff", font=self.main_font)
            btn_sorch.pack(side=LEFT, padx=5, pady=5)
            btn_finalize = Button(btns_frame, text="Finalizar", command=lambda: self.FINALIZE_FRAME.lift(), bg="#ffffff", font=self.main_font)
            btn_finalize.pack(side=LEFT, padx=5, pady=5)
            
        def preview_widgets():
            def update():
                if not self.prod_in_list:
                    self.last_prod_name.set(" ")
                    self.prod_name_view.config(text="")
                    self.value_total_view.config(text="R$ 0,00")
                    return
                value_total_sum = sum(float(value["price"].replace(",", ".")) * float(value["qnt"]) for value in self.prod_in_list)
                value_total_sum = self.locale.format_string("%.2f", value_total_sum, grouping=True)
                self.value_total.set(value = f"R$ {value_total_sum}")
                #self.last_prod_name.set(self.prod_in_list[-1]["name"].capitalize() if self.prod_in_list else " ")
                self.prod_name_view.config(text=self.last_prod_name.get().upper())
                last_prod_amount_value.set(value=f"{format(float(self.prod_in_list[-1]['qnt']), ".3f")} X R$ {self.locale.format_string('%.2f', float(self.prod_in_list[-1]['price'].replace(",", ".")), grouping=True)}")
                self.prod_name_view.after(100, update)
                
            bg = "#ffffff"
            font = "hevetica 14 bold"
            font_lgnd = "hevetica 12"
            wd = 20
            self.value_total = StringVar(value=f"R$ 0,00")
            Label(self.preview_frame, text="Total", bg=bg, font=font_lgnd, width=wd, anchor=W).grid(row=0, column=0, padx=5, pady=5, sticky=W)
            self.value_total_view = Label(self.preview_frame, text="", textvariable=self.value_total, bg=bg, font=font.replace("14","22"), bd=1, relief=SOLID, width=wd)
            self.value_total_view.grid(row=1, column=0, padx=5, pady=5, sticky=W+E, columnspan=2)
            Label(self.preview_frame, text="Ultimo Item", bg=bg, font=font_lgnd, width=wd, anchor=W).grid(row=2, column=0, padx=5, pady=5, sticky=W)
            self.prod_name_view = Label(self.preview_frame, text="", bg=bg, font=font, textvariable=self.last_prod_name, width=wd)
            self.prod_name_view.grid(row=3, column=0, padx=5, pady=5, sticky=W+E, columnspan=2)
            last_prod_amount_value = StringVar(value="0,000")
            last_prod_amount = Label(self.preview_frame, text="", textvariable=last_prod_amount_value, bg=bg, font=font, width=wd, anchor=W)
            last_prod_amount.grid(row=4, column=0, padx=5, pady=5, sticky=W)
            update()
            
        def entry_widgets():
            bg = "#d1fcf0"
            Label(self.entry_frame, text="Código Gtin/EAN", bg=bg, font=self.main_font+" bold").grid(row=0, column=0, padx=5, pady=5, sticky=W)
            self.entry_code = self.entry_configured(self.entry_frame, bg="#fff3b2", font=self.main_font, width=20, filter=["numbers","decimal"])
            self.entry_code.grid(row=1, column=0, padx=5, pady=5, sticky=W)
            Label(self.entry_frame, text="Quantidade", bg=bg, font=self.main_font+" bold").grid(row=2, column=0, padx=5, pady=5, sticky=W)
            self.entry_qnt = self.entry_configured(self.entry_frame, bg="#fff3b2", font=self.main_font, width=20, filter=["numbers","decimal"], limit_amount={",":1})
            self.entry_qnt.config(justify=RIGHT)
            self.entry_qnt.insert(0, "1")
            self.entry_qnt.grid(row=3, column=0, padx=5, pady=5, sticky=W)
            self.entry_code.focus_set()

        #main variables
        
        self.last_prod_name = StringVar(value=self.prod_in_list[-1]["name"].upper() if self.prod_in_list else " ")
        
        frames()
        itens_widgets()
        preview_widgets()
        entry_widgets()
    
    def entry_configured(self, master, width=20, font=None, bg="#fff3b2", filter : list = "All", exclude_keys: list = None, add_on_filter: str =None, limit_amount: dict = {}):
        if filter:
            if filter == "all":
                filter = ["numbers", "mathematical", "alphabetic", "special", "decimal", "letters_acentuated"]
            keys_filter = {
                "numbers": "0123456789",
                "mathematical": "+-*/%",
                "alphabetic": " abcçdefghijklmnopqrstuvwxyz",
                "special": "!@#$%^&*()_+=-`~[]{}|;:'\",.<>?/\\",
                "decimal": ".,",
                "letters_acentuated": "áàãâéèêíìîóòõôúùûç"
            }
            if keys_filter.get("alphabetic"): keys_filter["alphabetic"] += keys_filter["alphabetic"].upper()
            if keys_filter.get("letters_acentuated"): keys_filter["letters_acentuated"] += keys_filter["letters_acentuated"].upper()
            keys_allowed = "".join(keys_filter[i] for i in filter if i in keys_filter)
            if add_on_filter: keys_allowed += add_on_filter
            
            def validate_command(*args):
                Value = value.get()
                key_variable = ""
                for i in Value:
                    if exclude_keys and (i.lower() in exclude_keys.lower()):
                        continue
                    if i in keys_allowed:
                        key_variable += i
                    if i in limit_amount and key_variable.count(i) > limit_amount[i]: key_variable = key_variable[:-1] 
                            
                value.set(key_variable)
            
            value = StringVar(value="")
            value.trace("w", validate_command)
            entry = Entry(master=master, bg=bg, validate='key',textvariable=value)
        else:
            # Regular entry without validation
            entry = Entry(master=master, bg=bg)
        if not font: font = self.main_font
        #entry = Entry(master=master, bg=bg)
        entry.config(font=font, bg=bg, width=width)
        def enter(event):
            if not "treeview" in str(entry.tk_focusNext()):
                entry.tk_focusNext().focus_set()
                entry.tk_focusNext().selection_range(0, END)
            
        entry.bind("<Return>", enter)
        entry.bind("<Shift-Return>", lambda event: entry.tk_focusPrev().focus_set())
        return entry
        
if __name__ == "__main__":
    
    pdv_window = PdvWindow()
    
    