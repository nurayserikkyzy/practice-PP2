import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mini Paint")
    clock = pygame.time.Clock()


    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    radius = 10
    mode = 'blue'

    drawing = False
    start_pos = None

    while True:
        pressed = pygame.key.get_pressed()
        ctrl = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        shift = pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_e:
                    mode = 'eraser'

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                elif event.button == 3:
                    radius = max(1, radius - 1)

            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False

                    if shift:
                        draw_rect(canvas, start_pos, event.pos, mode)
                    elif ctrl:
                        draw_circle(canvas, start_pos, event.pos, mode)

            
            if event.type == pygame.MOUSEMOTION:
                if drawing and not (shift or ctrl):
                    draw_brush(canvas, event.pos, radius, mode)

    
        screen.blit(canvas, (0, 0))

        
        if drawing and (shift or ctrl):
            temp = canvas.copy()
            if shift:
                draw_rect(temp, start_pos, pygame.mouse.get_pos(), mode)
            elif ctrl:
                draw_circle(temp, start_pos, pygame.mouse.get_pos(), mode)
            screen.blit(temp, (0, 0))

        pygame.display.flip()
        clock.tick(60)



def get_color(mode):
    if mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)
    elif mode == 'blue':
        return (0, 0, 255)



def draw_brush(surface, pos, radius, mode):
    color = (0, 0, 0) if mode == 'eraser' else get_color(mode)
    pygame.draw.circle(surface, color, pos, radius)



def draw_rect(surface, start, end, mode):
    color = (0, 0, 0) if mode == 'eraser' else get_color(mode)
    rect = pygame.Rect(start[0], start[1],
                       end[0] - start[0],
                       end[1] - start[1])
    pygame.draw.rect(surface, color, rect, 3)



def draw_circle(surface, start, end, mode):
    color = (0, 0, 0) if mode == 'eraser' else get_color(mode)
    radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    pygame.draw.circle(surface, color, start, radius, 3)


main()