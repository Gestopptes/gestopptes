from .scrape import ScrapeWorkflow, DownloadWorkflow, execute_scrape, ExtractMarkdownWorkflow
from .lama_index import LamaIndexDemoWorkflow
ALL_WORKFLOWS = [ScrapeWorkflow, DownloadWorkflow, ExtractMarkdownWorkflow,LamaIndexDemoWorkflow]
