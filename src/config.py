from dotenv import load_dotenv
import os

# load_dotenv(dotenv_path="../.env")
load_dotenv()

class Config:
    BASEURL = os.getenv("BASEURL")
    APIKEY = os.getenv("APIKEY")
    MODEL = os.getenv("MODEL")
