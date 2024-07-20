
IMPL STEPS

1. keyword search (see plan-data-ingestion)
    - keyword -> get back list of [url/seotext/seotitle]
    - TODO
2. website scrap
    - url -> [html + pic] -> [markdown] -> [vectors (lama3)]
    - is DONE
3. index neo4j + lamaindex
    - TODO  https://neo4j.com/labs/genai-ecosystem/llamaindex/
4. impl agents
    - agents
        - editor
        - reporter/writer
        - factchecker
        - chatboat agent
        - conflict dectector agent
5. impl user interactions
    - plz add more information / more docs / more search keywords
    - plz view/show review conflicts
    - plz get references + evidence for event X
    - plz generate wiki site (generate markdown) for event X / person Y / company Z / location W
    - plz generate / update final intelligence report
    - plz request periodic search for X 















- steps of investigative journn -- 2->5
    1. topic choise  = USER DECISION/NOT IN SCOPE
    2. Research design = USER PROMPTS / user settings
    3. Search and accumulation of data = BOT + SCRAPER -> nro4j
    4. Hypothesis formulation = (bot agent editor) + human in the loop
    5. Data analysis + hypothesis tesing = [bot agent factchecker]
    6. Text Writing = [bot agent reporter] + [bot agent editor]+ human in the loop
    7. Publication = USER DECISION/NOT IN SCOPE

