# Binary Search Visualizer

A tiny pygame program that shows binary search working, step by step, with nothing to click. You open it, sit back, and watch the search narrow down on its target.

## Run it

You need Python 3 and pygame:

```
pip install pygame
python binary_search_simple.py
```

Press `ESC` to close the window.

## What you'll see

At the top, the program tells you what number it's looking for ("Find 47"). Below that is a row of 16 sorted numbers, and every second the search takes one step:

- **Yellow**: the middle box it's checking right now
- **Blue**: boxes that could still hold the target
- **Grey**: boxes that are ruled out for good
- **Green**: the target, found

Small `lo`, `mid` and `hi` markers sit under the boxes so you can see exactly where the search window starts, ends and splits.

When the search finishes, you get a big **FOUND** or **NOT FOUND** for a couple of seconds. Then it picks a new target and goes again.

A few details:

- The array is generated **once**, when the program starts, and stays the same. Only the target changes between searches.
- Roughly one in five targets is deliberately *not* in the array, so you also see how a failed search ends (`lo` ends up past `hi`).

## The idea in one minute

The array is sorted, so you never need to check every box. Look at the middle one:

1. If it's the target, you're done.
2. If it's too small, the target must be to the right, so throw away the left half.
3. If it's too big, the target must be to the left, so throw away the right half.

Repeat on whatever is left. Each step cuts the problem in half, so 16 numbers take at most 5 steps, and a million numbers would take about 20. That's what O(log n) means in practice.

## How the code works

The search is written as a normal loop, but it uses `yield` to pause at each step:

```python
while lo <= hi:
    mid = (lo + hi) // 2
    yield lo, hi, mid, None   # pause so the screen can draw this step
```

Because of `yield`, the function becomes a generator: it hands its current state to the drawing code, waits, and then continues from exactly where it stopped. A timer asks for the next step once per second. The drawing code never needs to know how the search works, only what the current `lo`, `hi` and `mid` are.

## Tweaking it

These are near the top of `binary_search_simple.py`:

| Setting | What it does | Default |
|---------|--------------|---------|
| `STEP_MS` | Time between steps, in milliseconds | 1000 |
| `PAUSE_MS` | How long the result stays on screen | 2500 |
| `N` | How many boxes in the array | 16 |

If you raise `N`, widen `WIDTH` too, or the boxes get cramped.

## Troubleshooting

- **`No module named pygame`**: run `python -m pip install pygame` so it installs for the same Python you're running.
- **Font looks slightly different**: the program asks for a monospace font (Consolas, Menlo, and so on) and falls back to whatever your system has. Nothing is wrong.
