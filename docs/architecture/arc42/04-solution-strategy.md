# 4. Solution Strategy

## Overview

The system follows the structure and patterns of a standard pygame tutorial: a single main file with a module-level game loop, a sprite hierarchy for game objects, and immediate-mode rendering. Some of these choices were deliberate; others were adopted by default from the tutorial idiom.

## Key Architectural Decisions

### Single-File Script with Module-Level Game Loop

The entire runtime is `main.py`, executed top-to-bottom once at startup:
- Lines 1–7: imports and initialisation
- Lines 9–22: constants and global variables
- Lines 29–78: class definitions
- Lines 81–241: world construction (objects instantiated at module scope)
- Lines 250–358: the main game loop, itself at module scope
- Lines 360–395: the end-game sequence loop
- Lines 397–398: cleanup and exit

This structure is the standard shape of pygame tutorials and was adopted as the default rather than chosen for specific reasons.

**Consequence:** game state lives in module-level variables (`gameaktiv`, `gameLost`, `draftResult`) and lists (`redAppleList`, `greenAppleList`, `plumList`, `pearList`). This makes state global and harder to reason about or test.

### Sprite-as-Entity: the Element Base Class

Every game object—the raven, fruit, trees, the basket, even decorative fields—inherits from `Element` (`main.py:29–40`). `Element` owns:
- An image loaded from `pics/<name>.png`
- Position (pixel coordinates: `picPosX`, `picPosY`)
- Size (in pixels)
- A `drawPicture()` method that blits to the screen

This is the root architectural choice. It reflects the pygame tutorial pattern: *think of the game as a collection of sprites, where each sprite is primarily a picture and incidentally a rule*.

**Critical consequence:** there is no domain model separate from the render model. The raven's progress towards the orchard is not a count of steps—it is its pixel coordinate, `picPosX`. The loss condition (line 317) is `raven.picPosX > WINDOWWIDTH/10 + WINDOWWIDTH/2`. Whether the game is won is determined by checking if the four fruit lists are empty—the fruit counts live nowhere else. This coupling of state to rendering is the root cause of most findings in Chapter 11.

### Game State in Module-Level Variables and Lists

Rather than bundling game state into an owning object (e.g., a `GameState` or `World` class), state is scattered:
- `gameaktiv` and `gameLost` flags (lines 19, 20)
- `draftResult` (line 21), recording what the die rolled
- Four lists: `redAppleList`, `greenAppleList`, `plumList`, `pearList` (lines 147–241)
- The raven itself, an `Element`, which is the state

This is visible in the module's global namespace and in the for-loops that populate the four lists.

**Consequence:** the game loop (line 250 onwards) directly reads and modifies these globals. There is no encapsulation. A rule change requires understanding how the state is laid out across the module and then finding every place it is read or written.

### Immediate-Mode Rendering

Every frame (60 times per second), the entire screen is redrawn:
- Clear to grey (line 325)
- Draw dice, trees, fields, gate, raven, remaining fruit
- Call `pygame.display.flip()` (line 357)

There is no dirty tracking, no spatial partitioning, no culling. Every object is drawn every frame, even if it has not moved. This is simple and correct, and also inefficient, but acceptable for this scale.

**Consequence:** loading images on-the-fly (line 329: `pygame.image.load("pics/" + draftResult + ".png")`) executes 60 times a second, a waste of I/O (see Chapter 11).

### Two Sequential Loops Instead of a State Machine

The game has two phases:
1. Lines 250–358: the play loop, running `while gameaktiv`
2. Lines 360–395: the end-game loop, running `while endsequenz`, displaying the win/lose message

The loops are sequential, not unified by a state machine. The play loop runs until `gameaktiv` becomes false, then control passes to the end loop.

**Consequence:** the structure is readable but inflexible. Adding a menu state or restart would require threading another loop into the flow.

## Design Decisions Not Taken

### The 2021 Class Design with Tree Aggregate

In `diagramm/Class.drawio` (October 2021), the author sketched a class hierarchy in which `Tree` would aggregate fruit, with operations like `setAmount()`, `decrement()`, and `emptyTree()`. This design would have made the fruit counts properties of individual trees, not lists at module scope.

The note **"Tree eventuell löschen"** ("possibly delete Tree") on the canvas suggests the author was already uncertain about this in 2021.

In the implemented system, `Tree` was never built. Instead, trees became `Fruit("tree", …)` instances—pure decoration—and fruit counts became four module-level lists. The fruit aggregate that would have owned the rules was abandoned.

**Consequence:** the loss of structure left the rules scattered and the domain model absent. This is the single largest contributor to the maintainability and testability debt (see Chapter 11).

## Summary

The system chose the simplest path consistent with pygame tutorials: objects-as-sprites, rendering-as-storage, and global state. This made the first version quick to write and visually correct. It also made the rules implicit and the state invisible, which damages learnability—the primary quality goal.
