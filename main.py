from fastapi import FastAPI
from router import auth_router, form_router

app = FastAPI(title="Small FastAPI App")

# Include your routers
app.include_router(auth_router.router)
app.include_router(form_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI app!"}
