import pygame

def draw_line(surface, color, start, end, radius):
    """Рисует плавную линию, заполняя пространство между точками кругами."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    steps = max(abs(dx), abs(dy))

    for i in range(steps + 1):
        if steps == 0:
            x, y = start
        else:
            x = int(start[0] + dx * i / steps)
            y = int(start[1] + dy * i / steps)
        pygame.draw.circle(surface, color, (x, y), radius)

def normalize_rect(a, b):
    """Создает корректный pygame.Rect независимо от того, в какую сторону тянут мышь."""
    return pygame.Rect(min(a[0], b[0]), min(a[1], b[1]),
                       abs(a[0] - b[0]), abs(a[1] - b[1]))

def flood_fill(surface, x, y, new_color):
    """Алгоритм заливки области одним цветом."""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    width, height = surface.get_size()
    stack = [(x, y)]

    while stack:
        px, py = stack.pop()
        if 0 <= px < width and 0 <= py < height:
            if surface.get_at((px, py)) == target_color:
                surface.set_at((px, py), new_color)
                stack.append((px - 1, py))
                stack.append((px + 1, py))
                stack.append((px, py - 1))
                stack.append((px, py + 1))