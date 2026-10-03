# Local teaching-table browser check

`local-game.cjs` is an optional integration gate. It requires Python 3.9+, Node.js, the Playwright Node package resolvable by Node, and a compatible Chromium browser. These are test dependencies only; ordinary gameplay needs Python alone. This repository does not yet install or pin a browser toolchain or run this gate in CI.

From the project root, with Playwright available:

```sh
node tests/browser/local-game.cjs
```

Use `PYTHON` to select a Python executable, `CHROME_PATH` to select an installed Chrome/Chromium executable, and `NODE_PATH` if Playwright is installed outside the normal module search path. If `CHROME_PATH` is omitted, Playwright must have its bundled Chromium installed. Dependency installation is separate from this script; it makes no downloads.

The gate launches three independent loopback servers on OS-assigned ports, checks manual/known/missing advice, then closes pages, servers and temporary fixture files. It covers complete seed-7 play, hidden-card responses, unchanged reads, stale duplicate hits, unauthorized requests, keyboard Stand, terminal reveal/advice suppression, mobile overflow and JavaScript errors. Synthetic policy fixtures deliberately test interface behavior; they are not trained agents or performance evidence.

Successful output contains PASS for manual, known and missing. This is a focused integration check, not a full accessibility, visual, security or load audit. The local game remains single-session and unsuitable for public hosting.

The known-policy scenario now uses keyboard Bot step, verifies one-action execution and disabling at a missing next-state estimate, and replays a stale bot command to check nonmutation. Other scenarios retain manual play.
