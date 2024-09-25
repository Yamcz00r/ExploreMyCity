from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello_world():
    return {
        "message": "Hello World!"
    }