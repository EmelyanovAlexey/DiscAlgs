import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

silent = 0
only_result = 1
show_all = 2


def formatFloat(val):
    result = ''
    if val == float("Inf"):
        result += '-'
    else:
        result += str(val)
    return result


def underLineString(string):
    result = ''
    for char in string:
        result += frm.UNDERLINE + char
    return result


class frm:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TABLE = '\033[51m'
    BGB = '\033[40m'
    END = '\033[0m'


class Graph:

    def __init__(self, vertexes, name="Graph"):
        self.V = vertexes
        self.name = name
        self.maxSizeStr = 5
        self.graph = []

    def get_cnt_vertexes(self):
        return self.V

    def get_cnt_edges(self):
        return len(self.graph)

    def get_graph_name(self):
        return self.name

    def set_graph_name(self, newname):
        self.name = newname

    def clear_graph(self):
        if input("Are you sure (Y/N): ") == "Y":
            self.V = 0
            self.graph = []
            print(f"Cleared")
            

    def addEdge(self, u, v, w):
        self.graph.append([u - 1, v - 1, w])
        if len(str(w)) > self.maxSizeStr:
            self.maxSizeStr = len(str(w))

    def alg_BellmanFord(self, source=1, mode=only_result):
        if self.V <= 0:
            return 1
        source -= 1
        dist = [float("Inf")] * self.V
        dist[source] = 0
        if mode > 0:
            self.print_table_title(f"Bellman Ford ({source+1}) ({self.name})")
            self.print_table_header()
        for i in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    if mode > 1:
                        self.print_paths_from_vertex(dist)
                if dist[source] != 0:
                    if mode > 0:
                        self.print_table_title("Graph contain negative cycle\n")
                    return 0
        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                if mode > 0:
                    self.print_table_title("Graph contain negative cycle\n")
                return 0
        if mode > 0:
            self.print_paths_from_vertex(dist)
            print()
        return 1

    def alg_Matrix_multiplication(self, mode=only_result):
        if self.V <= 0:
            return
        matrix = []
        for i in range(self.V):
            matrix.append([float("Inf")] * self.V)
            matrix[i][i] = 0
        for u, v, w in self.graph:
            matrix[u][v] = w

        if mode > 0:
            self.print_table_title(f"Matrix Multi ({self.name})", rightColumn=True)
            if self.check_neg_cycle("", 0):
                allMatrixFlag = 1
                current_degree = 0
                for iterations in range(self.V - 1):
                    current_degree = 2**iterations
                    saveMatrix = [[]] * self.V
                    for i in range(self.V):
                        saveMatrix[i] = matrix[i].copy()
                    for row in range(self.V):
                        for column in range(self.V):
                            cacheArr = []
                            for i in range(self.V):
                                cacheArr.append(saveMatrix[row][i] + saveMatrix[i][column])
                            matrix[row][column] = min(saveMatrix[row][column], min(cacheArr))
                    if saveMatrix == matrix:
                        if mode > 1:
                            allMatrixFlag = 0
                        break
                    if mode > 1:
                        self.print_matrix(matrix, current_degree)
                if allMatrixFlag and mode > 0:
                    self.print_matrix(matrix, current_degree)

    def print_matrix(self, matrix, degree):
        self.print_table_title(f"Degree({degree})", rightColumn=True)
        self.print_table_header(rightColumn=True)
        row_number = 1
        for i in matrix:
            self.print_paths_from_vertex(i, rightColumn=True, row_number=row_number)
            row_number += 1
        print()

    def print_table_title(self, title, rightColumn=False):
        print(end=frm.BOLD + frm.GREEN)
        stringSize = self.maxSizeStr * self.V + self.V - 1
        if rightColumn:
            stringSize += self.V
        print(end=f"{' ' * int(stringSize / 2 - len(title) / 2)}{title}")
        print(frm.END)

    def print_table_header(self, rightColumn=False):
        if rightColumn:
            print(end=frm.BOLD + frm.TABLE)
            print(f"{' ' * self.maxSizeStr}",
                  end=' ')
            print(end=frm.END)
        print(end=frm.BOLD + frm.BGB + frm.TABLE)
        for i in range(1, self.V + 1):
            padding = (self.maxSizeStr - len(str(i)))
            print(f"{' ' * int((padding + 1) / 2)}{i}",
                  end=(' ' * int(padding / 2)))
            if i != self.V:
                print(end='|')
        print(frm.END)

    def print_paths_from_vertex(self, source, rightColumn=False, row_number=0):
        print(end=frm.TABLE)
        if rightColumn:
            print(end=frm.BOLD + frm.BGB)
            padding = (self.maxSizeStr - len(str(row_number)))
            print(f"{' ' * int((padding + 1) / 2)}{row_number}",
                  end=(' ' * int(padding / 2)) + ' ')
            print(end=frm.END)
        print(end=frm.TABLE)
        for i in range(self.V):
            if source[i] == float("Inf"):
                padding = (self.maxSizeStr - len("-"))
            else:
                padding = (self.maxSizeStr - len(str(source[i])))
            print(f"{' ' * int((padding + 1) / 2)}{formatFloat(source[i])}",
                  end=(' ' * int(padding / 2)))
            if i != self.V - 1:
                print(end='|')
        print(frm.END)

    def check_neg_cycle(self, title="Negative cycle check", mode=1):
        if title != "":
            self.print_table_title(f"{title} ({self.name})")
        if not self.alg_BellmanFord(0, silent):
            self.print_table_title("Graph contain negative cycle\n")
            return False
        if mode:
            self.print_table_title("No negative cycle\n")
        return True


if __name__ == '__main__':
    g = Graph(6)

    g.addEdge(1, 2, 1)
    g.addEdge(2, 4, 2)
    g.addEdge(2, 6, 7)
    g.addEdge(2, 3, 5)
    g.addEdge(3, 6, 1)
    g.addEdge(4, 1, 2)
    g.addEdge(4, 3, 1)
    g.addEdge(5, 4, 3)
    g.addEdge(6, 5, 1)

    # g.addEdge(0, 1, 1)
    # g.addEdge(1, 2, 5)
    # g.addEdge(1, 5, 7)
    # g.addEdge(1, 3, 2)
    # g.addEdge(2, 5, 1)
    # g.addEdge(3, 2, 1)
    # g.addEdge(3, 0, 2)
    # g.addEdge(4, 3, 3)
    # g.addEdge(5, 4, 1)

    g.check_neg_cycle()
    g.alg_BellmanFord(source=1, mode=show_all)
    g.alg_Matrix_multiplication(mode=show_all)

    negG = Graph(2, name="Negative graph")
    negG.addEdge(1,2,-1)
    negG.addEdge(2,1,-1)

    negG.check_neg_cycle()
    negG.alg_BellmanFord(1, mode=show_all)
    negG.alg_Matrix_multiplication(mode=only_result)
