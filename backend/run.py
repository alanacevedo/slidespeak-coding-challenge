import dotenv
import os


if __name__ == "__main__":
    dotenv.load_dotenv()
    print(f"Python env is working, host: {os.getenv('API_HOST')}, port: {os.getenv("API_PORT")}")
