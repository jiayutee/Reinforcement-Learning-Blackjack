# Answer — validate a custom wager

An 18-chip wager costs 36 half-chip units, so it is affordable within 37. A 19-chip wager costs 38 units, which is greater than the balance; Deal should remain disabled. The backend still needs to validate because browser controls can be bypassed or requests can be sent directly. Only the server-owned session can safely decide whether to debit chips and start the round.
