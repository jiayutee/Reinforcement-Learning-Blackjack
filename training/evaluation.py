import numpy as np
from environment import BlackjackEnv

def evaluate(agent, num_episodes=100, env=None):
    if env is None:
        env = BlackjackEnv()
        
    wins = 0
    losses = 0
    pushes = 0
    rewards = []
    
    for _ in range(num_episodes):
        state = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            action = agent.select_action(state, training=False)
            state, reward, done, _ = env.step(action)
            total_reward += reward
            
        rewards.append(total_reward)
        if total_reward > 0:
            wins += 1
        elif total_reward < 0:
            losses += 1
        else:
            pushes += 1
            
    win_rate = wins / num_episodes
    avg_reward = np.mean(rewards)
    
    return win_rate, avg_reward, (wins, losses, pushes)
