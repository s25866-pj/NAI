import pygame
import math
import sys
import os


class Car:
    def __init__(self):
        self.position_x = 300
        self.position_y = 300
        self.direction_angle = 0.0
        self.front_wheel_angle = 0.0
        self.speed = 0.0
        self.wheelbase = 50.0

        if os.path.exists("car.png"):
            original_image = pygame.image.load("car.png")
            self.width = 120
            self.height = 60
            self.car_image = pygame.transform.scale(original_image, (self.width, self.height))
        else:
            print("Obraz 'car.png' nie został znaleziony. Rysowanie prostokąta zamiast obrazu samochodu.")
            self.width = 120
            self.height = 60
            self.car_image = None

        self.hitbox_scale_x = 0.7
        self.hitbox_scale_y = 0.7
        self.sensor_offset = 20
        self.sensor_radius = 10

    def set_front_wheel_angle(self, angle):
        self.front_wheel_angle = max(-30, min(30, angle))

    def accelerate(self, amount):
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
        if self.car_image:
            rotated_image = pygame.transform.rotate(self.car_image, -self.direction_angle)
            rotated_rect = rotated_image.get_rect(center=(self.position_x, self.position_y))
            screen.blit(rotated_image, rotated_rect.topleft)
        else:
            rotated_rect = pygame.Rect(
                self.position_x - self.width // 2, self.position_y - self.height // 2, self.width, self.height
            )
            pygame.draw.rect(screen, (0, 255, 0), rotated_rect)

        return rotated_rect

    def draw_sensors(self, screen):
        sensor_positions = [
            (self.position_x + self.sensor_offset * math.cos(math.radians(self.direction_angle + 45)),
             self.position_y + self.sensor_offset * math.sin(math.radians(self.direction_angle + 45))),
            (self.position_x + self.sensor_offset * math.cos(math.radians(self.direction_angle - 45)),
             self.position_y + self.sensor_offset * math.sin(math.radians(self.direction_angle - 45))),
            (self.position_x + self.sensor_offset * math.cos(math.radians(self.direction_angle + 180)),
             self.position_y + self.sensor_offset * math.sin(math.radians(self.direction_angle + 180)))
        ]

        for pos in sensor_positions:
            pygame.draw.circle(screen, (0, 255, 0), (int(pos[0]), int(pos[1])), self.sensor_radius)

    def control_vehicle_based_on_sensors(self, obstacles):
        sensor_data = self.get_sensor_data(obstacles)
        for obstacle in sensor_data:
            if obstacle:
                self.speed = 0
                return
        self.accelerate(0.1)

    def get_sensor_data(self, obstacles):
        sensor_positions = [
            (self.position_x + self.sensor_offset * math.cos(math.radians(self.direction_angle + 45)),
             self.position_y + self.sensor_offset * math.sin(math.radians(self.direction_angle + 45))),
            (self.position_x + self.sensor_offset * math.cos(math.radians(self.direction_angle - 45)),
             self.position_y + self.sensor_offset * math.sin(math.radians(self.direction_angle - 45))),
            (self.position_x + self.sensor_offset * math.cos(math.radians(self.direction_angle + 180)),
             self.position_y + self.sensor_offset * math.sin(math.radians(self.direction_angle + 180)))
        ]

        sensor_data = []
        for pos in sensor_positions:
            closest_obstacle = None
            for obstacle in obstacles:
                if (obstacle.collidepoint(pos[0], pos[1])):
                    closest_obstacle = obstacle
                    break
            sensor_data.append(closest_obstacle)

        return sensor_data


pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Symulacja jazdy samochodem")
clock = pygame.time.Clock()

# Przeszkody i pole parkingowe
obstacle1_rect = pygame.Rect(0, 0, 100, 120)
obstacle2_rect = pygame.Rect(200, 0, 100, 120)
parking_rect = pygame.Rect(100, 0, 100, 120)

car = Car()
manual_mode = True  # Start w trybie ręcznym
running = True
parked = False  # Flaga wskazująca, czy samochód zaparkował

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Przełączanie trybu M - manualny/automatyczny
                manual_mode = not manual_mode
                print("Przełączono tryb:", "Ręczny" if manual_mode else "Automatyczny")

    keys = pygame.key.get_pressed()

    # Ręczna kontrola w trybie manualnym
    if manual_mode:
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
    elif not parked:
        # Tryb automatyczny - kontrola czujników
        car.control_vehicle_based_on_sensors([obstacle1_rect, obstacle2_rect])

    # Aktualizacja pozycji samochodu
    car.update_position()
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), obstacle1_rect)
    pygame.draw.rect(screen, (255, 0, 0), obstacle2_rect)
    pygame.draw.rect(screen, (0, 0, 255), parking_rect)
    car_rect = car.draw(screen)
    car.draw_sensors(screen)

    # Sprawdzenie, czy samochód całkowicie mieści się w polu parkingowym
    if parking_rect.contains(car_rect) and not parked:
        print("Zaparkowane")
        car.speed = 0.0  # Zatrzymaj samochód
        parked = True  # Ustaw flagę jako zaparkowane

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
