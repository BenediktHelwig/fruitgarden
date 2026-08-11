# 7. Deployment View

![Deployment](../diagrams/deployment.drawio)

## Two Deployment Scenarios

### Scenario 1: From Source

**Environment**
- Developer's workstation running Windows 11
- CPython 3.9 or later installed
- pygame package installed (and its SDL2 dependencies)

**Execution**
- Command line: `python main.py` from the repository root
- Working directory: repository root (`C:\Users\bened\source\repos\fruitgarden`)
- Asset loading: the code reads `pics/*.png` relative to the working directory (e.g., `pics/raven.png`)
- Runtime: the game runs in a window, driven by pygame and SDL2

**Constraints**
- The working directory must be the repository root, or `pics/` will not be found
- If a parent process (e.g., an IDE) changes the working directory, asset loading will fail

### Scenario 2: PyInstaller Bundle (Packaged Distribution)

**Build process**
- `main.spec` defines:
  - Entry point: `main.py`
  - `hiddenimports=[]` (empty): PyInstaller discovers pygame by static analysis; nothing is declared
  - `datas=[]` (empty): the problem—no additional files are bundled
  - `pathex=['C:\\Users\\Umschueler\\source\\repos\\fruitgarden']`: a build path from a different machine and user account (stale, see below)
  - `console=True`: open a console window alongside the game
  - Output mode: `onedir` (a directory with an executable and all runtime files)

- PyInstaller freezes the Python 3.9 interpreter, pygame packages, and SDL2 DLLs into `dist/main/`:
  - `main.exe` (the entry point)
  - `python39.dll` (the frozen interpreter)
  - `SDL2.dll`, `SDL2_image.dll`, `SDL2_ttf.dll`, `SDL2_mixer.dll` (SDL2 runtime)
  - Pygame `.pyd` extensions (compiled pygame modules)
  - `base_library.zip` (the frozen standard library)

**Execution**
- User runs `dist/main/main.exe`
- The frozen Python interpreter loads `base_library.zip` and the bundled pygame modules
- The game starts in a window (plus a console window, because `console=True`)

**Critical defect: Assets not bundled**

`main.spec` declares `datas=[]`, meaning no additional files are included in the bundle. **`pics/` is not packaged.** At runtime, the game tries to load `pics/raven.png` relative to the current working directory. For this to succeed, the user must:
- Navigate to a directory that contains a `pics/` folder, or
- Copy `pics/` into the directory alongside `main.exe`

This is a defect because the packaged executable advertises itself as self-contained (it is an `.exe` in `dist/`, ready to run) but is actually dependent on an external asset folder.

**Secondary defects**

- **`pathex` is stale:** the path `C:\Users\Umschueler\source\repos\fruitgarden` in `pathex` is from a different machine and user account. The spec no longer describes the environment it is actually used in; `pathex` feeds PyInstaller's module search path during the build.
- **`console=True` opens a console window:** alongside the game window, unnecessary for end users. Should be `console=False`.

## Impact on Quality Goals

| Defect | Quality Goal Damaged | Severity |
|---|---|---|
| `pics/` not bundled | Correctness of the game rules (goal 2); also Deployability (outside ranked goals) | Critical |
| Stale `pathex` | Learnability / Maintainability (goal 1) | Low |
| `console=True` | Usability for a pre-school child (goal 3) | Low |

See Chapter 11 for full analysis and direction for remediation.
