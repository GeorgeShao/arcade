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


def create_stress_test_comparison_results_chart():
    r1 = read_results("arcadeplus/examples/perf_test/arcade_results.csv")
    r2 = read_results("arcadeplus/examples/perf_test/arcadeplus_results.csv")

    sprite_count = [row[LINE_COUNT] for row in r1]
    d1 = [row[FPS] for row in r1]
    d2 = [row[FPS] for row in r2]

    # Plot our results
    plt.title("Line Drawing Stress Test - Arcade vs. ArcadePlus")
    plt.plot(sprite_count, d1, label="Arcade")
    plt.plot(sprite_count, d2, label="ArcadePlus")

    plt.legend(loc='lower left', shadow=True, fontsize='medium')

    plt.ylabel('Frames Per Second (FPS) - Higher is Better')
    plt.xlabel('# of Lines Drawn')

    # plt.show()
    plt.savefig("arcadeplus/examples/perf_test/stress_test_comparison_results.svg")
    plt.clf()

create_stress_test_comparison_results_chart()
