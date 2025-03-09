import pandas as pd
from pydantic import BaseModel
from main import SwifitORM


def main():
    orm = SwifitORM(
        backend="postgres"

    )



if __name__ == '__main__':
    main()


