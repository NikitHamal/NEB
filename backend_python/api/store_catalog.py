"""
Cosmetics store catalog — single source of truth for all purchasable items.
Prices are in contribution points; price 0 means free to claim.
"""

RARITIES = ('common', 'rare', 'epic', 'legendary')
KINDS = ('theme', 'banner', 'border', 'badge')

CATALOG = {
    'emerald-forest': {
        'key': 'emerald-forest', 'kind': 'theme', 'name': 'Emerald Forest',
        'description': 'Lose yourself in deep greens and calm woodland tones.',
        'price': 0, 'rarity': 'common', 'animated': False,
        'swatches': ['#064E3B', '#047857', '#10B981', '#A7F3D0'],
    },
    'solar-dawn': {
        'key': 'solar-dawn', 'kind': 'theme', 'name': 'Solar Dawn',
        'description': 'Warm amber sunrise hues to kick-start every study session.',
        'price': 400, 'rarity': 'rare', 'animated': False,
        'swatches': ['#7C2D12', '#EA580C', '#F59E0B', '#FDE68A'],
    },
    'sakura-bloom': {
        'key': 'sakura-bloom', 'kind': 'theme', 'name': 'Sakura Bloom',
        'description': 'Soft cherry-blossom pinks for a gentle, focused vibe.',
        'price': 500, 'rarity': 'rare', 'animated': False,
        'swatches': ['#831843', '#DB2777', '#F472B6', '#FCE7F3'],
    },
    'everest-mist': {
        'key': 'everest-mist', 'kind': 'theme', 'name': 'Everest Mist',
        'description': 'Cool slate and teal inspired by Himalayan morning mist.',
        'price': 500, 'rarity': 'rare', 'animated': False,
        'swatches': ['#1E293B', '#334155', '#0D9488', '#CCFBF1'],
    },
    'royal-amethyst': {
        'key': 'royal-amethyst', 'kind': 'theme', 'name': 'Royal Amethyst',
        'description': 'Regal purple and gold for scholars with refined taste.',
        'price': 800, 'rarity': 'epic', 'animated': False,
        'swatches': ['#4C1D95', '#7C3AED', '#A78BFA', '#F59E0B'],
    },
    'midnight-neon': {
        'key': 'midnight-neon', 'kind': 'theme', 'name': 'Midnight Neon',
        'description': 'Cyberpunk cyan and magenta glowing through the dark.',
        'price': 800, 'rarity': 'epic', 'animated': True,
        'swatches': ['#0F172A', '#06B6D4', '#D946EF', '#22D3EE'],
    },
    'liquid-glass': {
        'key': 'liquid-glass', 'kind': 'theme', 'name': 'Liquid Glass',
        'description': 'The flagship: frosted translucent layers with real depth and blur.',
        'price': 1500, 'rarity': 'legendary', 'animated': True,
        'swatches': ['#E0F2FE', '#BAE6FD', '#7DD3FC', '#C7D2FE'],
    },
    'gradient-sunset': {
        'key': 'gradient-sunset', 'kind': 'banner', 'name': 'Sunset Glow',
        'description': 'A blazing orange-red gradient that never sets.',
        'price': 0, 'rarity': 'common', 'animated': True,
        'deco_text': 'nebian', 'deco_color': 'rgba(255, 237, 213, 0.18)',
        'card_text': 'NEBIAN', 'card_rgb1': (234, 88, 12), 'card_rgb2': (190, 24, 93),
    },
    'gradient-ocean': {
        'key': 'gradient-ocean', 'kind': 'banner', 'name': 'Ocean Drift',
        'description': 'Sky blues flowing into deep cyan waves.',
        'price': 250, 'rarity': 'common', 'animated': True,
        'deco_text': 'nebian', 'deco_color': 'rgba(224, 242, 254, 0.18)',
        'card_text': 'NEBIAN', 'card_rgb1': (14, 116, 184), 'card_rgb2': (8, 145, 178),
    },
    'gradient-aurora': {
        'key': 'gradient-aurora', 'kind': 'banner', 'name': 'Aurora Sky',
        'description': 'Emerald and cyan lights dancing across your profile.',
        'price': 350, 'rarity': 'rare', 'animated': True,
        'deco_text': 'nebian', 'deco_color': 'rgba(209, 250, 229, 0.18)',
        'card_text': 'NEBIAN', 'card_rgb1': (5, 150, 105), 'card_rgb2': (6, 182, 212),
    },
    'gradient-royal': {
        'key': 'gradient-royal', 'kind': 'banner', 'name': 'Royal Velvet',
        'description': 'Rich purples fit for forum royalty.',
        'price': 350, 'rarity': 'rare', 'animated': True,
        'deco_text': 'nebian', 'deco_color': 'rgba(237, 233, 254, 0.18)',
        'card_text': 'NEBIAN', 'card_rgb1': (91, 33, 182), 'card_rgb2': (124, 58, 237),
    },
    'gradient-champion': {
        'key': 'gradient-champion', 'kind': 'banner', 'name': 'Champion Gold',
        'description': 'Molten gold reserved for those who earn it.',
        'price': 600, 'rarity': 'epic', 'animated': True,
        'deco_text': 'champion', 'deco_color': 'rgba(254, 243, 199, 0.20)',
        'card_text': 'CHAMPION', 'card_rgb1': (180, 83, 9), 'card_rgb2': (245, 158, 11),
    },
    'geometric-waves': {
        'key': 'geometric-waves', 'kind': 'banner', 'name': 'Geometric Waves',
        'description': 'Crisp indigo-teal waves with a modern geometric rhythm.',
        'price': 400, 'rarity': 'rare', 'animated': True,
        'deco_text': 'nebian', 'deco_color': 'rgba(224, 231, 255, 0.16)',
        'card_text': 'NEBIAN', 'card_rgb1': (67, 56, 202), 'card_rgb2': (13, 148, 136),
    },
    'himalaya': {
        'key': 'himalaya', 'kind': 'banner', 'name': 'Himalaya',
        'description': 'Slate-blue peaks and glacial ice from the roof of the world.',
        'price': 450, 'rarity': 'rare', 'animated': True,
        'deco_text': 'himalaya', 'deco_color': 'rgba(226, 232, 240, 0.18)',
        'card_text': 'HIMALAYA', 'card_rgb1': (51, 65, 85), 'card_rgb2': (125, 211, 252),
    },
    'starfield': {
        'key': 'starfield', 'kind': 'banner', 'name': 'Starfield',
        'description': 'A deep navy cosmos scattered with violet starlight.',
        'price': 500, 'rarity': 'rare', 'animated': True,
        'deco_text': 'cosmos', 'deco_color': 'rgba(196, 181, 253, 0.16)',
        'card_text': 'COSMOS', 'card_rgb1': (15, 23, 42), 'card_rgb2': (109, 40, 217),
    },
    'synthwave-grid': {
        'key': 'synthwave-grid', 'kind': 'banner', 'name': 'Synthwave Grid',
        'description': 'Magenta horizon lines straight out of the retro future.',
        'price': 700, 'rarity': 'epic', 'animated': True,
        'deco_text': 'retro', 'deco_color': 'rgba(251, 207, 232, 0.18)',
        'card_text': 'RETRO', 'card_rgb1': (157, 23, 77), 'card_rgb2': (126, 34, 206),
    },
    'aurora-borealis': {
        'key': 'aurora-borealis', 'kind': 'banner', 'name': 'Aurora Borealis',
        'description': 'Green, teal, and violet curtains shimmering in polar night.',
        'price': 700, 'rarity': 'epic', 'animated': True,
        'deco_text': 'aurora', 'deco_color': 'rgba(204, 251, 241, 0.18)',
        'card_text': 'AURORA', 'card_rgb1': (16, 185, 129), 'card_rgb2': (139, 92, 246),
    },
    'pixel-sunset': {
        'key': 'pixel-sunset', 'kind': 'banner', 'name': 'Pixel Sunset',
        'description': 'An 8-bit sun melting into orange and purple pixels.',
        'price': 750, 'rarity': 'epic', 'animated': True,
        'deco_text': 'pixel', 'deco_color': 'rgba(255, 237, 213, 0.18)',
        'card_text': 'PIXEL', 'card_rgb1': (249, 115, 22), 'card_rgb2': (126, 34, 206),
    },
    'pixel-night': {
        'key': 'pixel-night', 'kind': 'banner', 'name': 'Pixel Night',
        'description': 'A neon-lit pixel city under a dark blue midnight sky.',
        'price': 750, 'rarity': 'epic', 'animated': True,
        'deco_text': 'pixel', 'deco_color': 'rgba(165, 243, 252, 0.16)',
        'card_text': 'PIXEL', 'card_rgb1': (30, 41, 59), 'card_rgb2': (34, 211, 238),
    },
    'liquid-flow': {
        'key': 'liquid-flow', 'kind': 'banner', 'name': 'Liquid Flow',
        'description': 'Iridescent glass currents of blue and violet in constant motion.',
        'price': 1000, 'rarity': 'legendary', 'animated': True,
        'deco_text': 'liquid', 'deco_color': 'rgba(219, 234, 254, 0.20)',
        'card_text': 'LIQUID', 'card_rgb1': (37, 99, 235), 'card_rgb2': (139, 92, 246),
    },
    'emerald-vine': {
        'key': 'emerald-vine', 'kind': 'border', 'name': 'Emerald Vine',
        'description': 'A living green vine wrapped around your avatar.',
        'price': 0, 'rarity': 'common', 'animated': False,
    },
    'glass-ring': {
        'key': 'glass-ring', 'kind': 'border', 'name': 'Glass Ring',
        'description': 'A sleek frosted-glass halo with a subtle shine.',
        'price': 400, 'rarity': 'rare', 'animated': False,
    },
    'neon-pulse': {
        'key': 'neon-pulse', 'kind': 'border', 'name': 'Neon Pulse',
        'description': 'An electric cyan ring that pulses with energy.',
        'price': 450, 'rarity': 'rare', 'animated': True,
    },
    'ember-flame': {
        'key': 'ember-flame', 'kind': 'border', 'name': 'Ember Flame',
        'description': 'Flickering embers that keep your avatar burning bright.',
        'price': 450, 'rarity': 'rare', 'animated': True,
    },
    'pixel-frame': {
        'key': 'pixel-frame', 'kind': 'border', 'name': 'Pixel Frame',
        'description': 'A chunky retro pixel border for old-school legends.',
        'price': 550, 'rarity': 'epic', 'animated': False,
    },
    'gold-radiance': {
        'key': 'gold-radiance', 'kind': 'border', 'name': 'Gold Radiance',
        'description': 'Shimmering golden rays radiating pure prestige.',
        'price': 600, 'rarity': 'epic', 'animated': True,
    },
    'holo-prism': {
        'key': 'holo-prism', 'kind': 'border', 'name': 'Holo Prism',
        'description': 'A holographic prism cycling through every color of light.',
        'price': 900, 'rarity': 'legendary', 'animated': True,
    },
    'book-worm': {
        'key': 'book-worm', 'kind': 'badge', 'name': 'Book Worm',
        'description': 'Proof that you devour notes faster than momos.',
        'price': 0, 'rarity': 'common', 'animated': False,
        'icon': 'auto_stories', 'color': '#10B981',
    },
    'night-owl': {
        'key': 'night-owl', 'kind': 'badge', 'name': 'Night Owl',
        'description': 'For the late-night grinders who study while the city sleeps.',
        'price': 300, 'rarity': 'rare', 'animated': False,
        'icon': 'bedtime', 'color': '#6366F1',
    },
    'star-scholar': {
        'key': 'star-scholar', 'kind': 'badge', 'name': 'Star Scholar',
        'description': 'Shine bright as a five-star student of the community.',
        'price': 400, 'rarity': 'rare', 'animated': False,
        'icon': 'hotel_class', 'color': '#F59E0B',
    },
    'pixel-pioneer': {
        'key': 'pixel-pioneer', 'kind': 'badge', 'name': 'Pixel Pioneer',
        'description': 'A retro-gaming heart beating inside a modern scholar.',
        'price': 450, 'rarity': 'rare', 'animated': False,
        'icon': 'videogame_asset', 'color': '#8B5CF6',
    },
    'flame-streak': {
        'key': 'flame-streak', 'kind': 'badge', 'name': 'Flame Streak',
        'description': 'Your study streak is officially on fire.',
        'price': 500, 'rarity': 'epic', 'animated': True,
        'icon': 'local_fire_department', 'color': '#F97316',
    },
    'diamond-mind': {
        'key': 'diamond-mind', 'kind': 'badge', 'name': 'Diamond Mind',
        'description': 'A flawless intellect, polished under pressure.',
        'price': 800, 'rarity': 'epic', 'animated': True,
        'icon': 'diamond', 'color': '#06B6D4',
    },
}


def get_item(key):
    return CATALOG.get(key)


def items_of_kind(kind):
    return [item for item in CATALOG.values() if item['kind'] == kind]


def valid_keys_for_kind(kind):
    return {item['key'] for item in CATALOG.values() if item['kind'] == kind}


def banner_card_style(key):
    item = CATALOG.get(key)
    if not item or item['kind'] != 'banner':
        return None
    return (item['card_text'], item['card_rgb1'], item['card_rgb2'])
