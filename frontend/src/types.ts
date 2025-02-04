export interface EmailResult {
    id: number;
    subject: string;
    from: string;
    date: string;
    body: string;
    to: string;
    cc: string;
    score: number;
  }

  export interface Marker {
    color: string[];
    size: number | number[];
    opacity: number[];
  }
  
  export interface Trace {
    x: number[];
    y: number[];
    mode: string;
    type: string;
    marker: Marker;
    customdata: number[];
    hovertext: string[];
    hoverinfo: string;
  }
  
  export interface PlotData {
    data: Trace[];
    layout: {
      showlegend: boolean;
      hovermode: string;
      xaxis: {
        showgrid: boolean;
        showticklabels: boolean;
        zeroline: boolean;
      };
      yaxis: {
        showgrid: boolean;
        showticklabels: boolean;
        zeroline: boolean;
      };
      plot_bgcolor: string;
    };
  }