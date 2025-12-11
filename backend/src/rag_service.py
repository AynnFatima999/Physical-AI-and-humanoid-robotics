import asyncio
import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
import openai
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .models import DocumentChunk
import os
from datetime import datetime
import time
import tiktoken
from .database import engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize models
class RAGService:
    def __init__(self):
        # Initialize sentence transformer model for embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY", None)
        )

        # Initialize OpenAI client
        self.openai_client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here")
        )

        # Create collection if it doesn't exist
        self.collection_name = "book_content_chunks"
        self._create_collection()

    def _create_collection(self):
        """Create Qdrant collection for document chunks if it doesn't exist"""
        try:
            # Check if collection exists
            self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists")
        except:
            # Create collection
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
            )
            logger.info(f"Created collection {self.collection_name}")

    async def index_content(self, content_id: UUID, content_type: str, content_text: str, metadata: Dict[str, Any]):
        """Index content in the vector database"""
        try:
            # Split content into chunks
            chunks = self._split_content(content_text)

            points = []
            for i, chunk in enumerate(chunks):
                # Generate embedding for the chunk
                embedding = self.encoder.encode(chunk).tolist()

                # Create a point for Qdrant
                point = models.PointStruct(
                    id=str(content_id) + f"_{i}",  # Create unique ID for each chunk
                    vector=embedding,
                    payload={
                        "content_id": str(content_id),
                        "content_type": content_type,
                        "chunk_text": chunk,
                        "chunk_index": i,
                        "metadata": metadata
                    }
                )
                points.append(point)

            # Upload points to Qdrant
            if points:
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                logger.info(f"Indexed {len(points)} chunks for content {content_id}")

            return len(points)
        except Exception as e:
            logger.error(f"Error indexing content: {e}")
            raise

    def _split_content(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split content into overlapping chunks"""
        if not text:
            return []

        # Use tokenizer to split more intelligently
        encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoder.encode(text)

        chunks = []
        start_idx = 0

        while start_idx < len(tokens):
            end_idx = start_idx + chunk_size
            chunk_tokens = tokens[start_idx:end_idx]

            # Decode back to text
            chunk_text = encoder.decode(chunk_tokens)
            chunks.append(chunk_text)

            # Move to next chunk with overlap
            start_idx = end_idx - overlap

            # If we're near the end, just take remaining tokens
            if start_idx >= len(tokens):
                break

        # If token-based splitting didn't work well, fall back to character-based
        if len(chunks) == 0 or len(chunks[0]) < 100:
            # Character-based splitting as fallback
            chunks = []
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                if chunk.strip():
                    chunks.append(chunk)

        return chunks

    async def search(self, query: str, max_results: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for relevant content using vector similarity"""
        try:
            # Generate embedding for the query
            query_embedding = self.encoder.encode(query).tolist()

            # Prepare filters for Qdrant
            qdrant_filters = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        models.FieldCondition(
                            key=f"metadata.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )

                if conditions:
                    qdrant_filters = models.Filter(
                        must=conditions
                    )

            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=qdrant_filters,
                limit=max_results,
                with_payload=True
            )

            # Format results
            results = []
            for hit in search_results:
                result = {
                    "id": hit.id,
                    "content": hit.payload.get("chunk_text", ""),
                    "content_id": hit.payload.get("content_id"),
                    "content_type": hit.payload.get("content_type"),
                    "metadata": hit.payload.get("metadata", {}),
                    "score": hit.score
                }
                results.append(result)

            logger.info(f"Found {len(results)} results for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error searching content: {e}")
            raise

    async def generate_response(self, query: str, context_chunks: List[Dict[str, Any]], temperature: float = 0.7) -> str:
        """Generate a response using OpenAI based on the context"""
        try:
            # Prepare context from chunks
            context = "\n\n".join([chunk["content"] for chunk in context_chunks])

            # Create a prompt for the LLM
            prompt = f"""
            You are an expert assistant for the AI-Native Software Development book.
            Answer the user's question based on the provided context from the book.

            Context from the book:
            {context}

            User question: {query}

            Provide a helpful, accurate answer based on the context. If the context doesn't contain enough information to answer the question, say so clearly.
            """

            # Call OpenAI API
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert assistant for the AI-Native Software Development book. Provide helpful, accurate answers based on the book content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Fallback response
            return f"I encountered an error processing your request. The query was: {query}"

    async def query_rag(self, query: str, max_results: int = 5, temperature: float = 0.7, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Complete RAG query: search + generate response"""
        start_time = time.time()

        try:
            # Search for relevant content
            search_results = await self.search(query, max_results, filters)

            if not search_results:
                return {
                    "response": "I couldn't find relevant information in the book to answer your question.",
                    "sources": [],
                    "confidence": 0.0,
                    "response_time": time.time() - start_time
                }

            # Generate response based on context
            response_text = await self.generate_response(query, search_results, temperature)

            # Format sources
            sources = []
            for result in search_results:
                source = {
                    "id": result["id"],
                    "title": f"Content from {result['content_type']} {result['content_id']}",
                    "content": result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"],
                    "sourceType": result["content_type"],
                    "confidence": result["score"]
                }
                sources.append(source)

            # Calculate overall confidence based on highest score
            confidence = max([result["score"] for result in search_results])

            return {
                "response": response_text,
                "sources": sources,
                "confidence": confidence,
                "response_time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            return {
                "response": "An error occurred while processing your request.",
                "sources": [],
                "confidence": 0.0,
                "response_time": time.time() - start_time
            }

    async def validate_content_academic_standards(self, content: str, content_type: str = "chapter") -> Dict[str, Any]:
        """Validate content against academic standards"""
        validation_results = {
            "is_valid": True,
            "issues": [],
            "readability_score": None,
            "citation_check": True,  # Placeholder - in a real system, this would check for proper citations
            "technical_accuracy": True  # Placeholder - in a real system, this would validate technical claims
        }

        # Check content length
        if len(content) < 100:
            validation_results["is_valid"] = False
            validation_results["issues"].append("Content is too short (< 100 characters)")

        # Check for basic readability (simplified Flesch-Kincaid)
        # This is a very basic approximation - a real system would use proper readability algorithms
        words = content.split()
        if len(words) > 0:
            avg_word_length = sum(len(word) for word in words) / len(words)
            sentence_count = content.count('.') + content.count('!') + content.count('?')
            if sentence_count == 0:
                sentence_count = 1  # Avoid division by zero
            avg_words_per_sentence = len(words) / sentence_count

            # Basic readability approximation (Flesch Reading Ease)
            # Score = 206.835 - (1.015 × ASL) - (84.6 × ASW)
            # Where ASL = average sentence length, ASW = average word length
            readability_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_word_length)
            validation_results["readability_score"] = readability_score

            # Academic content should ideally have a readability score between 30-60 (college level)
            if readability_score < 20 or readability_score > 70:
                validation_results["issues"].append(f"Readability score ({readability_score:.2f}) may not match academic standards (aim for 30-60)")

        # Check for common academic writing issues
        if content.count("TODO") > 0 or content.count("FIXME") > 0:
            validation_results["is_valid"] = False
            validation_results["issues"].append("Content contains TODO or FIXME markers")

        # Check for placeholder content
        if "[Chapter content will be added here]" in content:
            validation_results["is_valid"] = False
            validation_results["issues"].append("Content contains placeholder text")

        return validation_results

    async def index_book_content(self, db: AsyncSession, book_id: UUID):
        """Index all content of a book with validation"""
        try:
            # Get all chapters of the book
            book = await crud.get_book(db, book_id)
            if not book:
                raise ValueError(f"Book with id {book_id} not found")

            # Get all modules of the book
            modules = await crud.get_modules_by_book(db, book_id)

            total_chunks = 0
            validation_issues = []

            for module in modules:
                chapters = await crud.get_chapters_by_module(db, module.id)

                for chapter in chapters:
                    # Validate the chapter content before indexing
                    if chapter.content:
                        validation = await self.validate_content_academic_standards(chapter.content, "chapter")
                        if not validation["is_valid"]:
                            validation_issues.extend([
                                f"Chapter '{chapter.title}' validation issues: {', '.join(validation['issues'])}"
                            ])

                        metadata = {
                            "book_id": str(book_id),
                            "book_title": book.title,
                            "module_id": str(module.id),
                            "module_title": module.title,
                            "chapter_id": str(chapter.id),
                            "chapter_title": chapter.title,
                            "chapter_number": chapter.chapter_number,
                            "validation": validation
                        }

                        chunks_count = await self.index_content(
                            content_id=chapter.id,
                            content_type="Chapter",
                            content_text=chapter.content,
                            metadata=metadata
                        )
                        total_chunks += chunks_count

                    # Get sections of the chapter and index them too
                    sections = await crud.get_sections_by_chapter(db, chapter.id)
                    for section in sections:
                        if section.content:
                            validation = await self.validate_content_academic_standards(section.content, "section")
                            if not validation["is_valid"]:
                                validation_issues.extend([
                                    f"Section '{section.title}' validation issues: {', '.join(validation['issues'])}"
                                ])

                            metadata = {
                                "book_id": str(book_id),
                                "book_title": book.title,
                                "module_id": str(module.id),
                                "module_title": module.title,
                                "chapter_id": str(chapter.id),
                                "chapter_title": chapter.title,
                                "section_id": str(section.id),
                                "section_title": section.title,
                                "section_type": section.type,
                                "validation": validation
                            }

                            chunks_count = await self.index_content(
                                content_id=section.id,
                                content_type="Section",
                                content_text=section.content,
                                metadata=metadata
                            )
                            total_chunks += chunks_count

            logger.info(f"Indexed {total_chunks} chunks for book {book_id}")

            if validation_issues:
                logger.warning(f"Validation issues found in book {book_id}: {validation_issues}")

            return {
                "chunks_indexed": total_chunks,
                "validation_issues": validation_issues
            }
        except Exception as e:
            logger.error(f"Error indexing book content: {e}")
            raise

# Create a singleton instance
rag_service = RAGService()