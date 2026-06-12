"""Cosmetics store catalog — themes, profile banners, avatar borders, and flair badges."""


def _item(item_id, item_type, name, description, price, rarity, **extra):
    item = {
        'id': item_id,
        'type': item_type,
        'name': name,
        'description': description,
        'price': price,
        'rarity': rarity,
    }
    item.update(extra)
    return item


_ITEMS = [
    _item('liquid-glass', 'theme', 'Liquid Glass',
          'Frosted translucent surfaces with a cool sky-blue shimmer.',
          500, 'legendary', preview=['#7dd3fc', '#e0f2fe', '#a5b4fc', '#f0f9ff']),
    _item('midnight-neon', 'theme', 'Midnight Neon',
          'Deep space purples cut by electric cyan and pink.',
          350, 'epic', preview=['#0f0c29', '#7c3aed', '#06b6d4', '#f472b6']),
    _item('emerald-forest', 'theme', 'Emerald Forest',
          'Calm greens straight from a misty Nepali forest.',
          0, 'common', preview=['#065f46', '#10b981', '#a7f3d0', '#f0fdf4']),
    _item('sakura-bloom', 'theme', 'Sakura Bloom',
          'Soft cherry-blossom pinks for a gentle study mood.',
          200, 'rare', preview=['#be185d', '#f472b6', '#fbcfe8', '#fff1f2']),
    _item('solar-amber', 'theme', 'Solar Amber',
          'Warm golden tones like late-afternoon sunlight.',
          200, 'rare', preview=['#92400e', '#f59e0b', '#fde68a', '#fffbeb']),
    _item('nord-frost', 'theme', 'Nord Frost',
          'Muted arctic blues with a crisp, frosty calm.',
          250, 'rare', preview=['#2e3440', '#5e81ac', '#88c0d0', '#eceff4']),
    _item('royal-gold', 'theme', 'Royal Gold',
          'Midnight black and gleaming gold for those who study like royalty.',
          400, 'epic', preview=['#1c1917', '#a16207', '#fbbf24', '#fef3c7']),

    _item('store-aurora-flow', 'banner', 'Aurora Flow',
          'Northern lights drifting slowly across your profile.',
          250, 'rare', deco_text='aurora', text_color='rgba(255,255,255,0.22)'),
    _item('store-pixel-sunset', 'banner', 'Pixel Sunset',
          'A retro 8-bit sunset sinking behind pixel mountains.',
          300, 'epic', deco_text='pixel', text_color='rgba(255,255,255,0.30)'),
    _item('store-starfield', 'banner', 'Starfield',
          'A quiet sweep of stars across a deep night sky.',
          250, 'rare', deco_text='cosmos', text_color='rgba(255,255,255,0.20)'),
    _item('store-synthwave-grid', 'banner', 'Synthwave',
          'Neon gridlines racing toward a retro horizon.',
          300, 'epic', deco_text='retro', text_color='rgba(255,255,255,0.25)'),
    _item('store-liquid-glass', 'banner', 'Glass Orbs',
          'Floating glass orbs catching soft prismatic light.',
          350, 'epic', deco_text='glass', text_color='rgba(255,255,255,0.28)'),
    _item('store-geo-mosaic', 'banner', 'Geo Mosaic',
          'Clean geometric tiles in classic NEBians blue.',
          0, 'common', deco_text='nebian', text_color='rgba(255,255,255,0.25)'),
    _item('store-ember-noir', 'banner', 'Ember Noir',
          'Smouldering embers glowing through the dark.',
          250, 'rare', deco_text='ember', text_color='rgba(255,255,255,0.18)'),

    _item('border-classic-ring', 'border', 'Classic Ring',
          'A clean, timeless ring around your avatar.',
          0, 'common'),
    _item('border-gradient-pulse', 'border', 'Gradient Pulse',
          'A smooth color gradient that pulses with energy.',
          200, 'rare'),
    _item('border-neon-ring', 'border', 'Neon Ring',
          'An electric neon glow circling your avatar.',
          250, 'rare'),
    _item('border-orbit', 'border', 'Orbit',
          'A tiny satellite endlessly orbiting your avatar.',
          250, 'rare'),
    _item('border-gold-luxe', 'border', 'Gold Luxe',
          'Lustrous gold trim for an unmistakably premium look.',
          300, 'epic'),
    _item('border-pixel-frame', 'border', 'Pixel Frame',
          'A chunky retro pixel frame straight from the arcade.',
          300, 'epic'),
    _item('border-holo-prism', 'border', 'Holo Prism',
          'A holographic prism shifting through rainbow hues.',
          350, 'epic'),

    _item('badge-sprout', 'badge', 'Sprout',
          'A fresh sprout for learners just getting started.',
          0, 'common', icon='potted_plant'),
    _item('badge-night-owl', 'badge', 'Night Owl',
          'For those who do their best studying after midnight.',
          100, 'common', icon='dark_mode'),
    _item('badge-bolt', 'badge', 'Bolt',
          'Quick answers and lightning-fast thinking.',
          100, 'common', icon='bolt'),
    _item('badge-heart', 'badge', 'Heart',
          'Spread the love, one thumbs-up at a time.',
          100, 'common', icon='favorite'),
    _item('badge-founder-star', 'badge', 'Star',
          'A shining star for standout NEBians.',
          150, 'rare', icon='star'),
    _item('badge-flame', 'badge', 'Flame',
          'Keep the streak alive and the flame burning.',
          150, 'rare', icon='local_fire_department'),
    _item('badge-crystal', 'badge', 'Crystal',
          'Rare clarity and crystal-sharp focus.',
          150, 'rare', icon='diamond'),
]

STORE_ITEMS = {item['id']: item for item in _ITEMS}

CATEGORY_LABELS = [
    ('theme', 'Themes'),
    ('banner', 'Profile Banners'),
    ('border', 'Avatar Borders'),
    ('badge', 'Flair Badges'),
]


def get_item(item_id):
    if not item_id:
        return None
    return STORE_ITEMS.get(item_id)


def items_by_type(item_type):
    return [item for item in STORE_ITEMS.values() if item['type'] == item_type]


def all_categories():
    return [
        {'type': item_type, 'label': label, 'items': items_by_type(item_type)}
        for item_type, label in CATEGORY_LABELS
    ]
