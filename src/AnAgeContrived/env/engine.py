from .helpers.convey import Convey
from .helpers.turn import Turn
from .entities.turn_state import TurnState
from .entities.player import Player
from env.entities.monument import Monument
from env.entities.monument_wall import MonumentWall
from .action_initiater import get_actions
from env.entities.energy import Energy

CHARACTER_NAMES = ["Freyith", "Ignotas", "Multanec", "Rusne"]
AGENT_NAMES = ["player_0", "player_1", "player_2", "player_3"]
NUM_MOVES = len(get_actions('self', 'eng'))

#Monuments From The Rule Book:
THE_ANFIRIEN_BEACON = Monument('THE ANFIRIEN BEACON', 'location', [
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.INVERTIBLE, Energy.INVERTIBLE], [Energy.CONSTRUCTIVE, Energy.INVERTIBLE]),
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.CONSTRUCTIVE, Energy.GENERATIVE], [Energy.PRIMAL]),
                                                        MonumentWall([Energy.GENERATIVE, Energy.INVERTIBLE, Energy.INVERTIBLE], [Energy.GENERATIVE]),
                                                        MonumentWall([Energy.GENERATIVE, Energy.CONSTRUCTIVE], ['Any']) #TODO: Need a mechanism to handle any energy reward
                                                    ])
THE_LIBRARY_OF_VALDUIN = Monument('THE LIBRARY OF VALDUIN', 'location', [
                                                        MonumentWall([Energy.GENERATIVE, Energy.CONSTRUCTIVE, Energy.CONSTRUCTIVE], [Energy.GENERATIVE, Energy.INVERTIBLE]),
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.INVERTIBLE, Energy.INVERTIBLE], [Energy.CONSTRUCTIVE]),
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.GENERATIVE, Energy.GENERATIVE], [Energy.PRIMAL]),
                                                        MonumentWall([Energy.INVERTIBLE, Energy.GENERATIVE], ['Any']) #TODO: Need a mechanism to handle any energy reward
                                                    ])
THE_ERIDONIC_GATE = Monument('THE ERIDONIC GATE', 'location', [
                                                        MonumentWall([Energy.GENERATIVE, Energy.INVERTIBLE, Energy.INVERTIBLE], [Energy.CONSTRUCTIVE, Energy.GENERATIVE]),
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.INVERTIBLE, Energy.GENERATIVE], [Energy.INVERTIBLE]),
                                                        MonumentWall([Energy.GENERATIVE, Energy.CONSTRUCTIVE, Energy.CONSTRUCTIVE], [Energy.GENERATIVE]),
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.INVERTIBLE], ['Any']) #TODO: Need a mechanism to handle any energy reward
                                                    ])
THE_NAMARILLION_FORGE = Monument('THE NAMARILLION FORGE', 'location', [
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.GENERATIVE, Energy.GENERATIVE], [Energy.INVERTIBLE, Energy.GENERATIVE]),
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.INVERTIBLE, Energy.GENERATIVE], [Energy.PRIMAL]),
                                                        MonumentWall([Energy.GENERATIVE, Energy.INVERTIBLE, Energy.INVERTIBLE], [Energy.CONSTRUCTIVE]),
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.INVERTIBLE], ['Any']) #TODO: Need a mechanism to handle any energy reward
                                                    ])
THE_FORTRESS_OF_KOLYM_THRIN = Monument('THE FORTRESS OF KOLYM THRIN', 'location', [
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.INVERTIBLE, Energy.GENERATIVE], [Energy.CONSTRUCTIVE, Energy.PRIMAL]),
                                                        MonumentWall([Energy.INVERTIBLE, Energy.INVERTIBLE, Energy.GENERATIVE], [Energy.GENERATIVE]),
                                                        MonumentWall([Energy.GENERATIVE, Energy.INVERTIBLE], ['Any']),#TODO: Need a mechanism to handle any energy reward
                                                        MonumentWall([Energy.CONSTRUCTIVE, Energy.CONSTRUCTIVE, Energy.GENERATIVE], [Energy.INVERTIBLE]),
                                                        MonumentWall([Energy.PRIMAL], []),
                                                    ])
THE_SHIP_OF_TOLINTHRA = Monument('THE SHIP OF TOLINTHRA', 'location', [
                                                        MonumentWall([Energy.GENERATIVE, Energy.GENERATIVE, Energy.INVERTIBLE], [Energy.CONSTRUCTIVE, Energy.INVERTIBLE]),
                                                        MonumentWall([Energy.GENERATIVE, Energy.CONSTRUCTIVE, Energy.INVERTIBLE], [Energy.GENERATIVE]),
                                                        MonumentWall([Energy.INVERTIBLE, Energy.CONSTRUCTIVE, Energy.CONSTRUCTIVE], [Energy.PRIMAL]),
                                                        MonumentWall([Energy.GENERATIVE, Energy.CONSTRUCTIVE], ['Any']) #TODO: Need a mechanism to handle any energy reward
                                                    ])

class Engine:
    def __init__(self):
        self.turnCounter = 0
        self.actionCounter = 0
        self.game = 1
        self.current_player = 0
        self.player_turn_queue = []
        self.players = []
        self.turn = TurnState()
        self.monuments = [THE_ANFIRIEN_BEACON, THE_LIBRARY_OF_VALDUIN ,THE_ERIDONIC_GATE, THE_NAMARILLION_FORGE , THE_FORTRESS_OF_KOLYM_THRIN, THE_SHIP_OF_TOLINTHRA]
        for i in range(4):
            self.players.append(Player(AGENT_NAMES[i], CHARACTER_NAMES[i]))

    def check_over(self):
        return self.turnCounter == 4*5

    def reset(self):
        self.__init__()

    def get_agents(self):
        return AGENT_NAMES

    def get_characters(self):
        return CHARACTER_NAMES

    def get_agent(self, name):
        for player in self.players:
            if player.get_player_name() == name:
                return player

    # Gets number of total actions
    def get_action_space(self):
        return NUM_MOVES

    def get_observation_space_shape(self):
        # index=0 will be all possible states, index=1 will be value for that state, index=2 is #of players,
        #TODO: might want to automate this as well instead of hardcoding it to make the new functionality integration easier
        return(7, 4, 1)

    def get_legal_actions(self, agent_name):
        actions = get_actions(self.players[self.current_player], self)
        legal_actions = []
        for action in actions:
            isLegal = action.check()
            legal_actions.append(isLegal)
        return legal_actions

    def play_turn(self, agent_name, action):
        agent = self.get_agent(agent_name)
        print(self.get_legal_actions(self.current_player))

        if(not self.get_legal_actions(self.current_player)[action]):
            print("ILLEGAL MOVE, is", action)
            return

        actions = get_actions(self.players[self.current_player], self)
        actions[action].execute()

        #check whether the monument wall is filled and either:
        # 1: start a mini turn for players who have energy tiles on the wall or
        # 2: end the game if all the walls of all the monuments are filled
        num_of_built_monuments = 0
        # for monument in self.monuments: #TODO: Later convert to this condition
        for i in range(0, 1):
            monument = self.monuments[i]
            if monument.is_top_wall_completed():
                filled_wall = monument.get_top_wall()
                monument.change_top_wall() #if the current top wall is completed, change the top wall to next wall
                #TODO: start mini turn here, use filled_wall to get the energy and the owner's of the energy to know which players will be part of the mini turn
            if monument.is_completed():
                num_of_built_monuments += 1
        #check if all monuments are built
        if num_of_built_monuments == len(self.monuments):
            #TODO: set game end condition to true and calculate the player's points
            pass
        self.actionCounter += 1


    def get_current_agents_turn(self):
        return self.get_agents()[self.current_player]

    def get_current_characters_turn(self):
        return CHARACTER_NAMES[self.current_player]

    def get_game_state_others(self, agent_name):
        others_game_state = []
        for agent in AGENT_NAMES:
            if(agent != agent_name):
                others_game_state.append(self.get_game_state(agent_name))
        return others_game_state

    def get_game_state(self, agent_name):
        return self.get_agent(agent_name).get_transmuter().getState()

    def get_reward(self, agent_name):
        return self.get_agent(agent_name).get_transmuter().getTotalEmptyCells() * 10

    def get_winner(self):
        max = 0
        winner = ""
        for agent in AGENT_NAMES:
            if self.get_agent(agent).get_transmuter().getTotalEmptyCells() > max:
                winner = agent
        return winner

    def render(self, agent_name):
        agent = self.get_agent(agent_name)
        print(agent.character)
        agent.get_transmuter().printTransmuter()
        # print(self.monuments[0].get_top_wall().print_wall())
        self.turn.print_turn_state()