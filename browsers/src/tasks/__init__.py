from .html_extract_links import extract_links_from_url
from .html_to_markdown import extract_markdown_from_html
from .download_html import render_page_to_html
from .lama_index import lama_index_demo

ALL_ACTIVITIES = [extract_links_from_url, extract_markdown_from_html, render_page_to_html, lama_index_demo]