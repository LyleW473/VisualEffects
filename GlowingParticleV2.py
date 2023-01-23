import pygame, sys, time

class GlowingParticleV2:

    def __init__(self, surface, starting_information_dict):
        
        # Surface that the glowing particle will be drawn onto
        self.surface = surface

        # List that holds dictionaries containing the information of each particle
        self.particles = []
        self.starting_information_dict = starting_information_dict        

        # Create the particles for the glowing particle
        self.create_particles()

        # Attribute which determines whether we decrement or increment the radius
        self.decrementing = False

        # The style in which the radius is changed
        self.dynamic_radius_style = 0 # 0, 1, etc.

    def create_particles(self):
        starting_information_dict = {"number_of_particles": 30, "minimum_particle_radius": 3, "default_gap_between_each_particle": 0.2, "increment_gap_between_each_particle": 0.04, "time_to_increment": 2000, "time_to_decrement": 2000}
        """     
        
        # Number of particles
        number_of_particles = self.starting_information_dict["number_of_particles"]

        # The smallest radius of all the particles (i.e. the first particle's maximum radius)
        minimum_particle_radius = self.starting_information_dict["minimum_particle_radius"]

        # The gap between each particle
        default_gap_between_each_particle = self.starting_information_dict["default_gap_between_each_particle"]

        # The increment gap between each particle (this is so that it looks less "uniform")
        increment_gap_between_each_particle = self.starting_information_dict["increment_gap_between_each_particle"]

        # Times to increment to the maximum radius and decrement from the maximum radius to 0
        time_to_increment = self.starting_information_dict["time_to_increment"] / self.starting_information_dict["number_of_particles"] 
        time_to_decrement = self.starting_information_dict["time_to_decrement"]

        """

        # The largest radius of all the particles (i.e. the last particle's maximum radius)
        maximum_particle_radius = self.starting_information_dict["minimum_particle_radius"] + ((self.starting_information_dict["number_of_particles"] - 1) * (self.starting_information_dict["default_gap_between_each_particle"] + ((self.starting_information_dict["number_of_particles"] - 1) * self.starting_information_dict["increment_gap_between_each_particle"])))

        for i in range(0, self.starting_information_dict["number_of_particles"]):

            # ------------------------------------------------------------------------------------------------------------------------
            # Basic properties of all particle surfaces 

            # Create a particle surface with the size set to the last particle's maximum diameter
            particle_surface = pygame.Surface((maximum_particle_radius * 2, maximum_particle_radius * 2))

            # Set the colourkey
            particle_surface.set_colorkey("black")

            # ------------------------------------------------------------------------------------------------------------------------
            # Particle radius

            particle_radius = self.starting_information_dict["minimum_particle_radius"] + (i * self.starting_information_dict["default_gap_between_each_particle"])

            # Time for each particle to reach their maximum radius (in milliseconds)

            # If this is the first particle
            if i == 0 :

                # The increment gradient would be the current particle's radius over time (as this is the first particle)(Time to increment is divided by the number of particles so that it takes in total x seconds to reach the maximum radius of the last particle)
                increment_gradient = particle_radius / (self.starting_information_dict["time_to_increment"] / self.starting_information_dict["number_of_particles"])
                decrement_gradient = particle_radius / self.starting_information_dict["time_to_decrement"]

            # If this is any other particle except from the first particle
            else:

                # The increment gradient would be difference between the current particle's radius and the previous particle's radius. (Time to increment is divided by the number of particles so that it takes in total x seconds to reach the maximum radius of the last particle)
                increment_gradient = (particle_radius - (self.particles[len(self.particles) - 1]["Radius"])) / (self.starting_information_dict["time_to_increment"] / self.starting_information_dict["number_of_particles"])
                decrement_gradient = particle_radius / self.starting_information_dict["time_to_decrement"]
            
            # Increment the gap between each particle
            self.starting_information_dict["default_gap_between_each_particle"] += self.starting_information_dict["increment_gap_between_each_particle"]

            # Append a dictionary containing the particle surface and all the required information
            self.particles.append({"Surface": particle_surface, "Radius": 0, "OriginalRadius": particle_radius, "IncrementGradient": increment_gradient, "DecrementGradient": decrement_gradient})


    def draw(self, delta_time, position):

        for i in range(0, len(self.particles)):
            
            # ------------------------------------------------------------------------------------------------------------------------
            # Drawing the particle surface onto the main surface 

            self.particles[i]["Surface"].fill("black")
            pygame.draw.circle(
                surface = self.particles[i]["Surface"],
                color  = self.starting_information_dict["particle_colour"], 
                center = (self.particles[i]["Surface"].get_width() / 2, self.particles[i]["Surface"].get_height() / 2), 
                radius = self.particles[i]["Radius"])

            self.surface.blit(self.particles[i]["Surface"], (position[0] - (self.particles[i]["Surface"].get_width() / 2), position[1] - (self.particles[i]["Surface"].get_height() / 2)), special_flags = pygame.BLEND_RGB_ADD)

            # ------------------------------------------------------------------------------------------------------------------------
            # Adjusting the radius of each circle that makes up the particle


            match self.dynamic_radius_style:

                # First dynamic radius style
                case 0:
                
                    # If we are decrementing the radius
                    if self.decrementing == True:

                        # If the radius of the last particle inside the particles list is 0
                        if self.particles[len(self.particles) - 1]["Radius"] == 0:
                            self.decrementing = False

                        # If the current particle's radius is not 0
                        if self.particles[i]["Radius"] != 0:

                            # If decrementing the radius will set the current particle's radius below their original radius
                            if self.particles[i]["Radius"] - (self.particles[i]["DecrementGradient"] * (1000 * delta_time)) <= 0:
                                # Set the current particle's radius to be 0 
                                self.particles[i]["Radius"] = 0
                            else:
                                # Decrement the radius of the current particle
                                self.particles[i]["Radius"] -= self.particles[i]["DecrementGradient"] * (1000 * delta_time)

                    # If we are incrementing the radius
                    elif self.decrementing == False:

                        # If the last particle's current radius is the same as its original radius 
                        if self.particles[len(self.particles) - 1]["Radius"] == self.particles[len(self.particles) - 1]["OriginalRadius"]:
                            # Start decrementing the radius
                            self.decrementing = True
                        
                        # If this is the first particle and the current radius of the first particle is not the same as its original radius
                        if i == 0 and self.particles[0]["Radius"] != self.particles[0]["OriginalRadius"]:

                            # If incrementing the radius will set the current particle's radius above their original radius
                            if self.particles[0]["Radius"] + (self.particles[0]["IncrementGradient"] * (1000 * delta_time)) >= self.particles[0]["OriginalRadius"]:
                                # Set the current particle's radius to be its original radius
                                self.particles[0]["Radius"]= self.particles[0]["OriginalRadius"] 
                            else:
                                # Increment the radius of the first particle
                                self.particles[0]["Radius"] +=  self.particles[0]["IncrementGradient"] * (1000 * delta_time)

                        # If this is not the first particle and the previous particle's radius is the same as its original radius and the current particle's radius is not its original radius
                        elif i > 0 and self.particles[i - 1]["Radius"] == self.particles[i - 1]["OriginalRadius"] and self.particles[i]["Radius"] != self.particles[i]["OriginalRadius"]:

                            # If incrementing the radius will set the current particle's radius above their original radius
                            if self.particles[i]["Radius"] + (self.particles[i]["IncrementGradient"] * (1000 * delta_time)) >= self.particles[i]["OriginalRadius"]:
                                # Set the current particle's radius to be its original radius
                                self.particles[i]["Radius"]= self.particles[i]["OriginalRadius"] 
                            else:
                                # Increment the radius of the first particle
                                self.particles[i]["Radius"] +=  self.particles[i]["IncrementGradient"] * (1000 * delta_time)


                # Second dynamic radius style
                case 1:
                    # If we are decrementing the radius
                    if self.decrementing == True:
                        # If the current particle's radius is not 0
                        if self.particles[i]["Radius"] != 0:
                            
                            # If decrementing the radius will set the current particle's radius below their original radius
                            if self.particles[i]["Radius"] - (self.particles[i]["DecrementGradient"] * (1000 * delta_time)) <= 0:
                                # Set the current particle's radius to be 0 
                                self.particles[i]["Radius"] = 0
                            else:
                                # Decrement the radius of the current particle
                                self.particles[i]["Radius"] -= self.particles[i]["DecrementGradient"] * (1000 * delta_time)

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

                            # If incrementing the radius will set the current particle's radius above their original radius
                            if self.particles[len(self.particles) - 1]["Radius"] + (self.particles[len(self.particles) - 1]["IncrementGradient"] * (1000 * delta_time)) >= self.particles[len(self.particles) - 1]["OriginalRadius"]:
                                # Set the current particle's radius to be its original radius
                                self.particles[len(self.particles) - 1]["Radius"] = self.particles[len(self.particles) - 1]["OriginalRadius"]
                            else:
                                # Increment the radius of the last particle
                                self.particles[len(self.particles) - 1]["Radius"] += self.particles[len(self.particles) - 1]["IncrementGradient"] * (1000 * delta_time)

                        # If this is not the last particle and the current radius of the next particle of the current particle is the same as its original radius and the current particle's radius is not the same as its original radius
                        elif i != len(self.particles) - 1 and self.particles[i + 1]["Radius"] == self.particles[i + 1]["OriginalRadius"] and self.particles[i]["Radius"] != self.particles[i]["OriginalRadius"]:
                            
                            # If incrementing the radius will set the current particle's radius above their original radius
                            if self.particles[i]["Radius"] + (self.particles[i]["IncrementGradient"] * (1000 * delta_time)) >=  self.particles[i]["OriginalRadius"]:
                                # Set the current particle's radius to be its original radius
                                self.particles[i]["Radius"] = self.particles[i]["OriginalRadius"]
                            else:
                                # Increment the radius of the current particle
                                self.particles[i]["Radius"] += self.particles[i]["IncrementGradient"] * (1000 * delta_time)


pygame.display.set_caption("GlowingParticleV2")
screen = pygame.display.set_mode((1000, 500))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
previous_time = time.perf_counter()
glowing_particle = GlowingParticleV2(
                                    surface = screen, 
                                    starting_information_dict = { 
                                                                "number_of_particles": 30, 
                                                                "minimum_particle_radius": 0.8, 
                                                                "default_gap_between_each_particle": 0.12, 
                                                                "increment_gap_between_each_particle": 0.02, 
                                                                "time_to_increment": 2500, 
                                                                "time_to_decrement": 2500, 
                                                                "particle_colour": (20, 20, 20)
                                                                }
                                    )

while True:
    
    # Limit fps
    clock.tick(60)

    # Delta time
    dt = time.perf_counter() - previous_time
    previous_time = time.perf_counter()

    # Fill the screen
    screen.fill("black")

    # Draw the glowing particle
    glowing_particle.draw(delta_time = dt, position = pygame.mouse.get_pos())

    # Update the display
    pygame.display.update()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()