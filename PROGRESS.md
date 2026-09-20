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
