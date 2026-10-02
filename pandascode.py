import random

import pandas as pd

# 좌석 만들기
rows = list("ABCDE")
cols = range(1, 9)

seats = pd.DataFrame(
    "□",
    index=rows,
    columns=cols
)

## 좌석
# seats.loc["A", 3] = "■"
# seats.loc["B", 5] = "■"
# seats.loc["C", 2] = "■"

random_percent = 20
if not 0 <= random_percent <= 100:
    raise ValueError("random_percent는 0에서 100 사이여야 합니다.")

empty_seats = [
    (row, col)
    for row in seats.index
    for col in seats.columns
    if seats.loc[row, col] == "□"
]
random_seat_count = min(int(seats.size * random_percent / 100), len(empty_seats))
for row, col in random.sample(empty_seats, random_seat_count):
    seats.loc[row, col] = "■"

cinema_name = "용산"
movie_name = "탑건"

seats.to_csv(f"C:\\Users\\seongyong\\git\\data\\{cinema_name}_{movie_name}_seats.csv", encoding="utf-8-sig")

seats.iloc[:, :] = "□"
print(seats)


