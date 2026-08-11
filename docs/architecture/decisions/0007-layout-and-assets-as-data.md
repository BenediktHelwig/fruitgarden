# 0007. Layout and assets as data

* Status: proposed
* Date: 2026-08-11
* Deciders: Developer (author)

## Context and Problem Statement

Two habits in the presentation code, both cheap to fix once a presentation layer exists [0001].

(a) Positional coupling: all game objects are built at module scope in five near-identical `for i in range(0,4)` loops. Each loop carries its position table inside the loop body as `if i == 0: posX = ...` through `if i == 3: ...`. To move one apple you edit one conditional branch; to shift all four you edit the same expression four times and hope not to miss one. Adding an object means adding another loop and another table.

(b) Per-frame disk I/O: the render pass calls `pygame.image.load("pics/" + draftResult + ".png")` every frame — sixty file reads per second for an image that changes only when the die is rolled. The end-game loop constructs `pygame.font.SysFont("comicsansms", 40)` inside the loop, building a font sixty times a second to draw a word that never changes.

There is also a hidden ordering coupling worth recording: `Element.__init__` calls `.convert_alpha()`, which requires an initialised display, so `pygame.display.set_mode(...)` must run before any object is constructed. Nothing in the source says so; construct an element one line earlier and the program crashes.

## Decision Drivers

* Quality goal 1 (learnability): coordinates are data and should look like data
* The ordering coupling is invisible and a maintenance trap; a cache with an explicit initialisation point makes it visible

## Considered Options

* A `Layout` module holding coordinates as plain data, and an `AssetCache` loading every image and font once at startup
* Keep the loops but extract the coordinates into module-level constants
* Move the layout into an external configuration file (JSON/TOML)

## Decision Outcome

Chosen option: "Layout module and AssetCache for one-time loading", because this makes coordinates visible as data and eliminates repeated I/O.

* `presentation/layout.py` holds the positions as data — a table per element kind, each entry a coordinate pair, expressed relative to the window size as today. Building the sprites becomes one loop over the table, with no conditionals
* `presentation/asset_cache.py` loads every PNG in pics/ and every font once, after the display is created, and hands them out by name. The point at which assets may first be loaded becomes an explicit, named step instead of an accident of line order
* `presentation/sprite.py` exposes the sprite's bounds as a public property. This retires the name-mangling in today's `Dice.overDice()`, which reads `self._Element__pictureWidth` and `self._Element__pictureHeight` — reaching through the parent class's private namespace because `Element` hides what a hit test legitimately needs

Rejected option 2: constants without a table still need one loop per kind. Rejected option 3: an external file adds a parsing step, a file-not-found path and a schema to a game whose layout changes roughly never; it also puts the layout outside the reach of the type checker.

### Positive Consequences

* Moving an element is editing one row; adding a fruit sort is adding rows
* Sixty image loads and sixty font constructions per second disappear
* The display-before-construction coupling becomes explicit
* Encapsulation of `Sprite` is no longer bypassed

### Negative Consequences

* Startup does slightly more work before the first frame
* A new place to keep in sync when an asset is added

## More Information

Resolves chapter 11 findings 6, 11 and 12. The asset naming contract stays as it is — every element name maps to `pics/<name>.png`. Related: [0001](0001-separate-domain-model-from-presentation.md), [0002](0002-one-class-per-file.md).
