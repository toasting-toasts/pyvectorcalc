import pygame
import math

WIDTH = 990 #must be divisible by 30
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

display_field_start = (WIDTH//3, 0)
display_field_end = (WIDTH, HEIGHT)

def draw_grid(start, end, frequency, color):
    for i in range(start[0], end[0], frequency):
        for j in range(start[1], end[1], frequency):
            pygame.draw.line(screen, color, (i, start[1]), (i, end[1]))
            pygame.draw.line(screen, color, (start[0], j), (end[0], j))

def draw_arrow(start, end, color, thickness, pointing=0): #0 from start to end
    pygame.draw.line(screen, color, start, end, thickness)

    dy = end[1]-start[1]
    dx = end[0]-start[0]

    angle = math.atan2(dy, dx)

    arrow_length = 15
    arrow_width = 8

    tip = end if pointing == 0 else start
    angle = angle if pointing == 0 else angle + math.pi

    left = (
        tip[0] - arrow_length * math.cos(angle) + arrow_width * math.sin(angle),
        tip[1] - arrow_length * math.sin(angle) - arrow_width * math.cos(angle)
    )

    right = (
        tip[0] - arrow_length * math.cos(angle) - arrow_width * math.sin(angle),
        tip[1] - arrow_length * math.sin(angle) + arrow_width * math.cos(angle)
    )

    pygame.draw.polygon(screen, color, [tip, left, right])

def draw():
    screen.fill("black")
    draw_grid(display_field_start, display_field_end, 30, 'cyan')
    draw_arrow((display_field_start[0]*2, display_field_start[1]), (display_field_start[0]*2, display_field_end[1]), "blue", 3)
    draw_arrow((display_field_start[0], display_field_end[1]//2), (display_field_end[0], display_field_end[1]//2), "blue", 3)
    pygame.display.flip()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw()

    clock.tick(60)  # limits FPS to 60


pygame.quit()
