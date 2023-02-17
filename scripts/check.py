import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    df = pd.read_excel("final_df/emails.xlsx")
    print(df[df['sector'] == "Food Products"].sort_values('sales'))
    # print(df.groupby("sector").count().sort_values("email").index.tolist())
