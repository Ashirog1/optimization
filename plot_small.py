import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os
import time


def plot(labels, ra, rb, rc, rd, name):
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - 2*width,ra, width, label='IP')
    rects2 = ax.bar(x - width,rb, width, label='CP')
    rects3 = ax.bar(x,rc, width, label='Local Search')
    rects4 = ax.bar(x + width,rd, width, label='Greedy')
    print(ra, rb,rc,rd)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Result')
    ax.set_title('Small dataset')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate(text='',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects4)

    fig.tight_layout()

    plt.savefig("Plot/" + str(name)+".png")


def run(labels,name):
    programs = ['ip.py', 'cp.py', 'localsearch.py', 'greedy.py']

    folder = 'Data/'
    input_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    program_input_map = {p: None for p in programs}

    results = []
    for i in range(4):
        results.append([])
    times = []
    for i in range(4):
        times.append([])

    for input in labels:
        for id, program in enumerate(programs):
            input_file = folder + input + ".txt"
            with open(input_file, 'r') as f:
                input_data = f.read()
            # print(input_data)
            # result = np.array([float(x) for x in output.split()])
            start = time.perf_counter()
            process = subprocess.Popen(["python", program], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            output_data, _ = process.communicate(input=input_data.encode())

            # print(output_data.decode())
            results[id].append(int(output_data.decode()))
            end = time.perf_counter()
            times[id].append(round(end-start, 2))
            

    # for i, result in enumerate(results):
    #     np.save(f'result{i}.npy', result)
    print(results)
    print(times)
    plot(labels, results[0], results[1],results[2], results[3], name+"acc")
    plot(labels, times[0], times[1], times[2], times[3], name+"time")

if __name__ == '__main__':
    run(['5', '10', '15', '20', '25', '30', '35', '40'], "test")