import pygame, sys, time

screen = pygame.display.set_mode((1000, 500))

class SimpleFadingEllipse:

    def __init__(self, surface, fade_time, max_width_time, starting_width, max_width, height, thickness):

        # ---------------------------------------------------------------------------------------
        # Alpha level 

        # The time it takes for the alpha level of the ellipse to go from 255 to 0 (in seconds)
        self.ellipse_alpha_decay_timer = 0
        self.time_taken_for_ellipse_to_fade = fade_time
        # The gradient should be the (other alpha level - maximum alpha level) divided by the time taken to go from one alpha level to the other
        self.ellipse_alpha_gradient = (0 - 255 / self.time_taken_for_ellipse_to_fade)
        self.ellipse_alpha_level = 255

        # ---------------------------------------------------------------------------------------
        # Ellipse measurements

        self.starting_ellipse_width = starting_width # The starting width for the equation to calculate the gradient
        self.ellipse_width = starting_width
        self.ellipse_max_width = max_width
        self.ellipse_height = height
        self.ellipse_thickness = thickness
        
        # The time it takes for the starting width to reach the max width (in seconds)
        self.ellipse_width_timer = 0
        self.time_taken_for_ellipse_to_reach_max_width = max_width_time
        self.ellipse_width_gradient = (self.ellipse_max_width - self.ellipse_width) / self.time_taken_for_ellipse_to_reach_max_width

        # ---------------------------------------------------------------------------------------
        # Ellipse surfaces

        self.surface = surface

        self.ellipse_surface = pygame.Surface((self.ellipse_max_width, self.ellipse_height))
        self.ellipse_surface.set_colorkey((0, 0, 0)) # Colorkey for transparency

    def draw(self, x, y, delta_time):
    
        # ---------------------------------------------------------------------------------------
        # Update the alpha levels

        # If the ellipse has not reached an alpha level of 0
        if (self.ellipse_alpha_decay_timer / 1000) < self.time_taken_for_ellipse_to_fade:

            # Increase the timer
            self.ellipse_alpha_decay_timer += 1000 * delta_time

            # y = (gradient)x + (starting alpha level), where y is the alpha level and x is the time
            self.ellipse_alpha_level = (self.ellipse_alpha_gradient * (self.ellipse_alpha_decay_timer / 1000)) + 255

            # Set the alpha level based on how much time has passed
            self.ellipse_surface.set_alpha(self.ellipse_alpha_level)

        # ---------------------------------------------------------------------------------------
        # Updating the ellipse
    
        # If the ellipse has not reached the max width
        if (self.ellipse_width_timer / 1000) < self.time_taken_for_ellipse_to_reach_max_width:
            # Increase the timer
            self.ellipse_width_timer += 1000 * delta_time
            # y = (gradient)x + (starting width), where y is the current width and x is time
            self.ellipse_width = (self.ellipse_width_gradient * (self.ellipse_width_timer / 1000)) + self.starting_ellipse_width
    
        # Fill the ellipse surfaces with black (For transparency)
        self.ellipse_surface.fill("black")

        # ---------------------------------------------------------------------------------------
        # Drawing the ellipse

        # Only draw the effect if the alpha level of the ellipse is greater than 0 or the width of the ellipse is less than the max width
        if (self.ellipse_alpha_level > 0) or (self.ellipse_width < self.ellipse_max_width):

            # Draw the ellipse
            pygame.draw.ellipse(self.ellipse_surface, "white", ((self.ellipse_surface.get_width() / 2) - (self.ellipse_width / 2), 0, self.ellipse_width, self.ellipse_height), self.ellipse_thickness)

            # Draw the ellipse surfaces onto the main surface
            self.surface.blit(self.ellipse_surface, (x - (self.ellipse_surface.get_width() / 2), y))

larger_ellipse = SimpleFadingEllipse(surface = screen, fade_time = 1, max_width_time = 0.25, starting_width = 100, max_width = 300, height = 20, thickness = 5)
smaller_ellipse = SimpleFadingEllipse(surface = screen, fade_time = 0.8, max_width_time = 0.25, starting_width = 50, max_width = 200, height = 10, thickness = 3)
clock = pygame.time.Clock()
previous_time = time.perf_counter()

while True:
    
    # Limit fps
    clock.tick(60)

    # Delta time
    dt = time.perf_counter() - previous_time
    previous_time = time.perf_counter()

    # Fill the screen
    screen.fill("black")
    
    # Draw the visual effect
    larger_ellipse.draw(x = screen.get_width() / 2, y = 200, delta_time = dt)
    smaller_ellipse.draw(x = screen.get_width() / 2, y = 215, delta_time = dt)

    # Update the display
    pygame.display.update()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
