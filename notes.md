# TODO
- implement dictionary
- test on 32x32
- blacklist broken leds

# Related Ideas
### Constellations
- Random flickering of stars until a constellation forms
    - the name of the constellation also fades in
- Integrate Planets with a zooming effect on a colored star, followed by text underneath
    - begin with 64x64 still images of planets
    - bake the scaling animation if possible
    - text with planets name (only if text looks good)
- Stars' displacement can have a jitter as well as brightness.
- These would need to be on 64x64!

# Future Efficiency
- Baking stars and planet zoom-ins to a file on bootup, then just display bake. perfect loop?