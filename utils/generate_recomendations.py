from tqdm import tqdm
import pandas as pd
import numpy as np
from model.embeddings_generator import EmbeddingsGenerator
from data.data_preprocessing import DataPreprocessing
from conf.settings import (
    EMBEDDING_CACHE_USERS_PATH, 
    EMBEDDING_CACHE_VACANCIES_PATH,
    PATH_VACANTES_TRADUCIDAS
)

from openai.embeddings_utils import (
    distances_from_embeddings,
    indices_of_nearest_neighbors_from_distances,
)
import logging

log = logging.getLogger()

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
            
    def data_processing(self):
        processing = DataPreprocessing(self.users, self.vacantes)
        processing.fill_na_data(self.users)
        self.vacantes["description"] = self.vacantes["description"].str.replace('\n',' ', regex=True) 
        self.vacantes["description"] = self.vacantes["description"].str.replace('\.', '\. ', regex = True)

        resultado_traduccion = processing.data_translation(self.vacantes["description"], PATH_VACANTES_TRADUCIDAS, self.vacantes["index"])
        self.vacantes = self.vacantes.merge(resultado_traduccion, left_on = "index", right_on="Llave")
        
    def generate_embeddings_users(self):
        prompt_embedding = "Area de trabajo : {} y {}, educación : {},\
        aspiración salarial : {}, disponibilidad de relocación : {},\
        idiomas : {}, años de experiencia : {}, nombre vacante deseada : {}, modalidad de trabajo : {}, habilidades : {}"
        
        self.users["prompt_embedding"] = self.users.apply(lambda x: prompt_embedding.format(x["area"], x["subareas"], x["degrees"], 
                                                                                    x["wage_aspiration"], x["change_cities"], 
                                                                                        x["language"], x["years_experience"],
                                                                                    x["wish_role_name"], x["work_modality"],
                                                                                    x["hardskills"]), axis=1)
        usuarios_para_embeddings = list(self.users["prompt_embedding"])
        gen_emb_users = EmbeddingsGenerator(EMBEDDING_CACHE_USERS_PATH)
        self.embeddings_users = gen_emb_users.generate_all_embeddings(usuarios_para_embeddings)
        self.dict_embeddings_users = gen_emb_users.generate_dict_embeddings(self.embeddings_users, self.users["id_user"])

        
    def generate_embeddings_vacancies(self):
        vacantes_para_embeddings = list(self.vacantes["Data traducida"].copy())
        gen_emb_vacancies = EmbeddingsGenerator(EMBEDDING_CACHE_VACANCIES_PATH)
        self.embeddings_vacancies = gen_emb_vacancies.generate_all_embeddings(vacantes_para_embeddings)
        self.dict_embeddings_vacancies = gen_emb_vacancies.generate_dict_embeddings(self.embeddings_vacancies, self.vacantes["index"])

    def get_similarity(self, n = 5):
        data_final = pd.DataFrame()
        id_users = list(self.dict_embeddings_users.keys())
        log.info("len(self.dict_embeddings_users)", len(self.dict_embeddings_users))
        log.info("id_users", id_users)
        for id in tqdm(id_users):
            log.info(id)
            query_embedding = self.dict_embeddings_users[id]
            # get distances between the source embedding and other embeddings (function from embeddings_utils.py)
            distances = distances_from_embeddings(query_embedding, self.dict_embeddings_vacancies.values(), distance_metric="cosine")
            # get indices of nearest neighbors (function from embeddings_utils.py)
            indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)[:n]

            distances_df = pd.DataFrame([dict(zip(indices_of_nearest_neighbors,distances))], index = ["match"]).T.reset_index()
            distances_df = distances_df.merge(self.vacantes[["index", "account executive", "description"]], on ="index")
            distances_df["id_user"] = id
            distances_df["prompt_user"] = self.users.loc[self.users.id_user == id, "prompt_embedding"].iloc[0]
            
            distances_df["match"] = 1 - distances_df["match"]
            
            distances_df = distances_df[["id_user", "prompt_user", "index","account executive", "description",  "match"]]
            data_final = pd.concat([data_final, distances_df], axis = 0)
        return data_final
         
    def generate_recommendations(self, n = 5):
        log.info("Data processing")
        self.data_processing()
        log.info("Embeddings Users")
        self.generate_embeddings_users()
        log.info("Data vacancies")
        self.generate_embeddings_vacancies()
        log.info("Get similarity")
        return self.get_similarity(n)
    