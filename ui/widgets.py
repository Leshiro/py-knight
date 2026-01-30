#imports
import pygame
import ui.colors as colors

#define button classes
class Button:
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.hovered = False
        self.flash_t = 0

    #update on hover
    def update(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    #draw button
    def draw(self, screen, font):
        if self.hovered:
            bg = (100, 100, 100) #hover color
        else:
            bg = (70, 70, 70)

        pygame.draw.rect(screen, bg, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    #do something on click
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
                return True
        return False
    
class ExpandableButton:
    def __init__(self, main_button, child_buttons, padding=8, gap=8):
        self.main_button = main_button
        self.child_buttons = child_buttons
        self.bg_color = colors.UI_COLOR
        self.padding = padding
        self.gap = gap
        self.expanded = False
        self.menu_rect = pygame.Rect(0, 0, 0, 0)

        # main click toggles
        self.main_button.action = self.toggle
        self.reposition_children()

    def toggle(self):
        self.expanded = not self.expanded

    def reposition_children(self):
        if not self.child_buttons:
            self.menu_rect = pygame.Rect(0, 0, 0, 0)
            return

        #compute total width of children row
        child_w = sum(b.rect.width for b in self.child_buttons)
        total_gap = self.gap * (len(self.child_buttons) - 1)
        row_w = child_w + total_gap
        row_h = max(b.rect.height for b in self.child_buttons)

        #background rect size (+ padding)
        bg_w = row_w + self.padding * 2
        bg_h = row_h + self.padding * 2

        #place background above main, centered to main
        bg_x = self.main_button.rect.centerx - bg_w // 2
        bg_y = self.main_button.rect.top - bg_h - self.gap  # small gap above main
        self.menu_rect = pygame.Rect(bg_x, bg_y, bg_w, bg_h)

        #place children inside background
        x = self.menu_rect.left + self.padding
        y = self.menu_rect.top + self.padding + (row_h - self.child_buttons[0].rect.height) // 2

        for b in self.child_buttons:
            b.rect.topleft = (x, self.menu_rect.top + self.padding + (row_h - b.rect.height) // 2)
            x += b.rect.width + self.gap

    def update(self):
        self.main_button.update()
        if self.expanded:
            for b in self.child_buttons:
                b.update()

    def draw(self, screen, font):
        #draw menu first (behind buttons) then children, then main
        if self.expanded:
            pygame.draw.rect(screen, self.bg_color, self.menu_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.menu_rect, 2)

            for b in self.child_buttons:
                b.draw(screen, font)
        self.main_button.draw(screen, font)

    def handle_event(self, event):
        used = False
        if self.expanded:
            for b in self.child_buttons:
                if b.handle_event(event):
                    return True  #consume click immediately
        if self.main_button.handle_event(event):
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and self.expanded:
            if self.menu_rect.collidepoint(event.pos):
                return True
            if not self.main_button.rect.collidepoint(event.pos):
                self.expanded = False
                return True
        return used