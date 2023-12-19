# Simple pygame program

#particle1
x1 = 125
y1 = 700
vx1 = -250
vy1 = 50
r1 = 10
m1 = 1
color1 = (10, 50, 200)

#particle2
x2 = 175
y2 = 600
vx2 = -175
vy2 = 75
r2 = 20
m2 = 10
color2 = (15, 70, 155)

#particle3
x3 = 250
y3 = 450
vx3 = 130
vy3 = -20
r3 = 10
m3 = 10
color3 = (150, 100, 0)

#particle4
x4 = 10
y4 = 15
vx4 = -100
vy4 = -30
r4 = 5
m4 = 5
color4 = (200, 30, 150)

#particle5
x5 = 140
y5 = 140
vx5 = 10
vy5 = -20
r5 = 15
m5 = 11
color5 = (180, 100, 144)

#particle6
x6 = 500
y6 = 770
vx6 = -50
vy6 = -40
r6 = 7
m6 = 7
color6 = (255, 50, 0)

rate = 60 # frames per second
dt = 1/rate # time step between frams
space_size = 800

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([space_size, space_size])

clock = pygame.time.Clock()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0, 0, 0))

    # Draw a solid pink circle in the center
    pygame.draw.circle(screen, color1, (x1, y1), r1)

    # Draw a solid purple circle in the center
    pygame.draw.circle(screen, color2, (x2, y2), r2)

    # Draw a solid color circle in the center
    pygame.draw.circle(screen, color3, (x3, y3), r3)
    
    #Draw a solid color circle 
    pygame.draw.circle(screen, color4, (x4, y4), r4)

    # Draw a solid color circle
    pygame.draw.circle(screen, color5, (x5, y5), r5)
    
    #Draw a solid color circle 
    pygame.draw.circle(screen, color6, (x6, y6), r6)



    #handling particle 1 to 2 collisions in x and y
    if (abs(x2 - x1)) < (r1 + r2) and (abs(y2 - y1)) < (r1 + r2):
        ux1, ux2 = vx1, vx2
        vx1 = ux1 * (m1 - m2)/(m1 + m2) + 2 * ux2 * m2/(m1 + m2)
        vx2 = 2 * ux1 * m1/(m1 + m2) + ux2 * (m2 - m1)/(m1 + m2)
    
        uy1, uy2 = vy1, vy2
        vy1 = vy1 = uy1 * (m1 - m2)/(m1 + m2) + 2 * uy2 * m2/(m1 + m2)
        vy2 = 2 * uy1 * m1/(m1 + m2) + uy2 * (m2 - m1)/(m1 + m2)
    #handling particle 1 to 3 collisions in x and y
    if (abs(x3 - x1)) < (r1 + r3) and (abs(y3 - y1)) < (r1 + r3):
        ux1, ux3 = vx1, vx3
        vx1 = ux1 * (m1 - m3)/(m1 + m3) + 2 * ux3 * m3/(m1 + m3)
        vx3 = 2 * ux1 * m1/(m1 + m3) + ux3 * (m3 - m1)/(m1 + m3)
    
        uy1, uy3 = vy1, vy3
        vy1 = uy1 * (m1 - m3)/(m1 + m3) + 2 * uy3 * m3/(m1 + m3)
        vy3 = 2 * uy1 * m1/(m1 + m3) + uy3 * (m3 - m1)/(m1 + m3)





    



    #handling wall collisions for particle 1 in x
    if ((x1 - r1) < 0) or ((x1 + r1) > space_size):
        vx1 = -vx1
    #handling wall collisions for particle 2 in x
    if ((x2 - r2) < 0) or ((x2 + r2) > space_size):
        vx2 = -vx2
    #handling wall collisions for particle 3 in x
    if ((x3 - r3) < 0) or ((x3 + r3) > space_size):
        vx3 = -vx3
    #handling wall collisions for particle 4 in x
    if ((x4 - r4) < 0) or ((x4 + r4) > space_size):
        vx4 = -vx4
    #handling wall collisions for particle 5 in x
    if ((x5 - r5) < 0) or ((x5 + r5) > space_size):
        vx5 = -vx5
    #handling wall collisions for particle 6 in x
    if ((x6 - r6) < 0) or ((x6 + r6) > space_size):
        vx6 = -vx6




    #handling wall collisions for particle 1 in y:
    if ((y1 - r1) < 0) or ((y1 + r1) > space_size):
        vy1 = -vy1
    #handling wall collisions for particle 2 in y:
    if ((y2 - r2) < 0) or ((y2 + r2) > space_size):
        vy2 = -vy2
    #handling wall collisions for particle 3 in y:
    if ((y3 - r3) < 0) or ((y3 + r3) > space_size):
        vy3 = -vy3
    #handling wall collisions for particle 4 in y:
    if ((y4 - r4) < 0) or ((y4 + r4) > space_size):
        vy4 = -vy4
    #handling wall collisions for particle 5 in y:
    if ((y5 - r5) < 0) or ((y5 + r5) > space_size):
        vy5 = -vy5
    #handling wall collisions for particle 6 in y:
    if ((y6 - r6) < 0) or ((y6 + r6) > space_size):
        vy6 = -vy6




    # Flip the display
    pygame.display.flip()

    #dynamics for particle 1 in x
    x1 = x1 + vx1*dt

    #dynamics for particle 2 in x
    x2 = x2 + vx2*dt

    #dynamics for particle 3 in x
    x3 = x3 + vx3*dt

    #dynamics for particle 1 in x
    x4 = x4 + vx4*dt

    #dynamics for particle 2 in x
    x5 = x5 + vx5*dt
    
    #dynamics for particle 3 in x
    x6 = x6 + vx6*dt


    #dynamics for particle 1 in y
    y1 = y1 + vy1*dt

    #dynamics for particle 2 in y
    y2 = y2 + vy2*dt

    #dynamics for particle 3 in y
    y3 = y3 + vy3*dt

    #dynamics for particle 4 in y
    y4 = y4 + vy4*dt

    #dynamics for particle 5 in y
    y5 = y5 + vy5*dt

    #dynamics for particle 6 in y
    y6 = y6 + vy6*dt





    #limit frame rate to desired frames per second

    clock.tick(rate)

# Done! Time to quit.
pygame.quit()