"""Python 3.15-compatible zero-dependency HTTP application."""
import csv
import io
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from wsd_engine import DATA, inventory, disambiguate

ROOT = Path(__file__).resolve().parent
SAMPLES = list(csv.DictReader((ROOT/'sample_sentences.csv').open(encoding='utf-8', newline='')))

class Handler(BaseHTTPRequestHandler):
    def respond(self, status, content, content_type='application/json; charset=utf-8', filename=None):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.send_header('X-Content-Type-Options','nosniff')
        if filename:
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(content)

    def json(self, status, payload):
        self.respond(status, json.dumps(payload, ensure_ascii=False).encode('utf-8'))

    def do_GET(self):
        route = urlparse(self.path).path
        if route == '/api/info':
            return self.json(200, {'words':sorted(DATA), 'samples':SAMPLES, 'python':'3.15-compatible', 'mode':'offline by default'})
        if route == '/api/export':
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(['Word','Sentence','Predicted sense','Definition','Overlap score','Fallback'])
            for row in SAMPLES:
                result = disambiguate(row['sentence'],row['word'])
                best = result['best'] or {}
                writer.writerow([row['word'],row['sentence'],best.get('id',''),best.get('definition',''),best.get('score',''),result['fallback']])
            return self.respond(200, buffer.getvalue().encode('utf-8-sig'), 'text/csv; charset=utf-8', 'wsd_results.csv')
        target = ROOT/'static' / ('index.html' if route=='/' else route.lstrip('/'))
        if not target.resolve().is_relative_to((ROOT/'static').resolve()) or not target.is_file():
            return self.json(404, {'error':'Not found'})
        self.respond(200, target.read_bytes(), mimetypes.guess_type(str(target))[0] or 'application/octet-stream')

    def do_POST(self):
        route = urlparse(self.path).path
        if route not in ('/api/inventory','/api/wsd','/api/batch'):
            return self.json(404, {'error':'Not found'})
        try:
            size = int(self.headers.get('Content-Length','0'))
            if size > 200_000 or size < 0:
                return self.json(413, {'error':'Request too large'})
            data = json.loads(self.rfile.read(size))
            source = data.get('source','offline')
            if source not in ('offline','wordnet'):
                return self.json(400, {'error':'Invalid source'})
            if route == '/api/batch':
                rows = data.get('rows',SAMPLES)
                if not isinstance(rows,list) or len(rows)>100:
                    return self.json(400,{'error':'Maximum 100 rows'})
                return self.json(200, {'results':[disambiguate(str(x['sentence'])[:2000],str(x['word'])[:80],source) for x in rows]})
            word = str(data.get('word',''))[:80].strip()
            if not word:
                return self.json(400, {'error':'Enter a target word'})
            if route == '/api/inventory':
                return self.json(200, inventory(word,source))
            sentence = str(data.get('sentence',''))[:2000].strip()
            if not sentence:
                return self.json(400, {'error':'Enter a sentence'})
            return self.json(200, disambiguate(sentence,word,source))
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            return self.json(400, {'error':f'Invalid request: {exc}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT','8501'))
    server = ThreadingHTTPServer(('127.0.0.1',port),Handler)
    print(f'LexiSense running at http://127.0.0.1:{port} (Ctrl+C to stop)',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
