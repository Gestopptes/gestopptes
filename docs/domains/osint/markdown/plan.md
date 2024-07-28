# RAG / OSINT prototype

This project involves using Open Source Intelligence (OSI)
 combined with Retrieval-Augmented Generation (RAG)
  to generate a comprehensive knowledge graph
   and lead generation system. 
   
   The workflow will include automated search queries, 
   information extraction,
    and user interaction to build and refine a knowledge base.


## User Interaction Story

### User Description and Motivation

User is journalist part of team researching specific subject ("the asssasination attempt on donald trump").

### User Role

User can have one of 3 types of roles:

- editor
- reporter
- fact checker


### Steps of a Journalism Investigation

Journalism in general follows this procedure:

1. topic choice
    - USER DECISION/NOT IN SCOPE
    - User Role: Editor
    - The topic choice is outside of the scope of the software; 
    - the software will ask information about topic before starting the process.

2. Research design
    - USER DECISION/settings
    - User Role: Editor
    - Research design is described by USER PROMPTS and SETTINGS

3. Search and accumulation of data
    - BOT + SCRAPER + INGESTION
    - User Role: Editor (very limited) + Reporter (all the time)
    - Download all documents related to the subject.
    - Ingest information using LLM into Graph Database and Vector Database.
    - Report to user with statistics and lead generation for given docs.
    
4. Hypothesis formulation
    - BOT LEAD GENERATION + HUMAN IN THE LOOP (chat)
    - User Role: Editor
    - User chooses some leads generated at previous step, or
    - User inputs their own hypothesis in chat

5. Data analysis + hypothesis tesing
    - BOT CONFLICT DETECTION + FACT CHECKING + HUMAN IN THE LOOP (chat)
    - User Role: Factchecker
    - Bot generates questions and answers that would prove or disprove hypothesis
    - Bot reports on conflicts between input documents

6. Text Writing
    - LLM + HUMNA IN HTE LOOP (chat)
    - User Role: Reporter

7. Publication
    - NOT IN SCOPE
    - The organization publishes the article in their newspaper.



### 1. User Registration and "Investigation" Initialization

1. User "john" creates account, signs in, joins group, and creates new "Investigation" called "Trump a attempt of july 2024"
2. User describes the event in a short paragraph, then adds starting keywords and URLs


### 2. Scraping

1. Bot generates and executes search queries on web, downloads 100 results
2. Download HTML selenium, convert to Markdown and pre-process for LLM ingestion


### 3. LLM Data Ingestion

1. Bot splits all pages into segments and analyzes each as follows.
2. Bot runs NER on each segment using LLM to extract from all the downloaded news articles the following 11 tags:
    - 1. LEAD
        - 1. WHO
        - 2. WHAT
        - 3. WHEN
        - 4. WHERE
        - 5. WHY
    - 2. BODY
        - EVIDENCCE
        - QUOTES (from user resources / scraped resources text)
        - MEMDIA OBJECCT (photo, video, html DOMM)
    - 3. TAIL
        - OPINION
        - PERSUASION TACTIC
        - SENTIMENT / MOOD
3. Bot takes the NER tags from above and saves to Graph Db (neo4j).
4. Bot runs model on each segment and saves to Vector DB (neo4j).
5. Bot generates report about what was done in this step:
    - statistics:
        - number of links/documents/entities/segmnets/tokens
        - time, timestamp. deltas (in seconds of runtime)
    - detected conflicts between documents
    - summary of knowledge base so far (and diff with previous)
6. Bot generates leads - interesting entities and keywords 


### 4. Wiki Site Generation

Bot generates Markdown Wiki Site based on the entities and how they inter-relate:


1. Each entity (e.g. "the shooter", "the weapon") has a markdown page
2. each edge (e.g. segment relating "the shooter" with some other fact e.g. "the weapon") appears as paragraph in both wiki pages ("the shooter" and "the weapon")
3. extract pictures from original documents and show on right side (like wikipedia)
4. references to inital documents (like on wikipedia)
5. Generate multi-level table of contents


### 5. CHAT

The chat interface shows the chat text on the left side, and a Graph DB UI on the right side. The Graph DB UI automatically highlights nodes that are relevant to the conversation, and filters out the ones that are not relevant.

1. User asks question about specific subject included in the documents
    - user says "what happened on the day of X related to Y?"
    - bot runs RAG and generates text response
    - Graph DB UI shows relevant nodes and highlights important ones.

2. User resolves conflict detected between different documents
    - users says "You are wrong about X, it is actually Y"
    - bot adjusts database based on those requests
    - user is shown summarized database diff in Graph UI, and summarized text description of the operation done

3. Users requests to add new documents/keywords/URLs to scrape set
    - bot re-runs previous steps on new data: scraping, ingestion
    - bot generates new report (of the diff) and new leads (based on new documents)


### 6. ARTICLE GENERATION

User adds new article in the UI - this shows a document editing interface that the can edit with the LLM.



## Features

1. user registration and management
- user login and management
- group membership and management

2. investigation (project) management
- "investigation" management:
    - access controls
    - audit history
    - metadata changes (starting pages, keywords and URLs)
    - settings changes (scraper settings, LLM model settings, system prompts)

3. scraping and parsing
- selenium bot pipeline (link --> html --> markdown + more links)
- search engine integration (langchain/llamaindex google/duckduck/wikipedia search engines)

4. LLM data ingestion
- document splitter into segments of adequate size (related to model context)
- NER in the "inverted pyramid model" of journalism, using the 11 tags grouped in 3 sections (lead, body, tail)
- ingest NER tags in Graph Databse
- ingest vector data into Vector DB
- generate report: statistics + summary
- detect conflicts between different documents
- lead generation: keywords, entities, events

5. wiki site generation
- generate top-level pages about entities (locations, events, people, orgs)
- generate paragraphs about all graph edges (cross linking 2 pages)
- extract relevant multimedia for each section
- generate references in each page to their original document (footnotes)
- generate multi-level table of contents, in its text form this can be a wiki page section ("see also") - max 5 links

6. chat
- user query
    - RAG + hybrid search
    - besides chat window, show Graph DB UI with the nodes relevant to conversation
- user resolve conflict between input documents
    - edit graph db
    - show user-friendly diff of what happend on Graph DB UI
- user requests new document/datasource/keywords
    - re-run scrape, ingestion, and wiki generation
    - show Wiki Site diff and let user review it
    - show summarized Graph DB UI with diff of new nodes added
    - show new conflicts between new documents
    - show new conflicst with existing documents

7. report generation
- editor user creates new report (links investigation, adds name, adds context, assigns reporters and factcheckers)
- reporter chats with bot to create article



## Implementation details



### Papers

https://arxiv.org/pdf/2310.13848

### LLM Agent Types


### Specific Frameworks


### Ops/Devops



## Market Study /  Marketing / Pitch / Revenue Generation


---

## MVP Milestones