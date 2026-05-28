import pygame


class Button:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text="Button",
        font=None,
        font_size=30,

        base_color=(50, 120, 255),
        hover_color=(30, 90, 220),
        text_color=(255, 255, 255),

        border_radius=12
    ):

        self.rect = pygame.Rect(x, y, width, height)

        self.text = text

        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.border_radius = border_radius

        self.font = pygame.font.SysFont(font, font_size)

    def draw(self, surface):

        mouse_pos = pygame.mouse.get_pos()

        # Hover color
        color = (self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color)

        # Draw button
        pygame.draw.rect(surface,color,self.rect,border_radius=self.border_radius)

        # Draw text
        text_surface = self.font.render(
            self.text,True,self.text_color)

        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self, event):

        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)