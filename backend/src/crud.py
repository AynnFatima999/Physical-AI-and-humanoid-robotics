from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from . import models, schemas
from uuid import UUID
import uuid

# Book CRUD operations
async def create_book(db: AsyncSession, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_book(db: AsyncSession, book_id: UUID) -> Optional[models.Book]:
    result = await db.execute(
        select(models.Book).where(models.Book.id == book_id)
    )
    return result.scalar_one_or_none()

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Book]:
    result = await db.execute(
        select(models.Book).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_book(db: AsyncSession, book_id: UUID, book: schemas.BookUpdate) -> Optional[models.Book]:
    db_book = await get_book(db, book_id)
    if db_book:
        update_data = book.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        await db.commit()
        await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: UUID) -> bool:
    db_book = await get_book(db, book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
        return True
    return False

# Module CRUD operations
async def create_module(db: AsyncSession, module: schemas.ModuleCreate) -> models.Module:
    db_module = models.Module(**module.model_dump())
    db.add(db_module)
    await db.commit()
    await db.refresh(db_module)
    return db_module

async def get_module(db: AsyncSession, module_id: UUID) -> Optional[models.Module]:
    result = await db.execute(
        select(models.Module).where(models.Module.id == module_id)
    )
    return result.scalar_one_or_none()

async def get_modules_by_book(db: AsyncSession, book_id: UUID) -> List[models.Module]:
    result = await db.execute(
        select(models.Module).where(models.Module.book_id == book_id)
    )
    return result.scalars().all()

async def update_module(db: AsyncSession, module_id: UUID, module: schemas.ModuleUpdate) -> Optional[models.Module]:
    db_module = await get_module(db, module_id)
    if db_module:
        update_data = module.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_module, field, value)
        await db.commit()
        await db.refresh(db_module)
    return db_module

async def delete_module(db: AsyncSession, module_id: UUID) -> bool:
    db_module = await get_module(db, module_id)
    if db_module:
        await db.delete(db_module)
        await db.commit()
        return True
    return False

# Chapter CRUD operations
async def create_chapter(db: AsyncSession, chapter: schemas.ChapterCreate) -> models.Chapter:
    db_chapter = models.Chapter(**chapter.model_dump())
    db.add(db_chapter)
    await db.commit()
    await db.refresh(db_chapter)
    return db_chapter

async def get_chapter(db: AsyncSession, chapter_id: UUID) -> Optional[models.Chapter]:
    result = await db.execute(
        select(models.Chapter).where(models.Chapter.id == chapter_id)
    )
    return result.scalar_one_or_none()

async def get_chapters_by_module(db: AsyncSession, module_id: UUID) -> List[models.Chapter]:
    result = await db.execute(
        select(models.Chapter).where(models.Chapter.module_id == module_id)
    )
    return result.scalars().all()

async def update_chapter(db: AsyncSession, chapter_id: UUID, chapter: schemas.ChapterUpdate) -> Optional[models.Chapter]:
    db_chapter = await get_chapter(db, chapter_id)
    if db_chapter:
        update_data = chapter.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_chapter, field, value)
        await db.commit()
        await db.refresh(db_chapter)
    return db_chapter

async def delete_chapter(db: AsyncSession, chapter_id: UUID) -> bool:
    db_chapter = await get_chapter(db, chapter_id)
    if db_chapter:
        await db.delete(db_chapter)
        await db.commit()
        return True
    return False

# Section CRUD operations
async def create_section(db: AsyncSession, section: schemas.SectionCreate) -> models.Section:
    db_section = models.Section(**section.model_dump())
    db.add(db_section)
    await db.commit()
    await db.refresh(db_section)
    return db_section

async def get_section(db: AsyncSession, section_id: UUID) -> Optional[models.Section]:
    result = await db.execute(
        select(models.Section).where(models.Section.id == section_id)
    )
    return result.scalar_one_or_none()

async def get_sections_by_chapter(db: AsyncSession, chapter_id: UUID) -> List[models.Section]:
    result = await db.execute(
        select(models.Section).where(models.Section.chapter_id == chapter_id)
    )
    return result.scalars().all()

async def update_section(db: AsyncSession, section_id: UUID, section: schemas.SectionUpdate) -> Optional[models.Section]:
    db_section = await get_section(db, section_id)
    if db_section:
        update_data = section.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_section, field, value)
        await db.commit()
        await db.refresh(db_section)
    return db_section

async def delete_section(db: AsyncSession, section_id: UUID) -> bool:
    db_section = await get_section(db, section_id)
    if db_section:
        await db.delete(db_section)
        await db.commit()
        return True
    return False

# Source CRUD operations
async def create_source(db: AsyncSession, source: schemas.SourceCreate) -> models.Source:
    db_source = models.Source(**source.model_dump())
    db.add(db_source)
    await db.commit()
    await db.refresh(db_source)
    return db_source

async def get_source(db: AsyncSession, source_id: UUID) -> Optional[models.Source]:
    result = await db.execute(
        select(models.Source).where(models.Source.id == source_id)
    )
    return result.scalar_one_or_none()

async def get_sources(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Source]:
    result = await db.execute(
        select(models.Source).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_source(db: AsyncSession, source_id: UUID, source: schemas.SourceUpdate) -> Optional[models.Source]:
    db_source = await get_source(db, source_id)
    if db_source:
        update_data = source.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_source, field, value)
        await db.commit()
        await db.refresh(db_source)
    return db_source

async def delete_source(db: AsyncSession, source_id: UUID) -> bool:
    db_source = await get_source(db, source_id)
    if db_source:
        await db.delete(db_source)
        await db.commit()
        return True
    return False

# Citation CRUD operations
async def create_citation(db: AsyncSession, citation: schemas.CitationCreate) -> models.Citation:
    db_citation = models.Citation(**citation.model_dump())
    db.add(db_citation)
    await db.commit()
    await db.refresh(db_citation)
    return db_citation

async def get_citation(db: AsyncSession, citation_id: UUID) -> Optional[models.Citation]:
    result = await db.execute(
        select(models.Citation).where(models.Citation.id == citation_id)
    )
    return result.scalar_one_or_none()

async def get_citations_by_source(db: AsyncSession, source_id: UUID) -> List[models.Citation]:
    result = await db.execute(
        select(models.Citation).where(models.Citation.source_id == source_id)
    )
    return result.scalars().all()

async def get_citations_by_content(db: AsyncSession, content_id: UUID, content_type: str) -> List[models.Citation]:
    result = await db.execute(
        select(models.Citation).where(
            models.Citation.content_id == content_id,
            models.Citation.content_type == content_type
        )
    )
    return result.scalars().all()

# User Session CRUD operations
async def create_user_session(db: AsyncSession, session: schemas.UserSessionCreate) -> models.UserSession:
    db_session = models.UserSession(**session.model_dump())
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

async def get_user_session(db: AsyncSession, session_id: UUID) -> Optional[models.UserSession]:
    result = await db.execute(
        select(models.UserSession).where(models.UserSession.id == session_id)
    )
    return result.scalar_one_or_none()

async def update_user_session(db: AsyncSession, session_id: UUID, is_active: bool) -> Optional[models.UserSession]:
    result = await db.execute(
        update(models.UserSession)
        .where(models.UserSession.id == session_id)
        .values(is_active=is_active)
    )
    await db.commit()
    return await get_user_session(db, session_id)

# User Query CRUD operations
async def create_user_query(db: AsyncSession, query: schemas.UserQueryCreate) -> models.UserQuery:
    db_query = models.UserQuery(**query.model_dump())
    db.add(db_query)
    await db.commit()
    await db.refresh(db_query)
    return db_query

async def get_user_query(db: AsyncSession, query_id: UUID) -> Optional[models.UserQuery]:
    result = await db.execute(
        select(models.UserQuery).where(models.UserQuery.id == query_id)
    )
    return result.scalar_one_or_none()

# Query Response CRUD operations
async def create_query_response(db: AsyncSession, response: schemas.QueryResponseCreate) -> models.QueryResponse:
    db_response = models.QueryResponse(**response.model_dump())
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response

# User Feedback CRUD operations
async def create_user_feedback(db: AsyncSession, feedback: schemas.UserFeedbackCreate) -> models.UserFeedback:
    db_feedback = models.UserFeedback(**feedback.model_dump())
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

# Simulation Environment CRUD operations
async def create_simulation_environment(db: AsyncSession, env: schemas.SimulationEnvironmentCreate) -> models.SimulationEnvironment:
    db_env = models.SimulationEnvironment(**env.model_dump())
    db.add(db_env)
    await db.commit()
    await db.refresh(db_env)
    return db_env

async def get_simulation_environment(db: AsyncSession, env_id: UUID) -> Optional[models.SimulationEnvironment]:
    result = await db.execute(
        select(models.SimulationEnvironment).where(models.SimulationEnvironment.id == env_id)
    )
    return result.scalar_one_or_none()

async def get_simulation_environments(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.SimulationEnvironment]:
    result = await db.execute(
        select(models.SimulationEnvironment).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_simulation_environment(db: AsyncSession, env_id: UUID, env: schemas.SimulationEnvironmentUpdate) -> Optional[models.SimulationEnvironment]:
    db_env = await get_simulation_environment(db, env_id)
    if db_env:
        update_data = env.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_env, field, value)
        await db.commit()
        await db.refresh(db_env)
    return db_env

# Simulation Session CRUD operations
async def create_simulation_session(db: AsyncSession, session: schemas.SimulationSessionCreate) -> models.SimulationSession:
    db_session = models.SimulationSession(**session.model_dump())
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

async def get_simulation_session(db: AsyncSession, session_id: UUID) -> Optional[models.SimulationSession]:
    result = await db.execute(
        select(models.SimulationSession).where(models.SimulationSession.id == session_id)
    )
    return result.scalar_one_or_none()

async def update_simulation_session(db: AsyncSession, session_id: UUID, session_update: schemas.SimulationSessionUpdate) -> Optional[models.SimulationSession]:
    db_session = await get_simulation_session(db, session_id)
    if db_session:
        update_data = session_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)
        await db.commit()
        await db.refresh(db_session)
    return db_session