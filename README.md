# Blackjack RL Framework

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
