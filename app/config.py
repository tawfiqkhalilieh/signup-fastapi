from pydantic import BaseSettings
class Settings(BaseSettings):

  endpoint_url: str = "http://localstack:4566"
  table : str = "table"
  verify: bool = False
  region_name: str = 'eu-central-1'
  aws_access_key_id: str = 'fake'
  aws_secret_access_key: str = 'fake'
  apikey:str= 'fake'

settings = Settings()