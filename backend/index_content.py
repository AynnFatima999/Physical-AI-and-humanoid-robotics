#!/usr/bin/env python3
"""
Script to index existing book content into the RAG system
"""
import asyncio
import os
import sys
from pathlib import Path
from uuid import UUID
import uuid

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from src import models, schemas, crud
from src.rag_service import rag_service
from src.database import DATABASE_URL

async def index_existing_books():
    """Index all existing books in the database"""
    engine = create_async_engine(DATABASE_URL)

    async with AsyncSession(engine) as db:
        # Get all books
        result = await db.execute(select(models.Book))
        books = result.scalars().all()

        print(f"Found {len(books)} books to index")

        for book in books:
            print(f"Indexing book: {book.title} (ID: {book.id})")
            try:
                chunks_count = await rag_service.index_book_content(db, book.id)
                print(f"  Indexed {chunks_count} chunks")
            except Exception as e:
                print(f"  Error indexing book {book.id}: {e}")

    await engine.dispose()
    print("Content indexing complete!")

if __name__ == "__main__":
    asyncio.run(index_existing_books())