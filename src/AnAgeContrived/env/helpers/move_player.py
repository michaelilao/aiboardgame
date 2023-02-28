import copy
from env.entities.turn_state import TurnType


class MovePlayer():

    @staticmethod
    def move_player(engine, player, location):

        # Check if bridge is crossed, get path from player location to where they want to move
        path = engine.map.get_path(player.location, location)
        bridge = engine.map.check_crossed_bridge(path)

        if(len(engine.map.map[location]) == 1):  # Check if moving into deadend, if so let them move in any direction after moving into dead end
            player.previous_location = 0
        else:
            player.previous_location = player.location
        player.location = location
        engine.turn.can_move = False

        if(bridge):
            reward_bridge = engine.map.get_player_bridge(bridge)
            if(reward_bridge.action_required):
                engine.turn.turn_type = TurnType.BRIDGE_REWARD_TURN
            else:
                print("assigning rewards")
                engine.turn.turn_type = TurnType.ACTION_TURN

        else:
            engine.turn.turn_type = TurnType.ACTION_TURN

    @staticmethod
    def is_legal_move(player, engine, next_location):

        # TODO Check if a bridge connecting areas hasnt been built if not built cannot move
        current_location = player.location
        map = engine.map

        if(not engine.turn.get_turn_type() == TurnType.MOVE_TURN):
            return False
        if(not engine.turn.can_move):
            return False
        if(current_location == next_location):
            return False
        if(next_location == player.previous_location):
            return False

        path = (engine.map.get_path(player.location, next_location))
        bridge = (engine.map.check_crossed_bridge(path))
        if(bridge and not engine.map.check_bridge_exists(bridge)):  # if they cross a bridge, check if its built, if not return false
            return False

        possible_locations = copy.deepcopy(map.map[current_location])
        for p in engine.players:
            if(p.character != player.character):
                if(p.location in map.map[current_location]):
                    possible_locations.extend(map.map[p.location])
        possible_locations = list(dict.fromkeys(possible_locations))
        return next_location in possible_locations
