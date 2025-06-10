import os
import locale
from keyboard_shortcuts import KeyboardShortcuts
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class config(object):
        
    def load_config(self, master=None, shurtcuts: bool = False):
        self.db_file = 'database.sql'
        self.db_table = 'data'
        
        self.main_bg = "#03A9B1"
        self.main_fg = '#333333'
        self.main_font = "Times 12"
        self.main_title = 'SPH - PDV 1.0'
        self.main_geometry = {'width': 800, 'height': 600, 'x': 100, 'y': 100}
        self.locale = locale
        
        if master:
            master.config(bg=self.main_bg)
            master.title(self.main_title)
            master.minsize(self.main_geometry['width'], self.main_geometry['height'])
            master.geometry(f"{self.main_geometry['width']}x{self.main_geometry['height']}+{self.main_geometry['x']}+{self.main_geometry['y']}")
            master.iconbitmap('icone.ico')
            if shurtcuts:
                self.shortcuts = KeyboardShortcuts(root=master)
            
        self.user = os.getenv('MASTER_USER', 'default_user')
        self.key = os.getenv('MASTER_KEY', 'default_key')
        
        
if __name__ == "__main__":
    run = config()