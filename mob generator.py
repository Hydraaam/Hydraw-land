import sys
import json
import os
import uuid
import shutil # Added for zipping and folder operations
import zipfile # Added for zipping

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox,
    QPushButton, QLabel, QFileDialog, QScrollArea, QGroupBox, QPlainTextEdit,
    QMessageBox
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class MobCreatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Custom Mob Addon Creator")
        self.setGeometry(100, 100, 1000, 800) # Main window dimensions

        self.setup_dark_theme()
        self.init_ui()

    def setup_dark_theme(self):
        # Set dark theme for the application
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        QApplication.setPalette(palette)

        # Set font for the entire application
        font = QFont("Inter", 10)
        QApplication.setFont(font)

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        # Create different tabs
        self.general_tab = QWidget()
        self.behavior_tab = QWidget()
        self.appearance_tab = QWidget()
        self.advanced_tab = QWidget()
        self.output_tab = QWidget()

        self.tab_widget.addTab(self.general_tab, "General")
        self.tab_widget.addTab(self.behavior_tab, "Behavior")
        self.tab_widget.addTab(self.appearance_tab, "Appearance")
        self.tab_widget.addTab(self.advanced_tab, "Advanced")
        self.tab_widget.addTab(self.output_tab, "Output")

        self.setup_general_tab()
        self.setup_behavior_tab()
        self.setup_appearance_tab()
        self.setup_advanced_tab()
        self.setup_output_tab()

        # Add a checkbox for .mcaddon generation
        self.generate_mcaddon_checkbox = QCheckBox("Generate .mcaddon file directly")
        self.generate_mcaddon_checkbox.setChecked(True) # Default to checked
        self.generate_mcaddon_checkbox.setToolTip("If checked, the tool will automatically zip the addon files into a .mcaddon format.")
        self.generate_mcaddon_checkbox.setStyleSheet("QCheckBox { color: white; margin-left: 5px; }")
        self.main_layout.addWidget(self.generate_mcaddon_checkbox)


        self.generate_button = QPushButton("Generate Addon Files")
        self.generate_button.clicked.connect(self.generate_addon_files)
        # Enhanced button styling
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 12px 25px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #45a049;
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #3e8e41;
                transform: translateY(0);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
        """)
        self.main_layout.addWidget(self.generate_button)

        # Set consistent margins for the main layout
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10) # Spacing between widgets

    def create_input_field(self, parent_layout, label_text, widget_type=QLineEdit, default_value="", min_val=0, max_val=100, step=1, tooltip_text=""):
        # Helper function to create input fields
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(180) # Fixed width for labels
        label.setToolTip(tooltip_text) # Add tooltip to label
        h_layout.addWidget(label)

        if widget_type == QLineEdit:
            widget = QLineEdit(str(default_value))
            widget.setPlaceholderText(label_text.replace(":", "").strip())
        elif widget_type == QSpinBox:
            widget = QSpinBox()
            widget.setRange(min_val, max_val)
            widget.setValue(default_value)
            widget.setSingleStep(step)
        elif widget_type == QDoubleSpinBox:
            widget = QDoubleSpinBox()
            widget.setRange(min_val, max_val)
            widget.setValue(default_value)
            widget.setSingleStep(step)
        elif widget_type == QCheckBox:
            widget = QCheckBox()
            widget.setChecked(default_value)
        elif widget_type == QPlainTextEdit:
            widget = QPlainTextEdit(str(default_value))
            widget.setMinimumHeight(80) # Taller for larger text fields
        else:
            widget = QLineEdit(str(default_value))

        widget.setContentsMargins(5, 5, 5, 5) # Internal padding
        widget.setStyleSheet("border-radius: 8px; padding: 5px; background-color: #444; color: #EEE; border: 1px solid #555;") # Style for rounded corners and dark theme
        widget.setToolTip(tooltip_text) # Add tooltip to widget

        h_layout.addWidget(widget)
        parent_layout.addLayout(h_layout)
        return widget

    def create_file_picker(self, parent_layout, label_text, file_type_filter="All Files (*)", tooltip_text=""):
        # Helper function to create a file picker
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(180)
        label.setToolTip(tooltip_text) # Add tooltip to label
        h_layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Select file path")
        line_edit.setReadOnly(True)
        line_edit.setToolTip(tooltip_text)
        line_edit.setStyleSheet("border-radius: 8px; padding: 5px; background-color: #444; color: #EEE; border: 1px solid #555;")
        h_layout.addWidget(line_edit)

        button = QPushButton("Browse")
        button.clicked.connect(lambda: self.open_file_dialog(line_edit, file_type_filter))
        # Enhanced button styling
        button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 8px;
                padding: 8px 15px;
                border: none;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #0056b3;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #004080;
                transform: translateY(0);
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
            }
        """)
        h_layout.addWidget(button)
        parent_layout.addLayout(h_layout)
        return line_edit

    def open_file_dialog(self, line_edit_widget, file_filter):
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if file_path:
            line_edit_widget.setText(file_path)

    def setup_general_tab(self):
        # Setup General Tab
        layout = QVBoxLayout(self.general_tab)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # General Mob Information
        general_group = QGroupBox("General Mob Information")
        general_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                   "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        general_layout = QVBoxLayout(general_group)

        self.mob_name_input = self.create_input_field(general_layout, "Mob Name (Display):", default_value="My Custom Mob",
                                                      tooltip_text="The name displayed in-game (e.g., in spawn eggs).")
        self.mob_identifier_input = self.create_input_field(general_layout, "Mob Identifier (e.g., my_addon:mob):", default_value="my_addon:my_custom_mob",
                                                            tooltip_text="A unique identifier for your mob (e.g., 'namespace:mob_name').")
        self.is_spawnable_checkbox = self.create_input_field(general_layout, "Is Spawnable:", widget_type=QCheckBox, default_value=True,
                                                             tooltip_text="If checked, the mob can naturally spawn in the world.")
        self.is_baby_checkbox = self.create_input_field(general_layout, "Is Baby:", widget_type=QCheckBox, default_value=False,
                                                        tooltip_text="If checked, the mob will be a baby version (smaller scale).")
        self.health_input = self.create_input_field(general_layout, "Health:", widget_type=QSpinBox, default_value=20, min_val=1, max_val=1000,
                                                    tooltip_text="The maximum health points of the mob.")
        self.burn_under_sun_checkbox = self.create_input_field(general_layout, "Burns Under Sun:", widget_type=QCheckBox, default_value=False,
                                                               tooltip_text="If checked, the mob will take damage and burn when exposed to sunlight.")
        self.water_damage_checkbox = self.create_input_field(general_layout, "Takes Water Damage:", widget_type=QCheckBox, default_value=False,
                                                             tooltip_text="If checked, the mob will take damage when in water (like Endermen).")

        general_layout.setContentsMargins(10, 20, 10, 10) # Inner padding for group box
        general_layout.setSpacing(8) # Spacing between fields
        scroll_layout.addWidget(general_group)
        scroll_layout.addStretch()

    def setup_behavior_tab(self):
        # Setup Behavior Tab
        layout = QVBoxLayout(self.behavior_tab)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # Spawn Rules
        spawn_group = QGroupBox("Spawn Rules")
        spawn_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                 "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        spawn_layout = QVBoxLayout(spawn_group)
        self.spawn_biomes_input = self.create_input_field(spawn_layout, "Biomes (comma separated):", default_value="plains,forest",
                                                          tooltip_text="List of biomes where the mob can spawn (e.g., 'plains,forest,desert').")
        self.spawn_min_count_input = self.create_input_field(spawn_layout, "Min Count:", widget_type=QSpinBox, default_value=1, min_val=0, max_val=64,
                                                             tooltip_text="Minimum number of mobs that can spawn in a group.")
        self.spawn_max_count_input = self.create_input_field(spawn_layout, "Max Count:", widget_type=QSpinBox, default_value=3, min_val=0, max_val=64,
                                                             tooltip_text="Maximum number of mobs that can spawn in a group.")
        self.spawn_weight_input = self.create_input_field(spawn_layout, "Spawn Weight:", widget_type=QSpinBox, default_value=10, min_val=1, max_val=1000,
                                                          tooltip_text="Higher weight means more frequent spawns relative to other mobs.")
        self.spawn_on_block_filter_input = self.create_input_field(spawn_layout, "Spawn on Blocks (comma separated):", default_value="minecraft:grass,minecraft:stone",
                                                                   tooltip_text="List of blocks the mob can spawn on (e.g., 'minecraft:grass,minecraft:stone').")
        spawn_layout.setContentsMargins(10, 20, 10, 10)
        spawn_layout.setSpacing(8)
        scroll_layout.addWidget(spawn_group)

        # Spawn Egg
        spawn_egg_group = QGroupBox("Spawn Egg")
        spawn_egg_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                     "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        spawn_egg_layout = QVBoxLayout(spawn_egg_group)
        self.spawn_egg_base_color_input = self.create_input_field(spawn_egg_layout, "Base Color (HEX):", default_value="#FF0000",
                                                                  tooltip_text="The primary color of the mob's spawn egg (HEX format, e.g., #FF0000).")
        self.spawn_egg_overlay_color_input = self.create_input_field(spawn_egg_layout, "Overlay Color (HEX):", default_value="#00FF00",
                                                                     tooltip_text="The secondary color of the mob's spawn egg (HEX format, e.g., #00FF00).")
        spawn_egg_layout.setContentsMargins(10, 20, 10, 10)
        spawn_egg_layout.setSpacing(8)
        scroll_layout.addWidget(spawn_egg_group)

        # Attack Behavior
        attack_group = QGroupBox("Attack Behavior")
        attack_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                  "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        attack_layout = QVBoxLayout(attack_group)
        self.attack_damage_input = self.create_input_field(attack_layout, "Attack Damage:", widget_type=QSpinBox, default_value=3, min_val=0, max_val=100,
                                                           tooltip_text="The amount of damage the mob deals in melee attacks.")
        self.break_door_checkbox = self.create_input_field(attack_layout, "Breaks Doors:", widget_type=QCheckBox, default_value=False,
                                                           tooltip_text="If checked, the mob can break wooden doors (like Zombies).")
        self.avoid_other_mob_checkbox = self.create_input_field(attack_layout, "Avoids Other Mobs:", widget_type=QCheckBox, default_value=False,
                                                                tooltip_text="If checked, the mob will try to avoid certain mob types (e.g., monsters).")
        attack_layout.setContentsMargins(10, 20, 10, 10)
        attack_layout.setSpacing(8)
        scroll_layout.addWidget(attack_group)

        # Breeding and Taming
        breed_tame_group = QGroupBox("Breeding and Taming")
        breed_tame_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                      "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        breed_tame_layout = QVBoxLayout(breed_tame_group)
        self.breedable_checkbox = self.create_input_field(breed_tame_layout, "Is Breedable:", widget_type=QCheckBox, default_value=False,
                                                          tooltip_text="If checked, the mob can be bred with specific items.")
        self.tameable_checkbox = self.create_input_field(breed_tame_layout, "Is Tameable:", widget_type=QCheckBox, default_value=False,
                                                         tooltip_text="If checked, the mob can be tamed with specific items.")
        self.tame_items_input = self.create_input_field(breed_tame_layout, "Tame Items (comma separated):", default_value="minecraft:bone",
                                                        tooltip_text="List of items that can be used to tame the mob (e.g., 'minecraft:bone,minecraft:fish').")
        self.follow_owner_checkbox = self.create_input_field(breed_tame_layout, "Follows Owner:", widget_type=QCheckBox, default_value=False,
                                                             tooltip_text="If checked, a tamed mob will follow its owner.")
        breed_tame_layout.setContentsMargins(10, 20, 10, 10)
        breed_tame_layout.setSpacing(8)
        scroll_layout.addWidget(breed_tame_group)

        scroll_layout.addStretch()

    def setup_appearance_tab(self):
        # Setup Appearance Tab
        layout = QVBoxLayout(self.appearance_tab)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # Model, Texture, and Animation
        assets_group = QGroupBox("Model, Texture, and Animation")
        assets_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                  "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        assets_layout = QVBoxLayout(assets_group)

        self.model_path_input = self.create_file_picker(assets_layout, "Model File (.geo.json):", "JSON Files (*.json *.geo.json)",
                                                        "Path to the mob's model file (e.g., my_mob.geo.json). This file should be placed in the models/entity/ folder in the Resource Pack.")
        self.texture_path_input = self.create_file_picker(assets_layout, "Texture File (.png):", "Image Files (*.png)",
                                                          "Path to the mob's texture file (e.g., my_mob.png). This file should be placed in the textures/entity/ folder in the Resource Pack.")
        self.animation_path_input = self.create_file_picker(assets_layout, "Animation File (.animation.json):", "JSON Files (*.json *.animation.json)",
                                                            "Path to the mob's animation file (e.g., my_mob.animation.json). This file should be placed in the animations/ folder in the Resource Pack.")
        self.animation_controller_path_input = self.create_file_picker(assets_layout, "Animation Controller File (.json):", "JSON Files (*.json)",
                                                                       "Path to the mob's animation controller file (e.g., my_mob.animation_controller.json). This file should be placed in the animation_controllers/ folder in the Resource Pack.")

        assets_layout.setContentsMargins(10, 20, 10, 10)
        assets_layout.setSpacing(8)
        scroll_layout.addWidget(assets_group)
        scroll_layout.addStretch()

    def setup_advanced_tab(self):
        # Setup Advanced Tab
        layout = QVBoxLayout(self.advanced_tab)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # Inventory
        inventory_group = QGroupBox("Inventory")
        inventory_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                     "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        inventory_layout = QVBoxLayout(inventory_group)
        self.has_inventory_checkbox = self.create_input_field(inventory_layout, "Has Inventory:", widget_type=QCheckBox, default_value=False,
                                                              tooltip_text="If checked, the mob will have an inventory.")
        self.inventory_size_input = self.create_input_field(inventory_layout, "Inventory Size:", widget_type=QSpinBox, default_value=0, min_val=0, max_val=54,
                                                            tooltip_text="The number of slots in the mob's inventory.")
        inventory_layout.setContentsMargins(10, 20, 10, 10)
        inventory_layout.setSpacing(8)
        scroll_layout.addWidget(inventory_group)

        # On Death Action
        on_death_group = QGroupBox("On Death Action")
        on_death_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                    "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        on_death_layout = QVBoxLayout(on_death_group)
        self.on_death_loot_table_input = self.create_input_field(on_death_layout, "Loot Table (e.g., loot_tables/entities/my_mob.json):", default_value="",
                                                                 tooltip_text="Path to the loot table file for drops when the mob dies.")
        self.on_death_action_commands_input = self.create_input_field(on_death_layout, "Commands (one per line):", widget_type=QPlainTextEdit, default_value="",
                                                                      tooltip_text="Commands to execute when the mob dies. Each command on a new line.")
        on_death_layout.setContentsMargins(10, 20, 10, 10)
        on_death_layout.setSpacing(8)
        scroll_layout.addWidget(on_death_group)

        # On Hit Action
        on_hit_group = QGroupBox("On Hit Action")
        on_hit_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                   "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        on_hit_layout = QVBoxLayout(on_hit_group)
        self.on_hit_damage_input = self.create_input_field(on_hit_layout, "Damage from Hit (if triggered by hit):", widget_type=QSpinBox, default_value=0, min_val=0, max_val=100,
                                                           tooltip_text="Amount of damage the mob takes when hit (if a custom trigger is set).")
        self.on_hit_action_commands_input = self.create_input_field(on_hit_layout, "Commands (one per line):", widget_type=QPlainTextEdit, default_value="",
                                                                     tooltip_text="Commands to execute when the mob is hit. Each command on a new line.")
        on_hit_layout.setContentsMargins(10, 20, 10, 10)
        on_hit_layout.setSpacing(8)
        scroll_layout.addWidget(on_hit_group)

        # Golem
        golem_group = QGroupBox("Golem")
        golem_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                 "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        golem_layout = QVBoxLayout(golem_group)
        self.is_golem_checkbox = self.create_input_field(golem_layout, "Is Golem (spawns with structure):", widget_type=QCheckBox, default_value=False,
                                                         tooltip_text="If checked, the mob can be spawned by building a specific structure (like Iron Golems).")
        self.golem_build_structure_input = self.create_input_field(golem_layout, "Build Structure (JSON):", widget_type=QPlainTextEdit, default_value="",
                                                                   tooltip_text="JSON definition of the structure required to build the golem.")
        golem_layout.setContentsMargins(10, 20, 10, 10)
        golem_layout.setSpacing(8)
        scroll_layout.addWidget(golem_group)

        # Trade
        trade_group = QGroupBox("Trade")
        trade_group.setStyleSheet("QGroupBox { border: 1px solid #666; border-radius: 5px; margin-top: 1ex; }"
                                 "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: white; font-weight: bold; }")
        trade_layout = QVBoxLayout(trade_group)
        self.is_tradeable_checkbox = self.create_input_field(trade_layout, "Is Tradeable:", widget_type=QCheckBox, default_value=False,
                                                            tooltip_text="If checked, the mob can trade with players.")
        self.trade_table_path_input = self.create_file_picker(trade_layout, "Trade Table File (.json):", "JSON Files (*.json)",
                                                              "Path to the mob's trade table file (e.g., my_mob_trade.json). This file should be placed in the trading/ folder in the Behavior Pack.")
        trade_layout.setContentsMargins(10, 20, 10, 10)
        trade_layout.setSpacing(8)
        scroll_layout.addWidget(trade_group)

        scroll_layout.addStretch()

    def setup_output_tab(self):
        # Setup Output Tab
        layout = QVBoxLayout(self.output_tab)
        self.output_log = QPlainTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setStyleSheet("background-color: #333; color: #EEE; border-radius: 8px; padding: 10px; font-family: 'Consolas', 'Monospace';")
        layout.addWidget(self.output_log)
        layout.setContentsMargins(10, 10, 10, 10) # Add some padding to the output tab itself

    def get_mob_data(self):
        # Collect all data from input fields
        data = {
            "general": {
                "name": self.mob_name_input.text(),
                "identifier": self.mob_identifier_input.text(),
                "is_spawnable": self.is_spawnable_checkbox.isChecked(),
                "is_baby": self.is_baby_checkbox.isChecked(),
                "health": self.health_input.value(),
                "burn_under_sun": self.burn_under_sun_checkbox.isChecked(),
                "water_damage": self.water_damage_checkbox.isChecked(),
            },
            "behavior": {
                "spawn_rules": {
                    "biomes": [b.strip() for b in self.spawn_biomes_input.text().split(',') if b.strip()],
                    "min_count": self.spawn_min_count_input.value(),
                    "max_count": self.spawn_max_count_input.value(),
                    "weight": self.spawn_weight_input.value(),
                    "spawn_on_block_filter": [b.strip() for b in self.spawn_on_block_filter_input.text().split(',') if b.strip()],
                },
                "spawn_egg": {
                    "base_color": self.spawn_egg_base_color_input.text(),
                    "overlay_color": self.spawn_egg_overlay_color_input.text(),
                },
                "attack": {
                    "damage": self.attack_damage_input.value(),
                    "break_door": self.break_door_checkbox.isChecked(),
                    "avoid_other_mob": self.avoid_other_mob_checkbox.isChecked(),
                },
                "breed_tame": {
                    "breedable": self.breedable_checkbox.isChecked(),
                    "tameable": self.tameable_checkbox.isChecked(),
                    "tame_items": [i.strip() for i in self.tame_items_input.text().split(',') if i.strip()],
                    "follow_owner": self.follow_owner_checkbox.isChecked(),
                }
            },
            "appearance": {
                "model_path": self.model_path_input.text(),
                "texture_path": self.texture_path_input.text(),
                "animation_path": self.animation_path_input.text(),
                "animation_controller_path": self.animation_controller_path_input.text(),
            },
            "advanced": {
                "inventory": {
                    "has_inventory": self.has_inventory_checkbox.isChecked(),
                    "size": self.inventory_size_input.value(),
                },
                "on_death": {
                    "loot_table": self.on_death_loot_table_input.text(),
                    "commands": [cmd.strip() for cmd in self.on_death_action_commands_input.toPlainText().split('\n') if cmd.strip()],
                },
                "on_hit": {
                    "damage": self.on_hit_damage_input.value(),
                    "commands": [cmd.strip() for cmd in self.on_hit_action_commands_input.toPlainText().split('\n') if cmd.strip()],
                },
                "golem": {
                    "is_golem": self.is_golem_checkbox.isChecked(),
                    "build_structure": self.golem_build_structure_input.toPlainText(),
                },
                "trade": {
                    "is_tradeable": self.is_tradeable_checkbox.isChecked(),
                    "trade_table_path": self.trade_table_path_input.text(),
                }
            }
        }
        return data

    def generate_addon_files(self):
        self.output_log.clear() # Clear previous output
        self.output_log.append("Starting addon file generation...")

        mob_data = self.get_mob_data()
        mob_identifier = mob_data["general"]["identifier"]
        mob_name = mob_data["general"]["name"]

        if not mob_identifier or not mob_name:
            self.output_log.append("<span style='color: red;'>Error: Mob Name and Mob Identifier cannot be empty.</span>")
            QMessageBox.warning(self, "Input Error", "Mob Name and Mob Identifier cannot be empty.")
            return

        # Generate unique UUIDs
        manifest_uuid_header = str(uuid.uuid4())
        manifest_uuid_bp_module = str(uuid.uuid4())
        manifest_uuid_rp_module = str(uuid.uuid4())

        output_dir = QFileDialog.getExistingDirectory(self, "Select Folder to Save Addon")
        if not output_dir:
            self.output_log.append("<span style='color: orange;'>Save operation cancelled by user.</span>")
            return

        # Create base addon folder name
        addon_folder_name = mob_identifier.split(':')[-1] + "_addon"
        base_path = os.path.join(output_dir, addon_folder_name)

        # Define paths for BP and RP
        bp_path = os.path.join(base_path, "BP")
        rp_path = os.path.join(base_path, "RP")

        # Define sub-paths
        bp_entities_path = os.path.join(bp_path, "entities")
        rp_entity_path = os.path.join(rp_path, "entity")
        rp_textures_entity_path = os.path.join(rp_path, "textures", "entity")
        rp_models_entity_path = os.path.join(rp_path, "models", "entity")
        rp_animations_path = os.path.join(rp_path, "animations")
        rp_animation_controllers_path = os.path.join(rp_path, "animation_controllers")
        bp_loot_tables_path = os.path.join(bp_path, "loot_tables", "entities") # For custom loot tables
        bp_trading_path = os.path.join(bp_path, "trading") # For custom trade tables

        try:
            # Create all necessary directories
            os.makedirs(bp_entities_path, exist_ok=True)
            os.makedirs(rp_entity_path, exist_ok=True)
            os.makedirs(rp_textures_entity_path, exist_ok=True)
            os.makedirs(rp_models_entity_path, exist_ok=True)
            os.makedirs(rp_animations_path, exist_ok=True)
            os.makedirs(rp_animation_controllers_path, exist_ok=True)
            os.makedirs(bp_loot_tables_path, exist_ok=True) # Ensure loot table path exists
            os.makedirs(bp_trading_path, exist_ok=True) # Ensure trading path exists

            self.output_log.append(f"Addon folder structure created at: <span style='color: lightblue;'>{base_path}</span>")

            # 1. Generate manifest.json
            manifest_content = {
                "format_version": 2,
                "header": {
                    "name": f"{mob_name} Addon",
                    "description": f"A custom mob add-on for {mob_name}.",
                    "uuid": manifest_uuid_header,
                    "version": [1, 0, 0],
                    "min_engine_version": [1, 20, 0]
                },
                "modules": [
                    {
                        "type": "data",
                        "uuid": manifest_uuid_bp_module,
                        "version": [1, 0, 0]
                    },
                    {
                        "type": "resources",
                        "uuid": manifest_uuid_rp_module,
                        "version": [1, 0, 0]
                    }
                ]
            }
            with open(os.path.join(base_path, "manifest.json"), "w", encoding="utf-8") as f:
                json.dump(manifest_content, f, indent=2, ensure_ascii=False)
            self.output_log.append("Manifest.json generated.")

            # 2. Generate Behavior Pack Entity JSON
            bp_entity_content = {
                "format_version": "1.20.0",
                "minecraft:entity": {
                    "description": {
                        "identifier": mob_identifier,
                        "is_spawnable": mob_data["general"]["is_spawnable"],
                        "is_summonable": True,
                        "is_experimental": False
                    },
                    "components": {
                        "minecraft:health": {
                            "value": mob_data["general"]["health"],
                            "max": mob_data["general"]["health"]
                        },
                        "minecraft:movement": {
                            "value": 0.2
                        },
                        "minecraft:navigation.walk": {
                            "can_path_over_water": True
                        },
                        "minecraft:lookat": {
                            "default_look_at_targets": ["minecraft:player"]
                        },
                        "minecraft:behavior.melee_attack": {
                            "priority": 2,
                            "speed_multiplier": 1.2
                        },
                        "minecraft:behavior.random_stroll": {
                            "priority": 3,
                            "speed_multiplier": 0.8
                        },
                        "minecraft:spawn_rules": {
                            "biomes": mob_data["behavior"]["spawn_rules"]["biomes"],
                            "min_count": mob_data["behavior"]["spawn_rules"]["min_count"],
                            "max_count": mob_data["behavior"]["spawn_rules"]["max_count"],
                            "spawn_on_block_filter": {
                                "test": "block_filter",
                                "value": mob_data["behavior"]["spawn_rules"]["spawn_on_block_filter"]
                            },
                            "spawn_limit": mob_data["behavior"]["spawn_rules"]["max_count"] * 5,
                            "weight": mob_data["behavior"]["spawn_rules"]["weight"]
                        },
                        "minecraft:spawn_egg": {
                            "base_color": mob_data["behavior"]["spawn_egg"]["base_color"],
                            "overlay_color": mob_data["behavior"]["spawn_egg"]["overlay_color"]
                        },
                        "minecraft:type_family": {
                            "family": [mob_identifier.split(':')[-1], "mob"]
                        },
                        "minecraft:attack": {
                            "damage": mob_data["behavior"]["attack"]["damage"]
                        },
                    }
                }
            }

            # Add conditional components
            if mob_data["general"]["burn_under_sun"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:burns_in_daylight"] = {}
            if mob_data["general"]["water_damage"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:damage_sensor"] = bp_entity_content["minecraft:entity"]["components"].get("minecraft:damage_sensor", {"triggers": []})
                bp_entity_content["minecraft:entity"]["components"]["minecraft:damage_sensor"]["triggers"].append(
                    {"cause": "drowning", "deals_damage": True, "damage": 2}
                )
            if mob_data["behavior"]["attack"]["break_door"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:break_door"] = {
                    "break_time": 3.0
                }
            if mob_data["behavior"]["attack"]["avoid_other_mob"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:behavior.avoid_mob_type"] = {
                    "priority": 1,
                    "entity_types": [{"filters": {"any_of": [{"test": "is_family", "subject": "other", "value": "monster"}]}}]
                }
            if mob_data["behavior"]["breed_tame"]["breedable"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:breedable"] = {
                    "love_timer": 600,
                    "breeds_with": [{"item": "minecraft:wheat"}]
                }
            if mob_data["behavior"]["breed_tame"]["tameable"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:tameable"] = {
                    "tame_items": mob_data["behavior"]["breed_tame"]["tame_items"],
                    "tame_chance": 0.3
                }
            if mob_data["behavior"]["breed_tame"]["follow_owner"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:follow_owner"] = {
                    "speed_multiplier": 1.0,
                    "stop_distance": 2.0
                }
            if mob_data["advanced"]["inventory"]["has_inventory"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:inventory"] = {
                    "container_type": "entity",
                    "inventory_size": mob_data["advanced"]["inventory"]["size"],
                    "private": True,
                    "restrict_to_owner": True
                }
            if mob_data["advanced"]["on_death"]["loot_table"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:loot"] = mob_data["advanced"]["on_death"]["loot_table"]
            if mob_data["advanced"]["on_death"]["commands"]:
                bp_entity_content["minecraft:entity"]["events"] = bp_entity_content["minecraft:entity"].get("events", {})
                bp_entity_content["minecraft:entity"]["events"]["minecraft:on_death"] = {
                    "run_command": {
                        "command": mob_data["advanced"]["on_death"]["commands"]
                    }
                }
            if mob_data["advanced"]["on_hit"]["damage"] > 0 or mob_data["advanced"]["on_hit"]["commands"]:
                if "minecraft:damage_sensor" not in bp_entity_content["minecraft:entity"]["components"]:
                    bp_entity_content["minecraft:entity"]["components"]["minecraft:damage_sensor"] = {"triggers": []}

                if mob_data["advanced"]["on_hit"]["damage"] > 0:
                    bp_entity_content["minecraft:entity"]["components"]["minecraft:damage_sensor"]["triggers"].append(
                        {"cause": "all", "deals_damage": True, "damage": mob_data["advanced"]["on_hit"]["damage"]}
                    )

                if mob_data["advanced"]["on_hit"]["commands"]:
                    on_hit_event_name = "my_addon:on_hit"
                    bp_entity_content["minecraft:entity"]["events"] = bp_entity_content["minecraft:entity"].get("events", {})
                    bp_entity_content["minecraft:entity"]["events"][on_hit_event_name] = {
                        "run_command": {
                            "command": mob_data["advanced"]["on_hit"]["commands"]
                        }
                    }
                    bp_entity_content["minecraft:entity"]["components"]["minecraft:damage_sensor"]["triggers"].append(
                        {"cause": "all", "on_damage": on_hit_event_name}
                    )

            if mob_data["advanced"]["golem"]["is_golem"]:
                bp_entity_content["minecraft:entity"]["components"]["minecraft:golem"] = {}
                if mob_data["advanced"]["golem"]["build_structure"]:
                    try:
                        golem_structure = json.loads(mob_data["advanced"]["golem"]["build_structure"])
                        bp_entity_content["minecraft:entity"]["components"]["minecraft:golem"]["build_structure"] = golem_structure
                    except json.JSONDecodeError:
                        self.output_log.append("<span style='color: red;'>Error: Invalid Golem build structure JSON. Please check the format.</span>")
            if mob_data["advanced"]["trade"]["is_tradeable"]:
                if mob_data["advanced"]["trade"]["trade_table_path"]:
                    bp_entity_content["minecraft:entity"]["components"]["minecraft:trade_table"] = os.path.basename(mob_data["advanced"]["trade"]["trade_table_path"])
                else:
                    self.output_log.append("<span style='color: orange;'>Warning: Mob is tradeable but trade table path is not specified.</span>")

            if mob_data["general"]["is_baby"]:
                bp_entity_content["minecraft:entity"]["component_groups"] = {
                    "my_addon:baby": {
                        "minecraft:scale": {"value": 0.5}
                    }
                }
                bp_entity_content["minecraft:entity"]["events"] = bp_entity_content["minecraft:entity"].get("events", {})
                bp_entity_content["minecraft:entity"]["events"]["minecraft:entity_spawned"] = {
                    "add": {"component_groups": ["my_addon:baby"]}
                }

            with open(os.path.join(bp_entities_path, f"{addon_name}.json"), "w", encoding="utf-8") as f:
                json.dump(bp_entity_content, f, indent=2, ensure_ascii=False)
            self.output_log.append(f"Behavior Pack entity file (<span style='color: lightblue;'>{addon_name}.json</span>) generated.")

            # 3. Generate Resource Pack Client Entity JSON
            rp_entity_content = {
                "format_version": "1.10.0",
                "minecraft:client_entity": {
                    "description": {
                        "identifier": mob_identifier,
                        "materials": {
                            "default": "entity_alphatest"
                        },
                        "textures": {
                            "default": f"textures/entity/{os.path.splitext(os.path.basename(mob_data['appearance']['texture_path']))[0]}"
                        },
                        "geometry": {
                            "default": f"geometry.{os.path.splitext(os.path.basename(mob_data['appearance']['model_path']))[0].replace('.', '_')}"
                        },
                        "animations": {
                            "idle": f"animation.{os.path.splitext(os.path.basename(mob_data['appearance']['animation_path']))[0].replace('.', '_')}.idle"
                        },
                        "animation_controllers": [
                            { "general": f"controller.animation.{os.path.splitext(os.path.basename(mob_data['appearance']['animation_controller_path']))[0].replace('.', '_')}.general" }
                        ],
                        "render_controllers": ["controller.render.default"],
                        "spawn_egg": {
                            "texture": "spawn_egg",
                            "texture_index": 0
                        }
                    }
                }
            }
            with open(os.path.join(rp_entity_path, f"{addon_name}.json"), "w", encoding="utf-8") as f:
                json.dump(rp_entity_content, f, indent=2, ensure_ascii=False)
            self.output_log.append(f"Resource Pack client entity file (<span style='color: lightblue;'>{addon_name}.json</span>) generated.")

            # Handle .mcaddon generation
            if self.generate_mcaddon_checkbox.isChecked():
                self.output_log.append("\nAttempting to generate .mcaddon file...")
                temp_zip_dir = os.path.join(output_dir, f"{addon_folder_name}_temp_zip")
                
                # Copy BP, RP, and manifest to a temporary directory for zipping
                try:
                    if os.path.exists(temp_zip_dir):
                        shutil.rmtree(temp_zip_dir) # Clean up previous temp dir if it exists
                    shutil.copytree(base_path, temp_zip_dir)
                    self.output_log.append("Copied addon contents to temporary directory for zipping.")
                except Exception as e:
                    self.output_log.append(f"<span style='color: red;'>Error copying files for zipping: {e}</span>")
                    QMessageBox.critical(self, "Error", f"Failed to copy files for zipping: {e}")
                    return

                try:
                    mcaddon_file_path = os.path.join(output_dir, addon_folder_name)
                    shutil.make_archive(mcaddon_file_path, 'zip', temp_zip_dir)
                    os.rename(f"{mcaddon_file_path}.zip", f"{mcaddon_file_path}.mcaddon")
                    self.output_log.append(f"<span style='color: green;'>Successfully generated .mcaddon file: {mcaddon_file_path}.mcaddon</span>")
                except Exception as e:
                    self.output_log.append(f"<span style='color: red;'>Error generating .mcaddon file: {e}</span>")
                    QMessageBox.critical(self, "Error", f"Failed to generate .mcaddon file: {e}")
                finally:
                    # Clean up the temporary directory
                    if os.path.exists(temp_zip_dir):
                        shutil.rmtree(temp_zip_dir)
                        self.output_log.append("Cleaned up temporary zipping directory.")
            else:
                self.output_log.append("\n.mcaddon generation skipped as per user choice.")


            self.output_log.append("\n<span style='color: #4CAF50; font-weight: bold;'>Addon files generated successfully!</span>")
            self.output_log.append("To use the addon in Minecraft:")
            self.output_log.append("1. Manually place your model, texture, and animation files into the following paths within the RP folder:")
            self.output_log.append(f"   - Texture: <span style='color: lightblue;'>{os.path.join(rp_textures_entity_path, os.path.basename(mob_data['appearance']['texture_path']))}</span>")
            self.output_log.append(f"   - Model: <span style='color: lightblue;'>{os.path.join(rp_models_entity_path, os.path.basename(mob_data['appearance']['model_path']))}</span>")
            self.output_log.append(f"   - Animation: <span style='color: lightblue;'>{os.path.join(rp_animations_path, os.path.basename(mob_data['appearance']['animation_path']))}</span>")
            self.output_log.append(f"   - Animation Controller: <span style='color: lightblue;'>{os.path.join(rp_animation_controllers_path, os.path.basename(mob_data['appearance']['animation_controller_path']))}</span>")
            if not self.generate_mcaddon_checkbox.isChecked():
                self.output_log.append("2. Compress the main addon folder (named '<span style='color: lightblue;'>{}</span>') into a .zip file.".format(addon_folder_name))
                self.output_log.append("3. Change the .zip file extension to .mcaddon.")
            self.output_log.append("4. Open the .mcaddon file to import it into Minecraft.")

            QMessageBox.information(self, "Generation Successful", "Addon files generated successfully!\nPlease follow the instructions in the 'Output' tab to finalize your addon.")

        except Exception as e:
            self.output_log.append(f"<span style='color: red;'>An unexpected error occurred during file generation: {e}</span>")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MobCreatorApp()
    window.show()
    sys.exit(app.exec_())
