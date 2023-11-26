from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

class Disc(BaseModel):
    Manufacturer: str
    Name: str
    Speed: float
    Glide: float
    Turn: float
    Fade: float
    Diameter: float
    Height: float
    RimDepth: float
    RimWidth: float

# Hardcoded path to the JSON file
json_file_path = "disc.json"

# Read existing data from the JSON file
try:
    with open(json_file_path, "r") as file:
        discs = json.load(file)
except FileNotFoundError:
    discs = []

# Helper function to write data to the JSON file
def _write_to_json_file(data):
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=2)

@app.post("/discs/", response_model=Disc)
def create_disc(disc: Disc):
    disc_dict = disc.dict()
    discs.append(disc_dict)
    _write_to_json_file(discs)
    return disc

@app.get("/discs/", response_model=List[Disc])
def read_discs():
    return discs

@app.get("/discs/{disc_id}", response_model=Disc)
def read_disc(disc_id: int):
    try:
        return discs[disc_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Disc not found")

@app.put("/discs/{disc_id}", response_model=Disc)
def update_disc(disc_id: int, disc: Disc):
    try:
        existing_disc = discs[disc_id]
        updated_disc = existing_disc.copy()
        updated_disc.update(disc.dict())
        discs[disc_id] = updated_disc
        _write_to_json_file(discs)
        return updated_disc
    except IndexError:
        raise HTTPException(status_code=404, detail="Disc not found")

@app.delete("/discs/{disc_id}", response_model=Disc)
def delete_disc(disc_id: int):
    try:
        deleted_disc = discs.pop(disc_id)
        _write_to_json_file(discs)
        return deleted_disc
    except IndexError:
        raise HTTPException(status_code=404, detail="Disc not found")

