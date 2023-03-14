import React, { useState, useEffect } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";
import Data from "../data/getData";
import SimulationFileSelection from "./Selections/SimulationFileSelection";
import PlayerSelection from "./Selections/PlayerSelection";
import SimulationSelection from "./Selections/SimulationSelection";

ChartJS.register(ArcElement, Tooltip, Legend);

const getRandomColor = () => {
  return "#" + Math.floor(Math.random() * 16777215).toString(16);
};

//parameter
const dataInit = new Data();

const getLabels = (allNonZeroActions) => {
  let labels = [];
  Object.entries(allNonZeroActions).forEach((action) => {
    labels.push(action[1].name);
  });
  return labels;
};

const getValues = (allNonZeroActions) => {
  let values = [];
  Object.entries(allNonZeroActions).forEach((action) => {
    values.push(action[1].frequency);
  });
  return values;
};

const getBackgroundColors = (allNonZeroActions) => {
  let backgroundColors = [];
  allNonZeroActions.forEach((action) => {
    backgroundColors.push(getRandomColor());
  });

  return backgroundColors;
};

const getBorderColors = (allNonZeroActions) => {
  let borderColors = [];
  allNonZeroActions.forEach((action) => {
    borderColors.push("#000000");
  });

  return borderColors;
};

const PieChart = ({ width, height }) => {
  const [loading, setLoading] = useState(null);
  const [simulationFile, setSimulationFile] = useState("none");
  const [allData, setAllData] = useState(dataInit.getAllDataExEnd());
  const [players, setPlayers] = useState(dataInit.getNumberOfPlayers(allData));
  const [numSimulations, setNumSimulations] = useState(
    dataInit.getNumberOfSimulations(allData)
  );
  const [player, setPlayer] = useState(0);
  const [numSims, setNumSims] = useState(1);
  const [freqMap, setFreqMap] = useState([]);
  const [allNonZeroActions, setAllNonZeroActions] = useState([]);
  const [data, setData] = useState({
    labels: [],
    datasets: [],
  });

  useEffect(() => {
    fetch(simulationFile)
      .then((response) => {
        loading !== null && setLoading(true);
        return response.json();
      })
      .then((data) => {
        dataInit.setAllData(data);
        setAllData(dataInit.getAllDataExEnd());
      })
      .catch((error) => {
        console.log(error);
      });
  }, [simulationFile]);

  useEffect(() => {
    setPlayers(dataInit.getNumberOfPlayers(allData));
    setNumSimulations(dataInit.getNumberOfSimulations(allData));
  }, [allData]);

  useEffect(() => {
    const mergedData = dataInit.getDataWithMergedActions(allData);

    setFreqMap(dataInit.getFrequencyMapForPlayer(mergedData, numSims, player));
  }, [allData, player, numSims]);

  useEffect(() => {
    setAllNonZeroActions(dataInit.getAllNonZeroActions(freqMap));
    setLoading(false);
  }, [allData, freqMap]);

  useEffect(() => {
    setData({
      labels: getLabels(allNonZeroActions),
      datasets: [
        {
          label: "# of times used",
          data: getValues(allNonZeroActions),
          backgroundColor: getBackgroundColors(allNonZeroActions),
          borderColor: getBorderColors(allNonZeroActions),
          borderWidth: 0.5,
        },
      ],
    });
  }, [allData, allNonZeroActions]);

  return (
    <div
      style={{
        marginBottom: 20,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        margin: "auto",
      }}
    >
      <h1>All Used Moves Frequency</h1>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
        }}
      >
        <SimulationFileSelection setSimulationFile={setSimulationFile} />
        <PlayerSelection
          setPlayer={setPlayer}
          players={players}
          simulationFile={simulationFile}
        />
        <SimulationSelection
          setNumSims={setNumSims}
          numSimulations={numSimulations}
          simulationFile={simulationFile}
          value={numSims}
        />
      </div>
      {loading && <h2>Loading...</h2>}
      {simulationFile !== "none" && !loading && (
        <div style={{ overflowX: "scroll", marginTop: 20 }}>
          {
            <Pie
              data={data}
              width={width}
              height={height}
              options={{ maintainAspectRatio: false }}
            />
          }
        </div>
      )}
    </div>
  );
};

export default PieChart;
