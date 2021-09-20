import pygame


class DebugInfo:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.left_offset = 10
        self.top_offset = 20
        self.font = pygame.font.SysFont("Arial", 18)
        self.frametime_size = 150
        self.frametime_array = [0]

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps = 'fps: ' + fps
        fps_text = self.font.render(fps, True, pygame.Color("coral"))
        return fps_text

    def update_frametime(self):
        frametime = str(int(self.clock.get_time()))
        frametime = 'frametime: ' + frametime + ' ms'
        frametime_text = self.font.render(frametime, True, pygame.Color("coral"))
        self.frametime_array.append(int(self.clock.get_time()))

        if len(self.frametime_array) == self.frametime_size:
            del self.frametime_array[0]

        return frametime_text

    def render(self, options):
        last_y = 0
        max_frame = 0

        if options['fps']:
            self.screen.blit(self.update_fps(), (self.left_offset, last_y))
            last_y += self.top_offset

        if options['frametime']:
            self.screen.blit(self.update_frametime(), (self.left_offset, last_y))
            last_y += self.top_offset

        if options['frametime_graph']:
            frame_graph_height = 50
            max_frame = max(self.frametime_array)
            divided = 1

            if max_frame:
                divided = frame_graph_height / max_frame

            def get_y(y): return last_y + (frame_graph_height - y * divided)

            points = [(self.left_offset + x, get_y(y)) for x, y in enumerate(self.frametime_array)]

            pygame.draw.lines(self.screen, pygame.Color("coral"), False, points, 1)
            last_y += frame_graph_height

        if options['frametime_peek']:
            if not max_frame:
                max_frame = max(self.frametime_array)

            peek_frame_str = 'Peek frametime: ' + str(max_frame) + ' ms'
            peek_frame_text = self.font.render(peek_frame_str, True, pygame.Color("coral"))
            self.screen.blit(peek_frame_text, (self.left_offset, last_y))
            last_y += self.top_offset
