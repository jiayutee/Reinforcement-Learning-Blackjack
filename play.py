import torch
import pygame
import time
import argparse
import config
from environment import BlackjackEnv
from environment.dealer import FixedDealer, LearningDealer
from rl_agent.dqn_agent import DQNAgent
from interface.game_ui import GameUI
import numpy as np

def play(mode='human_vs_fixed', player_model=None, dealer_model=None):
    ui = GameUI()
    
    # Setup Dealer
    if 'learning_dealer' in mode and dealer_model:
        # Load dealer model
        dealer_agent = DQNAgent(3, 2) # Hardcoded dims for now
        dealer_agent.load(dealer_model)
        dealer = LearningDealer(dealer_agent)
    else:
        dealer = FixedDealer()
        
    env = BlackjackEnv(dealer=dealer)
    
    # Setup Player
    if 'agent' in mode and player_model:
        # Load player model
        player_agent = DQNAgent(3, 2)
        player_agent.load(player_model)
    else:
        player_agent = None # Human
        
    running = True
    while running:
        state = env.reset()
        done = False
        message = "Hit (H) or Stand (S)?"
        
        while not done:
            # Render
            show_dealer = done # Only show full dealer hand if done? No, standard rules.
            # Standard rules: Dealer hole card hidden until player stands.
            # My current render logic handles "show_dealer_full"
            
            ui.render(env.player_hand, env.dealer.hand, message, show_dealer_full=False)
            
            # Action selection
            if player_agent:
                # AI Player
                pygame.event.pump() # Process event queue to prevent freeze
                time.sleep(1.0) # Slow down for visibility
                action = player_agent.select_action(state, training=False)
                
                # Update message to show what AI did
                message = f"AI chooses: {'Hit' if action==1 else 'Stand'}"
                ui.render(env.player_hand, env.dealer.hand, message, show_dealer_full=False)
                time.sleep(0.5)
            else:
                # Human Player
                action = None
                while action is None:
                    action = ui.handle_input()
                    # Redraw to keep window responsive?
                    ui.clock.tick(60)
            
            if action == 'reset':
                break
                
            state, reward, done, _ = env.step(action)
            
            if done:
                # Show result
                ui.render(env.player_hand, env.dealer.hand, show_dealer_full=True)
                if reward > 0:
                    final_msg = "Player Wins!"
                elif reward < 0:
                    final_msg = "Dealer Wins!"
                else:
                    final_msg = "Push!"
                
                ui.render(env.player_hand, env.dealer.hand, final_msg, show_dealer_full=True)
                
                # Wait for reset
                waiting = True
                while waiting:
                    inp = ui.handle_input()
                    if inp == 'reset' or inp is not None: # Any key to restart?
                        waiting = False
                        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='human_vs_fixed', 
                        choices=['human_vs_fixed', 'agent_vs_fixed', 'agent_vs_agent'],
                        help='Game mode')
    parser.add_argument('--player_model', type=str, default=None, help='Path to player model')
    parser.add_argument('--dealer_model', type=str, default=None, help='Path to dealer model')
    
    args = parser.parse_args()
    play(args.mode, args.player_model, args.dealer_model)
