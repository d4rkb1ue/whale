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
        self.stack = []

    def goTo(self, des):
        '''base on where I am to find the correct way to dest,
        push the steps in the stack'''
        
        # print("goTo: ", self.x, self.y, "=>", des)
        if (self.x, self.y) == des:
            return

        # bfs
        que = deque()
        vis = set()
        par = dict()
        found = False

        que.append((self.x, self.y))

        while len(que) > 0:
            cur = que.popleft()
            if cur == des:
                found = True
                break

            vis.add(cur)
            x = cur[0]
            y = cur[1]
            
            ar = []
            if x > 0:
                ar.append((x - 1, y))
            if y > 0:
                ar.append((x, y - 1))
            ar.append((x + 1, y))
            ar.append((x, y + 1))

            for i in ar:
                if (i in self.visited or i in self.safe) and i not in vis and i not in que:
                    que.append(i)
                    par[i] = cur
            
        if not found:
            # print("[error] no path from", self.x, self.y, "to", des[0], des[1])
            exit()
        
        # construct path
        path = [des]
        cur = des
        while cur in par:
            path.append(par[cur])
            cur = par[cur]
        
        # remove last, aka, self
        path.pop()
        path.reverse()

        # construct actions
        x = self.x
        y = self.y
        twd = self.toward
        for (nx, ny) in path:
            if nx > x:
                while twd != 3:
                    self.todo.append(Agent.Action.TURN_LEFT)
                    twd -= 3
            elif nx < x:
                while twd != 9:
                    self.todo.append(Agent.Action.TURN_RIGHT)
                    twd += 3
                    if twd > 12:
                        twd = 3
            elif ny > y:
                while twd != 12:
                    self.todo.append(Agent.Action.TURN_RIGHT)
                    twd += 3
            else:
                while twd != 6:
                    self.todo.append(Agent.Action.TURN_RIGHT)
                    twd += 3
                    if twd > 12:
                        twd = 3
            self.todo.append(Agent.Action.FORWARD)
            (x, y) = (nx, ny)

        # print("path = ", path, "action = ", self.todo)
        (self.x, self.y) = des
        self.toward = twd

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


    def getAction(self, stench, breeze, glitter, bump, scream):
        # self.pstate()
        self.visited.add((self.x, self.y))

        if len(self.todo) > 0:
            # self.pstate()
            return self.todo.popleft()

        if glitter:
            self.goTo((0, 0))
            self.todo.append(Agent.Action.CLIMB)
            # self.pstate()
            return Agent.Action.GRAB

        if bump:
            self.danger.add((self.x, self.y))
            if self.toward == 3:
                for i in range(10):
                    self.danger.add((self.x, i))
                self.x -= 1
            elif self.toward == 6:
                for i in range(10):
                    self.danger.add((i, self.y))
                self.y += 1
            elif self.toward == 9:
                for i in range(10):
                    self.danger.add((self.x, i))
                self.x += 1
            else:
                for i in range(10):
                    self.danger.add((i, self.y))
                self.y -= 1
        
        ar = []
        x = self.x
        y = self.y
        if x > 0:
            ar.append((x - 1, y))
        if y > 0:
            ar.append((x, y - 1))
        ar.append((x + 1, y))
        ar.append((x, y + 1))

        for i in ar:
            if i not in self.visited:
                if breeze or stench:
                    if i not in self.safe:
                        self.danger.add(i)
                else:
                    self.safe.add(i)
                    if i not in self.stack and i not in self.visited:
                        self.stack.append(i)

        

        while len(self.stack) > 0:
            n = self.stack.pop()
            if n not in self.visited and (n not in self.danger or n in self.safe):
                self.goTo(n)
                # self.pstate()
                return self.todo.popleft()

        if len(self.stack) == 0:
            self.goTo((0, 0))
            self.todo.append(Agent.Action.CLIMB)
            # self.pstate()
            return self.todo.popleft()