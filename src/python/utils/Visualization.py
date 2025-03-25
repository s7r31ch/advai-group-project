import matplotlib.pyplot as plt

class Visualization:
    def __init__(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-100, 100)  # x轴范围
        ax.set_ylim(-1, 1)  # x轴范围
        ax.yaxis.set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_position('center')
        self.point, = ax.plot([], [], 'ro')
        plt.ion()
        plt.draw()
        fig.canvas.manager.set_window_title("Monitor | Error on X-axis")
        plt.show()
        
    def show(self):
        plt.show()
    
    