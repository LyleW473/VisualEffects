        
        # self.mouse_pos = pygame.mouse.get_pos()

        # center = (400, 200)

        # pygame.draw.line(self.surface, "white", (0, center[1]), (self.surface.get_width(), center[1]))
        # pygame.draw.line(self.surface, "white", center, self.mouse_pos)

        # dx = self.mouse_pos[0] - center[0]
        # dy = self.mouse_pos[1] - center[1]

        # # Find the angle between the mouse and center. 
        # # Note: Modulo is so that the value of angle will always be in between 0 and 2pi.
        # # - If the angle is negative, it will be added to 2Pi
        # angle = math.atan2(-dy, dx) % (2 * math.pi)

        # new_angle = angle - math.radians(35)
        # new_angle_2 = angle + math.radians(35)
        # hypot = 50
        # adjacent = hypot * math.cos(new_angle)
        # opposite = hypot * math.sin(new_angle)
        # adjacent_2 = hypot * math.cos(new_angle_2)
        # opposite_2 = hypot * math.sin(new_angle_2)

        # next_point = (center[0] + adjacent, center[1] - opposite)
        # next_point_2 = (center[0] + adjacent_2, center[1] - opposite_2)

        # pygame.draw.line(self.surface, "green", center, next_point)
        # pygame.draw.line(self.surface, "green", center, next_point_2)


        # print(math.degrees(angle))