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

# TODO: 实现带权重的随机难度，例如 randproblem(0.2, 0.6, 0.2) 对应从easy、mid-easy、mid三个难度的题目池中随机选取一个并从中随机选取一个题目，其中三个题目池的随机权重（即被选中的概率）分别为20%、60%、20%。