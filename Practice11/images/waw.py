import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Geometry Paint")
    clock = pygame.time.Clock()

    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    radius = 10
    
    current_color = 'blue' 
    shape_mode = 'brush' 

    drawing = False
    start_pos = None

    while True:
        pressed = pygame.key.get_pressed()
        shift = pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]
        ctrl = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
           
                elif event.key == pygame.K_r: current_color = 'red'
                elif event.key == pygame.K_g: current_color = 'green'
                elif event.key == pygame.K_b: current_color = 'blue'
                elif event.key == pygame.K_e: current_color = 'eraser'
                
                # Меняем ТОЛЬКО фигуру
                elif event.key == pygame.K_s: shape_mode = 'square'
                elif event.key == pygame.K_t: shape_mode = 'right_triangle'
                elif event.key == pygame.K_i: shape_mode = 'equilateral'
                elif event.key == pygame.K_h: shape_mode = 'rhombus'
                elif event.key == pygame.K_f: shape_mode = 'brush' 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    curr_pos = event.pos
                   
                    if shape_mode == 'square':
                        draw_square(canvas, start_pos, curr_pos, current_color)
                    elif shape_mode == 'right_triangle':
                        draw_right_triangle(canvas, start_pos, curr_pos, current_color)
                    elif shape_mode == 'equilateral':
                        draw_equilateral_triangle(canvas, start_pos, curr_pos, current_color)
                    elif shape_mode == 'rhombus':
                        draw_rhombus(canvas, start_pos, curr_pos, current_color)
                    elif shift:
                        draw_rect(canvas, start_pos, curr_pos, current_color)
                    elif ctrl:
                        draw_circle(canvas, start_pos, curr_pos, current_color)

            if event.type == pygame.MOUSEMOTION:
               
                if drawing and shape_mode == 'brush' and not (shift or ctrl):
                    draw_brush(canvas, event.pos, radius, current_color)

        screen.blit(canvas, (0, 0))
        
        
        if drawing:
            curr_pos = pygame.mouse.get_pos()
            if shape_mode == 'square':
                draw_square(screen, start_pos, curr_pos, current_color)
            elif shape_mode == 'right_triangle':
                draw_right_triangle(screen, start_pos, curr_pos, current_color)
            elif shape_mode == 'equilateral':
                draw_equilateral_triangle(screen, start_pos, curr_pos, current_color)
            elif shape_mode == 'rhombus':
                draw_rhombus(screen, start_pos, curr_pos, current_color)
            elif shift:
                draw_rect(screen, start_pos, curr_pos, current_color)
            elif ctrl:
                draw_circle(screen, start_pos, curr_pos, current_color)

        pygame.display.flip()
        clock.tick(60)

def get_color(mode):
    colors = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'eraser': (0, 0, 0)}
    return colors.get(mode, (255, 255, 255)) 

def draw_brush(surface, pos, radius, mode):
    pygame.draw.circle(surface, get_color(mode), pos, radius)

def draw_rect(surface, start, end, mode):
    rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
    rect.normalize()
    pygame.draw.rect(surface, get_color(mode), rect, 3)

def draw_circle(surface, start, end, mode):
    radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    pygame.draw.circle(surface, get_color(mode), start, radius, 3)

def draw_square(surface, start, end, mode):
    side = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    new_end_x = start[0] + side if end[0] > start[0] else start[0] - side
    new_end_y = start[1] + side if end[1] > start[1] else start[1] - side
    rect = pygame.Rect(start[0], start[1], new_end_x - start[0], new_end_y - start[1])
    rect.normalize()
    pygame.draw.rect(surface, get_color(mode), rect, 3)

def draw_right_triangle(surface, start, end, mode):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surface, get_color(mode), points, 3)

def draw_equilateral_triangle(surface, start, end, mode):
    side = end[0] - start[0]
    height = (math.sqrt(3) / 2) * side
    points = [
        (start[0], start[1]),           
        (start[0] - side/2, start[1] + height), 
        (start[0] + side/2, start[1] + height)  
    ]
    pygame.draw.polygon(surface, get_color(mode), points, 3)

def draw_rhombus(surface, start, end, mode):
    width = end[0] - start[0]
    height = end[1] - start[1]
    points = [
        (start[0] + width / 2, start[1]),          
        (start[0] + width, start[1] + height / 2),  
        (start[0] + width / 2, start[1] + height), 
        (start[0], start[1] + height / 2)          
    ]
    pygame.draw.polygon(surface, get_color(mode), points, 3)

if __name__ == "__main__":
    main()