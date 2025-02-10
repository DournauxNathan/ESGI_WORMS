# inventory.py
class Inventory:
    def __init__(self):
        self.weapons = ["Weapon 1", "Weapon 2", "Weapon 3"]
        self.current_weapon_index = 0

    def select_weapon(self, index):
        if 0 <= index < len(self.weapons):
            self.current_weapon_index = index

    def get_current_weapon(self):
        return self.weapons[self.current_weapon_index]

    def draw(self, screen, font):
        # Draw the inventory UI
        for i, weapon in enumerate(self.weapons):
            color = (255, 255, 255)  # Default color for weapons
            if i == self.current_weapon_index:
                color = (255, 0, 0)  # Highlight the selected weapon
            weapon_text = font.render(weapon, True, color)
            screen.blit(weapon_text, (50 + i * 150, 50))  # Position the weapons