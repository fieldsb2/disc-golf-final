# discapi.py

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import Disc
import json

app = FastAPI()

origins = ["http://localhost:7112",
           "http://localhost:7112/discbag/inbag",
           "http://localhost:7112/discbag/inbag/",
           "http://localhost:7112/discbag"]  # Replace with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load existing data from disc.json
json_file_path = "disc.json"
try:
    with open(json_file_path, "r") as file:
        master_list = json.load(file)
except FileNotFoundError:
    master_list = []

# Bag to store discs temporarily
bag = []

# Helper function to write data to disc.json
def _write_to_json_file(data):
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=2)

# Master list routes
@app.get("/discs/", response_model=List[Disc])
def read_discs():
    return master_list

@app.get("/discs/{disc_name}", response_model=Disc)
def read_disc(disc_name: str):
    for disc in master_list:
        if disc["Name"] == disc_name:
            return disc
    raise HTTPException(status_code=404, detail="Disc not found")

@app.post("/discs/", response_model=Disc)
def create_disc(disc: Disc):
    print("Received payload:", disc.model_dump())
    disc_dict = disc.model_dump()
    if any(existing_disc["Name"] == disc_dict["Name"] for existing_disc in master_list):
        raise HTTPException(status_code=400, detail="Disc with this name already exists")
    master_list.append(disc_dict)
    _write_to_json_file(master_list)
    return disc

@app.put("/discs/{disc_name}", response_model=Disc)
def update_disc(disc_name: str, updated_disc: Disc):
    for disc in master_list:
        if disc["Name"] == disc_name:
            disc.update(updated_disc.dict())
            _write_to_json_file(master_list)
            return disc
    raise HTTPException(status_code=404, detail="Disc not found")

@app.delete("/discs/{disc_name}", response_model=Disc)
def delete_disc(disc_name: str):
    for disc in master_list:
        if disc["Name"] == disc_name:
            master_list.remove(disc)
            _write_to_json_file(master_list)
            return disc
    raise HTTPException(status_code=404, detail="Disc not found")


# Bag routes
@app.get("/inbag", response_model=List[Disc])
def read_discs_in_bag():
    print(f"Bag contents: {bag}")
    return bag




@app.post("/discs/inbag/{disc_name}", response_model=Disc)
def add_disc_to_bag(disc_name: str):
    print(f"Received request to add disc {disc_name} to the bag.")
    for disc in master_list:
        if disc["Name"] == disc_name:
            bag.append(disc)
            print(f"Disc {disc_name} added to the bag. Bag contents: {bag}")
            return disc
    raise HTTPException(status_code=404, detail=f"Disc {disc_name} not found")

@app.delete("/discs/inbag/{disc_name}", response_model=Disc)
def remove_disc_from_bag(disc_name: str):
    for disc in bag:
        if disc["Name"] == disc_name:
            bag.remove(disc)
            return disc
    raise HTTPException(status_code=404, detail="Disc not found in bag")

import logging

logging.basicConfig(level=logging.DEBUG)
