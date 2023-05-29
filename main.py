import logging
import openai
from typing import Optional
from conf.settings import (PATH_FILE_VACANTES,
                      PATH_FILE_USERS,
                      SHEET_NAME_VACANTES,
                      SHEET_NAME_RECO,
                      SHEET_NAME_USERS,
                      PATH_API_KEY)

from fastapi import FastAPI
from pydantic import BaseModel
from utils.db import Database
from utils.generate_recomendations import GenerateRecomendations

logging.basicConfig(filename='example.log', 
                    level=logging.INFO, 
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger()

openai.api_key_path = PATH_API_KEY
app = FastAPI()

vacantes_df = Database.read_data(PATH_FILE_VACANTES)
vacantes = vacantes_df.reset_index().fillna("").reset_index().to_dict('records')

users_df = Database.read_data(PATH_FILE_USERS)
users = users_df.reset_index().fillna("").to_dict('records')

class User(BaseModel):
    id_user: int
    country: str
    area: Optional[str] = ...
    subareas: Optional[str] = ...
    degrees: Optional[str] = ...
    wage_aspiration: str
    currency: str
    current_wage: Optional[str] = ...
    change_cities: Optional[str] = ...
    language: Optional[str] = ...
    years_experience: str
    months_experience: Optional[str] = ...
    wish_role_name: str
    work_modality: str
    hardskills: str

@app.get("/")
def read_root():
    log.info("Using test")
    return {"Hello": "Welcome to the best recommendations for job offers!"}


@app.get("/vacancies/")
async def read_vacancies(skip: int = 0, limit: int = 10, id_vac: int = None):
    if id_vac is not None:
        return [d for d in vacantes if d["index"] == id_vac][skip : skip + limit]
    else:
        return vacantes[skip : skip + limit]

@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 10, id_user: int = None):
    if id_user is not None:
        return [d for d in users if d["id_user"] == id_user][skip : skip + limit]
    else:
        return users[skip : skip + limit]

@app.post("/users/")
async def create_user(user: User):
    for us in users:
        if us["id_user"] ==user.id_user:
            return {"Error": "User ID already exists"}
    Database.write_user(PATH_FILE_USERS, SHEET_NAME_USERS, users, user.dict())
    return user

@app.get("/recommendations/")
async def generate_recommendations():
    gen = GenerateRecomendations(users, vacantes)
    recs = gen.generate_recommendations()
    log.info(recs.shape)
    log.info(recs.id_user.unique())
    Database.write_recommendations(PATH_FILE_USERS, SHEET_NAME_RECO, recs)
    return  {"Success": "The recommendations were written in database users file"}