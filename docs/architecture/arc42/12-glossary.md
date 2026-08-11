# 12. Glossary

## Domain Terms (Game Concepts)

| Term | Definition |
|---|---|
| **Obstgarten** | The German children's board game by HABA on which Fruit Garden is based. English title: "First Orchard." The physical game is the specification for the digital version. |
| **Raven** | The player's opponent. Moves across the field one step at a time. If it reaches the orchard (gate) before all fruit is harvested, the player loses. |
| **Orchard** | The fruit garden; the destination the raven is advancing towards. In the digital game, represented as trees spread across the board (top-left, top-right, bottom-right, bottom-left quadrants). |
| **Tree** | A tree in the orchard bearing fruit of one colour (red, yellow, green, or blue in the physical game; typically red apple, pear, plum, green apple in variations). In the digital game, trees are pure visual elements with no behaviour (see Chapter 5). |
| **Field** | A path tile along which the raven walks. In the digital game, four fields form the raven's path running horizontally from the left edge towards the gate on the right. |
| **Gate** | The boundary marker on the right-hand side of the screen, at the far end of the raven's path, marking the orchard's entrance. When the raven reaches the gate, the player loses. |
| **Basket roll** | The outcome when the die shows the basket face. Allows the player to harvest one fruit of their choice (in the physical game) or a random fruit (in the digital game; see Chapter 11, finding 3). |
| **Harvest** | To remove fruit from the orchard and add it to the basket. In the digital game, this removes the fruit from the corresponding list. |
| **Win condition** | The player wins if they harvest all fruit before the raven reaches the gate. In the digital game, this is checked by testing if all four fruit lists are empty (Chapter 6, step 5). |
| **Loss condition** | The player loses if the raven reaches the gate before all fruit is harvested. In the digital game, this is checked by testing if `raven.picPosX > 648` (Chapter 6, step 5). Since the raven starts at x=10 and moves +130 pixels per roll, this threshold is reached exactly at the fifth raven roll (10→140→270→400→530→660), though this number is never declared in the code—it falls out of the geometry (see Chapter 11, finding 1). |

## Technical Terms (As Used in This Codebase)

| Term | Definition |
|---|---|
| **Element** | The base class for all visible game objects (`main.py:29–40`). Owns an image, position (in pixels), size, and a `drawPicture()` method. Subclassed by `Raven`, `Fruit`, `Basket`, and `Dice`. The design choice to use sprites (visual elements) as the primary abstraction, rather than domain objects (game concepts), is the root of the architecture's coupling. |
| **draftResult** | A module-level variable (`main.py:21`) that stores the outcome of the last die roll as a string: `"red"`, `"green"`, `"yellow"`, `"blue"`, `"raven"`, `"basket"`, or `"none"`. Persists across frames until the next roll. Used to display the rolled result and to apply the rule. See Chapter 11, finding 2. |
| **Sprite-as-entity** | The architectural choice to represent every game concept as a visual sprite first, with rules as a secondary concern. The raven is a sprite positioned at X pixels; its progress towards the orchard is implicit in the pixel coordinate. The fruit are sprites removed from lists; the win condition is the absence of sprites. This conflates rendering and domain logic (see Chapter 11, finding 1). |
| **Immediate-mode rendering** | The rendering approach used in Fruit Garden: every frame, the entire screen is cleared and redrawn from scratch (no dirty tracking, no partial updates). Each frame is independent. This is simple and correct but can be inefficient (see Chapter 11, finding 12). |
| **Game loop** | The main control flow of the game (`main.py:250–358`). Runs once per frame: collect input → apply rules → check outcomes → render. Runs 60 times per second. See Chapter 6. |
| **Name mangling** | A Python feature that prefixes private attributes (those starting with `__`) with the class name to prevent accidental external access. `Element.__pictureWidth` becomes `_Element__pictureWidth` in the compiled code. The `Dice` class violates this encapsulation by directly reading `self._Element__pictureWidth` (see Chapter 11, finding 6). |
| **Onedir bundle** | A PyInstaller output format: a directory containing the packaged executable, all runtime dependencies (DLLs, Python interpreter, frozen standard library), and optionally data files. The opposite is `onefile`, which bundles everything into a single `.exe`. |
| **convert_alpha()** | A pygame method that converts an image surface to an internal format optimized for transparency and blitting. Called by `Element.__init__` (line 32) and requires an initialised pygame display (window). See Chapter 5 for the ordering coupling this creates. |
| **PyInstaller `datas`** | A configuration option in `main.spec` (a list of tuples) specifying additional files or directories to include in the packaged bundle. Currently set to `datas=[]`, excluding `pics/`, which is a bug (see Chapter 11, finding 5). |
| **Render pass** | The phase of the game loop that draws the frame to the screen (`main.py:324–358`). Clears the screen, draws all sprites, flips the buffer, and enforces the frame rate. |
| **Rule block** | The part of the game loop that applies game logic based on player input (`main.py:265–313`). Contains the fruit harvesting logic, raven movement, and the fallback chains for basket rolls. See Chapter 11, findings 2, 3, and 10. |
