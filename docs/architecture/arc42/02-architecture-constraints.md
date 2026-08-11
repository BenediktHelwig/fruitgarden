# 2. Architecture Constraints

## Technical Constraints

**Pygame and SDL2**
- The system is built on pygame, which wraps SDL2. No graphics, input, or audio outside this stack is possible.
- Deployment requires SDL2 dynamic libraries: `SDL2.dll`, `SDL2_image.dll`, `SDL2_ttf.dll`, `SDL2_mixer.dll`.

**Python Runtime**
- The bundled executable was built against CPython 3.9 (visible in `cp39-win_amd64.pyd` and `python39.dll` in the PyInstaller output).
- The developer's current interpreter is Python 3.14.4.
- Version mismatch creates a dependency drift problem (see Chapter 11).

**Windows Desktop**
- Single-user, Windows desktop application.
- No network communication, no server backend.
- No persistent storage: game state exists only in RAM for the duration of a session.

**Asset Naming Convention**
- Images are stored as hand-made PNG files in `pics/`.
- The code assumes a hard contract: every named element (e.g., `"raven"`, `"redApple"`) has a matching file at `pics/<name>.png`.
- This convention is embedded in the `Element` constructor, which reads `"pics/" + name + ".png"`.

**Distribution**
- Packaged as a PyInstaller onedir bundle: a directory containing `main.exe` plus all runtime dependencies and a frozen Python interpreter.
- Currently, the generated `build/` and `dist/` directories are committed to the repository (see Chapter 11).

## Organisational Constraints

**Development Model**
- One developer, learning by doing.
- No formal requirements process, no code review, no continuous integration.
- No automated tests.

**Design Philosophy**
- Clarity and learnability outrank feature completeness.
- The codebase is a teaching artefact for its author's future self, not a production handover.
