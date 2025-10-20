import os
from Banco_de_Dados import Db
from tkinter import *
from tkinter import messagebox
from main_config import config
from PIL import Image, ImageTk
from pdv_window import PdvWindow
import XML_Read

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
        estoq_btn = button("ESTOQUE")
        estoq_btn.config(image=self.img_products, height=64, command=lambda: XML_Read.XML_READ())
        moviment_btn = button("MOVIMENTAÇÕES")
        moviment_btn.config(image=self.img_moviment, height=64)
        consult_vendas_btn = button("CONSULTA VENDAS")
        consult_vendas_btn.config(image=self.img_vendas, height=64)
        config_btn = button("CONFIGURAÇÕES")
        config_btn.config(image=self.img_config, height=64)
        fechamento_btn = button("FECHAMENTO")
        fechamento_btn.config(image=self.img_fechamento, height=64)
        pdv_btn = button("PDV")
        pdv_btn.config(image=self.img_pdv, height=64, command=lambda: PdvWindow(self.master))
        backup_btn = (button("BACKUP"))
        backup_btn.config(image=self.img_backup, height=64)
        backup_btn.config(command=self.master.quit)
    
    def image_main_upload(self):
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
        
        self.load_config(master=self.master)
        self.images_load()
        self.buttons()
        self.menuBar(self.master)
        
        self.master.state("zoomed")
        
    def menuBar(self, master):
        def sobre():
            messagebox.showinfo("Sobre", "PDV de frente de caixa\nDesenvolvido por: FelipeRodrigues\n Contato: Felipesgs@proton.me\nVersão 1.0")
        def instrucoes():
            topLevel_Info = Toplevel(master)
            topLevel_Info.title("Instruções")
            topLevel_Info.resizable(False,False)
            text = ("instruçoes para uso")
            Label(topLevel_Info, text=text, font="times 12", justify=LEFT).pack(pady=10, padx=30)
        menu_bar = Menu(master=master)
        
        help = Menu(menu_bar, tearoff=0)
        option = Menu(menu_bar, tearoff=0)
        option.add_command(label="Atualizar Dados", command=self.image_main_upload)
        option.add_separator()
        option.add_command(label="Sair", command=master.quit)
        help.add_command(label="Sobre", command=sobre)
        help.add_command(label="Instruções", command=instrucoes)
        
        menu_bar.add_cascade(label="Opções", menu=option)
        menu_bar.add_cascade(label="Ajuda", menu=help)
        master.config(menu=menu_bar)

    def update(self):
        try:
            db = Db(self.user, self.key)
            db.update()
            messagebox.showinfo("Atualização", "Dados atualizados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")

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