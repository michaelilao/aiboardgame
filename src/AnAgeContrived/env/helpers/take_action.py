# Author: Jonah Ada
# Date: February 5th, 2023
# Description: 
# Helper module to define action token actions in transmuter device

from __future__ import annotations
# these imports will not be imported in the runtime, it is just to help coding to do type_checking
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from env.entities.player import Player
    from env.engine import Engine
    # from env.entities.energy import EnergyTile
    pass

from env.entities.action_tokens import ActionType
from env.entities.turn_state import TurnType
from random import randint
from env.helpers.logger import Logger


# index is the index of the transmuter tile that you want to take action on
# main game rules that defines how to get an action token given resources
def take_action(player: Player, engine: Engine, index: int):
    if index < 0 or index > 4:
        Logger.log('index is suppose to be between [0, 4]. Current index is not valid: ' + str(index), 'ACTION_LOGS')
        return False
    transmuter_tile = player.transmuter.active_tiles[index]  # this is TransmuterTile object
    bottom_energies = transmuter_tile.bottom  # this is a list
    num_energies = len(bottom_energies) - bottom_energies.count(0)
    if num_energies > 0:
        energy = transmuter_tile.release_bottom_energy()
        player.exhausted_energies[energy.energy_type].append(energy)
        
        action_token = player.transmuter.get_action_token(index)
        if action_token == 'ANY':
            new_index = _get_random_token()
            action_token = player.transmuter.get_action_token(new_index)
        if action_token.type == ActionType.MOVE:
            if _take_move_action(engine, action_token):
                Logger.log('Move action completed successfuly', 'ACTION_LOGS')
                return True
            else:
                Logger.log('Move action could NOT be completed', 'ACTION_LOGS')
                return False
        elif action_token.type == ActionType.FILL_TRANSFORMATIVE:
            if _take_transformative_action(player):
                Logger.log('Transformative action completed successfuly', 'ACTION_LOGS')
                return True
            else:
                Logger.log('Transformative action could NOT be completed', 'ACTION_LOGS')
                return False
        elif action_token.type == ActionType.FILL_SENTINENT:
            if _take_sentient_action(player):
                Logger.log('Sentient action completed successfuly', 'ACTION_LOGS')
                return True
            else:
                Logger.log('Sentient action could NOT be completed', 'ACTION_LOGS')
                return False
        elif action_token.type == ActionType.RELEASE_ENERGY:
            if _take_release_energy_action(player, action_token):
                Logger.log('Release energy action completed successfuly', 'ACTION_LOGS')
                return True
            else:
                Logger.log('Release energy action could NOT be completed', 'ACTION_LOGS')
                return False
        elif action_token.type == ActionType.RECHARGE:
            _take_recharge_action(player)
        else:
            Logger.log('Not a valid action', 'ACTION_LOGS')
            return False
    else:
        Logger.log('No energy in the bottom tiles', 'ACTION_LOGS')
        return False

# defines game rules to implement the action mask
def is_take_action_legal(player: Player, engine: Engine, index: int):
    is_legal = False
    if(not engine.turn.get_turn_type() == TurnType.ACTION_TURN):
        return False
    if index < 0 or index > 4:
        Logger.log('index is suppose to be between [0, 4]. Current index is not valid: ' + str(index), 'ACTION_LOGS')
        return False
    action_token = player.transmuter.get_action_token(index)
    if action_token == 'ANY':
        new_index = _get_random_token()
        action_token = player.transmuter.get_action_token(new_index)
    transmuter_tile = player.transmuter.active_tiles[index]  # this is TransmuterTile object
    bottom_energies = transmuter_tile.bottom  # this is a list
    num_energies = len(bottom_energies) - bottom_energies.count(0)
    if action_token.type == ActionType.MOVE or action_token.type == ActionType.RECHARGE:
        if num_energies > 0:
            is_legal = True
    elif action_token.type == ActionType.RELEASE_ENERGY:
        if num_energies > 0:
            available_tiles = []
            for i in range(0, len(action_token.transmuter_tiles)):
                if action_token.transmuter_tiles[i] == 1 and ((len(player.transmuter.active_tiles[i].top) - player.transmuter.active_tiles[i].top.count(0)) > 0):
                    available_tiles.append(i)
            if len(available_tiles) > 0:
                is_legal = True
    return is_legal

# helper function for movement action tokens
def _take_move_action(engine: Engine, action_token):
    # TODO: discuss how to implement this
    # move_times = action_token.move_times
    engine.turn.turn_type = TurnType.MOVE_TURN
    return True

# helper function to take transformative track action token
def _take_transformative_action(player: Player):
    player.transformative_track.is_token_enable = True

# helper function to take sentient track action token
def _take_sentient_action(player: Player):
    player.sentient_track.is_token_enable = True

# helper function to take release energy action token
def _take_release_energy_action(player: Player, action_token):
    available_tiles = []
    for i in range(0, len(action_token.transmuter_tiles)):
        # print('top tiles is:', player.transmuter.active_tiles[i].top, 'and condition is:', action_token.transmuter_tiles[i] == 1 and ((len(player.transmuter.active_tiles[i].top) - player.transmuter.active_tiles[i].top.count(0)) > 0))
        # print('action_token.transmuter_tiles[i] is:', action_token.transmuter_tiles[i])
        # print('cond 1 is:', action_token.transmuter_tiles[i] == 1, 'and cond2 is:', ((len(player.transmuter.active_tiles[i].top) - player.transmuter.active_tiles[i].top.count(0)) > 0))
        if action_token.transmuter_tiles[i] == 1 and ((len(player.transmuter.active_tiles[i].top) - player.transmuter.active_tiles[i].top.count(0)) > 0):
            available_tiles.append(i)
    # print('AVAILABLE TILES:', available_tiles)
    if len(available_tiles) <= 0:
        Logger.log('not enough energies', 'ACTION_LOGS')
        return False
    rand_num = randint(0, len(available_tiles) - 1)
    # print('rand_num is:', rand_num)
    index = available_tiles[rand_num]
    transmuter_tile = player.transmuter.active_tiles[index]
    if (len(transmuter_tile.top) - transmuter_tile.top.count(0)) > 0:
        Logger.log('energies BEFORE: ' + str(player.energies_released), 'ACTION_LOGS')
        energy = transmuter_tile.release_top_energy()
        player.energies_released[energy.energy_type].append(energy)
        Logger.log('energies AFTER: ' + str(player.energies_released), 'ACTION_LOGS')
        return True

# helper function to recharge player's channel marker action token
def _take_recharge_action(player: Player):
    player.channel_marker = True

# helper function to generate random integer within token indexes
def _get_random_token() -> int:
    return randint(0, 3)
