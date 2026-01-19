from random import randint

def load(name:str) -> list[str]:
    with open(f"config/problems/{name}.txt", "r", encoding="utf-8") as f:
        rawdata = f.read().strip().split("\n")
    data = []
    for line in rawdata:
        data.append(line.strip())
    return data

class ProblemLibs:
    easy = load("easy")
    mideasy = load("mid-easy")
    mid = load("mid")

def randproblem(problemlib:list[str]) -> str:
    return problemlib[randint(0, len(problemlib) - 1)]