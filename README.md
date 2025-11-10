# 252R Deep Learning Course - LlamaIndex & RAG

A comprehensive learning repository for LlamaIndex and Retrieval-Augmented Generation (RAG) systems.

## Weekly Progress

| Week | Topic | Status | Notes |
|------|-------|--------|-------|
| 1 | Introduction to LlamaIndex | 🔄 In Progress | Setup & Basic Usage |
| 2 | LlamaIndex Pipeline | ⏳ Upcoming | Data Loading, Chunking, Indexing |
| 3 | Vector Stores | ⏳ Upcoming | Chroma, Pinecone, Qdrant |
| 4 | Text Document RAG | ⏳ Upcoming | PDF, TXT, CSV, HWP |
| 5 | Multimodal RAG | ⏳ Upcoming | Images & Text |
| 6 | Agent RAG | ⏳ Upcoming | Building Intelligent Agents |
| 7 | Advanced RAG | ⏳ Upcoming | ReRanking, HyDE |
| 8 | Function Calling Agents | ⏳ Upcoming | External API Integration |
| 9 | Text-to-SQL Agent | ⏳ Upcoming | Database Query Agent |
| 10 | Model Context Protocol (MCP) | ⏳ Upcoming | MCP Server & Client |

---

## Chapter 1: Introduction to LlamaIndex

- [ ] Understand what LlamaIndex supports
- [ ] Set up Python development environment
  - [ ] Install Python on Windows
  - [ ] Create virtual environment
  - [ ] Install Visual Studio Code
- [ ] Obtain API keys
  - [ ] OpenAI API key
  - [ ] Gemini API key
  - [ ] Add API keys to environment variables
- [ ] First LlamaIndex experience
  - [ ] Prepare sample data
  - [ ] Install LlamaIndex in virtual environment
  - [ ] Run first LlamaIndex application

## Chapter 2: LlamaIndex Pipeline

- [ ] Set up development environment
- [ ] Data Loading
  - [ ] Understand Data Readers
  - [ ] Learn about Data Connectors
- [ ] Text Chunking
  - [ ] Understand Documents and Nodes
  - [ ] Token-based splitting
  - [ ] Sentence-based splitting
  - [ ] Semantic splitting
  - [ ] Compare chunking strategies
- [ ] Indexing
  - [ ] What is indexing?
  - [ ] Vector Store Index
  - [ ] Top-K retrieval
- [ ] Persistence (Saving indexes)
- [ ] Querying
  - [ ] QueryEngine
  - [ ] Retrieval
  - [ ] Postprocessing
  - [ ] Response synthesis
  - [ ] Customization

## Chapter 3: Vector Stores

- [ ] Set up development environment
- [ ] Chroma
  - [ ] Create Chroma client
  - [ ] Create collections
  - [ ] Add vector data
  - [ ] Vector search
  - [ ] Metadata filtering
  - [ ] Add embedding data
  - [ ] Search embedding data
  - [ ] Understand Chroma storage
  - [ ] Generate responses with embeddings
  - [ ] Generate responses with LlamaIndex
- [ ] Pinecone
  - [ ] Initialize Pinecone API
  - [ ] Add vector data
  - [ ] Vector search
  - [ ] Metadata filtering
  - [ ] Generate responses with embeddings
  - [ ] Generate responses without explicit embeddings
- [ ] Qdrant
  - [ ] Generate responses with LlamaIndex
  - [ ] Set up local environment with Docker
  - [ ] Set up cloud-based environment

## Chapter 4: Text Document RAG

- [ ] Set up development environment
- [ ] Prepare practice data
- [ ] Working with PDF files
  - [ ] Prepare data
  - [ ] Text chunking
  - [ ] Indexing
  - [ ] Execute queries
- [ ] Working with text files
  - [ ] Basic RAG practice
  - [ ] Save index using Chroma
- [ ] Working with CSV files
- [ ] Working with HWP files
  - [ ] Use HWPReader
  - [ ] Use SimpleDirectoryReader

## Chapter 5: Multimodal RAG

- [ ] Set up development environment
- [ ] Prepare data
- [ ] Multimodal vector indexing with OpenAI API
- [ ] Build multimodal RAG with Qdrant
  - [ ] Install Qdrant and set up client
  - [ ] Create text and image vector stores
  - [ ] Create multimodal vector index
  - [ ] Perform retrieval
- [ ] Build Q&A-based RAG system
  - [ ] Execute basic queries
  - [ ] Execute queries with improved prompts
- [ ] Build image-based RAG system
  - [ ] Download and save new images
  - [ ] Perform image search
  - [ ] Analyze images with similar styles

## Chapter 6: Agent RAG

- [ ] Set up development environment
- [ ] Prepare data
- [ ] Use HuggingFace embeddings
- [ ] Create agents

## Chapter 7: Advanced RAG

- [ ] Set up development environment
- [ ] ReRanking
  - [ ] LLM-based reranking
- [ ] Address cost issues with LLM-based reranking
  - [ ] Cross-encoder based reranking
- [ ] HyDE (Hypothetical Document Embeddings)
  - [ ] Prepare data
  - [ ] Configure LLM and embeddings
  - [ ] Implement HyDE

## Chapter 8: Function Calling Agents

- [ ] Set up development environment
- [ ] Understand how function calling works
- [ ] Function calling with external APIs
  - [ ] Create stock market information agent
  - [ ] Prepare function calling tools
  - [ ] Create agent and execute queries
- [ ] RAG agent with function calling
  - [ ] Set up environment and prepare data
  - [ ] Prepare function calling tools
  - [ ] Create agent and execute queries

## Chapter 9: Text-to-SQL Consultant Agent

- [ ] Set up development environment
- [ ] Set up environment for agent development
- [ ] Design hospital database
- [ ] Implement Text-to-SQL agent
- [ ] Multi-turn conversation handling
- [ ] Build user interface with Gradio

## Chapter 10: Model Context Protocol (MCP)

- [ ] Understand what MCP is
- [ ] Set up MCP development environment
- [ ] MCP Server
  - [ ] Register tools using Adapter
  - [ ] MCP Inspector
  - [ ] Message format
  - [ ] Document search agent MCP practice
- [ ] MCP Client
- [ ] Weather agent practice
  - [ ] Obtain OpenWeatherMap API key
  - [ ] Extract city names
  - [ ] Integrate OpenWeatherMap API
  - [ ] Register MCP tools and run server
  - [ ] Implement MCP client for weather queries
  - [ ] Summary and wrap-up

---

## Resources

- **Course Materials**: [Add link]
- **Recommended Reading**: 
  - LlamaIndex Official Documentation
  - RAG Best Practices
  - Vector Database Comparison Guide
- **Frameworks**: LlamaIndex, OpenAI, HuggingFace, Gradio

## Setup

```bash
# Clone the repository
git clone https://github.com/dwhouse/252R_DL.git
cd 252R_DL

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## API Keys Required

- OpenAI API Key
- Google Gemini API Key
- Pinecone API Key (for Chapter 3)
- OpenWeatherMap API Key (for Chapter 10)

Store these in a `.env` file:
```bash
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key
PINECONE_API_KEY=your_pinecone_key
OPENWEATHER_API_KEY=your_openweather_key
```

## License

MIT License
