import pygame
import numpy as np
import random
import time

class Particle:
    def __init__(self, x, y, vx, vy, r, m, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = m
        self.color = color
        self.ax = 0  # acceleration in the x-direction
        self.ay = 0  # acceleration in the y-direction

    def update(self, dt, particles, G, space_size):
        # Save the current position
        current_x, current_y = self.x, self.y

        # Update the position using the Verlet method
        self.x += self.vx * dt + 0.5 * self.ax * dt**2
        self.y += self.vy * dt + 0.5 * self.ay * dt**2

        # Reflect off walls with a buffer distance of 50 pixels
        self.reflect_off_walls(space_size)

        # Reflect off massive particle
        self.reflect_off_massive_particle(particles[4])

        # Reflect off other particles
        self.reflect_off_other_particles(particles)

        # Apply gravity and update acceleration
        self.ax, self.ay = 0, 0
        for other_particle in particles:
            if other_particle != self:
                self.apply_gravity(other_particle, G)

        # Update the velocity using the Verlet method
        self.vx = (self.x - current_x) / dt
        self.vy = (self.y - current_y) / dt

        # Check for NaN values in position and velocity
        if np.isnan(self.x) or np.isnan(self.y) or np.isnan(self.vx) or np.isnan(self.vy):
            # Handle NaN values, e.g., set default position and velocity
            self.x = space_size / 2
            self.y = space_size / 2
            self.vx = 0
            self.vy = 0
            self.ax = 0
            self.ay = 0
            self.angular_momentum = 0

        # Check for NaN radius
        if np.isnan(self.r):
            self.r = 10  # Set to a default value or adjust as needed
        else:
            # Update angular momentum
            self.angular_momentum = self.m * np.sqrt(self.vx**2 + self.vy**2) * self.r

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
            # Update acceleration based on gravitational force
            self.ax += fx / self.m
            self.ay += fy / self.m

        # Update angular momentum
        self.angular_momentum = self.m * np.sqrt(self.vx**2 + self.vy**2) * self.r

    def reflect_off_walls(self, space_size):
        buffer_distance = 50

        if (self.x - self.r) < buffer_distance:
            self.vx = 0.9 * abs(self.vx)  # Reflect to the right with reduced damping
            self.x = buffer_distance + self.r
        elif (self.x + self.r) > (space_size - buffer_distance):
            self.vx = -0.9 * abs(self.vx)  # Reflect to the left with reduced damping
            self.x = space_size - buffer_distance - self.r
        else:
            self.x = self.x

        if (self.y - self.r) < buffer_distance:
            self.vy = 0.9 * abs(self.vy)  # Reflect downwards with reduced damping
            self.y = buffer_distance + self.r
        elif (self.y + self.r) > (space_size - buffer_distance):
            self.vy = -0.9 * abs(self.vy)  # Reflect upwards with reduced damping
            self.y = space_size - buffer_distance - self.r
        else:
            self.y = self.y

    def reflect_off_massive_particle(self, massive_particle):
        dx = self.x - massive_particle.x
        dy = self.y - massive_particle.y
        distance = np.sqrt(dx**2 + dy**2)

        if distance < (self.r + massive_particle.r):
            normal_x = dx / distance
            normal_y = dy / distance

            # Calculate the relative velocity
            relative_velocity_x = self.vx - massive_particle.vx
            relative_velocity_y = self.vy - massive_particle.vy

            # Calculate the dot product of relative velocity and normal vector
            dot_product = normal_x * relative_velocity_x + normal_y * relative_velocity_y

            # Update velocities using the reflection formula with reduced damping
            self.vx -= 1.8 * dot_product * normal_x
            self.vy -= 1.8 * dot_product * normal_y

            # Update angular momentum
            self.angular_momentum = self.m * np.sqrt(self.vx**2 + self.vy**2) * self.r

            # Move the particle outside the massive particle to avoid overlap
            overlap = (self.r + massive_particle.r) - distance
            self.x += overlap * normal_x
            self.y += overlap * normal_y

    def reflect_off_other_particles(self, particles):
        for other_particle in particles:
            if other_particle != self:
                dx = self.x - other_particle.x
                dy = self.y - other_particle.y
                distance = np.sqrt(dx**2 + dy**2)

                if distance < (self.r + other_particle.r):
                    if distance > 0:  # Avoid division by zero
                        normal_x = dx / distance
                        normal_y = dy / distance

                        # Calculate the relative velocity
                        relative_velocity_x = self.vx - other_particle.vx
                        relative_velocity_y = self.vy - other_particle.vy

                        # Calculate the dot product of relative velocity and normal vector
                        dot_product = normal_x * relative_velocity_x + normal_y * relative_velocity_y

                        # Update velocities using the reflection formula with reduced damping
                        self.vx -= 10 * dot_product * normal_x
                        self.vy -= 10 * dot_product * normal_y

                        # Update angular momentum
                        self.angular_momentum = self.m * np.sqrt(self.vx**2 + self.vy**2) * self.r

# ... (previous code)

def calculate_kinetic_energy(particles):
    kinetic_energy = 0.5 * sum(p.m * (p.vx**2 + p.vy**2) for p in particles)
    return kinetic_energy

def calculate_potential_energy(particles, G):
    potential_energy = 0.0
    for particle in particles:
        if particle != particles[4]:  # Ignore massive particle in potential energy calculation
            dx = particle.x - particles[4].x
            dy = particle.y - particles[4].y
            distance = np.sqrt(dx**2 + dy**2)
            if distance > 0:
                potential_energy -= G * particle.m * particles[4].m / distance
    return potential_energy

def calculate_total_energy(particles, G):
    kinetic_energy = calculate_kinetic_energy(particles)
    potential_energy = calculate_potential_energy(particles, G)
    total_energy = kinetic_energy + potential_energy
    return total_energy

# Create particles
particles = [
    Particle(400, 600, -5, 2, 20, 20, (10, 50, 200)),
    Particle(175, 650, -5, 7, 5, 50, (15, 70, 155)),
    Particle(750, 400, 2, -2, 30, 20, (150, 100, 0)),
    Particle(100, 150, 4, -3, 5, 40, (200, 30, 150)),
    Particle(500, 500, 0, 0, 70, 1000, (180, 100, 144)),  # massive particle
    Particle(600, 770, -5, -4, 7, 50, (255, 50, 0)),
]

start_time = time.time()

rate = 60
dt = 1 / rate
space_size = 1000
G = 10
# Adjusted the value of G to be positive for attractive force
# actual G is 6.674e-11 N*m^(2)/kg^(2)

# Initialize smaller particles in a circular pattern
num_particles = 20
for i in range(num_particles):
    angle = i * (2 * np.pi / num_particles)
    radius = 300  # Adjust as needed
    x = particles[0].x + radius * np.cos(angle)
    y = particles[0].y + radius * np.sin(angle)
    # Use angular velocity instead of linear velocity
    omega = 0.1  # Adjust as needed
    vx = -10*omega * radius * np.sin(angle)  # Adjust as needed
    vy = 10*omega * radius * np.cos(angle)  # Adjust as needed
    mass = random.uniform(1, 10)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    particles.append(Particle(x, y, vx, vy, 5, mass, color))

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
        pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), int(particle.r))

    # Update particle positions and apply gravity
    for particle in particles:
        particle.update(dt, particles, G, space_size)

    # Calculate and display potential energy
    potential_energy = calculate_potential_energy(particles, G)
    text = font.render(f'Potential Energy: {potential_energy: .2f}', True, text_color)
    screen.blit(text, (10, 50))

    # Calculate and display kinetic energy
    kinetic_energy = calculate_kinetic_energy(particles)
    text = font.render(f'Kinetic Energy: {kinetic_energy:.2f}', True, text_color)
    screen.blit(text, (10, 10))

    # Calculate and display total energy
    total_energy = calculate_total_energy(particles, G)
    text = font.render(f'Total Energy: {total_energy:.2f}', True, text_color)
    screen.blit(text, (10, 90))

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Display elapsed time
    text = font.render(f'Elapsed Time: {elapsed_time:.2f}', True, text_color)
    screen.blit(text, (10, 130))

    pygame.display.flip()
    clock.tick(rate)

pygame.quit()

