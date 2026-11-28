#!/usr/bin/env python3
"""Watch the trained bird play (needs flappy_model.npz from flappy_train.py).

The bird plays by itself and stops when it dies, showing the score.
R or a click starts another run. 1 / 2 / 3 change the difficulty.
"""

from __future__ import annotations

import argparse
import sys

from flappy import DIFFICULTIES, FlappyGUI
from flappy_train import Brain


class AIFlappy(FlappyGUI):
    def __init__(self, brain: Brain, gap: int, speed: float, seed: int | None,
                 difficulty: str = "normal"):
        super().__init__(gap, speed, seed, difficulty)
        self.brain = brain
        self.root.title("Flappy AI")

    def _on_flap(self, _event=None) -> None:
        if self.game.over:  # the human only restarts; the bird does the flapping
            self.restart()

    def _on_key(self, event) -> None:
        if event.keysym.lower() in {"space", "up", "w"}:
            return
        super()._on_key(event)

    def _tick(self) -> None:
        game = self.game
        if not self.paused and not game.over:
            if game.state == "ready" or self.brain.act(game):
                game.flap()
        super()._tick()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Watch the trained Flappy AI.")
    parser.add_argument("-d", "--difficulty", choices=DIFFICULTIES, default="normal")
    parser.add_argument("--seed", type=int, help="fixed pipes (same run every time)")
    parser.add_argument("--model", default="flappy_model.npz")
    args = parser.parse_args(argv)

    try:
        brain = Brain.load(args.model)
    except FileNotFoundError:
        print(f"{args.model} not found - run flappy_train.py first.", file=sys.stderr)
        return 1
    preset = DIFFICULTIES[args.difficulty]
    AIFlappy(brain, preset["gap"], preset["speed"], args.seed, args.difficulty).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
