import csv
import matplotlib.pyplot as plt

LINE_COUNT = 1
FPS = 2

def read_results(filename):
    results = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            results.append([float(cell) for cell in row])
        return results


def chart_stress_test_draw_moving_process_comparison():
    r1 = read_results("arcade_results.csv")
    r2 = read_results("arcadeplus_results.csv")

    sprite_count = [row[LINE_COUNT] for row in r1]
    d1 = [row[FPS] for row in r1]
    d2 = [row[FPS] for row in r2]

    # Plot our results
    plt.title("Moving Sprites - Arcade vs. Pygame")
    plt.plot(sprite_count, d1, label="Processing Time Arcade")
    plt.plot(sprite_count, d2, label="Processing Time Pygame")

    plt.legend(loc='upper left', shadow=True, fontsize='x-large')

    plt.ylabel('Time')
    plt.xlabel('# of Lines')

    # plt.show()
    plt.savefig("chart_stress_test_draw_moving_process_comparison.svg")
    plt.clf()




def main():
    chart_stress_test_draw_moving_process_comparison()


main()