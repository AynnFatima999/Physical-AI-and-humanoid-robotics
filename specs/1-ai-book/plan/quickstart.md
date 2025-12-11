# Quickstart Guide: AI-Native Software Development Book

## Overview

This guide provides a quick overview of setting up and running the AI-Native Software Development book project. The project consists of a Docusaurus-based book with integrated RAG (Retrieval-Augmented Generation) capabilities.

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- Docker and Docker Compose
- Git
- Access to OpenAI API (for RAG features)

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Node.js Dependencies

```bash
cd docusaurus
npm install
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
NEON_POSTGRES_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname

# Vector Database Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key

# Application Configuration
APP_ENV=development
PORT=3000
API_BASE_URL=http://localhost:3000/api
```

## Running the Application

### 1. Start Backend Services

```bash
# Start Neon Postgres (if running locally)
docker-compose up -d postgres

# Start Qdrant vector database
docker-compose up -d qdrant

# Start FastAPI backend
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Initialize the Database

```bash
cd backend
python -m scripts.init_db
```

### 3. Index Book Content

```bash
cd backend
python -m scripts.index_content --book-id <book-id>
```

### 4. Start the Docusaurus Frontend

```bash
cd docusaurus
npm start
```

The application will be available at `http://localhost:3000`.

## Key Components

### Docusaurus Book
- Located in the `docusaurus/` directory
- Built with Docusaurus v3
- Includes custom React components for interactive elements
- Integrated with the RAG backend via API calls

### FastAPI Backend
- Located in the `backend/` directory
- Provides REST APIs for content management and RAG services
- Connects to Neon Postgres for structured data
- Uses Qdrant for vector storage and retrieval

### RAG System
- Implements retrieval-augmented generation for book content
- Provides intelligent search and question-answering capabilities
- Uses embeddings for semantic search
- Integrates with OpenAI for response generation

## Development Workflow

### Adding New Content

1. Create new markdown files in the appropriate module directory
2. Update the sidebar configuration in `docusaurus/sidebars.js`
3. Run the content indexing script to update the RAG system

### Custom Components

To add interactive elements to the book:

1. Create React components in `docusaurus/src/components`
2. Use the components in markdown files with `<ComponentName />` syntax
3. Ensure components follow accessibility standards

### API Endpoints

The backend provides several key endpoints:

- `/api/v1/content/` - Content management
- `/api/v1/rag/query` - RAG query endpoint
- `/api/v1/rag/search` - Semantic search
- `/api/v1/rag/sessions` - Session management

## Testing

### Frontend Tests

```bash
cd docusaurus
npm test
```

### Backend Tests

```bash
cd backend
python -m pytest
```

### Integration Tests

```bash
# Run integration tests for the full system
cd backend
python -m pytest tests/integration/
```

## Deployment

### Production Build

```bash
# Build the Docusaurus site
cd docusaurus
npm run build

# The built site will be in the build/ directory
```

### Environment Variables for Production

```env
APP_ENV=production
OPENAI_API_KEY=your_production_openai_key
NEON_POSTGRES_URL=your_production_postgres_url
QDRANT_URL=your_production_qdrant_url
API_BASE_URL=https://yourdomain.com/api
```

## Troubleshooting

### Common Issues

1. **API Rate Limits**: If encountering OpenAI rate limits, implement proper caching and request throttling.

2. **Database Connection Issues**: Verify that Neon Postgres credentials are correct and the database is accessible.

3. **Vector Search Performance**: If search is slow, verify that Qdrant is properly configured and indexes are built.

4. **Content Not Appearing**: After adding new content, ensure it has been indexed by running the indexing script.

### Useful Commands

```bash
# Check backend service status
curl http://localhost:8000/health

# Check Qdrant health
curl http://localhost:6333/health

# Rebuild content index
python -m scripts.rebuild_index

# Check current embeddings in Qdrant
python -m scripts.check_embeddings
```

## Next Steps

1. Review the complete implementation plan in `specs/1-ai-book/plan/plan.md`
2. Examine the data models in `specs/1-ai-book/plan/data-model.md`
3. Review API contracts in `specs/1-ai-book/plan/contracts/`
4. Explore the research findings in `specs/1-ai-book/plan/research.md`