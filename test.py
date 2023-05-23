import pandas as pd

data = {-2.0: [0.0], -1.0: [-1.0, 0.0, 0.0, 1.0], 1.0: [0.0, 0.0, -1.0, 1.0], 0.0: [0.0, 1.0, 0.0, 0.0, -1.0], 2.0: [0.0]}
columns_ordered = sorted([key for key in data.keys()])
print(columns_ordered)
df = pd.DataFrame(index=sorted(set(val for sublist in data.values() for val in sublist)), columns=columns_ordered)

for key, values in data.items():
    column_name = key
    df[column_name] = 0  # Initialize column with zeros
    for value in values:
        df.loc[value, column_name] += 1

print(df)