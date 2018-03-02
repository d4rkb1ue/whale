# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from collections import deque

class MyAI (Agent):

    def __init__(self):
        self.todo = deque()
        self.x = 0
        self.y = 0
        # like the clock, 3 is right, 6 is down, 9 is left, 12 is up
        self.toward = 3
        self.visited = set()
        self.danger = set()
        self.safe = set()
        self.bound = set()
        self.stack = []

    def pathOf(self, des):
        '''calculate the path of arriving des, not actually go'''

        # bfs
        que = deque()
        par = dict()
        vis = set()
        found = False

        if (self.x, self.y) == des:
            return []
    
        que.append((self.x, self.y, self.toward))

        while len(que) > 0:
            cur = que.popleft()
            loc = (cur[0], cur[1])
            if loc == des:
                found = cur
                break

            vis.add(cur)
            x = cur[0]
            y = cur[1]
            t = cur[2]
            
            ar = []
            if x > 0 and t == 9:
                ar.append((x - 1, y, t))
            if y > 0 and t == 6:
                ar.append((x, y - 1, t))
            if y < 6 and t == 12:
                ar.append((x, y + 1, t))
            if x < 6 and t == 3:
                ar.append((x + 1, y, t))
            if t == 3:
                ar.append((x, y, 12))
            else:
                ar.append((x, y, t - 3))
            if t == 12:
                ar.append((x, y, 3))
            else:
                ar.append((x, y, t + 3))

            for i in ar:
                loc = (i[0], i[1])
                if (loc in self.visited or loc in self.safe) \
                    and loc not in self.bound \
                    and i not in vis \
                    and i not in que:

                    que.append(i)
                    par[i] = cur
            
        if not found:
            print("[error] no path from", self.x, self.y, "to", des[0], des[1])
            exit()
        
        # construct path
        path = [found]
        cur = found
        while cur in par:
            path.append(par[cur])
            cur = par[cur]
        
        # remove last, aka, self
        path.pop()
        path.reverse()

        return path


    def goTo(self, des, path):
        '''base on the path, push the steps(actions) in the stack'''
        
        # construct actions
        x = self.x
        y = self.y
        t = self.toward
        for (nx, ny, nt) in path:
            if nx != x or ny != y:
                self.todo.append(Agent.Action.FORWARD)

            else:
                if (t == 3 and nt == 6) \
                    or (t == 6 and nt == 9) \
                    or (t == 9 and nt == 12) \
                    or (t == 12 and nt == 3):
                    self.todo.append(Agent.Action.TURN_RIGHT)
                elif abs(t - nt) == 6:
                    self.todo.append(Agent.Action.TURN_RIGHT)
                    self.todo.append(Agent.Action.TURN_RIGHT)
                elif (t == 6 and nt == 3) \
                    or (t == 9 and nt == 6) \
                    or (t == 12 and nt == 9) \
                    or (t == 3 and nt == 12):
                    self.todo.append(Agent.Action.TURN_LEFT)
                else:
                    print("[err] turn wrong!")
                    exit()

            (x, y, t) = (nx, ny, nt)

        # print("path = ", path, "action = ", self.todo)
        (self.x, self.y) = des
        self.toward = t

    def pstate(self):
        print("state:", self.x, ",", self.y, self.toward)
        print("stack:", self.stack)
        print("visit:")
        for s in self.visited:
            print(s, end=" ")
        print("")
        print("dange:")
        for s in self.danger:
            print(s, end=" ")
        print("")
        print("safe :")
        for s in self.safe:
            print(s, end=" ")
        print("")

    def goHome(self):
        self.goTo((0, 0), self.pathOf((0, 0)))
        self.todo.append(Agent.Action.CLIMB)

    def getAction(self, stench, breeze, glitter, bump, scream):
        # self.pstate()
        self.visited.add((self.x, self.y))

        if len(self.todo) > 0:
            # self.pstate()
            return self.todo.popleft()

        if glitter:
            self.goHome()
            # self.pstate()
            return Agent.Action.GRAB

        if bump:
            self.bound.add((self.x, self.y))
            if self.toward == 3:
                for i in range(10):
                    self.bound.add((self.x, i))
                self.x -= 1
            elif self.toward == 6:
                for i in range(10):
                    self.bound.add((i, self.y))
                self.y += 1
            elif self.toward == 9:
                for i in range(10):
                    self.bound.add((self.x, i))
                self.x += 1
            else:
                for i in range(10):
                    self.bound.add((i, self.y))
                self.y -= 1
        
        # go around
        ar = []
        x = self.x
        y = self.y
        if x > 0:
            ar.append((x - 1, y))
        if y > 0:
            ar.append((x, y - 1))
        if y < 6:
            ar.append((x, y + 1))
        if x < 6:
            ar.append((x + 1, y))

        for i in ar:
            if i not in self.visited:
                if breeze or stench:
                    if i not in self.safe:
                        self.danger.add(i)
                else:
                    self.safe.add(i)
                    if i not in self.visited and i not in self.bound:
                        self.stack.append(i)

        # filter
        fstack = []
        for s in self.stack:
            if s not in self.visited and (s not in self.danger or s in self.safe) and s not in self.bound:
                fstack.append(s)

        self.stack = fstack

        # found the nearest
        if len(self.stack) > 0:
            path = self.pathOf(self.stack[0])
            dest = self.stack[0]
            for nx in self.stack:
                dpath = self.pathOf(nx)
                if len(dpath) < len(path):
                    path = dpath
                    dest = nx
            self.goTo(dest, path)
            return self.todo.popleft()
            
        else:
            self.goHome()
            # self.pstate()
            return self.todo.popleft()