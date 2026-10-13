"""Transport-independent command boundary for the public-rule session."""


def apply_command(session, payload):
    """Accept intent only; wagers are integer half-chip units, not client outcomes.

    HTTP authentication/origin checks and per-user session isolation belong to
    the future transport adapter. The session owns legality and stale revisions.
    """
    if type(payload) is not dict:
        raise ValueError('command must be an object')
    command = payload.get('command')
    if type(command) is not str or command not in ('deal','hit','stand','double','split'):
        raise ValueError('unknown command')
    expected = {'command','revision','stake'} if command == 'deal' else {'command','revision'}
    if set(payload) != expected:
        raise ValueError('unexpected or missing command fields')
    if type(payload['revision']) is not int or payload['revision'] < 0:
        raise ValueError('revision must be a nonnegative integer')
    if command == 'deal':
        return session.deal(payload['stake'], payload['revision'])
    return session.act(command, payload['revision'])
