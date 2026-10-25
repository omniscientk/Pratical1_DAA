
import random
import sys

import pygame

WIDTH, HEIGHT = 1000, 340
MARGIN = 40
N = 16
STEP_MS = 1000      # time per step
PAUSE_MS = 2500     # pause on the result before the next search

BG = (18, 20, 28)
TEXT = (230, 233, 240)
CANDIDATE = (80, 140, 235)
MID = (250, 215, 70)
OUT = (45, 48, 62)
OUT_TEXT = (95, 100, 120)
FOUND = (90, 220, 130)
MISSING = (235, 100, 100)


def search_steps(arr, target):
    """Yield (lo, hi, mid, result) for every step."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        yield lo, hi, mid, None            # looking at mid
        if arr[mid] == target:
            yield lo, hi, mid, "found"
            return
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
        yield lo, hi, None, None           # range shrinks
    yield lo, hi, None, "missing"


def new_search(arr):
    """Same array every time, only the target changes."""
    if random.random() < 0.8:
        target = random.choice(arr)
    else:
        target = random.choice([x for x in range(1, 100) if x not in arr])
    return target, search_steps(arr, target)


def main():
    pygame.init()
    pygame.display.set_caption("Binary Search")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    names = "consolas,menlo,dejavusansmono,couriernew,monospace"
    f_big = pygame.font.SysFont(names, 28, bold=True)
    f_num = pygame.font.SysFont(names, 22, bold=True)
    f_small = pygame.font.SysFont(names, 16)

    arr = sorted(random.sample(range(1, 100), N))   # created only once
    target, steps = new_search(arr)
    lo, hi, mid, result = 0, N - 1, None, None
    timer = 0
    slot = (WIDTH - 2 * MARGIN) / N

    while True:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # advance the animation
        timer += dt
        if timer >= (PAUSE_MS if result else STEP_MS):
            timer = 0
            if result:
                target, steps = new_search(arr)
                lo, hi, mid, result = 0, N - 1, None, None
            else:
                lo, hi, mid, result = next(steps)

        # draw
        screen.fill(BG)
        label = f_big.render(f"Find {target}", True, MID)
        screen.blit(label, (MARGIN, 30))

        pointers = {}
        for name, idx in (("lo", lo), ("mid", mid), ("hi", hi)):
            if idx is not None and 0 <= idx < N:
                pointers.setdefault(idx, []).append(name)

        for i, v in enumerate(arr):
            r = pygame.Rect(MARGIN + i * slot + 3, 130, slot - 6, 64)
            if result == "found" and i == mid:
                color, tcolor = FOUND, BG
            elif i == mid:
                color, tcolor = MID, BG
            elif not (lo <= i <= hi):
                color, tcolor = OUT, OUT_TEXT
            else:
                color, tcolor = CANDIDATE, TEXT
            pygame.draw.rect(screen, color, r, border_radius=8)
            img = f_num.render(str(v), True, tcolor)
            screen.blit(img, img.get_rect(center=r.center))

        for i, names_ in pointers.items():
            cx = MARGIN + i * slot + slot / 2
            pygame.draw.polygon(screen, TEXT, [(cx, 204), (cx - 6, 216), (cx + 6, 216)])
            img = f_small.render("/".join(names_), True, TEXT)
            screen.blit(img, img.get_rect(midtop=(cx, 220)))

        if result:
            msg = "FOUND" if result == "found" else "NOT FOUND"
            col = FOUND if result == "found" else MISSING
            img = f_big.render(msg, True, col)
            screen.blit(img, img.get_rect(midtop=(WIDTH // 2, 270)))

        pygame.display.flip()


if __name__ == "__main__":
    main()
