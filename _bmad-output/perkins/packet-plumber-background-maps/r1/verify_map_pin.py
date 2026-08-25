#!/usr/bin/env python3
# Independent reimplementation of app/render/map.odin (story 7.4) — Perkins verification.
# Reproduces: per-cell classification + FNV-1a-64 cells hash, to check MAP_IDENTITY_PIN
# and the PR-body land/water/park percentages. Pure IEEE f32 via numpy float32.
import numpy as np, sys

M = (1 << 64) - 1
DELTA  = 0x9E3779B97F4A7C15
GAMMA1 = 0xBF58476D1CE4E5B9
GAMMA2 = 0x94D049BB133111EB
F32 = np.float32

def map_hash(seed, x, y):
    z = (seed ^ ((x * DELTA) & M) ^ ((y * GAMMA2) & M)) & M
    z = ((z ^ (z >> 30)) * GAMMA1) & M
    z = ((z ^ (z >> 27)) * GAMMA2) & M
    return (z ^ (z >> 31)) & M

def hash_unit(z):
    return F32(z >> 40) / F32(1 << 24)  # exact operands; one rounding

def value_noise(seed, x, y, cell_px):
    gx, gy = x // cell_px, y // cell_px
    fx = F32(x - gx * cell_px) / F32(cell_px)
    fy = F32(y - gy * cell_px) / F32(cell_px)
    sx = fx * fx * (F32(3.0) - F32(2.0) * fx)
    sy = fy * fy * (F32(3.0) - F32(2.0) * fy)
    h00 = hash_unit(map_hash(seed, gx, gy))
    h10 = hash_unit(map_hash(seed, gx + 1, gy))
    h01 = hash_unit(map_hash(seed, gx, gy + 1))
    h11 = hash_unit(map_hash(seed, gx + 1, gy + 1))
    top = h00 + (h10 - h00) * sx
    bot = h01 + (h11 - h01) * sx
    return top + (bot - top) * sy

LAND_LEVEL = F32(0.38)   # MAP_LAND_LEVEL (f32 context)
PARK_LEVEL = F32(0.72)   # MAP_PARK_LEVEL
W, H = 1040, 780         # 40x30 tiles x 26px

def generate(seed):
    water = np.zeros((H, W), dtype=np.uint8)
    for y in range(H):
        for x in range(W):
            if value_noise(seed, x, y, 72) < LAND_LEVEL:
                water[y, x] = 1
    near = np.zeros((H, W), dtype=np.uint8)
    for y in range(H):
        for x in range(W):
            if water[y, x]:
                for dy in (-1, 0, 1):
                    yy = y + dy
                    if yy < 0 or yy >= H: continue
                    for dx in (-1, 0, 1):
                        xx = x + dx
                        if xx < 0 or xx >= W: continue
                        near[yy, xx] = 1
    park_seed = (seed ^ DELTA) & M
    cells = np.zeros(H * W, dtype=np.uint8)
    for y in range(H):
        for x in range(W):
            i = y * W + x
            if water[y, x]:        cells[i] = 0  # Water
            elif near[y, x]:       cells[i] = 2  # Coast
            elif value_noise(park_seed, x, y, 120) >= PARK_LEVEL:
                                    cells[i] = 3  # Park
            else:                  cells[i] = 1  # Land
    return cells

def fnv(cells):
    h = 14695981039346656037
    for b in cells:
        h = ((h ^ int(b)) * 0x100000001B3) & M
    return h

for seed in (7, 8, 1234, 42):
    cells = generate(seed)
    names = {0: "water", 1: "land", 2: "coast", 3: "park"}
    counts = {names[k]: int((cells == k).sum()) for k in names}
    n = len(cells)
    pin = fnv(cells)
    print(f"seed {seed}: pin=0x{pin:016X}  " +
          "  ".join(f"{k}={v} ({100.0*v/n:.1f}%)" for k, v in counts.items()))
