import numpy as np
import torch
from environment import BlackjackEnv
from environment.dealer import LearningDealer
from .dqn_agent import DQNAgent

class ActionRecorder:
    """Wrapper to record agent actions/states during dealer play."""
    def __init__(self, agent):
        self.agent = agent
        self.episode_buffer = []

    def select_action(self, state, training=True):
        action = self.agent.select_action(state, training)
        self.episode_buffer.append((state, action))
        return action
    
    def clear(self):
        self.episode_buffer = []

    def get_episode_data(self):
        return self.episode_buffer

class AdversarialTrainer:
    def __init__(self, player_agent, dealer_agent):
        self.player_agent = player_agent
        self.dealer_agent = dealer_agent
        
        # Wrap dealer agent to record actions
        self.dealer_recorder = ActionRecorder(dealer_agent)
        self.learning_dealer = LearningDealer(self.dealer_recorder)
        
        self.env = BlackjackEnv(dealer=self.learning_dealer)

    def train_episode(self):
        # Reset
        state = self.env.reset()
        self.dealer_recorder.clear()
        
        # Player Turn
        state_history = []
        action_history = []
        
        done = False
        final_reward = 0
        
        while not done:
            action = self.player_agent.select_action(state)
            next_state, reward, done, _ = self.env.step(action)
            
            # Store transition for Player (using DQN style)
            # Note: For DQN we usually store (s, a, s', r, done) immediately.
            # But the reward for non-terminal steps is 0.
            # The final reward is only known at end.
            
            # push to memory
            self.player_agent.memory.push(state, action, next_state, reward, done)
            
            state = next_state
            final_reward = reward

        # Optimize Player
        self.player_agent.optimize_model()

        # Dealer Updates
        # Dealer 'reward' is effectively -1 * player_reward (Zero-Sum)
        # Exception: Blackjack payoff is 1.5, so dealer loses 1.5.
        dealer_reward = -final_reward
        
        # Get dealer transitions
        dealer_data = self.dealer_recorder.get_episode_data()
        
        # We need next_state for dealer transitions?
        # The dealer sequence was s1 -> a1 -> s2 -> a2 ...
        # The last state resulted in terminal.
        # We can reconstruct s' from the list.
        
        for i in range(len(dealer_data)):
            d_state, d_action = dealer_data[i]
            if i < len(dealer_data) - 1:
                d_next_state = dealer_data[i+1][0]
                d_done = False
                d_step_reward = 0
            else:
                d_next_state = d_state # Terminal, doesn't matter much if done=True
                d_done = True
                d_step_reward = dealer_reward
            
            # Push to dealer memory
            self.dealer_agent.memory.push(d_state, d_action, d_next_state, d_step_reward, d_done)
            
        # Optimize Dealer
        if len(dealer_data) > 0:
            self.dealer_agent.optimize_model()

        return final_reward
