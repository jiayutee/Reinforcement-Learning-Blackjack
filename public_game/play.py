"""Local terminal adapter for public-rule sessions; virtual chips only."""
import argparse
from public_game.session import PublicSession
from public_game.cards import Card
from public_game.hands import hand_facts


def format_view(view):
    def cards(items):
        return ' '.join('??' if c is None else c['rank'] + '-' + c['suit'] for c in items)
    lines = ['Balance: %g chips | %s | revision %s' %
             (view['balance']/2, view['phase'], view['revision'])]
    if view['dealer']:
        lines.append('Dealer: ' + cards(view['dealer']) +
                     (' | total %s' % view['dealer_total'] if view['dealer_total'] is not None else ''))
    for i, hand in enumerate(view['hands']):
        marker = ' ->' if view['active_hand'] == i else ''
        facts = hand_facts([Card(c['rank'], c['suit']) for c in hand['cards']],
                           from_split=hand['from_split'])
        label = 'bust' if facts.bust else 'soft' if facts.usable_ace else 'hard'
        lines.append('Hand %s%s: %s | %s %s | stake %g chips%s' %
                     (i+1, marker, cards(hand['cards']), label, facts.total, hand['stake']/2,
                      ' | '+hand['outcome'] if hand['outcome'] else ''))
    if view['profit'] is not None:
        lines.append('Round profit: %g chips | normalized: %g' %
                     (view['profit']/2, view['normalized_profit']))
    lines.append('Commands: ' + ', '.join(view['legal_actions'] or ['deal <whole chips>']) + ', quit')
    return '\n'.join(lines)


def run(session, read=input, write=print):
    write('Public-rule terminal prototype. Virtual chips; no trained coach. Seeded local game.')
    write(format_view(session.view()))
    while True:
        try:
            parts = read('> ').strip().lower().split()
        except (EOFError, KeyboardInterrupt):
            return
        if parts == ['quit']:
            return
        view = session.view()
        try:
            if len(parts) == 2 and parts[0] == 'deal':
                view = session.deal(int(parts[1])*2, view['revision'])
            elif len(parts) == 1 and parts[0] in ('hit','stand','double','split'):
                view = session.act(parts[0], view['revision'])
            else:
                raise ValueError('use deal <whole chips>, hit, stand, double, split or quit')
        except ValueError as error:
            write('Rejected: ' + str(error))
            continue
        write(format_view(view))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=7)
    args = parser.parse_args()
    run(PublicSession(seed=args.seed))


if __name__ == '__main__':
    main()
