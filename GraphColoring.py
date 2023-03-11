import sys
import copy
import time

colors = 0

def valueOrder(v,domain,graph):
    ## Least constraining value (LCV)
    ## The one that rules out the fewest values in the remaining variables

    lcv = {} ## {color:lcv}
    for color in domain[v]:
        count = 0
        for x in graph[v]:
            if color in domain[x]:
                count += 1
        lcv[color] = count
    domain[v].sort(key=lambda c:lcv[c])
    
    return domain[v]

def nextVariableVertex(solution,domain,graph):
    ## Minimum Remaining Values (MRV)
    ## MRV:find the variable that has the smallest domain

    l = colors + 1
    mrv = None
    for v in graph:
        if v not in solution:
            if len(domain[v]) < l:
                mrv = v
                l = len(domain[v])
            elif len(domain[v]) == l:
                if len(graph[mrv]) < len(graph[v]):
                    mrv = v

    return mrv

def RemoveInconsistentValues(domain,constraint):
    #for every item in x there should be a satisfied one in y
    #specified for this, there should be at least 2 items in y or delete all x that is the same from y[0]

    dx = domain[constraint[0]]
    dy = domain[constraint[1]]
    
    if len(dy) == 1 and dy[0] in dx:
        dx.remove(dy[0])
        return True
    else:
        return False

def AC3(domain,graph):
    #revise for 2-consistent
    #input: graph-the graph matrix domain-the current domain list
    #output:the revised domain list or failure if there is no solution

    queue=[(x,y) for x in graph for y in graph[x]]
    while(len(queue)!=0):
        constraint = queue.pop()
        if RemoveInconsistentValues(domain,constraint):
            x = constraint[0]
            if len(domain[x]) == 0:
                return False
            for y in graph[x]:
                queue.append((y,x))

    return True
                            
def backTrackSearch(solution,domain,graph):

    if len(solution) == len(graph):
        return solution
    v = nextVariableVertex(solution,domain,graph)
    for color in valueOrder(v,domain,graph):
        newdomain = copy.deepcopy(domain)
        solution[v] = color
        newdomain[v]=[color]
        if AC3(newdomain,graph):
            result = backTrackSearch(solution,newdomain,graph)
            if result is not None:
                return result
        solution.pop(v)

    return None
    	              
def loadFile(filename):

    colors = 0
    edges = 0
    graph = {} # vertexs with set of neighbors
    with open(filename, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line != "" and line[0] != '#': # not a comment and empty line
                if "colors" in line or "Colors" in line:
                    colors = int(line.split('=')[1])
                elif ',' in line:
                    x = int(line.split(',')[0])
                    y = int(line.split(',')[1])
                    if x not in graph:
                        graph[x] = set()
                    graph[x].add(y)
                    if y not in graph:
                        graph[y] = set()
                    graph[y].add(x)
                    edges += 1

    print("Filename: ",filename)
    print("Colors: ",colors)
    print("Vertices: ",len(graph))
    print("Edges: ",edges)
    print("")

    return colors, graph
    
def printSolution(solution):

##    print(solution)
    if solution is None:
        print("There is no result!")
    else:
        print("Here is the coloring result for all nodes:")
        for v in sorted(solution):
            print("{} and this node color is: {}".format(v,solution[v]))

class Coloring:

    def testFile(self,filename):

        global colors
        
        colors, graph = loadFile(filename)
        solution = {}
        domain = {}
        for v in graph:
            domain[v] = [c for c in range(colors)]
        print("Searching...")
        start_time = time.time()
        solution = backTrackSearch(solution,domain,graph)
        end_time = time.time()
        printSolution(solution)
        print(f"Time cost: {format(end_time - start_time, '.4f')}s\n\n")

# main function
if __name__ == '__main__':

    coloring = Coloring()
    if len(sys.argv) > 1:
        coloring.testFile(sys.argv[1])
    else:
        test_files = ['gc_78317094521100.txt', 'gc_78317097930400.txt',
                      'gc_78317097930401.txt', 'gc_78317100510400.txt',
                      'gc_78317103208800.txt', 'gc_1378296846561000.txt']
        for filename in test_files:
            coloring.testFile(filename)
