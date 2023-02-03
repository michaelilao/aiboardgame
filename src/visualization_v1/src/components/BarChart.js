import React, { useMemo } from "react";
import { Bar } from "@visx/shape";
import { Group } from "@visx/group";
import { GradientTealBlue } from "@visx/gradient";
import { scaleBand, scaleLinear } from "@visx/scale";
import { AxisBottom, AxisLeft } from "@visx/axis";

const data = [
  { name: "Move 1", frequency: 10 },
  { name: "Move 2", frequency: 2 },
  { name: "Move 3", frequency: 15 },
  { name: "Move 4", frequency: 1 },
  { name: "Move 5", frequency: 3 },
  { name: "Move 6", frequency: 9 },
];

const axisTextColor = "#000000";
const getMove = (move) => move.name;
const getFrequecy = (move) => move.frequency;

const axisBottomScale = scaleBand({
  domain: data.map(getMove),
  padding: 0.2,
});

const axisLeftScale = scaleLinear({
  domain: [0, Math.max(...data.map(getFrequecy))],
  nice: true,
  padding: 0.2,
});

const verticalMargin = 120;

const BarChart = ({ width, height }) => {
  const xMax = width;
  const yMax = height - verticalMargin;

  const xScale = useMemo(
    () =>
      scaleBand({
        range: [0, xMax],
        round: true,
        domain: data.map(getMove),
        padding: 0.4,
      }),
    [xMax]
  );
  const yScale = useMemo(
    () =>
      scaleLinear({
        range: [yMax, 0],
        round: true,
        domain: [0, Math.max(...data.map(getFrequecy))],
      }),
    [yMax]
  );

  axisBottomScale.rangeRound([0, xMax]);
  axisLeftScale.rangeRound([yMax, 0]);

  return (
    <div className="centering">
      <svg width={width} height={height}>
        <GradientTealBlue id="teal" />
        <rect width={width} height={height} fill="url(#teal)" rx={14} />
        <Group top={verticalMargin / 2}>
          {data.map((d) => {
            const move = getMove(d);
            const barWidth = xScale.bandwidth();
            const barHeight = yMax - (yScale(getFrequecy(d)) ?? 0);
            const barX = xScale(move);
            const barY = yMax - barHeight;
            return (
              <Bar
                key={`bar-${move}`}
                x={barX}
                y={barY}
                width={barWidth}
                height={barHeight}
                fill="rgba(23, 233, 217, .5)"
                //   onClick={() => {
                //     if (events) alert(`clicked: ${JSON.stringify(Object.values(d))}`);
                //   }}
              />
            );
          })}
        </Group>
        <AxisLeft
          left={20}
          top={60}
          scale={axisLeftScale}
          stroke={axisTextColor}
          tickStroke={axisTextColor}
          tickLabelProps={() => ({
            fill: axisTextColor,
            fontSize: 12,
            textAnchor: "middle",
          })}
        />
        <AxisBottom
          top={yMax + 60}
          scale={axisBottomScale}
          stroke={axisTextColor}
          tickStroke={axisTextColor}
          tickLabelProps={() => ({
            fill: axisTextColor,
            fontSize: 12,
            textAnchor: "middle",
          })}
        />
      </svg>
    </div>
  );
};

export default BarChart;