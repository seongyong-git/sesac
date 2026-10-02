import pandas as pd

# 좌석 만들기
rows = list("ABCDE")
cols = range(1, 9)

seats = pd.DataFrame(
    "□",
    index=rows,
    columns=cols
)

print(seats)




seats.loc["A", 3] = "■"
seats.loc["B", 5] = "■"
seats.loc["C", 2] = "■"


seat = input("좌석을 선택하세요 (예: A3): ")

row = seat[0]
col = int(seat[1:])

if seats.loc[row, col] == "□":
    print("좌석이 선택되었습니다.")
elif seats.loc[row, col] = "■":
    print("이미 예약된 좌석입니다.")

print(seats)
