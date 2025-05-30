import os
from Banco_de_Dados import Db
from tkinter import *
from main_config import config
from PIL import Image, ImageTk

class Window(config):
    def __init__(self):
        self.master = Tk()
        self.main_config()
        self.master.mainloop()
    
    def images_load(self):
        try:
            img_pdv = Image.open("images/pdv.png").resize((64, 64))
            self.img_pdv = ImageTk.PhotoImage(img_pdv)
            img_clientes = Image.open("images/clientes.png").resize((64, 64))
            self.img_clientes = ImageTk.PhotoImage(img_clientes)
            payments = Image.open("images/payment.png").resize((64, 64))
            self.img_payments = ImageTk.PhotoImage(payments)
            products = Image.open("images/products.png").resize((64, 64))
            self.img_products = ImageTk.PhotoImage(products)
            moviment = Image.open("images/moviment.png").resize((64, 64))
            self.img_moviment = ImageTk.PhotoImage(moviment)
            vendas = Image.open("images/vendas.png").resize((64, 64))
            self.img_vendas = ImageTk.PhotoImage(vendas)
            img_config = Image.open("images/config.png").resize((64, 64))
            self.img_config = ImageTk.PhotoImage(img_config)
            fechamento = Image.open("images/fechamento.png").resize((64, 64))
            self.img_fechamento = ImageTk.PhotoImage(fechamento)
            backup = Image.open("images/backup.png").resize((64, 64))
            self.img_backup = ImageTk.PhotoImage(backup)
            
        except Exception as e:
            print(f"Error loading image: {e}")
            
    def buttons(self):
        def button(text):
            btn = Button(self.toolbar_frame, text=text, height=2, font=self.main_font, fg=self.main_fg)
            btn.pack(side=LEFT)
            return btn
        
        clients_btn = button("CLIENTES")
        clients_btn.config(image=self.img_clientes, height=64)
        payments_btn = button("PAGAMENTOS")
        payments_btn.config(image=self.img_payments, height=64)
        products_btn = button("PRODUTOS")
        products_btn.config(image=self.img_products, height=64)
        moviment_btn = button("MOVIMENTAÇÕES")
        moviment_btn.config(image=self.img_moviment, height=64)
        consult_vendas_btn = button("CONSULTA VENDAS")
        consult_vendas_btn.config(image=self.img_vendas, height=64)
        config_btn = button("CONFIGURAÇÕES")
        config_btn.config(image=self.img_config, height=64)
        fechamento_btn = button("FECHAMENTO")
        fechamento_btn.config(image=self.img_fechamento, height=64)
        vendas_btn = button("PDV")
        vendas_btn.config(image=self.img_pdv, height=64)
        backup_btn = (button("BACKUP"))
        backup_btn.config(image=self.img_backup, height=64)
        backup_btn.config(command=self.master.quit)
        
    def Labels(self):
        pass
    
    def main_config(self):
        def frame():
            self.toolbar_frame = Frame(self.master, relief=SUNKEN, bd=1, )
            self.toolbar_frame.pack(fill=X, side="top")
            self.toolbar_frame.config(bg="lightgray")
            self.img_frame = Frame(self.master)
            self.img_frame.pack(side="top", fill="both" , expand=True, )
            self.img_frame.config(bg="orange")
        frame()
        
        self.load_config()
        self.images_load()
        self.buttons()
        self.master.title(self.main_title)
        self.master.minsize(self.main_geometry['width'], self.main_geometry['height'])
        self.master.geometry(f"{self.main_geometry['width']}x{self.main_geometry['height']}+{self.main_geometry['x']}+{self.main_geometry['y']}")  
        self.master.config(bg=self.main_bg)
        #self.master.iconbitmap('icon.ico')
        

class app():
    def __init__(self):
        
        
        self.authenticate()
        win = Window()
        
        
    def authenticate(self):
        try:
            self.user = os.getenv('MASTER_USER')
            self.key = os.getenv('MASTER_KEY')
            
            if not self.user or not self.key:
                raise ValueError("Database file or password is not set in environment variables.")
        except Exception as e:
            print(f"An error occurred while authenticating: {e}")
            raise e


if __name__ == "__main__":
    run = app()