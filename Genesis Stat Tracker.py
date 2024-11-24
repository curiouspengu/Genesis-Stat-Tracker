import pathlib
import sys
from data import config
sys.dont_write_bytecode = True
sys.path.append(pathlib.Path(__file__).parent.resolve())
from ahk import AHK
def main():
    from data import main_loop
    main_loop.start()

if __name__ == "__main__":
    main()


    