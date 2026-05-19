import os
from datetime import datetime, timezone
from duckduckgo_search import DDGS
from pathlib import Path

QUERY = "Javier Lamarque Cano"
PLATFORM_SEARCH_URLS = {
    "Facebook": "https://www.facebook.com/search/posts?q=Javier%20Lamarque%20Cano",
    "Instagram": "https://www.instagram.com/explore/tags/javierlamarquecano/",
    "TikTok": "https://www.tiktok.com/search?q=Javier%20Lamarque%20Cano",
    "X (Twitter)": "https://x.com/search?q=Javier%20Lamarque%20Cano&f=top",
    "Google News": "https://news.google.com/search?q=Javier%20Lamarque%20Cano&hl=es-419&gl=MX"
}

def fetch_mentions():
    mentions = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.news(QUERY, timelimit='w', max_results=10):
                mentions.append({"date": r.get("date", "Reciente"), "source": "Noticias", "title": r.get("title", ""), "href": r.get("href", "#")})
            for r in ddgs.text(QUERY, timelimit='w', max_results=5):
                mentions.append({"date": r.get("date", "Reciente"), "source": "Web", "title": r.get("title", ""), "href": r.get("href", "#")})
    except Exception as e:
        mentions.append({"date": "-", "source": "Sistema", "title": f"Error en búsqueda: {e}", "href": "#"})
    return mentions

def generate_html(mentions):
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    seen = set()
    unique = [m for m in mentions if m['href'] not in seen and not seen.add(m['href'])]

    rows = ""
    for m in unique:
        rows += f"<tr><td>{m['date']}</td><td>{m['source']}</td><td>{m['title']}</td><td><a href='{m['href']}' target='_blank'>🔗 Ver publicación</a></td></tr>\n"

    plat_btns = "".join([f"<a href='{url}' target='_blank' class='plat-btn'>{name}</a>\n" for name, url in PLATFORM_SEARCH_URLS.items()])

    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Monitor: {QUERY}</title>
<style>
body{{font-family:system-ui,-apple-system,sans-serif;background:#f8f9fa;margin:0;padding:20px;color:#212529}}
.container{{max-width:900px;margin:auto;background:#fff;padding:25px;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,.08)}}
h1{{margin:0 0 5px;font-size:1.8rem}}.subtitle{{color:#6c757d;margin-bottom:20px}}
.platforms{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:25px}}
.plat-btn{{padding:10px 16px;background:#e9ecef;border-radius:8px;text-decoration:none;color:#495057;font-weight:500;transition:.2s}}
.plat-btn:hover{{background:#dee2e6;transform:translateY(-1px)}}
table{{width:100%;border-collapse:collapse;margin-top:10px}}th,td{{padding:12px 10px;border-bottom:1px solid #e9ecef;text-align:left}}
th{{background:#f1f3f5;font-weight:600}}a{{color:#0d6efd;text-decoration:none}}a:hover{{text-decoration:underline}}
.empty{{text-align:center;color:#adb5bd;padding:30px 0}}.footer{{margin-top:20px;font-size:.85rem;color:#6c757d;text-align:center}}
</style></head><body>
<div class="container">
<h1>📊 Monitor: {QUERY}</h1>
<div class="subtitle">Última actualización: {now} | Se refresca cada 3 horas (Hora Sonora)</div>
<h3>🌐 Búsquedas en vivo (resultados reales al instante)</h3>
<div class="platforms">{plat_btns}</div>
<h3>📰 Menciones indexadas recientemente</h3>
<table><thead><tr><th>Fecha</th><th>Fuente</th><th>Título</th><th>Enlace</th></tr></thead><tbody>
{rows if rows else '<tr><td colspan="4" class="empty">No se encontraron menciones nuevas. Usa los botones de arriba para ver contenido en vivo.</td></tr>'}
</tbody></table>
<div class="footer">Generado automáticamente con GitHub Actions. Datos públicos indexados.</div>
</div></body></html>"""
    return html

if __name__ == "__main__":
    mentions = fetch_mentions()
    html_content = generate_html(mentions)
    Path("index.html").write_text(html_content, encoding="utf-8")
    print("✅ index.html generado correctamente.")