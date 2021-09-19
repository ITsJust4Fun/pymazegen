import pygame


class DebugInfo:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.SysFont("Arial", 18)

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps = 'fps: ' + fps
        fps_text = self.font.render(fps, True, pygame.Color("coral"))
        return fps_text

    def update_frame_time(self):
        frame_time = str(int(self.clock.get_time()))
        frame_time = 'frame time: ' + frame_time
        frame_time_text = self.font.render(frame_time, True, pygame.Color("coral"))
        return frame_time_text

    def render(self, options):
        last_y = 0

        if options['fps']:
            self.screen.blit(self.update_fps(), (10, last_y))
            last_y += 20

        if options['frame_time']:
            self.screen.blit(self.update_frame_time(), (10, last_y))
            last_y += 20
