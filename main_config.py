import os

class config(object):
        
    def load_config(self):
        self.db_file = 'database.sql'
        self.db_table = 'data'
        
        self.main_bg = '#f0f0f0'
        self.main_fg = '#333333'
        self.main_font = ('times', 12)
        self.main_title = 'SPH - PDV 1.0'
        self.main_geometry = {'width': 800, 'height': 600, 'x': 100, 'y': 100}
        
        self.user = os.getenv('MASTER_USER', 'default_user')
        self.key = os.getenv('MASTER_KEY', 'default_key')
        
        
if __name__ == "__main__":
    run = config()