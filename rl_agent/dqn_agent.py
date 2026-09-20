import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import numpy as np
import config
from .replay_buffer import ReplayBuffer, Transition

class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, config.HIDDEN_SIZE)
        self.fc2 = nn.Linear(config.HIDDEN_SIZE, config.HIDDEN_SIZE)
        self.fc3 = nn.Linear(config.HIDDEN_SIZE, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class DQNAgent:
    def __init__(self, input_size, output_size, seed=42):
        self.input_size = input_size
        self.output_size = output_size
        
        # Random seeding
        random.seed(seed)
        torch.manual_seed(seed)
        
        # Networks
        self.policy_net = DQN(input_size, output_size)
        self.target_net = DQN(input_size, output_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=config.LEARNING_RATE)
        self.memory = ReplayBuffer(config.MEMORY_SIZE)
        
        self.steps_done = 0
        self.epsilon = config.EPSILON_START

    def select_action(self, state, training=True):
        if training:
            sample = random.random()
            if sample < self.epsilon:
                return random.randrange(self.output_size)
        
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.policy_net(state_tensor)
            return q_values.argmax().item()

    def optimize_model(self):
        if len(self.memory) < config.BATCH_SIZE:
            return
        
        transitions = self.memory.sample(config.BATCH_SIZE)
        batch = Transition(*zip(*transitions))

        # Check for non-final states (where next_state is not None)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                              batch.next_state)), dtype=torch.bool)
        
        # We need to handle cases where ALL states might be final (unlikely in batch but possible)
        # or handle formatting.
        # However, in our blackjack env, we always get a next_state, but if done=True, the next_state value matters less (reward is terminal).
        # Actually logic: Q(s,a) -> r + gamma * max Q(s', a') * (1-done)
        
        state_batch = torch.FloatTensor(np.array(batch.state))
        action_batch = torch.LongTensor(batch.action).unsqueeze(1)
        reward_batch = torch.FloatTensor(batch.reward)
        next_state_batch = torch.FloatTensor(np.array(batch.next_state))
        done_batch = torch.FloatTensor(batch.done)

        # Compute Q(s_t, a)
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # expected Q values are r + gamma * max(Q(s')) * (1-done)
        next_state_values = self.target_net(next_state_batch).max(1)[0].detach()
        expected_state_action_values = reward_batch + (config.GAMMA * next_state_values * (1 - done_batch))

        # Compute Hubers loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def update_target_network(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def update_epsilon(self):
        self.epsilon = max(config.EPSILON_END, self.epsilon * config.EPSILON_DECAY)

    def save(self, path):
        torch.save(self.policy_net.state_dict(), path)

    def load(self, path):
        self.policy_net.load_state_dict(torch.load(path))
        self.policy_net.eval()
