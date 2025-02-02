# Author: Jeffrey Dang
# Date: November 13th, 2022
# Description: 
# Module defining the victory points of An Age Contrived game

from __future__ import annotations

# these imports will not be imported in the runtime, it is just to help coding to do type_checking
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from env.engine import Engine
    from env.entities.player import Player
    # from env.entities.energy import EnergyTile
    pass

from env.entities.energy import Energy


class VictoryPoints:
    # calculates the victory points that the player earned by gaining energy types
    def calcFullyGainedEnergy(engine, player: Player):
        gainableEnergyList = player.remaining_energies[Energy.SINGLE]
        fullyGainedEnergy = 0
        vp_allocation = {0: 0, 1: 3, 2: 6, 3: 10, 4: 15}
        #single energy type checks
        if len(gainableEnergyList) > 5 and len(gainableEnergyList) < 8:
            fullyGainedEnergy += 1
        elif len(gainableEnergyList) > 3 and len(gainableEnergyList) < 6:
            fullyGainedEnergy += 1
        elif len(gainableEnergyList) > 1 and len(gainableEnergyList) < 4:
            fullyGainedEnergy += 1
        elif len(gainableEnergyList) >= 0 and len(gainableEnergyList) < 2:
            fullyGainedEnergy += 1

        vp_points = vp_allocation.get(fullyGainedEnergy)
        return vp_points

    # calculates the victory points the player earned by building bridges
    def calcBridgesBuilt(engine: Engine, player: Player):
        if player.num_bridges_left == 0:
            return 30
        if player.num_bridges_left == 1:
            return 15
        if player.num_bridges_left == 2:
            return 10
        return 0

    # calculates the victory points the player earned by building monuments with energies
    def calcMonumentEnergy(engine: Engine, player: Player):
        monumentList = engine.monuments
        vp_allocation = {
            0: 0,
            1: 3,
            2: 7,
            3: 12
        }
        total_energies_binded = 0
        for monument in monumentList:
            for energy in monument.binded_energies:
                if (energy.owner == player):
                    total_energies_binded += 1
        if total_energies_binded > 3:
            total_energies_binded = 3
        return vp_allocation.get(total_energies_binded)

    # calculates the victory points the player earned by building pillars of civilization
    def calcPillarsOfCivilization(engine: Engine, player: Player):
        filled_pillars = 0
        vp_allocation = {0: 0, 1: 3, 2: 8, 3: 14, 4: 21, 5: 29, 6: 38}
        for pillar in engine.pillars_of_civilization:
            if pillar.is_player_present(player):
                filled_pillars += 1
        return vp_allocation.get(filled_pillars)