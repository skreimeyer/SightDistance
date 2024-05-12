import plotly.graph_objects as go
from pathlib import Path

from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, NumberField, OptionField, Image
from viktor.views import PlotlyResult, PlotlyView, PlotlyAndDataResult, PlotlyAndDataView, DataGroup, DataItem, WebView, WebResult, ImageView, ImageResult

import core

def on_curve(params, **kwargs):
    if params.curve == 'True':
        return True
    else:
        return False

def summary_text(filename="SSDsummary.md"):
    source = Path(__file__).parent / "narrative" / filename
    return source.read_text()

class Parametrization(ViktorParametrization):

    speed = NumberField(
        'Speed (mph)',
        default=70,
        min=0,
        max=120,
        step=5,
        description="Speed in miles per hour, expected increments of 5 mph"
    )

    grade = NumberField(
        'Grade (%)',
        default=0.0,
        min=-999.0,
        max=999.0,
        description="Grade in percent. Negative values represent a descent. Positive values represent an ascent."
    )

    curve = OptionField(
        'Curve',
        options=['True', 'False'],
        variant='radio-inline',
        description="Is the road segment curved?"
    )

    radius = NumberField(
        'Radius (ft)',
        default=1000.0,
        min=1.0,
        max=1e6,
        #step=5.0,
        visible=on_curve,
        description="Radius of curvature in feet"
    )

    median = NumberField(
        'Median offset (ft)',
        default=0.0,
        min=0.0,
        max=100.0,
        visible=on_curve,
        description="Median offset in feet. This would include the width of a dividing barrier or separation from a center control line."
    )

    median_visibility = OptionField(
        'Median visibility',
        options=['Clear', 'Obstructed'],
        variant='radio-inline',
        visible=on_curve,
        description="Is the median clear or obstructed?"
    )

    lanes = NumberField(
        'Number of lanes',
        default=1,
        min=0,
        max=10,
        step=1,
        visible=on_curve,
        description="Number of lanes"
    )

    lane_width = NumberField(
        'Lane width (ft)',
        default=12.0,
        min=0,
        max=100.0,
        #step=0.5,
        visible=on_curve,
        description="Lane width in feet. If lane width is not constant, use an average value."
    )


class Controller(ViktorController):
    label = 'My Entity Type'
    parametrization = Parametrization

    @WebView("Theory", duration_guess=1)
    def show_html(self, params, **kwargs):
        content = Path(__file__).parent / "narrative" / "Theory.html"
        return WebResult.from_path(content)
    @PlotlyAndDataView('Results', duration_guess=1)
    def generate_view(self, params, **kwargs):
        mph = params.speed
        grade = params.grade/100.0
        curve = params.curve
        radius = params.radius
        lanes = params.lanes
        lane_width = params.lane_width
        median = params.median
        median_visibility = True if params.median_visibility == 'Clear' else False

        ssd = core.stopping_sight_distance(mph, grade)
        if curve == 'True':
            hso = round(core.hso(radius, mph, lanes, lane_width, grade, median), 2)
            offset = round(core.clear_offset(radius, mph, lanes, lane_width, grade, median), 2)
            inside_shoulder_offset = core.clear_inside_shoulder(radius, mph, grade, median, median_visibility)
        else:
            hso = 0.0
            offset = 0.0
            inside_shoulder_offset = 0.0
        dsds = [core.decision_sight_distance(mph, m, grade) for m in core.Maneuver.list_maneuvers()]

        data = [ssd, *dsds]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[core.feet_to_station(d) for d in data],
            y=[0 for d in data],
            mode='text',
            text=["S","A","B","C","D","E"],
            textfont=dict(color="black",size=20),
            textposition="top center",
        ))
        fig.update_xaxes(
            tickmode = 'linear',
            ticks = 'inside',
            tickson = 'boundaries',
            tick0 = 0,
            dtick = 1,
            ticklen = 25,
            gridcolor = 'black',
        )
        fig.update_yaxes(showgrid=False,
                         zeroline=True, zerolinecolor='black', zerolinewidth=3,
                         showticklabels=False)
        fig.update_layout(title="Stopping Sight Distance and Decision Sight Distances",plot_bgcolor='white',xaxis_title="Station",)

        summary = DataGroup(
            DataItem("Stopping Sight Distance", ssd),
            DataItem("Horizontal Sight Offset", hso),
            DataItem("Outside Shoulder Clear Offset", offset),
            DataItem("Inside Shoulder Clear Offset", inside_shoulder_offset),
            DataItem("Decision Sight Distance (A):", dsds[0]),
            DataItem("Decision Sight Distance (B):", dsds[1]),
            DataItem("Decision Sight Distance (C):", dsds[2]),
            DataItem("Decision Sight Distance (D):", dsds[3]),
            DataItem("Decision Sight Distance (E):", dsds[4]),
        )
        return PlotlyAndDataResult(fig.to_json(), summary)

    @ImageView("Diagram", duration_guess=1)
    def show_diagram(self, params, **kwargs):
        return ImageResult.from_path(Path(__file__).parent / "svg" / "Diagram.svg")

