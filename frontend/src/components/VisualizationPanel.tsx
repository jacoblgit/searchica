import { PlotMouseEvent } from "plotly.js";
import Plot from "react-plotly.js";

interface VisualizationPanelProps {
  plotData?: any;
  onPointClick?: (index: number) => void;
  hoveredId?: number | null;
}

function VisualizationPanel({
  plotData,
  onPointClick,
  hoveredId,
}: VisualizationPanelProps) {
  const defaultData = [
    {
      x: [],
      y: [],
      mode: "markers",
      type: "scatter",
      marker: {
        color: [],
        size: 10,
        opacity: [],
      },
      hovertext: [],
      hoverinfo: "text",
    },
  ];

  const defaultLayout = {
    showlegend: false,
    hovermode: "closest",
    xaxis: {
      showgrid: false,
      showticklabels: false,
      zeroline: false,
    },
    yaxis: {
      showgrid: false,
      showticklabels: false,
      zeroline: false,
    },
    plot_bgcolor: "white",
  };

  const data = plotData?.data ? [...plotData.data] : defaultData; // Create new array to avoid mutation

  if (hoveredId !== null && plotData) {
    data[0].marker.size = Array(data[0].x.length)
      .fill(10)
      .map((size, idx) => (idx === hoveredId ? 20 : 10));
  }

  return (
    <div
      className="border rounded p-4 bg-white shadow-sm"
      style={{ height: "80vh" }}
    >
      <Plot
        data={data}
        layout={plotData?.layout || defaultLayout}
        style={{ width: "100%", height: "100%" }}
        onClick={(event: PlotMouseEvent) => {
          if (event.points && event.points[0] && onPointClick) {
            onPointClick(event.points[0].pointIndex);
          }
        }}
      />
    </div>
  );
}

export default VisualizationPanel;
