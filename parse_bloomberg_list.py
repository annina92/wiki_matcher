import pandas as pd

df = pd.read_csv("./bloomberg_perimeter_1000.csv")

print(list(df))

companies_list = list(df.LONG_COMP_NAME)


print(companies_list)