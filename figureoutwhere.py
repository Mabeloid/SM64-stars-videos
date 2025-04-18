import json
import random

with open("figuringoutwhere/stars.json", "r", encoding="utf-8") as f:
    starsLUT: dict[tuple[int, int], str] = {
        tuple(v): k
        for k, v in json.load(f).items()
    }
with open("figuringoutwhere/enemies.json", "r", encoding="utf-8") as f:
    enemyLUT: dict[str, list[int]] = json.load(f)
with open("figuringoutwhere/courses.json", "r", encoding="utf-8") as f:
    coursesLUT: dict[str, int] = json.load(f)


def inc(probs: dict[tuple[int, int], int], AB: tuple[int, int], by: int = 1):
    if AB in probs: probs[AB] += by
    else: probs[AB] = 1


def figureoutwhere(text: str, printranking: bool = False) -> tuple[int, int]:
    text = text.lower()
    for c in ".,:?!()[]{}-":
        text = text.replace(c, " ")

    for coursename, COURSE in coursesLUT.items():
        if not coursename.lower() in text: continue
        STAR = random.choice(range(1, 6 + 1))
        return COURSE, STAR

    probs: dict[tuple[int, int], int] = {}
    for word in text.split(" "):
        for AB, starname in starsLUT.items():
            if word in starname: inc(probs, AB)

    for enemy, courses in enemyLUT.items():
        if not enemy.lower() in text: continue
        for A in courses:
            for B in range(1, 6 + 1):
                inc(probs, (A, B), by=1)

    if not probs:
        COURSE = random.choice(range(1, 15 + 1))
        STAR = random.choice(range(1, 6 + 1))
        return COURSE, STAR

    probs = {k: v for k, v in probs.items() if v == max(probs.values())}

    if printranking:
        D = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)
        for (AB, count) in D:
            print(f"{AB}".ljust(6), f"{count}pts".rjust(5),
                  starsLUT[AB].rjust(35))

    COURSE, STAR = random.choice([*probs.keys()])
    return COURSE, STAR


if __name__ == "__main__":
    print()
    text = "funny ukiki monkey star? with a cage perhaps?"
    print(f"{text = }")
    COURSE, STAR = figureoutwhere(text, printranking=True)
    print(f"{COURSE = }")
    print(f"{STAR = }")

    print()
    text = "The Red Coins are Mysterious and Important"
    print(f"{text = }")
    COURSE, STAR = figureoutwhere(text, printranking=True)
    print(f"{COURSE = }")
    print(f"{STAR = }")
