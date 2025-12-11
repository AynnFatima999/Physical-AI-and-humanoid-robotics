from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
import json

# Base schemas
class BookBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    version: Optional[str] = "1.0.0"
    status: Optional[str] = "draft"  # draft, published, archived

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = None

class Book(BookBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Module schemas
class ModuleBase(BaseModel):
    book_id: UUID
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    module_number: int = Field(..., ge=1)

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=500)

class Module(ModuleBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Chapter schemas
class ChapterBase(BaseModel):
    module_id: UUID
    title: str = Field(..., min_length=5, max_length=200)
    content: Optional[str] = Field(None, min_length=500)  # Markdown format
    learning_goals: Optional[List[str]] = Field(None, min_items=1, max_items=5)
    chapter_number: int = Field(..., ge=1)
    word_count: Optional[int] = Field(0, ge=0)
    reading_time: Optional[int] = Field(1, ge=1)  # in minutes

class ChapterCreate(ChapterBase):
    pass

class ChapterUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    content: Optional[str] = Field(None, min_length=500)
    learning_goals: Optional[List[str]] = Field(None, min_items=1, max_items=5)
    word_count: Optional[int] = Field(None, ge=0)
    reading_time: Optional[int] = Field(None, ge=1)

class Chapter(ChapterBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Section schemas
class SectionBase(BaseModel):
    chapter_id: UUID
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None)  # Markdown format
    section_number: int = Field(..., ge=1)
    type: Optional[str] = "text"  # text, code, diagram, exercise, summary

class SectionCreate(SectionBase):
    pass

class SectionUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None)
    section_number: Optional[int] = Field(None, ge=1)
    type: Optional[str] = None

class Section(SectionBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Content Reference schemas
class ContentReferenceBase(BaseModel):
    source_id: UUID
    source_type: str  # Book, Module, Chapter, Section
    reference_type: str = "citation"  # citation, cross_reference, related_topic
    target_id: UUID
    target_type: str  # Book, Module, Chapter, Section
    confidence: Optional[float] = Field(0.0, ge=0.0, le=1.0)

class ContentReferenceCreate(ContentReferenceBase):
    pass

class ContentReference(ContentReferenceBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Source schemas
class SourceBase(BaseModel):
    title: str
    authors: Optional[List[str]] = []
    publication: Optional[str] = None
    publication_date: Optional[datetime] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    source_type: str = "academic_paper"  # academic_paper, book, documentation, blog, video, other
    access_date: Optional[datetime] = None
    abstract: Optional[str] = None

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    publication: Optional[str] = None
    publication_date: Optional[datetime] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    source_type: Optional[str] = None
    access_date: Optional[datetime] = None
    abstract: Optional[str] = None

class Source(SourceBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Citation schemas
class CitationBase(BaseModel):
    source_id: UUID
    content_id: UUID  # Foreign key to content entities
    content_type: str  # Book, Module, Chapter, Section
    citation_text: str
    citation_type: str = "reference"  # direct_quote, paraphrase, reference, data_source
    page_numbers: Optional[str] = None

class CitationCreate(CitationBase):
    pass

class Citation(CitationBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# User Session schemas
class UserSessionBase(BaseModel):
    user_id: Optional[UUID] = None  # Nullable for anonymous users
    session_data: Optional[Dict[str, Any]] = None

class UserSessionCreate(UserSessionBase):
    pass

class UserSession(UserSessionBase):
    id: UUID
    start_time: datetime
    end_time: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True

# User Query schemas
class UserQueryBase(BaseModel):
    session_id: UUID
    query_text: str = Field(..., min_length=3, max_length=1000)
    user_id: Optional[UUID] = None  # Nullable for anonymous users
    query_type: str = "factual"  # factual, conceptual, procedural, navigation

class UserQueryCreate(UserQueryBase):
    pass

class UserQuery(UserQueryBase):
    id: UUID
    query_embedding: Optional[str] = None  # Vector as string representation
    created_at: datetime

    class Config:
        from_attributes = True

# Query Response schemas
class QueryResponseBase(BaseModel):
    query_id: UUID
    response_text: str
    source_chunks: Optional[List[Dict[str, Any]]] = []  # Array of content references
    confidence: Optional[float] = Field(0.0, ge=0.0, le=1.0)
    response_time: Optional[float] = None  # in milliseconds

class QueryResponseCreate(QueryResponseBase):
    pass

class QueryResponse(QueryResponseBase):
    id: UUID
    response_embedding: Optional[str] = None  # Vector as string representation
    created_at: datetime

    class Config:
        from_attributes = True

# User Feedback schemas
class UserFeedbackBase(BaseModel):
    query_id: UUID
    response_id: UUID
    rating: int = Field(..., ge=-1, le=5)  # -1 to 5
    feedback_text: Optional[str] = None
    feedback_type: str = "accuracy"  # accuracy, relevance, completeness, other

class UserFeedbackCreate(UserFeedbackBase):
    pass

class UserFeedback(UserFeedbackBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Document Chunk schemas
class DocumentChunkBase(BaseModel):
    content_id: UUID  # Foreign key to content entities
    content_type: str  # Book, Module, Chapter, Section
    chunk_text: str = Field(..., min_length=50, max_length=1000)
    chunk_index: int
    metadata: Optional[Dict[str, Any]] = {}

class DocumentChunkCreate(DocumentChunkBase):
    pass

class DocumentChunkUpdate(BaseModel):
    chunk_text: Optional[str] = Field(None, min_length=50, max_length=1000)
    metadata: Optional[Dict[str, Any]] = None

class DocumentChunk(DocumentChunkBase):
    id: UUID
    chunk_embedding: Optional[str] = None  # Vector as string representation
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Vector Index schemas
class VectorIndexBase(BaseModel):
    name: str
    description: Optional[str] = None
    dimension: int
    metric: str = "cosine"  # cosine, euclidean, dot

class VectorIndexCreate(VectorIndexBase):
    pass

class VectorIndexUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    dimension: Optional[int] = None
    metric: Optional[str] = None

class VectorIndex(VectorIndexBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Search Log schemas
class SearchLogBase(BaseModel):
    query: str
    results: List[Dict[str, Any]]  # Array of result objects
    execution_time: float  # in milliseconds
    session_id: UUID
    user_id: Optional[UUID] = None  # Nullable

class SearchLogCreate(SearchLogBase):
    pass

class SearchLog(SearchLogBase):
    id: UUID
    query_embedding: Optional[str] = None  # Vector as string representation
    created_at: datetime

    class Config:
        from_attributes = True

# Simulation Environment schemas
class SimulationEnvironmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    framework: str = "gazebo"  # gazebo, unity, isaac_sim, custom
    config: Optional[Dict[str, Any]] = {}  # Framework-specific configuration
    status: str = "active"  # active, inactive, maintenance

class SimulationEnvironmentCreate(SimulationEnvironmentBase):
    pass

class SimulationEnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    framework: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class SimulationEnvironment(SimulationEnvironmentBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Simulation Session schemas
class SimulationSessionBase(BaseModel):
    environment_id: UUID
    session_id: UUID
    user_id: Optional[UUID] = None  # Nullable
    parameters: Optional[Dict[str, Any]] = {}  # Simulation-specific parameters
    state: Optional[Dict[str, Any]] = {}  # Current simulation state

class SimulationSessionCreate(SimulationSessionBase):
    pass

class SimulationSessionUpdate(BaseModel):
    parameters: Optional[Dict[str, Any]] = None
    state: Optional[Dict[str, Any]] = None

class SimulationSession(SimulationSessionBase):
    id: UUID
    start_time: datetime
    end_time: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True

# RAG Query schemas
class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
    session_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    max_results: Optional[int] = Field(5, ge=1, le=10)
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0)

class RAGQueryResponse(BaseModel):
    id: UUID
    query: str
    response: str
    sources: List[Dict[str, Any]]
    confidence: float
    response_time: float
    created_at: datetime

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    filters: Optional[Dict[str, Any]] = {}
    max_results: Optional[int] = Field(10, ge=1, le=20)
    min_score: Optional[float] = Field(0.5, ge=0.0, le=1.0)