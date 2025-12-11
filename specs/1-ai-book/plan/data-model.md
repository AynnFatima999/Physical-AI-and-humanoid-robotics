# Data Model: AI-Native Software Development Book

## 1. Content Entities

### Book
- **Fields**:
  - id: UUID (primary key)
  - title: String
  - description: Text
  - version: String
  - createdAt: DateTime
  - updatedAt: DateTime
  - status: Enum ['draft', 'published', 'archived']

### Module
- **Fields**:
  - id: UUID (primary key)
  - bookId: UUID (foreign key to Book)
  - title: String
  - description: Text
  - moduleNumber: Integer
  - createdAt: DateTime
  - updatedAt: DateTime

### Chapter
- **Fields**:
  - id: UUID (primary key)
  - moduleId: UUID (foreign key to Module)
  - title: String
  - content: Text (Markdown format)
  - learningGoals: JSON array of strings
  - chapterNumber: Integer
  - wordCount: Integer
  - readingTime: Integer (minutes)
  - createdAt: DateTime
  - updatedAt: DateTime

### Section
- **Fields**:
  - id: UUID (primary key)
  - chapterId: UUID (foreign key to Chapter)
  - title: String
  - content: Text (Markdown format)
  - sectionNumber: Integer
  - type: Enum ['text', 'code', 'diagram', 'exercise', 'summary']
  - createdAt: DateTime
  - updatedAt: DateTime

### ContentReference
- **Fields**:
  - id: UUID (primary key)
  - sourceId: UUID (foreign key to various content entities)
  - sourceType: Enum ['Book', 'Module', 'Chapter', 'Section']
  - referenceType: Enum ['citation', 'cross_reference', 'related_topic']
  - targetId: UUID
  - targetType: Enum ['Book', 'Module', 'Chapter', 'Section']
  - confidence: Float (0.0-1.0)
  - createdAt: DateTime

## 2. User Interaction Entities

### UserQuery
- **Fields**:
  - id: UUID (primary key)
  - sessionId: UUID
  - queryText: Text
  - queryEmbedding: Vector (for similarity search)
  - userId: UUID (nullable for anonymous users)
  - createdAt: DateTime
  - queryType: Enum ['factual', 'conceptual', 'procedural', 'navigation']

### QueryResponse
- **Fields**:
  - id: UUID (primary key)
  - queryId: UUID (foreign key to UserQuery)
  - responseText: Text
  - responseEmbedding: Vector (for similarity search)
  - sourceChunks: JSON array of content references
  - confidence: Float (0.0-1.0)
  - responseTime: Float (milliseconds)
  - createdAt: DateTime

### UserFeedback
- **Fields**:
  - id: UUID (primary key)
  - queryId: UUID (foreign key to UserQuery)
  - responseId: UUID (foreign key to QueryResponse)
  - rating: Integer (-1 to 5)
  - feedbackText: Text
  - feedbackType: Enum ['accuracy', 'relevance', 'completeness', 'other']
  - createdAt: DateTime

### UserSession
- **Fields**:
  - id: UUID (primary key)
  - userId: UUID (nullable for anonymous users)
  - startTime: DateTime
  - endTime: DateTime (nullable)
  - sessionData: JSON (for tracking learning progress)
  - isActive: Boolean

## 3. RAG System Entities

### DocumentChunk
- **Fields**:
  - id: UUID (primary key)
  - contentId: UUID (foreign key to content entities)
  - contentType: Enum ['Book', 'Module', 'Chapter', 'Section']
  - chunkText: Text
  - chunkEmbedding: Vector
  - chunkIndex: Integer
  - metadata: JSON (source, context, tags)
  - createdAt: DateTime
  - updatedAt: DateTime

### VectorIndex
- **Fields**:
  - id: UUID (primary key)
  - name: String
  - description: Text
  - dimension: Integer
  - metric: Enum ['cosine', 'euclidean', 'dot']
  - createdAt: DateTime
  - updatedAt: DateTime

### SearchLog
- **Fields**:
  - id: UUID (primary key)
  - query: Text
  - queryEmbedding: Vector
  - results: JSON array of result objects
  - executionTime: Float (milliseconds)
  - userId: UUID (nullable)
  - sessionId: UUID
  - createdAt: DateTime

## 4. Simulation Integration Entities

### SimulationEnvironment
- **Fields**:
  - id: UUID (primary key)
  - name: String
  - description: Text
  - framework: Enum ['gazebo', 'unity', 'isaac_sim', 'custom']
  - config: JSON (framework-specific configuration)
  - status: Enum ['active', 'inactive', 'maintenance']
  - createdAt: DateTime
  - updatedAt: DateTime

### SimulationSession
- **Fields**:
  - id: UUID (primary key)
  - environmentId: UUID (foreign key to SimulationEnvironment)
  - userId: UUID (nullable)
  - sessionId: UUID
  - parameters: JSON (simulation-specific parameters)
  - state: JSON (current simulation state)
  - startTime: DateTime
  - endTime: DateTime (nullable)
  - isActive: Boolean

## 5. Source and Citation Entities

### Source
- **Fields**:
  - id: UUID (primary key)
  - title: String
  - authors: JSON array of strings
  - publication: String
  - publicationDate: Date
  - url: String
  - doi: String (nullable)
  - sourceType: Enum ['academic_paper', 'book', 'documentation', 'blog', 'video', 'other']
  - accessDate: Date
  - abstract: Text (nullable)
  - createdAt: DateTime

### Citation
- **Fields**:
  - id: UUID (primary key)
  - sourceId: UUID (foreign key to Source)
  - contentId: UUID (foreign key to content entities)
  - contentType: Enum ['Book', 'Module', 'Chapter', 'Section']
  - citationText: String
  - citationType: Enum ['direct_quote', 'paraphrase', 'reference', 'data_source']
  - pageNumbers: String (nullable)
  - createdAt: DateTime

## 6. Validation Rules

### Content Validation
- Book title: Required, minimum 5 characters, maximum 200 characters
- Module description: Required, minimum 10 characters, maximum 500 characters
- Chapter content: Required, minimum 500 words, maximum 5000 words
- Learning goals: Required, minimum 1 goal, maximum 5 goals per chapter
- Section type: Must be one of allowed enum values

### User Interaction Validation
- Query text: Required, minimum 3 characters, maximum 1000 characters
- Rating: Must be between -1 and 5 inclusive
- Session data: Must be valid JSON format

### RAG System Validation
- Chunk text: Required, minimum 50 characters, maximum 1000 characters
- Embedding dimension: Must match configured vector index dimension
- Confidence score: Must be between 0.0 and 1.0 inclusive

### Simulation Validation
- Environment config: Must be valid JSON format
- Parameters: Must be valid JSON format
- State: Must be valid JSON format

## 7. State Transitions

### Content States
- Book: draft → published → archived (linear progression)
- Chapter: draft → review → published → deprecated

### Session States
- UserSession: active → ended (based on timeout or explicit end)
- SimulationSession: initializing → active → paused → ended

## 8. Relationships

### Content Hierarchy
- Book (1) → (Many) Module
- Module (1) → (Many) Chapter
- Chapter (1) → (Many) Section

### Interaction Relationships
- UserSession (1) → (Many) UserQuery
- UserQuery (1) → (1) QueryResponse
- QueryResponse (1) → (Many) UserFeedback

### RAG Relationships
- DocumentChunk (Many) → (1) VectorIndex
- SearchLog (Many) → (1) VectorIndex

### Citation Relationships
- Source (1) → (Many) Citation
- Citation (Many) → (Many) Content entities (via contentId)