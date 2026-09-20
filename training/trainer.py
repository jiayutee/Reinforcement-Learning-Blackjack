import numpy as np
import config
from environment import BlackjackEnv
from environment.dealer import FixedDealer

class Trainer:
    def __init__(self, agent, env=None):
        self.agent = agent
        self.env = env if env else BlackjackEnv()
        
    def train(self, num_episodes):
        rewards = []
        
        for i_episode in range(num_episodes):
            state = self.env.reset()
            done = False
            total_reward = 0
            
            while not done:
                action = self.agent.select_action(state, training=True)
                next_state, reward, done, _ = self.env.step(action)
                
                # Check for "real" final state (Standard Gym behavior)
                # In Blackjack, episode always ends or continues.
                
                self.agent.memory.push(state, action, next_state, reward, done)
                state = next_state
                total_reward += reward
                
                self.agent.optimize_model()
                
            rewards.append(total_reward)
            
            # Epsilon decay
            if hasattr(self.agent, 'update_epsilon'):
                self.agent.update_epsilon()
                
            # Target network update
            if i_episode % config.TARGET_UPDATE == 0:
                if hasattr(self.agent, 'update_target_network'):
                    self.agent.update_target_network()
            
            if i_episode % 100 == 0:
                print(f"Episode {i_episode}/{num_episodes}, Epsilon: {getattr(self.agent, 'epsilon', 0):.2f}, Avg Reward: {np.mean(rewards[-100:]):.2f}")
                
        return rewards
