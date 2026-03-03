import pygame
import math

WIDTH = 990 #must be divisible by 30
HEIGHT = 720
resolution = 30


pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Arial', 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vector Visualization")
clock = pygame.time.Clock()
running = True

display_field_start = (WIDTH//3, 0)
display_field_end = (WIDTH, HEIGHT)

vector1_input_start = (0+30, 0+30)
vector1_input_end = (WIDTH//3-30, HEIGHT//2-30)
vector1_input_selected = True

vector2_input_start = (0+30, HEIGHT//2+30)
vector2_input_end = (WIDTH//3-30, HEIGHT-30)
vector2_input_selected = False

vector_1 = (1, 1)
vector_2 = (4, -2)

mode = "add" #or "subtract"

def draw_grid(start, end, frequency, color):
    for i in range(start[0], end[0]+1, frequency):
        pygame.draw.line(screen, color, (i, start[1]), (i, end[1]))
    for j in range(start[1], end[1]+1, frequency):
        pygame.draw.line(screen, color, (start[0], j), (end[0], j))

def draw_arrow(start, end, color, thickness, pointing=0): #0 from start to end
    pygame.draw.line(screen, color, start, end, thickness)

    dy = end[1]-start[1]
    dx = end[0]-start[0]

    angle = math.atan2(dy, dx)

    arrow_length = 10
    arrow_width = 5

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

def draw_essentials():
    screen.fill("black")
    draw_grid(display_field_start, display_field_end, resolution, 'cyan')
    draw_arrow((display_field_start[0]*2, display_field_start[1]), (display_field_start[0]*2, display_field_end[1]), "blue", 3, 1)
    draw_arrow((display_field_start[0], display_field_end[1]//2), (display_field_end[0], display_field_end[1]//2), "blue", 3)

    draw_grid(vector1_input_start, vector1_input_end, resolution, 'green' if vector1_input_selected else 'white')
    draw_grid(vector2_input_start, vector2_input_end, resolution, 'green' if vector2_input_selected else 'white')

    global text1_rect, text2_rect

    text1 = font.render("Додати", True, "green" if mode == "add" else "gray")
    text1_rect = text1.get_rect()
    text1_rect.topleft = (vector1_input_start[0] + resolution*2 - text1.get_width()//2 - 30, vector1_input_end[1] + 15)
    screen.blit(text1, text1_rect)

    
    text2 = font.render("Відняти(ниж від верхн)", True, "green" if mode == "subtract" else "gray")
    text2_rect = text2.get_rect()
    text2_rect.topleft = (vector2_input_end[0] - resolution*2 - text2.get_width()//2 - 30, vector2_input_start[1] - 45)
    screen.blit(text2, text2_rect)

    pygame.draw.circle(screen, "red", (vector1_input_start[0]+resolution*4, vector1_input_start[1]+resolution*5), 5)
    pygame.draw.circle(screen, "red", (vector2_input_start[0]+resolution*4, vector2_input_start[1]+resolution*5), 5)


def handle_input(mouse, mouse_pos):
    global vector1_input_selected, vector2_input_selected, mode, vector_1, vector_2, cooldown
    if vector1_input_start[0] < mouse_pos[0] < vector1_input_end[0] and vector1_input_start[1] < mouse_pos[1] < vector1_input_end[1] and mouse[0]:
        vector1_input_selected = True
        vector2_input_selected = False

    if vector2_input_start[0] < mouse_pos[0] < vector2_input_end[0] and vector2_input_start[1] < mouse_pos[1] < vector2_input_end[1] and mouse[0]:
        vector1_input_selected = False
        vector2_input_selected = True


    if mouse[0]:  # left click
        if text1_rect.collidepoint(mouse_pos):
            mode = "add"
        elif text2_rect.collidepoint(mouse_pos):
            mode = "subtract"

def clamp_vector(vector, xmin=-4, xmax=5, ymin=-5, ymax=5):
    return (max(xmin, min(xmax, vector[0])), max(ymin, min(ymax, vector[1])))

def handle_keyboard(event):
    global vector_1, vector_2
    if vector1_input_selected:
        if event.key == pygame.K_UP:
            vector_1 = (vector_1[0], vector_1[1] + 1)
        if event.key == pygame.K_DOWN:
            vector_1 = (vector_1[0], vector_1[1] - 1)
        if event.key == pygame.K_RIGHT:
            vector_1 = (vector_1[0] + 1, vector_1[1])
        if event.key == pygame.K_LEFT:
            vector_1 = (vector_1[0] - 1, vector_1[1])

    if vector2_input_selected:
        if event.key == pygame.K_UP:
            vector_2 = (vector_2[0], vector_2[1] + 1)
        if event.key == pygame.K_DOWN:
            vector_2 = (vector_2[0], vector_2[1] - 1)
        if event.key == pygame.K_RIGHT:
            vector_2 = (vector_2[0] + 1, vector_2[1])
        if event.key == pygame.K_LEFT:
            vector_2 = (vector_2[0] - 1, vector_2[1])

    vector_1 = clamp_vector(vector_1)
    vector_2 = clamp_vector(vector_2)

def draw_vector(vector, start, color):
    end = (start[0] + vector[0]*resolution, start[1] - vector[1]*resolution) 
    draw_arrow(start, end, color, 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN: handle_keyboard(event)

    handle_input(pygame.mouse.get_pressed(), pygame.mouse.get_pos())

    draw_essentials()
    draw_vector(vector_1, (vector1_input_start[0]+resolution*4, vector1_input_start[1]+resolution*5), "red")
    draw_vector(vector_2, (vector2_input_start[0]+resolution*4, vector2_input_start[1]+resolution*5), "red")

    if mode == "add":
        draw_vector(vector_1, (display_field_start[0]*2, (display_field_start[1]+display_field_end[1]//2)), "orange")
        draw_vector(vector_2, (display_field_start[0]*2+vector_1[0]*resolution, (display_field_start[1]+display_field_end[1]//2)-vector_1[1]*resolution), "orange")
        draw_vector(vector_2, (display_field_start[0]*2, (display_field_start[1]+display_field_end[1]//2)), "yellow")
        draw_vector(vector_1, (display_field_start[0]*2+vector_2[0]*resolution, (display_field_start[1]+display_field_end[1]//2)-vector_2[1]*resolution), "yellow")

        draw_vector(
            (vector_1[0] + vector_2[0], vector_1[1] + vector_2[1]), 
            (display_field_start[0]*2, display_field_start[1]+display_field_end[1]//2), 
            "red")
    elif mode == "subtract":
        neg_vector_2 = (-vector_2[0], -vector_2[1])
        draw_vector(vector_1, (display_field_start[0]*2, (display_field_start[1]+display_field_end[1]//2)), "cyan")
        draw_vector(neg_vector_2, (display_field_start[0]*2+vector_1[0]*resolution, (display_field_start[1]+display_field_end[1]//2)-vector_1[1]*resolution), "gray")
        draw_vector(neg_vector_2, (display_field_start[0]*2, (display_field_start[1]+display_field_end[1]//2)), "darkcyan")
        draw_vector(vector_1, (display_field_start[0]*2+neg_vector_2[0]*resolution, (display_field_start[1]+display_field_end[1]//2)-neg_vector_2[1]*resolution), "darkcyan")
        draw_vector(vector_2, (display_field_start[0]*2+vector_1[0]*resolution, (display_field_start[1]+display_field_end[1]//2)-vector_1[1]*resolution), "cyan")

        draw_vector(
            (vector_1[0] - vector_2[0], vector_1[1] - vector_2[1]), 
            (display_field_start[0]*2, display_field_start[1]+display_field_end[1]//2), 
            "magenta")
    
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
