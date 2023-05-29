import os
import pandas as pd

from utils.translator_new import TranslatorNew

class DataPreprocessing():
    
    def __init__(self, usuarios, vacantes):
        self.usuarios = usuarios
        self.vacantes = vacantes
        
        self.usuarios = self.fill_na_data(self.usuarios)
    
    @staticmethod
    def fill_na_data(usuarios : pd.DataFrame)->pd.DataFrame:
        usuarios["subareas"].fillna("", inplace = True)
        usuarios["degrees"].fillna("", inplace = True)
        usuarios["wage_aspiration"].fillna(0, inplace = True)
        usuarios["change_cities"].fillna("No desea reubicarse", inplace = True)
        usuarios["language"].fillna("", inplace = True)
        usuarios["years_experience"].fillna("Sin experiencia", inplace = True)
        usuarios["wish_role_name"].fillna("", inplace = True)
        usuarios["years_experience"].fillna("Sin experiencia", inplace = True)
        usuarios["years_experience"].fillna("Sin experiencia", inplace = True)
        usuarios.dropna(subset = ["hardskills"], inplace = True)
        
        return usuarios
    @staticmethod
    def data_translation(data:pd.Series, path_resultado:str, llave: pd.Series)->pd.DataFrame:
        
        if not os.path.exists(path_resultado):

            df_inicial = pd.DataFrame([{"Llave": "Llave",
                                        "Data original" : "Data original",
                                        "Data traducida" : "Data traducida"}])
            
            df_inicial.to_csv(path_resultado, header = None, index = False, encoding = "utf-8")
                
        translator = TranslatorNew()

        for i in range(len(data)):
        #for string in data:

            try:        
                translation = translator.Translate(data.iloc[i], dest_language_code = "es")
                df = pd.DataFrame([{"Llave": llave.iloc[i],
                                    "Data original" : data.iloc[i],
                                    "Data traducida" : translation}])
            except TypeError:
                df = pd.DataFrame([{"Llave": llave.iloc[i],
                                    "Data original" : data.iloc[i],
                                    "Data traducida" : "IMPOSIBLE DE TRADUCIR"}])
                
            # La API genera muchos fallos, por lo cual se va grabando continuamente
            df.to_csv(path_resultado, mode='a', index=False, header=False, encoding = "utf-8")
        
        resultado_traduccion = pd.read_csv(path_resultado)
        resultado_traduccion["Data traducida"] = resultado_traduccion["Data traducida"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        
        return resultado_traduccion        