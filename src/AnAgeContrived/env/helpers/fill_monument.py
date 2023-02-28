from __future__ import annotations
# these imports will not be imported in the runtime, it is just to help coding to do type_checking
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from env.engine import Engine
    from env.entities.player import Player
    from env.entities.energy import EnergyTile

#real imports start here
from env.entities.monument import Monument
from env.entities.energy import Energy
from env.entities.turn_state import TurnType


class FillMonument():

    # TODO: need to check the player location and get the closest monument to fill ,instead of currently just filling the monuments[0]
    @staticmethod
    def fill_monument_tile(player: Player, engine: Engine, energy: EnergyTile):
        if len(player.energies_released[energy.energy_type]) > 0:
            print(
                '------------- fillMonument.py - fill_monument_tile(): ----------------')
            print('player:', player.get_player_name(),
                  'Trying to fill section with energy:', energy.energy_type)

            monument_wall = engine.monuments[engine.monument_index].get_top_wall(
            )
            print('Monument supports energy types:', monument_wall.sections)
            result = monument_wall.fill_section(energy)
            if result == True:
                print(len(player.energies_released[energy.energy_type]))
                player.energies_released[energy.energy_type].pop()
                print(len(player.energies_released[energy.energy_type]))
                print('Remaining sections:', monument_wall.remaining_sections)
            print('***----------------------------------------***')

    def is_legal_primal(engine: Engine) -> bool:
        if(not engine.turn.get_turn_type() == TurnType.ACTION_TURN):
            return False

        if(engine.monuments[engine.monument_index].is_completed()):
            return False

        current_player = engine.players[engine.current_player]

        if(len(current_player.energies_released[Energy.PRIMAL]) == 0):
            return False

        return True
    
    def is_legal_constructive(engine: Engine) -> bool:
        current_player = engine.players[engine.current_player]
        current_monument = engine.monuments[engine.monument_index]
        if(not engine.turn.get_turn_type() == TurnType.ACTION_TURN):
            return False

        if(current_monument.is_completed()):
            return False

        if(len(current_player.energies_released[Energy.CONSTRUCTIVE]) == 0):
            return False
        
        if Energy.CONSTRUCTIVE in current_monument.get_top_wall().remaining_sections:
            return True

        return False
    
    def is_legal_invertible(engine: Engine) -> bool:
        current_player = engine.players[engine.current_player]
        current_monument = engine.monuments[engine.monument_index]
        if(not engine.turn.get_turn_type() == TurnType.ACTION_TURN):
            return False

        if(current_monument.is_completed()):
            return False

        if(len(current_player.energies_released[Energy.INVERTIBLE]) == 0):
            return False
        
        if Energy.INVERTIBLE in current_monument.get_top_wall().remaining_sections:
            return True

        return False
    
    def is_legal_generative(engine: Engine) -> bool:
        current_player = engine.players[engine.current_player]
        current_monument = engine.monuments[engine.monument_index]
        if(not engine.turn.get_turn_type() == TurnType.ACTION_TURN):
            return False

        if(current_monument.is_completed()):
            return False

        if(len(current_player.energies_released[Energy.GENERATIVE]) == 0):
            return False
        
        if Energy.GENERATIVE in current_monument.get_top_wall().remaining_sections:
            return True

        return False


    def is_legal_to_fill_monument_tile(engine: Engine, energy_type: Energy) -> bool:

        # print('!TURN *** type is:', engine.turn.get_turn_type())
        # Check turn is type action
        if(not engine.turn.get_turn_type() == TurnType.ACTION_TURN):
            #print('not action turn')
            return False

        # Check if current monument is completed, should never occur
        if(engine.monuments[engine.monument_index].is_completed()):
            #print('monument completed')
            return False

        current_player = engine.players[engine.current_player]
        current_monument = engine.monuments[engine.monument_index]

        # check if they even have that energy they want to fill
        if(len(current_player.energies_released[energy_type]) == 0):
            #print("dont have the energy", energy_type)
            return False

        # check if energy they have fits on current monument
        # if(not current_monument.get_top_wall().check_accept(energy_type)):
        #     print("does not accept the energy", energy_type)
        #     print('remaining sections:', current_monument.get_top_wall().remaining_sections, 'filled energies:', current_monument.get_top_wall().filled_sections, 'num of empty spaces:', current_monument.get_top_wall().empty_sections)
        #     print('current monument is:', current_monument.name, 'monument wall starting accepted:', current_monument.get_top_wall().sections)
        #     return False

        if energy_type != Energy.PRIMAL:
            if not (energy_type in current_monument.get_top_wall().remaining_sections):
                print("does not accept the energy", energy_type)
                print('remaining sections:', current_monument.get_top_wall().remaining_sections, 'filled energies:', current_monument.get_top_wall().filled_sections, 'num of empty spaces:', current_monument.get_top_wall().empty_sections)
                print('current monument is:', current_monument.name, 'monument wall starting accepted:', current_monument.get_top_wall().sections)
                return False

        return True
