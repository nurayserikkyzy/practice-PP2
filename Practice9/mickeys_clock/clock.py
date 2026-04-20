import pygame
import datetime
import math

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        # Загружаем твое фото (фон)
        self.bg = pygame.image.load('mickeys_clock/images/mickey_hand.png')
        self.center = (400, 400)
        self.rect_bg = self.bg.get_rect(center=self.center)

    def draw_hand(self, angle, length, color, width):
        # Математика: 0 градусов в тригонометрии — это 3 часа. 
        # Вычитаем 90, чтобы 0 стал 12 часами.
        rad = math.radians(angle - 90)
        end_x = self.center[0] + length * math.cos(rad)
        end_y = self.center[1] + length * math.sin(rad)
        pygame.draw.line(self.screen, color, self.center, (end_x, end_y), width)

    def draw(self):
        # Берем точное время с твоего ноутбука
        now = datetime.datetime.now()
        
        second = now.second
        minute = now.minute
        hour = now.hour % 12  # Формат 12 часов

        # РАСЧЕТ УГЛОВ:
        # Секунды: 6 градусов на одну секунду (360/60)
        sec_angle = second * 6
        
        # Минуты: 6 градусов на одну минуту + чуть-чуть в зависимости от секунд
        min_angle = minute * 6 + second * 0.1
        
        # Часы: 30 градусов на один час (360/12) + смещение от минут
        hour_angle = hour * 30 + minute * 0.5

        # 1. Рисуем фон
        self.screen.blit(self.bg, self.rect_bg)
        
        # 2. ЧАСОВАЯ СТРЕЛКА (самая короткая и жирная)
        self.draw_hand(hour_angle, 100, (50, 50, 50), 10)
        
        # 3. МИНУТНАЯ СТРЕЛКА (длиннее и средней толщины)
        self.draw_hand(min_angle, 160, (0, 0, 0), 6)
        
        # 4. СЕКУНДНАЯ СТРЕЛКА (самая длинная и тонкая, красная)
        self.draw_hand(sec_angle, 190, (255, 0, 0), 2)
        
        # Декоративный центр
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 12)