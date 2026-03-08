import asyncio

# https://www.youtube.com/watch?v=3_iZcoYrXOM

async def bresenham_low(x0, y0, x1, y1):
    points = [(x0, y0)]

    dy = y1 - y0
    dx = x1 - x0
    yi = 1

    if dy < 0:
        yi = -1
        dy = -dy

    ddy = 2 * dy
    ddx = 2 * dx

    value = 2 * (dy - dx)

    d = value
    y = y0

    for x in range(x0 + 1, x1 + 1):
        if d < 0:
            d += ddy
        else:
            d += value
            y += yi

        points.append((x, y))

    return points

async def bresenham_high(x0, y0, x1, y1):
    points = [(x0, y0)]

    dy = y1 - y0
    dx = x1 - x0
    xi = 1

    if dx < 0:
        xi = -1
        dx = -dx

    ddy = 2 * dy
    ddx = 2 * dx

    value = 2 * (dx - dy)

    d = value
    x = x0

    for y in range(y0 + 1, y1 + 1):
        if d < 0:
            d += ddx
        else:
            d += value
            x += xi

        points.append((x, y))

    return points

async def bresenham(x0, y0, x1, y1):
    result = []

    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            result = await bresenham_low(x1, y1, x0, y0)
        else:
            result = await bresenham_low(x0, y0, x1, y1)
    else:
        if y0 > y1:
            result = await bresenham_high(x1, y1, x0, y0)
        else:
            result = await bresenham_high(x0, y0, x1, y1)

    return result