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

### 25 September first control experiment recorded

- Reproduced the first sample from committed source [4b93436](https://github.com/jiayutee/Reinforcement-Learning-Blackjack/commit/4b93436ee3b28707febf9b2c0f099bd8b90177fb); Python 3.9.6, clean Foundations source. Saved compact results in `experiments/2026-09-25-monte-carlo-control.json` and prepared the dated lesson.
- Learned-policy evaluation selected no unvisited actions in this sample. Near-tied estimates and single-seed uncertainty remain explicit limitations; no optimality claim.
- 04:00 next: multi-seed replication at unchanged settings. The 25 September morning summary is still pending for 06:00.

## 2026-09-25, 04:00 checkpoint — multi-seed replication

- Repeated unchanged control settings for seeds 7, 19, 42, 101, 2026: 50,000 training hands, epsilon 0.1, and 20,000 evaluation hands per policy at seed 1,000,000 + training seed. Seed 7 repeats the previous sample and is counted once.
- Mean learned return -0.07400; threshold -0.07970; random -0.39771. Learned run means ranged -0.08550 to -0.06375; sample SD 0.00834 mixes training variation and evaluation noise. Learned seed 19 was worse than threshold. No claim of reliable threshold superiority, optimality, or positive profit.
- Saved `experiments/2026-09-25-control-multiseed.json` and updated the daily note with all rows, interpretation, and exact reproduction commands. Source [45ec0ca](https://github.com/jiayutee/Reinforcement-Learning-Blackjack/commit/45ec0ca3f9773dd31bbd7585d5d651f70efc3338), clean Foundations source. No product code changed; prior 33-test proof remains current.
- Preserved the user's Lesson 1 answers. Next checkpoint may add a small action-table presentation; final summary remains pending for 06:00 on 25 September.

## 2026-09-25, 05:00 checkpoint — evidence-labelled action table

- Added `foundations/policy_table.py` and the ready-to-read `docs/previews/monte-carlo-policy.md`. This renders a full control export as hard/soft decision tables with per-action evidence for selected states. It is separate from the V(s) heatmap and does not change the agent.
- Marks a choice when either action has fewer than the requested visit count, distinguishes untried/absent entries, validates stored greedy choices against Q estimates, and preserves unknown source provenance explicitly.
- All 39 tests passed; six new tests cover evidence handling and validation. CLI output matched the saved seed-7 estimates and the checked Markdown output. No browser behavior or gameplay changes are claimed.
- Updated today's daily note and README with a soft-18 evidence exercise and reproduction commands. Data provenance remains the original clean-source control checkpoint 4b93436; the renderer is new in this checkpoint.
- Preserved and excluded the user's local Lesson 1 answers. The 06:00 summary should link Lesson 3, today's five-seed results, and the policy table, report 39 passing tests, and state that advantage over threshold is not established. No final summary for 25 September has been sent yet.

## 2026-09-26, 03:00 checkpoint — TD(0) prediction

- Added `foundations/td.py`: online fixed-policy prediction, explicit terminal masking, constant alpha, per-transition counts, and a first-hand arithmetic trace. Kept the artifact distinct from MC exports.
- Added Lesson 4, separate solutions, README entry, and today's daily note. Recaps foundations and distinguishes prediction from control, sample means from constant-alpha estimates, and terminal pushes from unfinished zero rewards.
- All 45 tests passed, including six new TD tests. Seed-7/10,000 preview outcomes match MC exactly, as expected for the same fixed policy; value estimates differ. No accuracy or policy-improvement claim.
- Preserved user Lesson 1 edits. Commit and reproduce from clean source next; later checkpoints should keep this as tonight's coherent lesson. No September 26 morning summary sent yet.

- TD source checkpoint `b7fadb6` successfully pushed. Reproduced the stated 10,000-hand results from clean committed source and saved `experiments/2026-09-26-td-prediction.json` with provenance. Next: a bounded estimator comparison/presentation checkpoint at 04:00; do not interpret equal policy returns as equal value accuracy.

## 2026-09-26, 04:00 checkpoint — compare prediction updates

- Ran fixed MC/TD(0) comparisons with 10,000 hands per seed for seeds 7, 19, 42, 101, 2026 and TD alpha 0.1/0.05. Saved the runnable script and selected-state record with clean-source provenance (73f8723).
- Asserted identical outcomes across estimators within each seed. 50,000 distinct seeded hands replayed three ways, not 150,000 independent observations. Hard-20 estimates demonstrate constant-alpha weighting even without bootstrapping; rare soft-state counts were 6–14.
- Updated today's note and separate exercise answers. No accuracy ranking or policy improvement claimed; no algorithm code changed. Previous 45-test proof remains applicable; comparison assertions passed.
- Preserved Lesson 1 user edits. Next: a bounded browser explanation of one TD update, then the 06:00 summary. September 26 final summary remains pending.

## 2026-09-26, 05:00 checkpoint — interactive TD arithmetic

- Added `docs/previews/td-update.html`, an offline responsive learning exercise showing target, error, and one updated value. Terminal transitions visibly disable the next-state estimate; nonzero blackjack rewards force termination. No server or game deployment.
- Headless Chrome checks passed: default/terminal arithmetic, bootstrap restore, invalid alpha, reset, keyboard Space, 390px no horizontal page overflow, no JS errors or HTTP requests. No full accessibility audit or manual visual review claimed. Python source unchanged; prior 45-test proof remains current.
- Updated README and today's note with opening instructions and a terminal-zero-reward exercise. User Lesson 1 answers preserved and excluded.
- At 06:00 link Lesson 4, today's comparison, and the browser exercise; explain bootstrapping and constant-alpha limitations, include confirmed commits. September 26 morning summary has not yet been sent.

## 2026-09-28, first checkpoint — SARSA

- No completed September 27 checkpoint found; cause unknown. September 26 summary was delivered in the task (superseding its pending-summary notes).
- Added one-step on-policy SARSA with selected-action targets, terminal masking, carried-forward next actions, separate evaluation seeds, trace and distinct export type. Reused existing exploration and frozen evaluator.
- Added Lesson 5, separate solutions, daily note, README link. All 50 tests passed, including five SARSA tests. Preliminary seed-7 greedy mean -0.05540; no general superiority claim from a single training run.
- Preserved the user’s Lesson 1 edits. Next: record clean-source results, then replicate unchanged settings at the next checkpoint. No September 28 morning summary sent yet.

- Source `176a2ab` pushed successfully; clean-source reproduction matched the preview. Saved `experiments/2026-09-28-sarsa.json`.

## 2026-09-29, 03:00 checkpoint — SARSA replication

- Repeated unchanged alpha/epsilon=0.1, 50,000 training hands and 20,000 evaluation hands per policy for seeds 7,19,42,101,2026. Saved compact records and a beginner-friendly daily lesson with equations, reproduction commands and separate answers.
- Greedy mean -0.06249, threshold -0.07970, random -0.39771. Greedy run-mean sample SD 0.006905 combines training and evaluation noise. All five greedy runs exceeded threshold, but this small reused-seed experiment is not proof of optimality or a fresh final benchmark.
- Source b150217 had clean Foundations code; seed 7 reproduced the earlier result. Algorithm code unchanged, prior 50-test proof remains applicable. User Lesson 1 edits preserved.
- September 28 summary was delivered late; September 29 summary pending for 06:00. Next: inspect SARSA action evidence in the learning interface.

## 2026-09-29, 04:00 checkpoint — SARSA policy evidence

- Extended the existing policy-table renderer to accept explicit SARSA exports with validated alpha and algorithm-specific explanations, preserving MC support and unknown/low-count warnings.
- Generated `docs/previews/sarsa-policy.md` from the original clean-source seed-7 export (176a2ab), not an aggregate policy. Linked the snapshot and added an evidence exercise and separate answer.
- All 52 tests passed; actual export rendered successfully. No browser behavior or game deployment changes. User Lesson 1 edits preserved and excluded.
- Next checkpoint can improve lesson navigation/presentation; keep replication and evidence interpretation as tonight's focus. September 29 morning summary remains pending.

## 2026-09-29, 05:00 checkpoint — learning hub

- Added a static local learning hub linking ordered GitHub lessons, offline HTML exercises, and evidence tables. Clearly distinguishes online reading from offline interaction and unfinished public gameplay.
- Verified all 10 links map to existing project files; no remote availability, visual or accessibility audit claimed. Algorithm code unchanged; prior 52-test result remains current.
- Updated README and daily note. User Lesson 1 answers untouched. At 06:00 summarize replication, policy evidence, hub opening command, and confirmed commits. No September 29 morning summary sent yet.

## 2026-09-30, 03:00 checkpoint — Q-learning

- Added explicit off-policy Q-learning with max-next-Q targets, terminal masking, epsilon-greedy behavior, trace and a distinct export type. Reused environment/exploration/evaluation; no existing algorithm changes.
- Added Lesson 6, separate answers, daily record and README link. All 57 tests passed, including five new Q-learning tests.
- Seed-7 preview greedy mean -0.08295 versus threshold -0.08195. No superiority/inferiority inference from one seed. Next: clean-source reproduction, multi-seed replication, correctly labelled evidence.
- User Lesson 1 edits preserved. September 29 summary delivered; September 30 summary pending for 06:00.

- Source `8124f26` successfully pushed. Clean-source results reproduced and recorded in `experiments/2026-09-30-q-learning.json`.

## 2026-09-30, 04:00 checkpoint — Q-learning replication

- Ran unchanged settings across seeds 7,19,42,101,2026; saved compact records with clean-source provenance (36bbe25), reproduction commands and an interpretation exercise with separate answers.
- Greedy mean -0.06923 versus threshold -0.07970; three runs better, two worse. Greedy run-mean SD 0.009453 mixes training and evaluation noise. No superiority or algorithm-ranking claim; reused evaluation seeds are not a fresh final benchmark.
- Seed 7 reproduced the earlier result. No algorithm changes; prior 57-test proof remains current. User Lesson 1 edits preserved.
- Next: Q-learning-labelled policy evidence. September 30 morning summary pending for 06:00.

## 2026-09-30, 05:00 checkpoint — Q-learning policy evidence

- Extended the existing policy renderer with explicit Q-learning labels and alpha validation; preserved MC/SARSA behavior. Generated a seed-7 snapshot from clean source 8124f26 and linked it and Lesson 6 in the learning hub.
- All 58 tests passed; real-export CLI rendering succeeded. Checked hub links against project files; no browser visual audit claimed. Added count-warning exercise with separate answer.
- User Lesson 1 edits excluded. At 06:00 link Lesson 6, replication, snapshot/hub; report five-seed mean -0.06923 vs threshold -0.07970 without established superiority, tests and commits. September 30 summary remains pending.

## 2026-10-01, 03:00 checkpoint — visible hand boundary

- Started the web-game bridge with `Blackjack.visible_hand()`: detached JSON-ready visible values, hidden dealer card/total before termination, reveal afterward, and legal actions/rule label. No changes to training observations or transitions.
- Added a beginner lesson in today's daily note connecting internal state, RL observation and browser disclosure, with runnable experiment, worked ace scoring and separate answers.
- All 62 tests passed. New checks cover hidden-card noninterference, reveal, copy isolation and unchanged seeded transitions. User Lesson 1 edits preserved.
- This is an in-process Foundations view, not a web API, full public rules or deployment. Next: a bounded local playable teaching interface. September 30 summary delivered; October 1 summary pending.

## 2026-10-01, 04:00 checkpoint — round controller

- Added transport-independent GameSession owning the environment, phase validation, revision checks, visible snapshots and final reward. Repeated/stale commands fail before mutation; no client-supplied cards or settlement.
- Added runnable terminal game and daily explanations connecting revisions, duplicate intent and observations. All 66 tests passed; seed-7 deal/hit/stand produces soft 20 against 17, reward +1 at revision 3.
- Explicitly not yet concurrent, authenticated, persisted or served over HTTP. Browser connection remains next. User Lesson 1 edits preserved; October 1 summary pending.

## 2026-10-01, 05:00 checkpoint — local playable browser

- Added a loopback-only single-session standard-library server and responsive value-card table over the existing GameSession. Explicit local teaching scope; production React/FastAPI architecture remains planned.
- Server owns cards/actions/results, serializes commands, validates Host/origin/token and revision, and exposes only visible-hand snapshots. Browser disables in-flight actions and does not retry stale commands automatically.
- Browser checks passed for a complete seed-7 win, response-level concealment, reveal, keyboard Enter, unauthorized POST rejection, mobile width and JS errors. All 66 Python tests passed. Temporary browser check only; no permanent browser gate/manual visual audit claimed. Test server stopped.
- User Lesson 1 edits excluded. At 06:00 summarize visible information, session revisions, local launch command, limitations, tests and confirmed commits. No October 1 morning summary sent yet.

## 2026-10-02, 03:00 checkpoint — frozen-policy inference

- Added validated frozen control-export loader and CLI advice using the existing rule/artifact checks. Copies internal data, returns both values/counts, withholds absent/unvisited comparisons, and never trains or reads environment internals.
- Added today's lesson with decision arithmetic, runnable export/inference commands, limitations, exercises and separate answers. Explicitly distinguishes advice withholding from evaluator zero-initialization fallback.
- All 70 tests passed; real saved Q-learning export reproduced hard-20 stand advice and counts. No quality improvement claim. User Lesson 1 edits preserved.
- Next: connect optional advice to local visible observations, without exposing hidden cards or changing training. October 1 summary delivered; October 2 summary pending.

## 2026-10-02, 04:00 checkpoint — optional browser advisor

- Added --policy loading at local-server startup, visible-observation-only table advice, and a browser evidence panel. No retraining, automatic action or game mutation on reads; terminal hands suppress advice.
- All 72 tests passed. Headless browser verified initial/active/terminal advice, concealed dealer response, unchanged state on refresh and no JS errors. Test server stopped. Manual play remains available without a policy.
- Updated daily instructions and README; user Lesson 1 edits preserved. Next: repeatable browser checks including optional/missing evidence paths. October 2 summary pending.

## 2026-10-02, 05:00 checkpoint — repeatable browser gate

- Saved an optional Playwright integration script with temporary synthetic policy fixtures and isolated loopback servers. Documented external runtime requirements; no installation or CI provisioning implied.
- All three manual/known/missing-advice scenarios passed complete play, evidence/terminal states, concealed responses, nonmutating refresh, stale duplicate rejection, unauthorized POST, keyboard, mobile overflow and JS-error checks. Test resources cleaned up.
- No product-code changes; prior 72 Python tests remain current. User Lesson 1 edits preserved. At 06:00 summarize frozen inference, launch commands, browser gate and confirmed commits. October 2 summary pending.

## 2026-10-03, 03:00 checkpoint — one-action bot execution

- Added server-side bot command dispatch using visible frozen advice and the same revision-checked session path as manual actions. Rejects stale, missing-evidence and terminal bot commands without mutation; executes at most one action.
- Added today's lesson connecting observation/action/reward to frozen inference, deterministic worked example and separate exercise answers. All 75 tests passed; no new agent-quality claim.
- Browser button and repeatable browser coverage are next. User Lesson 1 edits preserved. October 2 summary delivered; October 3 summary pending for 06:00.

## 2026-10-03, 04:00 checkpoint — browser Bot step

- Added Bot step with active-hand/evidence/in-flight gating and clear one-action behavior. Server computes the action; manual play remains available.
- All 75 Python tests and three repeatable browser scenarios passed. Known fixture uses keyboard Bot step, confirms one transition, stops on unknown next-state evidence, and rejects replayed stale bot revision without mutation. Test resources cleaned up.
- Updated lesson, README and gate documentation. User Lesson 1 edits preserved. Next possible checkpoint: make the last executed action visible so new-state advice is not confused with the previous choice. October 3 summary pending.

## 2026-10-03, 05:00 checkpoint — last accepted action

- Session now exposes last accepted deal/hit/stand; browser labels it separately from current advice. Rejected requests do not rewrite history; new deals reset the label to deal. No full log or actor attribution claimed.
- All 76 Python tests and three browser scenarios passed, including history and bot/manual hit/stand labels. Initial review timed out before execution; one permitted retry succeeded. User Lesson 1 edits preserved.
- At 06:00 link today's lesson, explain frozen one-step execution, provide policy/server commands, report checks and confirmed commits. October 3 summary pending.

## 2026-10-04, 03:00 checkpoint — current-hand episode trace

- Session now records detached visible-observation/action/reward/next-observation/done rows for accepted learning actions. New deal clears rows; rejected commands and reads leave them unchanged. No hidden dealer data or training updates included.
- Added beginner lesson, return arithmetic, runnable exact seed-7 example and separate answers. All 77 tests passed, including trace/reset/copy/terminal checks; user Lesson 1 edits preserved.
- Next: browser trace presentation and focused verification. October 3 summary delivered; October 4 summary pending.

## 2026-10-04, 04:00 checkpoint — browser episode trace

- Added an expandable readable current-hand trace. Returns are pending while active and computed backward with gamma=1 only after termination; no agent updates. New deal clears it.
- All 77 Python tests and three browser scenarios passed, including pending/completed return labels, two winning transitions and reset, plus existing gates. User Lesson 1 edits preserved.
- Next: negative/zero-return examples and focused tests. October 4 morning summary pending.

## 2026-10-04, 05:00 checkpoint — terminal loss/push coverage

- Extended the repeatable browser gate with seed-0 standing loss and seed-6 standing push. Checks final reward, one terminal trace row, negative/zero completed return, disabled actions and JS errors.
- All five browser scenarios passed; resources cleaned up. No product changes; prior 77-test Python proof remains current. Documented runnable examples and why outcome-selected seeds are not evaluation evidence.
- User Lesson 1 edits preserved. At 06:00 link today's reward-vs-return lesson, give local-game command and trace-panel instructions, report tests and commits. October 4 summary pending.

## 2026-10-05, 03:00 checkpoint — sound event semantics

- Added pure presentation-only transitionCue helper for deal/hit/terminal outcomes, with silence for initial/repeated/stale/skipped states and no mutation. Bust selects loss, not two overlapping cues.
- Deterministic Node gate passed all event/silence/nonmutation checks. No game/learning changes; prior 77 Python tests and five browser scenarios remain applicable. No audible playback yet.
- Added beginner lesson distinguishing human feedback from reward with examples, commands and separate answers. Next: opt-in playback and controls; invoke cues only after successful local commands. User Lesson 1 edits preserved. October 4 summary delivered; October 5 summary pending.

## 2026-10-05, 04:00 checkpoint — opt-in sound playback

- Added original synthesized cues, explicit enable/mute, volume and local preferences with per-page gesture requirement. Invoked only after confirmed successful local commands; refresh/error responses silent. Audio failures do not stop gameplay.
- All 77 Python tests, sound classifier gate and five browser scenarios passed. Actual oscillator instrumentation verified silent default, deal/hit cues, refresh silence and mute. No listening review claimed.
- User Lesson 1 edits preserved. Next: preference/volume/unsupported-audio edge checks. October 5 summary pending.

## 2026-10-05, 05:00 checkpoint — sound edge checks

- Added no-dependency Node/VM tests for zero volume, mute, preference persistence, required reload activation, unavailable/blocked audio and denied/corrupt storage. Both sound suites passed.
- Explicitly simulated controls, complementing earlier real-browser scheduling checks; no listening review claimed. No product changes; prior 77 Python tests/five browser scenarios remain current.
- User Lesson 1 edits preserved. At 06:00 link today's feedback-vs-reward lesson, explain opt-in cues and controls, give local launch command, verification limits and commits. October 5 summary pending.

## 2026-10-06, 03:00 checkpoint — separate finite shoe

- Added immutable rank/suit cards and finite Shoe under public_game, separate from replacement-draw Foundations. Default six decks, 75% cut threshold, seeded shuffle stream, explicit between-round preparation, no draw-time refill.
- All 82 Python tests passed. Exact composition: 312 cards, 24/rank, six/rank-suit, 96 ten-valued. Tests cover threshold, exhaustion, reproducibility and validation. No browser/agent rule changes.
- Added beginner probability/state-observation lesson with equations, runnable counts and separate answers. Future engine must enforce round boundaries and card sufficiency; primitive alone is not full public gameplay.
- User Lesson 1 edits preserved. October 5 summary delivered; October 6 summary pending. Next: round-boundary requirements and visible rank/suit groundwork.

## 2026-10-06, 04:00 checkpoint — public hand facts

- Added rank-preserving hand facts using existing ace scoring: total/usable ace/bust, unsplit two-card natural, equal-rank pair. No payouts or legal-action claims.
- All 86 Python tests passed. New coverage distinguishes split 21 from natural and J+K from Q+Q, plus multi-ace, bust and validation. Existing learning/browser rules unchanged.
- Expanded today's observation lesson with runnable examples showing why total alone loses decision-relevant information. User Lesson 1 edits preserved. Next: explicit round transitions and settlement contract; October 6 summary pending.

## 2026-10-06, 05:00 checkpoint — public round contract

- Specified phases, natural checks, double/split restrictions, virtual half-chip arithmetic, settlement/net reward, information boundary and compatibility gates in docs/decisions/public-round-v1.md.
- Explicitly requires a shoe-reserve proof and safe exhaustion handling before full engine completion; does not claim the primitives satisfy round safety already. No implementation or game-rule changes in this checkpoint.
- Reviewed against planned profile and checked payout examples; prior 86-test result remains current. User Lesson 1 edits preserved. At 06:00 summarize finite shoe, state/natural distinctions, contract, tests and commits. October 6 summary pending.

## 2026-10-07, 03:00 checkpoint — exact hand settlement

- Added pure completed-hand settlement in half-chip integers, respecting natural/dealer-natural precedence, split ordinary 21, bust and ordinary comparisons. Returns immutable credit/profit facts; no balance mutation or round-lifecycle claim.
- All 91 Python tests passed, including five new settlement tests with split/double conservation and invalid/incomplete inputs. Foundations/browser rules unchanged.
- Added beginner lesson distinguishing stake, credit, profit and normalized RL reward with runnable examples and separate answers. User Lesson 1 edits preserved.
- Next: finite-shoe reserve and round lifecycle. October 6 summary delivered; October 7 summary pending.

## 2026-10-07, 04:00 checkpoint — conservative round reserve

- Derived 101-card upper bound (four player hands ×21 plus dealer17) under explicit stop/split assumptions. Updated contract; reserve may reshuffle earlier than nominal75%.
- Added optional minimum_cards to between-round preparation, default unchanged. All 93 tests passed including exact101/100 boundary, capacity validation and invalid-input nonmutation.
- Engine must still enforce round phases, assumptions and atomic failure handling; no full-game claim. User Lesson1 edits preserved. Next: bounded round lifecycle work; October7 summary pending.

## 2026-10-07, 05:00 checkpoint — pure opening transition

- Added private immutable opening state: strict wager/funds validation, player/dealer/player/dealer ordering, debit and immediate natural settlement using existing arithmetic. Ordinary openings enter player_turn with no completed result.
- All 98 Python tests passed. Runnable examples produced settled/balance230/profit30 and player_turn/balance180/no settlement. Added step-by-step explanation and separate exercise answer; diff whitespace check passed.
- This is a pure transition, not the complete session: transactional shoe ownership, revision/phase checks, actions, visible snapshots and committing balance once remain next. No browser changes. User Lesson1 edits preserved.
- At 06:00 summarize today's stake/credit/profit lesson, opening and reserve work, 98-test proof and GitHub commits. October7 morning summary pending.

## 2026-10-08, 03:00 checkpoint — transactional opening session

- Added opening-only PublicSession with revision/phase/funds checks before candidate shoe preparation, copied RNG/card state, and a single authoritative commit after successful opening resolution. Active snapshots conceal dealer hole/total and are detached.
- All 102 Python tests passed. Four new cases cover rejected requests, failure after tentative shuffle with full future-stream preservation, hidden snapshots, active redeal rejection and natural crediting once.
- Added beginner atomic-transition lesson, state equations, runnable test experiment and separate answers. No player actions/browser integration yet; next slice is round progression using the same transaction boundary.
- October7 morning summary delivered. October8 summary pending. User Lesson1 edits preserved.

## 2026-10-08, 04:00 checkpoint — transactional hit/stand completion

- Added hit/stand progression, automatic completion at 21/bust, S17 dealer play, one-time settlement credit and complete revealed dealer snapshots. All draws remain tentative until successful commit; no mid-round shuffle.
- All 105 Python tests passed, including terminal accounting, soft17, dealer bust, player bust without dealer draws, action rejection and injected dealer-draw failure preserving authoritative state. Seed7 stand example ends balance180/profit-20/dealer20.
- Expanded today's atomic-transition lesson and separate answers. Double/split, action masks, browser and agent integration remain incomplete. User Lesson1 edits preserved. October8 morning summary pending.

## 2026-10-08, 05:00 checkpoint — transactional double

- Added two-card/funds validation, tentative extra stake, exactly one player draw and automatic completion for double. Rollback includes the extra debit if subsequent draws fail.
- All 108 Python tests passed: double outcome conservation, one-card completion, insufficient/post-hit rejection and injected dealer failure. Updated lesson with ±2 normalized reward examples and separate answers; diff check passed.
- Split rules, action masks, concurrency, browser and compatible agent integration remain unfinished. User Lesson1 edits preserved. At 06:00 summarize atomic transitions, opening/hit/stand/double, 108-test proof and pushed commits. October8 summary pending.

## 2026-10-09, 04:00 checkpoint — shared action mask

- No completed 03:00 work found for today. Added supported legal-action lists to public snapshots and reused their eligibility in authoritative command validation. Ready/terminal lists are empty; deal remains a separate command.
- All 110 Python tests passed, including phase/funds/card-count changes, detached masks, rejected-action nonmutation and identical active snapshots across different nonnatural dealer hole cards.
- Added beginner action-mask lesson, constrained greedy/epsilon-greedy equations, runnable tests and separate answers. No trained-policy or browser changes; full split rules remain unfinished. User Lesson1 edits preserved.
- October8 summary delivered; October9 summary pending. Commit source/docs/tests together and push this bounded checkpoint.

## 2026-10-09, 05:00 checkpoint — real-shoe mask integration proof

- Added 300-round integration test across three seeds, sampling supported legal actions with an independent RNG and using actual persistent shoes. Checks concealment/reveal, stale-action nonmutation, per-round balance conservation, card consumption and between-round reshuffles.
- All 111 Python tests passed. No product behavior changes; expanded lesson with experiment limits and separate RNG exercise answer. This is rule verification, not trained-policy evaluation.
- User Lesson1 edits preserved. At 06:00 summarize action masks, 300-round proof, 111 tests and commits; explicitly note no saved 03:00 work. October9 summary pending.

## 2026-10-10, 03:00 checkpoint — fixed initial wager for normalization

- Preserve initial_stake independently of doubled stake; expose completed normalized_profit=profit/initial_stake, with None before settlement. Snapshot reads do not emit reward events.
- All 112 Python tests passed, including double ±2/0, ordinary loss -1, natural +1.5, pending/repeated reads and next-deal denominator reset. Existing 300-round proof remains passing.
- Added beginner equations, worked accounting, coding explanation, runnable tests and separate answers. No RL adapter/browser changes; split work remains unfinished. User Lesson1 edits preserved.
- October9 summary delivered; October10 summary pending. Save this verified checkpoint to GitHub.

## 2026-10-10, 04:00 checkpoint — pure split construction

- Added immutable split-hand construction with ordered additional cards, equal-rank/funds/hand-count validation, one extra debit and split-ace automatic completion. Supplied cards only; split remains unavailable in session masks pending integration.
- All 115 Python tests passed, including three new split tests for ordering/accounting, aces/ordinary21 payout, rank/funds/count restrictions and detached inputs. Expanded normalized-round-profit lesson and separate answers.
- Next: multi-hand session integration with pre-draw legality, transaction safety and aggregate settlement; no browser changes. User Lesson1 edits preserved. October10 morning summary pending.

## 2026-10-10, 05:00 checkpoint — pre-draw split validation

- Extracted shared validate_split for eligibility before future transactional draws; split construction reuses it. Session phase/revision and full multi-hand integration remain pending; split is still not advertised.
- All 116 Python tests passed. Added 1,352 rank/count/funds combinations comparing eligibility and construction with the declared rule, plus resplit-ace rejection. Updated lesson with rationale and coverage limits; diff check passed.
- User Lesson1 edits preserved. At 06:00 summarize fixed initial-wager normalization, split groundwork, 116 tests and commits; explicitly distinguish groundwork from enabled split gameplay. October10 summary pending.

## 2026-10-11, 03:00 checkpoint — aggregate round settlement

- Added pure aggregation of one to four completed hands with per-hand split-aware settlement, total stake/credit/profit and original-wager normalization. No balance mutation or session split enablement.
- All 119 Python tests passed, including mixed double results, balance conservation, ±8 four-double examples, all-bust settlement and incomplete/invalid inputs. Added beginner sum equations, worked example, runnable experiment and separate answers.
- Multi-hand session progression/transaction integration remain unfinished; helper trusts engine-owned completion metadata. User Lesson1 edits preserved. October10 summary delivered; October11 summary pending.

## 2026-10-11, 04:00 checkpoint — transactional multi-hand session

- Integrated split/resplit up to four, split-ace completion, double after non-ace splits, left-to-right advancement and aggregate settlement after all hands finish. Candidate draws and debits commit together; snapshots include full hand collection and active index.
- All 122 Python tests passed, including end-to-end split/double accounting, ace payout, four-hand limit and split-draw failure rollback. Updated 300-round check counts every hand's cards.
- Added session walkthrough and snapshot semantics to today's lesson. Local engine only; Foundations browser and trained policies unchanged. User Lesson1 edits preserved. Next: focused multi-hand edge verification; October11 summary pending.

## 2026-10-11, 05:00 checkpoint — multi-hand completion edge proof

- Added targeted tests for all-split bust without dealer draws, failure during final-hand dealer progression followed by successful retry and stale rejection, and split21 automatic skipping with detached nested snapshots/ordinary payout.
- All 125 Python tests passed, including prior 300-round integration. No product code changes; lesson now explains retry revision semantics and measured accounting outcomes, with separate answers.
- User Lesson1 edits preserved. At 06:00 summarize aggregate round rewards, enabled local split session, edge proof and pushed commits. Browser/compatible agent/concurrency integration remain pending. October11 summary pending.

## 2026-10-12, delayed 03:00 checkpoint at 04:18 — terminal public game

- Added runnable public_game.play adapter using visible session snapshots and engine-owned action validation. Whole-chip wagers convert to half-chip units; all hands, active marker and completed normalized profit display locally.
- All127 Python tests passed, including scripted seed7 round, invalid commands, concealment/reveal, unit output and EOF/nonmutation checks. Added beginner adapter lesson, equations, commands and separate answers.
- Run was delayed within the work window; no earlier October12 progress found. Browser/compatible agent/concurrency remain unfinished. User Lesson1 edits preserved. October11 summary delivered; October12 summary pending.

## 2026-10-12, delayed follow-up at 05:10 — terminal split journey

- Verified scripted terminal split/double/stand presentation, active-hand arrows, concealed pending dealer, chip conversion and final aggregate result. All128 Python tests passed.
- Actual module smoke test with seed7/deal10/stand/quit exited0 and showed balance90/profit-10/normalized-1. Added README launch instructions and lesson evidence; no product changes.
- Scheduled04:30 follow-up executed05:10 within the work window. User Lesson1 edits preserved. October12 summary pending; report delays and unfinished browser/agent integration.

## 2026-10-12, 05:13 checkpoint — visible terminal totals

- Added player hard/soft/bust totals using shared visible-card scoring and dealer total only after reveal. No game-rule changes.
- All129 Python tests passed, including soft17→hard17 after a ten-value hit and dealer-total concealment/reveal. Expanded adapter lesson with the ace arithmetic.
- User Lesson1 edits preserved. At06:00 summarize terminal launch, split display/totals,129 tests and commits, noting earlier delayed execution. Browser/agent integration remains unfinished.

## 2026-10-13, 03:00 checkpoint — strict public command boundary

- Added transport-independent intent parser with exact field sets, known actions and revision validation. Session remains authoritative for legality/funds/results; payloads cannot claim balances or profits.
- All131 Python tests passed, including seeded round/stale replay and malformed/extra-field nonmutation/control-stream checks. Added beginner interface-authority lesson, worked reward example and separate answers.
- HTTP/browser transport, per-user isolation and concurrency remain unfinished. User Lesson1 edits preserved. October12 summary delivered; October13 summary pending.

## 2026-10-13, 03:56 follow-up — local public-rule HTTP inspector

- Added separate loopback server and basic visible-state browser inspector on8766 using existing local transport pattern and strict command boundary. One shared local session; Foundations unchanged; no public hosting.
- All132 Python tests passed including actual HTTP authorization, concealed deal, stale409/current snapshot and stand settlement. HTML/JS real-browser verification and finished game graphics remain pending.
- Next: browser interaction gate. User Lesson1 edits preserved. October13 summary pending.

## 2026-10-13, 05:02 checkpoint — real-browser inspector gate

- Added repeatable Playwright/Chrome journey for invalid wager nonmutation, concealed deal, refresh, keyboard stand/settlement, disabled terminal actions, mobile width and no JS errors. Passed; resources closed.
- Initial node command unavailable on PATH; bundled Node retry succeeded without installations. Documented prerequisites and exact local command. Prior132 Python tests remain current; no product changes.
- User Lesson1 edits preserved. At06:00 summarize intent boundary, local inspector launch, HTTP/Python and browser verification, commits and remaining polished UI/agent/public-hosting work. October13 summary pending.

## 2026-10-14, 03:04 checkpoint — visible browser card table

- Added rank/suit card faces, patterned hidden card, per-hand sections/active highlight and chip balance/aggregate result above expandable visible JSON. Presentation reads snapshots only; no rule changes.
- Real Chrome gate passed with new concealment/card-count/highlight/reveal/profit assertions plus existing keyboard/mobile checks. Prior132 Python tests remain current. Manual visual/accessibility and split UI checks still pending.
- Added beginner rendering/observation lesson, unit equations, runnable example and separate answers. User Lesson1 edits preserved. October13 summary delivered; October14 summary pending.

## 2026-10-14, 03:57 follow-up — split browser journey

- Extended real Chrome gate using actual seed19 deal/split/double/stand. Verifies two hands, active marker advance, doubled stake, concealed pending dealer/no early result, terminal reveal/loss30chips and mobile width.
- Both public browser journeys passed without JS errors; resources closed. No product changes; prior132 Python proof remains current. Documented path-selected seed limitation and runnable reproduction.
- User Lesson1 edits preserved. Manual visual/accessibility review still pending. October14 summary pending.

## 2026-10-14, 04:55 checkpoint — desktop/mobile visual inspection

- Added optional screenshot capture in public browser gate and inspected seed19 split table at1280px/390px. Cards, hidden back, active label/border and hand sections readable; no clipping/overlap in sampled state. Mobile wraps controls and scrolls vertically.
- Both browser journeys passed again. Screenshots temporary; capture workflow documented. No product changes; prior132 Python tests current. Not a full accessibility/contrast/cross-browser audit.
- User Lesson1 edits preserved. At06:00 summarize card UI, two browser journeys and bounded visual review with commits; public hosting/compatible agent/audio/polish remain unfinished. October14 summary pending.

## 2026-10-15, 03:56 checkpoint — visible hand features

- Added per-hand total/usable_ace/bust from existing engine scoring and displayed hard/soft/bust labels in browser; dealer total appears only after settlement.
- All133 Python tests and both Chrome journeys passed, including soft17→hard17→bust22 and browser dealer-total concealment/reveal. Added beginner feature/ace lesson, worked equations and separate answers.
- Earlier02:59 wake correctly did no development. User Lesson1 edits preserved. October14 summary delivered; October15 summary pending. Compatible agent/public deployment remain unfinished.

## 2026-10-15, 04:58 checkpoint — browser ace transition proof

- Added real seed4 browser journey for Soft15→Hard15, concealed dealer, disabled post-hit Double and unchanged Refresh. All three Chrome journeys passed without JS errors; resources closed.
- No product changes; prior133 Python tests current. Added runnable seed example and path-selection limitation to lesson. User Lesson1 edits preserved.
- At06:00 summarize visible features and three browser journeys with commits; mention early02:59 wake skipped development. October15 summary pending.

## 2026-10-16, 03:02 checkpoint — public episode collection

- Added visible-observation policy collector with legal-action checks, zero intermediate rewards and one terminal normalized round reward. Opening naturals retain round outcome without fictitious actions; session shoe persists.
- All137 Python tests passed including split rewards, terminal opening, policy-copy isolation and illegal-action rejection. Added beginner episode/return lesson with runnable example and separate answers.
- No learner/browser coach yet; policy failures retain earlier accepted transitions. User Lesson1 edits preserved. October15 summary delivered; October16 summary pending. Next: fixed-policy collection experiment.

## 2026-10-17, 03:02 checkpoint — fixed-policy episode experiment

- Added reproducible threshold baseline runner over the public session, reporting per-round normalized profit, outcome counts, population spread, opening naturals and decision transitions. It does not learn.
- Both1,000-round runs completed: seed7 mean-0.0410 (409/474/117 W/L/P;101 naturals;1441 actions); seed19 mean-0.0595 (405/488/107;89;1443). Explicitly no strategy claim; persistent-shoe uncertainty requires later block-aware multi-seed evaluation.
- All140 Python tests passed including same-seed reproducibility/count checks. Added equations, worked results, command and separate answers. User Lesson1 edits preserved. October16 summary delivered; October17 pending.

## 2026-10-17, 04:00 checkpoint — first-visit Monte Carlo prediction

- Added a separate public-rule `FirstVisitMonteCarlo` estimator that computes discounted episode returns from terminal normalized profit, updates each visible state once per episode with an incremental sample mean, and tracks opening naturals separately. State keys include decision-visible hand/upcard/split/legal-action features. This predicts `V(s)` under the fixed threshold policy; it does not learn `Q(s,a)` or improve the policy.
- Added `--predict` to the reproducible episode runner; output includes visit counts and the12 most-visited state estimates by default (`--top 0` prints all). Seed7,1,000-round run:899 decision rounds,101 opening naturals,446 distinct state keys; top-8 visits were10–12 each. Example: total12/no usable ace/upcard8/hit-stand-double had12 visits and estimated-0.1667 initial wagers. Sparse samples and persistent-shoe dependence are limitations; this is not a strategy-quality claim.
- Lesson/answers: `docs/daily/2026-10-17.md` and `docs/lessons/solutions/2026-10-17-monte-carlo.md`. Focused public episode/MC suite passed10 tests. Full suite passed146 tests, including local HTTP coverage when run outside the restricted loopback sandbox. `git diff --check` passed. Existing foundational `tests/test_monte_carlo.py` baseline was restored untouched after identifying its name collision; new tests live in `tests/test_public_monte_carlo.py`. User Lesson1 edits remain untouched.
- GitHub checkpoint: the verified estimator, experiment, lesson, answers and tests are the saved lesson unit. No browser changes in that checkpoint. A later audit found Foundations action-value MC control already documented in Lesson3 and implemented in `foundations/control.py`; future work should integrate compatible advice into the public rule profile rather than duplicate that Foundations lesson. User Lesson1 work remains excluded from this checkpoint.

## 2026-10-18, 04:00 checkpoint — opt-in public-game sound cues

- Integrated the existing synthesized, silent-by-default sound player into the public local table. Added labelled Enable/Mute and volume controls; served the public cue classifier and shared player over the same loopback origin. Cues use only accepted consecutive revisions: deal/split, hit/double, and settled aggregate normalized outcome. Refreshes, rejected/gapped requests and mute remain silent. Audio never changes session state or reward.
- Real Chrome gate passed manual, split and soft-ace journeys. It verified silent default, explicit gesture, volume input, Deal/outcome cues, refresh silence, mute on a subsequent Deal, hidden-card behavior, mobile width and no JS errors. Pure public event classifier, existing player controls, and Foundations event tests passed. These instrument oscillator scheduling, not acoustic quality.
- Focused local HTTP asset test passed1/1. Full Python suite passed146/146; `git diff --check` passed. Browser prerequisites and commands are in `tests/browser/README.md`; daily lesson/answers are `docs/daily/2026-10-18.md` and `docs/lessons/solutions/2026-10-18-audio-ui.md`.
- This is a local single-session UI increment only; no production hosting, cross-browser/audio-quality audit, or rule changes. Existing Lesson1 edits remain untouched and excluded. The verified HTML integration, classifier, tests, and teaching note form this checkpoint's GitHub save unit.

## 2026-10-18, 05:00 checkpoint — screen-reader status messages

- Replaced the generic accepted-command status with polite live announcements derived from the authoritative visible state: active hand, hard/soft/bust total, dealer up-card, available actions, then aggregate settled result and chip profit. Rejected requests and Refresh remain distinct. No session, rule, or reward code changed.
- Real Chrome browser gate passed all three manual, split, and soft-ace journeys. New assertions cover initial accepted hand, active hand after split/double, soft-to-hard ace total, aggregate split result (`-30` chips), and ordinary round result (`-10` chips); no browser page errors.
- Lesson and separate answers: `docs/daily/2026-10-18.md` and `docs/lessons/solutions/2026-10-18-live-announcements.md`. This verifies live-region text, not actual speech in a screen reader; manual assistive-technology and cross-browser review remain outstanding. Public game remains a local single-session development inspector, not hosted.
- The unrelated pre-existing Lesson 1 edit remains untouched and excluded from this checkpoint.

## 2026-10-19, 03:00 checkpoint — first-load game context

- The first successful `/state` read now announces the current authoritative snapshot through the existing polite live region. On a new game it prompts for wager/Deal; on reconnect it reads out the active hand, total, dealer up-card and legal actions; if already settled it gives the final outcome. Later Refreshes remain neutral. Reads do not cue sound or mutate the session.
- Real Chrome browser gate passed all three manual, split, and soft-ace journeys. Added checks for fresh-game prompt, active-hand context after reload, neutral later Refresh, existing terminal announcements, and no JavaScript page errors. No rules, rewards, or session logic changed.
- Teaching note and separate answers: `docs/daily/2026-10-19.md` and `docs/lessons/solutions/2026-10-19-first-load-announcements.md`. Browser text assertions do not establish spoken behavior in every assistive technology; manual screen-reader and cross-browser verification remain necessary. The single-session game remains local, not hosted.
- Preserved the unrelated Lesson 1 edit and excluded it from the save checkpoint.

## 2026-10-19, 04:00 checkpoint — semantic landmarks and groups

- Added a main landmark around the playable inspector and accessible names for the Hand actions and Sound settings groups. Kept browser-native buttons and input labels; no custom keyboard or game-state behavior added.
- Real Chrome verified exactly one main landmark and both named groups, then passed manual, split, and soft-ace journeys with no JavaScript errors. Full Python suite and diff check are recorded with this checkpoint below.
- Added the second small lesson section to `docs/daily/2026-10-19.md` and separate answer `docs/lessons/solutions/2026-10-19-landmarks-and-groups.md`. Role assertions are not a full assistive-technology audit; manual screen-reader testing remains outstanding.
- User Lesson 1 edit remains preserved and excluded.

## 2026-10-19, 05:00 checkpoint — player-facing rule disclosure

- Added a keyboard-native collapsed Game rules disclosure describing the six-deck shoe, dealer standing on soft 17, natural and split-21 payouts, double/split restrictions, and unavailable insurance/surrender. It is presentation-only; the Python rules contract remains authoritative.
- Real Chrome checked the closed/open disclosure and all rule phrases. Manual, split, and soft-ace journeys all passed again. The full Python suite and `git diff --check` are recorded below. Static copy can drift when the rules contract changes; this test checks presence, not version synchronization.
- Lesson and separate answers: `docs/daily/2026-10-19.md` and `docs/lessons/solutions/2026-10-19-rules-disclosure.md`. The local single-session inspector is not deployed. Lesson 1 user changes remain untouched and excluded.

## 2026-10-20, 03:00 checkpoint — keyboard test for rules disclosure

- Extended the public browser test to focus the native Game rules summary, open with Enter, verify all listed rules while expanded, and close with Space. No product code or blackjack state changed.
- Installed Chrome passed the rules keyboard assertions and all three existing manual/split/soft-ace journeys, with no page errors. All 146 Python tests passed; `git diff --check` passed.
- Added the test walkthrough/exercise and separate answer in `docs/daily/2026-10-20.md` and `docs/lessons/solutions/2026-10-20-keyboard-disclosure.md`. This proves the disclosure works in tested Chrome only; it is not a complete accessibility audit. Local single-session app remains unpublished; unrelated Lesson 1 user edit is preserved.

## 2026-10-20, 04:00 checkpoint — quick whole-chip wagers

- Added accessible 5/10/25/50 virtual-chip presets beside the existing editable whole-chip wager. `aria-pressed` stays synchronized with custom edits. Presets only change the input; Deal still performs the existing chip-to-half-chip conversion and the Python backend owns balance/phase validation.
- Chrome verified preset selection by keyboard, input/pressed-state synchronization, custom input clearing stale selections, and unchanged revision before Deal. All three game journeys passed with no page errors. All 146 Python tests and `git diff --check` passed.
- Lesson/exercise and separate answer are in `docs/daily/2026-10-20.md` and `docs/lessons/solutions/2026-10-20-quick-wagers.md`. This is local UI only; no real currency or server/game rule changes. The unrelated Lesson1 user edit remains untouched.

## 2026-10-22, 03:00 checkpoint — complete wager availability

- Completed the wager-control availability behavior begun in the prior day's checkpoint: custom wager and quick-preset controls disable while a request is busy, before state loads, or during an active player hand; each preset also disables when its whole-chip cost exceeds the latest server snapshot bankroll. Deal/server validation remains authoritative.
- The Chrome gate verifies the initial affordance, low-bankroll preset selection using a temporary client-only snapshot (5/10 enabled; 25/50 disabled), lock during a real player hand, and re-enable after settlement. The synthetic snapshot is restored before play and never sent to the server.
- All 146 Python tests passed; all three public Chrome journeys passed; `git diff --check` passed. Browser verification is scoped to the installed Chrome test environment; no full accessibility audit is claimed.
- Lesson, runnable command, equation, exercise, and separate solution: `docs/daily/2026-10-21.md` and `docs/lessons/solutions/2026-10-21-wager-affordability.md`. This is a local UI affordance only; no rules, backend validation, money, or hosting changed.
- Preserved the unrelated pre-existing `docs/lessons/01-agent-environment.md` edit and excluded it from this checkpoint. Prior saved checkpoint is `6fa8112`; this verified unit is being saved as the next GitHub checkpoint now.

## 2026-10-22, 04:00 checkpoint — typed wager feedback

- The wager input now describes the whole-chip/balance constraint for assistive technology, marks zero or over-budget values with `aria-invalid`, and disables Deal until the custom amount is a positive safe integer affordable from the latest snapshot. Existing server validation remains authoritative.
- Chrome verifies at a 10-chip fixture balance that 5/10 presets remain available, 25/50 do not, and typed 11 or zero disables Deal; the temporary low-balance browser snapshot is restored before the real play path. The manual, split, and soft-ace Chrome journeys all passed with no page errors.
- Full Python suite: 146 tests passed. `git diff --check` passed. This is a client-side usability check, not a security boundary or a complete assistive-technology audit.
- Lesson and separate answer: `docs/daily/2026-10-22.md` and `docs/lessons/solutions/2026-10-22-custom-wager-validation.md`. No rules engine, reward, balance, or hosting behavior changed.
- The unrelated pre-existing `docs/lessons/01-agent-environment.md` edit remains untouched and excluded. This checkpoint follows saved commit `cd3bbb9` and is being saved separately.
