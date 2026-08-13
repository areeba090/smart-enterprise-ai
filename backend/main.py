from fastapi import FastAPI

app = FastAPI(title="Smart Enterprise Resource AI")


@app.get("/")
def root():
    return {"message": "Smart Enterprise Resource AI Backend is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}