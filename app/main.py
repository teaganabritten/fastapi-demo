#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os

api = FastAPI()

@api.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Teagan"}

@api.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@api.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

@api.get("/square/{e}")
def square(e: float):
    return {"square": e ** 2}

@api.get("/cube/{f}")
def cube(f: int):
    return {"cube": f ** 3}

from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import mysql.connector

# Add CORS middleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins
    allow_methods=['*'],  # Allow all HTTP methods
    allow_headers=['*'],  # Allow all headers
)

# Database connection parameters
DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "uup3cy"

# Establish database connection
db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur = db.cursor()

@api.get('/genres')
async def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = [dict(zip(headers, result)) for result in results]
        return JSONResponse(content=json_data)
    except mysql.connector.Error as e:
        print("MySQL Error: ", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        cur.close()
        db.close()

@api.get('/songs')
async def get_songs():
    query = """
    SELECT 
        s.title,
        s.album,
        s.artist,
        s.year,
        CONCAT(s.file) AS file,
        CONCAT(s.image) AS image,
        g.genre AS genre
    FROM
        songs s
    JOIN
        genres g ON s.genre = g.genreid
    ORDER BY
        s.title;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = [dict(zip(headers, result)) for result in results]
        return JSONResponse(content=json_data)
    except mysql.connector.Error as e:
        print("MySQL Error: ", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        cur.close()
        db.close()
