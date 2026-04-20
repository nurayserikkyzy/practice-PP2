import pygame
import datetime
import math

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.image.load('mickeys_clock/images/mickey_hand.png')
        self.center = (400, 400)
        self.rect_bg = self.bg.get_rect(center=self.center)

    def draw_hand(self, angle, length, color, width):
        rad = math.radians(angle - 90)
        end_x = self.center[0] + length * math.cos(rad)
        end_y = self.center[1] + length * math.sin(rad)
        pygame.draw.line(self.screen, color, self.center, (end_x, end_y), width)

    def draw(self):
        # Берем точное время 
        now = datetime.datetime.now()
        
        second = now.second
        minute = now.minute
        hour = now.hour % 12  # Формат 12 часов

        sec_angle = second * 6
        
        
        min_angle = minute * 6 + second * 0.1
        
        
        hour_angle = hour * 30 + minute * 0.5


        self.screen.blit(self.bg, self.rect_bg)
        
        
        self.draw_hand(hour_angle, 100, (50, 50, 50), 10)
        
        
        self.draw_hand(min_angle, 160, (0, 0, 0), 6)
        
        
        self.draw_hand(sec_angle, 190, (255, 0, 0), 2)
        
        
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 12)