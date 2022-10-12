# imports
import pandas as pd
import matplotlib.pyplot as plt
import os

# main class
class main:
    # constructor for main class
    def __init__(
        self, path_to_csvs="src/ubc-pair-grade-data-master/tableau-dashboard"
    ):  # takes in path to csvs
        self.PATH = path_to_csvs  # path to csvs
        self.DEBUG_MODE = True  # for debugging purposes

    # specify campus and course code
    def specify(self):
        CAMPUS = input("CAMPUS: ")
        while CAMPUS != "UBCV" and CAMPUS != "UBCO":
            print("Invalid campus.")
            CAMPUS = input("CAMPUS: ")

        COURSE_CODE = input("COURSE CODE: ")
        return CAMPUS, COURSE_CODE

    def read(self, CAMPUS, COURSE_CODE):
        LIST_DF = []
        self.COURSE_DETAIL = COURSE_CODE.split(" ")
        self.PATH = os.path.join(self.PATH, CAMPUS)
        for root, dir, file in os.walk(self.PATH):
            for name in file:
                if self.COURSE_DETAIL[0] in name:
                    self.PATH = os.path.join(root, name)
                    df = pd.read_csv(self.PATH, index_col=None, header=0)
                    LIST_DF.append(df)
        self.df = pd.concat(LIST_DF, axis=0, ignore_index=True)

    def filter_df(self):
        self.df = self.df.loc[
            (self.df["Course"] == int(self.COURSE_DETAIL[1]))
            & (self.df["Section"] == "OVERALL")
        ]
        self.df = self.df[
            [
                "Year",
                "Avg",
            ]
        ]
        if self.DEBUG_MODE:
            print(self.df)

    def draw(self):
        self.df.plot(
            x="Year",
            y="Avg",
            kind="scatter",
        )
        plt.show()
        if self.DEBUG_MODE:
            print(self.df.describe())

    def main(self):
        CAMPUS, COURSE_CODE = self.specify()
        self.read(CAMPUS, COURSE_CODE)
        self.filter_df()
        self.draw()


if __name__ == "__main__":
    main = main()
    main.main()
