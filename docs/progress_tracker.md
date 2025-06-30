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
    *   [x] Correlrate metadata with bills from navajonationcouncil.org
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

## Phase 2: Data Processing and Storage

### Milestones

*   [ ] **PDF Processing Pipeline**
    *   [ ] Implement PDF text extraction for all scraped documents
    *   [ ] Clean and normalize extracted text
    *   [ ] Unit tests for PDF processing

*   [ ] **NLP for Statute Identification**
    *   [ ] Develop regex/NLP model to identify statute citations in resolutions and court opinions
    *   [ ] Test and refine the model on a sample set of documents
    *   [ ] Unit tests for NLP model

*   [ ] **Diffing Engine**
    *   [ ] Implement logic to compare amended code with the base code
    *   [ ] Generate diffs to show changes
    *   [ ] Unit tests for diffing engine

*   [ ] **Database Schema and Setup**
    *   [ ] Set up local SQLite database for development
    *   [ ] Design and implement schema for Qdrant
    *   [ ] Write scripts to load processed data into the database
    *   [ ] Unit tests for database loading

## Phase 3: Backend Development (API)

### Milestones

*   [ ] **FastAPI Application Setup**
    *   [ ] Initialize FastAPI project structure
    *   [ ] Implement configuration management using `config.toml`
    *   [ ] Set up centralized logging

*   [ ] **API Endpoints**
    *   [ ] Endpoint for "living code" with version history
    *   [ ] Endpoint for bill tracking
    *   [ ] Endpoint for council member information
    *   [ ] Endpoint for court opinions
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