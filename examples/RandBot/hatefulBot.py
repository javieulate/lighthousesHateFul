#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys, math
import interface

def aStar(start, goal, grid):
    return [[1,0]]

def isAStarpossible(lighthouses, cx, cy):
    for lh in lighthouses:
        if(max(abs(lh["position"][0]-cx), abs(lh["position"][1]-cy)<=3)):
            return true
    return false

def getCloserToLighthouse(self, state, xLh, yLh, cx, cy):
    moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
    moves = [(x,y) for x,y in moves if self.map[cy+y][cx+x]]
    if cx < xLh:
        if cy < yLh:
            #return upright
            if (1,1) in moves:
                return [1,1]
            else 
                return random.choice(moves)
        if cy > yLh:
            #return downright
            if (1,-1) in moves:
                return [1,-1]
            else 
                return random.choice(moves)
        if cy == yLh:
            #return right
            if (1,0) in moves:
                return [1,0]
            else 
                return random.choice(moves)
    if cx > xLh:
        if cy < yLh:
            #return upleft
            if (-1,1) in moves:
                return [-1,1]
            else 
                return random.choice(moves)
        if cy > yLh:
            #return downleft
            if (-1,-1) in moves:
                return [-1,-1]
            else 
                return random.choice(moves)
        if cy == yLh:
            #return left
            if (-1,0) in moves:
                return [-1,0]
            else 
                return random.choice(moves)
    if cx == xLh:
        if cy < yLh:
            #return up
            if (0,1) in moves:
                return [0,1]
            else 
                return random.choice(moves)
        if cy > yLh:
            #return down
            return [0,-1]
            if (0,-1) in moves:
                return [0,-1]
            else 
                return random.choice(moves)

def chooseLighthouse(self, lighthouses, cx, cy):
    betterManhattan = 9999
    targetLh = lighthouses[0]
    for lh in lighthouses:
        xLh, yLh = lh["position"]
        if lh["owner"] != self.player_num:
            if max(abs(xLh-cx), abs(yLh-cy)) != 0 and betterManhattan > max(abs(xLh-cx), abs(yLh-cy)):
                betterManhattan = max(abs(xLh-cx), abs(yLh-cy))
                targetLh = lh
    return targetLh["position"]

class RandBot(interface.Bot):
    """Bot que juega aleatoriamente."""
    NAME = "RandBot"

    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una acción (jugada)."""
        cx, cy = state["position"]
        lighthouses = dict((tuple(lh["position"]), lh)
                            for lh in state["lighthouses"])

        # Si estamos en un faro...
        if (cx, cy) in lighthouses:
            # Probabilidad 60%: conectar con faro remoto válido
            if lighthouses[(cx, cy)]["owner"] == self.player_num:
                possible_connections = []
                for dest in lighthouses:
                    # No conectar con sigo mismo
                    # No conectar si no tenemos la clave
                    # No conectar si ya existe la conexión
                    # No conectar si no controlamos el destino
                    # Nota: no comprobamos si la conexión se cruza.
                    if (dest != (cx, cy) and
                        lighthouses[dest]["have_key"] and
                        [cx, cy] not in lighthouses[dest]["connections"] and
                        lighthouses[dest]["owner"] == self.player_num):
                        possible_connections.append(dest)

                if possible_connections:
                    return self.connect(random.choice(possible_connections))

            #Si no somos duenyos, conquistar
            energy = state["energy"]
            if lighthouses[(cx, cy)]["owner"] != self.player_num and energy != 0:
                return self.attack(energy)

        allLh = []
        move = [0,0]
        for lh in state["lighthouses"]:
            allLh.append(lh)
        
        xLh, yLh = chooseLighthouse(self, allLh, cx, cy)
        move = getCloserToLighthouse(self, state, xLh, yLh, cx, cy)
        return self.move(*move)

if __name__ == "__main__":
    iface = interface.Interface(RandBot)
    iface.run()
