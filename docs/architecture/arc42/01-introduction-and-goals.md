# 1. Introduction and Goals

## Purpose and Overview

Fruit Garden is a digital implementation of the German children's board game *Obstgarten* (HABA, "First Orchard"). It was written as a deliberate practice project by a single developer for their daughter to play.

The digital game reproduces the core mechanics of the physical game: the player rolls a die, harvests fruit matching the rolled colour, manages a basket, and races against a raven advancing across the board. The game ends when either all fruit has been harvested (win) or the raven reaches the orchard (loss). An end screen announces the outcome.

## Requirements

**Functional** — the following features must work:

- Roll the die by clicking it
- Harvest fruit corresponding to the colour rolled (or random fruit on a basket roll)
- Move the raven one step on each raven roll
- Detect win: all four fruit types harvested
- Detect loss: raven reaches the orchard
- Render the orchard, raven, available fruit, and the result of each roll
- Display an end screen with the outcome and no option to restart

**Quality Goals**

| # | Quality goal | Motivation | Scenario |
|---|---|---|---|
| 1 | Learnability / Maintainability | The project exists so its author learns from it. Code clarity outranks features. | A rule change—for example, making the basket roll a player choice rather than random—can be located and made in one place. |
| 2 | Correctness of the game rules | The digital game must behave like the physical *Obstgarten*; a child notices any deviation immediately. | Rolling the basket results in the player choosing which fruit to take, not a random selection. |
| 3 | Usability for a pre-school child | The game is playable by children aged 3–5 with no reading and one large click target. | A four-year-old can play a full game without adult help. |

## Stakeholders

| Stakeholder | Interests | Role |
|---|---|---|
| Developer (author) | Learning software design through practice; maintaining clarity of the code. | Developer, learner, architect of future changes. |
| Player (daughter) | Playing a game that behaves like the physical version. | End user; provides immediate feedback on correctness and usability. |
