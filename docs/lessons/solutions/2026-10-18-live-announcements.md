# Answers — live state announcements

1. The round profit is an aggregate across both hands. Announcing after the first hand would present an incomplete outcome as the result of the round. Wait for the authoritative `settled` snapshot.
2. While the second hand remains active, announce the current active hand, its total type/value, dealer up-card, and available legal actions. Do not announce a final round win/loss/push yet.
