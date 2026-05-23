from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Koneksi Database
# =========================
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

# =========================
# Model Data
# =========================
class Transaksi(BaseModel):
    tanggal: date
    keterangan: str
    jenis: str
    jumlah: float

# =========================
# Root
# =========================
@app.get("/")
def root():
    return {
        "message": "Backend berjalan"
    }

# =========================
# GET Semua Transaksi
# =========================
@app.get("/transaksi")
def get_transaksi():

    db = get_db()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM transaksi ORDER BY tanggal DESC"
    )

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return data

# =========================
# POST Tambah Transaksi
# =========================
@app.post("/transaksi")
def tambah_transaksi(data: Transaksi):

    db = get_db()

    cursor = db.cursor()

    query = """
    INSERT INTO transaksi
    (tanggal, keterangan, jenis, jumlah)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (
        data.tanggal,
        data.keterangan,
        data.jenis,
        data.jumlah
    ))

    db.commit()

    cursor.close()
    db.close()

    return {
        "message": "Transaksi berhasil ditambahkan"
    }