import sys
import matplotlib.pyplot as plt
import random
import math


class Point:
    def __init__(self, x=0, y=0, change=0):
        """
        :param x: X Value
        :param y: Y Value
        :param change: Conscience
        """
        self.x = x
        self.y = y
        self.change = change


class Index:
    def __init__(self, x=0, y=0):
        """
        :param x: X Value
        :param y: Y Value
        """
        self.x = x
        self.y = y


class Node:
    def __init__(self, point=Point(), index=Index(), adjacent=[]):
        """
        :param point: Point (X, Y)
        :param index: The point index in the matrix topology.
        :param adjacent: The current point neighbours - matrix topology.
        """
        self.point = point
        self.index = index
        self.adjacent = adjacent


def create_board(neurons):
    """
    :param neurons: 5x5 neurons (Total: 25)
    :return: Neurons arranged in a 5x5 topology.
    """
    board = [[Node() for i in range(5)] for j in range(5)]

    "Corners"
    board[0][0] = Node(neurons[0][0], Index(0, 0), [Index(0, 1), Index(1, 0)])
    board[0][4] = Node(neurons[0][4], Index(0, 4), [Index(0, 3), Index(1, 4)])
    board[4][0] = Node(neurons[4][0], Index(4, 0), [Index(3, 0), Index(4, 1)])
    board[4][4] = Node(neurons[4][4], Index(4, 4), [Index(3, 4), Index(4, 3)])

    for i in range(1, 4):
        "Edges"
        board[0][i] = Node(neurons[0][i], Index(0, i), [Index(0, i - 1), Index(1, i), Index(0, i + 1)])
        board[i][0] = Node(neurons[i][0], Index(i, 0), [Index(i - 1, 0), Index(i, 1), Index(i + 1, 0)])
        board[4][i] = Node(neurons[4][i], Index(4, i), [Index(4, i - 1), Index(3, i), Index(4, i + 1)])
        board[i][4] = Node(neurons[i][4], Index(i, 4), [Index(i - 1, 4), Index(i, 3), Index(i + 1, 4)])

        "General Case"
        for j in range(1, 4):
            board[i][j] = Node(neurons[i][j], Index(i, j), [Index(i, j-1), Index(i-1, j), Index(i, j+1), Index(i+1, j)])

    return board


def min_distance(point, neurons):
    """
    Function to find the minimum distance for tasks A & B
    :param point: Given Point
    :param neurons: Array of neurons
    :return: The closest neuron to the given point.
    """
    minimum = sys.maxsize
    index = 0
    for i in range(len(neurons)):
        if neurons[i].change == 0:
            distance = math.sqrt((point.x - neurons[i].x)**2 + (point.y - neurons[i].y)**2)
            if distance < minimum:
                minimum = distance
                index = i
    return index


def min_distance_board(point, board):
    """
    Function to find the minimum distance for task C
    :param point: Given Point
    :param board: Matrix of neurons
    :return: The closest neuron to the given point.
    """
    minimum = sys.maxsize
    index = Index()
    for i in range(len(board[0])):
        for j in range(len(board[0])):
            if board[i][j].point.change == 0:
                distance = math.sqrt((point.x - board[i][j].point.x) ** 2 + (point.y - board[i][j].point.y) ** 2)
                if distance < minimum:
                    minimum = distance
                    index = Index(i, j)
    return index


def update_conscience(index, neurons):
    """
    This function will reset the neurons conscience except for the closest neuron for tasks A & B.
    :param index: Index of the closest neuron
    :param neurons: Array of neurons
    :return: The updated neurons consciences.
    """
    for i in range(len(neurons)):
        if i != index:
            neurons[i].change = 0
    return neurons


def update_conscience_board(index, board):
    """
    This function will reset the neurons conscience except for the closest neuron for task C.
    :param index: Index of the closest neuron
    :param board: Matrix of neurons
    :return: The updated neurons consciences.
    """
    for i in range(len(board[0])):
        for j in range(len(board[0])):
            if i != index.x and j != index.y:
                board[i][j].point.change = 0
    return board


def move_algorithm(point, index, neurons, radius, task):
    """
    Algorithm for tasks A & B:
    - Given neurons with topology of a line / circle, moving the adjacent neurons using Gaussian Distribution.
    :param point: Given Point
    :param index: Index of the closest neuron
    :param neurons: Array of neurons
    :param radius: Number of adjacent neighbours.
    :param task: Task A / B
    :return: The updated neurons locations according to the given radius.
    """
    neurons[index].x += (point.x - neurons[index].x) / 2
    neurons[index].y += (point.y - neurons[index].y) / 2
    neurons[index].change = 1
    if task == "A":
        for i in range(1, radius + 1):
            i_right = index + i
            i_left = index - i
            delta = 1 / (2 ** (i + 1))
            if i_right < len(neurons):
                neurons[i_right].x += (point.x - neurons[i_right].x) * delta
                neurons[i_right].y += (point.y - neurons[i_right].y) * delta
                neurons[i_right].change = 1
            if i_left >= 0:
                neurons[i_left].x += (point.x - neurons[i_left].x) * delta
                neurons[i_left].y += (point.y - neurons[i_left].y) * delta
                neurons[i_left].change = 1

    elif task == "B":
        for i in range(1, radius + 1):
            i_right = (index + i) % len(neurons)
            i_left = index - i
            if i_left < 0:
                i_left += len(neurons)
            delta = 1 / (2 ** (i + 1))
            if i_left != i_right:
                neurons[i_left].x += (point.x - neurons[i_left].x) * delta
                neurons[i_left].y += (point.y - neurons[i_left].y) * delta
                neurons[i_left].change = 1

                neurons[i_right].x += (point.x - neurons[i_right].x) * delta
                neurons[i_right].y += (point.y - neurons[i_right].y) * delta
                neurons[i_right].change = 1

    return update_conscience(index, neurons)


def move_algorithm_board(point, index, board, radius):
    """
    Algorithm for task C: Given neurons with topology of a 5x5, moving the adjacent neurons using Gaussian Distribution.
    :param point: Given Point
    :param index: Index of the closest neuron
    :param board: Matrix of neurons
    :param radius: Number of adjacent neighbours.
    :return: The updated board locations according to the given radius.
    """
    board[index.x][index.y].point.x += (point.x - board[index.x][index.y].point.x) / 2
    board[index.x][index.y].point.y += (point.y - board[index.x][index.y].point.y) / 2
    board[index.x][index.y].point.change = 1

    counter = 0
    queue1 = []
    queue2 = []

    for i in range(len(board[index.x][index.y].adjacent)):
        queue1.append(board[index.x][index.y].adjacent[i])

    for i in range(1, radius + 1):
        counter += 1
        delta = 1 / (2 ** (i + 1))
        if counter % 2 == 1:
            while len(queue1) > 0:
                locate = queue1.pop(0)
                node = board[locate.x][locate.y]
                if node.point.change == 0:
                    board[locate.x][locate.y].point.x += (point.x - node.point.x) * delta
                    board[locate.x][locate.y].point.y += (point.y - node.point.y) * delta
                    board[locate.x][locate.y].point.change = 1
                    for k in range(len(node.adjacent)):
                        queue2.append(node.adjacent[k])

        if counter % 2 == 0:
            while len(queue2) > 0:
                locate = queue2.pop(0)
                node = board[locate.x][locate.y]
                if node.point.change == 0:
                    board[locate.x][locate.y].point.x += (point.x - node.point.x) * delta
                    board[locate.x][locate.y].point.y += (point.y - node.point.y) * delta
                    board[locate.x][locate.y].point.change = 1
                    for k in range(len(node.adjacent)):
                        queue1.append(node.adjacent[k])

    return update_conscience_board(index, board)


def paint_neurons(points, neurons, task, label, border, done=0):
    """
    Function to draw the points and neurons.
    :param points: Array of points
    :param neurons: Array of neurons
    :param task: Task A / B
    :param label: Title of the task.
    :param border: if border = 0, draw circle border, if border = 1, draw ring border (2 circles)
    :param done: If done = 0, draw the neurons and clear, if done = 1, last iteration, show the neurons.
    :return: None
    """
    neurons_x = []
    neurons_y = []
    for i in range(len(points)):
        plt.scatter(points[i].x, points[i].y, color='pink')
    for i in range(len(neurons)):
        neurons_x.append(neurons[i].x)
        neurons_y.append(neurons[i].y)
        plt.scatter(neurons[i].x, neurons[i].y, color='blue')
    if task == "B":
        neurons_x.append(neurons_x[0]), neurons_y.append(neurons_y[0])
    if border == 0:
        circle1 = plt.Circle((0,0), 2, color='r', fill=False)
        ax = plt.gca()
        ax.add_patch(circle1)
    elif border == 1:
        circle1 = plt.Circle((0, 0), 2, color='r', fill=False)
        circle2 = plt.Circle((0, 0), 4, color='r', fill=False)
        ax = plt.gca()
        ax.add_patch(circle1)
        ax.add_patch(circle2)
    plt.suptitle(label)
    plt.plot(neurons_x, neurons_y)
    if done == 1:
        plt.show()
    else:
        plt.draw()
        plt.pause(0.01)
        plt.clf()


def paint_board(points, board, label, done=0):
    """
        Function to draw the points and board.
        :param points: Array of points
        :param board: Matrix of neurons
        :param label: Title of the task
        :param done: If done = 0, draw the board and clear, if done = 1, last iteration, show the board.
        :return: None
        """
    neurons_x = [[] for i in range(2 * len(board[0]))]
    neurons_y = [[] for i in range(2 * len(board[0]))]
    for i in range(len(points)):
        plt.scatter(points[i].x, points[i].y, color='pink')
    index = 0
    for i in range(len(board[0])):
        for j in range(len(board[0])):
            plt.scatter(board[i][j].point.x, board[i][j].point.y, color='blue')
            neurons_x[index].append(board[i][j].point.x)
            neurons_y[index].append(board[i][j].point.y)
        index += 1
    for i in range(len(board[0])):
        for j in range(len(board[0])):
            neurons_x[index].append(board[j][i].point.x)
            neurons_y[index].append(board[j][i].point.y)
        index += 1
    plt.suptitle(label)
    for i in range(len(neurons_x)):
        plt.plot(neurons_x[i], neurons_y[i], 'b')
    circle1 = plt.Circle((0, 0), 2, color='r', fill=False)
    ax = plt.gca()
    ax.add_patch(circle1)
    if done == 1:
        plt.show()
    else:
        plt.draw()
        plt.pause(0.01)
        plt.clf()


def algorithm(points, neurons, task, label="", border=0):
    """
    Function to activate the Kohonen algorithm for tasks A & B
    :param points: Array of points
    :param neurons: Array of neurons
    :param task: Task A / B
    :param label: Title of the task
    :param border: if border = 0, draw circle border, if border = 1, draw ring border (2 circles)
    :return: The updated neurons locations according to the given radius.
    """
    if task == "A":
        paint_neurons(points, neurons, "A", label, border)
    elif task == "B":
        paint_neurons(points, neurons, "B", label, border)
    size = int(len(points)/len(neurons)*2) + 1
    radius = int(len(neurons)/2)
    for i in range(len(points)):
        if i % size == 0 and i != 0:
            radius -= 1
        if task == "A":
            new_neurons = move_algorithm(points[i], min_distance(points[i], neurons), neurons, radius, "A")
            if i % 10 == 0:
                paint_neurons(points, new_neurons, "A", label, border)
        elif task == "B":
            new_neurons = move_algorithm(points[i], min_distance(points[i], neurons), neurons, radius, "B")
            if i % 10 == 0:
                paint_neurons(points, new_neurons, "B", label, border)

    return new_neurons


def algorithm_board(points, board, label=""):
    """
    Function to activate the Kohonen algorithm for task C
    :param points: Array of points
    :param board: Matrix of neurons
    :param label: Title of the task
    :return: None
    """
    paint_board(points, board, label)
    radius = len(board[0]) + 1
    for j in range(len(board[0])):
        radius -= 1
        random.shuffle(points)
        for i in range(len(points)):
            new_board = move_algorithm_board(points[i], min_distance_board(points[i], board), board, radius)
            if i % 10 == 0:
                paint_board(points, new_board, label)

    paint_board(points, new_board, label, 1)


def create_points(x, radius):
    y_ = random.uniform(-radius, radius)
    while y_ ** 2 + x ** 2 > radius ** 2:
        y_ = random.uniform(-radius, radius)
    return y_


def create_points_ring(x, radius1, radius2):
    y_ = random.uniform(-radius2, radius2)
    while (y_ ** 2 + x ** 2 > radius2 ** 2) or (y_ ** 2 + x ** 2 < radius1 ** 2):
        y_ = random.uniform(-radius2, radius2)
    return y_


def main():
    radius = 2
    """ ====================> Tasks: A - C <==================== """
    # Question A - TEST
    neurons = []
    points = []
    for i in range(30):
        neurons.append(Point(random.uniform(-.2, .2), random.uniform(-.2, .2)))

    for i in range(200):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))

    for i in range(10):
        random.shuffle(points)
        neurons = algorithm(points, neurons, "A", "Line Topology - Uniform Data & Neurons Distribution")

    paint_neurons(points, neurons, "A", "Line Topology - Uniform Data & Neurons Distribution", 0, 1)


    #Question B - TEST
    neurons = []
    points = []
    for i in range(30):
        neurons.append(Point(random.uniform(-.2, .2), random.uniform(-.2, .2)))

    for i in range(200):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))

    for i in range(10):
        random.shuffle(points)
        neurons = algorithm(points, neurons, "B", "Circle Topology - Uniform Data & Neurons Distribution")

    paint_neurons(points, neurons, "B", "Circle Topology - Uniform Data & Neurons Distribution", 0, 1)

    #Question C - TEST
    points = []
    for i in range(200):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))
    neurons = [[Point() for i in range(5)] for j in range(5)]
    for i in range(5):
        for j in range(5):
            neurons[i][j] = Point(random.uniform(-.2, .2), random.uniform(-.2, .2))
    board = create_board(neurons)
    algorithm_board(points, board, "5x5 Topology - Uniform Data & Neurons Distribution")

    """ ====================> Task: D <==================== """
    # Question A - TEST
    neurons = []
    points = []
    for i in range(30):
        neurons.append(Point(random.uniform(-.2, .2), random.uniform(-.2, .2)))

    radius = 1
    for i in range(100):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))

    radius = 2
    for i in range(100):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))

    for i in range(10):
        random.shuffle(points)
        neurons = algorithm(points, neurons, "A", "Line Topology - Random Data & Neurons Distribution")

    paint_neurons(points, neurons, "A", "Line Topology - Random Data & Neurons Distribution", 0, 1)

    # Question B - TEST
    neurons = []
    points = []
    for i in range(30):
        neurons.append(Point(random.uniform(-.2, .2), random.uniform(-.2, .2)))

    radius = 1
    for i in range(100):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))

    radius = 2
    for i in range(100):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))

    for i in range(10):
        random.shuffle(points)
        neurons = algorithm(points, neurons, "B", "Circle Topology - Random Data & Neurons Distribution")

    paint_neurons(points, neurons, "B", "Circle Topology - Random Data & Neurons Distribution", 0, 1)

    # Question C - TEST
    points = []
    radius = 1
    for i in range(100):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))

    radius = 2
    for i in range(100):
        x = random.uniform(-radius, radius)
        points.append(Point(x, create_points(x, radius)))
    neurons = [[Point() for i in range(5)] for j in range(5)]
    for i in range(5):
        for j in range(5):
            neurons[i][j] = Point(random.uniform(-.2, .2), random.uniform(-.2, .2))
    board = create_board(neurons)
    algorithm_board(points, board, "5x5 Topology - Random Data & Neurons Distribution")

    """ ====================> Task: E <==================== """
    radius1 = 2
    radius2 = 4
    # Question A - TEST
    neurons = []
    points = []
    for i in range(30):
        neurons.append(Point(random.uniform(-.2, .2), random.uniform(-.2, .2)))

    for i in range(200):
        x = random.uniform(-radius2, radius2)
        points.append(Point(x, create_points_ring(x, radius1, radius2)))

    for i in range(10):
        random.shuffle(points)
        neurons = algorithm(points, neurons, "A", "Line Topology - Uniform Data & Neurons Distribution", 1)

    paint_neurons(points, neurons, "A", "Line Topology - Uniform Data & Neurons Distribution", 1, 1)

    # Question B - TEST
    neurons = []
    points = []
    for i in range(30):
        neurons.append(Point(random.uniform(-.2, .2), random.uniform(-.2, .2)))

    for i in range(200):
        x = random.uniform(-radius2, radius2)
        points.append(Point(x, create_points_ring(x, radius1, radius2)))

    paint_neurons(points, neurons, "B", "Circle Topology - Uniform Data & Neurons Distribution", 1, 1)
    for i in range(10):
        random.shuffle(points)
        neurons = algorithm(points, neurons, "B", "Circle Topology - Uniform Data & Neurons Distribution", 1)

    paint_neurons(points, neurons, "B", "Circle Topology - Uniform Data & Neurons Distribution", 1, 1)


if __name__ == '__main__':
    main()
