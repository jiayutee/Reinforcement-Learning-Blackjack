# Blackjack RL: learning curriculum and public web platform

Status: proposed plan, 20 September 2026. No implementation changes made.

## 1. Outcomes and working assumptions

Build three connected deliverables:

1. A step-by-step course in reinforcement learning (RL), probability, and implementation.
2. Reproducible blackjack agents whose decisions and learning can be inspected.
3. A polished, responsive public web game with graphics, sound, and an optional AI coach.

Start with free play and virtual chips. Assume one human player against a fixed-rule dealer, desktop and mobile browser support, guest access, and local training. Accounts, multiplayer, real-money play, paid infrastructure, and public training jobs are outside the first release. Hosting provider and budget remain open.

Teaching pace depends on the user's Python, JavaScript, and probability experience. Work in small lessons rather than delivering an unexplained finished codebase. Each milestone should be runnable independently.

## 2. Existing project and reuse

The folder contains a Python environment, DQN and policy-gradient agents, adversarial training, training/evaluation scripts, and a Pygame interface. It is not currently a Git repository. The GitHub CLI has an invalid authentication token; repository destination is pending.

Preserve the prototype as a baseline before changes. Audit agents and training code before reusing them; their presence is not evidence of correctness. Keep the Pygame interface as a historical demo rather than maintaining two polished frontends.

Observed environment concerns to address:

- Legacy Gym reset/step interfaces need a planned Gymnasium migration.
- Natural blackjack is not distinguished correctly from ordinary 21 in all outcomes.
- Reset recreates a six-deck shoe, despite comments suggesting persistent shoe behavior.
- The compact observation omits shoe composition; finite-deck play is not exactly Markov under that observation.
- An adaptive dealer changes the game and is not the standard blackjack benchmark.

## 3. Two explicit rule profiles

### Foundations profile

Use Gymnasium Blackjack-v1 with explicitly recorded `natural=False, sab=False`: draws with replacement, hit/stand, dealer stands on 17, rewards +1/0/-1. This is a deliberately simplified teaching environment. Use the observation (player total, dealer upcard, usable ace), and gamma=1 for undiscounted episodic return.

Build and explain a small equivalent simulator, then compare seeded statistical behavior and targeted cases with the reference environment. Identical RNG streams are not required across implementations.

### Public game profile

Proposed initial rules: six-deck shoe; dealer stands on soft 17; American hole-card and natural check; natural blackjack pays 3:2; equal naturals push; ordinary wins pay 1:1; double on the initial two cards; equal-rank split; maximum four hands; double after split; split aces receive one card each and cannot resplit; split-hand 21 pays 1:1; no insurance or surrender. Reshuffle between rounds at a declared penetration threshold, never arbitrarily during a hand.

Document these as product choices before implementing them. Legal actions, bankroll constraints, payouts, round settlement, and split-hand rewards must be explicit. The browser must not receive the dealer's hidden card before reveal.

Do not silently use a hit/stand agent as a full-game expert. Train and evaluate a policy for the public rules before enabling full-game AI advice. Expanded observations include hand/pair information, split context, and legal actions. Explain partial observability for a finite shoe; card counting and belief-state methods are later extensions.

## 4. Lesson format

Every lesson follows: intuition -> definitions -> one hand-worked example -> small coding exercise -> runnable experiment -> interpretation -> short comprehension check -> GitHub checkpoint.

Provide a lesson document, runnable Python module, optional notebook for exploration, focused tests, and a progress entry. Explain prerequisites just before use: functions, dictionaries, arrays, random seeds, expectations, conditional probability, and gradients. Keep solutions separate from exercises.

The central conceptual loop is observation -> action -> reward -> next observation. Explain environment state versus agent observation, episode versus training run, policy versus value function, and training versus evaluation before introducing neural networks.

## 5. Curriculum and algorithm choices

| Lesson | Theory | Coding deliverable | Evidence of understanding/completion |
|---|---|---|---|
| 0 | Setup, Python essentials, reproducibility | Run preserved prototype and a seeded random policy | Reproduce a run and explain its inputs/outputs |
| 1 | Blackjack rules; agent/environment boundary | Hand scoring and deterministic example rounds | Explain soft aces, naturals, pushes, and legal actions |
| 2 | MDPs, return, policy, value, expected reward | Episode recorder and fixed policies | Trace observations/actions/rewards without hidden-card access |
| 3 | Model-based planning and Bellman equations | Small worked MDP; blackjack reference solver when useful | Hand-calculate a backup and distinguish planning from learning |
| 4 | Monte Carlo prediction and control | First-visit value estimates, epsilon-greedy control | Plot sample counts and learned hard/soft-hand policy tables |
| 5 | TD prediction, bootstrapping, bias/variance | TD(0) and SARSA | Explain learning before an episode ends and on-policy targets |
| 6 | Off-policy learning and exploration | Tabular Q-learning, then Expected SARSA comparison | Hand-calculate an update and explain SARSA/Q-learning differences |
| 7 | Experimental design | Multi-seed evaluation harness and reference comparison | Distinguish noise from a supported improvement |
| 8 | Approximation and the deadly triad | DQN, replay buffer, target network; optional Double DQN | Show terminal masking, correct targets, and comparison to tables |
| 9 | Policy gradients, baseline, advantage | REINFORCE with baseline, then an actor-critic lesson | Explain variance and why actions are sampled during training |
| 10 | Practical policy optimization | Optional PPO experiment using a maintained library | Compare cost, stability, and return without assuming newer is better |
| 11 | Distribution shift and partial observability | Extend to public rules and inspect policy failures | Demonstrate action masking and rules-compatible evaluation |

Tabular Monte Carlo and Q-learning are the core deliverables: transparent and well matched to a small state space. SARSA and Expected SARSA teach useful target differences. DQN is an educational extension for larger observations, not an assumed upgrade. REINFORCE introduces policy gradients; actor-critic and PPO extend that foundation. Continuous-action algorithms such as SAC/TD3 are not priorities for hit/stand blackjack. Adversarial dealers and self-play remain explicitly labeled alternative-game experiments.

Example Q-learning equation to unpack term by term:

`Q(s,a) <- Q(s,a) + alpha * [r + gamma * max_a' Q(s',a') - Q(s,a)]`

For terminal transitions the bootstrap term is zero. Explain the distinction between termination and truncation when implementing environment wrappers.

## 6. Evaluation: what makes the bot good?

Optimize mean net reward per initial wager, with all split/double stakes accounted for. Win rate alone is insufficient. Do not promise positive expected profit or a particular winning percentage.

- Compare random, fixed threshold, rule-matched reference strategy, and learned policies.
- Freeze policies for evaluation and disable exploratory actions for greedy value policies. Record the policy-gradient evaluation mode explicitly.
- Use separate training/evaluation seeds and several independent training seeds; begin with at least five for comparisons.
- Report mean return, uncertainty intervals, win/loss/push rates, training steps, runtime, and hard/soft policy maps. Inspect rare states and visit counts.
- Distinguish evaluation-sampling uncertainty from variation across training seeds. For persistent shoes, account for within-shoe dependence rather than treating all hands as independent.
- Record rules version, observation/action schema, seed, dependencies, hyperparameters, Git commit, and policy version for every experiment.
- Define a target gap to the rule-matched reference after obtaining a measured baseline; do not invent an accuracy target upfront.

Never mix results from incompatible rule profiles. Use held-out evaluation for final claims, not repeated parameter tuning.

## 7. Proposed architecture

Python owns the authoritative rules engine, Gymnasium adapter, training, evaluation, and policy inference. React with TypeScript and Vite provides the web interface; FastAPI connects game sessions and policies to the browser. Begin with request/response actions; add WebSockets only if a demonstrated feature needs them.

Use one public-game Python rules implementation for training and web play, with thin adapters. The Foundations profile remains an explicitly different benchmark. Train offline; deploy versioned frozen policies. Never retrain on every web request.

Initially use no account database. Define a bounded guest-session lifetime and restart behavior. Backend validates action legality and owns chips, hand state, and outcomes. Prevent duplicate action submissions from settling a round twice. Do not treat client-provided results as authoritative.

Suggested eventual structure (migrate incrementally):

```text
docs/lessons/        theory, exercises, worked solutions
docs/decisions/      rules and architecture decisions
environment/        shared rules and Gymnasium adapters
rl_agent/           tabular and neural agents
training/           training and evaluation entry points
apps/api/           web sessions and policy inference
apps/web/           table, coach, and learning lab
tests/              rules, agent updates, API, browser journeys
experiments/        small configs and result summaries
```

Pin compatible dependency versions when implementing; avoid speculative infrastructure. Add persistence, distributed sessions, and accounts only when a concrete release requirement needs them.

## 8. Web experience

Three views share the same game concepts:

- **Play:** green felt, readable cards, chip stacks, clear bets and payouts, deal/flip/chip animations, responsive touch controls, rule summary, and hand history.
- **Watch the bot:** pause, single-step, speed controls, selected action, Q-values or policy probabilities, and a plain-language explanation. Values are expected returns, not automatically win probabilities.
- **Learning lab:** lesson navigation, policy heatmaps, saved training curves, and comparisons of checkpoints. Start with precomputed results; defer unrestricted public training.

Sound design includes card deals, chip movement, and restrained outcome cues. Enable audio after a user gesture, include mute/volume controls, and persist preferences. Provide reduced motion, keyboard controls, visible focus, screen-reader outcome announcements, and information that does not depend solely on sound or color. Use original or appropriately licensed assets with an attribution manifest.

Build an attractive playable table early; reserve elaborate visual polish until game flow is correct. Avoid showing implementation jargon in ordinary Play mode.

## 9. Delivery milestones and exit criteria

| Milestone | Deliverable | Exit criteria |
|---|---|---|
| M0: plan and preservation | GitHub baseline, this plan, progress log, agreed rules | Existing files preserved; repository confirmed; baseline pushed |
| M1: correct foundations | Lessons 0-2, simplified simulator, rules fixtures | Ace/terminal/reward tests pass; seeded random run reproducible |
| M2: first learning bot | Monte Carlo and Q-learning lessons, tables, evaluation | Learning visible; evaluation separated; comparisons reproducible |
| M3: playable web alpha | Python API, responsive table, frozen compatible bot | Human and bot complete legal rounds; hidden information stays hidden |
| M4: realistic blackjack | Public rule profile, doubles/splits, matching observations/policy | Settlement/action tests pass; incompatible policies rejected |
| M5: teaching platform | Coach, lesson pages, heatmaps, optional neural lessons | User can inspect a decision and reproduce its training experiment |
| M6: public beta | Graphics/audio polish, accessibility, deployment | Browser journeys, build, production smoke test, and rollback pass |

M0-M2 establish the scientific foundation. M3 can start once the first agent and game contracts are stable; later algorithm lessons need not delay the first playable web release. Split M4 into smaller lessons if its rules overwhelm the learning pace. Estimate schedules after the baseline audit and user skill assessment rather than committing to an arbitrary deadline.

## 10. Quality and publishing

Rules tests cover multi-ace hands, naturals versus multi-card 21, dealer behavior, busts, pushes, doubles, split restrictions, wager accounting, shuffle boundaries, and terminal actions. Agent tests check numerical updates and terminal bootstrap handling. API/browser tests cover hidden-card secrecy, invalid/duplicate actions, complete rounds, reconnect behavior, mobile layout, mute, and keyboard operation.

GitHub Actions should run focused Python tests, frontend type/build checks, and essential browser journeys. Keep stochastic training benchmarks separate from quick deterministic CI; use scheduled/manual benchmark runs when needed.

Deployment plan: production frontend and Python service, HTTPS, explicit origins, rate/session limits, error reporting, bounded resource use, health checks, environment configuration, and a tested previous-version rollback. Select hosting based on cost and Python service support at the deployment milestone. Define concurrent-user and latency targets before load testing. Keep secrets out of git and record asset licenses. Add data retention and privacy details if analytics/accounts are later introduced.

## 11. GitHub progress policy

Save each completed coherent lesson or milestone with a meaningful commit and push. Use feature branches and reviewable pull requests for substantial work. Update PROGRESS.md with what changed, what ran, results, the lesson checkpoint, and next work. Tag runnable milestones.

Before the first commit, review the existing tree for secrets and generated files; do not blindly add everything. Exclude caches, virtual environments, secrets, bulky logs, and model checkpoints. Keep small configs/metrics in git and publish larger models as appropriate release artifacts with provenance.

A local file or commit is not a GitHub save. Report successful pushes with links; if authentication/network/repository access fails, explicitly state which checkpoint remains local. Preserve work locally and resolve the blocker before describing it as saved on GitHub.

## 12. Immediate next session

1. Confirm repository destination and establish working GitHub access.
2. Preserve and publish the current prototype plus plan as the baseline.
3. Assess coding prerequisites and teach Lesson 0.
4. Audit the environment and write the first deterministic rule examples together.
5. End with a runnable exercise, explanation, progress entry, and pushed checkpoint.

## Sources

- Gymnasium Blackjack reference: https://gymnasium.farama.org/environments/toy_text/blackjack/
- Sutton and Barto, Reinforcement Learning: An Introduction: http://www.incompleteideas.net/book/RLbook2020.pdf (linked by the Gymnasium reference).
- Stable-Baselines3 evaluation and algorithm guidance: https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html
