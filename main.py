from utils.simulator import Simulator
from utils.vix import VixCenter


def main():
    simulator = Simulator()
    simulator.execute_vix_rsi()

if __name__ == "__main__":
    main()