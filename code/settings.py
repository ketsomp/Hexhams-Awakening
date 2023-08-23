# game setup
WIDTH    = 1280	
HEIGHT   = 720
FPS      = 60
TILESIZE = 128
BLACK = (0, 0, 0)
WHITE= (255, 255, 255)

HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0,
    '200':0,
    '0':50,'01':100,'02':50,'16':100,'17':100,'22':100,'25':20,'36':15,'39':15,'40':0,'49':10,'58':0,'59':0,'67':15,'71':0,'73':15,'75':15,'93':30,'94':30,'105':30,'106':30,'107':100}
X_HITBOX_OFFSET={
    '200':0,
    '0':50,'01':100,'02':50,'16':100,'17':100,'22':100,'25':50,'36':20,'39':16,'40':5,'49':10,'58':10,'59':10,'67':25,'71':10,'73':15,'75':20,'93':30,'94':30,'105':30,'106':30,'107':100}


SPEED_OFFSET=1.5

#ui
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
BAR_HEIGHT = 20
HOTBOX_SIZE = 80

#logo
LOGO_FONT='../graphics/font/magnific_chaos.ttf'
LOGO_FONT_COLOR='#FFBC00'

# general colors
BG_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
 
# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
STAMINA_COLOR='yellow'
UI_BORDER_COLOR_ACTIVE = 'gold'
XP_COLOR=(109, 232, 102)

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons 
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphic':'../graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
    'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'}}

# projectiles
proj_data = {
    'spike': {'strength': 5,'cost': 20,'graphic':'../graphics/projectiles/knife.png'},
    'hp_potion' : {'strength': 20,'cost': 10,'graphic':'../graphics/projectiles/hp_potion.png'}}

# enemies
monster_data = {
    'skeleton': {'health': 300,'xp':250,'damage':40,'attack_type': 'slash', 'attack_sound':'../audio/attack/claw.wav', 'speed': 2, 'resistance': 4, 'attack_radius': 100, 'aggro_radius': 400,'atk_delay':10},
    'mushroom': {'health': 100,'xp':100,'damage':20,'attack_type': 'slash',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 100, 'aggro_radius': 360,'atk_delay':400},
    'goblin': {'health': 100,'xp':110,'damage':8,'attack_type': 'claw', 'attack_sound':'../audio/attack/claw.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 100, 'aggro_radius': 350,'atk_delay':300},
    'flying_eye': {'health': 70,'xp':120,'damage':6,'attack_type': 'thunder', 'attack_sound':'../audio/attack/slash.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 100, 'aggro_radius': 300,'atk_delay':200}}