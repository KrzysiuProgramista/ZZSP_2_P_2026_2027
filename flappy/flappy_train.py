#!/usr/bin/env python3
"""Train a Flappy bird by evolution (numpy only, no other installs).

    python3 flappy_train.py            train, saves flappy_model.npz
    python3 flappy_train.py --test     score the saved model against a random player

A small neural network looks at the bird and the next two pipes and decides
every frame: flap or not. A population of networks plays; the best ones are
kept and mutated to make the next generation. Ctrl+C stops and keeps the best.

The network gets raw numbers only. The built-in autopilot in flappy.py is not
used, so whatever it learns, it learns by itself.
"""

from __future__ import annotations

import argparse
import random
import sys
import time

import numpy as np

from flappy import DIFFICULTIES, FlappyGame

N_IN, N_HID = 6, 8
N_PARAMS = N_HID * N_IN + N_HID + N_HID + 1
MODEL_FILE = "flappy_model.npz"


# --------------------------------------------------------------------------- #
# The brain
# --------------------------------------------------------------------------- #


def observe(g: FlappyGame) -> np.ndarray:
    """What the network sees: bird height, bird speed, next two pipes."""
    ahead = [p for p in g.pipes if p.x + g.PIPE_W >= g.BIRD_X - g.bird_half]

    def pipe_view(pipe):
        if pipe is None:
            return 1.0, 0.0
        return (pipe.x - g.BIRD_X) / g.WIDTH, (pipe.gap_y - g.bird_y) / 200

    dx1, dy1 = pipe_view(ahead[0] if ahead else None)
    dx2, dy2 = pipe_view(ahead[1] if len(ahead) > 1 else None)
    return np.array([g.bird_y / g.HEIGHT * 2 - 1, g.bird_vy / 10, dx1, dy1, dx2, dy2])


class Brain:
    """6 inputs -> 8 tanh units -> 1 output. Output above 0 means flap."""

    def __init__(self, params: np.ndarray):
        a = N_HID * N_IN
        self.w1 = params[:a].reshape(N_HID, N_IN)
        self.b1 = params[a:a + N_HID]
        self.w2 = params[a + N_HID:a + 2 * N_HID]
        self.b2 = params[-1]

    def act(self, g: FlappyGame) -> bool:
        hidden = np.tanh(self.w1 @ observe(g) + self.b1)
        return float(self.w2 @ hidden + self.b2) > 0

    @staticmethod
    def load(path: str = MODEL_FILE) -> "Brain":
        return Brain(np.load(path)["params"])


# --------------------------------------------------------------------------- #
# Playing
# --------------------------------------------------------------------------- #


def run_episode(act, gap: int, speed: float, seed: int, max_frames: int) -> tuple[int, int]:
    """Play one game headless. Returns (frames survived, pipes passed)."""
    g = FlappyGame(random.Random(seed), gap=gap, speed=speed)
    g.flap()
    frames = 0
    while not g.over and frames < max_frames:
        if act(g):
            g.flap()
        g.step()
        frames += 1
    return frames, g.score


def random_player(seed: int):
    rng = random.Random(seed)
    return lambda _g: rng.random() < 0.06


# --------------------------------------------------------------------------- #
# Evolution
# --------------------------------------------------------------------------- #


def evaluate(params: np.ndarray, seeds, gap, speed, max_frames) -> tuple[float, float]:
    brain = Brain(params)
    results = [run_episode(brain.act, gap, speed, s, max_frames) for s in seeds]
    return (sum(r[0] for r in results) / len(results),
            sum(r[1] for r in results) / len(results))


def save(params: np.ndarray) -> None:
    np.savez(MODEL_FILE, params=params)


def report(params: np.ndarray, gap: int, speed: float, frames: int) -> None:
    seeds = range(10_000, 10_030)  # games the network has never seen
    brain = Brain(params)
    ai = [run_episode(brain.act, gap, speed, s, frames)[1] for s in seeds]
    rnd = [run_episode(random_player(s), gap, speed, s, frames)[1] for s in seeds]
    ai_avg, rnd_avg = sum(ai) / len(ai), sum(rnd) / len(rnd)
    print(f"\ntest on {len(ai)} new games (each capped at {frames // 60}s of play)")
    print(f"  AI      avg score {ai_avg:6.1f}   min {min(ai)}   max {max(ai)}")
    print(f"  random  avg score {rnd_avg:6.1f}   min {min(rnd)}   max {max(rnd)}")


def train(args) -> int:
    preset = DIFFICULTIES[args.difficulty]
    gap, speed = preset["gap"], preset["speed"]
    rng = np.random.default_rng(args.seed)

    pop = rng.normal(0, 1, (args.pop, N_PARAMS))
    if args.resume:
        champion = np.load(MODEL_FILE)["params"]
        pop[0] = champion
        for i in range(1, args.pop):
            pop[i] = champion + rng.normal(0, 0.1, N_PARAMS)

    print(f"training on '{args.difficulty}' (gap {gap}, speed {speed}) "
          f"- population {args.pop}, Ctrl+C to stop\n")
    best = pop[0]
    try:
        for gen in range(1, args.generations + 1):
            start = time.time()
            seeds = [int(rng.integers(1 << 30)) for _ in range(args.episodes)]
            results = [evaluate(p, seeds, gap, speed, args.max_frames) for p in pop]
            order = np.argsort([-r[0] for r in results])
            best = pop[order[0]].copy()
            best_frames, best_score = results[order[0]]
            avg = sum(r[0] for r in results) / len(results)
            save(best)
            print(f"gen {gen:3d}   best {best_frames:6.0f} frames (score {best_score:5.1f})"
                  f"   avg {avg:6.0f}   {time.time() - start:4.1f}s")

            if best_frames >= args.max_frames:
                # looks perfect - double-check on 20 games it has never seen
                check = [int(rng.integers(1 << 30)) for _ in range(20)]
                if evaluate(best, check, gap, speed, args.max_frames)[0] >= args.max_frames:
                    print("\nsurvived every game to the time limit, including 20 fresh ones - done.")
                    break

            elites = pop[order[:max(2, args.pop // 10)]]
            top_half = pop[order[:args.pop // 2]]
            children = []
            for _ in range(args.pop - len(elites)):
                parent = top_half[rng.integers(len(top_half))]
                mask = rng.random(N_PARAMS) < 0.3
                children.append(parent + rng.normal(0, 0.2, N_PARAMS) * mask)
            pop = np.vstack([elites, children])
    except KeyboardInterrupt:
        print("\nstopped.")

    save(best)
    print(f"saved {MODEL_FILE}")
    report(best, gap, speed, args.max_frames * 3)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evolve a Flappy-playing neural network.")
    parser.add_argument("-d", "--difficulty", choices=DIFFICULTIES, default="normal")
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--pop", type=int, default=50, help="networks per generation")
    parser.add_argument("--episodes", type=int, default=5, help="games per network per generation")
    parser.add_argument("--max-frames", type=int, default=3000,
                        help="a game ends after this many frames (60 = one second)")
    parser.add_argument("--seed", type=int, help="fix the random seed")
    parser.add_argument("--resume", action="store_true", help="continue from the saved model")
    parser.add_argument("--test", action="store_true", help="only test the saved model")
    args = parser.parse_args(argv)

    if args.test:
        preset = DIFFICULTIES[args.difficulty]
        report(np.load(MODEL_FILE)["params"], preset["gap"], preset["speed"],
               args.max_frames * 3)
        return 0
    return train(args)


if __name__ == "__main__":
    sys.exit(main())
