from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "ผมรักวิชานี้ SPCN19"}