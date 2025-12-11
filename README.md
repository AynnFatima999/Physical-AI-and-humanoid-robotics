# AI-Native Software Development: Physical AI & Humanoid Robotics

Welcome to the comprehensive guide on AI-Native Software Development with a focus on Physical AI & Humanoid Robotics. This book is designed for students and developers learning embodied AI, covering the essential aspects of humanoid robot development from basic ROS 2 concepts to advanced Vision-Language-Action systems.

## Project Structure

```
├── docusaurus/           # Docusaurus frontend for the book
│   ├── docs/            # Book content organized by modules
│   ├── src/             # Custom React components and CSS
│   ├── package.json     # Frontend dependencies
│   └── docusaurus.config.js # Docusaurus configuration
├── backend/             # FastAPI backend services
│   ├── src/             # Python source code
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Backend container configuration
├── docker-compose.yml   # Docker orchestration for all services
└── specs/              # Specification and planning documents
    └── 1-ai-book/       # Feature-specific specifications
```

## Modules

This book is structured into four comprehensive modules:

1. **ROS 2 (Robotic Nervous System)** - Introduction to Robot Operating System 2 as the foundational communication framework for humanoid robots
2. **Digital Twin (Gazebo & Unity)** - Creating realistic simulation environments that mirror real-world physics and sensor behavior
3. **NVIDIA Isaac (AI-Robot Brain)** - Advanced AI integration for robotic systems using NVIDIA's Isaac ecosystem
4. **Vision-Language-Action (VLA)** - Integration of perception, language understanding, and action execution

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- Docker and Docker Compose
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Set up the Docusaurus frontend:
   ```bash
   cd docusaurus
   npm install
   npm start
   ```

3. Set up the backend services:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn src.main:app --reload --port 8000
   ```

### Using Docker Compose (Recommended)

For a complete setup with all services:

```bash
docker-compose up --build
```

This will start:
- Backend API service on port 8000
- PostgreSQL database
- Qdrant vector database
- Docusaurus frontend on port 3000

## Development

### Adding New Content

1. Create new markdown files in the appropriate module directory in `docusaurus/docs/`
2. Update the sidebar configuration in `docusaurus/sidebars.js`
3. Add any custom components in `docusaurus/src/components/`

### Backend Development

The backend is built with FastAPI and includes:
- Content management APIs
- RAG (Retrieval-Augmented Generation) system
- Simulation integration endpoints
- User session management

## Architecture

### Frontend
- Built with Docusaurus for documentation
- Custom React components for interactive elements
- Integrated RAG chatbot interface

### Backend
- FastAPI for RESTful services
- PostgreSQL for structured data
- Qdrant for vector storage and semantic search
- Python for data processing and AI integration

### RAG System
- Implements retrieval-augmented generation for book content
- Provides intelligent search and question-answering capabilities
- Uses embeddings for semantic search
- Integrates with OpenAI for response generation

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please open an issue in the repository.