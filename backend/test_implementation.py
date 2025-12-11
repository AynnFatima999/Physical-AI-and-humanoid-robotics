#!/usr/bin/env python3
"""
Test script to validate the implementation of the AI-Native Robotics Book API
"""
import asyncio
import sys
from pathlib import Path
import uuid
from typing import Dict, Any

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from src import models, schemas, crud
from src.database import DATABASE_URL
from src.rag_service import rag_service

async def test_implementation():
    """Test the implementation by validating key functionality"""
    print("Testing AI-Native Robotics Book API Implementation...")

    engine = create_async_engine(DATABASE_URL)
    async with AsyncSession(engine) as db:
        # Test 1: Check if books exist and can be retrieved
        print("\n1. Testing book retrieval...")
        books = await crud.get_books(db, skip=0, limit=10)
        print(f"   Found {len(books)} books in the database")

        if books:
            book = books[0]  # Test with the first book
            print(f"   Successfully retrieved book: {book.title}")

            # Test 2: Check modules for the book
            print("\n2. Testing module retrieval...")
            modules = await crud.get_modules_by_book(db, book.id)
            print(f"   Found {len(modules)} modules for book {book.title}")

            # Test 3: Check chapters for the first module
            if modules:
                module = modules[0]
                chapters = await crud.get_chapters_by_module(db, module.id)
                print(f"   Found {len(chapters)} chapters for module {module.title}")

                # Test 4: Validate content indexing and validation
                print("\n3. Testing content validation and indexing...")
                try:
                    result = await rag_service.index_book_content(db, book.id)
                    print(f"   Successfully indexed book content: {result['chunks_indexed']} chunks")
                    if result['validation_issues']:
                        print(f"   Validation issues found: {len(result['validation_issues'])}")
                        for issue in result['validation_issues']:
                            print(f"     - {issue}")
                    else:
                        print("   No validation issues found")
                except Exception as e:
                    print(f"   Error during content indexing: {e}")

            # Test 5: Test RAG search functionality
            print("\n4. Testing RAG search functionality...")
            try:
                search_results = await rag_service.search("ROS 2 nodes and topics", max_results=3)
                print(f"   Search returned {len(search_results)} results for 'ROS 2 nodes and topics'")
                if search_results:
                    print(f"   First result score: {search_results[0]['score']:.3f}")
            except Exception as e:
                print(f"   Error during search: {e}")

            # Test 6: Test RAG query functionality
            print("\n5. Testing RAG query functionality...")
            try:
                rag_result = await rag_service.query_rag("What are ROS 2 nodes?", max_results=2)
                print(f"   RAG query completed with confidence: {rag_result['confidence']:.3f}")
                print(f"   Response time: {rag_result['response_time']:.3f}s")
                print(f"   Sources returned: {len(rag_result['sources'])}")
            except Exception as e:
                print(f"   Error during RAG query: {e}")

        else:
            print("   No books found in database - this may be expected if database is empty")

    await engine.dispose()
    print("\nImplementation testing completed!")

if __name__ == "__main__":
    asyncio.run(test_implementation())