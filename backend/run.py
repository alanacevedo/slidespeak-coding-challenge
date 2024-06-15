import uvicorn
import dotenv
import os

if __name__ == "__main__":
    dotenv.load_dotenv()
    uvicorn.run("app.main:app",
                host=os.getenv("API_HOST"),
                port=int(os.getenv("API_PORT")))
