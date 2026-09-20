import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical
import numpy as np
import config

class PolicyNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, config.HIDDEN_SIZE)
        self.dropout = nn.Dropout(p=0.6)
        self.fc2 = nn.Linear(config.HIDDEN_SIZE, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.dropout(x)
        x = F.relu(x)
        x = self.fc2(x)
        return F.softmax(x, dim=1)

class PolicyAgent:
    def __init__(self, input_size, output_size, seed=42):
        self.input_size = input_size
        self.output_size = output_size
        
        torch.manual_seed(seed)
        
        self.policy = PolicyNetwork(input_size, output_size)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=config.LEARNING_RATE)
        
        self.saved_log_probs = []
        self.rewards = []

    def select_action(self, state, training=True):
        state = torch.from_numpy(state).float().unsqueeze(0)
        probs = self.policy(state)
        m = Categorical(probs)
        action = m.sample()
        
        if training:
            self.saved_log_probs.append(m.log_prob(action))
            # If not training, we might just want to return action, 
            # or we might want to still collect log_probs if we are evaluating loss?
            # For pure evaluation, we usually don't need log_probs.
        
        return action.item()

    def store_reward(self, reward):
        self.rewards.append(reward)

    def optimize_model(self):
        R = 0
        policy_loss = []
        returns = []
        
        # Calculate returns in reverse order
        for r in self.rewards[::-1]:
            R = r + config.GAMMA * R
            returns.insert(0, R)
            
        returns = torch.tensor(returns)
        # Normalize returns
        if len(returns) > 1:
            returns = (returns - returns.mean()) / (returns.std() + 1e-9)
        
        for log_prob, R in zip(self.saved_log_probs, returns):
            policy_loss.append(-log_prob * R)
            
        self.optimizer.zero_grad()
        if policy_loss:
            policy_loss = torch.cat(policy_loss).sum()
            policy_loss.backward()
            self.optimizer.step()
        
        self.clear_memory()

    def clear_memory(self):
        del self.saved_log_probs[:]
        del self.rewards[:]

    def save(self, path):
        torch.save(self.policy.state_dict(), path)

    def load(self, path):
        self.policy.load_state_dict(torch.load(path))
        self.policy.eval()
