"""Loopback-only, single-session teaching table. Not a production web server."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets

from foundations.session import GameSession
from foundations.policy import load_policy

PAGE = Path(__file__).with_name('local_game.html')


def table_view(session, policy=None):
    """Advice is computed only from the same visible information sent to the player."""
    view = session.view()
    hand = view['hand']
    view['advice'] = None
    view['advisor_loaded'] = policy is not None
    if policy is not None and hand is not None and not hand['done']:
        observation = (hand['player_total'], hand['dealer_cards'][0], hand['player_usable_ace'])
        view['advice'] = policy.advise(observation)
    return view


def apply_table_command(session, policy, command, revision):
    """Execute at most one action; the client never supplies the bot's choice."""
    if command == 'bot':
        current = session.view()
        if type(revision) is not int or revision != current['revision']:
            raise ValueError('Stale or invalid revision; fetch the current view.')
        advice = table_view(session, policy)['advice']
        if advice is None or advice['action'] not in (0, 1):
            raise ValueError('No supported bot action. Deal an active hand with a loaded policy and recorded action evidence.')
        command = 'stand' if advice['action'] == 0 else 'hit'
    session.command(command, revision)
    return table_view(session, policy)


def make_server(port=8765, seed=7, policy=None):
    session = GameSession(seed)
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
                self.reply(200, table_view(session, policy))
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
                if not isinstance(payload, dict) or set(payload) != {'command', 'revision'} or not isinstance(payload['command'], str):
                    raise ValueError('Expected command and revision only.')
            except (ValueError, UnicodeError):
                self.reply(400, {'error': 'Invalid request.'})
                return
            try:
                view = apply_table_command(session, policy, payload['command'], payload['revision'])
            except ValueError as error:
                self.reply(409, {'error': str(error), 'state': table_view(session, policy)})
                return
            self.reply(200, view)

    # HTTPServer serializes requests, making revision check + update atomic here.
    return HTTPServer(('127.0.0.1', port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--policy', type=Path, help='Optional saved Foundations control export; no training at startup')
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('port must be in [0, 65535]')
    try:
        policy = load_policy(args.policy) if args.policy else None
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    with make_server(args.port, args.seed, policy) as server:
        print(f'Open http://127.0.0.1:{server.server_port} — one shared local session; Ctrl-C to stop.', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
