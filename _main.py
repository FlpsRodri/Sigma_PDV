from main_window import Window
import os

class app:
    def __init__(self):

        self.authenticate()
        self.master_variables()
        self.window = Window()
        
    def authenticate(self):
        try:
            self.db_file = os.getenv('MASTER_DB_FILE')
            self.password = os.getenv('MASTER_PASSWORD')
            if not self.db_file or not self.password:
                raise ValueError("Database file or password is not set in environment variables.")
        except Exception as e:
            print(f"An error occurred while authenticating: {e}")
            raise e

    def master_variables(self):
        
        try:
            self.db_file = ""
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