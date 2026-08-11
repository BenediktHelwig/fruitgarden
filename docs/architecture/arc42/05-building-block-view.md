# 5. Building Block View

## Level 1: System Whitebox

![Building Block View](../diagrams/building-blocks.drawio)

| Component | Responsibility | Contains |
|---|---|---|
| `main.py` | The entire runtime: startup, game loop, rules, rendering, and end-game sequence | Configuration, class definitions, world construction, game loop, end loop |
| `pics/` | Asset store; provides named images used as sprites | 15 PNG files: basket, dice, fruit, raven, trees, fields, gate, and the rolled result display |
| `module/objects.py` | **Not part of the runtime**; an orphaned attempt at a domain model (see "Intended versus actual" below) | Broken sketch classes: `Element`, `Tree`, `Fruit`, `Raven`, `Basket`, `Dice` |
| `main.spec` | PyInstaller build configuration | Python entry point, `hiddenimports=[]` (empty), `datas=[]` (empty, which is the defect in chapter 11, finding 5) |

## Level 2: main.py Whitebox

| Block | Responsibility | Lines |
|---|---|---|
| **Configuration & globals** | Constants, mutable state flags, and initial pygame setup | 1–25 |
| **Element hierarchy** | Base class `Element` and its subclasses `Raven`, `Fruit`, `Basket`, `Dice` | 29–78 |
| **World construction** | Instantiation of the raven, dice, fruit lists, trees, fields, gate, and basket at module scope | 81–241 |
| **Main game loop** | Input handling, rule application, outcome checks, rendering; runs once per frame | 250–358 |
| **End-game sequence** | Display of win/lose message; runs until player closes the window | 360–395 |
| **Cleanup** | Pygame shutdown and debug output | 397–398 |

### Configuration & Globals (Lines 1–25)

**Imports and initialisation**
- Lines 1–7: pygame, random, and local constants are imported; `pygame.init()` is called

**Window constants**
- `WINDOWWIDTH = 1080, WINDOWHEIGHT = 720` (line 10)
- `FPS = 60` (line 11)
- Colour tuples: WHITE, RED, GREEN, BLUE, YELLOW, GREY (lines 12–17)

**Mutable global state**
- `gameaktiv = True` (line 19): the play loop's exit condition
- `gameLost = False` (line 20): set to true when the loss condition is met
- `draftResult = "none"` (line 21): holds the last die roll result; initialised to `"none"`, which loads `pics/none.png` (a blank display)
- `ravenPosStart = 10` (line 22): passed as the raven's starting X coordinate at line 141

**Critical ordering coupling**
- Line 25: `screen = pygame.display.set_mode(...)` is called at module scope—before any `Element` is constructed. This is necessary because `Element.__init__` calls `.convert_alpha()` on the loaded image, which requires an initialised pygame display. If an `Element` is instantiated before this line, the code will crash. This coupling is invisible in the source and a maintenance hazard.

### Element Hierarchy (Lines 29–78)

**`Element` (base class, lines 29–40)**
- `__init__(name, posX, posY, width, height)` loads the image from `pics/<name>.png` and calls `.convert_alpha()` on it (requires an initialised display)
- Private attributes: `__name`, `__picture`, `__pictureWidth`, `__pictureHeight`, `__sizeOfPicture` (all derived from the loaded image)
- Public attributes: `picPosX`, `picPosY` (position in pixels)
- `drawPicture()` scales the image to the sprite's size and blits it to `screen` at the current position

**`Raven` (subclass, lines 42–48)**
- `moveForward()`: increments `self.picPosX += 130` (in pixels, moving one tile width on the game board)
- The raven's progress towards the orchard is stored solely as a pixel coordinate; the loss condition is implicit in the window geometry (see Chapter 11)

**`Fruit` (subclass, lines 50–53)**
- Sets `self.__amount = 4` in `__init__`, which is never read anywhere; the fruit count is stored in the module-level lists instead

**`Basket` (subclass, lines 55–57)**
- No additional behaviour; purely a visual element
- Contrast with the 2021 design, which had `Basket` managing `amount` (see "Intended versus actual" below)

**`Dice` (subclass, lines 59–78)**
- `__sign` dict (lines 62–68): maps die faces 1–6 to outcomes: red, green, yellow, blue, raven, basket
- `overDice(mousePos)` (lines 71–73): bounding-box hit test; **uses name mangling to read inherited private attributes** `self._Element__pictureWidth` and `self._Element__pictureHeight` (line 72; see Chapter 11, finding 6)
- `rollDice()` (lines 75–78): returns `self.__sign[random.randint(1,6)]`, a string like `"red"` or `"raven"`

### World Construction (Lines 81–241)

All game objects are instantiated at module scope. The structure is highly repetitive: five near-identical `for i in range(0,4)` blocks, each building one element type with position tables embedded as `if i == 0: … if i == 1: …` statements. This is duplicated positional coupling (see Chapter 11, finding 11).

Objects created (in order):
- Line 81: `dice`
- Line 83: `basket`
- Lines 85–105: `treeList` (4 `Fruit("tree", ...)` instances)
- Lines 109–129: `fieldList` (4 `Fruit("field", ...)` instances, the path tiles)
- Lines 133–138: `gate` (destination for the raven)
- Lines 140–145: `raven`
- Lines 147–169: `redAppleList` (4 `Fruit` each)
- Lines 171–193: `greenAppleList` (4 `Fruit` each)
- Lines 195–217: `plumList` (4 `Fruit` each)
- Lines 219–241: `pearList` (4 `Fruit` each)

Each list is built identically except for the asset name and position table. Trees and fields are `Fruit` objects with names `"tree"` and `"field"`, not distinct classes—they are pure visual elements.

### Main Game Loop (Lines 250–358)

The loop runs `while gameaktiv:` and has four phases each iteration:

**Phase 1: Input handling (lines 252–263)**
- `pygame.event.get()` collects all pending events
- `QUIT` or `ESC` → break and set `gameaktiv = False`
- `SPACE` → no-op (a test hook)
- `MOUSEBUTTONDOWN` → get mouse position; check if it hit the dice

**Phase 2: Rule application (lines 265–313)**
- **Critical:** the rule block (lines 265–313) sits at the same indentation level as the hit test (line 263), both inside the `MOUSEBUTTONDOWN` branch. There is no guard; the rules run **on every mouse-button press**, whether or not the die was hit. See Chapter 6, runtime view, and Chapter 11, finding 2.
- If `draftResult == "raven"`: `raven.moveForward()` (line 265)
- If `draftResult` is a colour (red, green, yellow, blue): pop one fruit from the matching list if it is non-empty (lines 268–275)
- If `draftResult == "basket"`: pick a "preferred" fruit stock, try to pop from it, and fall back to the other three stocks in a chain (approximately 40 lines of duplicated fallback chains, lines 276–313; see Chapter 11, finding 10)
- `draftResult` is **never reset** after use; it persists until the next die roll (see Chapter 11, finding 2)

**Phase 3: Outcome checks (lines 317–322)**
- Line 317: check if `raven.picPosX > (WINDOWWIDTH/10 + WINDOWWIDTH/2)` (i.e., pixel coordinate > 648). If so, set `gameLost = True` and `gameaktiv = False` (loss).
- Line 321: check if all four fruit lists are empty. If so, exit the loop (win, `gameLost` remains false). The condition uses Python's truthiness: `if gameLost == False and not redAppleList and not greenAppleList and not plumList and not pearList:`

**Phase 4: Rendering (lines 324–358)**
- Line 325: fill the screen with grey
- Line 328: draw the dice
- **Line 329: load and draw the rolled result image from disk** (`pygame.image.load("pics/" + draftResult + ".png")`), executed 60 times per second even when nothing changed
- Lines 332–354: draw the basket, trees, fields, gate, raven, and the four fruit lists in sequence
- Line 357: call `pygame.display.flip()` to update the display
- Line 358: call `clock.tick(FPS)` to enforce 60 frames per second

### End-Game Sequence (Lines 360–395)

After the main loop exits (when `gameaktiv` becomes false), a second loop runs `while endsequenz:`, displaying the result. A font is **constructed from disk every frame** using `pygame.font.SysFont("comicsansms", 40)` — at line 370 for the loss path and line 387 for the win path, both inside the loop, so it is constructed anew 60 times per second. The text is rendered in German: `"Verloren"` (lost, line 371) or `"Gewonnen"` (won, line 388). The loop exits only on QUIT or ESC. There is no option to restart.

## Intended Versus Actual

### The 2021 Design (diagramm/Class.drawio)

The author's 2021 class diagram specified:
- A base class `item` (not `Element`) with common sprite properties
- A `Tree` class that would own the fruit: `- amount: int`, `- sortOfFruit: string`, `+ decrement(int): int`, `+ emptyTree(int): void`
- A `Basket` class with `- amount: int` and `+ setAmount(int): string`
- Subclasses for `Raven` and `Dice`

This design would have embedded game rules into objects that own state. Checking if the game is won would have been: "are all trees empty?" A rule change would have been local to the `Tree` class.

### What Was Built

Three divergences stand out:

1. **`Tree` was abandoned.** The canvas contains a note: **"Tree eventuell löschen"** ("possibly delete Tree"). Trees were demoted to pure visual elements: `Fruit("tree", …)` instances with no behaviour. The fruit counts moved into four module-level lists.

   **Effect:** the game's core state—how many fruit remain—lives nowhere with a name or an owner. It is distributed across four lists. Rules that check "are we done?" must count or check emptiness on all four lists. There is no object to ask "how many apples are left?"

2. **`Basket.amount` was never implemented.** The basket is a picture, nothing more. The 2021 design would have tracked what the player has harvested. The implemented basket does not.

   **Effect:** there is no way to inspect what fruit the player has taken. The win condition is "the orchard is empty," not "the basket is full."

3. **`Dice` was left unspecified** in the 2021 diagram. The implemented `Dice` class ended up as the only object with stateful behaviour: it owns the mapping of die faces to outcomes and generates random rolls.

   **Effect:** the game has behaviour, but only in `Dice`. Rules are scattered in the module-level game loop.

### Summary

The gap between design and implementation reflects the choice not to build a domain model. The sketch in 2021 showed the author considering one; the note "possibly delete Tree" shows them reconsidering. The result was a system where game state is *data* (lists of fruit) with no *owners*—no objects that hold the rules. This is the root cause of the maintainability deficit (Chapter 11).
