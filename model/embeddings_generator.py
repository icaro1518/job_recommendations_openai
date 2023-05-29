from conf.settings import EMBEDDING_MODEL, PATH_API_KEY
import pandas as pd
import pickle
from openai.embeddings_utils import get_embedding
from tqdm import tqdm

class EmbeddingsGenerator:
    
    def __init__(self, embedding_cache_path, embedding_model: str =EMBEDDING_MODEL ) -> None:
        self.embedding_cache_path = embedding_cache_path
        self.model = embedding_model
        self.embedding_cache = self.load_cache_embeddings(embedding_cache_path)

    @staticmethod
    def load_cache_embeddings(embedding_cache_path):

        # load the cache if it exists, and save a copy to disk
        try:
            embedding_cache = pd.read_pickle(embedding_cache_path)
        except FileNotFoundError:
            embedding_cache = {}

        with open(embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(embedding_cache, embedding_cache_file)
            
        return embedding_cache
        
    def embedding_from_string(self,
        string: str
    ) -> list:
        
        """Return embedding of given string, using a cache to avoid recomputing."""
        if (string, self.model) not in self.embedding_cache.keys():
            self.embedding_cache[(string, self.model)] = get_embedding(string, self.model)
            
            with open(self.embedding_cache_path, "wb") as embedding_cache_file:
                pickle.dump(self.embedding_cache, embedding_cache_file)
        return self.embedding_cache[(string, self.model)]
    
    def generate_all_embeddings(self, data_para_embeddings : list):

        embeddings_final = []
        for data in tqdm(data_para_embeddings):

            embedding_data = self.embedding_from_string(data)
            embeddings_final.append(embedding_data)
            
        return embeddings_final
    
    def generate_dict_embeddings(self, embeddings, key:pd.Series):
        
        return dict(zip(key, embeddings))