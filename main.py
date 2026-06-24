from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def read_test():
    return {"message": "Hello from FastAPI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
