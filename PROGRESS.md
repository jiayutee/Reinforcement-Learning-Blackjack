# Progress

## 2026-09-20 — Planning checkpoint

- Inspected the existing project README, configuration, environment, dependency list, and directory structure.
- Found an existing Python RL/Pygame prototype; no implementation changes made.
- Created PROJECT_PLAN.md covering curriculum, algorithms, game rules, web architecture, evaluation, milestone acceptance, publishing, and GitHub workflow.
- Identified environment questions requiring an audit before trusting benchmark results.
- Verification: documentation planning only; no code tests run or claimed.
- GitHub status: NOT SAVED REMOTELY. Folder has no Git repository; destination is pending and local gh authentication reports an invalid token.
- Next: establish repository/access, preserve the prototype, then begin the setup and blackjack foundations lesson.

## Repository setup

- Confirmed repository: https://github.com/jiayutee/Reinforcement-Learning-Blackjack
- GitHub CLI access works with network permission; the earlier authentication result was not conclusive under the restricted environment.
- Updated the repository description to describe the learning project and planned web game.
- No hosted web game exists yet; the repository website field remains blank until a playable deployment is available.
- Prepared the existing source and planning documents for the initial GitHub checkpoint, excluding generated models, logs, caches, and environment files.
- No implementation changes or runtime test claims in this checkpoint.

## Lesson 1 — agent/environment foundations

- Added a dependency-free Foundations simulator with replacement draws, hit/stand, dealer standing on soft 17, and no natural bonus.
- Added seeded random and fixed-threshold players with readable transition traces and sample summaries. Neither player learns yet.
- Added a guided lesson, a small coding exercise, and separate worked answers; linked the course from README.
- Preserved the original prototype and clearly distinguished its rules and audit status.
- Verification: all 10 unittest cases passed on Python 3.9.19; the three-hand trace ran successfully. The fixed threshold policy produced 4,009 wins, 4,922 losses, and 1,069 pushes in 10,000 hands at seed 7 (mean return -0.0913). This is one descriptive run, not a statistical performance claim.
- M1 remains partial: Gymnasium cross-check and subsequent foundational lessons are pending. The public web game is not built or deployed.
- Next teaching checkpoint: user runs Lesson 1 and answers its comprehension questions, then we implement Monte Carlo value estimation.

## 2026-09-21, 03:00 checkpoint — Monte Carlo prediction

- Added `foundations/monte_carlo.py`: full-episode recording, undiscounted returns, first-visit incremental means, visit counts, a trace, and optional versioned JSON export with rules/policy/source provenance.
- Added Lesson 2 with prerequisite recap, worked numerical updates, Python explanations, experiments, exercises, and separate answers. The learner estimates values; the threshold policy deliberately remains fixed.
- Verification: 19 tests passed, including all 10 previous environment tests. The committed-source experiment runtime is recorded in the dated results JSON. New tests cover first-visit semantics, numerical averages, zero-return visits, terminal observation exclusion, parameter validation, reproducibility, and preservation of the earlier 10,000-hand baseline. CLI trace, sparse one-hand output, invalid input rejection, and documentation links were checked.
- At seed 7 / threshold 17 / 10,000 episodes: 4,009 wins, 4,922 losses, 1,069 pushes; mean return -0.0913. Selected state estimates are paired with visit counts; no claim of policy improvement or statistical significance.
- This checkpoint prepares exportable data for the future learning lab; no web interface or public deployment is claimed.
- GitHub checkpoint: implementation and lesson prepared for commit; the subsequent dated experiment record will identify the exact committed source. Push status must be verified before reporting remote completion.
- Next overnight checkpoint: keep this as the night's central lesson; strengthen the rule/reference verification and presentation rather than racing ahead to unrelated algorithms. M1's Gymnasium cross-check remains pending, and the policy has not learned to choose actions yet.

### 2026-09-21 late finalization

- Latest clock check was 17:20 Europe/Berlin, outside the scheduled work window; stopped development and prepared only the completed-work summary and GitHub checkpoint. The 06:00 delivery deadline was missed.
- Source checkpoint: [a0fe44b](https://github.com/jiayutee/Reinforcement-Learning-Blackjack/commit/a0fe44b4bd9aedbe6824ab5818a91ba747d75663). Generated seven descriptive experiment records from that committed, clean source; runtime Python 3.9.6.
- Morning lesson: [21 September](docs/daily/2026-09-21.md). Saved experiment configs/results in `experiments/2026-09-21-monte-carlo.json`. No trained action policy, Gymnasium equivalence, or hosted game is claimed.
- Summary prepared for this task now; later delayed wakeups should not send a duplicate summary for this date. Push confirmation is recorded by the task's tool result after the documentation commit.

## 2026-09-22, 04:00 checkpoint — verify rules before extending learning

- Preserved the user's uncommitted answers in `docs/lessons/01-agent-environment.md`; they are not part of this automation's commits.
- Added an optional reference checker against installed Gymnasium 1.1.1 with `natural=False, sab=False`. Core Foundations lessons remain dependency-free; optional installation is documented in `requirements-reference.txt`.
- Verification: all 21 tests passed, including 8,007 hand-score comparisons for rank combinations of lengths 1–6 and 13 legal transitions across 10 scripted cases. Exact tests compare draw counts and final hands as well as observations, rewards, and termination.
- Scope of proof: the rank distribution and the tested hand/transition cases match. Random-number streams, reset draw order, rendering, API signatures, and invalid/post-terminal action handling are not claimed equivalent.
- Next in this bounded checkpoint: run independent seeded samples for random and threshold policies, save descriptive results and the dated teaching note, then push only the automation's changes. Final morning summary remains scheduled for 06:00.

### 2026-09-22 reference experiment completed

- Source [5e50777](https://github.com/jiayutee/Reinforcement-Learning-Blackjack/commit/5e50777db550d2c0f63fc2cf69026018249c083b); Python 3.9.6, Gymnasium 1.1.1, NumPy 2.0.2, clean Foundations source. Ran 400,000 total hands covering random and threshold policies, five seeds, and both implementations. Saved results to `experiments/2026-09-22-gymnasium-reference.json`.
- Largest individual mean-return difference approximately 0.0259, difference SE approximately 0.0094. These are descriptive diagnostics, not a stochastic equivalence gate. Exact fixture checks passed separately.
- Prepared [the 22 September learning note](docs/daily/2026-09-22.md), with policy/value explanations, feedback on the user's answers, reproduction commands, an exercise, and separate solutions. No final morning summary sent yet; 06:00 checkpoint should deliver it once.
- Preserved the user's uncommitted Lesson 1 edit. Next: small presentation support for this lesson, then action-value learning in a future lesson. The public web game is still pending.

## 2026-09-22, 05:00 checkpoint — visual value-map preview

- Added a dependency-free offline HTML renderer for the existing Monte Carlo JSON export. It displays hard/soft state values, per-state visit counts, selected-position explanations, and a minimum-visit filter. It explicitly distinguishes unknown/filtered values from zero and fixed-policy actions from learned recommendations.
- All 26 Python tests passed (including the optional reference checks). New tests verify data preservation, incompatible-rule rejection, invalid/duplicate estimates, summary consistency, and safe embedding of metadata containing HTML delimiters.
- Automated browser checks passed using installed Chrome in an isolated temporary profile: 180 cells per hand type, displayed values/counts, keyboard selection, hard/soft switching, minimum-visit filtering, unknown states, 390px mobile layout, no page errors, and no network requests. The bundled Playwright browser was absent, so installed Chrome was used. Screenshot files were captured, but the image inspection tool could not display them; visual appearance is not claimed manually reviewed.
- The user's uncommitted Lesson 1 answers remain untouched and excluded from commits. No changes to game rules, policies, or training behavior were needed. This is a local learning-lab preview, not a hosted game.
- Next: save the ready-to-open seeded snapshot and instructions in today's learning note, push the checkpoint, and leave the final morning summary for 06:00.

### 05:00 visual checkpoint prepared

- Source [14fedf6](https://github.com/jiayutee/Reinforcement-Learning-Blackjack/commit/14fedf619dff6cdf2952723a92b1ad8ade85b36b); generated `docs/previews/monte-carlo-values.html` from a clean-source, 10,000-hand seed-7 threshold-17 export. It contains the experiment metadata and source commit.
- Updated today's daily note and README with local-open instructions, generation commands, interpretation, a hard/soft visit-count exercise, and verification limits.
- Final summary has not yet been sent for 22 September. At 06:00, link the daily note and local preview, report 26 tests and browser checks, and include the confirmed GitHub checkpoint. Avoid duplicate summaries afterward.

## 2026-09-25, 03:00 checkpoint — Monte Carlo action learning

- Found no completed source checkpoints for 23–24 September; the last saved checkpoint was 22 September. No cause for the missed work is established.
- Added first-visit epsilon-greedy Monte Carlo control: separate state-action means/counts, random training tie-breaking, episode-end updates, and a frozen greedy evaluation with deterministic stand ties. Uses existing environment and return calculation.
- Added Lesson 3 with prerequisites, equations, worked examples, Python walkthrough, exploration probabilities, evaluation limits, and separate solutions. Control exports are distinct from the existing state-value map format.
- All 33 tests passed. Seven new tests cover state-action updates, exploration/exploitation, tie behavior, reproducibility, parameter checks, and non-mutating evaluation. User Lesson 1 edits remain untouched and excluded.
- First preview: train 50,000 hands, seed 7, epsilon 0.1; evaluate 20,000 hands per policy at seed 1,000,007. Learned mean -0.06935, threshold -0.08195, random -0.38865. One training seed is preliminary, not proof of superiority or optimality. Reproduce from committed source before saving the result record.
- Next checkpoint: several independent training seeds at the same prespecified settings; retain this as tonight's main lesson. No 25 September final morning summary has been sent yet.
