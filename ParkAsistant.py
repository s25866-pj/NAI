import pygame
import math
import sys



class Car:
    def __init__(self):
        # Pozycja i kąt pojazdu
        self.position_x = 300  # Pozycja początkowa w osi X
        self.position_y = 300  # Pozycja początkowa w osi Y
        self.direction_angle = 0.0  # Kąt kierunku jazdy
        self.front_wheel_angle = 0.0  # Kąt przednich kół
        self.speed = 0.0  # Aktualna prędkość pojazdu
        self.wheelbase = 50.0  # Rozstaw osi pojazdu


        original_image = pygame.image.load("car.png")
        self.width = 120
        self.height = 60
        self.car_image = pygame.transform.scale(original_image, (self.width, self.height))

    def set_front_wheel_angle(self, angle):

        self.front_wheel_angle = max(-30, min(30, angle))

    def accelerate(self, amount):
        # Zmiana prędkości
        self.speed += amount

    def update_position(self, time_interval=1.0):

        if self.front_wheel_angle != 0:
            front_wheel_radians = math.radians(self.front_wheel_angle)
            turning_radius = self.wheelbase / math.sin(front_wheel_radians)
            delta_angle = (self.speed / turning_radius) * time_interval
            self.direction_angle += math.degrees(delta_angle)
        rad_angle = math.radians(self.direction_angle)
        self.position_x += self.speed * math.cos(rad_angle) * time_interval
        self.position_y += self.speed * math.sin(rad_angle) * time_interval

    def draw(self, screen):

        rotated_image = pygame.transform.rotate(self.car_image, -self.direction_angle)
        rotated_rect = rotated_image.get_rect(center=(self.position_x, self.position_y))
        screen.blit(rotated_image, rotated_rect.topleft)



pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Symulacja jazdy samochodem")
clock = pygame.time.Clock()


car = Car()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car.set_front_wheel_angle(car.front_wheel_angle - 5)
    if keys[pygame.K_RIGHT]:
        car.set_front_wheel_angle(car.front_wheel_angle + 5)
    if keys[pygame.K_UP]:
        car.accelerate(0.1)
    if keys[pygame.K_DOWN]:
        car.accelerate(-0.1)
    if keys[pygame.K_SPACE]:
        car.speed = 0.0
    if keys[pygame.K_r]:
        car.set_front_wheel_angle(0)
    car.update_position()
    screen.fill((0, 0, 0))
    car.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
