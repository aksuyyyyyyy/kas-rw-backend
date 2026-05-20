from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import date
import os
from datetime import date
from typing import Optional

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="KAS RW Backend API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


class TransactionBase(BaseModel):
    tanggal: date
    keterangan: str
    jenis: str
    jumlah: float


class updateTransaksi(BaseModel):
    tanggal: Optional[date] = None
    keterangan: Optional[str] = None
    jenis: Optional[str] = None
    jumlah: Optional[float] = None


@app.get("/")
def root():
    return {"message": "Welcome to the KAS RW Backend API!"}


@app.post("/transaksi", status_code=201)
def create_transaksi(transaksi: TransactionBase):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO transaksi (tanggal, keterangan, jenis, jumlah)
        VALUES (%s, %s, %s, %s)
    """
    values = (
        transaksi.tanggal,
        transaksi.keterangan,
        transaksi.jenis,
        transaksi.jumlah,
    )
    cursor.execute(query, values)
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"message": "Transaction created successfully", "id": new_id}