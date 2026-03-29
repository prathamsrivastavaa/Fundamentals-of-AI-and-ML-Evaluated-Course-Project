import time
import csv
from datetime import datetime

def setup_file():
    try:
        with open("traffic_data.csv", "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Time", "Road A", "Road B", "Road C", "Road D",
                "Priority Road", "Emergency"
            ])
    except FileExistsError:
        pass


def log_data(roads, priority, emergency):
    with open("traffic_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            roads["A"],
            roads["B"],
            roads["C"],
            roads["D"],
            priority,
            emergency
        ])


def get_signal_time(cars):
    if cars == 0:
        return 3

    base_time = 5
    time_per_car = 1.2
    buffer = 2

    total_time = base_time + (cars * time_per_car) + buffer
    return min(int(total_time), 40)


def show_countdown(seconds):
    for sec in range(seconds, 0, -1):
        print(f"⏳ {sec} sec remaining", end="\r")
        time.sleep(1)
    print(" " * 30, end="\r")


def display_data():
    print("\n📊 Stored Traffic Data:\n")
    try:
        with open("traffic_data.csv", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No data available yet.")


def find_peak_hour():
    try:
        highest_traffic = 0
        peak_time = ""

        with open("traffic_data.csv", "r") as file:
            next(file)

            for line in file:
                data = line.strip().split(",")

                total_cars = (
                    int(data[1]) +
                    int(data[2]) +
                    int(data[3]) +
                    int(data[4])
                )

                if total_cars > highest_traffic:
                    highest_traffic = total_cars
                    peak_time = data[0]

        print("\n⏰ Peak Traffic Details")
        print("------------------------")
        print(f"Time: {peak_time}")
        print(f"Total Vehicles: {highest_traffic}")

    except FileNotFoundError:
        print("No data available.")


def run_traffic_system():
    setup_file()

    print("🚦 Smart Traffic Signal System")

    while True:
        try:
            print("\nEnter number of vehicles on each road:")

            roads = {
                "A": int(input("Road A: ")),
                "B": int(input("Road B: ")),
                "C": int(input("Road C: ")),
                "D": int(input("Road D: "))
            }

        except ValueError:
            print("❌ Please enter valid numbers only.")
            continue

        emergency = input(
            "Emergency vehicle on which road? (A/B/C/D or N): "
        ).upper()

        print("\n--- Signal Cycle Starting ---")

        if emergency in roads:
            print(f"\n🚑 Emergency on Road {emergency}! Giving priority.")
            order = [emergency] + [r for r in roads if r != emergency]
            priority = emergency
        else:
            order = sorted(roads, key=roads.get, reverse=True)
            priority = order[0]

        log_data(roads, priority, emergency)

        for road in order:
            green_time = get_signal_time(roads[road])

            print(f"\n🟢 Road {road} GREEN for {green_time} sec")

            for r in roads:
                if r != road:
                    print(f"🔴 Road {r} RED")

            show_countdown(green_time)

            print("\nSwitching signals...\n")
            time.sleep(1)

        print("\n--- Cycle Completed ---")

        choice = input("""
Options:
1. Continue
2. Show Data
3. Peak Hour
4. Exit
Choose: """)

        if choice == "2":
            display_data()
        elif choice == "3":
            find_peak_hour()
        elif choice == "4":
            print("\nExiting system. Goodbye!")
            break

if __name__ == "__main__":
    run_traffic_system()
