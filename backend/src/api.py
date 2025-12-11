from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict
from uuid import UUID
import uuid
from datetime import datetime
import logging

from . import crud, models, schemas
from .database import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Book endpoints
@router.post("/books", response_model=schemas.Book, tags=["books"])
async def create_book_endpoint(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    db_book = await crud.create_book(db, book)
    return db_book

@router.get("/books/{book_id}", response_model=schemas.Book, tags=["books"])
async def get_book_endpoint(book_id: UUID, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/books", response_model=List[schemas.Book], tags=["books"])
async def get_books_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    books = await crud.get_books(db, skip=skip, limit=limit)
    return books

@router.put("/books/{book_id}", response_model=schemas.Book, tags=["books"])
async def update_book_endpoint(
    book_id: UUID,
    book_update: schemas.BookUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_book = await crud.update_book(db, book_id, book_update)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/books/{book_id}", tags=["books"])
async def delete_book_endpoint(book_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# Module endpoints
@router.post("/modules", response_model=schemas.Module, tags=["modules"])
async def create_module_endpoint(module: schemas.ModuleCreate, db: AsyncSession = Depends(get_db)):
    # Verify the book exists
    db_book = await crud.get_book(db, module.book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_module = await crud.create_module(db, module)
    return db_module

@router.get("/modules/{module_id}", response_model=schemas.Module, tags=["modules"])
async def get_module_endpoint(module_id: UUID, db: AsyncSession = Depends(get_db)):
    db_module = await crud.get_module(db, module_id)
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module

@router.get("/books/{book_id}/modules", response_model=List[schemas.Module], tags=["modules"])
async def get_modules_by_book_endpoint(book_id: UUID, db: AsyncSession = Depends(get_db)):
    # Verify the book exists
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    modules = await crud.get_modules_by_book(db, book_id)
    return modules

@router.put("/modules/{module_id}", response_model=schemas.Module, tags=["modules"])
async def update_module_endpoint(
    module_id: UUID,
    module_update: schemas.ModuleUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_module = await crud.update_module(db, module_id, module_update)
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module

@router.delete("/modules/{module_id}", tags=["modules"])
async def delete_module_endpoint(module_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_module(db, module_id)
    if not success:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"message": "Module deleted successfully"}

# Chapter endpoints
@router.post("/chapters", response_model=schemas.Chapter, tags=["chapters"])
async def create_chapter_endpoint(chapter: schemas.ChapterCreate, db: AsyncSession = Depends(get_db)):
    # Verify the module exists
    db_module = await crud.get_module(db, chapter.module_id)
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")

    db_chapter = await crud.create_chapter(db, chapter)
    return db_chapter

@router.get("/chapters/{chapter_id}", response_model=schemas.Chapter, tags=["chapters"])
async def get_chapter_endpoint(chapter_id: UUID, db: AsyncSession = Depends(get_db)):
    db_chapter = await crud.get_chapter(db, chapter_id)
    if not db_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return db_chapter

@router.get("/modules/{module_id}/chapters", response_model=List[schemas.Chapter], tags=["chapters"])
async def get_chapters_by_module_endpoint(module_id: UUID, db: AsyncSession = Depends(get_db)):
    # Verify the module exists
    db_module = await crud.get_module(db, module_id)
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")

    chapters = await crud.get_chapters_by_module(db, module_id)
    return chapters

@router.put("/chapters/{chapter_id}", response_model=schemas.Chapter, tags=["chapters"])
async def update_chapter_endpoint(
    chapter_id: UUID,
    chapter_update: schemas.ChapterUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_chapter = await crud.update_chapter(db, chapter_id, chapter_update)
    if not db_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return db_chapter

@router.delete("/chapters/{chapter_id}", tags=["chapters"])
async def delete_chapter_endpoint(chapter_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_chapter(db, chapter_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {"message": "Chapter deleted successfully"}

# Section endpoints
@router.post("/sections", response_model=schemas.Section, tags=["sections"])
async def create_section_endpoint(section: schemas.SectionCreate, db: AsyncSession = Depends(get_db)):
    # Verify the chapter exists
    db_chapter = await crud.get_chapter(db, section.chapter_id)
    if not db_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    db_section = await crud.create_section(db, section)
    return db_section

@router.get("/sections/{section_id}", response_model=schemas.Section, tags=["sections"])
async def get_section_endpoint(section_id: UUID, db: AsyncSession = Depends(get_db)):
    db_section = await crud.get_section(db, section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    return db_section

@router.get("/chapters/{chapter_id}/sections", response_model=List[schemas.Section], tags=["sections"])
async def get_sections_by_chapter_endpoint(chapter_id: UUID, db: AsyncSession = Depends(get_db)):
    # Verify the chapter exists
    db_chapter = await crud.get_chapter(db, chapter_id)
    if not db_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    sections = await crud.get_sections_by_chapter(db, chapter_id)
    return sections

@router.put("/sections/{section_id}", response_model=schemas.Section, tags=["sections"])
async def update_section_endpoint(
    section_id: UUID,
    section_update: schemas.SectionUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_section = await crud.update_section(db, section_id, section_update)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    return db_section

@router.delete("/sections/{section_id}", tags=["sections"])
async def delete_section_endpoint(section_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_section(db, section_id)
    if not success:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"message": "Section deleted successfully"}

# Source endpoints
@router.post("/sources", response_model=schemas.Source, tags=["sources"])
async def create_source_endpoint(source: schemas.SourceCreate, db: AsyncSession = Depends(get_db)):
    db_source = await crud.create_source(db, source)
    return db_source

@router.get("/sources/{source_id}", response_model=schemas.Source, tags=["sources"])
async def get_source_endpoint(source_id: UUID, db: AsyncSession = Depends(get_db)):
    db_source = await crud.get_source(db, source_id)
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    return db_source

@router.get("/sources", response_model=List[schemas.Source], tags=["sources"])
async def get_sources_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    sources = await crud.get_sources(db, skip=skip, limit=limit)
    return sources

@router.put("/sources/{source_id}", response_model=schemas.Source, tags=["sources"])
async def update_source_endpoint(
    source_id: UUID,
    source_update: schemas.SourceUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_source = await crud.update_source(db, source_id, source_update)
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    return db_source

@router.delete("/sources/{source_id}", tags=["sources"])
async def delete_source_endpoint(source_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_source(db, source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"message": "Source deleted successfully"}

# Citation endpoints
@router.post("/citations", response_model=schemas.Citation, tags=["citations"])
async def create_citation_endpoint(citation: schemas.CitationCreate, db: AsyncSession = Depends(get_db)):
    # Verify the source exists
    db_source = await crud.get_source(db, citation.source_id)
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")

    db_citation = await crud.create_citation(db, citation)
    return db_citation

@router.get("/sources/{source_id}/citations", response_model=List[schemas.Citation], tags=["citations"])
async def get_citations_by_source_endpoint(source_id: UUID, db: AsyncSession = Depends(get_db)):
    # Verify the source exists
    db_source = await crud.get_source(db, source_id)
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")

    citations = await crud.get_citations_by_source(db, source_id)
    return citations

@router.get("/content/{content_id}/citations", response_model=List[schemas.Citation], tags=["citations"])
async def get_citations_by_content_endpoint(
    content_id: UUID,
    content_type: str,
    db: AsyncSession = Depends(get_db)
):
    citations = await crud.get_citations_by_content(db, content_id, content_type)
    return citations

# RAG endpoints
from .rag_service import rag_service

@router.post("/rag/query", response_model=schemas.RAGQueryResponse, tags=["rag"])
async def rag_query_endpoint(query_request: schemas.RAGQueryRequest, db: AsyncSession = Depends(get_db)):
    import time
    start_time = time.time()

    # Log the query first
    user_query = schemas.UserQueryCreate(
        session_id=query_request.session_id or uuid.uuid4(),
        query_text=query_request.query,
        user_id=query_request.user_id,
        query_type="factual"
    )
    created_query = await crud.create_user_query(db, user_query)

    # Call the actual RAG service
    rag_result = await rag_service.query_rag(
        query=query_request.query,
        max_results=query_request.max_results,
        temperature=query_request.temperature
    )

    # Create the response with the query ID
    query_response = schemas.QueryResponseCreate(
        query_id=created_query.id,
        response_text=rag_result["response"],
        source_chunks=rag_result["sources"],
        confidence=rag_result["confidence"],
        response_time=rag_result["response_time"]
    )
    created_response = await crud.create_query_response(db, query_response)

    # Create the response object
    response_obj = schemas.RAGQueryResponse(
        id=created_response.id,
        query=query_request.query,
        response=rag_result["response"],
        sources=rag_result["sources"],
        confidence=rag_result["confidence"],
        response_time=rag_result["response_time"],
        created_at=datetime.utcnow()
    )

    return response_obj

@router.post("/rag/search", response_model=List[Dict], tags=["rag"])
async def rag_search_endpoint(search_request: schemas.SearchRequest, db: AsyncSession = Depends(get_db)):
    # Call the actual RAG service for search
    search_results = await rag_service.search(
        query=search_request.query,
        max_results=search_request.max_results,
        filters=search_request.filters
    )

    # Format results to match expected response
    formatted_results = []
    for result in search_results:
        formatted_result = {
            "id": result["id"],
            "title": f"Content from {result['content_type']} {result['content_id']}",
            "content": result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"],
            "sourceType": result["content_type"],
            "score": result["score"],
            "metadata": result["metadata"]
        }
        formatted_results.append(formatted_result)

    return formatted_results

@router.post("/rag/index-book/{book_id}", tags=["rag"])
async def index_book_endpoint(book_id: UUID, db: AsyncSession = Depends(get_db)):
    """Index all content of a specific book in the vector database"""
    try:
        # Verify the book exists
        book = await crud.get_book(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # Index the book content
        result = await rag_service.index_book_content(db, book_id)
        chunks_count = result["chunks_indexed"]
        validation_issues = result["validation_issues"]

        response_data = {
            "message": f"Successfully indexed {chunks_count} content chunks from book {book_id}",
            "chunks_indexed": chunks_count
        }

        if validation_issues:
            response_data["validation_issues"] = validation_issues
            response_data["message"] += f" with {len(validation_issues)} validation issues found"

        return response_data
    except Exception as e:
        logger.error(f"Error indexing book: {e}")
        raise HTTPException(status_code=500, detail=f"Error indexing book: {str(e)}")

# Simulation endpoints
@router.post("/simulation/environments", response_model=schemas.SimulationEnvironment, tags=["simulation"])
async def create_simulation_environment_endpoint(
    env: schemas.SimulationEnvironmentCreate,
    db: AsyncSession = Depends(get_db)
):
    db_env = await crud.create_simulation_environment(db, env)
    return db_env

@router.get("/simulation/environments/{env_id}", response_model=schemas.SimulationEnvironment, tags=["simulation"])
async def get_simulation_environment_endpoint(env_id: UUID, db: AsyncSession = Depends(get_db)):
    db_env = await crud.get_simulation_environment(db, env_id)
    if not db_env:
        raise HTTPException(status_code=404, detail="Simulation environment not found")
    return db_env

@router.get("/simulation/environments", response_model=List[schemas.SimulationEnvironment], tags=["simulation"])
async def get_simulation_environments_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    environments = await crud.get_simulation_environments(db, skip=skip, limit=limit)
    return environments

@router.put("/simulation/environments/{env_id}", response_model=schemas.SimulationEnvironment, tags=["simulation"])
async def update_simulation_environment_endpoint(
    env_id: UUID,
    env_update: schemas.SimulationEnvironmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_env = await crud.update_simulation_environment(db, env_id, env_update)
    if not db_env:
        raise HTTPException(status_code=404, detail="Simulation environment not found")
    return db_env

@router.post("/simulation/sessions", response_model=schemas.SimulationSession, tags=["simulation"])
async def create_simulation_session_endpoint(
    session: schemas.SimulationSessionCreate,
    db: AsyncSession = Depends(get_db)
):
    # Verify the environment exists
    db_env = await crud.get_simulation_environment(db, session.environment_id)
    if not db_env:
        raise HTTPException(status_code=404, detail="Simulation environment not found")

    db_session = await crud.create_simulation_session(db, session)
    return db_session