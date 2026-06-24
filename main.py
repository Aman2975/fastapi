from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def read_test():
    return {"message": "Hello from FastAPI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
