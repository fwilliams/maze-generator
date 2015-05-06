import random, sys, os

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

    _UP = 0
    _DOWN = 1
    _LEFT = 2
    _RIGHT = 3
    _NONE = 4
    def _pv_maze_block(self, orientation, x, y,
                       withFloor=True, withCeil=True,
                       floorTex="CheckerFloorTex",
                       wallTexParamName="WallTex",
                       enablePhotonsParamName="EnablePhotons"):
        output = ""
        if orientation is not Maze._NONE:
            output += "object {\n"
            output += "  object { Wall }\n"
            output += "  texture{ WallTex }\n"
            output += "  #if (" + enablePhotonsParamName + ")\n"
            output += "    photons{ target reflection " + \
                      enablePhotonsParamName + " }\n"
            output += "  #end"
            if orientation == Maze._DOWN:
                output += "  scale <1, 1, -1>\n"
            elif orientation == Maze._LEFT:
                output += "  rotate 90*y\n"
            elif orientation == Maze._RIGHT:
                output += "  rotate -90*y\n"
            output += "  translate <" + str(x) + ", 0, " + str(y) + ">\n"
            output += "}\n"
        
        if withFloor:
            output += "object {\n"
            output += "  Floor\n"
            output += "  texture { " + floorTex + " }\n"
            output += "  photons { target reflection on }\n"
            output += "  translate <" + str(x) + ", 0, " + str(y) + ">\n"
            output += "}"
        if withCeil:
            output += "object {\n"
            output += "  Ceiling\n"
            output += "  translate <" + str(x) + ", 0, " + str(y) + ">\n"
            output += "}\n"
            
        return output
                
    def outputPovray(self, floor=True, ceil=True):
        output = '#include "reflection_experiments/objects.inc"'
        output += "#declare MazeWidth = " + str(self.width) + ";\n"
        output += "#declare MazeHeight = " + str(self.height) + ";\n"
        output += "#macro Maze(WallTex, EnablePhotons)\n"
        output += "union {\n"
        for i in range(self.width):
            output += self._pv_maze_block(Maze._UP, i, 0, floor, ceil)

        for j in range(self.height):
            for i in range(self.width):
                if i == 0:
                    output += self._pv_maze_block(Maze._LEFT, i, j, floor, ceil)

                conn = self.conn[j*self.width + i]
                if conn[0] and conn[1]:
                    output += self._pv_maze_block(Maze._NONE, i, j, floor, ceil)
                if conn[0] and not conn[1]:
                    output += self._pv_maze_block(Maze._DOWN, i, j, floor, ceil)
                elif not conn[0] and conn[1]:
                    output += self._pv_maze_block(Maze._RIGHT, i, j, floor, ceil)
                elif not conn[0] and not conn[1]:
                    output += self._pv_maze_block(Maze._RIGHT, i, j, floor, ceil)
                    output += self._pv_maze_block(Maze._DOWN, i, j, floor, ceil)
        output += "}"
        output += "#end\n"
        return output

    
if __name__ == "__main__":
    width = int(sys.argv[1]) \
            if len(sys.argv) >= 2 and sys.argv[1].isnumeric() else 5
    height = int(sys.argv[2]) \
             if len(sys.argv) >= 3 and sys.argv[2].isnumeric() else 5

    try:
        outputFileName = "mirrormaze.inc"
        filenameArgPos = sys.argv.index("-f")
        if filenameArgPos != -1:
            if filenameArgPos != len(sys.argv):
                outputFileName = sys.argv[filenameArgPos+1]
            else:
                print("Error: missing filename argument to -f")
    except ValueError:
        pass

    try:
        includeFloor = True
        includeFloorArgPos = sys.argv.index("-nf")
        if includeFloorArgPos != -1:
            includeFloor = False
    except ValueError:
        pass


    try:
        includeCeil = True
        includeCeilArgPos = sys.argv.index("-nc")
        if includeCeilArgPos != -1:
            includeCeil = False
    except ValueError:
        pass
        
    try:
        os.remove(outputFileName)
    except OSError:
        pass

    try:
        outputFile = open(outputFileName, 'w')
    except OSError:
        print("Error opening file " + outputFileName)
        sys.exit(1)

    maze = Maze(width, height)
    outputFile.write(maze.outputPovray(includeFloor, includeCeil))
                
