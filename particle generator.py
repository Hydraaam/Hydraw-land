import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import math 

# --- Bilingual strings dictionary ---
TEXTS = {
    "app_title": {
        "en": "Minecraft Particle Studio - by hydraw",
        "fa": "استودیوی پارتیکل ماینکرافت - ساخته شده توسط hydraw"
    },
    "basic_settings_frame_title": {
        "en": "Basic Particle Settings",
        "fa": "تنظیمات پایه پارتیکل"
    },
    "particle_type_label": {
        "en": "Particle Type:",
        "fa": "نوع پارتیکل:"
    },
    "particle_type_tooltip": {
        "en": "Select the type of particle you want to generate.",
        "fa": "نوع پارتیکلی که می‌خواهید تولید کنید را انتخاب کنید."
    },
    "target_selector_label": {
        "en": "Target Selector:",
        "fa": "انتخاب‌کننده هدف:"
    },
    "target_selector_example": {
        "en": "(e.g., @p, @a, @e[type=cow])",
        "fa": "(مثال: @p, @a, @e[type=cow])"
    },
    "target_selector_tooltip": {
        "en": "Specify a target (player/entity) for the particles. Leave empty for fixed coordinates. If a target is used, position coordinates will be ignored.",
        "fa": "هدف (بازیکن/موجودیت) برای پارتیکل‌ها را مشخص کنید. برای مختصات ثابت، خالی بگذارید. اگر از انتخاب‌کننده هدف استفاده شود، مختصات موقعیت نادیده گرفته می‌شوند."
    },
    "position_label": {
        "en": "Position (X Y Z):",
        "fa": "موقعیت (X Y Z):"
    },
    "position_example": {
        "en": "(e.g., ~ ~ ~ or 100 60 -20)",
        "fa": "(مثال: ~ ~ ~ یا 100 60 -20)"
    },
    "pos_x_tooltip": {"en": "X coordinate for particle origin. Use '~' for relative position.", "fa": "مختصات X برای مبدأ پارتیکل. از '~' برای موقعیت نسبی استفاده کنید."},
    "pos_y_tooltip": {"en": "Y coordinate for particle origin. Use '~' for relative position.", "fa": "مختصات Y برای مبدأ پارتیکل. از '~' برای موقعیت نسبی استفاده کنید."},
    "pos_z_tooltip": {"en": "Z coordinate for particle origin. Use '~' for relative position.", "fa": "مختصات Z برای مبدأ پارتیکل. از '~' برای موقعیت نسبی استفاده کنید."},
    "show_advanced_settings_button": {
        "en": "Show Advanced Settings",
        "fa": "نمایش تنظیمات پیشرفته"
    },
    "movement_spawn_settings_frame_title": {
        "en": "Movement & Spawn Settings",
        "fa": "تنظیمات حرکت و اسپاون"
    },
    "delta_label": {
        "en": "Delta (dX dY dZ):",
        "fa": "دلتا (dX dY dZ):"
    },
    "delta_description": {
        "en": "(Particle spread on each axis)",
        "fa": "(پراکندگی پارتیکل در هر محور)"
    },
    "delta_x_tooltip": {"en": "Max spread distance on the X-axis from the origin (e.g., 0.5 for small spread).", "fa": "حداکثر فاصله پراکندگی در محور X از مبدأ (مثلاً 0.5 برای پراکندگی کم)."},
    "delta_y_tooltip": {"en": "Max spread distance on the Y-axis from the origin.", "fa": "حداکثر فاصله پراکندگی در محور Y از مبدأ."},
    "delta_z_tooltip": {"en": "Max spread distance on the Z-axis from the origin.", "fa": "حداکثر فاصله پراکندگی در محور Z از مبدأ."},
    "speed_label": {
        "en": "Speed:",
        "fa": "سرعت:"
    },
    "speed_description": {
        "en": "(Value 0 to 10.0+)",
        "fa": "(مقدار 0 تا 10.0+)"
    },
    "speed_tooltip": {
        "en": "The speed at which particles move. 0 means they stay in place. Higher values make them move faster.",
        "fa": "سرعتی که پارتیکل‌ها با آن حرکت می‌کنند. 0 به معنای ثابت ماندن آن‌هاست. مقادیر بالاتر باعث حرکت سریع‌تر آن‌ها می‌شود."
    },
    "count_label": {
        "en": "Count:",
        "fa": "تعداد:"
    },
    "count_description": {
        "en": "(Number of particles spawned)",
        "fa": "(تعداد پارتیکل‌های اسپاون شده)"
    },
    "count_tooltip": {
        "en": "The number of particles to spawn per command execution. Higher count can cause lag.",
        "fa": "تعداد پارتیکل‌هایی که در هر بار اجرای دستور اسپاون می‌شوند. تعداد بالا می‌تواند باعث لگ شود."
    },
    "display_mode_label": {
        "en": "Display Mode:",
        "fa": "حالت نمایش:"
    },
    "mode_normal": {
        "en": "Normal",
        "fa": "عادی"
    },
    "mode_normal_tooltip": {
        "en": "Particles are visible only within a certain distance from the player.",
        "fa": "پارتیکل‌ها فقط در فاصله مشخصی از بازیکن قابل مشاهده هستند."
    },
    "mode_force": {
        "en": "Force (Always visible)",
        "fa": "اجباری (همیشه قابل مشاهده)"
    },
    "mode_force_tooltip": {
        "en": "Particles are always visible, even from far away, potentially causing more lag.",
        "fa": "پارتیکل‌ها همیشه قابل مشاهده هستند، حتی از راه دور، که به طور بالقوه می‌تواند باعث لگ بیشتر شود."
    },
    "initial_velocity_label": {
        "en": "Initial Velocity (X Y Z):",
        "fa": "سرعت اولیه (X Y Z):"
    },
    "motion_x_tooltip": {"en": "Initial velocity of particles on the X-axis.", "fa": "سرعت اولیه پارتیکل‌ها در محور X."},
    "motion_y_tooltip": {"en": "Initial velocity of particles on the Y-axis.", "fa": "سرعت اولیه پارتیکل‌ها در محور Y."},
    "motion_z_tooltip": {"en": "Initial velocity of particles on the Z-axis.", "fa": "سرعت اولیه پارتیکل‌ها در محور Z."},
    "gravity_modifier_label": {
        "en": "Gravity Modifier:",
        "fa": "ضریب جاذبه:"
    },
    "gravity_tooltip": {
        "en": "How much particles are affected by gravity. Positive for falling, negative for rising. (e.g., 0.1, -0.05)",
        "fa": "میزان تأثیر پارتیکل‌ها از جاذبه. مثبت برای سقوط، منفی برای بالا رفتن. (مثال: 0.1, -0.05)"
    },
    "enable_collisions_checkbox": {
        "en": "Enable Collisions with Blocks",
        "fa": "فعال کردن برخورد با بلاک‌ها"
    },
    "collisions_tooltip": {
        "en": "If checked, particles will collide and bounce off blocks. May affect performance.",
        "fa": "اگر انتخاب شود، پارتیکل‌ها با بلاک‌ها برخورد کرده و از آن‌ها بازمی‌گردند. ممکن است بر عملکرد تأثیر بگذارد."
    },
    "max_lifetime_label": {
        "en": "Max Lifetime (seconds):",
        "fa": "حداکثر طول عمر (ثانیه):"
    },
    "max_lifetime_tooltip": {
        "en": "The maximum duration (in seconds) before the particle despawns. Use 0 for infinite (or particle's default).",
        "fa": "حداکثر مدت زمان (به ثانیه) قبل از ناپدید شدن پارتیکل. از 0 برای بی‌نهایت (یا پیش‌فرض پارتیکل) استفاده کنید."
    },
    "spawn_rate_label": {
        "en": "Spawn Rate (per tick):",
        "fa": "نرخ اسپاون (در هر تیک):"
    },
    "spawn_rate_tooltip": {
        "en": "The number of particles spawned per tick. Used for Bedrock Addon export (not directly /particle command).",
        "fa": "تعداد پارتیکل‌های اسپاون شده در هر تیک. برای خروجی Bedrock Addon استفاده می‌شود (نه مستقیماً دستور /particle)."
    },
    "max_particles_label": {
        "en": "Max Particles (total):",
        "fa": "حداکثر پارتیکل (کل):"
    },
    "max_particles_tooltip": {
        "en": "The maximum number of particles that can exist from this emitter. Used for Bedrock Addon export (not directly /particle command).",
        "fa": "حداکثر تعداد پارتیکل‌هایی که می‌توانند از این امیتر وجود داشته باشند. برای خروجی Bedrock Addon استفاده می‌شود (نه مستقیماً دستور /particle)."
    },
    "particle_specific_data_frame_title": {
        "en": "Particle Type Specific Data",
        "fa": "داده‌های خاص نوع پارتیکل"
    },
    "redstone_color_start_label": {"en": "Redstone Color (Start):", "fa": "رنگ ردستون (شروع):"},
    "redstone_color_end_label": {"en": "Redstone Color (End):", "fa": "رنگ ردستون (پایان):"},
    "red_tooltip": {"en": "Red color component (0.0 for no red, 1.0 for full red).", "fa": "جزء رنگ قرمز (0.0 برای بدون قرمز، 1.0 برای قرمز کامل)."},
    "green_tooltip": {"en": "Green color component (0.0 to 1.0).", "fa": "جزء رنگ سبز (0.0 تا 1.0)."},
    "blue_tooltip": {"en": "Blue color component (0.0 to 1.0).", "fa": "جزء رنگ آبی (0.0 تا 1.0)."},
    "size_tooltip": {"en": "Size of the dust particle (0.0 for smallest, 4.0 for largest).", "fa": "اندازه پارتیکل گرد و غبار (0.0 برای کوچکترین، 4.0 برای بزرگترین)."},
    "block_item_id_label": {"en": "Block/Item ID:", "fa": "شناسه بلاک/آیتم:"},
    "block_item_id_tooltip": {"en": "Enter the Minecraft ID for the block or item (e.g., minecraft:stone, minecraft:diamond).", "fa": "شناسه ماینکرافت برای بلاک یا آیتم را وارد کنید (مثلاً minecraft:stone, minecraft:diamond)."},
    "from_red_tooltip": {"en": "Starting Red color component (0.0 to 1.0).", "fa": "جزء رنگ قرمز شروع (0.0 تا 1.0)."},
    "from_green_tooltip": {"en": "Starting Green color component (0.0 to 1.0).", "fa": "جزء رنگ سبز شروع (0.0 تا 1.0)."},
    "from_blue_tooltip": {"en": "Starting Blue color component (0.0 to 1.0).", "fa": "جزء رنگ آبی شروع (0.0 تا 1.0)."},
    "to_red_tooltip": {"en": "Ending Red color component (0.0 to 1.0).", "fa": "جزء رنگ قرمز پایان (0.0 تا 1.0)."},
    "to_green_tooltip": {"en": "Ending Green color component (0.0 to 1.0).", "fa": "جزء رنگ سبز پایان (0.0 تا 1.0)."},
    "to_blue_tooltip": {"en": "Ending Blue color component (0.0 to 1.0).", "fa": "جزء رنگ آبی پایان (0.0 تا 1.0)."},
    "size_transition_tooltip": {"en": "Size of the transitioning dust particle (0.0 to 4.0).", "fa": "اندازه پارتیکل گرد و غبار در حال انتقال (0.0 تا 4.0)."},
    "dest_x_label": {"en": "Dest. X:", "fa": "مقصد X:"},
    "dest_y_label": {"en": "Dest. Y:", "fa": "مقصد Y:"},
    "dest_z_label": {"en": "Dest. Z:", "fa": "مقصد Z:"},
    "arrival_ticks_label": {"en": "Arrival Ticks:", "fa": "تیک‌های رسیدن:"},
    "vibration_x_tooltip": {"en": "X coordinate of the vibration's destination.", "fa": "مختصات X مقصد ارتعاش."},
    "vibration_y_tooltip": {"en": "Y coordinate of the vibration's destination.", "fa": "مختصات Y مقصد ارتعاش."},
    "vibration_z_tooltip": {"en": "Z coordinate of the vibration's destination.", "fa": "مختصات Z مقصد ارتعاش."},
    "arrival_ticks_tooltip": {"en": "Time in ticks for the vibration to reach its destination (20 ticks = 1 second).", "fa": "زمان بر حسب تیک برای رسیدن ارتعاش به مقصد (20 تیک = 1 ثانیه)."},
    "roll_label": {"en": "Roll (0 to 2π):", "fa": "چرخش (0 تا 2π):"},
    "roll_tooltip": {"en": "The rotation of the sculk charge particle in radians.", "fa": "چرخش پارتیکل شارژ اسکالک بر حسب رادیان."},
    "delay_label": {"en": "Delay (ticks):", "fa": "تأخیر (تیک):"},
    "delay_tooltip": {"en": "The delay in ticks before the shriek particle appears (20 ticks = 1 second).", "fa": "تأخیر بر حسب تیک قبل از ظاهر شدن پارتیکل شریک (20 تیک = 1 ثانیه)."},
    "block_state_label": {"en": "Block State:", "fa": "حالت بلاک:"},
    "block_state_tooltip": {"en": "Enter the block ID and optional block states (e.g., minecraft:sand[falling=true]).", "fa": "شناسه بلاک و حالت‌های اختیاری بلاک را وارد کنید (مثلاً minecraft:sand[falling=true])."},
    "generic_extra_params_label": {
        "en": "Generic Extra Parameters:",
        "fa": "پارامترهای اضافی عمومی:"
    },
    "generic_extra_params_help": {
        "en": """For particles not covered by specific fields,
enter raw parameters here (e.g., NBT data).""",
        "fa": """برای پارتیکل‌هایی که توسط فیلدهای خاص پوشش داده نشده‌اند،
پارامترهای خام را اینجا وارد کنید (مثلاً داده‌های NBT)."""
    },
    "generic_extra_params_tooltip": {
        "en": "For particles not covered by specific fields, enter raw parameters here. This can include NBT data.",
        "fa": "برای پارتیکل‌هایی که توسط فیلدهای خاص پوشش داده نشده‌اند، پارامترهای خام را اینجا وارد کنید. این می‌تواند شامل داده‌های NBT باشد."
    },
    "advanced_rendering_frame_title": {
        "en": "Advanced Rendering & Behavior",
        "fa": "رندرینگ و رفتار پیشرفته"
    },
    "custom_texture_path_label": {
        "en": "Custom Texture Path:",
        "fa": "مسیر تکسچر سفارشی:"
    },
    "custom_texture_path_tooltip": {
        "en": "Path to a custom texture (e.g., textures/custom/my_particle.png). Used in Bedrock Addon export.",
        "fa": "مسیر به یک تکسچر سفارشی (مثلاً textures/custom/my_particle.png). در خروجی Bedrock Addon استفاده می‌شود."
    },
    "uv_coordinates_label": {
        "en": "UV Coordinates (U V W H):",
        "fa": "مختصات UV (U V W H):"
    },
    "uv_u_tooltip": {"en": "U coordinate (pixel X) for the top-left of the texture region.", "fa": "مختصات U (پیکسل X) برای بالا-چپ ناحیه تکسچر."},
    "uv_v_tooltip": {"en": "V coordinate (pixel Y) for the top-left of the texture region.", "fa": "مختصات V (پیکسل Y) برای بالا-چپ ناحیه تکسچر."},
    "uv_w_tooltip": {"en": "Width (in pixels) of the texture region.", "fa": "عرض (بر حسب پیکسل) ناحیه تکسچر."},
    "uv_h_tooltip": {"en": "Height (in pixels) of the texture region.", "fa": "ارتفاع (بر حسب پیکسل) ناحیه تکسچر."},
    "initial_roll_label": {
        "en": "Initial Roll (radians):",
        "fa": "چرخش اولیه (رادیان):"
    },
    "initial_roll_tooltip": {
        "en": "Initial Z-axis rotation of the particle in radians.",
        "fa": "چرخش اولیه پارتیکل در محور Z بر حسب رادیان."
    },
    "angular_velocity_label": {
        "en": "Angular Velocity:",
        "fa": "سرعت زاویه‌ای:"
    },
    "angular_velocity_tooltip": {
        "en": "Speed of rotation (radians per tick). Positive for clockwise, negative for counter-clockwise. Used in Bedrock Addon export.",
        "fa": "سرعت چرخش (رادیان در هر تیک). مثبت برای جهت عقربه‌های ساعت، منفی برای خلاف جهت عقربه‌های ساعت. در خروجی Bedrock Addon استفاده می‌شود."
    },
    "affected_by_lighting_checkbox": {
        "en": "Affected by Lighting",
        "fa": "تحت تأثیر نورپردازی"
    },
    "lighting_tooltip": {
        "en": "If checked, the particle's appearance will be influenced by the world's lighting conditions. Used in Bedrock Addon export.",
        "fa": "اگر انتخاب شود، ظاهر پارتیکل تحت تأثیر شرایط نورپردازی جهان قرار خواهد گرفت. در خروجی Bedrock Addon استفاده می‌شود."
    },
    "linear_drag_label": {"en": "Linear Drag Coefficient:", "fa": "ضریب کشش خطی:"},
    "linear_drag_tooltip": {"en": "How much particles slow down due to air resistance (0.0 for no drag, 1.0 for full drag). Used in Bedrock Addon export.", "fa": "میزان کاهش سرعت پارتیکل‌ها به دلیل مقاومت هوا (0.0 برای بدون کشش، 1.0 برای کشش کامل). در خروجی Bedrock Addon استفاده می‌شود."},
    "collision_resilience_label": {"en": "Collision Resilience:", "fa": "انعطاف‌پذیری برخورد:"},
    "collision_resilience_tooltip": {"en": "How much particles bounce off surfaces after collision (0.0 for no bounce, 1.0 for full bounce). Used in Bedrock Addon export.", "fa": "میزان بازگشت پارتیکل‌ها از سطوح پس از برخورد (0.0 برای بدون بازگشت، 1.0 برای بازگشت کامل). در خروجی Bedrock Addon استفاده می‌شود."},
    "collision_radius_label": {"en": "Collision Radius:", "fa": "شعاع برخورد:"},
    "collision_radius_tooltip": {"en": "The radius of the particle for collision detection. Used in Bedrock Addon export.", "fa": "شعاع پارتیکل برای تشخیص برخورد. در خروجی Bedrock Addon استفاده می‌شود."},
    "spawn_offset_label": {"en": "Spawn Offset (X Y Z):", "fa": "افست اسپاون (X Y Z):"},
    "spawn_offset_tooltip": {"en": "A fixed offset from the emitter's origin for particle spawning. Used in Bedrock Addon export.", "fa": "یک افست ثابت از مبدأ امیتر برای اسپاون پارتیکل. در خروجی Bedrock Addon استفاده می‌شود."},
    "size_over_lifetime_label": {"en": "Size Over Lifetime:", "fa": "اندازه در طول عمر:"},
    "size_over_lifetime_tooltip": {"en": "Defines how the particle's size changes from start to end of its lifetime. Used in Bedrock Addon export.", "fa": "نحوه تغییر اندازه پارتیکل از شروع تا پایان طول عمر آن را تعریف می‌کند. در خروجی Bedrock Addon استفاده می‌شود."},
    "start_size_label": {"en": "Start Size:", "fa": "اندازه شروع:"},
    "end_size_label": {"en": "End Size:", "fa": "اندازه پایان:"},
    "start_size_tooltip": {"en": "Initial size of the particle (relative to base size).", "fa": "اندازه اولیه پارتیکل (نسبت به اندازه پایه)."},
    "end_size_tooltip": {"en": "Final size of the particle (relative to base size).", "fa": "اندازه نهایی پارتیکل (نسبت به اندازه پایه)."},
    "alpha_over_lifetime_label": {"en": "Alpha Over Lifetime:", "fa": "آلفا در طول عمر:"},
    "alpha_over_lifetime_tooltip": {"en": "Defines how the particle's transparency changes from start to end of its lifetime. Used in Bedrock Addon export.", "fa": "نحوه تغییر شفافیت پارتیکل از شروع تا پایان طول عمر آن را تعریف می‌کند. در خروجی Bedrock Addon استفاده می‌شود."},
    "start_alpha_label": {"en": "Start Alpha (0-1):", "fa": "آلفای شروع (0-1):"},
    "end_alpha_label": {"en": "End Alpha (0-1):", "fa": "آلفای پایان (0-1):"},
    "start_alpha_tooltip": {"en": "Initial transparency of the particle (0.0 for fully transparent, 1.0 for fully opaque).", "fa": "شفافیت اولیه پارتیکل (0.0 برای کاملاً شفاف، 1.0 برای کاملاً مات)."},
    "end_alpha_tooltip": {"en": "Final transparency of the particle (0.0 for fully transparent, 1.0 for fully opaque).", "fa": "شفافیت نهایی پارتیکل (0.0 برای کاملاً شفاف، 1.0 برای کاملاً مات)."},
    "emitter_lifetime_label": {"en": "Emitter Lifetime:", "fa": "طول عمر امیتر:"},
    "emitter_lifetime_continuous": {"en": "Continuous", "fa": "پیوسته"},
    "emitter_lifetime_once": {"en": "Once", "fa": "یک بار"},
    "emitter_duration_label": {"en": "Emitter Duration (ticks):", "fa": "مدت زمان امیتر (تیک):"},
    "emitter_duration_tooltip": {"en": "How long the emitter will spawn particles (in ticks, 20 ticks = 1 second). Only for 'Once' lifetime.", "fa": "مدت زمانی که امیتر پارتیکل اسپاون می‌کند (بر حسب تیک، 20 تیک = 1 ثانیه). فقط برای طول عمر 'یک بار'."},

    "generate_command_button": {
        "en": "Generate Particle Command",
        "fa": "تولید دستور پارتیکل"
    },
    "clear_fields_button": {
        "en": "Clear Fields",
        "fa": "پاک کردن فیلدها"
    },
    "copy_command_button": {
        "en": "Copy Command",
        "fa": "کپی دستور"
    },
    "export_command_json_button": {
        "en": "Export Command JSON",
        "fa": "خروجی JSON دستور"
    },
    "export_bedrock_addon_button": {
        "en": "Export Bedrock Addon (Basic)",
        "fa": "خروجی ادان Bedrock (پایه)"
    },
    "final_command_label": {
        "en": "Final Command:",
        "fa": "دستور نهایی:"
    },
    "how_to_use_frame_title": {
        "en": "How to Use in Minecraft",
        "fa": "نحوه استفاده در ماینکرافت"
    },
    "how_to_use_intro": {
        "en": "This section will guide you on how to use the generated particle commands and JSONs in Minecraft.",
        "fa": "این بخش شما را در نحوه استفاده از دستورات پارتیکل و فایل‌های JSON تولید شده در ماینکرافت راهنمایی می‌کند."
    },
    "how_to_use_step1_title": {"en": "1. Generating Your Command:", "fa": "1. تولید دستور شما:"},
    "how_to_use_step1_desc": {"en": "Customize your particle effect using the various options. The 'Final Command' field updates in real-time.", "fa": "با استفاده از گزینه‌ها و اسلایدرهای مختلف، افکت پارتیکل خود را سفارشی کنید. فیلد 'Final Command' به صورت لحظه‌ای با تغییرات شما به‌روزرسانی می‌شود."},
    "how_to_use_step2_title": {"en": "2. Copying the Command:", "fa": "2. کپی کردن دستور:"},
    "how_to_use_step2_desc": {"en": "Click 'Copy Command' to copy it to your clipboard. Use it in Minecraft chat (press 'T') or in a command block.", "fa": "پس از اینکه از دستور خود راضی بودید، روی دکمه 'Copy Command' کلیک کنید تا در کلیپ‌بورد کپی شود. می‌توانید آن را در چت ماینکرافت (با فشردن کلید 'T') یا در یک کامند بلاک استفاده کنید."},
    "how_to_use_step3_title": {"en": "3. Exporting to JSON:", "fa": "3. خروجی گرفتن به JSON:"},
    "how_to_use_step3a_title": {"en": "a. 'Export Command JSON':", "fa": "الف. 'خروجی JSON دستور':"},
    "how_to_use_step3a_desc": {"en": "Saves all current panel settings into a structured JSON file. This is for documentation or sharing the precise parameters you used to generate a `/particle` command.", "fa": "تمام تنظیمات فعلی پنل را در یک فایل JSON ساختاریافته ذخیره می‌کند. این برای مستندسازی یا اشتراک‌گذاری پارامترهای دقیقی است که برای تولید دستور `/particle` استفاده کرده‌اید."},
    "how_to_use_step3b_title": {"en": "b. 'Export Bedrock Addon (Basic)':", "fa": "ب. 'خروجی ادان Bedrock (پایه)':"},
    "how_to_use_step3b_desc": {
        "en": "Generates a `.particle.json` file for Minecraft Bedrock Edition behavior packs. This file defines a **custom particle effect**. You'll need to place this JSON within a behavior pack's `particles/` folder and ensure your `manifest.json` correctly references it. Remember, this is a basic template; complex effects might require manual additions to the JSON (e.g., render controllers, material setup, complex curves for animation).",
        "fa": "یک فایل `.particle.json` برای Behavior Packهای Minecraft Bedrock Edition تولید می‌کند. این فایل یک **افکت پارتیکل سفارشی** را تعریف می‌کند. شما باید این JSON را در پوشه `particles/` یک Behavior Pack قرار دهید و اطمینان حاصل کنید که `manifest.json` شما به درستی به آن ارجاع می‌دهد. به یاد داشته باشید، این یک قالب پایه است؛ افکت‌های پیچیده ممکن است نیاز به ویرایش دستی JSON (مانند کنترل‌کننده‌های رندر، تنظیم متریال، منحنی‌های پیچیده برای انیمیشن) داشته باشند."
    },
    "how_to_use_step4_title": {"en": "4. Understanding Particle Command Components:", "fa": "4. درک اجزای دستور پارتیکل:"},
    "how_to_use_step4_structure": {"en": "The basic structure is: `/particle <type> <pos> <delta> <speed> <count> <mode> [parameters]`", "fa": "ساختار اصلی به این صورت است: `/particle <type> <pos> <delta> <speed> <count> <mode> [parameters]`"},
    "how_to_use_step4_type": {"en": "- `<type>`: The specific particle ID (e.g., `minecraft:flame`, `minecraft:redstone`).", "fa": "- `<type>`: شناسه پارتیکل خاص (مثلاً `minecraft:flame`، `minecraft:redstone`)."},
    "how_to_use_step4_pos": {"en": "- `<pos>`: Where particles spawn (X Y Z coordinates or a target selector).", "fa": "- `<pos>`: محل اسپاون پارتیکل‌ها (مختصات X Y Z یا یک انتخاب‌کننده هدف)."},
    "how_to_use_step4_delta": {"en": "- `<delta>`: The maximum spread (dX dY dZ) from the origin. `0 0 0` means no random spread.", "fa": "- `<delta>`: حداکثر پراکندگی (dX dY dZ) از مبدأ. `0 0 0` به معنای عدم پراکندگی تصادفی است."},
    "how_to_use_step4_speed": {"en": "- `<speed>`: How fast particles move. `0` makes them stationary.", "fa": "- `<speed>`: سرعت حرکت پارتیکل‌ها. `0` باعث می‌شود پارتیکل‌ها ثابت بمانند."},
    "how_to_use_step4_count": {"en": "- `<count>`: Number of particles to spawn per command. Be cautious with high values to avoid lag.", "fa": "- `<count>`: تعداد پارتیکل‌هایی که در هر بار اجرای دستور اسپاون می‌شوند. در مورد مقادیر بالا برای جلوگیری از لگ احتیاط کنید."},
    "how_to_use_step4_mode": {"en": "- `<mode>`: `normal` (visible nearby) or `force` (always visible).", "fa": "- `<mode>`: `normal` (در نزدیکی قابل مشاهده) یا `force` (همیشه قابل مشاهده)."},
    "how_to_use_step4_parameters": {"en": "- `[parameters]`: Optional arguments for specific particle types (e.g., colors for `redstone`, block ID for `block`).", "fa": "- `[parameters]`: آرگومان‌های اختیاری برای انواع پارتیکل‌های خاص (مثلاً رنگ‌ها برای `redstone`، شناسه بلاک برای `block`)."},
    "how_to_use_step5_title": {"en": "5. Troubleshooting Common Issues:", "fa": "5. عیب‌یابی مشکلات رایج:"},
    "how_to_use_step5_cmd_not_working": {"en": "- Command Not Working: Double-check for typos, correct Minecraft IDs, and proper syntax. Permissions are also required (OP in single-player/server).", "fa": "- دستور کار نمی‌کند: املای کلمات، شناسه‌های صحیح ماینکرافت و نحو صحیح را دوباره بررسی کنید. همچنین مجوزهای لازم (OP در حالت تک‌نفره/سرور) مورد نیاز است."},
    "how_to_use_step5_no_particles": {"en": "- No Particles Appearing: Ensure you are in the correct Minecraft version and that 'Particles' are enabled in your video settings. Check command block power if applicable.", "fa": "- پارتیکل‌ها ظاهر نمی‌شوند: اطمینان حاصل کنید که در نسخه صحیح ماینکرافت هستید و 'Particles' در تنظیمات ویدیویی شما فعال است. اگر از کامند بلاک استفاده می‌کنید، بررسی کنید که آیا روشن است یا روی 'Always Active' تنظیم شده است."},
    "how_to_use_step5_lag": {"en": "- Lag/Performance Issues: Reduce 'Count' or 'Speed'. Avoid 'force' mode if not strictly necessary. Custom textures should be optimized.", "fa": "- مشکلات لگ/عملکرد: 'Count' یا 'Speed' پارتیکل‌ها را کاهش دهید. در صورت عدم نیاز ضروری، از حالت 'force' خودداری کنید. تکسچرهای سفارشی باید بهینه شوند."},
    "how_to_use_step5_addon_not_showing": {
        "en": "- Bedrock Addon Not Showing: Verify the `.particle.json` file is in the correct `behavior_pack/particles/` folder structure and that your `manifest.json` correctly points to the behavior pack. Check Minecraft's log for errors.",
        "fa": "- ادان Bedrock نمایش داده نمی‌شود: بررسی کنید که فایل `.particle.json` در ساختار پوشه `behavior_pack/particles/` صحیح قرار دارد و `manifest.json` شما به درستی به Behavior Pack اشاره می‌کند. لاگ‌های ماینکرافت را برای خطاها بررسی کنید."
    },
    "input_error": {"en": "Input Error", "fa": "خطای ورودی"},
    "cleared": {"en": "Cleared", "fa": "پاک شد"},
    "all_fields_cleared": {"en": "All fields have been cleared to default values.", "fa": "تمام فیلدها به مقادیر پیش‌فرض پاک شدند."},
    "copied": {"en": "Copied", "fa": "کپی شد"},
    "command_copied": {"en": "Command copied to clipboard!", "fa": "دستور در کلیپ‌بورد کپی شد!"},
    "no_command_to_copy": {"en": "No command to copy.", "fa": "دستوری برای کپی وجود ندارد."},
    "export_successful": {"en": "Export Successful", "fa": "خروجی با موفقیت انجام شد"},
    "particle_settings_saved": {"en": "Particle settings saved to:", "fa": "تنظیمات پارتیکل در مسیر ذخیره شد:"},
    "export_error": {"en": "Export Error", "fa": "خطای خروجی"},
    "failed_to_save_json": {"en": "Failed to save JSON file:", "fa": "ذخیره فایل JSON با شکست مواجه شد:"},
    "basic_template_note": {
        "en": "NOTE: This is a basic template. Further manual editing might be required to create complex Bedrock particle effects.",
        "fa": "توجه: این یک قالب پایه است. برای ایجاد افکت‌های پارتیکل پیچیده در Bedrock ممکن است نیاز به ویرایش دستی بیشتری باشد."
    },
    "uv_int_error": {"en": "UV coordinates must be integers.", "fa": "مختصات UV باید اعداد صحیح باشند."},
    "block_item_id_empty_error": {"en": "Block/Item ID cannot be empty for this particle type.", "fa": "شناسه بلاک/آیتم برای این نوع پارتیکل نمی‌تواند خالی باشد."},
    "particle_count_negative_error": {"en": "Particle count cannot be negative.", "fa": "تعداد پارتیکل نمی‌تواند منفی باشد."},
    "must_be_between": {"en": "must be between", "fa": "باید بین"},
    "and": {"en": "and", "fa": "و"},
    "must_be_a_number": {"en": "must be a number", "fa": "باید یک عدد باشد"},
    "cannot_be_negative": {"en": "cannot be negative", "fa": "نمی‌تواند منفی باشد"},
    "must_be_an_integer": {"en": "must be an integer", "fa": "باید یک عدد صحیح باشد"},
    "language_label": {"en": "Language:", "fa": "زبان:"},
    "language_tooltip": {"en": "Change the display language of the application.", "fa": "زبان نمایش برنامه را تغییر دهید."},
    "save_particle_settings_json_title": {"en": "Save Particle Settings as JSON", "fa": "ذخیره تنظیمات پارتیکل به عنوان JSON"},
    "save_bedrock_particle_json_title": {"en": "Save Bedrock Particle JSON", "fa": "ذخیره JSON پارتیکل Bedrock"},
}

# Global variable for current language 
current_language = "en"

# Helper function to get text based on current_language 
def get_localized_text(key):
    return TEXTS[key][current_language]

def get_localized_tooltip(key):
    return TEXTS[key][current_language]

# --- Tooltip Class for enhanced UI/UX ---
class ToolTip:
    """
    A simple tooltip class to display information when hovering over a widget.
    یک کلاس ساده برای نمایش راهنمای ابزار هنگام نگه داشتن ماوس روی یک ویجت.
    """
    def __init__(self, widget, text_key):
        self.widget = widget
        self.text_key = text_key
        self.tip_window = None
        self.id = None
        self.x = 0
        self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.update_text() # Initial text update 

    def update_text(self):
        """Updates the tooltip text based on the current language. / متن راهنمای ابزار را بر اساس زبان فعلی به‌روزرسانی می‌کند."""
        self.text = get_localized_tooltip(self.text_key)

    def enter(self, event=None):
        """Schedules the tooltip to appear after a short delay. / راهنمای ابزار را برای نمایش پس از تأخیر کوتاه برنامه‌ریزی می‌کند."""
        self.schedule()

    def leave(self, event=None):
        """Unschedules and hides the tooltip when the mouse leaves. / راهنمای ابزار را لغو و پنهان می‌کند."""
        self.unschedule()
        self.hide()

    def schedule(self):
        """Sets a timer to show the tooltip. / یک زمان‌سنج برای نمایش راهنمای ابزار تنظیم می‌کند."""
        self.unschedule()
        self.id = self.widget.after(500, self.show) 

    def unschedule(self):
        """Cancels the scheduled tooltip if it hasn't appeared yet. / راهنمای ابزار برنامه‌ریزی شده را لغو می‌کند."""
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show(self):
        """Displays the tooltip window. / پنجره راهنمای ابزار را نمایش می‌دهد."""
        if self.tip_window or not self.text:
            return
        
        # Calculate tooltip position relative to the widget
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        # Create a top-level window for the tooltip 
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True) 
        self.tip_window.wm_geometry(f"+{x}+{y}") 

        # Create and pack the label inside the tooltip window 
        label = tk.Label(self.tip_window, text=self.text, background="#FFFFCC", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide(self):
        """Hides (destroys) the tooltip window. / پنجره راهنمای ابزار را پنهان (نابود) می‌کند."""
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None

# List to hold all widgets that need language updates 
language_sensitive_widgets = []

def update_widget_text(widget, text_key=None, tooltip_key=None):
    """Updates a widget's text and tooltip based on the current language. / متن و راهنمای ابزار یک ویجت را بر اساس زبان فعلی به‌روزرسانی می‌کند."""
    if text_key:
        if isinstance(widget, (ttk.Label, ttk.Button, ttk.Checkbutton, ttk.Radiobutton, ttk.LabelFrame)):
            widget.config(text=get_localized_text(text_key))
        elif isinstance(widget, ttk.Combobox):
            # For combobox, update the displayed value if it's one of the language options
            if text_key == "particle_type_label": # This is a special case, not a direct text update
                pass
            else:
                widget.config(text=get_localized_text(text_key))
        elif isinstance(widget, tk.Toplevel): # For tooltip labels
            widget.config(text=get_localized_text(text_key))
    
    if hasattr(widget, '_tooltip'):
        widget._tooltip.update_text()

def set_language(lang):
    """Sets the application language and updates all UI elements. / زبان برنامه را تنظیم کرده و تمام عناصر رابط کاربری را به‌روزرسانی می‌کند."""
    global current_language
    current_language = lang
    root.title(get_localized_text("app_title"))
    for widget, text_key, tooltip_key in language_sensitive_widgets:
        update_widget_text(widget, text_key, tooltip_key)
    
    # Special handling for radio buttons and comboboxes where text might be part of options
    mode_radio_normal.config(text=get_localized_text("mode_normal"))
    mode_radio_force.config(text=get_localized_text("mode_force"))
    emitter_lifetime_radio_continuous.config(text=get_localized_text("emitter_lifetime_continuous"))
    emitter_lifetime_radio_once.config(text=get_localized_text("emitter_lifetime_once"))

    # Update dynamic UI elements 
    update_extra_params_ui()
    generate_command() # Regenerate command to update any language-dependent parts (e.g., tooltips in string)

# --- Validation Functions ---
def validate_float_range(value_str, min_val, max_val, field_name):
    """Validates if a string is a float within a specified range. / بررسی می‌کند که آیا یک رشته یک عدد اعشاری در محدوده مشخص است."""
    try:
        value = float(value_str)
        if not (min_val <= value <= max_val):
            messagebox.showerror(get_localized_text("input_error"), f"{field_name} {get_localized_text('must_be_between')} {min_val} {get_localized_text('and')} {max_val}.")
            return None
        return value
    except ValueError:
        messagebox.showerror(get_localized_text("input_error"), f"{field_name} {get_localized_text('must_be_a_number')}.")
        return None

def validate_int_positive(value_str, field_name):
    """Validates if a string is a positive integer. / بررسی می‌کند که آیا یک رشته یک عدد صحیح مثبت است."""
    try:
        value = int(value_str)
        if value < 0:
            messagebox.showerror(get_localized_text("input_error"), f"{field_name} {get_localized_text('cannot_be_negative')}.")
            return None
        return value
    except ValueError:
        messagebox.showerror(get_localized_text("input_error"), f"{field_name} {get_localized_text('must_be_an_integer')}.")
        return None

# --- Dynamic UI Logic  ---
def update_extra_params_ui(event=None):
    """
    Dynamically updates the extra parameters section based on the selected particle type.
    This function hides/shows specific input fields (RGB for redstone, ID for block/item,
    transition colors for dust_color_transition, vibration data for vibration,
    roll for sculk_charge, delay for shriek, block state for falling_dust)
    or the generic extra_params_entry.
    بخش پارامترهای اضافی را به صورت پویا بر اساس نوع پارتیکل انتخاب شده به‌روزرسانی می‌کند.
    این تابع فیلدهای ورودی خاص (RGB برای ردستون، ID برای بلاک/آیتم،
    رنگ‌های انتقال برای dust_color_transition، داده‌های ارتعاش برای vibration،
    چرخش برای sculk_charge، تأخیر برای shriek، حالت بلاک برای falling_dust)
    یا ورودی عمومی extra_params_entry را پنهان/نمایش می‌دهد.
    """
    # Clear all widgets in the dynamic extra params frame
    for widget in extra_params_dynamic_frame.winfo_children():
        widget.destroy()
    
    selected_particle = particle_type_var.get()

    # Hide all advanced texture/rotation/gravity/collision controls by default for simplicity
    texture_path_label.grid_remove()
    texture_path_entry.grid_remove()
    uv_label.grid_remove()
    uv_frame.grid_remove()
    rotation_label.grid_remove()
    roll_slider.grid_remove()
    angular_velocity_label.grid_remove()
    angular_velocity_entry.grid_remove()
    gravity_label.grid_remove()
    gravity_entry.grid_remove()
    collisions_checkbox.grid_remove()
    max_lifetime_label.grid_remove()
    max_lifetime_entry.grid_remove()
    linear_velocity_label.grid_remove()
    linear_velocity_frame.grid_remove()
    spawn_rate_label.grid_remove()
    spawn_rate_entry.grid_remove()
    max_particles_label.grid_remove()
    max_particles_entry.grid_remove()
    lighting_checkbox.grid_remove() 

    linear_drag_label.grid_remove()
    linear_drag_entry.grid_remove()
    collision_resilience_label.grid_remove()
    collision_resilience_entry.grid_remove()
    collision_radius_label.grid_remove()
    collision_radius_entry.grid_remove()
    spawn_offset_label.grid_remove()
    spawn_offset_frame.grid_remove()
    size_over_lifetime_label.grid_remove()
    size_over_lifetime_frame.grid_remove()
    alpha_over_lifetime_label.grid_remove()
    alpha_over_lifetime_frame.grid_remove()
    emitter_lifetime_label.grid_remove()
    emitter_lifetime_frame.grid_remove()
    emitter_duration_label.grid_remove()
    emitter_duration_entry.grid_remove()

    # Set default values for general sliders and reset dynamic specific ones
    speed_slider.set(1.0)
    count_slider.set(1)
    
    # Redstone particle specific controls 
    ttk.Label(extra_params_dynamic_frame, text=get_localized_text("redstone_color_start_label")).grid(row=0, column=0, sticky="w", pady=2, padx=5)
    red_slider.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
    ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('green_tooltip').split('(')[0].strip()} (0-1):").grid(row=1, column=0, sticky="w", pady=2, padx=5)
    green_slider.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
    ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('blue_tooltip').split('(')[0].strip()} (0-1):").grid(row=2, column=0, sticky="w", pady=2, padx=5)
    blue_slider.grid(row=2, column=1, sticky="ew", pady=2, padx=5)
    ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('size_tooltip').split('(')[0].strip()} (0-4):").grid(row=3, column=0, sticky="w", pady=2, padx=5)
    size_slider.grid(row=3, column=1, sticky="ew", pady=2, padx=5)

    red_slider.set(1.0)
    green_slider.set(0.0)
    blue_slider.set(0.0)
    size_slider.set(1.0)

    ttk.Label(extra_params_dynamic_frame, text=get_localized_text("redstone_color_end_label")).grid(row=4, column=0, sticky="w", pady=2, padx=5)
    end_red_slider.grid(row=4, column=1, sticky="ew", pady=2, padx=5)
    ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('green_tooltip').split('(')[0].strip()} (0-1):").grid(row=5, column=0, sticky="w", pady=2, padx=5)
    end_green_slider.grid(row=5, column=1, sticky="ew", pady=2, padx=5)
    ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('blue_tooltip').split('(')[0].strip()} (0-1):").grid(row=6, column=0, sticky="w", pady=2, padx=5)
    end_blue_slider.grid(row=6, column=1, sticky="ew", pady=2, padx=5)

    end_red_slider.set(1.0) 
    end_green_slider.set(0.0)
    end_blue_slider.set(0.0)


    if selected_particle == "minecraft:block" or selected_particle == "minecraft:item":
        ttk.Label(extra_params_dynamic_frame, text=get_localized_text("block_item_id_label")).grid(row=0, column=0, sticky="w", pady=2, padx=5)
        block_item_id_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        ToolTip(block_item_id_entry, "block_item_id_tooltip")
        block_item_id_entry.delete(0, tk.END)
    elif selected_particle == "minecraft:dust_color_transition":
        ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('from_red_tooltip').split('(')[0].strip()} (0-1):").grid(row=0, column=0, sticky="w", pady=2, padx=5)
        from_red_slider.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('from_green_tooltip').split('(')[0].strip()} (0-1):").grid(row=1, column=0, sticky="w", pady=2, padx=5)
        from_green_slider.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('from_blue_tooltip').split('(')[0].strip()} (0-1):").grid(row=2, column=0, sticky="w", pady=2, padx=5)
        from_blue_slider.grid(row=2, column=1, sticky="ew", pady=2, padx=5)
        
        ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('to_red_tooltip').split('(')[0].strip()} (0-1):").grid(row=3, column=0, sticky="w", pady=2, padx=5)
        to_red_slider.grid(row=3, column=1, sticky="ew", pady=2, padx=5)
        ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('to_green_tooltip').split('(')[0].strip()} (0-1):").grid(row=4, column=0, sticky="w", pady=2, padx=5)
        to_green_slider.grid(row=4, column=1, sticky="ew", pady=2, padx=5)
        ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('to_blue_tooltip').split('(')[0].strip()} (0-1):").grid(row=5, column=0, sticky="w", pady=2, padx=5)
        to_blue_slider.grid(row=5, column=1, sticky="ew", pady=2, padx=5)

        ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('size_transition_tooltip').split('(')[0].strip()} (0-4):").grid(row=6, column=0, sticky="w", pady=2, padx=5)
        size_transition_slider.grid(row=6, column=1, sticky="ew", pady=2, padx=5)

        from_red_slider.set(1.0)
        from_green_slider.set(0.0)
        from_blue_slider.set(0.0)
        to_red_slider.set(0.0)
        to_green_slider.set(1.0)
        to_blue_slider.set(0.0)
        size_transition_slider.set(1.0)
    elif selected_particle == "minecraft:vibration":
        ttk.Label(extra_params_dynamic_frame, text=get_localized_text("dest_x_label")).grid(row=0, column=0, sticky="w", pady=2, padx=5)
        vibration_x_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        ttk.Label(extra_params_dynamic_frame, text=get_localized_text("dest_y_label")).grid(row=1, column=0, sticky="w", pady=2, padx=5)
        vibration_y_entry.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        ttk.Label(extra_params_dynamic_frame, text=get_localized_text("dest_z_label")).grid(row=2, column=0, sticky="w", pady=2, padx=5)
        vibration_z_entry.grid(row=2, column=1, sticky="ew", pady=2, padx=5)
        ttk.Label(extra_params_dynamic_frame, text=get_localized_text("arrival_ticks_label")).grid(row=3, column=0, sticky="w", pady=2, padx=5)
        arrival_ticks_entry.grid(row=3, column=1, sticky="ew", pady=2, padx=5)
        
        ToolTip(vibration_x_entry, "vibration_x_tooltip")
        ToolTip(vibration_y_entry, "vibration_y_tooltip")
        ToolTip(vibration_z_entry, "vibration_z_tooltip")
        ToolTip(arrival_ticks_entry, "arrival_ticks_tooltip")

        vibration_x_entry.delete(0, tk.END)
        vibration_y_entry.delete(0, tk.END)
        vibration_z_entry.delete(0, tk.END)
        arrival_ticks_entry.delete(0, tk.END)
    elif selected_particle == "minecraft:sculk_charge":
        ttk.Label(extra_params_dynamic_frame, text=get_localized_text("roll_label")).grid(row=0, column=0, sticky="w", pady=2, padx=5)
        sculk_roll_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        ToolTip(sculk_roll_entry, "roll_tooltip")
        
        sculk_roll_entry.delete(0, tk.END); sculk_roll_entry.insert(0, "0.0")
    elif selected_particle == "minecraft:shriek":
        ttk.Label(extra_params_dynamic_frame, text=get_localized_text("delay_label")).grid(row=0, column=0, sticky="w", pady=2, padx=5)
        shriek_delay_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        ToolTip(shriek_delay_entry, "delay_tooltip")
        
        shriek_delay_entry.delete(0, tk.END); shriek_delay_entry.insert(0, "0")
    elif selected_particle == "minecraft:falling_dust":
        ttk.Label(extra_params_dynamic_frame, text=get_localized_text("block_state_label")).grid(row=0, column=0, sticky="w", pady=2, padx=5)
        falling_dust_block_state_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        ToolTip(falling_dust_block_state_entry, "block_state_tooltip")
        
        falling_dust_block_state_entry.delete(0, tk.END); falling_dust_block_state_entry.insert(0, "minecraft:sand")
    else:
        # Generic extra parameters for other particle types
        extra_params_label.grid(row=0, column=0, sticky="w", pady=10, padx=5)
        extra_params_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=5)
        extra_params_help_label.grid(row=0, column=2, sticky="w", padx=5)
        extra_params_entry.delete("1.0", tk.END) 
    
    # Restore visibility of advanced texture/rotation/gravity/collision if advanced view is on
    if show_advanced_var.get():
        texture_path_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        texture_path_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        uv_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        uv_frame.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        rotation_label.grid(row=2, column=0, sticky="w", pady=5, padx=5)
        roll_slider.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        angular_velocity_label.grid(row=3, column=0, sticky="w", pady=5, padx=5)
        angular_velocity_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
        gravity_label.grid(row=4, column=0, sticky="w", pady=5, padx=5)
        gravity_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
        collisions_checkbox.grid(row=5, column=0, columnspan=2, sticky="w", pady=5, padx=5)
        max_lifetime_label.grid(row=6, column=0, sticky="w", pady=5, padx=5)
        max_lifetime_entry.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
        linear_velocity_label.grid(row=7, column=0, sticky="w", pady=5, padx=5)
        linear_velocity_frame.grid(row=7, column=1, sticky="ew", pady=5, padx=5)
        spawn_rate_label.grid(row=8, column=0, sticky="w", pady=5, padx=5)
        spawn_rate_entry.grid(row=8, column=1, sticky="ew", pady=5, padx=5)
        max_particles_label.grid(row=9, column=0, sticky="w", pady=5, padx=5)
        max_particles_entry.grid(row=9, column=1, sticky="ew", pady=5, padx=5)
        lighting_checkbox.grid(row=10, column=0, columnspan=2, sticky="w", pady=5, padx=5) 

        #  advanced rendering/behavior controls
        linear_drag_label.grid(row=11, column=0, sticky="w", pady=5, padx=5)
        linear_drag_entry.grid(row=11, column=1, sticky="ew", pady=5, padx=5)
        collision_resilience_label.grid(row=12, column=0, sticky="w", pady=5, padx=5)
        collision_resilience_entry.grid(row=12, column=1, sticky="ew", pady=5, padx=5)
        collision_radius_label.grid(row=13, column=0, sticky="w", pady=5, padx=5)
        collision_radius_entry.grid(row=13, column=1, sticky="ew", pady=5, padx=5)
        spawn_offset_label.grid(row=14, column=0, sticky="w", pady=5, padx=5)
        spawn_offset_frame.grid(row=14, column=1, sticky="ew", pady=5, padx=5)
        size_over_lifetime_label.grid(row=15, column=0, sticky="w", pady=5, padx=5)
        size_over_lifetime_frame.grid(row=15, column=1, sticky="ew", pady=5, padx=5)
        alpha_over_lifetime_label.grid(row=16, column=0, sticky="w", pady=5, padx=5)
        alpha_over_lifetime_frame.grid(row=16, column=1, sticky="ew", pady=5, padx=5)
        emitter_lifetime_label.grid(row=17, column=0, sticky="w", pady=5, padx=5)
        emitter_lifetime_frame.grid(row=17, column=1, sticky="ew", pady=5, padx=5)
        
        if emitter_lifetime_var.get() == "once":
            emitter_duration_label.grid(row=18, column=0, sticky="w", pady=5, padx=5)
            emitter_duration_entry.grid(row=18, column=1, sticky="ew", pady=5, padx=5)
        else:
            emitter_duration_label.grid_remove()
            emitter_duration_entry.grid_remove()

    # After updating UI, regenerate command for live preview
    generate_command()
    # Update all tooltips after UI changes
    for widget, _, _ in language_sensitive_widgets:
        if hasattr(widget, '_tooltip'):
            widget._tooltip.update_text()


# --- Command Generation Logic / منطق تولید دستور ---
def generate_command(event=None):
    """
    Generates the Minecraft /particle command based on user input from the GUI.
    This function is called when the button is pressed or when a relevant input changes.
    دستور /particle ماینکرافت را بر اساس ورودی کاربر از رابط کاربری تولید می‌کند.
    این تابع هنگام فشرده شدن دکمه یا تغییر ورودی مربوطه فراخوانی می‌شود.
    """
    particle_type = particle_type_var.get()
    
    # Get target selector or position coordinates
    target_selector = target_selector_entry.get().strip()
    x_pos = x_pos_entry.get() or "~"
    y_pos = y_pos_entry.get() or "~"
    z_pos = z_pos_entry.get() or "~"

    # Validate numeric inputs for delta
    x_delta = validate_float_range(x_delta_entry.get() or "0", -1000.0, 1000.0, get_localized_text("delta_x_tooltip").split('(')[0].strip())
    if x_delta is None: return
    y_delta = validate_float_range(y_delta_entry.get() or "0", -1000.0, 1000.0, get_localized_text("delta_y_tooltip").split('(')[0].strip())
    if y_delta is None: return
    z_delta = validate_float_range(z_delta_entry.get() or "0", -1000.0, 1000.0, get_localized_text("delta_z_tooltip").split('(')[0].strip())
    if z_delta is None: return
    
    # Get values from sliders 
    speed = speed_slider.get()
    count = int(count_slider.get())

    # Validate count (already handled by slider range, but good for direct input)
    if count < 0:
        messagebox.showerror(get_localized_text("input_error"), get_localized_text("particle_count_negative_error"))
        return

    mode = mode_var.get()
    
    # Handle extra parameters based on selected particle type
    extra_params_str = ""
    if particle_type == "minecraft:redstone":
        r = validate_float_range(red_slider.get(), 0.0, 1.0, get_localized_text("red_tooltip").split('(')[0].strip())
        g = validate_float_range(green_slider.get(), 0.0, 1.0, get_localized_text("green_tooltip").split('(')[0].strip())
        b = validate_float_range(blue_slider.get(), 0.0, 1.0, get_localized_text("blue_tooltip").split('(')[0].strip())
        size = validate_float_range(size_slider.get(), 0.0, 4.0, get_localized_text("size_tooltip").split('(')[0].strip())
        
        end_r = validate_float_range(end_red_slider.get(), 0.0, 1.0, get_localized_text("redstone_color_end_label").split('(')[0].strip())
        end_g = validate_float_range(end_green_slider.get(), 0.0, 1.0, get_localized_text("redstone_color_end_label").split('(')[0].strip())
        end_b = validate_float_range(end_blue_slider.get(), 0.0, 1.0, get_localized_text("redstone_color_end_label").split('(')[0].strip())

        if None in [r, g, b, size, end_r, end_g, end_b]: return

        if (r, g, b) == (end_r, end_g, end_b):
            extra_params_str = f"{r} {g} {b} {size}"
        else:
            extra_params_str = f"{r} {g} {b} {size}" 

    elif particle_type == "minecraft:block" or particle_type == "minecraft:item":
        block_item_id = block_item_id_entry.get().strip()
        if not block_item_id:
            messagebox.showerror(get_localized_text("input_error"), get_localized_text("block_item_id_empty_error"))
            return
        extra_params_str = block_item_id
    elif particle_type == "minecraft:dust_color_transition":
        from_r = validate_float_range(from_red_slider.get(), 0.0, 1.0, get_localized_text("from_red_tooltip").split('(')[0].strip())
        from_g = validate_float_range(from_green_slider.get(), 0.0, 1.0, get_localized_text("from_green_tooltip").split('(')[0].strip())
        from_b = validate_float_range(from_blue_slider.get(), 0.0, 1.0, get_localized_text("from_blue_tooltip").split('(')[0].strip())
        to_r = validate_float_range(to_red_slider.get(), 0.0, 1.0, get_localized_text("to_red_tooltip").split('(')[0].strip())
        to_g = validate_float_range(to_green_slider.get(), 0.0, 1.0, get_localized_text("to_green_tooltip").split('(')[0].strip())
        to_b = validate_float_range(to_blue_slider.get(), 0.0, 1.0, get_localized_text("to_blue_tooltip").split('(')[0].strip())
        size = validate_float_range(size_transition_slider.get(), 0.0, 4.0, get_localized_text("size_transition_tooltip").split('(')[0].strip())
        if None in [from_r, from_g, from_b, to_r, to_g, to_b, size]: return
        extra_params_str = f"{from_r} {from_g} {from_b} {to_r} {to_g} {to_b} {size}"
    elif particle_type == "minecraft:vibration":
        dest_x = vibration_x_entry.get() or "~"
        dest_y = vibration_y_entry.get() or "~"
        dest_z = vibration_z_entry.get() or "~"
        arrival_ticks = validate_int_positive(arrival_ticks_entry.get(), get_localized_text("arrival_ticks_label"))
        if arrival_ticks is None: return
        extra_params_str = f"minecraft:block {dest_x} {dest_y} {dest_z} {arrival_ticks}" 
    elif particle_type == "minecraft:sculk_charge":
        roll = validate_float_range(sculk_roll_entry.get(), 0.0, 2 * math.pi, get_localized_text("roll_label").split('(')[0].strip())
        if roll is None: return
        extra_params_str = f"{roll}"
    elif particle_type == "minecraft:shriek":
        delay = validate_int_positive(shriek_delay_entry.get(), get_localized_text("delay_label"))
        if delay is None: return
        extra_params_str = f"{delay}"
    elif particle_type == "minecraft:falling_dust":
        block_state = falling_dust_block_state_entry.get().strip()
        if not block_state:
            messagebox.showerror(get_localized_text("input_error"), get_localized_text("block_state_tooltip").split('(')[0].strip())
            return
        extra_params_str = block_state
    else:
        extra_params_str = extra_params_entry.get("1.0", tk.END).strip()

    # Determine position or target selector for the command
    if target_selector:
        position_part = target_selector
    else:
        position_part = f"{x_pos} {y_pos} {z_pos}"

    # Construct the base particle command
    command = f"/particle {particle_type} {position_part} {x_delta} {y_delta} {z_delta} {speed} {count} {mode}"

    # Add extra parameters if provided 
    if extra_params_str:
        command += f" {extra_params_str}"

    # Display the generated command in the output entry field
    command_output.delete(0, tk.END)
    command_output.insert(0, command)

# --- Utility Functions ---
def clear_fields():
    """
    Clears all input fields and resets them to default values.
    تمام فیلدهای ورودی را پاک کرده و آن‌ها را به مقادیر پیش‌فرض بازنشانی می‌کند.
    """
    particle_type_var.set(particle_types[0])
    target_selector_entry.delete(0, tk.END)
    x_pos_entry.delete(0, tk.END); x_pos_entry.insert(0, "~")
    y_pos_entry.delete(0, tk.END); y_pos_entry.insert(0, "~")
    z_pos_entry.delete(0, tk.END); z_pos_entry.insert(0, "~")
    x_delta_entry.delete(0, tk.END); x_delta_entry.insert(0, "0.0")
    y_delta_entry.delete(0, tk.END); y_delta_entry.insert(0, "0.0")
    z_delta_entry.delete(0, tk.END); z_delta_entry.insert(0, "0.0")
    speed_slider.set(1.0)
    count_slider.set(1)
    mode_var.set("normal")
    extra_params_entry.delete("1.0", tk.END)
    
    # Custom/Advanced Parameters 
    red_slider.set(1.0); green_slider.set(0.0); blue_slider.set(0.0); size_slider.set(1.0)
    end_red_slider.set(1.0); end_green_slider.set(0.0); end_blue_slider.set(0.0)
    
    block_item_id_entry.delete(0, tk.END)
    from_red_slider.set(1.0); from_green_slider.set(0.0); from_blue_slider.set(0.0)
    to_red_slider.set(0.0); to_green_slider.set(1.0); to_blue_slider.set(0.0)
    size_transition_slider.set(1.0)
    vibration_x_entry.delete(0, tk.END)
    vibration_y_entry.delete(0, tk.END)
    vibration_z_entry.delete(0, tk.END)
    arrival_ticks_entry.delete(0, tk.END)
    sculk_roll_entry.delete(0, tk.END); sculk_roll_entry.insert(0, "0.0")
    shriek_delay_entry.delete(0, tk.END); shriek_delay_entry.insert(0, "0")
    falling_dust_block_state_entry.delete(0, tk.END); falling_dust_block_state_entry.insert(0, "minecraft:sand")

    # Clear texture/rotation/gravity/collision params
    texture_path_entry.delete(0, tk.END)
    uv_u_entry.delete(0, tk.END); uv_u_entry.insert(0, "0")
    uv_v_entry.delete(0, tk.END); uv_v_entry.insert(0, "0")
    uv_w_entry.delete(0, tk.END); uv_w_entry.insert(0, "16")
    uv_h_entry.delete(0, tk.END); uv_h_entry.insert(0, "16")
    roll_slider.set(0.0)
    angular_velocity_entry.delete(0, tk.END); angular_velocity_entry.insert(0, "0.0")
    gravity_entry.delete(0, tk.END); gravity_entry.insert(0, "0.0")
    collisions_var.set(False)
    max_lifetime_entry.delete(0, tk.END); max_lifetime_entry.insert(0, "5.0")
    motion_x_entry.delete(0, tk.END); motion_x_entry.insert(0, "0.0")
    motion_y_entry.delete(0, tk.END); motion_y_entry.insert(0, "0.0")
    motion_z_entry.delete(0, tk.END); motion_z_entry.insert(0, "0.0")
    spawn_rate_entry.delete(0, tk.END); spawn_rate_entry.insert(0, "10")
    max_particles_entry.delete(0, tk.END); max_particles_entry.insert(0, "100")
    lighting_var.set(True) 

    linear_drag_entry.delete(0, tk.END); linear_drag_entry.insert(0, "0.0")
    collision_resilience_entry.delete(0, tk.END); collision_resilience_entry.insert(0, "0.0")
    collision_radius_entry.delete(0, tk.END); collision_radius_entry.insert(0, "0.1")
    spawn_offset_x_entry.delete(0, tk.END); spawn_offset_x_entry.insert(0, "0.0")
    spawn_offset_y_entry.delete(0, tk.END); spawn_offset_y_entry.insert(0, "0.0")
    spawn_offset_z_entry.delete(0, tk.END); spawn_offset_z_entry.insert(0, "0.0")
    size_over_lifetime_start_entry.delete(0, tk.END); size_over_lifetime_start_entry.insert(0, "1.0")
    size_over_lifetime_end_entry.delete(0, tk.END); size_over_lifetime_end_entry.insert(0, "1.0")
    alpha_over_lifetime_start_entry.delete(0, tk.END); alpha_over_lifetime_start_entry.insert(0, "1.0")
    alpha_over_lifetime_end_entry.delete(0, tk.END); alpha_over_lifetime_end_entry.insert(0, "1.0")
    emitter_lifetime_var.set("continuous")
    emitter_duration_entry.delete(0, tk.END); emitter_duration_entry.insert(0, "20")


    command_output.delete(0, tk.END)
    messagebox.showinfo(get_localized_text("cleared"), get_localized_text("all_fields_cleared"))
    update_extra_params_ui() 

def copy_command():
    """
    Copies the generated command to the clipboard.
    دستور تولید شده را در کلیپ‌بورد کپی می‌کند.
    """
    command_text = command_output.get()
    if command_text:
        root.clipboard_clear()
        root.clipboard_append(command_text)
        messagebox.showinfo(get_localized_text("copied"), get_localized_text("command_copied"))
    else:
        messagebox.showwarning(get_localized_text("input_error"), get_localized_text("no_command_to_copy"))

def export_to_json():
    """
    Exports the current particle command parameters to a JSON file.
    This JSON represents the parameters used to generate the /particle command.
    پارامترهای دستور پارتیکل فعلی را به یک فایل JSON خروجی می‌گیرد.
    این JSON نشان‌دهنده پارامترهای استفاده شده برای تولید دستور /particle است.
    """
    particle_data = {
        "particle_type": particle_type_var.get(),
        "target_selector": target_selector_entry.get().strip(),
        "position": {
            "x": x_pos_entry.get() or "~",
            "y": y_pos_entry.get() or "~",
            "z": z_pos_entry.get() or "~"
        },
        "delta": {
            "dx": float(x_delta_entry.get() or "0"),
            "dy": float(y_delta_entry.get() or "0"),
            "dz": float(z_delta_entry.get() or "0")
        },
        "speed": speed_slider.get(),
        "count": int(count_slider.get()),
        "display_mode": mode_var.get(),
        "advanced_parameters": {
            "texture": texture_path_entry.get().strip(),
            "uv_rect": {
                "u": int(uv_u_entry.get() or "0"),
                "v": int(uv_v_entry.get() or "0"),
                "w": int(uv_w_entry.get() or "16"),
                "h": int(uv_h_entry.get() or "16")
            },
            "roll": roll_slider.get(),
            "angular_velocity": float(angular_velocity_entry.get() or "0"),
            "gravity_modifier": float(gravity_entry.get() or "0"),
            "linear_drag_coefficient": float(linear_drag_entry.get() or "0.0"),
            "collision_resilience": float(collision_resilience_entry.get() or "0.0"),
            "collision_radius": float(collision_radius_entry.get() or "0.1"),
            "collisions": collisions_var.get(),
            "max_lifetime": float(max_lifetime_entry.get() or "5.0"),
            "linear_velocity": {
                "x": float(motion_x_entry.get() or "0"),
                "y": float(motion_y_entry.get() or "0"),
                "z": float(motion_z_entry.get() or "0")
            },
            "spawn_rate": int(spawn_rate_entry.get() or "10"),
            "max_particles": int(max_particles_entry.get() or "100"),
            "lighting": lighting_var.get(),
            "spawn_offset": {
                "x": float(spawn_offset_x_entry.get() or "0.0"),
                "y": float(spawn_offset_y_entry.get() or "0.0"),
                "z": float(spawn_offset_z_entry.get() or "0.0")
            },
            "size_over_lifetime": {
                "start_size": float(size_over_lifetime_start_entry.get() or "1.0"),
                "end_size": float(size_over_lifetime_end_entry.get() or "1.0")
            },
            "alpha_over_lifetime": {
                "start_alpha": float(alpha_over_lifetime_start_entry.get() or "1.0"),
                "end_alpha": float(alpha_over_lifetime_end_entry.get() or "1.0")
            },
            "emitter_lifetime_type": emitter_lifetime_var.get(),
            "emitter_duration_ticks": int(emitter_duration_entry.get() or "20") if emitter_lifetime_var.get() == "once" else None
        },
        "particle_specific_parameters": {}
    }

    selected_particle = particle_type_var.get()
    if selected_particle == "minecraft:redstone":
        particle_data["particle_specific_parameters"] = {
            "start_color": {
                "red": red_slider.get(),
                "green": green_slider.get(),
                "blue": blue_slider.get()
            },
            "end_color": { 
                "red": end_red_slider.get(),
                "green": end_green_slider.get(),
                "blue": end_blue_slider.get()
            },
            "size": size_slider.get()
        }
    elif selected_particle == "minecraft:block" or selected_particle == "minecraft:item":
        particle_data["particle_specific_parameters"] = {
            "id": block_item_id_entry.get().strip()
        }
    elif selected_particle == "minecraft:dust_color_transition":
        particle_data["particle_specific_parameters"] = {
            "from_color": {
                "red": from_red_slider.get(),
                "green": from_green_slider.get(),
                "blue": from_blue_slider.get()
            },
            "to_color": {
                "red": to_red_slider.get(),
                "green": to_green_slider.get(),
                "blue": to_blue_slider.get()
            },
            "size": size_transition_slider.get()
        }
    elif selected_particle == "minecraft:vibration":
        particle_data["particle_specific_parameters"] = {
            "destination": {
                "x": vibration_x_entry.get() or "~",
                "y": vibration_y_entry.get() or "~",
                "z": vibration_z_entry.get() or "~"
            },
            "arrival_ticks": int(arrival_ticks_entry.get() or "0")
        }
    elif selected_particle == "minecraft:sculk_charge":
        particle_data["particle_specific_parameters"] = {
            "roll": float(sculk_roll_entry.get() or "0.0")
        }
    elif selected_particle == "minecraft:shriek":
        particle_data["particle_specific_parameters"] = {
            "delay": int(shriek_delay_entry.get() or "0")
        }
    elif selected_particle == "minecraft:falling_dust":
        particle_data["particle_specific_parameters"] = {
            "block_state": falling_dust_block_state_entry.get().strip()
        }
    else:
        extra_text = extra_params_entry.get("1.0", tk.END).strip()
        if extra_text:
            particle_data["particle_specific_parameters"] = {"raw_extra_data": extra_text}

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title=get_localized_text("save_particle_settings_json_title") 
    )
    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(particle_data, f, indent=4)
            messagebox.showinfo(get_localized_text("export_successful"), f"{get_localized_text('particle_settings_saved')}\n{file_path}")
        except Exception as e:
            messagebox.showerror(get_localized_text("export_error"), f"{get_localized_text('failed_to_save_json')} {e}")

def export_as_bedrock_addon():
    """
    Exports the current settings as a basic Minecraft Bedrock Edition particle JSON.
    This generates a simplified .particle.json structure.
    تنظیمات فعلی را به عنوان یک JSON پارتیکل پایه Minecraft Bedrock Edition خروجی می‌گیرد.
    این یک ساختار .particle.json ساده شده را تولید می‌کند.
    """
    identifier_name = particle_type_var.get().replace("minecraft:", "custom:").replace("/", "_")
    
    # Use selected texture or default
    texture_path = texture_path_entry.get().strip()
    if not texture_path:
        texture_path = "textures/particle/particles" 

    # UV coordinates 
    try:
        u = int(uv_u_entry.get() or "0")
        v = int(uv_v_entry.get() or "0")
        w = int(uv_w_entry.get() or "16")
        h = int(uv_h_entry.get() or "16")
    except ValueError:
        messagebox.showerror(get_localized_text("input_error"), get_localized_text("uv_int_error"))
        return

    # Colors 
    start_r, start_g, start_b = red_slider.get(), green_slider.get(), blue_slider.get()
    end_r, end_g, end_b = end_red_slider.get(), end_green_slider.get(), end_blue_slider.get()

    # Alpha over lifetime 
    start_alpha = validate_float_range(alpha_over_lifetime_start_entry.get() or "1.0", 0.0, 1.0, get_localized_text("start_alpha_label"))
    end_alpha = validate_float_range(alpha_over_lifetime_end_entry.get() or "1.0", 0.0, 1.0, get_localized_text("end_alpha_label"))
    if start_alpha is None or end_alpha is None: return

    # Size over lifetime 
    start_size_scale = validate_float_range(size_over_lifetime_start_entry.get() or "1.0", 0.0, 10.0, get_localized_text("start_size_label"))
    end_size_scale = validate_float_range(size_over_lifetime_end_entry.get() or "1.0", 0.0, 10.0, get_localized_text("end_size_label"))
    if start_size_scale is None or end_size_scale is None: return

    # Spawn Offset 
    spawn_off_x = validate_float_range(spawn_offset_x_entry.get() or "0.0", -100.0, 100.0, get_localized_text("spawn_offset_label") + " X")
    spawn_off_y = validate_float_range(spawn_offset_y_entry.get() or "0.0", -100.0, 100.0, get_localized_text("spawn_offset_label") + " Y")
    spawn_off_z = validate_float_range(spawn_offset_z_entry.get() or "0.0", -100.0, 100.0, get_localized_text("spawn_offset_label") + " Z")
    if None in [spawn_off_x, spawn_off_y, spawn_off_z]: return

    # Linear Drag 
    linear_drag_coeff = validate_float_range(linear_drag_entry.get() or "0.0", 0.0, 1.0, get_localized_text("linear_drag_label"))
    if linear_drag_coeff is None: return

    # Collision Resilience 
    collision_res = validate_float_range(collision_resilience_entry.get() or "0.0", 0.0, 1.0, get_localized_text("collision_resilience_label"))
    if collision_res is None: return

    # Collision Radius 
    collision_rad = validate_float_range(collision_radius_entry.get() or "0.1", 0.0, 10.0, get_localized_text("collision_radius_label"))
    if collision_rad is None: return

    # Emitter Lifetime 
    emitter_lifetime_type = emitter_lifetime_var.get()
    emitter_duration_ticks = None
    if emitter_lifetime_type == "once":
        emitter_duration_ticks = validate_int_positive(emitter_duration_entry.get() or "20", get_localized_text("emitter_duration_label"))
        if emitter_duration_ticks is None: return


    # Bedrock particle structure 
    bedrock_particle_json = {
        "format_version": "1.10.0", 
        "minecraft:particle_effect": {
            "description": {
                "identifier": identifier_name,
                "basic_render_parameters": {
                    "material": "particles_alpha", 
                    "texture": texture_path
                }
            },
            "components": {
                "minecraft:emitter_rate_steady": {
                    "spawn_rate": int(spawn_rate_entry.get() or "10"),
                    "max_particles": int(max_particles_entry.get() or "100")
                },
                "minecraft:emitter_lifetime_expression": {
                    "activation_expression": "1", 
                    "expiration_expression": "1" 
                },
                "minecraft:emitter_shape_point": {
                    "offset": [spawn_off_x, spawn_off_y, spawn_off_z]
                }, 
                "minecraft:particle_initial_speed": float(speed_slider.get()),
                "minecraft:particle_initial_spin": {
                    "rotation": float(roll_slider.get()),
                    "rotation_rate": float(angular_velocity_entry.get() or "0")
                },
                "minecraft:particle_lifetime_expression": {
                    "max_lifetime": float(max_lifetime_entry.get() or "5.0")
                },
                "minecraft:particle_motion_basic": {
                    "linear_acceleration": [
                        float(motion_x_entry.get() or "0"),
                        float(motion_y_entry.get() or "0"),
                        float(motion_z_entry.get() or "0")
                    ],
                    "linear_drag_coefficient": linear_drag_coeff
                },
                "minecraft:particle_appearance_billboard": {
                    "size": {
                        "interpolant": "query.life_time / query.particle_lifetime",
                        "controller": f"variable.size = ({start_size_scale}) + (({end_size_scale}) - ({start_size_scale})) * query.interpolant;" 
                    },
                    "facing_camera_mode": "lookat_xyz",
                    "uv": {
                        "texture_width": 16, 
                        "texture_height": 16,
                        "uv_rect": {
                            "u": u,
                            "v": v,
                            "w": w,
                            "h": h
                        }
                    }
                },
                "minecraft:particle_motion_collision": {
                    "collision_drag": linear_drag_coeff, 
                    "collision_radius": collision_rad, 
                    "collision_resilience": collision_res,
                    "enabled": collisions_var.get()
                },
                "minecraft:particle_motion_dynamics": {
                    "linear_acceleration": ["0", f"-{float(gravity_entry.get() or '0')}", "0"] 
                }
            }
        }
    }

    # Set emitter lifetime component
    if emitter_lifetime_type == "once" and emitter_duration_ticks is not None:
        bedrock_particle_json["minecraft:particle_effect"]["components"]["minecraft:emitter_lifetime_once"] = {
            "active_time": emitter_duration_ticks
        }
        if "minecraft:emitter_lifetime_expression" in bedrock_particle_json["minecraft:particle_effect"]["components"]:
            del bedrock_particle_json["minecraft:particle_effect"]["components"]["minecraft:emitter_lifetime_expression"]
    elif emitter_lifetime_type == "continuous":
        if "minecraft:emitter_lifetime_once" in bedrock_particle_json["minecraft:particle_effect"]["components"]:
            del bedrock_particle_json["minecraft:particle_effect"]["components"]["minecraft:emitter_lifetime_once"]
        bedrock_particle_json["minecraft:particle_effect"]["components"]["minecraft:emitter_lifetime_expression"] = {
            "activation_expression": "1", 
            "expiration_expression": "1" 
        }


    # Add color interpolation if start and end colors are different OR alpha transition is enabled
    if (start_r, start_g, start_b) != (end_r, end_g, end_b) or start_alpha != end_alpha:
        bedrock_particle_json["minecraft:particle_effect"]["components"]["minecraft:particle_appearance_tinting"] = {
            "color": {
                "interpolant": "query.life_time / query.particle_lifetime",
                "grad_color": [
                    [start_r, start_g, start_b, start_alpha], 
                    [end_r, end_g, end_b, end_alpha] 
                ]
            }
        }
    else: 
        bedrock_particle_json["minecraft:particle_effect"]["components"]["minecraft:particle_appearance_tinting"] = {
            "color": [start_r, start_g, start_b, start_alpha]
        }
    
    # Add lighting component if enabled 
    if lighting_var.get(): 
        bedrock_particle_json["minecraft:particle_effect"]["components"]["minecraft:particle_appearance_lighting"] = {}
    else:
        if "minecraft:particle_appearance_lighting" in bedrock_particle_json["minecraft:particle_effect"]["components"]:
            del bedrock_particle_json["minecraft:particle_effect"]["components"]["minecraft:particle_appearance_lighting"]


    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title=get_localized_text("save_bedrock_particle_json_title") 
    )
    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(bedrock_particle_json, f, indent=4)
            messagebox.showinfo(get_localized_text("export_successful"), f"{get_localized_text('particle_settings_saved')}\n{file_path}\n\n{get_localized_text('basic_template_note')}")
        except Exception as e:
            messagebox.showerror(get_localized_text("export_error"), f"{get_localized_text('failed_to_save_json')} {e}")


def toggle_advanced_view():
    """Toggles the visibility of advanced settings frames. / قابلیت مشاهده فریم‌های تنظیمات پیشرفته را تغییر می‌دهد."""
    if show_advanced_var.get():
        advanced_settings_frame.grid()
        custom_particle_frame.grid()
        advanced_rendering_frame.grid() 
    else:
        advanced_settings_frame.grid_remove()
        custom_particle_frame.grid_remove()
        advanced_rendering_frame.grid_remove() 
    update_extra_params_ui() 
    root.after(100, lambda: main_canvas.configure(scrollregion = main_canvas.bbox("all"))) 

def on_canvas_resize(event):
    """Adjusts the width of the scrollable frame when the canvas is resized. / عرض فریم قابل اسکرول را هنگام تغییر اندازه کانواس تنظیم می‌کند."""
    main_canvas.itemconfig(scrollable_frame_id, width=event.width)
    main_canvas.configure(scrollregion=main_canvas.bbox("all")) 

# --- Main Window Setup ---
root = tk.Tk()
root.title(get_localized_text("app_title")) 
root.geometry("1000x950") 
root.minsize(900, 700) 
root.resizable(True, True) 

# --- Styling (Dark Theme for a beautiful and user-friendly interface) ---
root.tk_setPalette(background='#2C2F33', foreground='#DCDCDC',
                    activeBackground='#505359', activeForeground='#FFFFFF')
style = ttk.Style()
style.theme_use('clam')

# Configure specific styles for a more modern look
style.configure("TLabel", background='#2C2F33', foreground='#DCDCDC', font=('Arial', 11))
style.configure("TButton", background='#7289DA', foreground='#FFFFFF', font=('Arial', 11, 'bold'), borderwidth=0, relief="flat", padding=10)
style.map("TButton", background=[('active', '#6778C2')])
style.configure("TEntry", fieldbackground='#40444B', foreground='#DCDCDC', insertbackground='#DCDCDC', borderwidth=0, padding=5)
style.configure("TCombobox", fieldbackground='#40444B', foreground='#DCDCDC', selectbackground='#7289DA', selectforeground='#FFFFFF', borderwidth=0, padding=5)
style.map('TCombobox', fieldbackground=[('readonly', '#40444B')], background=[('readonly', '#40444B')])
style.configure("TRadiobutton", background='#2C2F33', foreground='#DCDCDC', font=('Arial', 10))
style.configure("TFrame", background='#2C2F33')
style.configure("TLabelframe", background='#2C2F33', foreground='#DCDCDC', font=('Arial', 12, 'bold'), borderwidth=2, relief="groove")
style.configure("TLabelframe.Label", background='#2C2F33', foreground='#DCDCDC', font=('Arial', 12, 'bold'))
style.configure("Horizontal.TScale", background='#2C2F33', troughcolor='#40444B', sliderrelief="flat", sliderthickness=15)
style.configure("TCheckbutton", background='#2C2F33', foreground='#DCDCDC', font=('Arial', 10))
style.map("TCheckbutton", background=[('active', '#2C2F33')])


# --- Create a Canvas for scrollability ---
main_canvas = tk.Canvas(root, background='#2C2F33', highlightthickness=0)
main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=main_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

main_canvas.configure(yscrollcommand=scrollbar.set)
main_canvas.bind('<Configure>', on_canvas_resize) 
main_canvas.bind_all('<MouseWheel>', lambda e: main_canvas.yview_scroll(int(-1*(e.delta/120)), "units")) 

# Create a frame inside the canvas to hold all content
scrollable_frame = ttk.Frame(main_canvas, padding="20 20 20 20", relief="flat", style="TFrame")
scrollable_frame_id = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") 

# Configure column to expand horizontally
scrollable_frame.grid_columnconfigure(1, weight=1)


# --- Language Selection ---
language_frame = ttk.Frame(scrollable_frame)
language_frame.grid(row=0, column=2, sticky="ne", padx=5, pady=5)

ttk.Label(language_frame, text=get_localized_text("language_label")).pack(side="left", padx=5)
language_var = tk.StringVar(root)
language_var.set("en") 
language_options = ["en", "fa"]
language_combobox = ttk.Combobox(language_frame, textvariable=language_var, values=language_options, state="readonly", width=5)
language_combobox.pack(side="left", padx=5)
language_combobox.bind("<<ComboboxSelected>>", lambda event: set_language(language_var.get()))
language_combobox._tooltip = ToolTip(language_combobox, "language_tooltip")
language_sensitive_widgets.append((language_combobox, "language_label", "language_tooltip"))


# --- Basic Particle Settings Frame ---
basic_settings_frame = ttk.LabelFrame(scrollable_frame, text=get_localized_text("basic_settings_frame_title"), padding="15 15 15 15")
basic_settings_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
basic_settings_frame.grid_columnconfigure(1, weight=1) # Make second column expandable

# Particle Type Selection 
ttk.Label(basic_settings_frame, text=get_localized_text("particle_type_label")).grid(row=0, column=0, sticky="w", pady=5, padx=5)
particle_types = [
    "minecraft:flame", "minecraft:heart", "minecraft:smoke",
    "minecraft:explosion", "minecraft:lava", "minecraft:redstone",
    "minecraft:end_rod", "minecraft:totem_of_undying",
    "minecraft:dragon_breath", "minecraft:crit", "minecraft:enchant",
    "minecraft:sparkle", "minecraft:bubble", "minecraft:note",
    "minecraft:portal", "minecraft:falling_dust", 
    "minecraft:block",
    "minecraft:item",
    "minecraft:cloud", "minecraft:water_splash",
    "minecraft:drip_water", "minecraft:drip_lava", "minecraft:villager_happy",
    "minecraft:angry_villager", "minecraft:sweep_attack", "minecraft:sneeze",
    "minecraft:wax_on", "minecraft:wax_off", "minecraft:electric_spark",
    "minecraft:shriek",
    "minecraft:sculk_charge",
    "minecraft:sonic_boom",
    "minecraft:reverse_portal", "minecraft:white_ash", "minecraft:light",
    "minecraft:dust_color_transition",
    "minecraft:vibration",
    "minecraft:spore_blossom_air", "minecraft:squid_ink", "minecraft:glow",
    "minecraft:falling_lava", "minecraft:falling_water", "minecraft:composter",
    "minecraft:flash", "minecraft:soul", "minecraft:ash", "minecraft:warped_spore",
    "minecraft:cherry_leaves", "minecraft:sculk_soul", "minecraft:raid_omen",
    "minecraft:trial_omen", "minecraft:ominous_spawning"
]
particle_type_var = tk.StringVar(root)
particle_type_var.set(particle_types[0]) 
particle_type_menu = ttk.Combobox(basic_settings_frame, textvariable=particle_type_var, values=particle_types, state="readonly", width=35, font=('Arial', 10))
particle_type_menu.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
particle_type_menu.set("minecraft:flame") 
particle_type_menu.bind("<<ComboboxSelected>>", update_extra_params_ui)
particle_type_menu._tooltip = ToolTip(particle_type_menu, "particle_type_tooltip")
language_sensitive_widgets.append((particle_type_menu, "particle_type_label", "particle_type_tooltip"))

# Target Selector Input 
ttk.Label(basic_settings_frame, text=get_localized_text("target_selector_label")).grid(row=1, column=0, sticky="w", pady=5, padx=5)
target_selector_entry = ttk.Entry(basic_settings_frame, width=30, font=('Arial', 10))
target_selector_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
ttk.Label(basic_settings_frame, text=get_localized_text("target_selector_example"), font=('Arial', 9)).grid(row=1, column=2, sticky="w", padx=5)
target_selector_entry._tooltip = ToolTip(target_selector_entry, "target_selector_tooltip")
language_sensitive_widgets.append((target_selector_entry, "target_selector_label", "target_selector_tooltip"))
target_selector_entry.bind("<KeyRelease>", generate_command)


# Position (X, Y, Z) Inputs 
ttk.Label(basic_settings_frame, text=get_localized_text("position_label")).grid(row=2, column=0, sticky="w", pady=5, padx=5)
pos_frame = ttk.Frame(basic_settings_frame) 
pos_frame.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
x_pos_entry = ttk.Entry(pos_frame, width=10, font=('Arial', 10))
x_pos_entry.pack(side="left", padx=2, expand=True, fill="x")
y_pos_entry = ttk.Entry(pos_frame, width=10, font=('Arial', 10))
y_pos_entry.pack(side="left", padx=2, expand=True, fill="x")
z_pos_entry = ttk.Entry(pos_frame, width=10, font=('Arial', 10))
z_pos_entry.pack(side="left", padx=2, expand=True, fill="x")
ttk.Label(basic_settings_frame, text=get_localized_text("position_example"), font=('Arial', 9)).grid(row=2, column=2, sticky="w", padx=5)
x_pos_entry._tooltip = ToolTip(x_pos_entry, "pos_x_tooltip")
y_pos_entry._tooltip = ToolTip(y_pos_entry, "pos_y_tooltip")
z_pos_entry._tooltip = ToolTip(z_pos_entry, "pos_z_tooltip")
language_sensitive_widgets.extend([
    (x_pos_entry, "position_label", "pos_x_tooltip"),
    (y_pos_entry, None, "pos_y_tooltip"), # No direct label, but needs tooltip update
    (z_pos_entry, None, "pos_z_tooltip")  # No direct label, but needs tooltip update
])
x_pos_entry.insert(0, "~"); y_pos_entry.insert(0, "~"); z_pos_entry.insert(0, "~")
x_pos_entry.bind("<KeyRelease>", generate_command)
y_pos_entry.bind("<KeyRelease>", generate_command)
z_pos_entry.bind("<KeyRelease>", generate_command)


# --- Toggle Advanced View Button ---
show_advanced_var = tk.BooleanVar(value=True) 
toggle_advanced_button = ttk.Checkbutton(scrollable_frame, text=get_localized_text("show_advanced_settings_button"), variable=show_advanced_var, command=toggle_advanced_view)
toggle_advanced_button.grid(row=1, column=0, columnspan=3, pady=10)
language_sensitive_widgets.append((toggle_advanced_button, "show_advanced_settings_button", None))


# --- Advanced Particle Settings Frame ---
advanced_settings_frame = ttk.LabelFrame(scrollable_frame, text=get_localized_text("movement_spawn_settings_frame_title"), padding="15 15 15 15")
advanced_settings_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10, padx=5)
advanced_settings_frame.grid_columnconfigure(1, weight=1)

# Delta (Spread) Inputs 
ttk.Label(advanced_settings_frame, text=get_localized_text("delta_label")).grid(row=0, column=0, sticky="w", pady=5, padx=5)
delta_frame = ttk.Frame(advanced_settings_frame) 
delta_frame.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
x_delta_entry = ttk.Entry(delta_frame, width=10, font=('Arial', 10))
x_delta_entry.pack(side="left", padx=2, expand=True, fill="x")
y_delta_entry = ttk.Entry(delta_frame, width=10, font=('Arial', 10))
y_delta_entry.pack(side="left", padx=2, expand=True, fill="x")
z_delta_entry = ttk.Entry(delta_frame, width=10, font=('Arial', 10))
z_delta_entry.pack(side="left", padx=2, expand=True, fill="x")
ttk.Label(advanced_settings_frame, text=get_localized_text("delta_description"), font=('Arial', 9)).grid(row=0, column=2, sticky="w", padx=5)
x_delta_entry._tooltip = ToolTip(x_delta_entry, "delta_x_tooltip")
y_delta_entry._tooltip = ToolTip(y_delta_entry, "delta_y_tooltip")
z_delta_entry._tooltip = ToolTip(z_delta_entry, "delta_z_tooltip")
language_sensitive_widgets.extend([
    (x_delta_entry, "delta_label", "delta_x_tooltip"),
    (y_delta_entry, None, "delta_y_tooltip"),
    (z_delta_entry, None, "delta_z_tooltip")
])
x_delta_entry.insert(0, "0.0"); y_delta_entry.insert(0, "0.0"); z_delta_entry.insert(0, "0.0")
x_delta_entry.bind("<KeyRelease>", generate_command)
y_delta_entry.bind("<KeyRelease>", generate_command)
z_delta_entry.bind("<KeyRelease>", generate_command)

# Speed Input (Slider) 
ttk.Label(advanced_settings_frame, text=get_localized_text("speed_label")).grid(row=1, column=0, sticky="w", pady=5, padx=5)
speed_slider = ttk.Scale(advanced_settings_frame, from_=0.0, to=10.0, orient="horizontal", length=200, style="Horizontal.TScale", command=generate_command)
speed_slider.set(1.0) 
speed_slider.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
ttk.Label(advanced_settings_frame, text=get_localized_text("speed_description"), font=('Arial', 9)).grid(row=1, column=2, sticky="w", padx=5)
speed_slider._tooltip = ToolTip(speed_slider, "speed_tooltip")
language_sensitive_widgets.append((speed_slider, "speed_label", "speed_tooltip"))

# Count Input (Slider) 
ttk.Label(advanced_settings_frame, text=get_localized_text("count_label")).grid(row=2, column=0, sticky="w", pady=5, padx=5)
count_slider = ttk.Scale(advanced_settings_frame, from_=1, to=2000, orient="horizontal", length=200, style="Horizontal.TScale", command=generate_command) 
count_slider.set(1) 
count_slider.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
ttk.Label(advanced_settings_frame, text=get_localized_text("count_description"), font=('Arial', 9)).grid(row=2, column=2, sticky="w", padx=5)
count_slider._tooltip = ToolTip(count_slider, "count_tooltip")
language_sensitive_widgets.append((count_slider, "count_label", "count_tooltip"))

# Mode (Normal/Force) Selection 
ttk.Label(advanced_settings_frame, text=get_localized_text("display_mode_label")).grid(row=3, column=0, sticky="w", pady=5, padx=5)
mode_var = tk.StringVar(root)
mode_var.set("normal") 
mode_radio_normal = ttk.Radiobutton(advanced_settings_frame, text=get_localized_text("mode_normal"), variable=mode_var, value="normal", command=generate_command)
mode_radio_normal.grid(row=3, column=1, sticky="w", pady=2, padx=5)
mode_radio_force = ttk.Radiobutton(advanced_settings_frame, text=get_localized_text("mode_force"), variable=mode_var, value="force", command=generate_command)
mode_radio_force.grid(row=4, column=1, sticky="w", pady=2, padx=5)
mode_radio_normal._tooltip = ToolTip(mode_radio_normal, "mode_normal_tooltip")
mode_radio_force._tooltip = ToolTip(mode_radio_force, "mode_force_tooltip")
language_sensitive_widgets.extend([
    (mode_radio_normal, "display_mode_label", "mode_normal_tooltip"),
    (mode_radio_force, None, "mode_force_tooltip")
])

# Initial Linear Velocity (Motion) - 
linear_velocity_label = ttk.Label(advanced_settings_frame, text=get_localized_text("initial_velocity_label"))
linear_velocity_label.grid(row=5, column=0, sticky="w", pady=5, padx=5)
linear_velocity_frame = ttk.Frame(advanced_settings_frame)
linear_velocity_frame.grid(row=5, column=1, sticky="ew", pady=5, padx=5)
motion_x_entry = ttk.Entry(linear_velocity_frame, width=10, font=('Arial', 10)); motion_x_entry.pack(side="left", padx=2, expand=True, fill="x"); motion_x_entry.insert(0, "0.0")
motion_y_entry = ttk.Entry(linear_velocity_frame, width=10, font=('Arial', 10)); motion_y_entry.pack(side="left", padx=2, expand=True, fill="x"); motion_y_entry.insert(0, "0.0")
motion_z_entry = ttk.Entry(linear_velocity_frame, width=10, font=('Arial', 10)); motion_z_entry.pack(side="left", padx=2, expand=True, fill="x"); motion_z_entry.insert(0, "0.0")
motion_x_entry._tooltip = ToolTip(motion_x_entry, "motion_x_tooltip")
motion_y_entry._tooltip = ToolTip(motion_y_entry, "motion_y_tooltip")
motion_z_entry._tooltip = ToolTip(motion_z_entry, "motion_z_tooltip")
language_sensitive_widgets.extend([
    (linear_velocity_label, "initial_velocity_label", None),
    (motion_x_entry, None, "motion_x_tooltip"),
    (motion_y_entry, None, "motion_y_tooltip"),
    (motion_z_entry, None, "motion_z_tooltip")
])
motion_x_entry.bind("<KeyRelease>", generate_command)
motion_y_entry.bind("<KeyRelease>", generate_command)
motion_z_entry.bind("<KeyRelease>", generate_command)


# Gravity Modifier -
gravity_label = ttk.Label(advanced_settings_frame, text=get_localized_text("gravity_modifier_label"))
gravity_label.grid(row=6, column=0, sticky="w", pady=5, padx=5)
gravity_entry = ttk.Entry(advanced_settings_frame, width=10, font=('Arial', 10))
gravity_entry.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
gravity_entry.insert(0, "0.0")
gravity_entry._tooltip = ToolTip(gravity_entry, "gravity_tooltip")
language_sensitive_widgets.append((gravity_entry, "gravity_modifier_label", "gravity_tooltip"))
gravity_entry.bind("<KeyRelease>", generate_command)

# Collisions - 
collisions_var = tk.BooleanVar(value=False)
collisions_checkbox = ttk.Checkbutton(advanced_settings_frame, text=get_localized_text("enable_collisions_checkbox"), variable=collisions_var, command=generate_command)
collisions_checkbox.grid(row=7, column=0, columnspan=2, sticky="w", pady=5, padx=5)
collisions_checkbox._tooltip = ToolTip(collisions_checkbox, "collisions_tooltip")
language_sensitive_widgets.append((collisions_checkbox, "enable_collisions_checkbox", "collisions_tooltip"))

# Max Lifetime - 
max_lifetime_label = ttk.Label(advanced_settings_frame, text=get_localized_text("max_lifetime_label"))
max_lifetime_label.grid(row=8, column=0, sticky="w", pady=5, padx=5)
max_lifetime_entry = ttk.Entry(advanced_settings_frame, width=10, font=('Arial', 10))
max_lifetime_entry.grid(row=8, column=1, sticky="ew", pady=5, padx=5)
max_lifetime_entry.insert(0, "5.0")
max_lifetime_entry._tooltip = ToolTip(max_lifetime_entry, "max_lifetime_tooltip")
language_sensitive_widgets.append((max_lifetime_entry, "max_lifetime_label", "max_lifetime_tooltip"))
max_lifetime_entry.bind("<KeyRelease>", generate_command)

# Spawn Rate & Max Particles (for Bedrock Addon Export) -
spawn_rate_label = ttk.Label(advanced_settings_frame, text=get_localized_text("spawn_rate_label"))
spawn_rate_label.grid(row=9, column=0, sticky="w", pady=5, padx=5)
spawn_rate_entry = ttk.Entry(advanced_settings_frame, width=10, font=('Arial', 10))
spawn_rate_entry.grid(row=9, column=1, sticky="ew", pady=5, padx=5)
spawn_rate_entry.insert(0, "10")
spawn_rate_entry._tooltip = ToolTip(spawn_rate_entry, "spawn_rate_tooltip")
language_sensitive_widgets.append((spawn_rate_entry, "spawn_rate_label", "spawn_rate_tooltip"))
spawn_rate_entry.bind("<KeyRelease>", generate_command)

max_particles_label = ttk.Label(advanced_settings_frame, text=get_localized_text("max_particles_label"))
max_particles_label.grid(row=10, column=0, sticky="w", pady=5, padx=5)
max_particles_entry = ttk.Entry(advanced_settings_frame, width=10, font=('Arial', 10))
max_particles_entry.grid(row=10, column=1, sticky="ew", pady=5, padx=5)
max_particles_entry.insert(0, "100")
max_particles_entry._tooltip = ToolTip(max_particles_entry, "max_particles_tooltip")
language_sensitive_widgets.append((max_particles_entry, "max_particles_label", "max_particles_tooltip"))
max_particles_entry.bind("<KeyRelease>", generate_command)


# --- Dynamic Extra Parameters Frame (for specific particle types) ---
custom_particle_frame = ttk.LabelFrame(scrollable_frame, text=get_localized_text("particle_specific_data_frame_title"), padding="15 15 15 15")
custom_particle_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10, padx=5)
custom_particle_frame.grid_columnconfigure(1, weight=1)
language_sensitive_widgets.append((custom_particle_frame, "particle_specific_data_frame_title", None))

extra_params_dynamic_frame = ttk.Frame(custom_particle_frame)
extra_params_dynamic_frame.pack(fill="both", expand=True)
extra_params_dynamic_frame.grid_columnconfigure(1, weight=1)


# Specific entries/sliders for redstone particle 
ttk.Label(extra_params_dynamic_frame, text=get_localized_text("redstone_color_start_label")).grid(row=0, column=0, sticky="w", pady=2, padx=5)
red_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
red_slider.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
red_slider._tooltip = ToolTip(red_slider, "red_tooltip")
language_sensitive_widgets.append((red_slider, "redstone_color_start_label", "red_tooltip"))

ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('green_tooltip').split('(')[0].strip()} (0-1):").grid(row=1, column=0, sticky="w", pady=2, padx=5)
green_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
green_slider.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
green_slider._tooltip = ToolTip(green_slider, "green_tooltip")
language_sensitive_widgets.append((green_slider, None, "green_tooltip"))

ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('blue_tooltip').split('(')[0].strip()} (0-1):").grid(row=2, column=0, sticky="w", pady=2, padx=5)
blue_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
blue_slider.grid(row=2, column=1, sticky="ew", pady=2, padx=5)
blue_slider._tooltip = ToolTip(blue_slider, "blue_tooltip")
language_sensitive_widgets.append((blue_slider, None, "blue_tooltip"))

ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('size_tooltip').split('(')[0].strip()} (0-4):").grid(row=3, column=0, sticky="w", pady=2, padx=5)
size_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=4.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
size_slider.grid(row=3, column=1, sticky="ew", pady=2, padx=5)
size_slider._tooltip = ToolTip(size_slider, "size_tooltip")
language_sensitive_widgets.append((size_slider, None, "size_tooltip"))

ttk.Label(extra_params_dynamic_frame, text=get_localized_text("redstone_color_end_label")).grid(row=4, column=0, sticky="w", pady=2, padx=5)
end_red_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
end_red_slider.grid(row=4, column=1, sticky="ew", pady=2, padx=5)
end_red_slider._tooltip = ToolTip(end_red_slider, "red_tooltip") # Reusing for end color
language_sensitive_widgets.append((end_red_slider, "redstone_color_end_label", "red_tooltip"))

ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('green_tooltip').split('(')[0].strip()} (0-1):").grid(row=5, column=0, sticky="w", pady=2, padx=5)
end_green_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
end_green_slider.grid(row=5, column=1, sticky="ew", pady=2, padx=5)
end_green_slider._tooltip = ToolTip(end_green_slider, "green_tooltip")
language_sensitive_widgets.append((end_green_slider, None, "green_tooltip"))

ttk.Label(extra_params_dynamic_frame, text=f"{get_localized_text('blue_tooltip').split('(')[0].strip()} (0-1):").grid(row=6, column=0, sticky="w", pady=2, padx=5)
end_blue_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
end_blue_slider.grid(row=6, column=1, sticky="ew", pady=2, padx=5)
end_blue_slider._tooltip = ToolTip(end_blue_slider, "blue_tooltip")
language_sensitive_widgets.append((end_blue_slider, None, "blue_tooltip"))


# Specific entry for block/item particles 
block_item_id_entry = ttk.Entry(extra_params_dynamic_frame, width=30, font=('Arial', 10))
block_item_id_entry.bind("<KeyRelease>", generate_command)
block_item_id_entry._tooltip = ToolTip(block_item_id_entry, "block_item_id_tooltip")
language_sensitive_widgets.append((block_item_id_entry, "block_item_id_label", "block_item_id_tooltip"))

# Specific entries/sliders for dust_color_transition particle
from_red_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
from_red_slider._tooltip = ToolTip(from_red_slider, "from_red_tooltip")
language_sensitive_widgets.append((from_red_slider, None, "from_red_tooltip"))

from_green_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
from_green_slider._tooltip = ToolTip(from_green_slider, "from_green_tooltip")
language_sensitive_widgets.append((from_green_slider, None, "from_green_tooltip"))

from_blue_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
from_blue_slider._tooltip = ToolTip(from_blue_slider, "from_blue_tooltip")
language_sensitive_widgets.append((from_blue_slider, None, "from_blue_tooltip"))

to_red_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
to_red_slider._tooltip = ToolTip(to_red_slider, "to_red_tooltip")
language_sensitive_widgets.append((to_red_slider, None, "to_red_tooltip"))

to_green_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
to_green_slider._tooltip = ToolTip(to_green_slider, "to_green_tooltip")
language_sensitive_widgets.append((to_green_slider, None, "to_green_tooltip"))

to_blue_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=1.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
to_blue_slider._tooltip = ToolTip(to_blue_slider, "to_blue_tooltip")
language_sensitive_widgets.append((to_blue_slider, None, "to_blue_tooltip"))

size_transition_slider = ttk.Scale(extra_params_dynamic_frame, from_=0.0, to=4.0, orient="horizontal", length=150, style="Horizontal.TScale", command=generate_command)
size_transition_slider._tooltip = ToolTip(size_transition_slider, "size_transition_tooltip")
language_sensitive_widgets.append((size_transition_slider, None, "size_transition_tooltip"))


# Specific entries for vibration particle 
vibration_x_entry = ttk.Entry(extra_params_dynamic_frame, width=10, font=('Arial', 10))
vibration_y_entry = ttk.Entry(extra_params_dynamic_frame, width=10, font=('Arial', 10))
vibration_z_entry = ttk.Entry(extra_params_dynamic_frame, width=10, font=('Arial', 10))
arrival_ticks_entry = ttk.Entry(extra_params_dynamic_frame, width=10, font=('Arial', 10))
vibration_x_entry.bind("<KeyRelease>", generate_command)
vibration_y_entry.bind("<KeyRelease>", generate_command)
vibration_z_entry.bind("<KeyRelease>", generate_command)
arrival_ticks_entry.bind("<KeyRelease>", generate_command)
language_sensitive_widgets.extend([
    (vibration_x_entry, "dest_x_label", "vibration_x_tooltip"),
    (vibration_y_entry, "dest_y_label", "vibration_y_tooltip"),
    (vibration_z_entry, "dest_z_label", "vibration_z_tooltip"),
    (arrival_ticks_entry, "arrival_ticks_label", "arrival_ticks_tooltip")
])

# Specific entry for sculk_charge particle 
sculk_roll_entry = ttk.Entry(extra_params_dynamic_frame, width=10, font=('Arial', 10))
sculk_roll_entry.bind("<KeyRelease>", generate_command)
sculk_roll_entry._tooltip = ToolTip(sculk_roll_entry, "roll_tooltip")
language_sensitive_widgets.append((sculk_roll_entry, "roll_label", "roll_tooltip"))

# Specific entry for shriek particle 
shriek_delay_entry = ttk.Entry(extra_params_dynamic_frame, width=10, font=('Arial', 10))
shriek_delay_entry.bind("<KeyRelease>", generate_command)
shriek_delay_entry._tooltip = ToolTip(shriek_delay_entry, "delay_tooltip")
language_sensitive_widgets.append((shriek_delay_entry, "delay_label", "delay_tooltip"))

# Specific entry for falling_dust particle 
falling_dust_block_state_entry = ttk.Entry(extra_params_dynamic_frame, width=30, font=('Arial', 10))
falling_dust_block_state_entry.bind("<KeyRelease>", generate_command)
falling_dust_block_state_entry._tooltip = ToolTip(falling_dust_block_state_entry, "block_state_tooltip")
language_sensitive_widgets.append((falling_dust_block_state_entry, "block_state_label", "block_state_tooltip"))


# Generic Extra Parameters Input 
extra_params_label = ttk.Label(extra_params_dynamic_frame, text=get_localized_text("generic_extra_params_label"))
extra_params_entry = tk.Text(extra_params_dynamic_frame, width=40, height=4, font=('Arial', 10), background='#40444B', foreground='#DCDCDC', insertbackground='#DCDCDC', borderwidth=0, relief="flat", padx=5, pady=5)
extra_params_help_label = ttk.Label(extra_params_dynamic_frame, text=get_localized_text("generic_extra_params_help"), justify=tk.LEFT, font=('Arial', 9))
extra_params_entry._tooltip = ToolTip(extra_params_entry, "generic_extra_params_tooltip")
language_sensitive_widgets.extend([
    (extra_params_label, "generic_extra_params_label", None),
    (extra_params_entry, None, "generic_extra_params_tooltip"),
    (extra_params_help_label, "generic_extra_params_help", None)
])
extra_params_entry.bind("<KeyRelease>", generate_command)


# --- Advanced Rendering & Behavior Frame ---
advanced_rendering_frame = ttk.LabelFrame(scrollable_frame, text=get_localized_text("advanced_rendering_frame_title"), padding="15 15 15 15")
advanced_rendering_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10, padx=5)
advanced_rendering_frame.grid_columnconfigure(1, weight=1)
language_sensitive_widgets.append((advanced_rendering_frame, "advanced_rendering_frame_title", None))

# Custom Texture Path 
texture_path_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("custom_texture_path_label"))
texture_path_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)
texture_path_entry = ttk.Entry(advanced_rendering_frame, width=40, font=('Arial', 10))
texture_path_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
texture_path_entry._tooltip = ToolTip(texture_path_entry, "custom_texture_path_tooltip")
language_sensitive_widgets.append((texture_path_entry, "custom_texture_path_label", "custom_texture_path_tooltip"))
texture_path_entry.bind("<KeyRelease>", generate_command)

# UV Coordinates 
uv_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("uv_coordinates_label"))
uv_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)
uv_frame = ttk.Frame(advanced_rendering_frame)
uv_frame.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
uv_u_entry = ttk.Entry(uv_frame, width=8, font=('Arial', 10)); uv_u_entry.pack(side="left", padx=2, expand=True, fill="x"); uv_u_entry.insert(0, "0")
uv_v_entry = ttk.Entry(uv_frame, width=8, font=('Arial', 10)); uv_v_entry.pack(side="left", padx=2, expand=True, fill="x"); uv_v_entry.insert(0, "0")
uv_w_entry = ttk.Entry(uv_frame, width=8, font=('Arial', 10)); uv_w_entry.pack(side="left", padx=2, expand=True, fill="x"); uv_w_entry.insert(0, "16")
uv_h_entry = ttk.Entry(uv_frame, width=8, font=('Arial', 10)); uv_h_entry.pack(side="left", padx=2, expand=True, fill="x"); uv_h_entry.insert(0, "16")
uv_u_entry._tooltip = ToolTip(uv_u_entry, "uv_u_tooltip")
uv_v_entry._tooltip = ToolTip(uv_v_entry, "uv_v_tooltip")
uv_w_entry._tooltip = ToolTip(uv_w_entry, "uv_w_tooltip")
uv_h_entry._tooltip = ToolTip(uv_h_entry, "uv_h_tooltip")
language_sensitive_widgets.extend([
    (uv_label, "uv_coordinates_label", None),
    (uv_u_entry, None, "uv_u_tooltip"),
    (uv_v_entry, None, "uv_v_tooltip"),
    (uv_w_entry, None, "uv_w_tooltip"),
    (uv_h_entry, None, "uv_h_tooltip")
])
uv_u_entry.bind("<KeyRelease>", generate_command)
uv_v_entry.bind("<KeyRelease>", generate_command)
uv_w_entry.bind("<KeyRelease>", generate_command)
uv_h_entry.bind("<KeyRelease>", generate_command)

# Rotation and Angular Velocity 
rotation_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("initial_roll_label"))
rotation_label.grid(row=2, column=0, sticky="w", pady=5, padx=5)
roll_slider = ttk.Scale(advanced_rendering_frame, from_=0.0, to=2*math.pi, orient="horizontal", length=200, style="Horizontal.TScale", command=generate_command)
roll_slider.set(0.0) 
roll_slider.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
roll_slider._tooltip = ToolTip(roll_slider, "initial_roll_tooltip")
language_sensitive_widgets.append((roll_slider, "initial_roll_label", "initial_roll_tooltip"))

angular_velocity_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("angular_velocity_label"))
angular_velocity_label.grid(row=3, column=0, sticky="w", pady=5, padx=5)
angular_velocity_entry = ttk.Entry(advanced_rendering_frame, width=10, font=('Arial', 10))
angular_velocity_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
angular_velocity_entry.insert(0, "0.0")
angular_velocity_entry._tooltip = ToolTip(angular_velocity_entry, "angular_velocity_tooltip")
language_sensitive_widgets.append((angular_velocity_entry, "angular_velocity_label", "angular_velocity_tooltip"))
angular_velocity_entry.bind("<KeyRelease>", generate_command)

# Lighting Control 
lighting_var = tk.BooleanVar(value=True) 
lighting_checkbox = ttk.Checkbutton(advanced_rendering_frame, text=get_localized_text("affected_by_lighting_checkbox"), variable=lighting_var, command=generate_command)
lighting_checkbox.grid(row=10, column=0, columnspan=2, sticky="w", pady=5, padx=5)
lighting_checkbox._tooltip = ToolTip(lighting_checkbox, "lighting_tooltip")
language_sensitive_widgets.append((lighting_checkbox, "affected_by_lighting_checkbox", "lighting_tooltip"))

# Linear Drag Coefficient  
linear_drag_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("linear_drag_label"))
linear_drag_label.grid(row=11, column=0, sticky="w", pady=5, padx=5)
linear_drag_entry = ttk.Entry(advanced_rendering_frame, width=10, font=('Arial', 10))
linear_drag_entry.grid(row=11, column=1, sticky="ew", pady=5, padx=5)
linear_drag_entry.insert(0, "0.0")
linear_drag_entry._tooltip = ToolTip(linear_drag_entry, "linear_drag_tooltip")
language_sensitive_widgets.append((linear_drag_entry, "linear_drag_label", "linear_drag_tooltip"))
linear_drag_entry.bind("<KeyRelease>", generate_command)

# Collision Resilience  
collision_resilience_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("collision_resilience_label"))
collision_resilience_label.grid(row=12, column=0, sticky="w", pady=5, padx=5)
collision_resilience_entry = ttk.Entry(advanced_rendering_frame, width=10, font=('Arial', 10))
collision_resilience_entry.grid(row=12, column=1, sticky="ew", pady=5, padx=5)
collision_resilience_entry.insert(0, "0.0")
collision_resilience_entry._tooltip = ToolTip(collision_resilience_entry, "collision_resilience_tooltip")
language_sensitive_widgets.append((collision_resilience_entry, "collision_resilience_label", "collision_resilience_tooltip"))
collision_resilience_entry.bind("<KeyRelease>", generate_command)

# Collision Radius  
collision_radius_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("collision_radius_label"))
collision_radius_label.grid(row=13, column=0, sticky="w", pady=5, padx=5)
collision_radius_entry = ttk.Entry(advanced_rendering_frame, width=10, font=('Arial', 10))
collision_radius_entry.grid(row=13, column=1, sticky="ew", pady=5, padx=5)
collision_radius_entry.insert(0, "0.1")
collision_radius_entry._tooltip = ToolTip(collision_radius_entry, "collision_radius_tooltip")
language_sensitive_widgets.append((collision_radius_entry, "collision_radius_label", "collision_radius_tooltip"))
collision_radius_entry.bind("<KeyRelease>", generate_command)


# Spawn Offset 
spawn_offset_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("spawn_offset_label"))
spawn_offset_label.grid(row=14, column=0, sticky="w", pady=5, padx=5)
spawn_offset_frame = ttk.Frame(advanced_rendering_frame)
spawn_offset_frame.grid(row=14, column=1, sticky="ew", pady=5, padx=5)
spawn_offset_x_entry = ttk.Entry(spawn_offset_frame, width=8, font=('Arial', 10)); spawn_offset_x_entry.pack(side="left", padx=2, expand=True, fill="x"); spawn_offset_x_entry.insert(0, "0.0")
spawn_offset_y_entry = ttk.Entry(spawn_offset_frame, width=8, font=('Arial', 10)); spawn_offset_y_entry.pack(side="left", padx=2, expand=True, fill="x"); spawn_offset_y_entry.insert(0, "0.0")
spawn_offset_z_entry = ttk.Entry(spawn_offset_frame, width=8, font=('Arial', 10)); spawn_offset_z_entry.pack(side="left", padx=2, expand=True, fill="x"); spawn_offset_z_entry.insert(0, "0.0")
spawn_offset_x_entry._tooltip = ToolTip(spawn_offset_x_entry, "spawn_offset_tooltip")
spawn_offset_y_entry._tooltip = ToolTip(spawn_offset_y_entry, "spawn_offset_tooltip")
spawn_offset_z_entry._tooltip = ToolTip(spawn_offset_z_entry, "spawn_offset_tooltip")
language_sensitive_widgets.extend([
    (spawn_offset_label, "spawn_offset_label", None),
    (spawn_offset_x_entry, None, "spawn_offset_tooltip"),
    (spawn_offset_y_entry, None, "spawn_offset_tooltip"),
    (spawn_offset_z_entry, None, "spawn_offset_tooltip")
])
spawn_offset_x_entry.bind("<KeyRelease>", generate_command)
spawn_offset_y_entry.bind("<KeyRelease>", generate_command)
spawn_offset_z_entry.bind("<KeyRelease>", generate_command)

# Size Over Lifetime  
size_over_lifetime_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("size_over_lifetime_label"))
size_over_lifetime_label.grid(row=15, column=0, sticky="w", pady=5, padx=5)
size_over_lifetime_frame = ttk.Frame(advanced_rendering_frame)
size_over_lifetime_frame.grid(row=15, column=1, sticky="ew", pady=5, padx=5)
ttk.Label(size_over_lifetime_frame, text=get_localized_text("start_size_label")).pack(side="left", padx=2)
size_over_lifetime_start_entry = ttk.Entry(size_over_lifetime_frame, width=8, font=('Arial', 10)); size_over_lifetime_start_entry.pack(side="left", padx=2, expand=True, fill="x"); size_over_lifetime_start_entry.insert(0, "1.0")
ttk.Label(size_over_lifetime_frame, text=get_localized_text("end_size_label")).pack(side="left", padx=2)
size_over_lifetime_end_entry = ttk.Entry(size_over_lifetime_frame, width=8, font=('Arial', 10)); size_over_lifetime_end_entry.pack(side="left", padx=2, expand=True, fill="x"); size_over_lifetime_end_entry.insert(0, "1.0")
size_over_lifetime_start_entry._tooltip = ToolTip(size_over_lifetime_start_entry, "start_size_tooltip")
size_over_lifetime_end_entry._tooltip = ToolTip(size_over_lifetime_end_entry, "end_size_tooltip")
language_sensitive_widgets.extend([
    (size_over_lifetime_label, "size_over_lifetime_label", None),
    (size_over_lifetime_start_entry, "start_size_label", "start_size_tooltip"),
    (size_over_lifetime_end_entry, "end_size_label", "end_size_tooltip")
])
size_over_lifetime_start_entry.bind("<KeyRelease>", generate_command)
size_over_lifetime_end_entry.bind("<KeyRelease>", generate_command)

# Alpha Over Lifetime 
alpha_over_lifetime_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("alpha_over_lifetime_label"))
alpha_over_lifetime_label.grid(row=16, column=0, sticky="w", pady=5, padx=5)
alpha_over_lifetime_frame = ttk.Frame(advanced_rendering_frame)
alpha_over_lifetime_frame.grid(row=16, column=1, sticky="ew", pady=5, padx=5)
ttk.Label(alpha_over_lifetime_frame, text=get_localized_text("start_alpha_label")).pack(side="left", padx=2)
alpha_over_lifetime_start_entry = ttk.Entry(alpha_over_lifetime_frame, width=8, font=('Arial', 10)); alpha_over_lifetime_start_entry.pack(side="left", padx=2, expand=True, fill="x"); alpha_over_lifetime_start_entry.insert(0, "1.0")
ttk.Label(alpha_over_lifetime_frame, text=get_localized_text("end_alpha_label")).pack(side="left", padx=2)
alpha_over_lifetime_end_entry = ttk.Entry(alpha_over_lifetime_frame, width=8, font=('Arial', 10)); alpha_over_lifetime_end_entry.pack(side="left", padx=2, expand=True, fill="x"); alpha_over_lifetime_end_entry.insert(0, "1.0")
alpha_over_lifetime_start_entry._tooltip = ToolTip(alpha_over_lifetime_start_entry, "start_alpha_tooltip")
alpha_over_lifetime_end_entry._tooltip = ToolTip(alpha_over_lifetime_end_entry, "end_alpha_tooltip")
language_sensitive_widgets.extend([
    (alpha_over_lifetime_label, "alpha_over_lifetime_label", None),
    (alpha_over_lifetime_start_entry, "start_alpha_label", "start_alpha_tooltip"),
    (alpha_over_lifetime_end_entry, "end_alpha_label", "end_alpha_tooltip")
])
alpha_over_lifetime_start_entry.bind("<KeyRelease>", generate_command)
alpha_over_lifetime_end_entry.bind("<KeyRelease>", generate_command)

# Emitter Lifetime 
emitter_lifetime_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("emitter_lifetime_label"))
emitter_lifetime_label.grid(row=17, column=0, sticky="w", pady=5, padx=5)
emitter_lifetime_frame = ttk.Frame(advanced_rendering_frame)
emitter_lifetime_frame.grid(row=17, column=1, sticky="ew", pady=5, padx=5)
emitter_lifetime_var = tk.StringVar(root, value="continuous")
emitter_lifetime_radio_continuous = ttk.Radiobutton(emitter_lifetime_frame, text=get_localized_text("emitter_lifetime_continuous"), variable=emitter_lifetime_var, value="continuous", command=update_extra_params_ui)
emitter_lifetime_radio_continuous.pack(side="left", padx=5)
emitter_lifetime_radio_once = ttk.Radiobutton(emitter_lifetime_frame, text=get_localized_text("emitter_lifetime_once"), variable=emitter_lifetime_var, value="once", command=update_extra_params_ui)
emitter_lifetime_radio_once.pack(side="left", padx=5)
language_sensitive_widgets.extend([
    (emitter_lifetime_label, "emitter_lifetime_label", None),
    (emitter_lifetime_radio_continuous, "emitter_lifetime_continuous", None),
    (emitter_lifetime_radio_once, "emitter_lifetime_once", None)
])

emitter_duration_label = ttk.Label(advanced_rendering_frame, text=get_localized_text("emitter_duration_label"))
emitter_duration_entry = ttk.Entry(advanced_rendering_frame, width=10, font=('Arial', 10))
emitter_duration_entry.insert(0, "20")
emitter_duration_entry._tooltip = ToolTip(emitter_duration_entry, "emitter_duration_tooltip")
language_sensitive_widgets.append((emitter_duration_entry, "emitter_duration_label", "emitter_duration_tooltip"))
emitter_duration_entry.bind("<KeyRelease>", generate_command)


# --- Action Buttons ---
action_buttons_frame = ttk.Frame(scrollable_frame)
action_buttons_frame.grid(row=5, column=0, columnspan=3, pady=25)

generate_button = ttk.Button(action_buttons_frame, text=get_localized_text("generate_command_button"), command=generate_command)
generate_button.pack(side="left", padx=10)
language_sensitive_widgets.append((generate_button, "generate_command_button", None))

clear_button = ttk.Button(action_buttons_frame, text=get_localized_text("clear_fields_button"), command=clear_fields)
clear_button.pack(side="left", padx=10)
language_sensitive_widgets.append((clear_button, "clear_fields_button", None))

copy_button = ttk.Button(action_buttons_frame, text=get_localized_text("copy_command_button"), command=copy_command)
copy_button.pack(side="left", padx=10)
language_sensitive_widgets.append((copy_button, "copy_command_button", None))

export_json_button = ttk.Button(action_buttons_frame, text=get_localized_text("export_command_json_button"), command=export_to_json)
export_json_button.pack(side="left", padx=10)
language_sensitive_widgets.append((export_json_button, "export_command_json_button", None))

export_addon_button = ttk.Button(action_buttons_frame, text=get_localized_text("export_bedrock_addon_button"), command=export_as_bedrock_addon)
export_addon_button.pack(side="left", padx=10)
language_sensitive_widgets.append((export_addon_button, "export_bedrock_addon_button", None))


# --- Command Output Display ---
ttk.Label(scrollable_frame, text=get_localized_text("final_command_label"), font=('Arial', 12, 'bold')).grid(row=6, column=0, sticky="w", pady=10, padx=5)
command_output = ttk.Entry(scrollable_frame, width=70, font=('Arial', 10))
command_output.grid(row=6, column=1, columnspan=2, sticky="ew", pady=10, padx=5)
language_sensitive_widgets.append((command_output, "final_command_label", None))


# --- How to Use Section ---
how_to_use_frame = ttk.LabelFrame(scrollable_frame, text=get_localized_text("how_to_use_frame_title"), padding="15 15 15 15")
how_to_use_frame.grid(row=7, column=0, columnspan=3, sticky="ew", pady=10, padx=5)
language_sensitive_widgets.append((how_to_use_frame, "how_to_use_frame_title", None))

ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_intro"), wraplength=850, justify="left").pack(anchor="w", pady=5)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step1_title")).pack(anchor="w", pady=2, padx=5)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step1_desc"), wraplength=850, justify="left").pack(anchor="w", padx=15)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step2_title")).pack(anchor="w", pady=2, padx=5)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step2_desc"), wraplength=850, justify="left").pack(anchor="w", padx=15)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step3_title")).pack(anchor="w", pady=2, padx=5)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step3a_title")).pack(anchor="w", pady=2, padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step3a_desc"), wraplength=850, justify="left").pack(anchor="w", padx=35)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step3b_title")).pack(anchor="w", pady=2, padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step3b_desc"), wraplength=850, justify="left").pack(anchor="w", padx=35)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_title")).pack(anchor="w", pady=5, padx=5)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_structure"), wraplength=850, justify="left", font=('Arial', 10, 'bold')).pack(anchor="w", padx=15)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_type"), wraplength=850, justify="left").pack(anchor="w", padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_pos"), wraplength=850, justify="left").pack(anchor="w", padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_delta"), wraplength=850, justify="left").pack(anchor="w", padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_speed"), wraplength=850, justify="left").pack(anchor="w", padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_count"), wraplength=850, justify="left").pack(anchor="w", padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_mode"), wraplength=850, justify="left").pack(anchor="w", padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step4_parameters"), wraplength=850, justify="left").pack(anchor="w", padx=25)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step5_title")).pack(anchor="w", pady=5, padx=5)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step5_cmd_not_working"), wraplength=850, justify="left").pack(anchor="w", padx=15)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step5_no_particles"), wraplength=850, justify="left").pack(anchor="w", padx=15)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step5_lag"), wraplength=850, justify="left").pack(anchor="w", padx=15)
ttk.Label(how_to_use_frame, text=get_localized_text("how_to_use_step5_addon_not_showing"), wraplength=850, justify="left").pack(anchor="w", padx=15)


# --- Signature ---
signature_label = ttk.Label(root, text=get_localized_text("signature"), font=('Arial', 9, 'italic'), foreground='#6C7A89')
signature_label.pack(side="bottom", pady=10) 
language_sensitive_widgets.append((signature_label, "signature", None))


# --- Initial UI Update ---
set_language("en") # Set initial language and update all texts
update_extra_params_ui()

# --- Run the application ---
root.mainloop()
