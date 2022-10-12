# Program by Adrian, Lam - 10/12/2022

# DESCRIPTION --------------------------------------------------------------------------
#
# This program contains the necessary classes, functions, and imports to fetch UBC grade
# data from https://github.com/DonneyF/ubc-pair-grade-data and displays it as a scatter
# plot (thanks Donney F!).


# FUTURE IMPLEMENATIONS ----------------------------------------------------------------
# - Machine Learning to predict grades
# - Add more data
# - Website (hopefully)
# - Instead of storing data locally, fetch it from https://github.com/DonneyF/ubc-pair-grade-data


# IMPORTS ------------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import os


# MAIN CLASS ---------------------------------------------------------------------------
class main:
    # CONSTRUCTOR - initialize variables
    def __init__(
        self, path_to_csvs="src/ubc-pair-grade-data-master/tableau-dashboard"
    ):  # takes in path to csvs
        self.PATH = path_to_csvs  # path to csvs
        self.DEBUG_MODE = True  # for debugging purposes

    # SPECIFY CAMPUS AND COURSE CODE FUNCTION
    def specify(self):
        CAMPUS = input("CAMPUS: ")
        # input validation
        while CAMPUS != "UBCV" and CAMPUS != "UBCO":
            print("Invalid campus.")
            CAMPUS = input("CAMPUS: ")
        COURSE_CODE = input("COURSE CODE: ")
        return CAMPUS, COURSE_CODE

    # SETS CSV FILE GIVEN ARGS & READS CSV FILE FUNCTION
    def read(self, CAMPUS, COURSE_CODE):
        LIST_DF = []
        self.COURSE_DETAIL = COURSE_CODE.split(" ")
        self.PATH = os.path.join(self.PATH, CAMPUS)
        # gets root, dir, file names in path
        for root, dir, file in os.walk(self.PATH):
            for name in file:
                if self.COURSE_DETAIL[0] in name:  # if course name is in file name
                    self.PATH = os.path.join(root, name)
                    df = pd.read_csv(
                        self.PATH, index_col=None, header=0
                    )  # turn csv file to data frame
                    LIST_DF.append(df)  # adds data frame to list
        self.df = pd.concat(
            LIST_DF, axis=0, ignore_index=True
        )  # list of all data frame -> one data frame

    # FILTER DATA FRAME FUNCTION
    def filter_df(self):
        # selects data frame with course code in "Course" column and data frames with "OVERALL" in Section column
        self.df = self.df.loc[
            (self.df["Course"] == int(self.COURSE_DETAIL[1]))
            & (self.df["Section"] == "OVERALL")
        ]
        # drops unnecessary columns
        self.df = self.df[
            [
                "Year",
                "Avg",
            ]
        ]
        # for debugging purpoeses
        if self.DEBUG_MODE:
            print(self.df)

    # DRAW FUNCTION
    def draw(self):
        # plot Avg (y) with respect to Year (x)
        self.df.plot(
            x="Year",
            y="Avg",
            kind="scatter",
        )
        plt.show()  # show plotted graph
        # for debugging purposes
        if self.DEBUG_MODE:
            print(self.df.describe())  # describes the data frame

    # STATISTICS FUNCTION
    def stats(self):
        self.df.describe()

    # MAIN FUNCTION
    def main(self):
        CAMPUS, COURSE_CODE = self.specify()
        self.read(CAMPUS, COURSE_CODE)
        self.filter_df()
        self.draw()


# MAIN PROGRAM RUN ---------------------------------------------------------------------
if __name__ == "__main__":
    main = main()
    main.main()
