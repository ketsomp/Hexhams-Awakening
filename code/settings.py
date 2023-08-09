# game setup
WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60
TILESIZE = 64
BLACK = (0, 0, 0)

#ui
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
BAR_HEIGHT = 20
HOTBOX_SIZE = 80

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
 
# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
XP_COLOR=(109, 232, 102)

# weapons 
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphic':'../graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
    'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'}}