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

class MyAI (Agent):

    def __init__(self):
        self.finishX = False
        self.todo = []
        self.x = 1
        

    __actions = [
        Agent.Action.TURN_LEFT,
        Agent.Action.TURN_RIGHT,
        Agent.Action.FORWARD,
        Agent.Action.CLIMB,
        Agent.Action.SHOOT,
        Agent.Action.GRAB
    ]

    def finish(self):
        self.finished = True
        if self.finishX:
            self.todo.append(Agent.Action.CLIMB)
        else:
            self.finishX = True
            self.todo.append(Agent.Action.TURN_RIGHT)
        while self.x > 1:
            self.x -= 1
            self.todo.append(Agent.Action.FORWARD)
        self.todo.append(Agent.Action.TURN_LEFT)
        self.todo.append(Agent.Action.TURN_LEFT)


    def getAction(self, stench, breeze, glitter, bump, scream):
        if len(self.todo) > 0:
            return self.todo.pop()

        if self.x == 1 and (stench or breeze):
            return Agent.Action.CLIMB
        
        if bump:
            self.x -= 1
            self.finish()
            return self.todo.pop()

        if glitter:
            self.finish()
            return Agent.Action.GRAB
        
        if stench or breeze:
            self.finish()
            return self.todo.pop()
        else:
            self.x += 1
            return Agent.Action.FORWARD