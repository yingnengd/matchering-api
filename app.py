from fastapi import FastAPI, UploadFile
import subprocess
import uuid
import os

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/master")
async def master(target: UploadFile, reference: UploadFile):
    tid = str(uuid.uuid4())
    os.makedirs("/tmp/audio", exist_ok=True)

    t_path = f"/tmp/audio/{tid}_target.wav"
    r_path = f"/tmp/audio/{tid}_ref.wav"
    o_path = f"/tmp/audio/{tid}_master.wav"

    with open(t_path, "wb") as f:
        f.write(await target.read())
    with open(r_path, "wb") as f:
        f.write(await reference.read())

    subprocess.run([
        "matchering",
        "--target", t_path,
        "--reference", r_path,
        "--output", o_path
    ], check=True)

    return {"output": o_path}
