"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path



SAMPLES = (
    Path(__file__).parent
    .joinpath('samples'))



STATE_PHIDS = [

    ('e693d3a2-f4ef-36de'
     '-a583-e4fcc23f8f7c'),

    ('da4c6a04-c9e8-4915'
     '-9818-0f898029a1e8')]

STATE_PATHS = [

    ('https://192.168.1.10'
     '/clip/v2/resource'
     '/grouped_light'
     f'/{STATE_PHIDS[0]}'),

    ('https://192.168.2.10'
     '/clip/v2/resource'
     '/grouped_light'
     f'/{STATE_PHIDS[1]}')]



LEVEL_PHIDS = STATE_PHIDS

LEVEL_PATHS = [

    ('https://192.168.1.10'
     '/clip/v2/resource'
     '/grouped_light'
     f'/{LEVEL_PHIDS[0]}'),

    ('https://192.168.2.10'
     '/clip/v2/resource'
     '/grouped_light'
     f'/{LEVEL_PHIDS[1]}')]



SCENE_PHIDS = [

    ('5808a516-aab3-3ec3'
     '-8eee-4db5152b07b5'),

    ('9678ff8b-d452-49f3'
     '-861c-74e5c5b2ca7c')]

SCENE_PATHS = [

    ('https://192.168.1.10'
     '/clip/v2/resource/scene'
     f'/{SCENE_PHIDS[0]}'),

    ('https://192.168.2.10'
     '/clip/v2/resource/scene'
     f'/{SCENE_PHIDS[1]}')]
