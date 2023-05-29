from pathlib import Path
import openai

# Constants data
PATH_DATA = Path(r"data")

PATH_FILE_VACANTES = PATH_DATA.joinpath("vacantes2.xlsx")
PATH_FILE_USERS = PATH_DATA.joinpath("users2.xlsx")
SHEET_NAME_VACANTES = "Sheet1"
SHEET_NAME_RECO = "Recomendaciones"
SHEET_NAME_USERS = "Raw Data"

EMBEDDING_CACHE_USERS_PATH = PATH_DATA.joinpath("embeddings_vacancies2.pkl")
EMBEDDING_CACHE_VACANCIES_PATH = PATH_DATA.joinpath("embeddings_users2.pkl")

PATH_VACANTES_TRADUCIDAS = PATH_DATA.joinpath("vacantes_traducidas2.csv")

# Constants model
EMBEDDING_MODEL = "text-embedding-ada-002"
PATH_API_KEY = r"C:/Users/heile/Documents/Prueba Selección Hunty/apikey/api_key.txt"

openai.api_key_path = PATH_API_KEY