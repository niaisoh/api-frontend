from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

class Store_request(BaseModel):
    statement : str
    # branch : int

class Stock_request(BaseModel):
    statement : str
    branch : int
