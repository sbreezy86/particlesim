#version 1.2 is simplified using vectors and numpy
#added gravitational interaction between the masses
#added display of kinetic energy calculation

import pygame
import numpy as np

class Particle:
    def __init__(self, x, y, vx, vy, r, m, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = m
        self.color = color

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Reflect off walls
        if (self.x - self.r) < 0 or (self.x + self.r) > space_size:
            self.vx = -self.vx
        if (self.y - self.r) < 0 or (self.y + self.r) > space_size:
            self.vy = -self.vy
    
    def apply_gravity(self, other_particle, G):
        # Calculate distance between particles
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = np.sqrt(dx**2 + dy**2)

        # Avoid division by zero and calculate gravitational force
        if distance > 0:
            force = G * self.m * other_particle.m / distance**2
            # Calculate components of the force in x and y directions
            fx = force * dx / distance
            fy = force * dy / distance
            # Update velocities based on gravitational force
            self.vx += fx / self.m
            self.vy += fy / self.m

            # Update velocities of the other particle
            other_particle.vx -= fx / other_particle.m
            other_particle.vy -= fy / other_particle.m

# Calculate kinetic energy
def calculate_kinetic_energy(particles):
    kinetic_energy = 0.5 * sum(p.m * (p.vx**2 + p.vy**2) for p in particles)
    return kinetic_energy

# Create particles
particles = [
    Particle(125, 700, -250, 50, 10, 100, (10, 50, 200)),
    Particle(175, 600, -175, 75, 20, 110, (15, 70, 155)),
    Particle(250, 450, 130, -20, 10, 50, (150, 100, 0)),
    Particle(10, 15, -100, -30, 5, 90, (200, 30, 150)),
    Particle(140, 140, 10, -20, 70, 1000, (180, 100, 144)),
    Particle(500, 770, -50, -40, 7, 200, (255, 50, 0)),
]

rate = 60
dt = 1 / rate
space_size = 800
G = 6  # Adjusted the value of G to be positive for attractive force

pygame.init()
screen = pygame.display.set_mode([space_size, space_size])
clock = pygame.time.Clock()

# Set up font
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw particles
    for particle in particles:
        pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), particle.r)

    # Update particle positions and apply gravity
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            particles[i].apply_gravity(particles[j], G)
            particles[j].apply_gravity(particles[i], G)
        particles[i].update(dt)

    # Handle particle collisions
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            dx = particles[j].x - particles[i].x
            dy = particles[j].y - particles[i].y
            distance = np.sqrt(dx**2 + dy**2)

            if distance < (particles[i].r + particles[j].r):
                # Implement collision response using elastic collision equations
                ux1, ux2 = particles[i].vx, particles[j].vx
                particles[i].vx = ux1 * (particles[i].m - particles[j].m) / (particles[i].m + particles[j].m) + \
                                  2 * ux2 * particles[j].m / (particles[i].m + particles[j].m)
                particles[j].vx = 2 * ux1 * particles[i].m / (particles[i].m + particles[j].m) + \
                                  ux2 * (particles[j].m - particles[i].m) / (particles[i].m + particles[j].m)

                uy1, uy2 = particles[i].vy, particles[j].vy
                particles[i].vy = uy1 * (particles[i].m - particles[j].m) / (particles[i].m + particles[j].m) + \
                                  2 * uy2 * particles[j].m / (particles[i].m + particles[j].m)
                particles[j].vy = 2 * uy1 * particles[i].m / (particles[i].m + particles[j].m) + \
                                  uy2 * (particles[j].m - particles[i].m) / (particles[i].m + particles[j].m)

    # Calculate and display kinetic energy
    kinetic_energy = calculate_kinetic_energy(particles)
    text = font.render(f'Kinetic Energy: {kinetic_energy:.2f}', True, text_color)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(rate)

pygame.quit()
