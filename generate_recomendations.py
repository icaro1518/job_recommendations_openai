import pandas as pd
import numpy as np

class GenerateRecomendations():
    def __init__(self, users, vacantes):
        if isinstance(users, list):
            self.users = pd.DataFrame(users)
        else:
            self.users = users
        if isinstance(users, list):
            self.vacantes = pd.DataFrame(vacantes)
        else:
            self.vacantes = vacantes
        
    def generate_embeddings(self):
        pass
    
    def get_similarity(self):
        pass
         
    def generate_recommendations(self, n = 5):
        return self.generate_mock_recomendations(n)
    
    def generate_mock_recomendations(self, n = 5):
        mock_dataset = pd.DataFrame(self.users.index, columns = ["id_user"]).merge(pd.Series(list(range(n)), name = "id_jobs"), how = "cross")
        mock_dataset["similarity"] = np.random.rand(len(mock_dataset))
        return mock_dataset