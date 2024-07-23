
IDEI ALEX ===== OSI + RAG - Knowledge Graph and Lead Generation ===========

- users says: plz look at <THIS EVENT>  using <THESE 3 URLS>   containing <SOME FILTERS or KEYWORDS>
- bot generates 5 search query, obtains 5x20 page results
- fromm mresulting 100 pages we extract "framengted narratives"
    - NER with LLM to anser 
        - LEAD
            - 1. WHO
            - 2. WHAT
            - 3. WHEN
            - 4. WHERE
            - 5. WHY
        - BODY
            - EVIDENCCE
            - QUOTES (from user resources / scraped resources text)
            - MEMDIA OBJECCT (photo, video, html DOMM)
        - TAIL
            - OPINION
            - PERSUASION TACTIC
            - SENTIMENT / MOOD
        
    - all results of the above 
        =--- > NEO4J
        - llamaindex + NEO4j 
- user + bot cconverse:
    - users says "you are wrong about X, it is actually Y"
        - bot inserts in GraphDb
    - user says "also look at these NEW DOCCUMENTS: <url>"
        - re-run all of the above on new documents
        - bot reports CONFLICTS vs. existing dataset:
            - each documemnt is separate neo4j graph
            - LLM reads each graphs, then commparets cchat logs and looks for cocnflicts
    - users query about specific subject
        - bot generates initial intelligence report
            - "narrative prompt set" based on "iinverted pyramid" which is the 3 steps above LEAD, BODY, TAIL
        - user comments/remaks changes in report
        - bot accecpts, corrects 
    - WIKI SITE GENERATION
        - user-readbale knowledge base
        - user-editable mamrkdown
        - generated Table of Contents
        - generated fact checking pages
        - generated Wikipedia-style page for each acttor in whole dataset
        - generated Wikipedia-style page for each node in neo4j (events, specific answers to all lead questiosn "who what when where why?")



https://arxiv.org/pdf/2310.13848


IDEI ALEX ===== CODE GENERATION ===========


- software developmment bot 
   + code review bot 
   + test writer bot 
   = self developing app


- user says: plz immplement issue #123
    - ISSUE INFO:
        - bug desccription / feature descc.
        - details linking to area in code where mmomdifications mut happen
        - for bug show error log
        - for bug, steps to reproduce
        - commmmmon sense info: in simple terms, what must be achieved
    - STEPS:
        - user gets backc pull request variants + tests + passing tests + "commmon sense test: is this a solution"
        - user reviews / accepts / rejeccts with coment one pull request variant
        - user acccepts one variant and issue marked done

- user says: plz review PR #234
    - PR INFO:
        - issue ID (all pr have 1 issue assigned)
        - code
    - STEPS:
        - user gets back: code review
    
- user says: plz help me create new issue
    - CCHAT BOT CCONVERSION to GET INFO about ISSUE (desccription, details, ccode, snippets, steps to reproduce, ccommon sense info, test exapmles)
    - user produces above on demand (5-10 questions asked and answered)
- autogenerate docs



================================================================

idee aberanta paralela ccu hekrtonu

