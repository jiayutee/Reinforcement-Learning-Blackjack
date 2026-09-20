import matplotlib.pyplot as plt
import numpy as np
import os
import config

def plot_learning_curve(rewards, window=100):
    moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
    
    plt.figure(figsize=(10, 5))
    plt.plot(rewards, alpha=0.3, label='Raw Reward')
    plt.plot(np.arange(len(moving_avg)) + window - 1, moving_avg, color='red', label=f'{window}-Episode Moving Avg')
    plt.title('Training Learning Curve')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(config.LOG_DIR, 'learning_curve.png'))
    print(f"Plot saved to {os.path.join(config.LOG_DIR, 'learning_curve.png')}")
    # plt.show() # Optional

if __name__ == "__main__":
    log_path = os.path.join(config.LOG_DIR, 'rewards.npy')
    if os.path.exists(log_path):
        rewards = np.load(log_path)
        plot_learning_curve(rewards)
    else:
        print(f"No logs found at {log_path}. Run train.py first.")
