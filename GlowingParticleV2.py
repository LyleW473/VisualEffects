import pygame, sys, time

class GlowingParticleV2:

    def __init__(self, surface):
        
        # Surface that the glowing particle will be drawn onto
        self.surface = surface

        # List that holds dictionaries containing the information of each particle
        self.particles = []

        # Create the particles for the glowing particle
        self.create_particles()

        # Attribute which determines whether we decrement or increment the radius
        self.decrementing = True

        # The style in which the radius is changed
        self.dynamic_radius_style = 0 # 0, 1, etc.
        

    def create_particles(self):

        # Number of particles
        number_of_particles = 3

        # The smallest radius of all the particles (i.e. the first particle's maximum radius)
        minimum_particle_radius = 20

        # The gap between each particle
        default_gap_between_each_particle = 10
        # The increment gap between each particle (this is so that it looks less "uniform")
        increment_gap_between_each_particle = 5

        # The largest radius of all the particles (i.e. the last particle's maximum radius)
        maximum_particle_radius = minimum_particle_radius + ((number_of_particles - 1) * (default_gap_between_each_particle + ((number_of_particles - 1) * increment_gap_between_each_particle)))

        for i in range(0, number_of_particles):
            
            # Calculate the radius of the particle
            particle_radius = minimum_particle_radius + (i * (default_gap_between_each_particle + (i * increment_gap_between_each_particle)))

            # Create a particle surface with the size set to the last particle's maximum diameter
            particle_surface = pygame.Surface((maximum_particle_radius * 2, maximum_particle_radius * 2))

            # Set the colourkey
            particle_surface.set_colorkey("black")

            # Append the particle surface, the radius that will be changed, the original particle radius
            self.particles.append({"Surface": particle_surface, "Radius": particle_radius, "OriginalRadius": particle_radius})


    def draw(self):
        mouse_position = pygame.mouse.get_pos()


        for i in range(0, len(self.particles)):
            
            # ------------------------------------------------------------------------------------------------------------------------
            # Drawing the particle surface onto the main surface 

            self.particles[i]["Surface"].fill("black")
            pygame.draw.circle(surface = self.particles[i]["Surface"], color  = (25, 0, 0), center = (self.particles[i]["Surface"].get_width() / 2, self.particles[i]["Surface"].get_height() / 2), radius = self.particles[i]["Radius"])
            self.surface.blit(self.particles[i]["Surface"], (mouse_position[0] - (self.particles[i]["Surface"].get_width() / 2), mouse_position[1] - (self.particles[i]["Surface"].get_height() / 2)), special_flags = pygame.BLEND_RGB_ADD)

            # ------------------------------------------------------------------------------------------------------------------------
            # Adjusting the radius of each circle that makes up the particle


            match self.dynamic_radius_style:

                # First dynamic radius style
                case 0:
                
                    # If we are decrementing the radius
                    if self.decrementing == True:
                        
                        # If the current particle's radius is not 0
                        if self.particles[i]["Radius"] != 0:
                            # Decrement the radius
                            self.particles[i]["Radius"] -= 1

                        # If the radius of the last particle inside the particles list is 0
                        if self.particles[len(self.particles) - 1]["Radius"] == 0:
                            self.decrementing = False


                    # If we are incrementing the radius
                    elif self.decrementing == False:

                        # If the last particle's current radius is the same as its original radius 
                        if self.particles[len(self.particles) - 1]["Radius"] == self.particles[len(self.particles) - 1]["OriginalRadius"]:
                            # Start decrementing the radius
                            self.decrementing = True
                        
                        # If this is the first particle and the current radius of the first particle is not the same as its original radius
                        if i == 0 and self.particles[0]["Radius"] != self.particles[0]["OriginalRadius"]:
                            # Increment the radius of the first particle
                            self.particles[i]["Radius"] += 1

                        # If this is not the first particle and the previous particle's radius is the same as its original radius and the current particle's radius is not its original radius
                        elif i > 0 and self.particles[i - 1]["Radius"] == self.particles[i - 1]["OriginalRadius"] and self.particles[i]["Radius"] != self.particles[i]["OriginalRadius"]:
                            
                            # If the radius is currently set to 0
                            if self.particles[i]["Radius"] == 0:
                                # Set it to be the same as the radius of the previous particle
                                self.particles[i]["Radius"] = self.particles[i - 1]["OriginalRadius"]

                            # Increment the radius of the current particle
                            self.particles[i]["Radius"] += 1

                # Second dynamic radius style
                case 1:

                    # If we are decrementing the radius
                    if self.decrementing == True:
                        
                        # If the current particle's radius is not 0
                        if self.particles[i]["Radius"] != 0:
                            # Decrement the radius
                            self.particles[i]["Radius"] -= 1

                        # If the radius of the last particle inside the particles list is 0
                        if self.particles[len(self.particles) - 1]["Radius"] == 0:
                            self.decrementing = False

                    # If we are incrementing the radius
                    elif self.decrementing == False:
                        
                        # If the current radius of the first particle is the same as its original radius
                        if self.particles[0]["Radius"] == self.particles[0]["OriginalRadius"]:
                            # Start decrementing the radius
                            self.decrementing = True

                        # If the current particle is the last particle and the current radius of the last particle is not the same as its original radius
                        if i == len(self.particles) - 1 and self.particles[len(self.particles) - 1]["Radius"] != self.particles[len(self.particles) - 1]["OriginalRadius"]:
                            # Increment the radius of the last particle
                            self.particles[len(self.particles) - 1]["Radius"] += 1

                        # If this is not the last particle and the current radius of the next particle of the current particle is the same as its original radius and the current particle's radius is not the same as its original radius
                        elif i != len(self.particles) - 1 and self.particles[i + 1]["Radius"] == self.particles[i + 1]["OriginalRadius"] and self.particles[i]["Radius"] != self.particles[i]["OriginalRadius"]:
                            # Increment the radius of the current particle
                            self.particles[i]["Radius"] += 1

pygame.display.set_caption("GlowingParticleV2")
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
previous_time = time.perf_counter()
glowing_particle = GlowingParticleV2(surface = screen)

while True:
    
    # Limit fps
    clock.tick(60)

    # Delta time
    dt = time.perf_counter() - previous_time
    previous_time = time.perf_counter()

    # Fill the screen
    screen.fill("black")

    # Draw the glowing particle
    glowing_particle.draw()

    # Update the display
    pygame.display.update()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()