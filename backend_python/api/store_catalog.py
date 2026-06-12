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
    'crimson-ember': {
        'key': 'crimson-ember', 'kind': 'theme', 'name': 'Crimson Ember',
        'description': 'Smoldering reds and warm coals for fearless late-night grinders.',
        'price': 500, 'rarity': 'rare', 'animated': False,
        'swatches': ['#7F1D1D', '#DC2626', '#F87171', '#FECACA'],
    },
    'ocean-depth': {
        'key': 'ocean-depth', 'kind': 'theme', 'name': 'Ocean Depth',
        'description': 'Dive into deep marine blues with bright cyan currents.',
        'price': 500, 'rarity': 'rare', 'animated': False,
        'swatches': ['#0C4A6E', '#0369A1', '#0EA5E9', '#BAE6FD'],
    },
    'mono-ink': {
        'key': 'mono-ink', 'kind': 'theme', 'name': 'Mono Ink',
        'description': 'A distraction-free monochrome ink palette for pure focus.',
        'price': 400, 'rarity': 'rare', 'animated': False,
        'swatches': ['#111827', '#374151', '#9CA3AF', '#F3F4F6'],
    },
    'obsidian-gold': {
        'key': 'obsidian-gold', 'kind': 'theme', 'name': 'Obsidian Gold',
        'description': 'Jet-black volcanic glass trimmed with molten gold luxury.',
        'price': 900, 'rarity': 'epic', 'animated': False,
        'swatches': ['#0B0B0F', '#1F2937', '#D97706', '#FCD34D'],
    },
    'cosmic-nebula': {
        'key': 'cosmic-nebula', 'kind': 'theme', 'name': 'Cosmic Nebula',
        'description': 'Violet and magenta stardust swirling across the whole site.',
        'price': 1200, 'rarity': 'legendary', 'animated': True,
        'swatches': ['#1E1B4B', '#7C3AED', '#EC4899', '#C4B5FD'],
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
    'ink-brush': {
        'key': 'ink-brush', 'kind': 'banner', 'name': 'Ink Brush',
        'description': 'Minimal sumi-e ink washes sweeping across rice paper.',
        'price': 400, 'rarity': 'rare', 'animated': False,
        'deco_text': 'ink', 'deco_color': 'rgba(243, 244, 246, 0.16)',
        'card_text': 'INK', 'card_rgb1': (31, 41, 55), 'card_rgb2': (107, 114, 128),
    },
    'koi-pond': {
        'key': 'koi-pond', 'kind': 'banner', 'name': 'Koi Pond',
        'description': 'Tranquil teal waters with drifting ripples of light.',
        'price': 450, 'rarity': 'rare', 'animated': True,
        'deco_text': 'koi', 'deco_color': 'rgba(204, 251, 241, 0.18)',
        'card_text': 'KOI', 'card_rgb1': (13, 148, 136), 'card_rgb2': (56, 189, 248),
    },
    'topo-contour': {
        'key': 'topo-contour', 'kind': 'banner', 'name': 'Topo Contour',
        'description': 'Elevation contour lines mapped over deep evergreen terrain.',
        'price': 650, 'rarity': 'epic', 'animated': False,
        'deco_text': 'explore', 'deco_color': 'rgba(209, 250, 229, 0.16)',
        'card_text': 'EXPLORE', 'card_rgb1': (6, 78, 59), 'card_rgb2': (16, 185, 129),
    },
    'pixel-meadow': {
        'key': 'pixel-meadow', 'kind': 'banner', 'name': 'Pixel Meadow',
        'description': 'An 8-bit meadow with pixel clouds rolling through a spring sky.',
        'price': 750, 'rarity': 'epic', 'animated': True,
        'deco_text': 'pixel', 'deco_color': 'rgba(220, 252, 231, 0.18)',
        'card_text': 'PIXEL', 'card_rgb1': (34, 197, 94), 'card_rgb2': (56, 189, 248),
    },
    'molten-core': {
        'key': 'molten-core', 'kind': 'banner', 'name': 'Molten Core',
        'description': 'Magma veins pulsing through cooling volcanic rock.',
        'price': 800, 'rarity': 'epic', 'animated': True,
        'deco_text': 'molten', 'deco_color': 'rgba(254, 215, 170, 0.18)',
        'card_text': 'MOLTEN', 'card_rgb1': (153, 27, 27), 'card_rgb2': (249, 115, 22),
    },
    'prism-cascade': {
        'key': 'prism-cascade', 'kind': 'banner', 'name': 'Prism Cascade',
        'description': 'A legendary waterfall of holographic light split into pure spectrum.',
        'price': 1100, 'rarity': 'legendary', 'animated': True,
        'deco_text': 'prism', 'deco_color': 'rgba(255, 255, 255, 0.20)',
        'card_text': 'PRISM', 'card_rgb1': (99, 102, 241), 'card_rgb2': (236, 72, 153),
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
    'sakura-ring': {
        'key': 'sakura-ring', 'kind': 'border', 'name': 'Sakura Ring',
        'description': 'Soft cherry-blossom petals circling your avatar.',
        'price': 400, 'rarity': 'rare', 'animated': False,
    },
    'frost-halo': {
        'key': 'frost-halo', 'kind': 'border', 'name': 'Frost Halo',
        'description': 'A crystalline ring of glacial ice and winter light.',
        'price': 400, 'rarity': 'rare', 'animated': False,
    },
    'ocean-swirl': {
        'key': 'ocean-swirl', 'kind': 'border', 'name': 'Ocean Swirl',
        'description': 'Rolling teal and azure currents in endless motion.',
        'price': 500, 'rarity': 'rare', 'animated': True,
    },
    'royal-laurel': {
        'key': 'royal-laurel', 'kind': 'border', 'name': 'Royal Laurel',
        'description': 'Regal purple and gold laurels worthy of forum royalty.',
        'price': 650, 'rarity': 'epic', 'animated': False,
    },
    'galaxy-orbit': {
        'key': 'galaxy-orbit', 'kind': 'border', 'name': 'Galaxy Orbit',
        'description': 'A comet of starlight orbiting a deep-space ring.',
        'price': 950, 'rarity': 'legendary', 'animated': True,
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
    'quiz-whiz': {
        'key': 'quiz-whiz', 'kind': 'badge', 'name': 'Quiz Whiz',
        'description': 'Lightning-fast answers, first-try accuracy.',
        'price': 350, 'rarity': 'rare', 'animated': False,
        'icon': 'quiz', 'color': '#14B8A6',
    },
    'helping-hand': {
        'key': 'helping-hand', 'kind': 'badge', 'name': 'Helping Hand',
        'description': 'Always there when a fellow NEBian needs a boost.',
        'price': 350, 'rarity': 'rare', 'animated': False,
        'icon': 'volunteer_activism', 'color': '#EC4899',
    },
    'summit-seeker': {
        'key': 'summit-seeker', 'kind': 'badge', 'name': 'Summit Seeker',
        'description': 'Climbing every syllabus peak, one chapter at a time.',
        'price': 400, 'rarity': 'rare', 'animated': False,
        'icon': 'landscape', 'color': '#0284C7',
    },
    'golden-quill': {
        'key': 'golden-quill', 'kind': 'badge', 'name': 'Golden Quill',
        'description': 'For writers whose notes read like literature.',
        'price': 600, 'rarity': 'epic', 'animated': True,
        'icon': 'ink_pen', 'color': '#D97706',
    },
    'cosmic-comet': {
        'key': 'cosmic-comet', 'kind': 'badge', 'name': 'Cosmic Comet',
        'description': 'A streak of brilliance blazing across the leaderboard.',
        'price': 700, 'rarity': 'epic', 'animated': True,
        'icon': 'rocket_launch', 'color': '#8B5CF6',
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
