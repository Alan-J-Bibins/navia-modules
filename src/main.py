from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"HOla": "NAVIA"}

@app.get("/health")
def checkhealth():
    return {"msg": "Server is running"}
