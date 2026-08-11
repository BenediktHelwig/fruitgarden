# 6. Runtime View

## One Dice Roll

![Runtime: Dice Roll](../diagrams/runtime-dice-roll.drawio)

This sequence describes one complete cycle from a player clicking the die to the new game state being rendered.

1. **Player clicks the die.** `pygame.event.get()` yields a `MOUSEBUTTONDOWN` event. The event loop queries `pygame.mouse.get_pos()` to get the mouse coordinates.

2. **Hit test.** The code checks `if dice.overDice(mousePosition):` (line 263). The `overDice()` method (line 71) performs a bounding-box test, comparing the mouse coordinates to the dice sprite's bounds. If the click is outside the dice, the condition is false and the die is not rolled.

   If the click is inside the dice, execution continues to step 3.

3. **Roll the die.** `dice.rollDice()` (lines 75–78) calls `random.randint(1,6)` and looks up the result in the `__sign` dict, returning a string: `"red"`, `"green"`, `"yellow"`, `"blue"`, `"raven"`, or `"basket"`. This value is assigned to the module-level variable `draftResult` (line 264).

4. **Apply the rule.** The rule block (lines 265–313) executes and modifies game state based on `draftResult`. This block sits at the same indentation level as the hit test (line 263), both inside the `MOUSEBUTTONDOWN` event handler. **There is no guard—the rule block runs on every mouse-button press**, whether or not the die was hit.

   The rules applied:
   - Line 265: if `draftResult == "raven"` → `raven.moveForward()` increments the raven's X position by 130 pixels
   - Lines 268–275: if `draftResult` is a colour (red, green, yellow, blue) → pop one fruit from the matching list if non-empty
   - Lines 276–313: if `draftResult == "basket"` → pick a fruit stock at random with fallback logic

   When the player clicks outside the dice and misses, `draftResult` retains its previous value from the last successful roll. The rule block re-applies that roll. See Chapter 11, finding 2.

   `draftResult` is **not reset** after being applied. It persists until the next successful die roll.

5. **Outcome checks.** After the event loop finishes (lines 317–322):
   - Lines 317–319: Check if the raven has reached the orchard: `if raven.picPosX > ((WINDOWWIDTH/10) + (WINDOWWIDTH/2)):` (i.e., X > 648). If true, set `gameLost = True` and exit the main loop.
   - Line 321: Otherwise, check if all four fruit lists are empty: `if gameLost == False and not redAppleList and not greenAppleList and not plumList and not pearList:`. If true, exit the main loop (win).

6. **Render the frame.** The render pass (lines 324–358) redraws everything:
   - Line 325: clear the screen to grey
   - Line 328: draw the dice sprite
   - **Line 329: load the image for `draftResult` from disk** and draw it at the top-left (a display of the last rolled outcome)
   - Lines 332–354: draw the basket, trees, fields, gate, raven, and all remaining fruit sprites in sequence
   - This entire pass happens 60 times per second, regardless of whether game state changed

7. **Update the display and tick the clock.** Line 357: `pygame.display.flip()` swaps the back buffer to the front. Line 358: `clock.tick(FPS)` enforces 60 frames per second. If rendering is faster than 60 FPS, the clock blocks; if slower, frames are dropped.

The loop repeats: next `MOUSEBUTTONDOWN` → hit test → roll → rule → outcome check → render → loop.

## Key Observations for Understanding Bugs

### The rule block runs on every mouse button event

Lines 265–313 sit at the same indentation level as the hit test (line 263), both inside the `MOUSEBUTTONDOWN` event handler (which starts at line 262). When a player clicks outside the dice (missing), they trigger a `MOUSEBUTTONDOWN` event; the hit test fails and the die is not rolled; but the rule block still runs because `draftResult` still holds the previous roll's value.

**Consequence:** once any roll has happened, every subsequent click anywhere in the window re-applies that same result until the next successful roll. A single lucky red roll lets the player empty the red apple tree by clicking; a single raven roll lets the player walk the raven to the gate by clicking. This is the dominant correctness bug (see Chapter 11, finding 2).

### draftResult is never cleared

After the rule block applies `draftResult`, the value persists in the module-level variable. The rendering phase loads the image again (every frame) and displays it—the user sees the last rolled result continuously. On the next frame, if the player has not clicked since, the rule block will not run (because the event loop would be empty). But if they click anywhere, the stale `draftResult` is applied again.

### The loss condition is implicit in geometry

The raven's progress is stored as a pixel coordinate: `raven.picPosX`. It starts at `int(ravenPosStart)` = **10 pixels** (line 141). Each `moveForward()` call (line 47) adds 130 pixels. The loss threshold (line 317) is `raven.picPosX > (WINDOWWIDTH/10 + WINDOWWIDTH/2)` = **648 pixels**.

The sequence: 10 → 140 → 270 → 400 → 530 → 660 (loss). **Exactly five raven rolls end the game.** This number is not declared anywhere and was never written down as a design requirement—it falls out of the geometry. Changing the window width, tile width, or raven start position changes the game's difficulty unintentionally.
