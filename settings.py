from pathlib import Path
import openai

# Constants data
PATH_DATA = Path(r"data")

PATH_FILE_VACANTES = PATH_DATA.joinpath("vacantes.xlsx")
PATH_FILE_USERS = PATH_DATA.joinpath("users.xlsx")
SHEET_NAME_VACANTES = "Sheet1"
SHEET_NAME_RECO = "Recomendaciones"
SHEET_NAME_USERS = "Raw Data"

# Constants model
EMBEDDING_MODEL = "text-embedding-ada-002"
PATH_API_KEY = r"/apikey/api_key.txt"

openai.api_key_path = PATH_API_KEY