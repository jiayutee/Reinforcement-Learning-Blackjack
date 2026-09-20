import argparse
import os
import torch
import numpy as np
import config
from rl_agent.dqn_agent import DQNAgent
from training.trainer import Trainer
from rl_agent.adversarial_trainer import AdversarialTrainer
from environment import BlackjackEnv
from environment.dealer import FixedDealer

def main():
    parser = argparse.ArgumentParser(description='Train Blackjack RL Agent')
    parser.add_argument('--adversarial', action='store_true', help='Enable adversarial training (Agent vs Learning Dealer)')
    parser.add_argument('--episodes', type=int, default=config.NUM_EPISODES, help='Number of episodes to train')
    parser.add_argument('--save_path', type=str, default=config.MODEL_SAVE_DIR, help='Directory to save models')
    
    args = parser.parse_args()
    
    os.makedirs(args.save_path, exist_ok=True)
    os.makedirs(config.LOG_DIR, exist_ok=True)
    
    # Initialize environment just to get dimensions
    env = BlackjackEnv()
    input_size = env.observation_space.shape[0]
    output_size = env.action_space.n
    
    # Initialize Player Agent
    player_agent = DQNAgent(input_size, output_size)
    
    rewards_history = []
    
    if args.adversarial:
        print(f"Starting Adversarial Training for {args.episodes} episodes...")
        # Dealer Agent needs same input/output logic?
        # Dealer output: 0 (Stand), 1 (Hit)
        # Dealer input: 3 (Dealer Sum, Player Sum, Usable Ace)
        dealer_agent = DQNAgent(input_size, output_size) # Reuse DQN Class
        
        trainer = AdversarialTrainer(player_agent, dealer_agent)
        
        for i in range(args.episodes):
            reward = trainer.train_episode()
            rewards_history.append(reward)
            
            # Epsilon decay for both
            player_agent.update_epsilon()
            dealer_agent.update_epsilon()
            
            # Target Update
            if i % config.TARGET_UPDATE == 0:
                player_agent.update_target_network()
                dealer_agent.update_target_network()
                
            if i % 100 == 0:
                print(f"Episode {i}/{args.episodes}, Player Eps: {player_agent.epsilon:.2f}, Dealer Eps: {dealer_agent.epsilon:.2f}, Avg Reward: {np.mean(rewards_history[-100:]):.2f}")

        # Save Dealer too
        dealer_agent.save(os.path.join(args.save_path, 'dealer_dqn.pth'))
        
    else:
        print(f"Starting Standard Training (vs Fixed Dealer) for {args.episodes} episodes...")
        trainer = Trainer(player_agent, env)
        rewards_history = trainer.train(args.episodes)
    
    # Save Player Model
    player_agent.save(os.path.join(args.save_path, 'player_dqn.pth'))
    
    # Save Logs
    np.save(os.path.join(config.LOG_DIR, 'rewards.npy'), np.array(rewards_history))
    print("Training Complete. Models and logs saved.")

if __name__ == "__main__":
    main()
