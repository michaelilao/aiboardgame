import gameData from "./game2.json";
import allActions from "./allActions.json";

export default class Data {
  constructor(data = JSON.parse(JSON.stringify(gameData))) {
    this.data = data;
    this.allActions = allActions;
  }

  setAllData(data) {
    this.data = data;
  }

  setAllActions(actions) {
    this.allActions = actions;
  }

  getAllData() {
    return this.data;
  }

  getAllActions() {
    return this.allActions;
  }

  getAllDataExEnd() {
    let allDataExEnd = [];
    this.data.forEach((element) => {
      let elemData = {};

      Object.entries(element).forEach((turn) => {
        if (
          turn[1].action !== "End Turn" &&
          turn[1].action !== "Action Turn" &&
          turn[1].action !== "Convey Turn"
        ) {
          elemData[turn[0]] = turn[1];
        }
      });
      allDataExEnd.push(elemData);
    });
    return allDataExEnd;
  }

  getDataWithMergedActions(data) {
    let newData = JSON.parse(JSON.stringify(data));
    let allDataMerged = [];

    newData.forEach((element) => {
      Object.entries(element).forEach((turn) => {
        if (turn[0] !== "meta_data") {
          const actionDetail = turn[1].action_details;
          turn[1].action_details = `${turn[1].action} ${actionDetail}`;
        }
      });

      allDataMerged.push(element);
    });

    return allDataMerged;
  }

  getSimulationData(data, startIndex = 0, endIndex = 1) {
    return Object.keys(data)
      .slice(startIndex, endIndex)
      .reduce((result, key) => {
        result[key] = data[key];

        return result;
      }, {});

    //return Object.fromEntries(Object.entries(data).slice(startIndex, endIndex));
  }

  getPlayerData(data, player) {
    let playerData = {};

    Object.entries(data).forEach((turn) => {
      if (turn[0] !== "meta_data") {
        if (turn[1].player == player) {
          playerData[turn[0]] = turn[1];
        }
      }
    });

    return playerData;
  }

  getFrequencyMap() {
    let actions = [];
    Object.entries(this.allActions).forEach((action) => {
      actions.push({ name: action[0], frequency: 0 });
    });

    return actions;
  }

  getFrequencyMapForPlayer(data, startSim, endSim, player) {
    const simulationData = this.getSimulationData(data, startSim, endSim);

    let freqMap = this.getFrequencyMap();

    if (simulationData) {
      Object.entries(simulationData).forEach((simulation) => {
        const playerData = this.getPlayerData(simulation[1], player);

        Object.entries(playerData).forEach((turn) => {
          const objIndex = freqMap.findIndex(
            (obj) => obj.name == turn[1].action_details
          );
          if (objIndex !== -1) {
            freqMap[objIndex].frequency++;
          }
        });
      });
    }

    return freqMap;
  }

  getCountMap() {
    let actions = [];
    Object.entries(this.allActions).forEach((action) => {
      actions.push({ name: action[0], count: 0 });
    });

    return actions;
  }

  getCountMapForPlayer(data, startSim, endSim, player) {
    const simulationData = this.getSimulationData(data, startSim, endSim);

    let freqMap = this.getCountMap();
    if (simulationData) {
      Object.entries(simulationData).forEach((simulation) => {
        const playerData = this.getPlayerData(simulation[1], player);

        Object.entries(playerData).forEach((turn) => {
          const objIndex = freqMap.findIndex(
            (obj) => obj.name == turn[1].action_details
          );
          if (objIndex !== -1) {
            freqMap[objIndex].count++;
          }
        });
      });
    }
    return freqMap;
  }

  sortFrequencyMap(freqMap) {
    freqMap.sort((a, b) => {
      if (a.frequency !== b.frequency) {
        return a.frequency < b.frequency ? 1 : -1;
      }
      return 0;
    });
  }

  getAllNonZeroActions(frequencyMap) {
    let newMap = JSON.parse(JSON.stringify(frequencyMap));
    this.sortFrequencyMap(newMap);
    const filteredMap = newMap.filter((action) => {
      return action.frequency > 0;
    });
    return filteredMap;
  }

  // getMap(data, startSim, endSim, player) {
  //   let result = [];
  //   let map = {};
  //   const simulationData = this.getSimulationData(data, startSim, endSim);

  //   if (simulationData) {
  //     Object.entries(simulationData).forEach((simulation) => {
  //       let turnNum = 1;
  //       const playerData = this.getPlayerData(simulation[1], player);

  //       const size = Object.keys(playerData).length;
  //       Object.entries(playerData).forEach((turn, index) => {
  //         const turnStr = `Turn ${turnNum}, ${turn[1].action_details}`;
  //         if (!map.hasOwnProperty(turnStr)) {
  //           map[turnStr] = turnNum;
  //           result.push([]);
  //         }

  //         result[index].push(turnStr);
  //         turnNum++;

  //         if (index === size - 1) {
  //           if (!map.hasOwnProperty("End Game")) {
  //             map["End Game"] = turnNum;
  //             result.push([]);
  //           }
  //           result[turnNum - 1].push("End Game");
  //         }
  //       });
  //     });
  //   }
  //   return [result, map];
  // }

  getMap(data, startSim, endSim, player) {
    let result = [];
    const simulationData = this.getSimulationData(data, startSim, endSim);

    if (simulationData) {
      let simNum = 0;
      Object.entries(simulationData).forEach((simulation) => {
        let turnNum = 1;
        const playerData = this.getPlayerData(simulation[1], player);

        const size = Object.keys(playerData).length;
        if (size > 0) {
          result.push([]);
          Object.entries(playerData).forEach((turn, index) => {
            const turnStr = `Turn ${turnNum}, ${turn[1].action_details}`;

            result[simNum].push(turnStr);
            turnNum++;

            if (index === size - 1) {
              result[simNum].push("End Game");
            }
          });
        }
        simNum++;
      });
    }
    return result;
  }

  getScores(data, startSim, endSim) {
    const simulationData = this.getSimulationData(data, startSim, endSim);
    let result = [];
    if (simulationData) {
      Object.entries(simulationData).forEach((simulation, index) => {
        result.push({
          [`Sim ${index}`]: simulation[1].meta_data
            ? simulation[1].meta_data
            : {
                player_0: 0,
                player_1: 0,
                player_2: 0,
                player_3: 0,
                player_4: 0,
              },
        });
      });
    }
    return result;
  }

  getNumberOfPlayers(data) {
    let players = [];
    const simulation = Object.entries(data).find((sim) => {
      return sim[1].meta_data !== undefined;
    });
    if (simulation) {
      Object.entries(simulation[1]).forEach((turn) => {
        if (turn[0] === "meta_data") {
          Object.keys(turn[1]).forEach((player) => {
            const playerNum = Number(player.split("_")[1]);

            players.push(playerNum);
          });
        }
      });
    }
    return players;
  }

  getNumberOfSimulations(data) {
    let result = Array(Object.keys(data).length)
      .fill()
      .map((_, i) => i + 1);

    return result;
  }

  getNumberOfMoves(data, startSim, endSim, player) {
    const simulationData = this.getSimulationData(data, startSim, endSim);

    let result = 2;
    if (simulationData) {
      Object.entries(simulationData).forEach((simulation) => {
        const playerData = this.getPlayerData(simulation[1], player);
        const moves = Object.keys(playerData).length;

        if (moves > result) {
          result = moves;
        }
      });
    }
    return result + 1;
  }
}
