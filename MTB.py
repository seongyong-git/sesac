import os
from pathlib import Path

import pandas as pd
from movie_pamphlet import print_movie_menu, print_movie_pamphlet

def clear_console():
    os.system("cls")

clear_console()

data_dir = Path(__file__).resolve().parent / "data"
movies_by_theater = {}

for csv_file in sorted(data_dir.glob("*.csv")):
    name_parts = csv_file.stem.split("_")
    if len(name_parts) < 2:
        continue

    theater_name, movie_name = name_parts[:2]
    movies_by_theater.setdefault(theater_name, []).append(movie_name)


print("영화 목록:")
  

def print_options(title, options):
    print(title)
    for number, option in enumerate(options, start=1):
        print(f"{number}. {option}")


def get_number_choice(prompt, option_count):
    while True:
        try:
            choice = int(input(prompt))
        except ValueError:
            choice = 0

        if 1 <= choice <= option_count:
            return choice
        print("목록에 있는 번호를 입력하세요.")


class ReservationApp:
    def __init__(self, data_dir=None):
        self.data_dir = data_dir or Path(__file__).resolve().parent / "data"
        self.movies_by_theater = self.load_movies()
        self.reservation_data = {}


    def load_movies(self):
        movies_by_theater = {}
        for csv_file in sorted(self.data_dir.glob("*.csv")):
            name_parts = csv_file.stem.split("_")
            if len(name_parts) < 2:
                continue

            theater_name, movie_name = name_parts[:2]
            movies_by_theater.setdefault(theater_name, []).append(movie_name)
        return movies_by_theater

    def choose_movie(self):
        movies = sorted(
            {movie for movie_list in self.movies_by_theater.values() for movie in movie_list}
        )
        if not movies:
            print(f"영화 CSV 파일이 없습니다: {self.data_dir}")
            return None

        print_movie_menu(movies)
        return movies[get_number_choice("영화 번호를 선택하세요: ", len(movies)) - 1]

    def choose_theater(self, movie):
        theaters = [
            theater
            for theater, movies in self.movies_by_theater.items()
            if movie in movies
        ]
        print_options(f"{movie} 상영관 목록:", theaters)
        theater_number = get_number_choice("상영관 번호를 선택하세요: ", len(theaters))
        return theaters[theater_number - 1]

    def load_seats(self, theater, movie):
        seats_path = self.data_dir / f"{theater}_{movie}_seats.csv"
        seats = pd.read_csv(seats_path, index_col=0)
        seats.columns = seats.columns.astype(int)
        return seats, seats_path

    def choose_people_count(self, seats):
        available_count = int((seats == "□").to_numpy().sum())
        while True:
            try:
                people_count = int(input("예매 인원수를 입력하세요: "))
            except ValueError:
                people_count = 0

            if 1 <= people_count <= available_count:
                return people_count
            print(f"인원수는 1명 이상 {available_count}명 이하로 입력하세요.")

    def choose_seats(self, seats, people_count):
        selected_seats = []
        while len(selected_seats) < people_count:
            seat = input(
                f"좌석 {len(selected_seats) + 1}/{people_count}을(를) 선택하세요: "
            ).strip().upper()
            try:
                row, column = seat[0], int(seat[1:])
            except (ValueError, IndexError):
                print("좌석을 A3 형식으로 입력하세요.")
                continue

            if row not in seats.index or column not in seats.columns:
                print("좌석표에 있는 좌석을 입력하세요.")
                continue
            if seats.loc[row, column] != "□" or seat in selected_seats:
                print("이미 선택되었거나 예약된 좌석입니다.")
                continue

            seats.loc[row, column] = "■"
            selected_seats.append(seat)
            print(f"{seat} 좌석이 선택되었습니다.")

        return selected_seats

    def get_seat_price(self, selected_seats):
        price_per_seat = 10000
        vip_seats = {"C3", "C4", "C5", "C6", "D3", "D4", "D5", "D6"}
        for seat in selected_seats:
            if seat in vip_seats:
                price_per_seat = 15000
                break

        total_price = price_per_seat * len(selected_seats)
        return total_price

    def cancel_reservation(self, seats, selected_seats):
        
        for seat in selected_seats:
            row, column = seat[0], int(seat[1:])
            seats.loc[row, column] = "□"
        print(f"선택된 좌석 {', '.join(selected_seats)} 예약이 취소되었습니다.")


    def run(self):
        clear_console()
        movie = self.choose_movie()
        if movie is None:
            return

        clear_console()
        print_movie_pamphlet(movie)
        theater = self.choose_theater(movie)
        seats, seats_path = self.load_seats(theater, movie)

        clear_console()
        print(f"선택된 영화: {movie}")
        print(f"선택된 상영관: {theater}\n")
        people_count = self.choose_people_count(seats)

        clear_console()
        print(f"선택된 영화: {movie}")
        print(f"선택된 상영관: {theater}")
        print(f"예매 인원수: {people_count}명\n")
        print(f"{theater} {movie} 좌석표:")
        print(seats)

        selected_seats = self.choose_seats(seats, people_count)
        clear_console()
        print(f"선택된 영화: {movie}")
        print(f"선택된 상영관: {theater}")
        print(f"예매 인원수: {people_count}명")
        print(f"선택된 좌석: {', '.join(selected_seats)}\n")
        print(seats)

        print(f"총 결제 금액: {self.get_seat_price(selected_seats)}원 \n")

        self.reservation_data = {
            "movie": movie,
            "theater": theater,
            "people_count": people_count,
            "selected_seats": selected_seats,
            "seats": seats,
        }

        print("예약이 완료되었습니다.")
        # 예약 결과를 파일에 반영하려면 아래 줄의 주석을 해제하세요.
        # seats.to_csv(seats_path, encoding="utf-8-sig")

        print(f"1. 예매하기 2. 예약 취소 3. 종료")
        selection = input("선택하세요: ")

        if selection == "1":            
            self.run()
        elif selection == "2":
            clear_console()
    
            cancel_app = cancel_reservation(self.reservation_data)
            cancel_app.cancel()
        elif selection == "3":
            print("프로그램을 종료합니다.")
            raise SystemExit
        

        self.reservation_data["seats"].to_csv(seats_path, encoding="utf-8-sig")               



class cancel_reservation(ReservationApp):
    def __init__(self, reservation_data):
        self.reservation_data = reservation_data

    def cancel(self):
        for seat in self.reservation_data["selected_seats"]:
            row, column = seat[0], int(seat[1:])
            self.reservation_data["seats"].loc[row, column] = "□"
        print(f"선택된 좌석 {', '.join(self.reservation_data['selected_seats'])} 예약이 취소되었습니다.\n")
        print(self.reservation_data["seats"])
    
        print(f"\n1. 예매하기 2. 종료\n")
        selection = input("선택하세요: ")

        if selection == "1":
            ReservationApp().run()        
            
        elif selection == "2":      
            print("프로그램을 종료합니다.\n")
            raise SystemExit


if __name__ == "__main__":
    ReservationApp().run()








