import xml.etree.ElementTree as ET
import os
import json
from Banco_de_Dados import Db
from time import time

class XmlToDatabase:
    
    def __init__(self, bank_name:str, table:str, main_info:dict=None):

        self.bank_name = bank_name
        self.table = table
        self.main_info = {
            "CNPJ": ["07340876000126", "14269827000100"],
            "xNome": ["Helilton Teixeira de souza", "Aguilar e souza"]
        }
        #self.main_info = main_info

        self.dir = "NFE"
        self.dir_arq = "Arq"
        self.chave_list = []
        self.xml = []
        self.key_nfe = None
        self.log_path = os.path.join("Log","Log.txt")
        os.makedirs("Log", exist_ok=True)
        
        self.connect_bank()
        xmlList = self.get_filesName()

        for xml in xmlList:

            self.key_nfe = None
            json_data = self.xmlToJson(xml)
            json_dict = json.loads(json_data)
            json_data = json.dumps(json_dict, ensure_ascii=False)
            json_data = json_data.replace("'"," ")
            json_data = json_data.replace("{http://www.portalfiscal.inf.br/nfe}","")
            self.log("Xml convertido para json")
            json_dict = json.loads(json_data)
            self.log("Json convertido para dicionario")
            json_dict = self.get_only_xml(json_dict)
            if json_dict:
                if self.creat_resumed_xml_dict(json_dict=json_dict):
                    self.move_file_to_arq(xml)
                    #print("moved")

        self.db.closeDB()
        self.log("Importação finalizada")
        return
    
    def log(self, text:str):
        print(text)
        with open(self.log_path, "a") as file:
            file.write(text + "\n")
            
    def move_file_to_arq(self, file_name:str):
        try:
            os.makedirs("arq", exist_ok=True)
            if self.key_nfe in self.chave_list:
                self.log("File on the list")
                os.remove(f"{self.dir}\\{file_name}")
                self.log("removed file " + file_name)
                return False
            os.rename(f"{self.dir}/{file_name}", f"{self.dir_arq}/{file_name}")
            self.log("moveu")
        except Exception as ERROR:
            self.log("MOVE FILE TO ARQ : " + str(ERROR))
            return ERROR
        
    def creat_resumed_xml_dict(self, json_dict:dict):
        try:
            if json_dict:
                self.teste = json_dict
                ide = self.get_only_xml(xmlDict=json_dict, keyArg="ide")
                emit = self.get_only_xml(xmlDict=json_dict, keyArg="emit")
                det = self.get_only_xml(xmlDict=json_dict, keyArg="det")
                total = self.get_only_xml(xmlDict=json_dict, keyArg="total")
                dest = self.get_only_xml(xmlDict=json_dict, keyArg="dest")
                cobr = self.get_only_xml(xmlDict=json_dict, keyArg="cobr") if "cobr" in json_dict.keys() else None
                xml =  {"ide":ide, "emit":emit, "dest":dest, "det":det, "total":total, "cobr":cobr}
                key = "CNPJ" if "CNPJ" in emit.keys() else "CPF"
                if emit[key]["text"] in self.main_info["CNPJ"]:
                    #print(emit)
                    return True
                else:
                    self.insert_xml_in_db(self.key_nfe, xml)
                    return True
            return None
        except Exception as ERROR:
            self.log( "CREAT RESUMED XML DICT : " + str(ERROR))
            return False
    
    def insert_xml_in_db(self, chave_nfe:str, xml_dict:dict):
        self.log("inserindo no banco")
        try:
            #json_data = json.dumps(xml_dict, ensure_ascii=False)
            if not chave_nfe in self.chave_list:
                if self.db.Insert(table=self.table,columns= ["chave_nfe","json_data"],values=[chave_nfe, xml_dict]):
                    self.log("Inserido no banco "+chave_nfe)
                    return None
                return None
            return None

        except Exception as ERROR:
            self.log("INSERT XML IN DB : " + str(ERROR))
            return ERROR
        
    def get_only_xml(self, xmlDict:dict, keyArg:str=None):
        try:
            if keyArg:
                if keyArg in xmlDict.keys():
                    for i in xmlDict.keys():
                        if keyArg in i:
                            return xmlDict[i]
                else:
                    k = list(xmlDict.keys())[0]
                    return self.get_only_xml(xmlDict=xmlDict[k],keyArg=keyArg)

            if list(xmlDict.keys())[0] == "nfeProc":
                self.key_nfe = xmlDict["nfeProc"]["protNFe"]["infProt"]["chNFe"]["text"]
                return self.get_only_xml(xmlDict["nfeProc"])
            
            return xmlDict["NFe"]
            
        except Exception as ERROR:
            self.log("GET ONLY XML : " + str(ERROR))
            print(xmlDict.keys(), keyArg)
            print(self.teste)
            return False
    
    def connect_bank(self):
        
        self.db = Db()
        self.db.createBank(bank_name=self.bank_name, table=self.table, columns=["chave_nfe","json_data"])
        self.db.Update(table=self.table, columns= ["chave_nfe","json_data"], values=["Dev:FelipeRodrigues", "Contato:felipesgs@proton.me"],whereID=1)
        #self.db.Delete(self.table,"id=2")
        data_base_value = self.db.consultDB("data")

        for value in data_base_value:
            id = value[0]
            if int(id) > 1:
                
                xml = value[2]
                #self.db.Update(table=self.table, columns=["json_data"], values=[xml], whereID=id)
                
                xml = json.loads(xml)
                
                chave = value[1]
                if chave == "None":
                    chave = xml["ide"]["chNFe"]["text"]
                    self.db.Update(table=self.table, columns=["chave_nfe"],values=[chave],whereID=id)
                    self.log(chave)
                    self.log("Update #2")
                self.chave_list.append(chave)
                self.xml.append(xml)
            
    def get_filesName(self):
        try:
            xmlList = os.listdir(self.dir)
            xmlList = [file for file in xmlList if (file.endswith('.xml') or file.endswith('.XML'))]
            return xmlList
        except Exception as ERROR:
            self.log("GET FILES NAME : " + str(ERROR))
            return ERROR

    def xmlToJson(self, xml:str):
        try:
            tree = ET.parse(f'{self.dir}/{xml}')
            root = tree.getroot()
            xml_dict = {root.tag: self._element_to_dict(root)}
            json_data = json.dumps(xml_dict, ensure_ascii=False)
            return json_data
        except Exception as ERROR:
            self.log("XML TO JSON : " + str(ERROR))
            return ERROR

    def _element_to_dict(self, element):
        node = {}
        if element.text:
            node['text'] = element.text.strip()
        for child in element:
            child_dict = self._element_to_dict(child)
            if child.tag not in node:
                node[child.tag] = child_dict
            else:
                if not isinstance(node[child.tag], list):
                    node[child.tag] = [node[child.tag]]
                node[child.tag].append(child_dict)
        return node


if __name__ == '__main__':
    Time = time()
    XmlToDatabase("Xml_DB.sql", "data")
    print(time()-Time)
    