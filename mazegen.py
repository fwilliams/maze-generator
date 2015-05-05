import random, sys

class UnionFind:
    elements = []
    rank = []

    def __init__(self, numElements):
        self.elements = list(range(numElements))
        self.rank = [1] * numElements
        
    def union(self, e1, e2):
        xx = self.find(e1)
        yy = self.find(e2)
        
        if xx == yy:
            return False

        if self.rank[xx] > self.rank[yy]:
            temp = xx
            xx = yy
            yy = temp
            
        if self.rank[xx] == self.rank[yy]:
            self.rank[yy] += 1

        self.elements[xx] = yy
        return True

    def find(self, elem):
        if self.elements[elem] != self.elements[self.elements[elem]]:
            # Path compression
            self.elements[elem] = self.find(self.elements[elem]) 
        return self.elements[elem]

    def insert(self, elem):
        self.elements.append(elem)
        self.rank.append(1)
        return elem


class Maze:
    conn = []

    def __init__(self, w, h):
        self.width = w
        self.height = h
        random.seed(None)
        self.regenerate()
        
    def __str__(self):
        output = ""
        for i in range(self.width):
            output += (" _")

        output += ("\n")

        for j in range(self.height):
            for i in range(self.width):
                if i == 0:
                    output += ("|")

                conn = self.conn[j*self.width + i]
                if conn[0] and conn[1]:
                    output += ("  ")
                elif conn[0] and not conn[1]:
                    output += ("_ ")
                elif not conn[0] and conn[1]:
                    output += (" |")
                elif not conn[0] and not conn[1]:
                    output += ("_|")
            output += ("\n")
        return output


    def _generate_edges(self):
        edges = []

        numVerts = self.width * self.height
        for i in range(self.height-1):
            for j in range(self.width-1):
                baseVert = i * width + j
                edges.append((baseVert, baseVert+1))
                edges.append((baseVert, baseVert+width))
            baseVert = (i+1) * width - 1 
            edges.append((baseVert, baseVert + width))

        offset = self.width * (self.height - 1)
        for i in range(self.width-1):
            baseVert = offset + i
            edges.append((baseVert, baseVert+1))
            
        random.shuffle(edges)
        return edges

    def regenerate(self):
        edges = self._generate_edges()
        numComponents = self.width * self.height
        uf = UnionFind(numComponents)
        self.conn = [[False, False] for i in range(numComponents)]
        
        for e in edges:
            if uf.union(e[0], e[1]):
                numComponents -= 1
                if (e[1] - e[0]) == 1:
                    self.conn[e[0]][0] = True
                else:
                    self.conn[e[0]][1] = True
                if numComponents == 0:
                    print("cool")
                    return

if __name__ == "__main__":
    width = int(sys.argv[1]) if len(sys.argv) >= 2 else 5
    height = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
    maze = Maze(width, height)
    print(maze)
                
        

