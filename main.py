from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.router.student import user_router
from apis.router.classroom import classroom_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(classroom_router)


@app.get("/")
async def main():
    return {"message": "Hello World"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
