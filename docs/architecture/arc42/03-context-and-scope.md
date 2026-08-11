# 3. Context and Scope

## System Scope

![Context](../diagrams/context.drawio)

**In Scope**

- `main.py` — the entire runtime and game logic
- `module/` — helper packages (currently orphaned; see Chapter 5)
- `pics/` — asset library, the contract between code and images
- `main.spec` — the build definition for PyInstaller

**Out of Scope**

- The pygame and SDL2 libraries (external dependencies)
- The Windows desktop and its runtime environment
- The generated `build/` and `dist/` directories (build artefacts)

## Business Context

The system has one external actor: the **player**. The interaction is simple and bidirectional:

- **Input:** mouse clicks on the die
- **Output:** rendered graphics (orchard, fruit, raven position, rolled result) and a final verdict (win or lose)

There is no network communication, no user accounts, no external services. The game is entirely self-contained.

## Technical Context

Fruit Garden runs on a Windows desktop as a standalone executable. It interacts with:

- **Filesystem:** reads image files from `pics/`, relative to the working directory at runtime
- **Pygame:** calls the pygame API for rendering, input handling, and timing
- **SDL2 (via pygame):** the underlying graphics and audio library (`SDL2.dll`, `SDL2_image.dll`, `SDL2_ttf.dll`, `SDL2_mixer.dll`)
- **CPU and GPU:** renders 60 frames per second via SDL2 to the display

From the player's perspective, only the graphical output and input responsiveness are visible. The technical stack below is invisible.

## Deployment

For deployment contexts, see Chapter 7.
