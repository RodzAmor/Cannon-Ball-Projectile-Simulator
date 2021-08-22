import pygame
import math


class CannonBall(pygame.sprite.Sprite):
    """
    The CannonBall class inherits from the pygame.sprite.Sprite class.
    This class keeps track over all the cannon ball sprite objects in the game.

    It requires 8 parameters:
    The X position, The Y position
    The X veloity, The Y velocity
    gravity and friction
    cannon_ball and cannon_ball_group
    """
    def __init__(self, pos_x, pos_y, vel_x, vel_y, gravity, friction, cannon_ball, cannon_ball_group):
        super().__init__()
        self.image = cannon_ball.copy()
        self.rect = self.image.get_rect(center=(500, 680))
        self.rect.center = [pos_x, pos_y]
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.gravity = gravity
        self.friction = friction
        cannon_ball_group.add(self)

    def update(self, GAME_SCREEN, cannon_wheel, rotated_cannon, rotated_cannon_rect):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += self.gravity

        # Hard Coding the Collision with the wall
        if self.rect.x > 920 and self.rect.x < 955 and self.rect.y > 480:
            self.rect.x = 920
            self.vel_x = -self.vel_x / 2

        if self.rect.y >= 700:
            self.rect.y = 700

            #Setting up bounce mechanic
            if self.vel_y > 2:
                self.vel_y = -self.vel_y / 2
            else:
                self.vel_y = 0

            # Losing horizontal velocity due to friction
            if self.vel_x >= 0:
                self.vel_x -= self.friction
            elif self.vel_x < 0:
                self.vel_x += self.friction

        # Destroys the ball after it stops moving
        if self.vel_x < 0.5 and self.vel_x > -0.5 and self.vel_y > -0.5 and self.vel_y < 0.5:
            self.vel_y = 0
            self.vel_x = 0
            self.kill()

        GAME_SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        GAME_SCREEN.blit(rotated_cannon, rotated_cannon_rect.topleft)
        GAME_SCREEN.blit(cannon_wheel, pygame.Rect(65, 640, 10, 10))

    def returnDistance(self):
        return self.rect.x
    def returnVelocityX(self):
        return self.vel_x
    def returnVelocityY(self):
        return self.vel_y

def calculateVector(x, y):
    return math.sqrt(x ** 2 + y ** 2)

def calculateAngle(mouseX, mouseY, cannonX, cannonY):
    return math.atan2(mouseX - cannonX, mouseY - cannonY)

def drawBackground(GAME_SCREEN, background, cannon_wheel, wall, render_text, render_instructions, render_distance, display_distance, render_vel_x, render_vel_y, display_vel_x, display_vel_y, rotated_cannon, rotated_cannon_rect):
    # Alternate Background Settings
    # GAME_SCREEN.fill(SKY_BLUE)
    # pygame.draw.rect(GAME_SCREEN, GRASS_GREEN, pygame.Rect(0, 700, 1200, 100))

    GAME_SCREEN.blit(background, (0, 0))

    GAME_SCREEN.blit(rotated_cannon, rotated_cannon_rect.topleft)
    GAME_SCREEN.blit(cannon_wheel, pygame.Rect(65, 640, 10, 10))
    GAME_SCREEN.blit(wall, pygame.Rect(900, 500, 100, 100))

    GAME_SCREEN.blit(render_text, pygame.Rect(300, 90, 100, 100))
    GAME_SCREEN.blit(render_instructions, pygame.Rect(310, 60, 100, 100))
    GAME_SCREEN.blit(render_distance, pygame.Rect(880, 150, 100, 100))
    GAME_SCREEN.blit(display_distance, pygame.Rect(1090, 150, 100, 100))
    GAME_SCREEN.blit(render_vel_x, pygame.Rect(903, 180, 100, 100))
    GAME_SCREEN.blit(display_vel_x, pygame.Rect(1090, 180, 100, 100))
    GAME_SCREEN.blit(render_vel_y, pygame.Rect(929, 210, 100, 100))
    GAME_SCREEN.blit(display_vel_y, pygame.Rect(1090, 210, 100, 100))

def main():
    pygame.init()

    # Constants
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1200
    SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
    FRAME_RATE = 60
    GRAVITY = .5
    FRICTION = 0.5

    # Alternate Background Colors for sky and ground
    SKY_BLUE = (135, 206, 235)
    GRASS_GREEN = (69, 100, 56)
    WHITE = (255, 255, 255)

    GAME_SCREEN = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption("2D Cannon Projectile Motion Simulator")

    # Creates the clock object to make 60 frames a second
    clock = pygame.time.Clock()

    # Setting up background
    background = pygame.image.load('background4.jpg')
    background = pygame.transform.smoothscale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load and Scale Cannon and Ball Image
    cannon = pygame.image.load('cannon_base.png')
    cannon = pygame.transform.smoothscale(cannon, (180, 150))

    cannon_wheel = pygame.image.load('cannon_wheel.png')
    cannon_wheel = pygame.transform.scale(cannon_wheel, (150, 150))

    cannon_ball = pygame.image.load('blue_cannon_ball.png')
    cannon_ball = pygame.transform.smoothscale(cannon_ball, (33, 33))

    wall = pygame.image.load('wall.png')
    wall = pygame.transform.smoothscale(wall, (100, 250))

    # Setting the font and text
    # Setting the font and text
    bold_font = pygame.font.Font('OpenSans-Bold.ttf', 24)
    reg_font = pygame.font.Font('OpenSans-Regular.ttf', 20)

    display_text = 'The farther your mouse is, the farther you shoot!'
    render_text = bold_font.render(display_text, True, WHITE)

    instructions_text = 'Instructions: Left click on your mouse to shoot'
    render_instructions = bold_font.render(instructions_text, True, WHITE)
    
    # Creating the Statistics to display in the screen
    distance_text = 'Cannon Ball Distance:'
    render_distance = reg_font.render(distance_text, True, WHITE)
    distance = '0'
    display_distance = reg_font.render(distance, True, WHITE)

    velocity_x_text = 'Horizontal Velocity: '
    velocity_y_text = 'Vertical Velocity: '
    vel_x, vel_y = '0', '0'
    render_vel_x = reg_font.render(velocity_x_text, True, WHITE)
    render_vel_y = reg_font.render(velocity_y_text, True, WHITE)
    display_vel_x = reg_font.render(vel_x, True, WHITE)
    display_vel_y = reg_font.render(vel_y, True, WHITE)

    #global cannon_ball_group
    cannon_ball_group = pygame.sprite.Group()

    # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouseX > cannon_pos[0]:
                    # shooting_angle = math.degrees(calculateAngle(mouseX, mouseY, cannon_pos[0], cannon_pos[1])) - 90
                    mouseX, mouseY = pygame.mouse.get_pos()
                    distanceX, distanceY = cannon_pos[0] + (math.cos(math.radians(angle)) * 30), cannon_pos[1] - (math.sin(math.radians(angle)) * 60) - 25

                    # Shooting Velocity is determined by the distance the mouse is from the cannon
                    # The farther the mouse is, the farther the cannon will shoot
                    shootingVelX, shootingVelY = (mouseX - cannon_pos[0]) / 40, (cannon_pos[1] - mouseY) / 20
                    CannonBall(distanceX, distanceY, shootingVelX, -shootingVelY, GRAVITY, FRICTION, cannon_ball, cannon_ball_group)

        mouseX, mouseY = pygame.mouse.get_pos()
        cannon_pos = [150, 680]
        cannon_rect = cannon.get_rect(center=cannon_pos)

        # Rotates the cannon to track the mouse
        degreeX, degreeY = mouseX - cannon_rect.centerx, mouseY - cannon_rect.centery
        angle = math.degrees(math.atan2(-degreeY, degreeX)) - 32
        rotated_cannon = pygame.transform.rotate(cannon, angle)
        rotated_cannon_rect = rotated_cannon.get_rect(center=cannon_rect.center)

        # Drawing the the sky, ground, and the cannon
        drawBackground(GAME_SCREEN, background, cannon_wheel, wall, render_text, render_instructions, render_distance, display_distance, render_vel_x, render_vel_y, display_vel_x, display_vel_y ,rotated_cannon, rotated_cannon_rect)

        # Update each cannon in the screen
        index = 0
        for cannonball in cannon_ball_group:
            cannonball.update(GAME_SCREEN, cannon_wheel, rotated_cannon, rotated_cannon_rect)
            index += 1
            if len(cannon_ball_group) == 1 or index == len(cannon_ball_group) - 1:
                display_distance = reg_font.render(str(cannonball.returnDistance()), True, WHITE)
                display_vel_x = reg_font.render(str(int(cannonball.returnVelocityX())), True, WHITE)
                display_vel_y = reg_font.render(str(-int(cannonball.returnVelocityY())), True, WHITE)

        pygame.display.flip()
        clock.tick(FRAME_RATE)

    pygame.quit()

if __name__ == "__main__":
    main()
