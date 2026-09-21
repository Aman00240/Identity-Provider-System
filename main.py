from fastapi import FastAPI

app = FastAPI(title="Identity Provider")


@app.get("/health")
async def health_check():
    return {"status": "IdP is running"}
