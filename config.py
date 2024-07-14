import os
from flask import Flask

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:

    PORT: int = 5000
    HOST: str = "0.0.0.0"
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    OPENAI_KEY: str = os.environ.get('OPENAI_KEY')


class TestConfig(Config):

    TESTING = True

    ENV: str = "testing"

    @staticmethod
    def init_app(app: Flask) -> None:

        pass


class DevelopmentConfig(Config):

    ENV: str ="development"
    @staticmethod
    def init_app(app: Flask) -> None:

        from redis import Redis
        from openai import OpenAI

        app.redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

        app.open_ai_client = OpenAI(api_key=app.config['OPENAI_KEY'])


    @staticmethod
    def load_data(file_name:str):
        import csv
        from app.schema import ProductReview

        data_file = os.path.join(base_dir, f"data/{file_name}")

        with open(data_file) as f:

            reader = csv.reader(f)

            counter = 0

            for row in reader:
                # skip header
                if counter == 0:
                    counter += 1
                    continue

                yield ProductReview(
                    Id =row[0], 
                    productid=row[1], 
                    userid=row[2],
                    profilename=row[3], 
                    HelpfulnessNumerator=row[4], 
                    HelpfulnessDenominator=row[5], 
                    Score=row[6], 
                    Time=row[7], 
                    Summary=row[8],
                    Text=row[9],
                )

                print("Loading review: ", row[0])
                counter +=1

    
class ProductionConfig(Config):

    ENV: str = "production"

    @staticmethod
    def init_app(app) -> None:

        pass


environment = dict(
    default=DevelopmentConfig,
    development=DevelopmentConfig,
    testing=TestConfig,
    production=ProductionConfig
)