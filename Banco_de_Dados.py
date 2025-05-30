import sqlite3
import json
import os

class Db:
    def __init__(self, bank_name:str = None, table:str = None):
        os.makedirs("Log", exist_ok=True)
        self.log_path = os.path.join("Log","db_log.txt")
        
        if bank_name:
            if self.check_db(bank_name):
                self.bank_name = bank_name
                self.table = table
                self.connect(bank_name, table)
            else:
                self.log(f"Database {bank_name} does not exist.")
                raise Exception(f"Database {bank_name} does not exist.")
        
    def log(self, text:str):
        with open(self.log_path, "a") as file:
            file.write(str(text) + "\n")
    
    def check_db(self, bank_name:str):
        try:
            with open(bank_name, "r") as file:
                return True
        except Exception as ERROR:
            self.log(str(ERROR))
            return False
    
    def connect(self, bank_name:str, table:str):
        try:
            self.bank = sqlite3.connect(bank_name)
            self.cursor = self.bank.cursor()
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not self.cursor.fetchone():
                raise Exception(f"Table {table} does not exist in {bank_name}.")
        except Exception as ERROR:
            self.log(str(ERROR))
            pass
    
    def createBank(self, bank_name:str, table:str,columns:list):
        try:
            self.bank = sqlite3.connect(bank_name)
            self.cursor = self.bank.cursor()
            columnsName = columns
            temp =""
            for i in columns:
                type_ = " json_data," if "json" in i.lower() else " text,"
                temp += i + type_
            columns = temp[:-1]
            temp=""
            columns ="id integer primary key autoincrement, " + columns
            self.cursor.execute(f"create table if not exists {table} ({columns}) ")
            self.bank.commit()
            for index,i in enumerate(columnsName):
                if (index+1) != len(columnsName):
                    temp += i + ", "
                else:
                    temp += i 
            columnsName = temp
            if len(self.consultDB(table)) == 0:
                values = ("Null, " * len(columnsName.split(",")))[:-2]
                self.cursor.execute(f"INSERT INTO {table} ({columnsName}) VALUES ({values})")
                self.bank.commit()
                
        except Exception as ERROR: 
            self.log(str(ERROR))
            return ERROR

    def consultDB(self,table: str=None):
        if not table: table = self.table
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchall()
        except Exception as ERROR: return ERROR
        
    def Insert(self, columns:list, values:list, table:str=None):
        try:
            #_list = []
            for ind, i in enumerate(columns):
                if "json" in i.lower():
                    values[ind] = json.dumps(values[ind], ensure_ascii=False)

            values = ("".join([f"'{i}', " for i in values]))[:-2]
            columns = ("".join([f"{i}," for i in columns]))[:-1]
            if not table: table = self.table
                    
            self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
            self.bank.commit()
            return True
        except Exception as ERROR: 
            self.log(str(ERROR))
            return ERROR
                
    def Update(self,columns:list, values:list, whereID:int,table:str=None):
        if not table: table = self.table
        try:
            _list = []
            
            for index,column in enumerate(columns):
                if len(columns) != (index + 1):
                    if "json" in column.lower():
                        values[index] = json.dumps(values[index])
                        
                    _list.append( column + "=" + (f'"{values[index]}"') + ", ")
                else:
                    _list.append( column + "=" + (f'"{values[index]}"'))
            columns = ""
            for i in _list: 
                columns +=i
            print(columns)
            
            self.cursor.execute(f"UPDATE {table} SET {columns} WHERE id = {str(whereID)}")
            self.bank.commit()
        except Exception as ERROR:
            self.log("Update Funciton : " + str(ERROR))
            return ERROR
            
    def Delete(self,table:str,where:str):
        if not "=" in str(where): return False  
        self.cursor.execute(f"DELETE FROM {table} WHERE {where}")
        self.bank.commit()
    
    def closeDB(self):
        self.bank.close()

class start():
    
    def __init__(self, *args, **kwargs):
        db = Db()
        db.createBank("Xml_DB.sql", "data", ["chave_nfe","json_data"])
        valueDic = {"dev":"Felipe Rodrigues","contato":"felipesgs@proton.me"}
        chave, xml = valueDic['dev'], valueDic
        
        #db.log(db.Insert(columns=["chave_nfe","json_data"], values=[chave, xml], table="data"))
        db.Update(table="data", columns=["chave_nfe", "json_data"], values=[chave, xml], whereID=1)
        data = db.consultDB("data")
        db.log(data)
        db.closeDB()
        
        
if __name__ == "__main__":
    start()
        
