from main_window import Window
import os
from Banco_de_Dados import Db


class app:
    def __init__(self):

        self.authenticate()
        self.master_variables()
        self.window = Window()
        
    def authenticate(self):
        try:
            self.user = os.getenv('MASTER_USER')
            self.key = os.getenv('MASTER_KEY')
            
            if not self.user or not self.key:
                raise ValueError("Database file or password is not set in environment variables.")
        except Exception as e:
            print(f"An error occurred while authenticating: {e}")
            raise e

    def master_variables(self):
        
        try:
            self.db_file = os.getenv('DB_FILE', 'database.sql')
            self.db_table = os.getenv('DB_TABLE', 'data')
            self.user = ""
            self.password = ""
            self.main_bg= "#f0f0f0"
            self.main_fg = "#333333"
            self.main_font = ("Arial", 12)
            
            
        except Exception as e:
            print(f"An error occurred while setting master variables: {e}")
            raise e

if __name__ == "__main__":
    run = app()