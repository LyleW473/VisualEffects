import pygame, sys, time, random

screen = pygame.display.set_mode((1000, 500))

class FallingPolygons:

    def __init__(self, surface):

        pygame.display.set_caption("FallingPolygons")
        self.surface = surface

        # Dictionary to hold all the polygons created
        self.polygons_dict = {}

        # Number of polygons created, used as the key for each polygon created
        self.polygons_created = 0

        # Colour palettes for the polygons
        self.polygons_colour_palettes = [
            [(125, 229, 237), (129, 198, 232), (93, 167, 219), (88, 55, 208)],
            [(249, 7, 22), (255, 84, 3), (255, 202, 3), (255, 243, 35)],
            [(238, 235, 221), (206, 18, 18), (129, 0, 0), (27, 23, 23)],
            [(62, 193, 211), (246, 247, 215), (255, 154, 0), (255, 22, 93)],
            [(7, 26, 82), (8, 105, 114), (23, 185, 120), (167, 255, 131)]
            ]

        # Chosen colour palette
        self.chosen_colour_palette = len(self.polygons_colour_palettes) - 1
        # Attribute set to True whenever the user wants to switch the colour palette
        self.switch_colour_palette = False

    def create_polygons(self):
        
        # Random width and height of the polygon
        random_width = random.randint(5, 20)
        random_height = random.randint(20, 60)

        # The points go clockwise, with point 1 being the top of the rhombus
        self.point_1 = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        self.point_2 = [self.point_1[0] + random_width, self.point_1[1] + random_height]
        self.point_3 = [self.point_1[0], self.point_1[1] + random_height * 2]
        self.point_4 = [self.point_1[0] - random_width, self.point_1[1] + random_height]
        
        # Calculate the distance the polygon must travel before disappearing and the time 
        distance_polygon_must_travel_to_disappear = random.randint(100, 500)
        time_to_travel_distance = random.randint(5, 10) / 10

        # The dimensions are in the order of: Smallest x, smallest y, largest x, largest y
        self.polygons_dict[self.polygons_created] = {
            "id": self.polygons_created,
            "distance_travelled": 0,
            "distance_polygon_must_travel_to_disappear": distance_polygon_must_travel_to_disappear,
            "gradient": distance_polygon_must_travel_to_disappear / time_to_travel_distance,
            "colour": self.polygons_colour_palettes[self.chosen_colour_palette][random.randint(0, len(self.polygons_colour_palettes[self.chosen_colour_palette]) - 1)],
            "polygon_surface": pygame.Surface((random_width * 2, random_height * 2)),
            "dimensions_list": [[random_width, 0], [random_width * 2, random_height], [random_width, random_height * 2], [0, random_height]],
            "drawing_position" : self.point_1,
            }

        # Increment the number of polygons created
        self.polygons_created += 1

    def draw(self, delta_time):

        # If the left mouse button is pressed
        if pygame.mouse.get_pressed()[0]:
            # For i in range(0, x) to create x polygons per click
            for i in range(0, 1):
                # Create polygons at the mouse position
                self.create_polygons()
        
        # If the "space" key is pressed
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            # Set the switch colour palette attribute to True
            self.switch_colour_palette = True

        # If the "space" key is released and the user has requested to switch the colour palette
        if pygame.key.get_pressed()[pygame.K_SPACE] == False and self.switch_colour_palette == True:
            # If the chosen colour palette is the last one in the colour palettes list
            if self.chosen_colour_palette == (len(self.polygons_colour_palettes) - 1):
                # Go back to the first colour palette in the list
                self.chosen_colour_palette = 0
            # If the chosen colour palette is not the last one in the colour palettes list 
            else:
                # Go to the next colour palette
                self.chosen_colour_palette += 1

            # Set the switch colour palette attribute to False
            self.switch_colour_palette = False
            
        # Loop through the dictionary of each polygon
        for polygon_points_dict in self.polygons_dict.copy().values():

            # If the polygon has not travelled the complete distance
            if polygon_points_dict["distance_travelled"] < polygon_points_dict["distance_polygon_must_travel_to_disappear"]:
                
                # Increase the distance travelled of the entire polygon
                polygon_points_dict["distance_travelled"] += polygon_points_dict["gradient"] * delta_time

                # Update the drawing position of the polygon surface
                polygon_points_dict["drawing_position"][1] += polygon_points_dict["gradient"] * delta_time

                # Draw the polygon onto the polygon surface
                polygon_points_dict["polygon_surface"].set_colorkey("black")
                polygon_points_dict["polygon_surface"].fill("black")
                pygame.draw.polygon(polygon_points_dict["polygon_surface"], polygon_points_dict["colour"], polygon_points_dict["dimensions_list"])

                # Draw the polygon surface onto the main surface, with the special flag
                # Note: The destination is so that the center of the polygon is blitted at the mouse
                self.surface.blit(
                    source = polygon_points_dict["polygon_surface"], 
                    dest = (polygon_points_dict["drawing_position"][0] - (polygon_points_dict["polygon_surface"].get_width() // 2), polygon_points_dict["drawing_position"][1] - (polygon_points_dict["polygon_surface"].get_height() // 2)),  
                    special_flags = pygame.BLEND_RGB_ADD)

            # If the polygon has travelled the complete distance
            else:
                # Delete the polygon from the polygons dictionary
                self.polygons_dict.pop(polygon_points_dict["id"])

clock = pygame.time.Clock()
previous_time = time.perf_counter()

falling_polygons = FallingPolygons(surface = screen)

while True:
    
    # Limit fps
    clock.tick(60)

    # Delta time
    dt = time.perf_counter() - previous_time
    previous_time = time.perf_counter()

    # Fill the screen
    screen.fill("black")

    # Draw the falling polygons
    falling_polygons.draw(delta_time = dt)

    # Update the display
    pygame.display.update()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
