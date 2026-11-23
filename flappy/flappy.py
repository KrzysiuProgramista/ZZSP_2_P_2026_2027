#!/usr/bin/env python3
"""Flappy — flap through the gaps without hitting the pipes.

GUI controls
    Space / Up / left click   flap
    R / F2                    restart
    P                         pause
    1 / 2 / 3                 easy / normal / hard

Other modes
    --selftest               run the physics/collision tests and exit
    --simulate SECONDS       fly with a built-in autopilot and report the score
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass

# gap between the pipes, and scroll speed in pixels per frame (60 fps)
# One flap lifts the bird ~74 px, so a gap below ~96 px is impossible by
# construction: the bird cannot hold a line inside it. Hard sits near that
# floor; difficulty otherwise comes from how fast the pipes close in.
DIFFICULTIES = {
    "easy": {"gap": 150, "speed": 2.0},
    "normal": {"gap": 130, "speed": 2.3},
    "hard": {"gap": 110, "speed": 2.5},
}

try:  # tkinter is optional: --selftest and --simulate need no display
    import tkinter as tk

    TK_AVAILABLE = True
except ImportError:  # pragma: no cover
    TK_AVAILABLE = False


def rects_overlap(x1: float, y1: float, w1: float, h1: float,
                  x2: float, y2: float, w2: float, h2: float) -> bool:
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2


@dataclass(slots=True)
class Pipe:
    x: float
    gap_y: float
    passed: bool = False


# --------------------------------------------------------------------------- #
# Game logic — no UI code in here, so it is fully testable.
# --------------------------------------------------------------------------- #


class FlappyGame:
    """Frame-based physics: one step() is one 1/60 s frame, speeds are px/frame."""

    WIDTH, HEIGHT = 360, 540
    GRAVITY = 0.45
    FLAP_VY = -8.4
    PIPE_W = 60
    BIRD_X = 80
    BIRD_SIZE = 14
    GROUND_H = 4
    SPAWN_GAP = 150   # horizontal distance between consecutive pipes
    EDGE_MARGIN = 100  # keeps a gap this far from the ceiling and the ground
    # A flap lifts the bird ~74 px over ~18 frames, so consecutive gaps may only
    # move a fraction of the gap height. The original picks each gap anywhere in
    # [100, 440], which can demand a 340 px climb between two pipes that are only
    # 150 px apart — unwinnable by construction. Clamping keeps runs fair.
    GAP_STEP_RATIO = 0.6

    def __init__(self, rng: random.Random | None = None,
                 gap: int = 110, speed: float = 2.3):
        self.rng = rng or random.Random()
        self.gap = gap
        self.speed = speed
        self.flap_rise = self._climb_height()
        self.reset()

    @classmethod
    def _climb_height(cls) -> float:
        """How far one flap lifts the bird, from the same discrete loop."""
        vy, y = cls.FLAP_VY, 0.0
        for _ in range(1000):
            vy += cls.GRAVITY
            y += vy
            if vy >= 0:
                break
        return -y

    # -- setup ------------------------------------------------------------- #

    def reset(self) -> None:
        self.bird_y = self.HEIGHT / 2
        self.bird_vy = 0.0
        self.pipes: list[Pipe] = []
        self.score = 0
        self.state = "ready"  # ready | playing | over
        self.death_reason: str | None = None

    @property
    def playing(self) -> bool:
        return self.state == "playing"

    @property
    def over(self) -> bool:
        return self.state == "over"

    @property
    def bird_half(self) -> float:
        return self.BIRD_SIZE / 2

    # -- player action ------------------------------------------------------ #

    def flap(self) -> list[str]:
        if self.over:
            return []
        self.bird_vy = self.FLAP_VY
        self.state = "playing"
        return ["flap"]

    # -- one frame ---------------------------------------------------------- #

    def step(self) -> list[str]:
        events: list[str] = []
        if not self.playing:
            return events

        self.bird_vy += self.GRAVITY
        self.bird_y += self.bird_vy

        for pipe in self.pipes:
            pipe.x -= self.speed
        if not self.pipes or self.pipes[-1].x < self.WIDTH - self.SPAWN_GAP:
            self._spawn_pipe()

        for pipe in self.pipes:
            if not pipe.passed and pipe.x + self.PIPE_W < self.BIRD_X:
                pipe.passed = True
                self.score += 1
                events.append(f"score:{self.score}")

        while self.pipes and self.pipes[0].x + self.PIPE_W < 0:
            self.pipes.pop(0)

        reason = self._collision()
        if reason is not None:
            self.state = "over"
            self.death_reason = reason
            events.append(f"over:{reason}")
        return events

    def _spawn_pipe(self) -> None:
        previous = self.pipes[-1].gap_y if self.pipes else self.HEIGHT / 2
        step = self.gap * self.GAP_STEP_RATIO
        low = max(self.EDGE_MARGIN, previous - step)
        high = min(self.HEIGHT - self.EDGE_MARGIN, previous + step)
        self.pipes.append(Pipe(x=float(self.WIDTH), gap_y=self.rng.uniform(low, high)))

    def _collision(self) -> str | None:
        half = self.bird_half
        if self.bird_y - half < 0:
            return "ceiling"
        if self.bird_y + half > self.HEIGHT - self.GROUND_H:
            return "ground"

        bx, by = self.BIRD_X - half, self.bird_y - half
        size = self.BIRD_SIZE
        for pipe in self.pipes:
            top_h = pipe.gap_y - self.gap / 2
            bottom_y = pipe.gap_y + self.gap / 2
            if rects_overlap(bx, by, size, size, pipe.x, 0, self.PIPE_W, top_h):
                return "pipe"
            if rects_overlap(bx, by, size, size, pipe.x, bottom_y, self.PIPE_W,
                             self.HEIGHT - bottom_y):
                return "pipe"
        return None

    # -- helpers used by the draw code and the autopilot -------------------- #

    def next_pipe(self) -> Pipe | None:
        """The first pipe the bird has not fully passed yet."""
        for pipe in self.pipes:
            if pipe.x + self.PIPE_W >= self.BIRD_X - self.bird_half:
                return pipe
        return None

    def autopilot_flap(self) -> bool:
        """Built-in pilot: keep the bird inside the gap it is flying towards.

        A flap lifts the bird ``flap_rise`` px, so it flaps when that climb
        would top out just inside the gap — or when gravity is about to sink it
        out of the bottom of the gap.
        """
        pipe = self.next_pipe()
        target = pipe.gap_y if pipe is not None else self.HEIGHT / 2
        clearance = self.gap / 2 - self.bird_half - 3.0
        safe_top, safe_bottom = target - clearance, target + clearance
        flap_at = safe_top + self.flap_rise  # climbing from here tops out at safe_top

        if self.bird_y < flap_at:
            return False  # too high to flap: the climb would clip the top pipe
        if self.bird_vy > 0:
            self.flap()
            return True
        # Still rising — flap early only if gravity would sink us out of the gap.
        lookahead = 6
        predicted = (self.bird_y + self.bird_vy * lookahead
                     + 0.5 * self.GRAVITY * lookahead * (lookahead + 1))
        if predicted >= safe_bottom:
            self.flap()
            return True
        return False


def run_simulate(seconds: float, seed: int | None = None, gap: int = 110,
                 speed: float = 2.3, verbose: bool = True) -> FlappyGame:
    """Headless flight with the autopilot — used by --simulate and the self test."""
    game = FlappyGame(random.Random(seed), gap=gap, speed=speed)
    game.flap()
    for frame in range(int(seconds * 60)):
        if game.over:
            break
        game.autopilot_flap()
        events = game.step()
        if verbose:
            for event in events:
                print(f"frame {frame:5d}  {event}")
    return game


# --------------------------------------------------------------------------- #
# Tkinter GUI
# --------------------------------------------------------------------------- #


class FlappyGUI:
    BG = "#16181d"
    PIPE = "#3f8f6b"
    GROUND = "#2a2d35"
    BIRD = "#f5c542"
    CARD = "#24272e"
    FG = "#e8e8e8"
    MUTED = "#8e8e93"
    TICK_MS = 16  # ~60 frames per second

    def __init__(self, gap: int = 110, speed: float = 2.3, seed: int | None = None):
        self.seed = seed
        self.gap = gap
        self.speed = speed
        self.game = FlappyGame(random.Random(seed), gap=gap, speed=speed)
        self.best = 0
        self.paused = False
        self.after_id: str | None = None

        self.root = tk.Tk()
        self.root.title("Flappy")
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root, width=self.game.WIDTH, height=self.game.HEIGHT,
            bg=self.BG, highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self._on_flap)
        self.root.bind("<KeyPress>", self._on_key)
        self.canvas.focus_set()

        self._draw()

    # -- input ------------------------------------------------------------- #

    def _on_flap(self, _event=None) -> None:
        if self.game.over:
            self.restart()
            return
        self.game.flap()

    def _on_key(self, event) -> None:
        key = event.keysym.lower()
        if key in {"space", "up", "w"}:
            self._on_flap()
        elif key in {"r", "n", "f2"}:
            self.restart()
        elif key == "p":
            self.paused = not self.paused
        elif key in {"1", "2", "3"}:
            preset = list(DIFFICULTIES.values())[int(key) - 1]
            self.set_difficulty(preset["gap"], preset["speed"])
        elif key == "escape":
            self.root.destroy()

    # -- game flow --------------------------------------------------------- #

    def restart(self) -> None:
        self.game.reset()
        self.paused = False
        self._draw()

    def set_difficulty(self, gap: int, speed: float) -> None:
        self.gap, self.speed = gap, speed
        self.game = FlappyGame(random.Random(self.seed), gap=gap, speed=speed)
        self.restart()

    # -- loop -------------------------------------------------------------- #

    def _tick(self) -> None:
        if not self.paused:
            for event in self.game.step():
                if event.startswith("score:"):
                    self.best = max(self.best, int(event.split(":")[1]))
            self._draw()
        self.after_id = self.root.after(self.TICK_MS, self._tick)

    # -- drawing ----------------------------------------------------------- #

    def _draw(self) -> None:
        game = self.game
        canvas = self.canvas
        canvas.delete("all")
        w, h = game.WIDTH, game.HEIGHT

        for pipe in game.pipes:
            top_h = pipe.gap_y - game.gap / 2
            bottom_y = pipe.gap_y + game.gap / 2
            canvas.create_rectangle(pipe.x, 0, pipe.x + game.PIPE_W, top_h,
                                    fill=self.PIPE, outline="")
            canvas.create_rectangle(pipe.x, bottom_y, pipe.x + game.PIPE_W, h,
                                    fill=self.PIPE, outline="")

        canvas.create_rectangle(0, h - game.GROUND_H, w, h, fill=self.GROUND, outline="")

        half = game.bird_half
        canvas.create_oval(game.BIRD_X - half, game.bird_y - half,
                           game.BIRD_X + half, game.bird_y + half,
                           fill=self.BIRD, outline="")

        canvas.create_text(w / 2, 56, text=str(game.score), fill=self.FG,
                           font=("Helvetica", 32, "bold"))

        if game.state == "ready":
            canvas.create_text(w / 2, h / 2 - 80, fill=self.MUTED,
                               font=("Helvetica", 14), text="點擊或按空白鍵")
        if game.over:
            canvas.create_rectangle(0, h / 2 - 70, w, h / 2 + 50, fill=self.CARD, outline="")
            canvas.create_text(w / 2, h / 2 - 40, fill=self.FG,
                               font=("Helvetica", 20, "bold"), text="遊戲結束")
            canvas.create_text(w / 2, h / 2 - 8, fill=self.FG, font=("Helvetica", 13),
                               text=f"分數 {game.score}    最高 {self.best}")
            canvas.create_text(w / 2, h / 2 + 24, fill=self.MUTED,
                               font=("Helvetica", 11), text="按 R 或點擊重來")
        if self.paused:
            canvas.create_text(w / 2, h / 2, fill=self.FG,
                               font=("Helvetica", 22, "bold"), text="暫停")

    def run(self) -> None:
        self._tick()
        self.root.mainloop()


# --------------------------------------------------------------------------- #
# Self test
# --------------------------------------------------------------------------- #


def selftest(verbose: bool = True) -> int:
    checks = 0

    def check(name: str, condition: bool) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(name)
        if verbose:
            print(f"  ok  {name}")

    game = FlappyGame(random.Random(0))
    check("starts ready, bird centred",
          game.state == "ready" and game.bird_y == game.HEIGHT / 2 and not game.pipes)

    check("flapping starts the game", game.flap() == ["flap"] and game.playing)
    check("flap gives the bird upward speed", game.bird_vy == FlappyGame.FLAP_VY)

    # a flap lifts the bird, then gravity pulls it back down
    game = FlappyGame(random.Random(0))
    game.flap()
    start_y, start_vy = game.bird_y, game.bird_vy
    game.step()
    check("the bird climbs right after a flap", game.bird_y < start_y)
    check("gravity decelerates the climb", game.bird_vy > start_vy)
    for _ in range(20):
        game.step()
    check("the bird starts falling again", game.bird_vy > 0)
    check("climb height matches the physics", 70 < game.flap_rise < 80)

    # nothing moves until the first flap
    game = FlappyGame(random.Random(0))
    game.step()
    check("the bird waits for the first flap",
          game.state == "ready" and game.bird_y == game.HEIGHT / 2 and not game.pipes)

    # hitting the ceiling and the ground ends the run
    game = FlappyGame(random.Random(0))
    game.flap()
    game.bird_y, game.bird_vy = 2, -6
    check("the ceiling kills the bird",
          "over:ceiling" in game.step() and game.over and game.death_reason == "ceiling")
    check("a dead bird stops moving", game.step() == [])

    game = FlappyGame(random.Random(0))
    game.flap()
    game.bird_y, game.bird_vy = game.HEIGHT - 6, 6
    check("the ground kills the bird", "over:ground" in game.step())

    # pipes spawn, scroll left, and gaps stay inside the play area
    game = FlappyGame(random.Random(1))
    game.flap()
    for _ in range(10):
        game.step()
    check("pipes spawn", len(game.pipes) >= 1)
    first_x = game.pipes[0].x
    game.step()
    check("pipes scroll left", game.pipes[0].x < first_x)
    check("gaps stay inside the play area",
          all(FlappyGame.EDGE_MARGIN <= p.gap_y <= FlappyGame.HEIGHT - FlappyGame.EDGE_MARGIN
              for p in game.pipes))

    # a pipe that has left the screen is dropped from the list
    game = FlappyGame(random.Random(1))
    game.flap()
    game.bird_y = game.HEIGHT / 2
    game.pipes = [Pipe(x=-FlappyGame.PIPE_W - 5, gap_y=game.HEIGHT / 2)]
    game.step()
    check("off-screen pipes are dropped", all(p.x > -FlappyGame.PIPE_W for p in game.pipes))

    # passing a pipe scores exactly once (autopilot keeps the bird alive)
    game = FlappyGame(random.Random(2))
    game.flap()
    game.pipes = [Pipe(x=FlappyGame.BIRD_X + 40, gap_y=game.HEIGHT / 2)]
    game.bird_y, game.bird_vy = game.HEIGHT / 2, 0
    scored = []
    for _ in range(60):
        game.autopilot_flap()
        scored.extend(game.step())
        if game.over:
            break
    check("passing a pipe scores", game.score == 1 and "score:1" in scored)
    check("a pipe only scores once", sum(1 for e in scored if e.startswith("score:")) == 1)

    # flying into a pipe ends the run
    game = FlappyGame(random.Random(3))
    game.flap()
    game.pipes = [Pipe(x=FlappyGame.BIRD_X - 10, gap_y=60.0)]
    game.bird_y, game.bird_vy = 400, 0  # far from the gap at y=60
    check("hitting a pipe kills the bird", "over:pipe" in game.step())

    # the pipe body is solid: no free pass through the gap edges
    game = FlappyGame(random.Random(4))
    game.flap()
    game.pipes = [Pipe(x=FlappyGame.BIRD_X - 10, gap_y=270.0)]
    game.bird_y, game.bird_vy = 270.0, 0
    events = game.step()
    check("flying through the middle is safe", not any(e.startswith("over:") for e in events))

    # difficulty presets change the gap and the speed
    check("difficulty presets are ordered", DIFFICULTIES["easy"]["gap"] > DIFFICULTIES["hard"]["gap"]
          and DIFFICULTIES["easy"]["speed"] < DIFFICULTIES["hard"]["speed"])

    # the autopilot survives and scores on every difficulty, so no preset is
    # impossible by construction
    for name, preset in DIFFICULTIES.items():
        scores = [
            run_simulate(60, seed=seed, gap=preset["gap"], speed=preset["speed"],
                         verbose=False).score
            for seed in (11, 12, 13)
        ]
        check(f"autopilot clears pipes on {name} ({scores})", min(scores) >= 10)

    # a new gap never moves further than the bird can travel between pipes
    game = FlappyGame(random.Random(8), gap=DIFFICULTIES["hard"]["gap"],
                      speed=DIFFICULTIES["hard"]["speed"])
    game.flap()
    game.bird_y = game.HEIGHT / 2
    game.pipes = []
    step = DIFFICULTIES["hard"]["gap"] * FlappyGame.GAP_STEP_RATIO
    previous = game.HEIGHT / 2
    deltas = []
    for _ in range(40):
        game._spawn_pipe()
        gap_y = game.pipes[-1].gap_y
        deltas.append(abs(gap_y - previous))
        previous = gap_y
    check("consecutive gaps stay reachable", max(deltas) <= step + 1e-9)

    # a bird that never flaps falls to the ground
    game = FlappyGame(random.Random(5))
    game.flap()
    game.bird_vy = 0
    for _ in range(600):
        game.step()
        if game.over:
            break
    check("not flapping ends the run", game.over and game.death_reason == "ground")

    print(f"\n{checks} checks passed.")
    return 0


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Flappy (Tkinter GUI). Use --selftest or --simulate without a display.",
    )
    parser.add_argument("-d", "--difficulty", choices=DIFFICULTIES, default="normal",
                        help="gap and speed preset (default: normal)")
    parser.add_argument("--gap", type=int, help="custom gap size in pixels")
    parser.add_argument("--speed", type=float, help="custom scroll speed in pixels per frame")
    parser.add_argument("--seed", type=int, help="fixed random seed (repeatable pipes)")
    parser.add_argument("--simulate", type=float, metavar="SECONDS",
                        help="fly with the built-in autopilot for this many seconds")
    parser.add_argument("--selftest", action="store_true", help="run the logic tests and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        print("running Flappy self tests...")
        return selftest()

    preset = DIFFICULTIES[args.difficulty]
    gap = args.gap if args.gap is not None else preset["gap"]
    speed = args.speed if args.speed is not None else preset["speed"]

    if args.simulate is not None:
        game = run_simulate(args.simulate, args.seed, gap, speed)
        outcome = f"crashed into the {game.death_reason}" if game.over else "still flying"
        print(f"\nautopilot score {game.score} after {args.simulate:g}s — {outcome}")
        return 0

    if not TK_AVAILABLE:
        print("tkinter is unavailable — try --simulate or --selftest.", file=sys.stderr)
        return 1
    try:
        FlappyGUI(gap, speed, args.seed).run()
    except tk.TclError as exc:  # no display
        print(f"cannot open a window ({exc}); try --simulate instead.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
