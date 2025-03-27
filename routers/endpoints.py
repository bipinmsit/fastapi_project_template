from pydantic import BaseModel
from sqlalchemy import select
from utils.config.logger import logger
from fastapi import UploadFile, File, HTTPException, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from utils.crud import (
    get_stages,
    create_mail,
    get_pkstage,
    create_workflow,
    get_pk_mail,
)
from fastapi.responses import JSONResponse
import pgvector
from transformers import AutoTokenizer, AutoModel
import torch
from postgres.database import get_db
from models.models import Document

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}


# Load embedding model
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


def generate_embedding(text: str):
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embedding = model(**tokens).last_hidden_state.mean(dim=1)
    return embedding.numpy().tolist()


@router.post("/ingest/")
async def ingest_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    text = content.decode("utf-8")
    embedding = generate_embedding(text)

    doc = Document(content=text, embedding=embedding)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return {"id": doc.id, "content": doc.content}


@router.post("/query/")
async def query_document(query: str, db: Session = Depends(get_db)):
    query_embedding = generate_embedding(query)

    result = await db.execute(
        select(Document).order_by(Document.embedding.l2_distance(query_embedding))
    )
    doc = result.scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail="No relevant document found")

    return {"document": doc.content}


@router.get("/documents/")
async def list_documents(db: Session = Depends(get_db)):
    result = await db.execute(select(Document))
    return result.scalars().all()
