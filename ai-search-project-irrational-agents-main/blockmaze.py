import sys
import heapq
from collections import deque


class Node: #node class from hw1
    def __init__(self, state, standing, parent, cost):
        self.state = state 
        self.parent = parent
        self.cost = cost
        self.standing = standing
    # Nodes with the same state are viewed as equal
    def __eq__(self, other_node):#checks if a node and other node are in the same position. Second term in the and statement checks that irrespective of which half of the block is in which spot.
        return isinstance(other_node, Node) and (self.state == other_node.state or (self.state[0] == other_node.state[1] and self.state[1] == other_node.state[0])) 
    
    # Nodes with the same state hash to the same value
    # (e.g., when storing them in a set or dictionary)
    def __hash__(self):
        return hash(self.state)

    def __lt__(self, other):#less than comparison for nodes. Used when we add nodes to the frontier heap.
        mazeFile = sys.argv[1]
        heuristic_choice = sys.argv[2]#less than will return different values depending on the heuristic chosen
        _, goal = get_map(mazeFile) #find goal position from map
        if(heuristic_choice == "manhattan"):#manhattan distance modified for a two-long block. We multiply by 2/3 so that the heuristic will always underestimate from the optimal straight line distance.
            return (self.cost + (2/3)*(abs(goal[0] - self.state[0][0]) + abs(goal[1] - self.state[0][1]))) < (other.cost + (2/3)*(abs(goal[0] - other.state[0][0]) + abs(goal[1] - other.state[0][1]))) #compare f(n) for both nodes. h(n) is manhattan distance
        elif(heuristic_choice == "trivial"):#h(n) is just 1-- trivial heuristic to compare to manhattan's performace.
            return self.cost + 1 < other.cost + 1 
        else:#In case a heuristic is not given as a command line argument.
            print("please use either \"trivial\" or \"manhattan\" as the second program argument.")
            quit()


def get_map(filename):
    map_file = open(filename) #open file into map_file
    map = map_file.readlines() #create list where each element is a row on map
    for i in range(0, len(map)):
        map[i] = map[i].strip() #iterate through map and remove \n characters
    for i in range(0,len(map)):
        for j in range(0, len(map[i])): #Find S and G to get start and end positions.
            if (map[i][j] == 'S'):
                start_pos = (i,j)
            if (map[i][j] == 'G'):
                end_pos = (i,j)
    startNode = Node((start_pos, start_pos), True, None, 0)#Initialise first node standing up where the start position is.
    return(startNode, end_pos) #return map


def A_Star(S, goal, map):#Search algorithm that returns the optimal path through a block maze.
    nodes_generated = 1#We count the starting node as a node that is generated.
    nodes_visited = 0
    frontier = []#when taking an action out of possible actions, evaluate heuristic for the action and heappush
    explored = set()
    path_list = deque()
    heapq.heappush(frontier, S)#frontier,possible_actions[i])
    while (frontier):#While there are nodes left to explore, loop.
        x = heapq.heappop(frontier)#remove a node from the frontier and explore the moves that can branch from it.
        nodes_visited+=1
        if (x.state[0] == goal and x.standing == True):#Terminal test
            while x is not None:#This loop returns the path of moves that was taken to reach the goal.
                path_list.appendleft(x.state)
                x = x.parent
            return path_list, nodes_generated, nodes_visited
        explored.add(x)
        for cur_act in Actions(x,map): #Actions returns a list of nodes
            child = cur_act #child is a node, not a state.
            nodes_generated+=1
            if (child not in frontier and child not in explored):#If this is a new node that has never been explored
                heapq.heappush(frontier, child)#Add this node to the frontier
            elif(child in frontier):#If this node is in the frontier, replace it if the newer version has a lower f(n) (path cost + heuristic value)
                for i in range(0,len(frontier)):
                    if frontier[i]==child:
                        replaced_child = frontier[i]
                if(child < replaced_child):
                    replaced_child = child
    return "F", nodes_generated, nodes_visited #If a path is not found


def Actions(Current_Node, map):#Returns a list of all possible actions from a given node. Note that the list is actually a list of Nodes, because we want to pass information about path cost, standing vs laying, etc.
    #For each attempt at an action, check if there are * obstacles in the way or if it would result in going off the board. If the move is possible, add it to a list to be returned.
    possible_actions = []
    cur_pos = Current_Node.state[0]#This is used when the block is standing up, as you only need one set of coordinates
    cur_pos2= Current_Node.state#the set of both coordinates for the block
    valid_tiles = ".GS"#possible tiles to move to. 
    if(Current_Node.standing == True):#block is standing up
        if (cur_pos[1] + 2 < len(map[0])-1):
            if(cur_pos[1] < len(map[0])-2 and map[cur_pos[0]][cur_pos[1]+1] in valid_tiles and map[cur_pos[0]][cur_pos[1]+2] in valid_tiles):#right condition
                right_node = Node(((cur_pos[0], cur_pos[1]+1),(cur_pos[0],cur_pos[1]+2)), False, Current_Node, Current_Node.cost+1)
                possible_actions.append(right_node)
        if(cur_pos[1] > 1 and map[cur_pos[0]][cur_pos[1]-1] in valid_tiles and map[cur_pos[0]][cur_pos[1]-2] in valid_tiles):#left
            left_node = Node(((cur_pos[0], cur_pos[1]-1),(cur_pos[0],cur_pos[1]-2)), False, Current_Node, Current_Node.cost+1)
            possible_actions.append(left_node)
        if(cur_pos[0] < len(map)-2 and map[cur_pos[0]+1][cur_pos[1]] in valid_tiles and map[cur_pos[0]+2][cur_pos[1]] in valid_tiles):#down
            down_node = Node(((cur_pos[0]+1, cur_pos[1]),(cur_pos[0]+2,cur_pos[1])), False, Current_Node, Current_Node.cost+1)
            possible_actions.append(down_node)
        if(cur_pos[0] > 1 and map[cur_pos[0]-1][cur_pos[1]] in valid_tiles and map[cur_pos[0]-2][cur_pos[1]] in valid_tiles):#up
            up_node = Node(((cur_pos[0]-1, cur_pos[1]),(cur_pos[0]-2,cur_pos[1])), False, Current_Node, Current_Node.cost+1)
            possible_actions.append(up_node)
    elif(cur_pos2[0][1]==cur_pos2[1][1]):#if block laying vertically
        if(cur_pos2[0][1] + 1 < len(map[0]) - 1 and cur_pos2[1][1] + 1 < len(map[0]) - 1):
            if(cur_pos[1] < len(map[0])-2 and map[cur_pos2[1][0]][cur_pos2[1][1]+1] in valid_tiles and map[cur_pos2[0][0]][cur_pos2[0][1]+1] in valid_tiles):#roll right condition
                roll_right_node = Node(((cur_pos2[0][0],cur_pos2[0][1]+1),(cur_pos2[1][0],cur_pos2[1][1]+1)), False, Current_Node, Current_Node.cost+1)
                possible_actions.append(roll_right_node)
        if(cur_pos[1] > 0 and map[cur_pos2[0][0]][cur_pos2[0][1]-1] in valid_tiles and map[cur_pos2[1][0]][cur_pos2[1][1]-1] in valid_tiles):#roll left condition
            roll_left_node = Node(((cur_pos2[0][0],cur_pos2[0][1]-1),(cur_pos2[1][0],cur_pos2[1][1]-1)), False, Current_Node, Current_Node.cost+1)
            possible_actions.append(roll_left_node)
        if(cur_pos2[0][0] > 0 and cur_pos2[1][0] > 0 and map[cur_pos2[0][0]-1][cur_pos2[0][1]] in valid_tiles and map[cur_pos2[1][0]-1][cur_pos2[1][1]] in valid_tiles):#construct up
            if(cur_pos2[0][0] < cur_pos2[1][0]):
                top_node = cur_pos2[0]
            else:
                top_node = cur_pos2[1]
            construct_up_node = Node(((top_node[0]-1,top_node[1]),(top_node[0]-1,top_node[1])), True, Current_Node, Current_Node.cost+1)
            possible_actions.append(construct_up_node)
        if(cur_pos2[0][0] < len(map)-1 and cur_pos2[1][0] < len(map)-1 and map[cur_pos2[0][0]+1][cur_pos2[0][1]] in valid_tiles and map[cur_pos2[1][0]+1][cur_pos2[1][1]] in valid_tiles):#construct down
            if(cur_pos2[0][0] > cur_pos2[1][0]):
                bot_node = cur_pos2[0]
            else:
                bot_node = cur_pos2[1]
            construct_down_node = Node(((bot_node[0]+1,bot_node[1]),(bot_node[0]+1,bot_node[1])), True, Current_Node, Current_Node.cost+1)
            possible_actions.append(construct_down_node)
    else:#if block is laying horizontally
        if(cur_pos[0] < len(map)-1 and map[cur_pos2[0][0]+1][cur_pos2[0][1]] in valid_tiles and map[cur_pos2[1][0]+1][cur_pos2[1][1]] in valid_tiles):#roll down
            roll_down_node = Node(((cur_pos2[0][0]+1,cur_pos2[0][1]),(cur_pos2[1][0]+1,cur_pos2[1][1])), False, Current_Node, Current_Node.cost+1)
            possible_actions.append(roll_down_node)
        if(cur_pos[0] > 0 and map[cur_pos2[0][0]-1][cur_pos2[0][1]] in valid_tiles and map[cur_pos2[1][0]-1][cur_pos2[1][1]] in valid_tiles):#roll up
            roll_up_node = Node(((cur_pos2[0][0]-1,cur_pos2[0][1]),(cur_pos2[1][0]-1,cur_pos2[1][1])), False, Current_Node, Current_Node.cost+1)
            possible_actions.append(roll_up_node) 
        if(cur_pos2[0][1] > 0 and cur_pos2[1][1] > 0 and map[cur_pos2[0][0]][cur_pos2[0][1]-1] in valid_tiles and map[cur_pos2[1][0]][cur_pos2[1][1]-1] in valid_tiles):#construct left
            if(cur_pos2[0][1] < cur_pos2[1][1]):
                far_left_node = cur_pos2[0]
            else:
                far_left_node = cur_pos2[1]
            construct_left_node = Node(((far_left_node[0],far_left_node[1]-1),(far_left_node[0],far_left_node[1]-1)), True, Current_Node, Current_Node.cost+1)
            possible_actions.append(construct_left_node)  
        if(cur_pos2[0][1] + 1 < len(map[0])-1 and cur_pos2[1][1] + 1 < len(map[0])-1):
            if(cur_pos2[0][1] < len(map[0])-1 and cur_pos2[1][1] < len(map[0]) and map[cur_pos2[0][0]][cur_pos2[0][1]+1] in valid_tiles and map[cur_pos2[1][0]][cur_pos2[1][1]+1] in valid_tiles):#construct right
                if(cur_pos2[0][1] > cur_pos2[1][1]):
                    far_right_node = cur_pos2[0]
                else:
                    far_right_node = cur_pos2[1]
                construct_right_node = Node(((far_right_node[0],far_right_node[1]+1),(far_right_node[0],far_right_node[1]+1)), True, Current_Node, Current_Node.cost+1)
                possible_actions.append(construct_right_node)
    return(possible_actions)


def main():
    mazeFile = sys.argv[1]#Get file from command line argument
    Starting_Node, Goal_position = get_map(mazeFile)
    map_file = open(mazeFile) #open file into map_file
    map = map_file.readlines()
    returned_list, nodesGenerated, nodesVisited = A_Star(Starting_Node, Goal_position, map)#A* is performed on the map
    no_moves = len(returned_list)#The number of moves.
    if(returned_list[0]=="F"):#Failure condition, print out stats.
        print("Failure: No possible paths were found.")
        print("number of nodes generated using " + sys.argv[2] + " heuristic: " + str(nodesGenerated))
        print("number of nodes visited using " + sys.argv[2] + " heuristic: " + str(nodesVisited))
        quit()
    else:#If a path was found, print out sequence of moves and other relevant stats.
        for i in range(0,len(returned_list)):
            print(returned_list[i])
        print("number of moves using " + sys.argv[2] + " heuristic: " + str(no_moves - 1))
        print("number of nodes generated using " + sys.argv[2] + " heuristic: " + str(nodesGenerated))
        print("number of nodes visited using " + sys.argv[2] + " heuristic: " + str(nodesVisited))

if __name__ == "__main__":#For running in python interpreter.
    main()



#https://stackoverflow.com/questions/49983661/how-to-convert-txt-file-into-2d-array-of-each-char  we used this to understand the the readlines(function)
#https://www.digitalocean.com/community/tutorials/python-remove-character-from-string we used this to learn how to replace the \n in our strings