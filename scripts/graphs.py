import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    df = pd.read_excel("final_df/emails.xlsx")
    grouped_sector = df.groupby("sector").count().sort_values("email")[["email"]]
    fig, axs = plt.subplots(figsize=(20, 24))
    kind = "box"
    grouped_sector.plot(y="email", kind=kind, ax=axs)
    fig.savefig(f"figures/emails_{kind}.png")
