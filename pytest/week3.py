import pandas as pd
import numpy as np

class node(self, state, init_state, action, transition, goal, path) :
    state = self.state
    init_state = self.init_state
    action = self.action
    transition = self.transition
    goal = self.goal
    path = self.path

class Problem(self, parent, cost, depth, state, action, x, y) :
    
    def transition_model(self, state, action) :
        new_state = state.cop()
        index = new_state.index(0)



        for i in range(len(init_state)) :
            for j in range(len(init_state)) :
                if(init_state[i][j] == 0) :
                    x, y =(i,j)            

        if(x+1, y) :
            if(x+1 > 2) :
                return failure
            else :
                temp = init_state[x+1][y]
                init_state[X+1][y] = init_state[x][y]
                init_state[x][y] = temp
        
        if(x-1, y) :
            if(x-1 < 0) :
                return failure
            else :
                temp = init_state[x-1][y]
                init_state[X-1][y] = init_state[x][y]
                init_state[x][y] = temp
            
        if(x, y+1) :
            if(y+1 > 2) :
                return failure
            else :
                temp = init_state[x][y+1]
                init_state[X][y+1] = init_state[x][y]
                init_state[x][y] = temp
        if(x, y-1) :
            if(y-1 < 0) :
                return failure
            else :
                temp = init_state[x][y-1]
                init_state[X][y-1] = init_state[x][y]
                init_state[x][y] = temp

if __name__ == "__main__":
    init_state = [[1, 2, 3,],
                [4,0,5],
                [6,7,8]]