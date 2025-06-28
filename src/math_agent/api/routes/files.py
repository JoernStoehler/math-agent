"""File serving routes"""
from fastapi import APIRouter, Response

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/")
async def files_index():
    """Simple index page for file browsing"""
    html = """
    <html>
    <head>
        <title>File Browser</title>
        <style>
            body { font-family: monospace; margin: 20px; }
            a { text-decoration: none; color: blue; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>File Browser</h1>
        <hr>
        <pre>
<a href="/files/data/">data/</a>
<a href="/files/jobs/">jobs/</a>
        </pre>
        <hr>
    </body>
    </html>"""
    return Response(content=html, media_type="text/html")