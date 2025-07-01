# Project Progress Tracker

## Phase 1: Data Acquisition (Scraping)

### Milestones

*   [x] **Scraper for nnols.org (Base Code & Amendments)**
    *   [x] Initial setup for Playwright with pytest-playwright
    *   [x] Scrape the main code page for PDF links
    *   [x] Scrape the amendments page for resolution summaries
    *   [x] Follow links to individual resolution PDFs
    *   [x] Download and save all PDF files
    *   [x] Implement error handling and logging
    *   [x] Unit tests for nnols.org scraper

*   [x] **Scraper for navajonationcouncil.org (Bills & Resolutions)**
    *   [x] Scrape the legislation list for bill information
    *   [x] Extract links to full-text PDF documents
    *   [x] Download and save all bill PDFs
    *   [x] Implement error handling and logging
    *   [x] Unit tests for navajonationcouncil.org scraper

*   [x] **Scraper for dibb.nnols.org (Legislative Metadata)**
    *   [x] Scrape for bill metadata (sponsors, status, history)
    *   [x] Correlate metadata with bills from navajonationcouncil.org
    *   [x] Implement error handling and logging
    *   [x] Unit tests for dibb.nnols.org scraper

*   [x] **Scraper for navajonationcouncil.org/council (Council Member Data)**
    *   [x] Scrape the council roster
    *   [x] Implement logic to reconcile with other sources (press releases, etc.)
    *   [x] Implement error handling and logging
    *   [x] Unit tests for council member data scraper

*   [x] **Scraper for courts.navajo-nsn.gov (Supreme Court Opinions)**
    *   [x] Scrape the opinions page for PDF links
    *   [x] Download and save all opinion PDFs
    *   [x] Implement error handling and logging
    *   [ ] Unit tests for Supreme Court opinions scraper

*   [x] **Scraper for opvp.navajo-nsn.gov (Office of the President and Vice President)**
    *   [x] Scrape the administration roster
    *   [x] Scrape press releases
    *   [x] Implement error handling and logging
    *   [ ] Unit tests for OPVP scraper

*   [x] **Scraper for nndoj.navajo-nsn.gov (Navajo Nation Department of Justice)**
    *   [x] Scrape press releases
    *   [x] Scrape staff roster
    *   [x] Implement error handling and logging
    *   [ ] Unit tests for NNDOJ scraper

## Phase 2: Data Processing and Storage (Revised)

### Milestones

*   [ ] **Text Extraction & Chunking**
    *   [ ] Implement a robust text extraction pipeline for all scraped documents (PDFs, press release HTML) using libraries like PyMuPDF and BeautifulSoup.
    *   [ ] Clean and normalize the extracted text.
    *   [ ] Implement a strategy to chunk text into semantically complete units (e.g., by statute section for code, by paragraph for articles/opinions).
    *   [ ] Unit tests for extraction and chunking.

*   [ ] **Metadata & Relationship Extraction (NLP)**
    *   [ ] Develop regex/NLP model to extract key entities: specific citations from legal docs, and names/topics from press releases.
    *   [ ] Extract other key metadata: resolution numbers, case names, press release headlines, dates, etc.
    *   [ ] Test and refine the model on a sample set of documents.
    *   [ ] Unit tests for metadata extraction.

*   [ ] **Vector Embedding (Local)**
    *   [ ] Set up local embedding via Ollama using Qwen/Qwen3-Embedding-0.6B-GGUF.
    *   [ ] Develop a client to interface with the local Ollama embedding endpoint.
    *   [ ] Create a process to convert all text chunks (from legal docs and press articles) into vector embeddings.
    *   [ ] Implement error handling and batching for the embedding process.

*   [ ] **LLM-Powered Smart Diffing Engine**
    *   [ ] Set up local LLM for analysis via Ollama using unsloth/gemma-3n-E4B-it-GGUF.
    *   [ ] Develop prompts to instruct the LLM to analyze changes between two versions of a statute.
    *   [ ] Implement logic to feed the original and amended text to the LLM for a "smart check."
    *   [ ] The LLM will generate a summary of the change and classify its type (e.g., typo fix, clarification, substantive legal change).
    *   [ ] Store the LLM's analysis alongside a standard difflib output.
    *   [ ] Unit tests for the smart diffing engine.

*   [ ] **Database Upsert**
    *   [ ] Set up local SQLite DB and production Qdrant vector DB.
    *   [ ] Design final schema for Qdrant to store vectors alongside their corresponding text chunks and rich metadata (for all document types).
    *   [ ] Write and test scripts to "upsert" all processed data into the databases.

## Phase 3: Backend Development (API)

### Milestones

*   [ ] **FastAPI Application Setup**
    *   [ ] Initialize FastAPI project structure
    *   [ ] Implement configuration management using config.toml
    *   [ ] Set up centralized logging

*   [ ] **API Endpoints**
    *   [ ] Endpoint for "living code" with version history (using diffs)
    *   [ ] Endpoint for bill tracking
    *   [ ] Endpoint for council member information
    *   [ ] Endpoint for court opinions and press releases
    *   [ ] Endpoint for semantic search queries to Qdrant
    *   [ ] Endpoint for "Mind Map" data
    *   [ ] Implement API documentation (e.g., Swagger UI)
    *   [ ] Unit and integration tests for all endpoints

## Phase 4: Frontend Development

### Milestones

*   [ ] **UI/UX Design**
    *   [ ] Wireframes and mockups for the web interface
    *   [ ] Design for the "Mind Map" visualization

*   [ ] **Frontend Implementation**
    *   [ ] Set up frontend project (e.g., using a modern JavaScript framework)
    *   [ ] Implement all UI components
    *   [ ] Integrate with the FastAPI backend
    *   [ ] Implement the "Mind Map" visualization using a library like D3.js or similar
    *   [ ] End-to-end testing

## Phase 5: Deployment and Maintenance

### Milestones

*   [ ] **Deployment**
    *   [ ] Set up CI/CD pipeline
    *   [ ] Deploy application to a cloud platform
    *   [ ] Configure production database and other services

*   [ ] **Maintenance**
    *   [ ] Set up monitoring and alerting
    *   [ ] Establish a regular schedule for running scrapers
    *   [ ] Document maintenance procedures