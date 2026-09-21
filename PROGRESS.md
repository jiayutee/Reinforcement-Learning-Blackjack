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
- Verification: 19 tests passed on Python 3.9.19, including all 10 previous environment tests. New tests cover first-visit semantics, numerical averages, zero-return visits, terminal observation exclusion, parameter validation, reproducibility, and preservation of the earlier 10,000-hand baseline. CLI trace, sparse one-hand output, invalid input rejection, and documentation links were checked.
- At seed 7 / threshold 17 / 10,000 episodes: 4,009 wins, 4,922 losses, 1,069 pushes; mean return -0.0913. Selected state estimates are paired with visit counts; no claim of policy improvement or statistical significance.
- This checkpoint prepares exportable data for the future learning lab; no web interface or public deployment is claimed.
- GitHub checkpoint: implementation and lesson prepared for commit; the subsequent dated experiment record will identify the exact committed source. Push status must be verified before reporting remote completion.
- Next overnight checkpoint: keep this as the night's central lesson; strengthen the rule/reference verification and presentation rather than racing ahead to unrelated algorithms. M1's Gymnasium cross-check remains pending, and the policy has not learned to choose actions yet.
