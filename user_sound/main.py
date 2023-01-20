from fastapi import FastAPI, Response
import uvicorn

from user_sound.v1 import users, audio

app = FastAPI()

app.include_router(users.router)
app.include_router(audio.router)

@app.get("/health")
async def health_check():
    return Response(status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)