def ui_main():
    from .router import router, hd
    try:
        template = hd.template(title="Hekthon")  # logo="/assets/hd-logo-white.svg", 
        template.add_sidebar_menu(
            {
                "DASHBOARDS": {
                    "Homepage": {"icon": "house", "href": "/"},
                    "TemporalIO UI": {"icon": "caret-right-square", "href": "/iframe/8080"},
                    "Mongo Express": {"icon": "database", "href": "/iframe/8081"},
                    "Selenium": {"icon": "browser-chrome", "href": "/iframe/4444"},
                    "Llama Index Mongo": {"icon": "browser-chrome", "href": "/iframe/11434"},
                    "Neo4J BROWSER": {"icon": "browser-chrome", "href": "/iframe/8082"},
                },
                "SCRAPE": {
                    "New Scrape": {"icon": "patch-plus", "href": "/new-scrape"},
                    "View Scrapes": {"icon": "file-earmark-bar-graph", "href": "/view-scrapes"},
                    "Original Demo": {"icon": "type-bold", "href": "/original-demo"},
                    "Chat": {"icon": "chat-left-dots", "href": "/chat"},
                },
            },
            expanded=True
        )

        # A topbar contact link:
        template.add_topbar_links(
            {
                "GitHub @Gestopptes/hekthon": {"icon": "github", "href": "https://github.com/Gestopptes/hekthon"},
                "hyperdiv docs": {"icon": "github", "href": "https://docs.hyperdiv.io/introduction/overview"}
            },
        )
    
        with template.body:
            with hd.box(padding=0.1, gap=0.1, width="100%", height="100%"):
                router.run()
    except Exception as e:
        with template.body:
            with hd.scope('ERROR_MAIN'):
                with hd.box(padding=0.3, gap=0.3, border="3px solid green" , width="80%", height="80%"):
                    import traceback
                    hd.markdown('###  Error (main): ' + str(e) + '\n\n```\n' + traceback.format_exc() + '\n```')
