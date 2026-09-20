# Blackjack RL Framework

## Start the guided course

This project is being developed into a step-by-step RL course and a public blackjack web game. The web game is not deployed yet.

Start with [Lesson 1: the agent and environment](docs/lessons/01-agent-environment.md). It runs on Python 3.9+ with no additional dependencies:

```sh
python3 -m foundations.play --seed 7 --episodes 3
python3 -m unittest discover -s tests -v
```

See [the project plan](PROJECT_PLAN.md) and [progress](PROGRESS.md). The `foundations/` package uses simplified, explicitly documented rules. The code below is the preserved early prototype; its agents and realistic rules have not yet been fully audited. In particular, the adaptive dealer is an alternative-game experiment.

## Original prototype

A Reinforcement Learning framework for playing Blackjack, featuring Deep Q-Networks (DQN), Policy Gradients, and Adversarial Training (GAN-style learning).

## Features

- **RL Agents**:
  - `DQNAgent`: Deep Q-Network implementation.
  - `PolicyAgent`: Policy Gradient (REINFORCE) implementation.
- **Adversarial Training**: Train your agent against a "Learning Dealer" to improve robustness.
- **Custom Environment**: OpenAI Gym compatible Blackjack environment.
- **Interface**: PyGame-based visual interface for human vs AI or watching AI play.

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   conda create -n myenv python=3.9
   conda activate myenv
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Training

Train a standard DQN agent against a fixed dealer:
```bash
python train.py --episodes 5000
```

Train using Adversarial Training (Agent vs Agent):
```bash
python train.py --adversarial --episodes 5000
```

### Visualization

Plot training learning curves:
```bash
python visualize.py
```

### Playing / Watching

Play against the fixed dealer:
```bash
python play.py --mode human_vs_fixed
```

Watch trained agent play against fixed dealer:
```bash
python play.py --mode agent_vs_fixed --player_model models/player_dqn.pth
```

Watch trained agent play against trained dealer:
```bash
python play.py --mode agent_vs_agent --player_model models/player_dqn.pth --dealer_model models/dealer_dqn.pth
```

## Structure

- `rl_agent/`: Agent implementations.
- `environment/`: Blackjack logic and Gym environment.
- `training/`: Training loops and evaluation.
- `interface/`: PyGame UI.
