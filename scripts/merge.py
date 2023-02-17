import pandas as pd
import os

from glob import glob


def excels(path_to_dir):
    all_dirs = os.listdir(path_to_dir)
    all_dirs.remove("category_pages")
    df_frames = []

    for dirname in all_dirs:
        xlsx_file = os.path.join(path_to_dir, dirname, "excels", f"{dirname}.xlsx")
        df_sub = pd.read_excel(xlsx_file, engine="openpyxl")
        df_frames.append(df_sub)

    super_df = pd.concat(df_frames)
    super_df.drop_duplicates(subset="email", inplace=True)
    super_df.to_excel("/home/<YOUR PATH>/final_df/emails.xlsx", index=False)


if __name__ == "__main__":
    path = "/home/<YOUR PATH>/data"
    excels(path)
