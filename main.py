
import sys
from agent.orchestrator import Agent

def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "your question here"')
        sys.exit(1)
    q = " ".join(sys.argv[1:])
    print(Agent().answer(q))

if __name__ == "__main__":
    main()