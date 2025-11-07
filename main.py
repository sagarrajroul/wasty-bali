from fastapi import FastAPI
from router import auth_router, form_router, volunteer_router, scan_router, admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Small FastAPI App")
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://admin-wasty.netlify.app/", 
    "https://admin-wasty.netlify.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include your routers
app.include_router(auth_router.router)
app.include_router(form_router.router)
app.include_router(volunteer_router.router)
app.include_router(scan_router.router)
app.include_router(admin_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI app!"}
