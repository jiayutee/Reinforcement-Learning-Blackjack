# Public round v1: implementation contract

Status: specified for implementation, 6 October 2026. This describes the planned virtual-chip game, not behavior already available in the Foundations browser. It refines the public profile in PROJECT_PLAN.md; existing trained agents remain incompatible until separately evaluated under these rules.

## Rules and money representation

Use six decks, dealer stands on all 17s, American hole card, natural check before player actions, natural pays 3:2, ordinary wins 1:1, ties push. No insurance or surrender. Allow double on any initial two-card hand, including after splitting except split aces. Split equal ranks, maximum four player hands; resplit non-aces within that limit. Split aces each receive one card, automatically stand and cannot resplit. Any split-hand 21 is ordinary 21.

All chips are virtual and local to the game. Store integer half-chip units to represent 3:2 exactly. Initial wagers must be positive whole chips (an even number of half-chip units) and no greater than available balance. Split stakes inherit the initial wager; doubling adds that hand's current stake once. Debit additional stake before accepting double/split. Reject insufficient funds before drawing or mutating anything.

## Round phases and legal actions

| Phase | Accepted commands | Result |
|---|---|---|
| Ready / settled | Deal with valid wager | Prepare shoe between rounds, debit wager, deal player/dealer/player/dealer |
| Initial check | No player action | Check dealer natural internally; settle naturals or select first active hand |
| Player turn | Hit, stand; double/split if eligible | Modify only the active hand, then advance when it completes |
| Dealer turn | No player action | Reveal and draw to 17 if a comparison is required |
| Settlement | No player action | Settle each hand once and publish round result |

These phases may execute synchronously inside one command, but no client can skip checks. Every accepted external command advances the revision once. Stale/invalid requests leave balance, shoe, hands and settlement unchanged.

Hit draws one card; bust or reaching 21 completes the hand. Stand completes it. Double doubles its stake, draws exactly one card, then completes it. Split creates two hands from the original pair and debits one matching stake; deal one new card to each in order before continuing the first hand. Advance left to right through active hands. Split context survives subsequent resplits. No hit/double/resplit on split aces after their one added card.

A dealer natural ends the round before split/double can occur. Equal initial naturals push; dealer natural beats ordinary player 21; player natural beats a nonnatural dealer without further player actions. If all player hands bust, reveal the existing dealer cards and settle losses without unnecessary dealer draws.

## Net reward and returned chips

Let w be a hand's final stake, including double. Let R be net profit, not total returned chips. Stakes have already been debited.

| Outcome | Net profit R | Chips credited at settlement |
|---|---:|---:|
| Ordinary win | +w | 2w |
| Loss / bust | -w | 0 |
| Push | 0 | w |
| Eligible natural | +1.5w | 2.5w |

For initial wager b, round net profit = sum of hand profits. Proposed RL terminal round reward = round net profit / b. Ordinary actions give intermediate reward zero. A four-hand split round may yield rewards beyond [-1,1]; doubled hands can contribute ±2. Do not reuse the Foundations export validator's bounds or evaluator variance formula for these rewards.

Example: initial wager 10 chips. Split costs 10 more; double the first hand costs another 10. Total stake is 30. If the doubled hand wins and the other loses, net = +20-10 = +10. Settlement returns 40 chips, not 10; balance change from before the round is +10. Normalized reward is +10/10 = +1. This separates returned stake from profit.

Use exact integer arithmetic in half-chip units: natural profit is 3*w/2, which is integral for an even initial wager. Assert conservation: ending balance - starting balance equals net round profit. Settlement must be idempotent under repeated reads/rejected requests.

## Shoe lifecycle

Persistent shoe across rounds; 75% penetration triggers preparation before the next round only. No draw-time refill. The current Shoe primitive does not enforce phase, so the engine must own that boundary and never call prepare_round during play.

Before implementation completion, prove a conservative maximum-card requirement for the allowed hand/split rules, then enforce a between-round reserve sufficient for it in addition to penetration. Do not assume the 78 cards left at the cut threshold suffice without the proof. Exhaustion is an explicit error; it must never silently replace the shoe or partially settle a round. Handling an unexpected invariant failure requires transactional rollback or an explicit void-and-refund path preserving the starting balance; implement and test that path before enabling the profile.

## Visible information and agent compatibility

Expose visible rank/suit cards, player totals and split context, dealer upcard, active hand, legal actions and virtual balance. Conceal the hole card, private dealer total, remaining-card order and random seed. Reveal only when the round rules permit. The server computes legality and outcomes; clients submit intents, not state or payout claims.

A new observation schema must include decision-relevant split/double/natural context and legal-action masks. Exact hidden shoe composition is not an ordinary observation. No existing hit/stand policy is a full-game coach. Keep the Foundations profile and its exports unchanged.

## Implementation gates

Implement in small slices: round lifecycle and natural check; exact settlement; double; split and split aces; persistent shoe/reserve; visible snapshots and compatible policy integration. Each slice needs deterministic cases, invalid/stale command nonmutation, hidden-information checks and balance conservation before browser connection. The current Card, Shoe and hand_facts primitives are groundwork only; this contract is not a claim that the engine is complete.
