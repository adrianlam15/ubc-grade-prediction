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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


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
        if self.DEBUG_MODE:
            CAMPUS = "UBCV"
            COURSE_CODE = "CPSC 110"
        else:
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
        # for debugging purposes
        if self.DEBUG_MODE:
            choice = input("Print course data? (y/n): ")
            if choice == "y":
                print(f"\n{self.df}")

    # DRAW FUNCTION
    def draw(self):
        # plot Avg (y) with respect to Year (x)
        self.df.plot(
            x="Year",
            y="Avg",
            kind="scatter",
        )
        plt.plot(self.X_TEST, self.avg_pred, color="red", linewidth=2)
        plt.show()

    # STATISTICS FUNCTION
    def stats(self):
        SEED = 42
        self.TRAIN, self.TEST = train_test_split(
            self.df, test_size=0.3, random_state=SEED
        )
        self.X = self.df["Year"]  # returns Year Series object
        self.y = self.df.Avg
        # plt.show()

    # REGRESSION FUNCTION
    def regression(self):
        self.regressor = LinearRegression()

        self.X_TRAIN = self.TRAIN["Year"].values.reshape(-1, 1)
        self.Y_TRAIN = self.TRAIN["Avg"].values.reshape(-1, 1)
        self.X_TEST = self.TEST["Year"].values.reshape(-1, 1)
        self.Y_TEST = self.TEST["Avg"].values.reshape(-1, 1)

        self.regressor.fit(self.X_TRAIN, self.Y_TRAIN)
        self.avg_pred = self.regressor.predict(self.X_TEST)
        if self.DEBUG_MODE:
            df_preds = pd.DataFrame(
                {"Actual": self.Y_TEST.squeeze(), "Predicted": self.avg_pred.squeeze()}
            )
            print(df_preds)

    # PREDICT FUNCTION
    def predict(self):
        year = int(input("\nYear for prediction: "))
        pred_avg = self.regressor.predict([[year]])
        print(pred_avg.squeeze().round(2))

    # MAIN FUNCTION
    def main(self):
        CAMPUS, COURSE_CODE = self.specify()
        self.read(CAMPUS, COURSE_CODE)
        self.filter_df()
        self.stats()
        self.regression()
        self.predict()
        self.draw()


# MAIN PROGRAM RUN ---------------------------------------------------------------------
if __name__ == "__main__":
    main = main()
    main.main()
