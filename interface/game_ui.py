import pygame
import sys
import config
import os

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)

class GameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Blackjack RL")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
    def draw_text(self, text, x, y, color=WHITE):
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x, y))
        
    def draw_card(self, card, x, y):
        # Draw a simple card rectangle
        card_rect = pygame.Rect(x, y, 80, 120)
        pygame.draw.rect(self.screen, WHITE, card_rect)
        pygame.draw.rect(self.screen, BLACK, card_rect, 2)
        
        # Draw rank and suit
        rank_text = self.font.render(card.rank, True, BLACK)
        suit_text = self.font.render(card.suit[0], True, RED if card.suit in ['Hearts', 'Diamonds'] else BLACK)
        
        self.screen.blit(rank_text, (x + 5, y + 5))
        self.screen.blit(suit_text, (x + 5, y + 35))

    def render(self, player_hand, dealer_hand, message="", show_dealer_full=False):
        self.screen.fill(GREEN)
        
        # Dealer Cards
        self.draw_text("Dealer's Hand:", 50, 50)
        for i, card in enumerate(dealer_hand):
            if i == 0 and not show_dealer_full:
                # Draw back of card
                card_rect = pygame.Rect(50 + i * 90, 100, 80, 120)
                pygame.draw.rect(self.screen, RED, card_rect)
                pygame.draw.rect(self.screen, BLACK, card_rect, 2)
            else:
                self.draw_card(card, 50 + i * 90, 100)
                
        # Player Cards
        self.draw_text("Player's Hand:", 50, 300)
        for i, card in enumerate(player_hand):
            self.draw_card(card, 50 + i * 90, 350)
            
        # Message
        if message:
            self.draw_text(message, 50, 500, WHITE)
            
        pygame.display.flip()
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    return 1 # Hit
                if event.key == pygame.K_s:
                    return 0 # Stand
                if event.key == pygame.K_r:
                    return 'reset'
        return None
