from sqlalchemy import Column, Integer, String, Text, DateTime, UUID, Float, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    version = Column(String, default="1.0.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String, default="draft")  # draft, published, archived

    # Relationships
    modules = relationship("Module", back_populates="book", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(PG_UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    module_number = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    book = relationship("Book", back_populates="modules")
    chapters = relationship("Chapter", back_populates="module", cascade="all, delete-orphan")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(PG_UUID(as_uuid=True), ForeignKey("modules.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text)  # Markdown format
    learning_goals = Column(JSON)  # Array of strings
    chapter_number = Column(Integer, nullable=False)
    word_count = Column(Integer, default=0)
    reading_time = Column(Integer, default=1)  # in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    module = relationship("Module", back_populates="chapters")
    sections = relationship("Section", back_populates="chapter", cascade="all, delete-orphan")


class Section(Base):
    __tablename__ = "sections"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(PG_UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    title = Column(String)
    content = Column(Text)  # Markdown format
    section_number = Column(Integer, nullable=False)
    type = Column(String, default="text")  # text, code, diagram, exercise, summary
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    chapter = relationship("Chapter", back_populates="sections")


class ContentReference(Base):
    __tablename__ = "content_references"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(PG_UUID(as_uuid=True), nullable=False)  # Foreign key to various content entities
    source_type = Column(String, nullable=False)  # Book, Module, Chapter, Section
    reference_type = Column(String, default="citation")  # citation, cross_reference, related_topic
    target_id = Column(PG_UUID(as_uuid=True), nullable=False)
    target_type = Column(String, nullable=False)  # Book, Module, Chapter, Section
    confidence = Column(Float, default=0.0)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserQuery(Base):
    __tablename__ = "user_queries"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PG_UUID(as_uuid=True), nullable=False)
    query_text = Column(Text, nullable=False)
    query_embedding = Column(String)  # Vector as string representation
    user_id = Column(PG_UUID(as_uuid=True))  # Nullable for anonymous users
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    query_type = Column(String, default="factual")  # factual, conceptual, procedural, navigation


class QueryResponse(Base):
    __tablename__ = "query_responses"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(PG_UUID(as_uuid=True), ForeignKey("user_queries.id"), nullable=False)
    response_text = Column(Text, nullable=False)
    response_embedding = Column(String)  # Vector as string representation
    source_chunks = Column(JSON)  # Array of content references
    confidence = Column(Float, default=0.0)  # 0.0 to 1.0
    response_time = Column(Float)  # in milliseconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    query = relationship("UserQuery", back_populates="response")


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(PG_UUID(as_uuid=True), ForeignKey("user_queries.id"), nullable=False)
    response_id = Column(PG_UUID(as_uuid=True), ForeignKey("query_responses.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # -1 to 5
    feedback_text = Column(Text)
    feedback_type = Column(String, default="accuracy")  # accuracy, relevance, completeness, other
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    query = relationship("UserQuery")
    response = relationship("QueryResponse")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True))  # Nullable for anonymous users
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))  # Nullable
    session_data = Column(JSON)  # For tracking learning progress
    is_active = Column(Boolean, default=True)

    # Relationships
    queries = relationship("UserQuery", back_populates="session")


# Add back_populates relationships
UserQuery.session = relationship("UserSession", back_populates="queries")
UserQuery.response = relationship("QueryResponse", back_populates="query", uselist=False)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(PG_UUID(as_uuid=True), nullable=False)  # Foreign key to content entities
    content_type = Column(String, nullable=False)  # Book, Module, Chapter, Section
    chunk_text = Column(Text, nullable=False)
    chunk_embedding = Column(String)  # Vector as string representation
    chunk_index = Column(Integer, nullable=False)
    metadata = Column(JSON)  # Source, context, tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class VectorIndex(Base):
    __tablename__ = "vector_indexes"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    dimension = Column(Integer, nullable=False)
    metric = Column(String, default="cosine")  # cosine, euclidean, dot
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SearchLog(Base):
    __tablename__ = "search_logs"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(Text, nullable=False)
    query_embedding = Column(String)  # Vector as string representation
    results = Column(JSON)  # Array of result objects
    execution_time = Column(Float)  # in milliseconds
    user_id = Column(PG_UUID(as_uuid=True))  # Nullable
    session_id = Column(PG_UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulationEnvironment(Base):
    __tablename__ = "simulation_environments"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    framework = Column(String, default="gazebo")  # gazebo, unity, isaac_sim, custom
    config = Column(JSON)  # Framework-specific configuration
    status = Column(String, default="active")  # active, inactive, maintenance
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SimulationSession(Base):
    __tablename__ = "simulation_sessions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    environment_id = Column(PG_UUID(as_uuid=True), ForeignKey("simulation_environments.id"), nullable=False)
    user_id = Column(PG_UUID(as_uuid=True))  # Nullable
    session_id = Column(PG_UUID(as_uuid=True), nullable=False)
    parameters = Column(JSON)  # Simulation-specific parameters
    state = Column(JSON)  # Current simulation state
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))  # Nullable
    is_active = Column(Boolean, default=True)

    # Relationships
    environment = relationship("SimulationEnvironment")


class Source(Base):
    __tablename__ = "sources"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    authors = Column(JSON)  # Array of strings
    publication = Column(String)
    publication_date = Column(DateTime)
    url = Column(String)
    doi = Column(String)  # Nullable
    source_type = Column(String, default="academic_paper")  # academic_paper, book, documentation, blog, video, other
    access_date = Column(DateTime)
    abstract = Column(Text)  # Nullable
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Citation(Base):
    __tablename__ = "citations"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(PG_UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    content_id = Column(PG_UUID(as_uuid=True), nullable=False)  # Foreign key to content entities
    content_type = Column(String, nullable=False)  # Book, Module, Chapter, Section
    citation_text = Column(String, nullable=False)
    citation_type = Column(String, default="reference")  # direct_quote, paraphrase, reference, data_source
    page_numbers = Column(String)  # Nullable
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    source = relationship("Source")