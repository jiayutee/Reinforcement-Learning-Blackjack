"""Loopback-only public-rule inspection page; one shared local session."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets
from public_game.session import PublicSession
from public_game.commands import apply_command

PAGE = Path(__file__).with_name('local_game.html')
FOUNDATIONS = Path(__file__).resolve().parents[1] / 'foundations'
SOUND_ASSETS = {
    '/sound-events.js': Path(__file__).with_name('sound_events.js'),
    '/sound-player.js': FOUNDATIONS / 'sound-player.js',
}


def make_server(port=8766, seed=7):
    session = PublicSession(seed=seed)
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, status, body, content_type='application/json'):
            data = body.encode() if isinstance(body, str) else json.dumps(body).encode()
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(data)

        def allowed_host(self):
            return self.headers.get('Host') == f'127.0.0.1:{self.server.server_port}'

        def do_GET(self):
            if not self.allowed_host():
                self.reply(403, {'error': 'Use the printed loopback address.'})
            elif self.path == '/':
                self.reply(200, PAGE.read_text().replace('__TOKEN__', token), 'text/html; charset=utf-8')
            elif self.path == '/state':
                self.reply(200, session.view())
            elif self.path in SOUND_ASSETS:
                self.reply(200, SOUND_ASSETS[self.path].read_text(), 'text/javascript; charset=utf-8')
            else:
                self.reply(404, {'error': 'Not found'})

        def do_POST(self):
            origin = f'http://127.0.0.1:{self.server.server_port}'
            if not self.allowed_host() or self.headers.get('Origin') != origin or self.headers.get('X-Game-Token') != token:
                self.reply(403, {'error': 'Request not authorized for this local table.'})
                return
            if self.path != '/command':
                self.reply(404, {'error': 'Not found'})
                return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 1024 or self.headers.get('Content-Type') != 'application/json':
                    raise ValueError('Expected a small JSON request.')
                payload = json.loads(self.rfile.read(size))
            except (ValueError, UnicodeError):
                self.reply(400, {'error': 'Invalid request.'})
                return
            try:
                view = apply_command(session, payload)
            except ValueError as error:
                self.reply(409, {'error': str(error), 'state': session.view()})
                return
            self.reply(200, view)

    # HTTPServer serializes requests, making revision check + update atomic here.
    return HTTPServer(('127.0.0.1', port), Handler)



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8766)
    parser.add_argument('--seed', type=int, default=7)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('port must be in [0, 65535]')
    with make_server(args.port, args.seed) as server:
        print(f'Open http://127.0.0.1:{server.server_port} — one shared local session; Ctrl-C to stop.', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
