from src.ai import playerguess
from src.game import ProblemLibs, randproblem
from random import randint

# plib = [ProblemLibs.easy, ProblemLibs.mideasy, ProblemLibs.mid][randint(0, 2)]
plib = ProblemLibs.easy
p = randproblem(plib)
q = "question"
a = ""
counter = 0

def main() -> None:
    global p, q, a, counter
    while q and a != "CORRECT":
        counter += 1
        q = input(f"第 {counter} 次提问 > ")
        a = playerguess(p, q)
        print(a)
    print(f"游戏结束 答案：{p}")

if __name__ == "__main__":
    print("\033[91m由于题库优化，run-terminal.py不再可用。\033[0m")
    # main()