import pygame
import sys
import json

# --- Constants and Colors ---
# Adjusted WIDTH and HEIGHT for a non-fullscreen window
WIDTH, HEIGHT = 1366, 730
BLOCK_SIZE = 30

# Grid Colors
EMPTY_GRID_COLOR = (70, 70, 70)
BUILDING_BLOCK_COLOR = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# Redstone Component Colors
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 200)
SLIME_GREEN = (124, 252, 0)
DISPENSER_COLOR = (100, 100, 150)
CHEST_COLOR = (180, 150, 50)
TRAPPED_CHEST_COLOR = (180, 100, 50)
RAIL_COLOR = (80, 80, 80)
POWERED_RAIL_COLOR = (180, 50, 50)
DETECTOR_RAIL_COLOR = (150, 100, 50)
MINECART_COLOR = (120, 120, 120)
OBSERVER_COLOR = (100, 150, 150)
DAYLIGHT_COLOR = (200, 180, 100)
LECTERN_COLOR = (139, 69, 19)
TARGET_COLOR = (180, 80, 80)
BELL_COLOR = (200, 180, 0)
NOTE_BLOCK_COLOR = (150, 100, 50)
LAMP_OFF_COLOR = (80, 80, 0)
LAMP_ON_COLOR = (255, 255, 0)
SCULK_SENSOR_COLOR = (50, 100, 120)

# UI Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
LIGHT_GRAY = (200, 200, 200)
ERASER_COLOR = (200, 200, 200)
TOOLBAR_BACKGROUND_COLOR = (40, 40, 40)
SCROLLBAR_COLOR = (150, 150, 150)
SCROLLBAR_THUMB_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (80, 80, 80) # Darker gray for hover effect
BUTTON_ACTIVE_COLOR = (60, 60, 60) # Even darker for active click

# Logical Grid Dimensions (for scrolling)
LOGICAL_GRID_WIDTH = 100
LOGICAL_GRID_HEIGHT = 100

# Visible Grid Dimensions (based on screen size and toolbar)
# Adjusted to make space for toolbar on the right
VISIBLE_GRID_WIDTH = (WIDTH // BLOCK_SIZE) - 8
VISIBLE_GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# Simulation Timings
SIMULATION_TICK_DURATION = 200  # Milliseconds per simulation tick
BUTTON_PRESS_DURATION = 1000    # How long a button stays pressed
PULSE_DURATION = 200            # Duration of a short Redstone pulse (e.g., Observer)

# Directions (for orientation)
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

DIRECTION_OFFSETS = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0)
}

# --- Pygame Initialization ---
pygame.init()
# Removed pygame.FULLSCREEN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Changed window caption
pygame.display.set_caption("made by hydraw")
FONT = pygame.font.Font(None, 24)
SMALL_FONT = pygame.font.Font(None, 18)
MEDIUM_FONT = pygame.font.Font(None, 20)

# --- Global Variables ---
grid = {} # Stores all placed blocks: {(x, y): Block_Object}
selected_block_type = "REDSTONE_DUST" # Currently selected block from toolbar
simulation_active = False # True if simulation is running
message_display_time = 0 # Timestamp for when current_message should disappear
current_message = "" # Message to display at the bottom left
made_by_hydraw_text = "Made by hydraw" # Signature text

# Grid Scrolling/Panning Variables
offset_x = 0
offset_y = 0
is_dragging_grid = False
last_mouse_pos = (0, 0)

# Toolbar Dimensions
TOOLBAR_WIDTH = WIDTH - (VISIBLE_GRID_WIDTH * BLOCK_SIZE)
TOOLBAR_X_START = VISIBLE_GRID_WIDTH * BLOCK_SIZE

# Toolbar Scrolling Variables
toolbar_scroll_y = 0
toolbar_content_height = 0 # Will be calculated in draw_toolbar
TOOLBAR_SCROLL_SPEED = 30 # Pixels to scroll per mouse wheel click

# List of blocks that typically need a solid block underneath in Minecraft
SURFACE_PLACED_BLOCKS = [
    "REDSTONE_DUST", "LEVER", "REDSTONE_TORCH", "BUTTON", "PRESSURE_PLATE",
    "REPEATER", "COMPARATOR", "LAMP", "TARGET_BLOCK", "BELL", "NOTE_BLOCK",
    "RAIL", "POWERED_RAIL", "DETECTOR_RAIL", "MINECART", "HOPPER_MINECART",
    "SCULK_SENSOR"
]

# --- Block Classes ---
class Block:
    """Base class for all Redstone blocks."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.power_level = 0 # Redstone power level (0-15)
        self.is_powered = False # True if receiving power
        self.type = "BUILDING_BLOCK"
        self.color = BUILDING_BLOCK_COLOR
        self.last_power_state = False # Used for edge detection (e.g., Observers, Bells)
        self.orientation = NORTH # For directional blocks

    def draw(self, screen_surface, offset_x, offset_y):
        """Draws the block on the screen."""
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

    def on_click(self):
        """Handles left-click interaction with the block."""
        pass

    def update(self):
        """Updates the block's state based on Redstone logic."""
        pass

    def get_neighbors(self):
        """Returns a list of (x, y) coordinates of adjacent blocks."""
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < LOGICAL_GRID_WIDTH and 0 <= ny < LOGICAL_GRID_HEIGHT:
                neighbors.append((nx, ny))
        return neighbors

    def get_block_in_direction(self, direction):
        """Returns the block object in a specific direction relative to this block."""
        dx, dy = DIRECTION_OFFSETS[direction]
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < LOGICAL_GRID_WIDTH and 0 <= ny < LOGICAL_GRID_HEIGHT:
            return grid.get((nx, ny))
        return None
    
    def get_coords_in_direction(self, direction):
        """Returns the (x, y) coordinates in a specific direction relative to this block."""
        dx, dy = DIRECTION_OFFSETS[direction]
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < LOGICAL_GRID_WIDTH and 0 <= ny < LOGICAL_GRID_HEIGHT:
            return (nx, ny)
        return None

class BuildingBlock(Block):
    """A simple solid block that can transmit Redstone power but not generate it."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "BUILDING_BLOCK"
        self.color = BUILDING_BLOCK_COLOR

class RedstoneDust(Block):
    """Redstone dust, transmits power with decay."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "REDSTONE_DUST"
        self.color = DARK_RED # Default unpowered color

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        
        # Draw base block color
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

        if self.power_level > 0:
            # Calculate color intensity based on power level
            power_intensity = self.power_level / 15.0
            current_red = int(DARK_RED[0] + (RED[0] - DARK_RED[0]) * power_intensity)
            current_green = int(DARK_RED[1] + (RED[1] - DARK_RED[1]) * power_intensity)
            current_blue = int(DARK_RED[2] + (RED[2] - DARK_RED[2]) * power_intensity)
            dust_color = (current_red, current_green, current_blue)
            
            # Draw powered dust center
            pygame.draw.rect(screen_surface, dust_color, (screen_x + 5, screen_y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)
            
            center_x = screen_x + BLOCK_SIZE // 2
            center_y = screen_y + BLOCK_SIZE // 2
            
            # Draw lines to powered neighbors
            for direction, (dx, dy) in DIRECTION_OFFSETS.items():
                nx, ny = self.x + dx, self.y + dy
                neighbor_block = grid.get((nx, ny))
                
                # Connect if neighbor is dust or a powered component
                if neighbor_block and (neighbor_block.type == "REDSTONE_DUST" or (neighbor_block.is_powered and neighbor_block.type not in ["REDSTONE_DUST"])):
                    end_pos_x = nx * BLOCK_SIZE + offset_x + BLOCK_SIZE // 2
                    end_pos_y = ny * BLOCK_SIZE + offset_y + BLOCK_SIZE // 2
                    pygame.draw.line(screen_surface, dust_color, (center_x, center_y), (end_pos_x, end_pos_y), 2)
        else:
            # Draw unpowered dust dot
            pygame.draw.circle(screen_surface, DARK_RED, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 3)

    def update(self):
        max_incoming_power = 0
        
        # Check power from all neighbors
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block:
                # Direct power from strong power sources (15)
                if neighbor_block.type in ["LEVER", "REDSTONE_BLOCK", "REDSTONE_TORCH", "REPEATER", "COMPARATOR",
                                          "BUTTON", "PRESSURE_PLATE", "COMMAND_BLOCK", "PISTON", "STICKY_PISTON",
                                          "DISPENSER", "DROPPER", "TRAPPED_CHEST", "DETECTOR_RAIL",
                                          "DAYLIGHT_DETECTOR", "LECTERN", "OBSERVER", "TARGET_BLOCK", "BELL", "NOTE_BLOCK", "LAMP", "SCULK_SENSOR"]:
                    if neighbor_block.is_powered:
                        max_incoming_power = max(max_incoming_power, 15)
                # Power from other Redstone dust (decay by 1)
                elif neighbor_block.type == "REDSTONE_DUST" and neighbor_block.power_level > 1:
                    max_incoming_power = max(max_incoming_power, neighbor_block.power_level - 1)

        self.power_level = max_incoming_power
        self.is_powered = (self.power_level > 0)

class Lever(Block):
    """A simple on/off switch."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "LEVER"
        self.is_on = False
        self.color = LIGHT_GRAY

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

        center_x = screen_x + BLOCK_SIZE // 2
        center_y = screen_y + BLOCK_SIZE // 2
        
        # Draw the lever arm and knob
        if self.is_on:
            pygame.draw.line(screen_surface, BLACK, (center_x, center_y), (center_x + 10, center_y - 10), 3)
            pygame.draw.circle(screen_surface, GREEN, (center_x + 10, center_y - 10), 5) # Green knob when on
        else:
            pygame.draw.line(screen_surface, BLACK, (center_x, center_y), (center_x - 10, center_y + 10), 3)
            pygame.draw.circle(screen_surface, BLACK, (center_x - 10, center_y + 10), 5) # Black knob when off

    def on_click(self):
        self.is_on = not self.is_on
        self.is_powered = self.is_on # Lever directly powers when on
        global current_message, message_display_time
        current_message = f"Lever at ({self.x},{self.y}) is {'ON' if self.is_on else 'OFF'}."
        message_display_time = pygame.time.get_ticks() + 2000

    def update(self):
        self.power_level = 15 if self.is_on else 0
        self.is_powered = self.is_on

class RedstoneBlock(Block):
    """A permanent power source (always on)."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "REDSTONE_BLOCK"
        self.color = RED
        self.is_powered = True # Always powered

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, (255, 50, 50), (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, (200, 0, 0), (screen_x + 7, screen_y + 7, BLOCK_SIZE - 14, BLOCK_SIZE - 14), 2, border_radius=1)

    def update(self):
        self.power_level = 15 # Always max power

class RedstoneTorch(Block):
    """A Redstone torch, inverts power and can burn out."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "REDSTONE_TORCH"
        self.is_on = True # Starts on
        self.color = LIGHT_GRAY # Base color of the block it's attached to

        self.last_power_state = False # To detect changes in input power
        self.orientation = SOUTH # Direction the torch is facing (visual only)

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

        center_x = screen_x + BLOCK_SIZE // 2
        center_y = screen_y + BLOCK_SIZE // 2

        # Draw the torch stick based on orientation
        if self.orientation == NORTH:
            pygame.draw.line(screen_surface, BROWN, (center_x, center_y + 10), (center_x, center_y - 5), 3)
        elif self.orientation == EAST:
            pygame.draw.line(screen_surface, BROWN, (center_x - 10, center_y), (center_x + 5, center_y), 3)
        elif self.orientation == SOUTH:
            pygame.draw.line(screen_surface, BROWN, (center_x, center_y - 10), (center_x, center_y + 5), 3)
        elif self.orientation == WEST:
            pygame.draw.line(screen_surface, BROWN, (center_x + 10, center_y), (center_x - 5, center_y), 3)

        # Calculate tip position for flame/smoke
        tip_x, tip_y = center_x, center_y
        if self.orientation == NORTH: tip_y -= 15
        elif self.orientation == EAST: tip_x += 15
        elif self.orientation == SOUTH: tip_y += 15
        elif self.orientation == WEST: tip_x -= 15

        # Draw flame or smoke
        if self.is_on:
            pygame.draw.circle(screen_surface, ORANGE, (tip_x, tip_y), 7)
            pygame.draw.circle(screen_surface, (255, 255, 0), (tip_x, tip_y), 4)
        else:
            pygame.draw.circle(screen_surface, DARK_GRAY, (tip_x, tip_y), 7) # Smoke when off

    def on_click(self):
        self.orientation = (self.orientation + 1) % 4 # Rotate on click
        global current_message, message_display_time
        current_message = f"Redstone Torch at ({self.x},{self.y}) rotated."
        message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        should_turn_off = False
        # Check if any adjacent block is powering the torch
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered and neighbor_block.type != "REDSTONE_TORCH":
                should_turn_off = True
                break
        
        # Torch logic: turns off if powered, turns on if unpowered
        if should_turn_off and self.is_on:
            self.is_on = False
        elif not should_turn_off and not self.is_on:
            self.is_on = True

        self.is_powered = self.is_on # Torch itself is powered if its light is on
        self.power_level = 15 if self.is_on else 0

class CommandBlock(Block):
    """A block that activates when powered."""
    def __init__(self, x, y, name=""):
        super().__init__(x, y)
        self.type = "COMMAND_BLOCK"
        self.name = name if name else f"Command Block {x}-{y}"
        self.color = ORANGE
        self.last_powered_state = False # To detect rising edge (activation)

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, (200, 150, 50), (screen_x + 5, screen_y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)
        text_surf = SMALL_FONT.render("CB", True, BLACK)
        text_rect = text_surf.get_rect(center=(screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2))
        screen_surface.blit(text_surf, text_rect)
        pygame.draw.line(screen_surface, BLACK, (screen_x + 2, screen_y + 2), (screen_x + BLOCK_SIZE - 2, screen_y + BLOCK_SIZE - 2), 1)
        pygame.draw.line(screen_surface, BLACK, (screen_x + BLOCK_SIZE - 2, screen_y + 2), (screen_x + 2, screen_y + BLOCK_SIZE - 2), 1)

    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break

        self.is_powered = current_powered_state
        self.power_level = 15 if self.is_powered else 0

        global current_message, message_display_time
        if self.is_powered and not self.last_powered_state:
            current_message = f"Command Block '{self.name}' activated!"
            message_display_time = pygame.time.get_ticks() + 2000
        self.last_powered_state = self.is_powered

class Piston(Block):
    """Pushes blocks when extended."""
    def __init__(self, x, y, is_sticky=False):
        super().__init__(x, y)
        self.type = "STICKY_PISTON" if is_sticky else "PISTON"
        self.is_sticky = is_sticky
        self.color = (170, 170, 170) # Piston body color
        self.head_color = (200, 0, 0) if not is_sticky else (0, 150, 0) # Head color (red for normal, green for sticky)
        self.is_extended = False
        self.orientation = NORTH # Direction the piston faces

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 5, screen_y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 5, screen_y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10), 1, border_radius=2)
        
        # Draw piston head
        head_rect = None
        if self.orientation == NORTH:
            head_rect = pygame.Rect(screen_x + 5, screen_y, BLOCK_SIZE - 10, 5)
        elif self.orientation == EAST:
            head_rect = pygame.Rect(screen_x + BLOCK_SIZE - 5, screen_y + 5, 5, BLOCK_SIZE - 10)
        elif self.orientation == SOUTH:
            head_rect = pygame.Rect(screen_x + 5, screen_y + BLOCK_SIZE - 5, BLOCK_SIZE - 10, 5)
        elif self.orientation == WEST:
            head_rect = pygame.Rect(screen_x, screen_y + 5, 5, BLOCK_SIZE - 10)

        if head_rect:
            pygame.draw.rect(screen_surface, self.head_color, head_rect)
            pygame.draw.rect(screen_surface, BLACK, head_rect, 1)

        # Draw extended part if extended
        if self.is_extended:
            ext_x, ext_y = self.x * BLOCK_SIZE, self.y * BLOCK_SIZE
            if self.orientation == NORTH:
                pygame.draw.rect(screen_surface, self.head_color, (ext_x + 5 + offset_x, ext_y - BLOCK_SIZE + 5 + offset_y, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)
            elif self.orientation == EAST:
                pygame.draw.rect(screen_surface, self.head_color, (ext_x + BLOCK_SIZE + 5 + offset_x, ext_y + 5 + offset_y, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)
            elif self.orientation == SOUTH:
                pygame.draw.rect(screen_surface, self.head_color, (ext_x + 5 + offset_x, ext_y + BLOCK_SIZE + 5 + offset_y, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)
            elif self.orientation == WEST:
                pygame.draw.rect(screen_surface, self.head_color, (ext_x - BLOCK_SIZE + 5 + offset_x, ext_y + 5 + offset_y, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)


    def on_click(self):
        self.orientation = (self.orientation + 1) % 4 # Rotate on click
        global current_message, message_display_time
        current_message = f"Piston at ({self.x},{self.y}) rotated."
        message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break

        self.is_powered = current_powered_state
        self.power_level = 15 if self.is_powered else 0

        # Piston extension logic
        if self.is_powered and not self.is_extended:
            self.is_extended = True
            pushed_blocks_chain = []
            current_check_coord = self.get_coords_in_direction(self.orientation)
            
            # Find blocks to push (up to 12 blocks)
            while current_check_coord and grid.get(current_check_coord) and \
                  grid.get(current_check_coord).type in ["BUILDING_BLOCK", "SLIME_BLOCK"] and \
                  len(pushed_blocks_chain) < 12:
                pushed_blocks_chain.append(current_check_coord)
                current_check_coord = (current_check_coord[0] + DIRECTION_OFFSETS[self.orientation][0],
                                       current_check_coord[1] + DIRECTION_OFFSETS[self.orientation][1])

            final_destination_coord = current_check_coord
            
            # If destination is clear, move blocks
            if final_destination_coord and (final_destination_coord not in grid):
                for i in range(len(pushed_blocks_chain) - 1, -1, -1): # Move from end of chain first
                    old_coord = pushed_blocks_chain[i]
                    new_coord = (old_coord[0] + DIRECTION_OFFSETS[self.orientation][0],
                                 old_coord[1] + DIRECTION_OFFSETS[self.orientation][1])
                    
                    block_to_move = grid.pop(old_coord)
                    block_to_move.x, block_to_move.y = new_coord
                    grid[new_coord] = block_to_move
                
                if pushed_blocks_chain:
                    global current_message, message_display_time
                    current_message = f"Piston pushed {len(pushed_blocks_chain)} block(s)!"
                    message_display_time = pygame.time.get_ticks() + 1500
            elif pushed_blocks_chain: # Cannot push
                if final_destination_coord is None:
                    current_message = "Piston cannot push block(s) (out of bounds)."
                else:
                    current_message = f"Piston cannot push block(s) at ({final_destination_coord}) (occupied)."
                message_display_time = pygame.time.get_ticks() + 1500


        # Piston retraction logic
        elif not self.is_powered and self.is_extended:
            self.is_extended = False
            if self.is_sticky: # Sticky pistons pull blocks back
                block_to_pull_coord = self.get_coords_in_direction(self.orientation)
                block_to_pull = grid.get(block_to_pull_coord)

                if block_to_pull and block_to_pull.type in ["BUILDING_BLOCK", "SLIME_BLOCK"]:
                    destination_coord = (self.x, self.y) # Pull back to piston's original spot

                    if destination_coord not in grid: 
                        block_to_move = grid.pop(block_to_pull_coord)
                        block_to_move.x, block_to_move.y = destination_coord
                        grid[destination_coord] = block_to_move
                        current_message = f"Sticky Piston pulled {block_to_pull.type}!"
                        message_display_time = pygame.time.get_ticks() + 1500
                    else:
                        current_message = f"Sticky Piston couldn't pull, space at {destination_coord} occupied."
                        message_display_time = pygame.time.get_ticks() + 1500
                else:
                    current_message = "Sticky Piston found nothing movable to pull."
                    message_display_time = pygame.time.get_ticks() + 1500

class Button(Block):
    """A momentary power source."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "BUTTON"
        self.is_pressed = False
        self.press_time = 0
        self.color = LIGHT_GRAY

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

        center_x = screen_x + BLOCK_SIZE // 2
        center_y = screen_y + BLOCK_SIZE // 2
        if self.is_pressed:
            pygame.draw.circle(screen_surface, GREEN, (center_x, center_y), 8) # Green when pressed
        else:
            pygame.draw.circle(screen_surface, BLACK, (center_x, center_y), 8, 2)
            pygame.draw.circle(screen_surface, (120, 120, 120), (center_x, center_y), 6) # Gray when unpressed

    def on_click(self):
        if not self.is_pressed: # Only press if not already pressed
            self.is_pressed = True
            self.press_time = pygame.time.get_ticks()
            global current_message, message_display_time
            current_message = f"Button at ({self.x},{self.y}) pressed!"
            message_display_time = pygame.time.get_ticks() + 2000

    def update(self):
        # Button stays pressed for a duration
        if self.is_pressed and (pygame.time.get_ticks() - self.press_time > BUTTON_PRESS_DURATION):
            self.is_pressed = False
        
        self.is_powered = self.is_pressed
        self.power_level = 15 if self.is_powered else 0

class PressurePlate(Block):
    """Activates when an entity is on it (simulated by click)."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "PRESSURE_PLATE"
        self.is_active = False # Simulates an entity being on it
        self.color = LIGHT_GRAY

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

        if self.is_active:
            pygame.draw.rect(screen_surface, GREEN, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2) # Green when active
        else:
            pygame.draw.rect(screen_surface, (120, 120, 120), (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)
            pygame.draw.rect(screen_surface, (80, 80, 80), (screen_x + 4, screen_y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8), border_radius=2) # Darker gray when inactive

    def on_click(self):
        self.is_active = not self.is_active # Toggle active state
        global current_message, message_display_time
        current_message = f"Pressure Plate at ({self.x},{self.y}) is {'ACTIVE' if self.is_active else 'INACTIVE'}."
        message_display_time = pygame.time.get_ticks() + 2000

    def update(self):
        self.is_powered = self.is_active
        self.power_level = 15 if self.is_powered else 0

class Repeater(Block):
    """Repeats and delays Redstone signals."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "REPEATER"
        self.delay = 1 # Tick delay (1-4)
        self.input_power_received = 0 # Power level from input
        self.output_power_buffer = 0 # Power level to output after delay
        self.current_delay_tick = 0 # Current tick in delay cycle
        self.color = BROWN # Repeater body color
        self.orientation = NORTH # Direction of signal flow

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

        center_x = screen_x + BLOCK_SIZE // 2
        center_y = screen_y + BLOCK_SIZE // 2
        
        pygame.draw.rect(screen_surface, BROWN, (screen_x + 5, screen_y + 10, BLOCK_SIZE - 10, BLOCK_SIZE - 20), border_radius=2)
        
        # Draw repeater torches based on orientation and power state
        if self.orientation == NORTH or self.orientation == SOUTH:
            torch1_pos = (center_x, center_y - 5)
            torch2_pos = (center_x, center_y + 5)
        else: # East/West
            torch1_pos = (center_x - 5, center_y)
            torch2_pos = (center_x + 5, center_y)

        if self.is_powered:
            pygame.draw.circle(screen_surface, RED, torch1_pos, 4)
            pygame.draw.circle(screen_surface, RED, torch2_pos, 4)
        else:
            pygame.draw.circle(screen_surface, DARK_GRAY, torch1_pos, 4)
            pygame.draw.circle(screen_surface, DARK_GRAY, torch2_pos, 4)

        # Display current delay
        delay_text = SMALL_FONT.render(str(self.delay), True, WHITE)
        text_rect = delay_text.get_rect(center=(center_x, center_y + 10))
        screen_surface.blit(delay_text, text_rect)

    def on_click(self):
        self.delay = (self.delay % 4) + 1 # Cycle delay (1, 2, 3, 4)
        global current_message, message_display_time
        current_message = f"Repeater at ({self.x},{self.y}) delay set to {self.delay} ticks."
        message_display_time = pygame.time.get_ticks() + 2000

    def update(self):
        input_direction = (self.orientation + 2) % 4 # Input is always opposite to orientation
        input_block = self.get_block_in_direction(input_direction)
        
        incoming_power = 0
        if input_block and input_block.is_powered: 
            incoming_power = input_block.power_level

        self.input_power_received = incoming_power

        # Reset delay buffer if input changes from off to on
        if self.input_power_received > 0 and not self.last_power_state:
            self.current_delay_tick = 0
            self.output_power_buffer = 0
        
        # Advance delay or output power
        if self.input_power_received > 0:
            if self.current_delay_tick < self.delay:
                self.current_delay_tick += 1
            else:
                self.output_power_buffer = 15 # Output full power after delay
        else:
            self.current_delay_tick = 0
            self.output_power_buffer = 0 # No input, no output

        self.power_level = self.output_power_buffer
        self.is_powered = (self.power_level > 0)
        self.last_power_state = (self.input_power_received > 0)

class Comparator(Block):
    """Compares or subtracts Redstone signals."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "COMPARATOR"
        self.mode = "COMPARE" # "COMPARE" or "SUBTRACT"
        self.input_rear_power = 0 # Power from the back
        self.input_side_power = 0 # Max power from sides
        self.color = BLUE # Comparator body color
        self.orientation = NORTH # Direction of output

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

        center_x = screen_x + BLOCK_SIZE // 2
        center_y = screen_y + BLOCK_SIZE // 2

        pygame.draw.rect(screen_surface, BLUE, (screen_x + 5, screen_y + 10, BLOCK_SIZE - 10, BLOCK_SIZE - 20), border_radius=2)
        
        # Draw comparator torches
        if self.orientation == NORTH or self.orientation == SOUTH:
            torch1_pos = (center_x, center_y - 5)
            torch2_pos = (center_x, center_y + 5)
        else: # East/West
            torch1_pos = (center_x - 5, center_y)
            torch2_pos = (center_x + 5, center_y)

        if self.is_powered:
            pygame.draw.circle(screen_surface, RED, torch1_pos, 4)
            pygame.draw.circle(screen_surface, RED, torch2_pos, 4)
        else:
            pygame.draw.circle(screen_surface, DARK_GRAY, torch1_pos, 4)
            pygame.draw.circle(screen_surface, DARK_GRAY, torch2_pos, 4)

        # Display current mode
        mode_text = SMALL_FONT.render("C" if self.mode == "COMPARE" else "S", True, WHITE)
        text_rect = mode_text.get_rect(center=(center_x, center_y + 10))
        screen_surface.blit(mode_text, text_rect)

    def on_click(self):
        self.mode = "SUBTRACT" if self.mode == "COMPARE" else "COMPARE" # Toggle mode
        global current_message, message_display_time
        current_message = f"Comparator at ({self.x},{self.y}) mode set to {self.mode}."
        message_display_time = pygame.time.get_ticks() + 2000

    def update(self):
        rear_input_direction = (self.orientation + 2) % 4 # Input from back
        side_input_direction_1 = (self.orientation + 1) % 4 # Input from one side
        side_input_direction_2 = (self.orientation + 3) % 4 # Input from other side

        rear_block = self.get_block_in_direction(rear_input_direction)
        side_block_1 = self.get_block_in_direction(side_input_direction_1)
        side_block_2 = self.get_block_in_direction(side_input_direction_2)

        self.input_rear_power = rear_block.power_level if rear_block and rear_block.is_powered else 0
        self.input_side_power = max(
            side_block_1.power_level if side_block_1 and side_block_1.is_powered else 0,
            side_block_2.power_level if side_block_2 and side_block_2.is_powered else 0
        )
        
        output = 0
        if self.mode == "COMPARE":
            if self.input_rear_power >= self.input_side_power:
                output = self.input_rear_power
            else:
                output = 0
        elif self.mode == "SUBTRACT":
            output = max(0, self.input_rear_power - self.input_side_power)
        
        self.power_level = output
        self.is_powered = (self.power_level > 0)

class SlimeBlock(Block):
    """A sticky block that can be pushed/pulled by pistons."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "SLIME_BLOCK"
        self.color = SLIME_GREEN

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, (SLIME_GREEN[0] - 20, SLIME_GREEN[1] - 20, SLIME_GREEN[2] - 20), 
                         (screen_x + 5, screen_y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=2)
        pygame.draw.circle(screen_surface, (255, 255, 255), (screen_x + BLOCK_SIZE // 4, screen_y + BLOCK_SIZE // 4), 3)

    def update(self):
        self.power_level = 0
        self.is_powered = False

class Dispenser(Block):
    """Dispenses items when powered."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "DISPENSER"
        self.color = DISPENSER_COLOR
        self.last_powered_state = False # For pulse detection
        self.orientation = NORTH # Direction of dispensing
        self.inventory = [] # Stores simulated items

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)
        
        # Draw dispensing hole
        hole_center_x, hole_center_y = screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2
        if self.orientation == NORTH: hole_center_y = screen_y + 7
        elif self.orientation == EAST: hole_center_x = screen_x + BLOCK_SIZE - 7
        elif self.orientation == SOUTH: hole_center_y = screen_y + BLOCK_SIZE - 7
        elif self.orientation == WEST: hole_center_x = screen_x + 7

        pygame.draw.circle(screen_surface, BLACK, (hole_center_x, hole_center_y), 5)
        if self.is_powered:
            pygame.draw.circle(screen_surface, GREEN, (hole_center_x, hole_center_y), 3) # Green dot when powered
        
        # Display item count
        if self.inventory:
            count_text = SMALL_FONT.render(str(len(self.inventory)), True, WHITE)
            text_rect = count_text.get_rect(center=(screen_x + BLOCK_SIZE - 10, screen_y + BLOCK_SIZE - 10))
            screen_surface.blit(count_text, text_rect)

    def on_click(self):
        if pygame.mouse.get_pressed()[0]: # Left click to add item
            self.inventory.append("item")
            global current_message, message_display_time
            current_message = f"Dispenser at ({self.x},{self.y}) got an item. ({len(self.inventory)} items)"
            message_display_time = pygame.time.get_ticks() + 1500
        elif pygame.mouse.get_pressed()[2]: # Right click to rotate
            self.orientation = (self.orientation + 1) % 4
            current_message = f"Dispenser at ({self.x},{self.y}) rotated."
            message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break
        
        self.is_powered = current_powered_state
        self.power_level = 15 if self.is_powered else 0

        global current_message, message_display_time
        # Dispense on rising edge of power
        if self.is_powered and not self.last_powered_state:
            if self.inventory:
                self.inventory.pop(0) # Remove one item
                output_coord = self.get_coords_in_direction(self.orientation)
                if output_coord and output_coord not in grid: # Place item entity if space is clear
                    grid[output_coord] = ItemEntity(output_coord[0], output_coord[1])
                current_message = f"Dispenser at ({self.x},{self.y}) dispensed an item! ({len(self.inventory)} left)"
            else:
                current_message = f"Dispenser at ({self.x},{self.y}) is empty."
            message_display_time = pygame.time.get_ticks() + PULSE_DURATION
        self.last_powered_state = self.is_powered

class Dropper(Block):
    """Drops items when powered."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "DROPPER"
        self.color = DISPENSER_COLOR # Same color as dispenser
        self.last_powered_state = False
        self.orientation = NORTH # Direction of dropping
        self.inventory = []

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)
        
        # Draw dropping slot
        slot_center_x, slot_center_y = screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2
        if self.orientation == NORTH: slot_center_y = screen_y + 7
        elif self.orientation == EAST: slot_center_x = screen_x + BLOCK_SIZE - 7
        elif self.orientation == SOUTH: slot_center_y = screen_y + BLOCK_SIZE - 7
        elif self.orientation == WEST: slot_center_x = screen_x + 7

        pygame.draw.rect(screen_surface, BLACK, (slot_center_x - 4, slot_center_y - 4, 8, 8))
        if self.is_powered:
            pygame.draw.rect(screen_surface, GREEN, (slot_center_x - 2, slot_center_y - 2, 4, 4)) # Green when powered

        # Display item count
        if self.inventory:
            count_text = SMALL_FONT.render(str(len(self.inventory)), True, WHITE)
            text_rect = count_text.get_rect(center=(screen_x + BLOCK_SIZE - 10, screen_y + BLOCK_SIZE - 10))
            screen_surface.blit(count_text, text_rect)

    def on_click(self):
        if pygame.mouse.get_pressed()[0]: # Left click to add item
            self.inventory.append("item")
            global current_message, message_display_time
            current_message = f"Dropper at ({self.x},{self.y}) got an item. ({len(self.inventory)} items)"
            message_display_time = pygame.time.get_ticks() + 1500
        elif pygame.mouse.get_pressed()[2]: # Right click to rotate
            self.orientation = (self.orientation + 1) % 4
            current_message = f"Dropper at ({self.x},{self.y}) rotated."
            message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break
        
        self.is_powered = current_powered_state
        self.power_level = 15 if self.is_powered else 0

        global current_message, message_display_time
        # Drop on rising edge of power
        if self.is_powered and not self.last_powered_state:
            if self.inventory:
                self.inventory.pop(0) # Remove one item
                output_coord = self.get_coords_in_direction(self.orientation)
                if output_coord and output_coord not in grid: # Place item entity if space is clear
                    grid[output_coord] = ItemEntity(output_coord[0], output_coord[1])
                current_message = f"Dropper at ({self.x},{self.y}) dropped an item! ({len(self.inventory)} left)"
            else:
                current_message = f"Dropper at ({self.x},{self.y}) is empty."
            message_display_time = pygame.time.get_ticks() + PULSE_DURATION
        self.last_powered_state = self.is_powered

class Hopper(Block):
    """Collects and transfers items."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "HOPPER"
        self.color = DARK_GRAY
        self.is_powered = False # Hoppers are powered (locked) by Redstone
        self.inventory = []

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)
        
        # Draw hopper funnel
        pygame.draw.polygon(screen_surface, (70, 70, 70), [
            (screen_x + 5, screen_y + BLOCK_SIZE - 5),
            (screen_x + BLOCK_SIZE - 5, screen_y + BLOCK_SIZE - 5),
            (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2 + 5)
        ])
        if self.is_powered:
            pygame.draw.rect(screen_surface, RED, (screen_x + BLOCK_SIZE // 2 - 3, screen_y + BLOCK_SIZE // 2 + 7, 6, 6)) # Red dot when locked
        
        # Display item count
        if self.inventory:
            count_text = SMALL_FONT.render(str(len(self.inventory)), True, WHITE)
            text_rect = count_text.get_rect(center=(screen_x + BLOCK_SIZE - 10, screen_y + BLOCK_SIZE - 10))
            screen_surface.blit(count_text, text_rect)

    def on_click(self):
        self.inventory.append("item") # Add item to hopper on click
        global current_message, message_display_time
        current_message = f"Hopper at ({self.x},{self.y}) got an item. ({len(self.inventory)} items)"
        message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break
        
        self.is_powered = current_powered_state # Hopper is locked if powered
        self.power_level = 0 # Hoppers don't output Redstone power directly

        global current_message, message_display_time
        if not self.is_powered and self.inventory: # If not locked and has items
            block_below = self.get_block_in_direction(SOUTH) # Hoppers drop items downwards
            if block_below and block_below.type in ["CHEST", "TRAPPED_CHEST", "HOPPER", "DISPENSER", "DROPPER"]:
                current_message = f"Hopper at ({self.x},{self.y}) transferred an item to {block_below.type}."
                self.inventory.pop(0)
                message_display_time = pygame.time.get_ticks() + 1500
            elif not block_below: # Drop item into the world if no container below
                 current_message = f"Hopper at ({self.x},{self.y}) dropped an item."
                 self.inventory.pop(0)
                 message_display_time = pygame.time.get_ticks() + 1500

class Chest(Block):
    """A storage block."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "CHEST"
        self.color = CHEST_COLOR
        self.inventory = []

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)
        pygame.draw.rect(screen_surface, (100, 80, 0), (screen_x + BLOCK_SIZE // 2 - 2, screen_y + 5, 4, 8)) # Latch
        pygame.draw.rect(screen_surface, (150, 120, 0), (screen_x + BLOCK_SIZE // 2 - 4, screen_y + 13, 8, 4)) # Lock
        
        # Display item count
        if self.inventory:
            count_text = SMALL_FONT.render(str(len(self.inventory)), True, WHITE)
            text_rect = count_text.get_rect(center=(screen_x + BLOCK_SIZE - 10, screen_y + BLOCK_SIZE - 10))
            screen_surface.blit(count_text, text_rect)

    def on_click(self):
        self.inventory.append("item") # Add item to chest on click
        global current_message, message_display_time
        current_message = f"Chest at ({self.x},{self.y}) got an item. ({len(self.inventory)} items)"
        message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        self.power_level = 0
        self.is_powered = False

class TrappedChest(Block):
    """A chest that emits a Redstone signal when opened."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "TRAPPED_CHEST"
        self.color = TRAPPED_CHEST_COLOR
        self.is_open = False
        self.open_time = 0
        self.inventory = []

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)
        pygame.draw.rect(screen_surface, (150, 50, 0), (screen_x + BLOCK_SIZE // 2 - 2, screen_y + 5, 4, 8)) # Latch
        pygame.draw.rect(screen_surface, (200, 80, 0), (screen_x + BLOCK_SIZE // 2 - 4, screen_y + 13, 8, 4)) # Lock (more red for trapped)

        if self.is_powered:
            pygame.draw.circle(screen_surface, RED, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 5) # Red dot when powered
        
        # Display item count
        if self.inventory:
            count_text = SMALL_FONT.render(str(len(self.inventory)), True, WHITE)
            text_rect = count_text.get_rect(center=(screen_x + BLOCK_SIZE - 10, screen_y + BLOCK_SIZE - 10))
            screen_surface.blit(count_text, text_rect)

    def on_click(self):
        if pygame.mouse.get_pressed()[0]: # Left click to add item
            self.inventory.append("item")
            global current_message, message_display_time
            current_message = f"Trapped Chest at ({self.x},{self.y}) got an item. ({len(self.inventory)} items)"
            message_display_time = pygame.time.get_ticks() + 1500
        elif pygame.mouse.get_pressed()[2]: # Right click to open (and power)
            self.is_open = True
            self.open_time = pygame.time.get_ticks()
            current_message = f"Trapped Chest at ({self.x},{self.y}) opened!"
            message_display_time = pygame.time.get_ticks() + 2000

    def update(self):
        # Stays powered for a duration after being opened
        if self.is_open and (pygame.time.get_ticks() - self.open_time < BUTTON_PRESS_DURATION * 2):
            self.is_powered = True
            self.power_level = 15
        else:
            self.is_open = False
            self.is_powered = False
            self.power_level = 0

class Rail(Block):
    """A basic rail for minecarts."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "RAIL"
        self.color = RAIL_COLOR

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        
        # Draw rail tracks
        pygame.draw.line(screen_surface, (150, 150, 150), (screen_x + 5, screen_y + 5), (screen_x + BLOCK_SIZE - 5, screen_y + BLOCK_SIZE - 5), 3)
        pygame.draw.line(screen_surface, (150, 150, 150), (screen_x + BLOCK_SIZE - 5, screen_y + 5), (screen_x + 5, screen_y + BLOCK_SIZE - 5), 3)
        pygame.draw.line(screen_surface, BROWN, (screen_x + BLOCK_SIZE // 2, screen_y + 5), (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE - 5), 2)
        pygame.draw.line(screen_surface, BROWN, (screen_x + 5, screen_y + BLOCK_SIZE // 2), (screen_x + BLOCK_SIZE - 5, screen_y + BLOCK_SIZE // 2), 2)

    def update(self):
        self.power_level = 0
        self.is_powered = False

class PoweredRail(Block):
    """A rail that boosts minecarts when powered."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "POWERED_RAIL"
        self.color = POWERED_RAIL_COLOR
        self.is_powered = False # Powered by Redstone input

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.line(screen_surface, (150, 150, 150), (screen_x + 5, screen_y + 5), (screen_x + BLOCK_SIZE - 5, screen_y + BLOCK_SIZE - 5), 3)
        pygame.draw.line(screen_surface, (150, 150, 150), (screen_x + BLOCK_SIZE - 5, screen_y + 5), (screen_x + 5, screen_y + BLOCK_SIZE - 5), 3)
        
        # Indicate power state
        if self.is_powered:
            pygame.draw.circle(screen_surface, GREEN, (screen_x + 10, screen_y + 10), 3)
            pygame.draw.circle(screen_surface, GREEN, (screen_x + BLOCK_SIZE - 10, screen_y + BLOCK_SIZE - 10), 3)
        else:
            pygame.draw.circle(screen_surface, DARK_RED, (screen_x + 10, screen_y + 10), 3)
            pygame.draw.circle(screen_surface, DARK_RED, (screen_x + BLOCK_SIZE - 10, screen_y + BLOCK_SIZE - 10), 3)

    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break
        self.is_powered = current_powered_state
        self.power_level = 15 if self.is_powered else 0

class DetectorRail(Block):
    """A rail that emits a Redstone signal when a minecart is on it."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "DETECTOR_RAIL"
        self.color = DETECTOR_RAIL_COLOR
        self.is_active = False # True if a minecart is on it

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.line(screen_surface, (150, 150, 150), (screen_x + 5, screen_y + 5), (screen_x + BLOCK_SIZE - 5, screen_y + BLOCK_SIZE - 5), 3)
        pygame.draw.line(screen_surface, (150, 150, 150), (screen_x + BLOCK_SIZE - 5, screen_y + 5), (screen_x + 5, screen_y + BLOCK_SIZE - 5), 3)
        
        # Indicate active state
        if self.is_active:
            pygame.draw.rect(screen_surface, GREEN, (screen_x + 10, screen_y + 10, BLOCK_SIZE - 20, BLOCK_SIZE - 20), border_radius=2)
        else:
            pygame.draw.rect(screen_surface, (100, 70, 30), (screen_x + 10, screen_y + 10, BLOCK_SIZE - 20, BLOCK_SIZE - 20), border_radius=2)

    def update(self):
        self.is_active = False
        # Check if a minecart is on this block
        for nx, ny in self.get_neighbors(): # Check neighbors for minecarts
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and (neighbor_block.type == "MINECART" or neighbor_block.type == "HOPPER_MINECART"):
                if neighbor_block.x == self.x and neighbor_block.y == self.y: # Is the minecart actually on this rail?
                    self.is_active = True
                    break

        self.is_powered = self.is_active
        self.power_level = 15 if self.is_active else 0

class Minecart(Block):
    """A basic minecart that moves on rails."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "MINECART"
        self.color = MINECART_COLOR
        self.speed = 0
        self.direction = EAST # Initial direction
        self.last_rail_coord = (x, y) # To prevent getting stuck

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 5, screen_y + 10, BLOCK_SIZE - 10, BLOCK_SIZE - 15), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 5, screen_y + 10, BLOCK_SIZE - 10, BLOCK_SIZE - 15), 1, border_radius=2)
        pygame.draw.circle(screen_surface, BLACK, (screen_x + 8, screen_y + BLOCK_SIZE - 8), 3) # Wheels
        pygame.draw.circle(screen_surface, BLACK, (screen_x + BLOCK_SIZE - 8, screen_y + BLOCK_SIZE - 8), 3)

    def on_click(self):
        self.speed = 1 # Give it a push!
        global current_message, message_display_time
        current_message = f"Minecart at ({self.x},{self.y}) got a push!"
        message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        current_rail = grid.get((self.x, self.y))
        
        if current_rail and (current_rail.type == "RAIL" or current_rail.type == "POWERED_RAIL" or current_rail.type == "DETECTOR_RAIL"):
            if current_rail.type == "POWERED_RAIL" and current_rail.is_powered:
                self.speed = 1 # Powered rails boost speed
            elif self.speed > 0:
                self.speed = max(0, self.speed - 0.1) # Decelerate on unpowered rails

            if self.speed > 0:
                next_x = self.x + DIRECTION_OFFSETS[self.direction][0]
                next_y = self.y + DIRECTION_OFFSETS[self.direction][1]
                next_coord = (next_x, next_y)
                
                next_block = grid.get(next_coord)

                if next_block and (next_block.type == "RAIL" or next_block.type == "POWERED_RAIL" or next_block.type == "DETECTOR_RAIL"):
                    # Move the minecart
                    del grid[(self.x, self.y)]
                    self.x, self.y = next_coord
                    grid[next_coord] = self
                    self.last_rail_coord = next_coord
                else:
                    self.speed = 0 # Stop if no rail ahead
                    global current_message, message_display_time
                    current_message = f"Minecart at ({self.x},{self.y}) stopped."
                    message_display_time = pygame.time.get_ticks() + 1500
        else:
            self.speed = 0 # Stop if off rails

        self.power_level = 0
        self.is_powered = False

class HopperMinecart(Minecart):
    """A minecart with a built-in hopper."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "HOPPER_MINECART"
        self.hopper_color = DARK_GRAY
        self.inventory = []

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 5, screen_y + 10, BLOCK_SIZE - 10, BLOCK_SIZE - 15), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 5, screen_y + 10, BLOCK_SIZE - 10, BLOCK_SIZE - 15), 1, border_radius=2)
        
        # Draw hopper part
        pygame.draw.polygon(screen_surface, self.hopper_color, [
            (screen_x + 8, screen_y + 10),
            (screen_x + BLOCK_SIZE - 8, screen_y + 10),
            (screen_x + BLOCK_SIZE // 2, screen_y + 15)
        ])
        pygame.draw.circle(screen_surface, BLACK, (screen_x + 8, screen_y + BLOCK_SIZE - 8), 3)
        pygame.draw.circle(screen_surface, BLACK, (screen_x + BLOCK_SIZE - 8, screen_y + BLOCK_SIZE - 8), 3)

        # Display item count
        if self.inventory:
            count_text = SMALL_FONT.render(str(len(self.inventory)), True, WHITE)
            text_rect = count_text.get_rect(center=(screen_x + BLOCK_SIZE - 10, screen_y + BLOCK_SIZE - 10))
            screen_surface.blit(count_text, text_rect)

    def on_click(self):
        if pygame.mouse.get_pressed()[0]: # Left click to add item
            self.inventory.append("item")
            global current_message, message_display_time
            current_message = f"Hopper Minecart at ({self.x},{self.y}) got an item. ({len(self.inventory)} items)"
            message_display_time = pygame.time.get_ticks() + 1500
        elif pygame.mouse.get_pressed()[2]: # Right click to push
            self.speed = 1
            current_message = f"Hopper Minecart at ({self.x},{self.y}) got a push!"
            message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        super().update() # Inherit movement logic from Minecart
        # Add hopper logic here if needed (e.g., picking up items)
        pass

class Observer(Block):
    """Detects block changes and emits a short pulse."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "OBSERVER"
        self.color = OBSERVER_COLOR
        self.orientation = NORTH # Direction of observation (face)
        self.last_observed_block_type = None # Stores type of block it last saw
        self.output_pulse_time = 0 # When the output pulse ends

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)

        # Draw observer face (input side)
        face_x, face_y = screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2
        if self.orientation == NORTH: face_y = screen_y + 7
        elif self.orientation == EAST: face_x = screen_x + BLOCK_SIZE - 7
        elif self.orientation == SOUTH: face_y = screen_y + BLOCK_SIZE - 7
        elif self.orientation == WEST: face_x = screen_x + 7
        pygame.draw.circle(screen_surface, (200, 200, 200), (face_x, face_y), 5) # White eye

        # Draw observer output (back side)
        output_direction = (self.orientation + 2) % 4 # Output is opposite to face
        output_x, output_y = screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2
        if output_direction == NORTH: output_y = screen_y + 7
        elif output_direction == EAST: output_x = screen_x + BLOCK_SIZE - 7
        elif output_direction == SOUTH: output_y = screen_y + BLOCK_SIZE - 7
        elif output_direction == WEST: output_x = screen_x + 7

        if self.is_powered:
            pygame.draw.circle(screen_surface, RED, (output_x, output_y), 5) # Red light when powered
        else:
            pygame.draw.circle(screen_surface, DARK_GRAY, (output_x, output_y), 5) # Gray when unpowered

    def on_click(self):
        self.orientation = (self.orientation + 1) % 4 # Rotate on click
        global current_message, message_display_time
        current_message = f"Observer at ({self.x},{self.y}) rotated."
        message_display_time = pygame.time.get_ticks() + 1500

    def update(self):
        observed_block_coord = self.get_coords_in_direction(self.orientation)
        observed_block = grid.get(observed_block_coord)

        current_observed_type = observed_block.type if observed_block else None

        # Detect changes in the observed block
        if self.last_observed_block_type is None and current_observed_type is not None: # Block placed
            self.output_pulse_time = pygame.time.get_ticks() + PULSE_DURATION
        elif self.last_observed_block_type is not None and current_observed_type is None: # Block broken
            self.output_pulse_time = pygame.time.get_ticks() + PULSE_DURATION
        elif self.last_observed_block_type is not None and current_observed_type is not None and self.last_observed_block_type != current_observed_type: # Block changed type
            self.output_pulse_time = pygame.time.get_ticks() + PULSE_DURATION

        self.last_observed_block_type = current_observed_type

        # Emit pulse if within pulse duration
        if pygame.time.get_ticks() < self.output_pulse_time:
            self.is_powered = True
            self.power_level = 15
        else:
            self.is_powered = False
            self.power_level = 0

class ItemEntity(Block):
    """A visual representation of a dropped item."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "ITEM_ENTITY"
        self.color = (255, 255, 0) # Yellow for item
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 500 # How long the item stays before despawning

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, BLACK, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 10, screen_y + 10, BLOCK_SIZE - 20, BLOCK_SIZE - 20), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 10, screen_y + 10, BLOCK_SIZE - 20, BLOCK_SIZE - 20), 1, border_radius=2)

    def update(self):
        # Returns True if the item should be removed (despawned)
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            return True
        return False

class DaylightDetector(Block):
    """Emits a Redstone signal based on time of day (simulated)."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "DAYLIGHT_DETECTOR"
        self.color = DAYLIGHT_COLOR
        self.is_active = False # Simulates day/night

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)
        pygame.draw.line(screen_surface, DARK_GRAY, (screen_x + 5, screen_y + BLOCK_SIZE // 2), (screen_x + BLOCK_SIZE - 5, screen_y + BLOCK_SIZE // 2), 2)
        pygame.draw.line(screen_surface, DARK_GRAY, (screen_x + BLOCK_SIZE // 2, screen_y + 5), (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE - 5), 2)
        
        if self.is_active:
            pygame.draw.circle(screen_surface, GREEN, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 5) # Green when active (day)

    def on_click(self):
        self.is_active = not self.is_active # Toggle day/night
        global current_message, message_display_time
        current_message = f"Daylight Detector at ({self.x},{self.y}) is now {'ACTIVE (Day)' if self.is_active else 'INACTIVE (Night)'}."
        message_display_time = pygame.time.get_ticks() + 2000

    def update(self):
        self.is_powered = self.is_active
        self.power_level = 15 if self.is_active else 0

class Lectern(Block):
    """Emits a Redstone signal based on book page number (simulated)."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "LECTERN"
        self.color = LECTERN_COLOR
        self.page_number = 0 # Current page (0-15)
        self.max_pages = 15

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 5, screen_y + BLOCK_SIZE - 10, BLOCK_SIZE - 10, 5), border_radius=2)
        pygame.draw.rect(screen_surface, self.color, (screen_x + BLOCK_SIZE // 2 - 5, screen_y + 10, 10, BLOCK_SIZE - 20), border_radius=2)
        pygame.draw.rect(screen_surface, (100, 50, 0), (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, 10), border_radius=2) # Book
        
        # Display current page number
        page_text = SMALL_FONT.render(str(self.page_number), True, WHITE)
        text_rect = page_text.get_rect(center=(screen_x + BLOCK_SIZE // 2, screen_y + 7))
        screen_surface.blit(page_text, text_rect)

    def on_click(self):
        self.page_number = (self.page_number + 1) % (self.max_pages + 1) # Cycle page number
        global current_message, message_display_time
        current_message = f"Lectern at ({self.x},{self.y}) page: {self.page_number} (Power: {self.page_number})."
        message_display_time = pygame.time.get_ticks() + 2000

    def update(self):
        self.power_level = self.page_number # Power level equals page number
        self.is_powered = (self.power_level > 0)

class TargetBlock(Block):
    """Emits a Redstone signal when hit (simulated)."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "TARGET_BLOCK"
        self.color = TARGET_COLOR
        self.is_hit = False
        self.hit_time = 0

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.circle(screen_surface, WHITE, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 10) # Outer ring
        pygame.draw.circle(screen_surface, RED, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 5) # Inner bullseye
        if self.is_hit:
            pygame.draw.circle(screen_surface, GREEN, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 3) # Green dot when hit

    def on_click(self):
        self.is_hit = True
        self.hit_time = pygame.time.get_ticks()
        global current_message, message_display_time
        current_message = f"Target Block at ({self.x},{self.y}) hit!"
        message_display_time = pygame.time.get_ticks() + 1000

    def update(self):
        # Stays powered for a short pulse after being hit
        if self.is_hit and (pygame.time.get_ticks() - self.hit_time > PULSE_DURATION):
            self.is_hit = False
        self.is_powered = self.is_hit
        self.power_level = 15 if self.is_hit else 0

class Bell(Block):
    """Rings when powered."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "BELL"
        self.color = BELL_COLOR
        self.is_ringing = False
        self.ring_time = 0

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 5, screen_y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10), border_radius=3)
        pygame.draw.circle(screen_surface, DARK_GRAY, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2 + 5), 5) # Clapper
        pygame.draw.line(screen_surface, DARK_GRAY, (screen_x + BLOCK_SIZE // 2, screen_y + 5), (screen_x + BLOCK_SIZE // 2, screen_y + 10), 2) # Rope
        if self.is_ringing:
            pygame.draw.circle(screen_surface, WHITE, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 3) # Visual ring effect

    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break
        
        # Ring on rising edge of power
        if current_powered_state and not self.last_power_state:
            self.is_ringing = True
            self.ring_time = pygame.time.get_ticks()
            global current_message, message_display_time
            current_message = f"Bell at ({self.x},{self.y}) rings!"
            message_display_time = pygame.time.get_ticks() + 1000
        
        # Stop ringing after duration
        if self.is_ringing and (pygame.time.get_ticks() - self.ring_time > PULSE_DURATION * 2):
            self.is_ringing = False

        self.last_power_state = current_powered_state
        self.is_powered = False # Bell doesn't output power
        self.power_level = 0

class NoteBlock(Block):
    """Plays a note when powered."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "NOTE_BLOCK"
        self.color = NOTE_BLOCK_COLOR
        self.note_played_time = 0
        self.instrument = 0 # Not implemented: different instruments based on block below
        self.pitch = 0 # Current pitch (0-24)

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        pygame.draw.rect(screen_surface, self.color, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), border_radius=2)
        pygame.draw.rect(screen_surface, BLACK, (screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 1, border_radius=2)
        pygame.draw.circle(screen_surface, WHITE, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 8) # Note symbol
        
        if pygame.time.get_ticks() - self.note_played_time < PULSE_DURATION:
            pygame.draw.circle(screen_surface, GREEN, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 6) # Visual pulse when played

    def on_click(self):
        self.pitch = (self.pitch + 1) % 25 # Cycle pitch (0-24)
        global current_message, message_display_time
        current_message = f"Note Block at ({self.x},{self.y}) pitch: {self.pitch}."
        message_display_time = pygame.time.get_ticks() + 1000

    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break
        
        # Play note on rising edge of power
        if current_powered_state and not self.last_power_state:
            self.note_played_time = pygame.time.get_ticks()
            global current_message, message_display_time
            current_message = f"Note Block at ({self.x},{self.y}) played note (pitch {self.pitch})!"
            message_display_time = pygame.time.get_ticks() + 1000

        self.last_power_state = current_powered_state
        self.is_powered = False # Note block doesn't output power
        self.power_level = 0

class Lamp(Block):
    """Lights up when powered."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "LAMP"
        self.color = LAMP_OFF_COLOR
        self.on_color = LAMP_ON_COLOR

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        current_draw_color = self.on_color if self.is_powered else self.color
        pygame.draw.rect(screen_surface, current_draw_color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        
        center_x = screen_x + BLOCK_SIZE // 2
        center_y = screen_y + BLOCK_SIZE // 2
        if self.is_powered:
            pygame.draw.circle(screen_surface, WHITE, (center_x, center_y), 8) # Bright center when on
            pygame.draw.circle(screen_surface, (255, 255, 150), (center_x, center_y), 5)
        else:
            pygame.draw.circle(screen_surface, (50, 50, 50), (center_x, center_y), 8) # Dark center when off


    def update(self):
        current_powered_state = False
        for nx, ny in self.get_neighbors():
            neighbor_block = grid.get((nx, ny))
            if neighbor_block and neighbor_block.is_powered:
                current_powered_state = True
                break
        
        self.is_powered = current_powered_state # Lamp is powered if receiving power
        self.power_level = 0 # Lamp doesn't output power

class SculkSensor(Block):
    """Detects vibrations and emits a Redstone signal."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "SCULK_SENSOR"
        self.color = SCULK_SENSOR_COLOR
        self.is_active = False # True when vibrating
        self.last_active_time = 0 # When it last vibrated
        self.activation_duration = 500 # How long it stays active

    def draw(self, screen_surface, offset_x, offset_y):
        screen_x = self.x * BLOCK_SIZE + offset_x
        screen_y = self.y * BLOCK_SIZE + offset_y
        pygame.draw.rect(screen_surface, self.color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
        pygame.draw.rect(screen_surface, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)
        
        pygame.draw.circle(screen_surface, (70, 120, 140), (screen_x + 8, screen_y + 8), 4) # Small sensors
        pygame.draw.circle(screen_surface, (70, 120, 140), (screen_x + BLOCK_SIZE - 8, screen_y + 8), 4)
        pygame.draw.circle(screen_surface, (70, 120, 140), (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE - 8), 4)

        if self.is_active:
            pygame.draw.circle(screen_surface, GREEN, (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 7) # Large center sensor, green when active
        else:
            pygame.draw.circle(screen_surface, (30, 60, 70), (screen_x + BLOCK_SIZE // 2, screen_y + BLOCK_SIZE // 2), 7) # Dark when inactive

    def on_click(self):
        self.is_active = True # Simulate a vibration
        self.last_active_time = pygame.time.get_ticks()
        global current_message, message_display_time
        current_message = f"Sculk Sensor at ({self.x},{self.y}) vibrated!"
        message_display_time = pygame.time.get_ticks() + 1000

    def update(self):
        # Stays active for a duration after vibration
        if self.is_active and (pygame.time.get_ticks() - self.last_active_time > self.activation_duration):
            self.is_active = False
        
        self.is_powered = self.is_active
        self.power_level = 15 if self.is_active else 0

# --- Toolbar and UI Elements Data ---
toolbar_items = [
    {"name": "BUILDING_BLOCK", "color": BUILDING_BLOCK_COLOR, "text": "Building Block"},
    {"name": "REDSTONE_DUST", "color": DARK_RED, "text": "Redstone Dust"},
    {"name": "LEVER", "color": LIGHT_GRAY, "text": "Lever"},
    {"name": "BUTTON", "color": LIGHT_GRAY, "text": "Button"},
    {"name": "PRESSURE_PLATE", "color": LIGHT_GRAY, "text": "Pressure Plate"},
    {"name": "REDSTONE_BLOCK", "color": RED, "text": "Redstone Block"},
    {"name": "REDSTONE_TORCH", "color": ORANGE, "text": "Redstone Torch"},
    {"name": "REPEATER", "color": BROWN, "text": "Repeater"},
    {"name": "COMPARATOR", "color": BLUE, "text": "Comparator"},
    {"name": "PISTON", "color": (170, 170, 170), "text": "Piston"},
    {"name": "STICKY_PISTON", "color": (0, 150, 0), "text": "Sticky Piston"},
    {"name": "SLIME_BLOCK", "color": SLIME_GREEN, "text": "Slime Block"},
    {"name": "COMMAND_BLOCK", "color": ORANGE, "text": "Command Block"},
    {"name": "DISPENSER", "color": DISPENSER_COLOR, "text": "Dispenser"},
    {"name": "DROPPER", "color": DISPENSER_COLOR, "text": "Dropper"},
    {"name": "HOPPER", "color": DARK_GRAY, "text": "Hopper"},
    {"name": "CHEST", "color": CHEST_COLOR, "text": "Chest"},
    {"name": "TRAPPED_CHEST", "color": TRAPPED_CHEST_COLOR, "text": "Trapped Chest"},
    {"name": "RAIL", "color": RAIL_COLOR, "text": "Rail"},
    {"name": "POWERED_RAIL", "color": POWERED_RAIL_COLOR, "text": "Powered Rail"},
    {"name": "DETECTOR_RAIL", "color": DETECTOR_RAIL_COLOR, "text": "Detector Rail"},
    {"name": "MINECART", "color": MINECART_COLOR, "text": "Minecart"},
    {"name": "HOPPER_MINECART", "color": MINECART_COLOR, "text": "Hopper Minecart"},
    {"name": "OBSERVER", "color": OBSERVER_COLOR, "text": "Observer"},
    {"name": "DAYLIGHT_DETECTOR", "color": DAYLIGHT_COLOR, "text": "Daylight Detector"},
    {"name": "LECTERN", "color": LECTERN_COLOR, "text": "Lectern"},
    {"name": "TARGET_BLOCK", "color": TARGET_COLOR, "text": "Target Block"},
    {"name": "BELL", "color": BELL_COLOR, "text": "Bell"},
    {"name": "NOTE_BLOCK", "color": NOTE_BLOCK_COLOR, "text": "Note Block"},
    {"name": "LAMP", "color": LAMP_OFF_COLOR, "text": "Lamp"},
    {"name": "SCULK_SENSOR", "color": SCULK_SENSOR_COLOR, "text": "Sculk Sensor"},
    {"name": "ERASER", "color": ERASER_COLOR, "text": "Eraser"},
]

# Mapping of block types to their classes for deserialization
BLOCK_CLASS_MAP = {
    "BUILDING_BLOCK": BuildingBlock,
    "REDSTONE_DUST": RedstoneDust,
    "LEVER": Lever,
    "REDSTONE_BLOCK": RedstoneBlock,
    "REDSTONE_TORCH": RedstoneTorch,
    "COMMAND_BLOCK": CommandBlock,
    "PISTON": Piston,
    "STICKY_PISTON": Piston, # Piston class handles sticky property
    "BUTTON": Button,
    "PRESSURE_PLATE": PressurePlate,
    "REPEATER": Repeater,
    "COMPARATOR": Comparator,
    "SLIME_BLOCK": SlimeBlock,
    "DISPENSER": Dispenser,
    "DROPPER": Dropper,
    "HOPPER": Hopper,
    "CHEST": Chest,
    "TRAPPED_CHEST": TrappedChest,
    "RAIL": Rail,
    "POWERED_RAIL": PoweredRail,
    "DETECTOR_RAIL": DetectorRail,
    "MINECART": Minecart,
    "HOPPER_MINECART": HopperMinecart,
    "OBSERVER": Observer,
    "DAYLIGHT_DETECTOR": DaylightDetector,
    "LECTERN": Lectern,
    "TARGET_BLOCK": TargetBlock,
    "BELL": Bell,
    "NOTE_BLOCK": NoteBlock,
    "LAMP": Lamp,
    "SCULK_SENSOR": SculkSensor,
    "ITEM_ENTITY": ItemEntity # Item entities are not placeable by user but can exist
}

# Mapping from internal block type to Minecraft block ID
MINECRAFT_BLOCK_IDS = {
    "BUILDING_BLOCK": "minecraft:stone",
    "REDSTONE_DUST": "minecraft:redstone_wire",
    "LEVER": "minecraft:lever",
    "REDSTONE_BLOCK": "minecraft:redstone_block",
    "REDSTONE_TORCH": "minecraft:redstone_torch",
    "COMMAND_BLOCK": "minecraft:command_block",
    "PISTON": "minecraft:piston",
    "STICKY_PISTON": "minecraft:sticky_piston",
    "BUTTON": "minecraft:stone_button", # Default to stone button
    "PRESSURE_PLATE": "minecraft:stone_pressure_plate", # Default to stone
    "REPEATER": "minecraft:repeater",
    "COMPARATOR": "minecraft:comparator",
    "SLIME_BLOCK": "minecraft:slime_block",
    "DISPENSER": "minecraft:dispenser",
    "DROPPER": "minecraft:dropper",
    "HOPPER": "minecraft:hopper",
    "CHEST": "minecraft:chest",
    "TRAPPED_CHEST": "minecraft:trapped_chest",
    "RAIL": "minecraft:rail",
    "POWERED_RAIL": "minecraft:powered_rail",
    "DETECTOR_RAIL": "minecraft:detector_rail",
    "MINECART": "minecraft:minecart",
    "HOPPER_MINECART": "minecraft:hopper_minecart",
    "OBSERVER": "minecraft:observer",
    "DAYLIGHT_DETECTOR": "minecraft:daylight_detector",
    "LECTERN": "minecraft:lectern",
    "TARGET_BLOCK": "minecraft:target",
    "BELL": "minecraft:bell",
    "NOTE_BLOCK": "minecraft:note_block",
    "LAMP": "minecraft:redstone_lamp",
    "SCULK_SENSOR": "minecraft:sculk_sensor",
    # Item entities are not blocks in mcstructure
}


# --- UI Drawing Functions ---
def draw_toolbar(screen_surface):
    """Draws the block selection toolbar on the right side of the screen with scrolling."""
    global toolbar_content_height, toolbar_scroll_y

    toolbar_rect = pygame.Rect(TOOLBAR_X_START, 0, TOOLBAR_WIDTH, HEIGHT)
    screen_surface.fill(TOOLBAR_BACKGROUND_COLOR, toolbar_rect)

    # Create a surface for toolbar content to enable scrolling
    # Max height needed for all items
    toolbar_content_height = len(toolbar_items) * 40 + 20 # 40px per item, 20px padding

    # Clamp scroll_y to valid range
    max_scroll = max(0, toolbar_content_height - HEIGHT + 40) # 40 for bottom padding
    toolbar_scroll_y = max(min(toolbar_scroll_y, 0), -max_scroll)

    # Draw toolbar items
    y_offset = 20 + toolbar_scroll_y
    for item in toolbar_items:
        rect = pygame.Rect(TOOLBAR_X_START + 10, y_offset, TOOLBAR_WIDTH - 20, 30)
        color = item["color"]
        
        # Draw button with rounded corners and shadow effect
        pygame.draw.rect(screen_surface, BLACK, (rect.x + 2, rect.y + 2, rect.width, rect.height), border_radius=5) # Shadow
        pygame.draw.rect(screen_surface, color, rect, border_radius=5)
        
        # Highlight if selected
        if selected_block_type == item["name"]:
            pygame.draw.rect(screen_surface, GREEN, rect, 3, border_radius=5)
        
        # Add hover effect
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, rect, border_radius=5)
            pygame.draw.rect(screen_surface, WHITE, rect, 2, border_radius=5) # White border on hover

        text_surf = MEDIUM_FONT.render(item["text"], True, BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        screen_surface.blit(text_surf, text_rect)
        item["rect"] = rect # Store rect for click detection
        y_offset += 40

    # Draw toolbar scrollbar
    if toolbar_content_height > HEIGHT:
        scrollbar_x = TOOLBAR_X_START + TOOLBAR_WIDTH - 15
        scrollbar_width = 10
        scrollbar_height = HEIGHT
        
        pygame.draw.rect(screen_surface, SCROLLBAR_COLOR, (scrollbar_x, 0, scrollbar_width, scrollbar_height))

        # Calculate thumb size and position
        thumb_height = (HEIGHT / toolbar_content_height) * scrollbar_height
        thumb_y = (-toolbar_scroll_y / toolbar_content_height) * scrollbar_height
        
        pygame.draw.rect(screen_surface, SCROLLBAR_THUMB_COLOR, (scrollbar_x, thumb_y, scrollbar_width, thumb_height), border_radius=3)


def draw_info_panel(screen_surface):
    """Draws the simulation status, messages, and signature."""
    info_x_start = VISIBLE_GRID_WIDTH * BLOCK_SIZE + 10
    
    # Simulation Status
    status_text = "Simulation: " + ("Running" if simulation_active else "Paused")
    status_surf = FONT.render(status_text, True, WHITE)
    screen_surface.blit(status_surf, (info_x_start, HEIGHT - 100))

    # Current Message Display
    global current_message, message_display_time
    if pygame.time.get_ticks() < message_display_time:
        message_surf = FONT.render(current_message, True, (255, 255, 0)) # Yellow for messages
        message_rect = message_surf.get_rect(midleft=(10, HEIGHT - 30))
        screen_surface.blit(message_surf, message_rect)
    
    # Signature
    signature_surf = SMALL_FONT.render(made_by_hydraw_text, True, WHITE)
    signature_rect = signature_surf.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
    screen_surface.blit(signature_surf, signature_rect)

def draw_controls(screen_surface):
    """Draws the control buttons (Start/Stop, Clear Grid, Export, Import)."""
    control_x_start = VISIBLE_GRID_WIDTH * BLOCK_SIZE + 10
    y_offset = HEIGHT - 60 # Position controls near the bottom

    # Start/Stop Simulation Button
    start_stop_text = "Stop Simulation" if simulation_active else "Start Simulation"
    start_stop_color = RED if simulation_active else GREEN
    start_stop_rect = pygame.Rect(control_x_start, y_offset, TOOLBAR_WIDTH - 20, 30)
    pygame.draw.rect(screen_surface, BLACK, (start_stop_rect.x + 2, start_stop_rect.y + 2, start_stop_rect.width, start_stop_rect.height), border_radius=5) # Shadow
    pygame.draw.rect(screen_surface, start_stop_color, start_stop_rect, border_radius=5)
    
    mouse_pos = pygame.mouse.get_pos()
    if start_stop_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, start_stop_rect, border_radius=5)
        pygame.draw.rect(screen_surface, WHITE, start_stop_rect, 2, border_radius=5)

    text_surf = FONT.render(start_stop_text, True, WHITE)
    text_rect = text_surf.get_rect(center=start_stop_rect.center)
    screen_surface.blit(text_surf, text_rect)
    
    global start_stop_button_rect
    start_stop_button_rect = start_stop_rect

    # Clear Grid Button
    clear_grid_rect = pygame.Rect(control_x_start, y_offset + 40, TOOLBAR_WIDTH - 20, 30)
    pygame.draw.rect(screen_surface, BLACK, (clear_grid_rect.x + 2, clear_grid_rect.y + 2, clear_grid_rect.width, clear_grid_rect.height), border_radius=5) # Shadow
    pygame.draw.rect(screen_surface, (200, 100, 0), clear_grid_rect, border_radius=5) # Orange color
    
    if clear_grid_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, clear_grid_rect, border_radius=5)
        pygame.draw.rect(screen_surface, WHITE, clear_grid_rect, 2, border_radius=5)

    text_surf = FONT.render("Clear Grid", True, WHITE)
    text_rect = text_surf.get_rect(center=clear_grid_rect.center)
    screen_surface.blit(text_surf, text_rect)
    
    global clear_grid_button_rect
    clear_grid_button_rect = clear_grid_rect

    # Export Grid Button
    export_grid_rect = pygame.Rect(control_x_start, y_offset + 80, TOOLBAR_WIDTH - 20, 30)
    pygame.draw.rect(screen_surface, BLACK, (export_grid_rect.x + 2, export_grid_rect.y + 2, export_grid_rect.width, export_grid_rect.height), border_radius=5) # Shadow
    pygame.draw.rect(screen_surface, (50, 150, 200), export_grid_rect, border_radius=5) # Blue color
    
    if export_grid_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, export_grid_rect, border_radius=5)
        pygame.draw.rect(screen_surface, WHITE, export_grid_rect, 2, border_radius=5)

    text_surf = FONT.render("Export Grid (JSON)", True, WHITE)
    text_rect = text_surf.get_rect(center=export_grid_rect.center)
    screen_surface.blit(text_surf, text_rect)
    
    global export_grid_button_rect
    export_grid_button_rect = export_grid_rect

    # Load Sample Grid Button (simulated import)
    load_sample_grid_rect = pygame.Rect(control_x_start, y_offset + 120, TOOLBAR_WIDTH - 20, 30)
    pygame.draw.rect(screen_surface, BLACK, (load_sample_grid_rect.x + 2, load_sample_grid_rect.y + 2, load_sample_grid_rect.width, load_sample_grid_rect.height), border_radius=5) # Shadow
    pygame.draw.rect(screen_surface, (100, 200, 100), load_sample_grid_rect, border_radius=5) # Light green color

    if load_sample_grid_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, load_sample_grid_rect, border_radius=5)
        pygame.draw.rect(screen_surface, WHITE, load_sample_grid_rect, 2, border_radius=5)

    text_surf = FONT.render("Load Sample Grid", True, WHITE)
    text_rect = text_surf.get_rect(center=load_sample_grid_rect.center)
    screen_surface.blit(text_surf, text_rect)
    
    global load_sample_grid_button_rect
    load_sample_grid_button_rect = load_sample_grid_rect

    # Export .mcstructure (JSON) Button
    export_mcstructure_rect = pygame.Rect(control_x_start, y_offset + 160, TOOLBAR_WIDTH - 20, 30)
    pygame.draw.rect(screen_surface, BLACK, (export_mcstructure_rect.x + 2, export_mcstructure_rect.y + 2, export_mcstructure_rect.width, export_mcstructure_rect.height), border_radius=5) # Shadow
    pygame.draw.rect(screen_surface, (200, 150, 50), export_mcstructure_rect, border_radius=5) # Gold-ish color
    
    if export_mcstructure_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen_surface, BUTTON_HOVER_COLOR, export_mcstructure_rect, border_radius=5)
        pygame.draw.rect(screen_surface, WHITE, export_mcstructure_rect, 2, border_radius=5)

    text_surf = FONT.render("Export .mcstructure (JSON)", True, WHITE)
    text_rect = text_surf.get_rect(center=export_mcstructure_rect.center)
    screen_surface.blit(text_surf, text_rect)
    
    global export_mcstructure_button_rect
    export_mcstructure_button_rect = export_mcstructure_rect


def draw_scrollbars(screen_surface, offset_x, offset_y):
    """Draws horizontal and vertical scrollbars for the grid."""
    h_bar_height = 15
    h_bar_width = VISIBLE_GRID_WIDTH * BLOCK_SIZE
    h_bar_x = 0
    h_bar_y = HEIGHT - h_bar_height

    # Horizontal scrollbar background
    pygame.draw.rect(screen_surface, SCROLLBAR_COLOR, (h_bar_x, h_bar_y, h_bar_width, h_bar_height))

    total_content_width = LOGICAL_GRID_WIDTH * BLOCK_SIZE
    visible_content_width = VISIBLE_GRID_WIDTH * BLOCK_SIZE
    
    if total_content_width > visible_content_width:
        thumb_width = (visible_content_width / total_content_width) * h_bar_width
        thumb_x = h_bar_x + (-offset_x / (total_content_width - visible_content_width)) * (h_bar_width - thumb_width)
        pygame.draw.rect(screen_surface, SCROLLBAR_THUMB_COLOR, (thumb_x, h_bar_y, thumb_width, h_bar_height), border_radius=3)

    v_bar_width = 15
    v_bar_height = VISIBLE_GRID_HEIGHT * BLOCK_SIZE
    v_bar_x = VISIBLE_GRID_WIDTH * BLOCK_SIZE - v_bar_width
    v_bar_y = 0

    # Vertical scrollbar background
    pygame.draw.rect(screen_surface, SCROLLBAR_COLOR, (v_bar_x, v_bar_y, v_bar_width, v_bar_height))

    total_content_height = LOGICAL_GRID_HEIGHT * BLOCK_SIZE
    visible_content_height = VISIBLE_GRID_HEIGHT * BLOCK_SIZE

    if total_content_height > visible_content_height:
        thumb_height = (visible_content_height / total_content_height) * v_bar_height
        thumb_y = v_bar_y + (-offset_y / (total_content_height - visible_content_height)) * (v_bar_height - thumb_height)
        pygame.draw.rect(screen_surface, SCROLLBAR_THUMB_COLOR, (v_bar_x, thumb_y, v_bar_width, thumb_height), border_radius=3)

# --- Export/Import Functions ---
def export_grid_to_json():
    """Converts the current grid state into a JSON string."""
    serializable_grid = []
    for (x, y), block in grid.items():
        block_data = {
            "x": block.x,
            "y": block.y,
            "type": block.type,
            "is_powered": block.is_powered,
            "power_level": block.power_level,
            "orientation": block.orientation
        }
        # Add specific properties for each block type
        if block.type == "LEVER":
            block_data["is_on"] = block.is_on
        elif block.type == "REDSTONE_TORCH":
            block_data["is_on"] = block.is_on
        elif block.type == "BUTTON":
            block_data["is_pressed"] = block.is_pressed
            block_data["press_time"] = block.press_time # Store for continuation if needed
        elif block.type == "PRESSURE_PLATE":
            block_data["is_active"] = block.is_active
        elif block.type == "REPEATER":
            block_data["delay"] = block.delay
        elif block.type == "COMPARATOR":
            block_data["mode"] = block.mode
        elif block.type in ["PISTON", "STICKY_PISTON"]:
            block_data["is_sticky"] = block.is_sticky
            block_data["is_extended"] = block.is_extended
        elif block.type in ["DISPENSER", "DROPPER", "HOPPER", "CHEST", "TRAPPED_CHEST", "HOPPER_MINECART"]:
            block_data["inventory"] = block.inventory # Store simple item names
        elif block.type == "TRAPPED_CHEST":
            block_data["is_open"] = block.is_open
            block_data["open_time"] = block.open_time
        elif block.type == "MINECART":
            block_data["speed"] = block.speed
            block_data["direction"] = block.direction
        elif block.type == "OBSERVER":
            block_data["last_observed_block_type"] = block.last_observed_block_type
        elif block.type == "DAYLIGHT_DETECTOR":
            block_data["is_active"] = block.is_active
        elif block.type == "LECTERN":
            block_data["page_number"] = block.page_number
        elif block.type == "TARGET_BLOCK":
            block_data["is_hit"] = block.is_hit
        elif block.type == "BELL":
            block_data["is_ringing"] = block.is_ringing
        elif block.type == "NOTE_BLOCK":
            block_data["pitch"] = block.pitch
        elif block.type == "SCULK_SENSOR":
            block_data["is_active"] = block.is_active
            block_data["last_active_time"] = block.last_active_time

        serializable_grid.append(block_data)
    
    return json.dumps(serializable_grid, indent=4)

def import_grid_from_json(json_string):
    """Reconstructs the grid from a JSON string."""
    global grid, current_message, message_display_time
    try:
        data = json.loads(json_string)
        new_grid = {}
        for block_data in data:
            block_type = block_data.get("type")
            x = block_data.get("x")
            y = block_data.get("y")

            if block_type and (x is not None) and (y is not None) and (block_type in BLOCK_CLASS_MAP):
                block_class = BLOCK_CLASS_MAP[block_type]
                
                # Handle special cases for constructor arguments
                if block_type in ["PISTON", "STICKY_PISTON"]:
                    new_block = block_class(x, y, is_sticky=block_data.get("is_sticky", False))
                else:
                    new_block = block_class(x, y)
                
                # Set common properties
                new_block.power_level = block_data.get("power_level", 0)
                new_block.is_powered = block_data.get("is_powered", False)
                new_block.orientation = block_data.get("orientation", NORTH)

                # Set specific properties
                if block_type == "LEVER":
                    new_block.is_on = block_data.get("is_on", False)
                elif block_type == "REDSTONE_TORCH":
                    new_block.is_on = block_data.get("is_on", True)
                elif block_type == "BUTTON":
                    new_block.is_pressed = block_data.get("is_pressed", False)
                    new_block.press_time = block_data.get("press_time", 0)
                elif block_type == "PRESSURE_PLATE":
                    new_block.is_active = block_data.get("is_active", False)
                elif block_type == "REPEATER":
                    new_block.delay = block_data.get("delay", 1)
                elif block_type == "COMPARATOR":
                    new_block.mode = block_data.get("mode", "COMPARE")
                elif block_type in ["PISTON", "STICKY_PISTON"]:
                    new_block.is_extended = block_data.get("is_extended", False)
                elif block_type in ["DISPENSER", "DROPPER", "HOPPER", "CHEST", "TRAPPED_CHEST", "HOPPER_MINECART"]:
                    new_block.inventory = block_data.get("inventory", [])
                elif block_type == "TRAPPED_CHEST":
                    new_block.is_open = block_data.get("is_open", False)
                    new_block.open_time = block_data.get("open_time", 0)
                elif block_type == "MINECART":
                    new_block.speed = block_data.get("speed", 0)
                    new_block.direction = block_data.get("direction", EAST)
                elif block_type == "OBSERVER":
                    new_block.last_observed_block_type = block_data.get("last_observed_block_type", None)
                elif block_type == "DAYLIGHT_DETECTOR":
                    new_block.is_active = block_data.get("is_active", False)
                elif block_type == "LECTERN":
                    new_block.page_number = block_data.get("page_number", 0)
                elif block_type == "TARGET_BLOCK":
                    new_block.is_hit = block_data.get("is_hit", False)
                elif block_type == "BELL":
                    new_block.is_ringing = block_data.get("is_ringing", False)
                elif block_type == "NOTE_BLOCK":
                    new_block.pitch = block_data.get("pitch", 0)
                elif block_type == "SCULK_SENSOR":
                    new_block.is_active = block_data.get("is_active", False)
                    new_block.last_active_time = block_data.get("last_active_time", 0)

                new_grid[(x, y)] = new_block
            else:
                print(f"Warning: Could not load block data: {block_data}")
        grid = new_grid
        current_message = "Grid loaded successfully!"
        message_display_time = pygame.time.get_ticks() + 3000
    except json.JSONDecodeError as e:
        current_message = f"Error loading grid: Invalid JSON. {e}"
        message_display_time = pygame.time.get_ticks() + 5000
    except Exception as e:
        current_message = f"Error loading grid: {e}"
        message_display_time = pygame.time.get_ticks() + 5000

def load_sample_grid():
    """Loads a predefined sample Redstone circuit."""
    sample_json = """
    [
        {"x": 2, "y": 2, "type": "REDSTONE_BLOCK", "is_powered": true, "power_level": 15, "orientation": 0},
        {"x": 3, "y": 2, "type": "REDSTONE_DUST", "is_powered": true, "power_level": 14, "orientation": 0},
        {"x": 4, "y": 2, "type": "REDSTONE_DUST", "is_powered": true, "power_level": 13, "orientation": 0},
        {"x": 5, "y": 2, "type": "LAMP", "is_powered": true, "power_level": 0, "orientation": 0},
        {"x": 2, "y": 4, "type": "LEVER", "is_powered": false, "power_level": 0, "is_on": false, "orientation": 0},
        {"x": 3, "y": 4, "type": "REPEATER", "is_powered": false, "power_level": 0, "delay": 2, "orientation": 1},
        {"x": 4, "y": 4, "type": "PISTON", "is_powered": false, "power_level": 0, "is_sticky": false, "is_extended": false, "orientation": 1},
        {"x": 5, "y": 4, "type": "BUILDING_BLOCK", "is_powered": false, "power_level": 0, "orientation": 0},
        {"x": 2, "y": 6, "type": "SCULK_SENSOR", "is_powered": false, "power_level": 0, "is_active": false, "last_active_time": 0, "orientation": 0},
        {"x": 3, "y": 6, "type": "REDSTONE_DUST", "is_powered": false, "power_level": 0, "orientation": 0},
        {"x": 4, "y": 6, "type": "NOTE_BLOCK", "is_powered": false, "power_level": 0, "pitch": 12, "orientation": 0}
    ]
    """
    import_grid_from_json(sample_json)
    global current_message, message_display_time
    current_message = "Sample grid loaded! Try interacting with the lever and sculk sensor."
    message_display_time = pygame.time.get_ticks() + 5000

def export_mcstructure_json():
    """
    Exports the current grid to a simplified JSON format resembling Minecraft .mcstructure.
    Note: This is a simplified textual representation, not a true binary .mcstructure file.
    It focuses on block IDs and positions.
    """
    if not grid:
        return json.dumps({"error": "No blocks to export."}, indent=4)

    min_x = min(b.x for b in grid.values())
    max_x = max(b.x for b in grid.values())
    min_y = min(b.y for b in grid.values())
    max_y = max(b.y for b in grid.values())

    # Assuming a 2D grid maps to a single Z-layer in Minecraft
    size_x = max_x - min_x + 1
    size_y = max_y - min_y + 1
    size_z = 1 # Always 1 for a 2D grid representation

    blocks_data = []
    for (x, y), block in grid.items():
        mc_id = MINECRAFT_BLOCK_IDS.get(block.type)
        if not mc_id:
            # Skip blocks not mapped or use a default
            print(f"Warning: Skipping unmapped block type: {block.type}")
            continue

        # Relative coordinates within the structure
        relative_x = x - min_x
        relative_y = y - min_y
        
        block_entry = {
            "pos": [relative_x, relative_y, 0], # Z is always 0 for 2D
            "name": mc_id,
            "states": {} # Placeholder for block states
        }

        # Add common block states based on simulator properties
        if block.type in ["LEVER", "REDSTONE_TORCH", "BUTTON", "PRESSURE_PLATE", "DAYLIGHT_DETECTOR", "SCULK_SENSOR"]:
            block_entry["states"]["powered"] = block.is_powered
        
        if block.type == "LEVER":
            block_entry["states"]["open"] = block.is_on # Lever state
            # Minecraft levers have direction, face, and powered state
            # This is a simplification. Full mapping would be complex.
            block_entry["states"]["direction"] = block.orientation # Simplified mapping
        
        if block.type == "REDSTONE_TORCH":
            block_entry["states"]["lit"] = block.is_on
            block_entry["states"]["facing_direction"] = block.orientation # Simplified mapping

        if block.type in ["PISTON", "STICKY_PISTON"]:
            block_entry["states"]["extended"] = block.is_extended
            block_entry["states"]["facing_direction"] = block.orientation
            block_entry["states"]["type"] = "sticky" if block.is_sticky else "normal"

        if block.type == "REPEATER":
            block_entry["states"]["delay"] = block.delay
            block_entry["states"]["facing_direction"] = block.orientation
            block_entry["states"]["locked"] = False # Not simulated
            block_entry["states"]["powered"] = block.is_powered

        if block.type == "COMPARATOR":
            block_entry["states"]["mode"] = block.mode.lower() # "compare" or "subtract"
            block_entry["states"]["facing_direction"] = block.orientation
            block_entry["states"]["powered"] = block.is_powered

        if block.type in ["DISPENSER", "DROPPER", "OBSERVER"]:
            block_entry["states"]["facing_direction"] = block.orientation
            block_entry["states"]["triggered"] = block.is_powered # Dispenser/Dropper triggered state

        if block.type == "HOPPER":
            block_entry["states"]["enabled"] = not block.is_powered # Hopper is enabled when not powered by redstone
            # Hopper direction is also a state, but we don't simulate it in the Block class
        
        if block.type in ["CHEST", "TRAPPED_CHEST"]:
            # Minecraft chests don't have "is_open" as a block state, but as NBT data or entity data.
            # We'll just note it here for conceptual completeness.
            if block.type == "TRAPPED_CHEST":
                block_entry["states"]["trapped"] = True
            # For inventory, this would typically be NBT data in block_entities
            if block.inventory:
                block_entry["nbt_data"] = {"Items": [{"id": "minecraft:stone", "Count": len(block.inventory)}]} # Simplified item representation

        if block.type in ["RAIL", "POWERED_RAIL", "DETECTOR_RAIL"]:
            block_entry["states"]["shape"] = "straight" # Simplified, could be curved
            if block.type == "POWERED_RAIL":
                block_entry["states"]["powered"] = block.is_powered
            if block.type == "DETECTOR_RAIL":
                block_entry["states"]["powered"] = block.is_active # Detector rail powers when active

        if block.type == "LECTERN":
            block_entry["states"]["has_book"] = True # Assuming it has a book if placed
            block_entry["nbt_data"] = {"Book": {"Page": block.page_number}} # Simplified page data

        if block.type == "NOTE_BLOCK":
            block_entry["states"]["note"] = block.pitch
            # Instrument is determined by block below, not handled here

        if block.type == "LAMP":
            block_entry["states"]["lit"] = block.is_powered


        blocks_data.append(block_entry)

    # Simplified .mcstructure JSON format
    mcstructure_json = {
        "format_version": 1,
        "size": [size_x, size_y, size_z],
        "structure_world_origin": [min_x, min_y, 0], # Origin of the structure in world coords
        "blocks": blocks_data,
        "entities": [], # Not simulating entities directly
        "block_entities": [] # Complex NBT data for special blocks (chests, command blocks)
    }

    # Populate block_entities for blocks that typically have NBT data
    for block_entry in blocks_data:
        if "nbt_data" in block_entry:
            # In a real .mcstructure, block_entities would contain NBT data
            # and reference the block's position. This is a simplified representation.
            mcstructure_json["block_entities"].append({
                "pos": block_entry["pos"],
                "nbt_data": block_entry["nbt_data"]
            })
            del block_entry["nbt_data"] # Remove from block's direct data if moved to block_entities

    return json.dumps(mcstructure_json, indent=4)


# --- Main Game Loop ---
def run_game():
    global selected_block_type, simulation_active, grid, offset_x, offset_y, is_dragging_grid, last_mouse_pos, toolbar_scroll_y

    running = True
    clock = pygame.time.Clock()
    simulation_tick_event = pygame.USEREVENT + 1
    pygame.time.set_timer(simulation_tick_event, SIMULATION_TICK_DURATION)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x = (mouse_x - offset_x) // BLOCK_SIZE
                grid_y = (mouse_y - offset_y) // BLOCK_SIZE

                # Check if click is within the main grid area
                if mouse_x < VISIBLE_GRID_WIDTH * BLOCK_SIZE and mouse_y < VISIBLE_GRID_HEIGHT * BLOCK_SIZE:
                    if event.button == 1: # Left click
                        if selected_block_type == "ERASER":
                            if (grid_x, grid_y) in grid:
                                del grid[(grid_x, grid_y)]
                        else:
                            if (grid_x, grid_y) not in grid: # Place new block
                                new_block = None
                                # For surface-placed blocks, ensure a building block is underneath if not already there
                                if selected_block_type in SURFACE_PLACED_BLOCKS and (grid_x, grid_y) not in grid:
                                    # We don't explicitly place a building block underneath for visual purposes,
                                    # but the logic assumes it's on a surface.
                                    # In a full game, you'd place a solid block first.
                                    pass # No need to add BuildingBlock if it's just a visual base

                                if selected_block_type == "REDSTONE_DUST":
                                    new_block = RedstoneDust(grid_x, grid_y)
                                elif selected_block_type == "LEVER":
                                    new_block = Lever(grid_x, grid_y)
                                elif selected_block_type == "REDSTONE_TORCH":
                                    new_block = RedstoneTorch(grid_x, grid_y)
                                elif selected_block_type == "BUTTON":
                                    new_block = Button(grid_x, grid_y)
                                elif selected_block_type == "PRESSURE_PLATE":
                                    new_block = PressurePlate(grid_x, grid_y)
                                elif selected_block_type == "REPEATER":
                                    new_block = Repeater(grid_x, grid_y)
                                elif selected_block_type == "COMPARATOR":
                                    new_block = Comparator(grid_x, grid_y)
                                elif selected_block_type == "LAMP":
                                    new_block = Lamp(grid_x, grid_y)
                                elif selected_block_type == "TARGET_BLOCK":
                                    new_block = TargetBlock(grid_x, grid_y)
                                elif selected_block_type == "BELL":
                                    new_block = Bell(grid_x, grid_y)
                                elif selected_block_type == "NOTE_BLOCK":
                                    new_block = NoteBlock(grid_x, grid_y)
                                elif selected_block_type == "RAIL":
                                    new_block = Rail(grid_x, grid_y)
                                elif selected_block_type == "POWERED_RAIL":
                                    new_block = PoweredRail(grid_x, grid_y)
                                elif selected_block_type == "DETECTOR_RAIL":
                                    new_block = DetectorRail(grid_x, grid_y)
                                elif selected_block_type == "MINECART":
                                    new_block = Minecart(grid_x, grid_y)
                                elif selected_block_type == "HOPPER_MINECART":
                                    new_block = HopperMinecart(grid_x, grid_y)
                                elif selected_block_type == "SCULK_SENSOR":
                                    new_block = SculkSensor(grid_x, grid_y)
                                elif selected_block_type == "BUILDING_BLOCK":
                                    new_block = BuildingBlock(grid_x, grid_y)
                                elif selected_block_type == "REDSTONE_BLOCK":
                                    new_block = RedstoneBlock(grid_x, grid_y)
                                elif selected_block_type == "PISTON":
                                    new_block = Piston(grid_x, grid_y, is_sticky=False)
                                elif selected_block_type == "STICKY_PISTON":
                                    new_block = Piston(grid_x, grid_y, is_sticky=True)
                                elif selected_block_type == "SLIME_BLOCK":
                                    new_block = SlimeBlock(grid_x, grid_y)
                                elif selected_block_type == "COMMAND_BLOCK":
                                    command_block_name = f"CB_{grid_x}_{grid_y}"
                                    new_block = CommandBlock(grid_x, grid_y, name=command_block_name)
                                    current_message = f"Placed Command Block. Name: {command_block_name}"
                                    message_display_time = pygame.time.get_ticks() + 2000
                                elif selected_block_type == "DISPENSER":
                                    new_block = Dispenser(grid_x, grid_y)
                                elif selected_block_type == "DROPPER":
                                    new_block = Dropper(grid_x, grid_y)
                                elif selected_block_type == "HOPPER":
                                    new_block = Hopper(grid_x, grid_y)
                                elif selected_block_type == "CHEST":
                                    new_block = Chest(grid_x, grid_y)
                                elif selected_block_type == "TRAPPED_CHEST":
                                    new_block = TrappedChest(grid_x, grid_y)
                                elif selected_block_type == "OBSERVER":
                                    new_block = Observer(grid_x, grid_y)
                                elif selected_block_type == "DAYLIGHT_DETECTOR":
                                    new_block = DaylightDetector(grid_x, grid_y)
                                elif selected_block_type == "LECTERN":
                                    new_block = Lectern(grid_x, grid_y)
                                
                                if new_block:
                                    grid[(grid_x, grid_y)] = new_block
                            else: # If block already exists, interact with it (left-click)
                                if (grid_x, grid_y) in grid:
                                    grid[(grid_x, grid_y)].on_click()
                    elif event.button == 3: # Right-click for rotation or interaction
                        if (grid_x, grid_y) in grid:
                            block_at_pos = grid[(grid_x, grid_y)]
                            # Blocks that rotate on right-click
                            if block_at_pos.type in ["REPEATER", "COMPARATOR", "PISTON", "STICKY_PISTON", "REDSTONE_TORCH", "DISPENSER", "DROPPER", "OBSERVER"]:
                                block_at_pos.orientation = (block_at_pos.orientation + 1) % 4
                                current_message = f"{block_at_pos.type} at ({grid_x},{grid_y}) rotated."
                                message_display_time = pygame.time.get_ticks() + 1500
                            # Blocks that have a secondary interaction on right-click (e.g., opening chest, changing page)
                            elif block_at_pos.type in ["DISPENSER", "DROPPER", "HOPPER", "CHEST", "TRAPPED_CHEST", "DAYLIGHT_DETECTOR", "LECTERN", "TARGET_BLOCK", "NOTE_BLOCK", "SCULK_SENSOR"]:
                                block_at_pos.on_click() 
                            else: # Default right-click behavior: erase
                                del grid[(grid_x, grid_y)]
                    elif event.button == 2: # Middle mouse button for dragging
                        is_dragging_grid = True
                        last_mouse_pos = event.pos

                else: # Clicked on toolbar or control buttons
                    # Check toolbar item clicks
                    for item in toolbar_items:
                        if "rect" in item and item["rect"].collidepoint(mouse_x, mouse_y):
                            selected_block_type = item["name"]
                            current_message = f"Selected: {item['text']}."
                            message_display_time = pygame.time.get_ticks() + 1500
                            break
                    
                    # Check control button clicks
                    if 'start_stop_button_rect' in globals() and start_stop_button_rect.collidepoint(mouse_x, mouse_y):
                        simulation_active = not simulation_active
                        current_message = f"Simulation {'started' if simulation_active else 'paused'}."
                        message_display_time = pygame.time.get_ticks() + 2000
                    elif 'clear_grid_button_rect' in globals() and clear_grid_button_rect.collidepoint(mouse_x, mouse_y):
                        grid.clear()
                        current_message = "Grid cleared."
                        message_display_time = pygame.time.get_ticks() + 1500
                    elif 'export_grid_button_rect' in globals() and export_grid_button_rect.collidepoint(mouse_x, mouse_y):
                        json_output = export_grid_to_json()
                        current_message = f"Grid Exported (JSON): Copy this text: {json_output[:100]}... (full JSON in console for debugging)"
                        print("--- EXPORTED GRID JSON ---")
                        print(json_output)
                        print("--------------------------")
                        message_display_time = pygame.time.get_ticks() + 5000
                    elif 'load_sample_grid_button_rect' in globals() and load_sample_grid_button_rect.collidepoint(mouse_x, mouse_y):
                        load_sample_grid()
                        # Message set within load_sample_grid
                    elif 'export_mcstructure_button_rect' in globals() and export_mcstructure_button_rect.collidepoint(mouse_x, mouse_y):
                        mcstructure_json_output = export_mcstructure_json()
                        current_message = f"Minecraft Structure Exported (JSON): Copy this text: {mcstructure_json_output[:100]}... (full JSON in console)"
                        print("--- EXPORTED MCSTRUCTURE JSON ---")
                        print(mcstructure_json_output)
                        print("---------------------------------")
                        message_display_time = pygame.time.get_ticks() + 5000

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    is_dragging_grid = False
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging_grid:
                    dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                    offset_x += dx
                    offset_y += dy
                    
                    # Clamp offsets to prevent scrolling too far
                    max_offset_x = (LOGICAL_GRID_WIDTH * BLOCK_SIZE) - (VISIBLE_GRID_WIDTH * BLOCK_SIZE)
                    max_offset_y = (LOGICAL_GRID_HEIGHT * BLOCK_SIZE) - (VISIBLE_GRID_HEIGHT * BLOCK_SIZE)
                    
                    offset_x = max(min(offset_x, 0), -(max_offset_x))
                    offset_y = max(min(offset_y, 0), -(max_offset_y))

                    last_mouse_pos = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                # Check if mouse is over the toolbar area
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if TOOLBAR_X_START <= mouse_x <= WIDTH:
                    toolbar_scroll_y += event.y * TOOLBAR_SCROLL_SPEED
                    # Clamping will happen in draw_toolbar

            elif event.type == simulation_tick_event and simulation_active:
                # Update order for Redstone logic accuracy (multi-pass system)
                
                # Phase 1: Minecarts (movement can trigger detector rails)
                for coord in list(grid.keys()):
                    block = grid[coord]
                    if block.type in ["MINECART", "HOPPER_MINECART"]:
                        block.update()

                # Phase 2: Inputs (levers, buttons, pressure plates, redstone blocks, trapped chests, detector rails, daylight detectors, lecterns, target blocks, bells, note blocks, lamps, sculk sensors)
                # These can change state independently or based on simple interactions
                for coord in list(grid.keys()):
                    block = grid[coord]
                    if block.type in ["LEVER", "BUTTON", "PRESSURE_PLATE", "REDSTONE_BLOCK", "TRAPPED_CHEST", "DETECTOR_RAIL", "DAYLIGHT_DETECTOR", "LECTERN", "TARGET_BLOCK", "BELL", "NOTE_BLOCK", "LAMP", "SCULK_SENSOR"]:
                        block.update()

                # Phase 3: Redstone components that propagate power (dust, command blocks, pistons, repeaters, comparators, dispensers, droppers, hoppers, observers, powered rails)
                # This phase needs multiple iterations to allow power to propagate through dust and repeaters
                for _ in range(16): # Multiple passes for signal propagation (Redstone dust takes time to propagate)
                    for coord in list(grid.keys()):
                        block = grid[coord]
                        if block.type in ["REDSTONE_DUST", "COMMAND_BLOCK", "PISTON", "STICKY_PISTON", "REPEATER", "COMPARATOR",
                                          "DISPENSER", "DROPPER", "HOPPER", "OBSERVER", "POWERED_RAIL"]:
                            block.update()
                    # Redstone torches are special: they invert power and can be part of oscillation, update them after other power changes
                    for coord in list(grid.keys()):
                        block = grid[coord]
                        if block.type == "REDSTONE_TORCH":
                            block.update()

                # Phase 4: Item entities (despawning)
                items_to_remove = []
                for coord in list(grid.keys()):
                    block = grid[coord]
                    if block.type == "ITEM_ENTITY":
                        if block.update(): # ItemEntity's update returns True if it should be removed
                            items_to_remove.append(coord)
                for coord in items_to_remove:
                    if coord in grid:
                        del grid[coord]

        # --- Drawing ---
        SCREEN.fill(DARK_GRAY) # Background color

        # Draw grid blocks
        for y in range(LOGICAL_GRID_HEIGHT):
            for x in range(LOGICAL_GRID_WIDTH):
                screen_x = x * BLOCK_SIZE + offset_x
                screen_y = y * BLOCK_SIZE + offset_y

                # Only draw blocks that are currently visible on screen
                if -BLOCK_SIZE < screen_x < VISIBLE_GRID_WIDTH * BLOCK_SIZE and \
                   -BLOCK_SIZE < screen_y < VISIBLE_GRID_HEIGHT * BLOCK_SIZE:
                    if (x, y) in grid:
                        grid[(x, y)].draw(SCREEN, offset_x, offset_y)
                    else:
                        # Draw empty grid cells
                        pygame.draw.rect(SCREEN, EMPTY_GRID_COLOR, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
                        pygame.draw.rect(SCREEN, DARK_GRAY, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=3)

        draw_toolbar(SCREEN)
        draw_controls(SCREEN)
        draw_info_panel(SCREEN)
        draw_scrollbars(SCREEN, offset_x, offset_y)

        pygame.display.flip() # Update the full display Surface to the screen
        clock.tick(60) # Limit frame rate to 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
