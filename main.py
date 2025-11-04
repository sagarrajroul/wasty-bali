from fastapi import FastAPI
from router import auth_router, form_router, volunteer_router, scan_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Small FastAPI App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include your routers
app.include_router(auth_router.router)
app.include_router(form_router.router)
app.include_router(volunteer_router.router)
app.include_router(scan_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI app!"}
