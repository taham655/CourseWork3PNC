import pygame
import sys
import time

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 30
LIGHT_DURATION = 5  # Duration in seconds for each light color
ROAD_TOP = SCREEN_HEIGHT // 2 + 50
ROAD_BOTTOM = SCREEN_HEIGHT // 2 - 40
ROAD_COLOR = (50, 50, 50)  # Dark grey road
# Stopping distance from the light
STOP_DISTANCE = 50  # Distance at which vehicles should stop from the traffic light


# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



class TrafficLight(pygame.sprite.Sprite):
    def __init__(self, x, y, size=50):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = GREEN
        self.last_change = time.time()
        self.is_green = True

    def update(self):
        current_time = time.time()
        if current_time - self.last_change >= LIGHT_DURATION:
            self.is_green = not self.is_green
            self.color = GREEN if self.is_green else RED
            self.last_change = current_time
        self.image.fill(self.color)

    def is_green_light(self):
        return self.is_green



class Vehicle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed, traffic_light, all_vehicles):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.traffic_light = traffic_light
        self.all_vehicles = all_vehicles  # Reference to all vehicles

    def update(self):
        # Calculate stopping distance from the traffic light or the nearest vehicle ahead
        min_distance = float('inf')  # Initialize with a large number

        # Check distance to all other vehicles
        for vehicle in self.all_vehicles:
            if vehicle != self and vehicle.rect.x > self.rect.x:
                # Calculate distance to vehicles ahead on the same lane
                distance = vehicle.rect.x - (self.rect.x + self.rect.width)
                min_distance = min(min_distance, distance)

        # Check traffic light status and position
        light_distance = self.traffic_light.rect.x - (self.rect.x + self.rect.width)
        if not self.traffic_light.is_green_light() and light_distance < 100:
            min_distance = min(min_distance, light_distance - 10)

        # Decision making based on the traffic light and other vehicles
        if min_distance < 20:  # Threshold for stopping
            return  # Stop moving if too close to another vehicle or the traffic light

        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -50  # Reset position after crossing the screen


# Create groups
all_sprites = pygame.sprite.Group()
vehicles = pygame.sprite.Group()
lights = pygame.sprite.Group()

# Create traffic light and vehicles
# Initialize the list of all vehicles
all_vehicles = []

# Create traffic light
traffic_light = TrafficLight(SCREEN_WIDTH // 2, ROAD_BOTTOM - 30)
lights.add(traffic_light)
all_sprites.add(traffic_light)

# Create vehicles
for i in range(5):
    vehicle = Vehicle(i * 140, ROAD_BOTTOM + 10, 40, 20, WHITE, 5, traffic_light, all_vehicles)
    vehicles.add(vehicle)
    all_vehicles.append(vehicle)  # Add the vehicle to the list after it has been created
    all_sprites.add(vehicle)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, ROAD_COLOR, (0, ROAD_BOTTOM, SCREEN_WIDTH, ROAD_TOP - ROAD_BOTTOM))  # Draw the road
    all_sprites.draw(screen)

    # Update display and maintain framerate
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()