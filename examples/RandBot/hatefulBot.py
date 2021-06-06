#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface

class HatefulBot(interface.Bot):
    """Bot de los hateful four."""
    NAME = "HatefulBot"

    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una acción (jugada)."""
        cx, cy = state["position"]
        lighthouses = dict((tuple(lh["position"]), lh)
                            for lh in state["lighthouses"])
            allLh = []
        for lh in state["lighthouses"]:
            allLh.append(lh)

        # Si estamos en un faro...
        if (cx, cy) in lighthouses:
            # Si podemos hacer conexion, conectar con faro remoto válido
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
            if lighthouses[(cx, cy)]["owner"] != self.player_num:
                return self.attack(energy)

        target = chooseLighthouse(allLh, cx, cy)
        move = []
        if isAStarPossible(allLh, cx, cy):
            path = aStar([cx, cy], target, state["view"])
            move = path[0]
        else:
            move = getCloserToLighthouse(target, cx, cy)
        # Mover aleatoriamente
        # moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        # Determinar movimientos válidos
        # moves = [(x,y) for x,y in path if self.map[cy+y][cx+x]]
        
        return self.move(*move)

    def chooseLighthouse(lighthouses, cx, cy):
        betterManhattan = 9999
        targetLh = lighthouses[0]
        for lh in lighthouses:
            if lh["owner"] != self.player_num:
                if betterManhattan != 0 and betterManhattan > max(abs(lh["position"][0]-cx), abs(lh["position"][1]-cy)):
                    betterManhattan = max(abs(lh["position"][0]-cx), abs(lh["position"][1]-cy))
                    targetLh = lh
        return targetLh

    def aStar(start, goal, grid):
        return [[1,0]]

    def isAStarpossible(lighthouses, cx, cy):
        for lh in lighthouses:
            if(max(abs(lh["position"][0]-cx), abs(lh["position"][1]-cy)<=3)):
                return true
        return false

    def getCloserToLighthouse(target, cx, cy):
        if cx < target[0]:
            if cy < target[1]:
                #return upright
                return [1,1]
            if cy > target[1]:
                #return downright
                return [1,-1]
            if cy == target[1]:
                #return right
                return [1,0]
        if cx > target[0]:
            if cy < target[1]:
                #return upleft
                return [-1,1]
            if cy > target[1]:
                #return downleft
                return [-1,-1]
            if cy == target[1]:
                #return left
                return [-1,0]
        if cx == target[0]:
            if cy < target[1]:
                #return up
                return [0,1]
            if cy > target[1]:
                #return down
                return [0,-1]

if __name__ == "__main__":
    iface = interface.Interface(HatefulBot)
    iface.run()