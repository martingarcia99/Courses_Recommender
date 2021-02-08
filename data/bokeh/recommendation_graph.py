from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.resources import CDN
from bokeh.models import FactorRange, OpenURL, TapTool
from bokeh.palettes import GnBu3, OrRd3

class RecommendationGraph:

    def createRecommendationGraph(self, recommendations):
        courses = []
        percentage = []
        if recommendations:
            for x in recommendations:
                if x[0] not in courses:
                    p = x[1] * 100
                    courses.append(x[0])
                    percentage.append(p)

            source = ColumnDataSource(data=dict(courses=courses, percentage=percentage))

            TOOLTIPS = [("name","@courses"), ("percentage", "@percentage{0.2f}")]

            # sorting the bars means sorting the range factors
            sorted_courses = sorted(courses, key=lambda x: percentage[courses.index(x)])

            p = figure(x_range=sorted_courses, plot_height=350, y_range=(0,100), title="Recommendation %", tools="hover,pan,box_select,zoom_in,zoom_out,save,reset,tap", tooltips=TOOLTIPS) 

            p.vbar(x='courses', top='percentage', width=0.5, source=source, color="rgb(52,101,164)")

            # url = "https://laproject.herokuapp.com/course/@courses"
            url = "http://127.0.0.1:5000/course/@courses"
            

            taptool = p.select(type=TapTool)
            taptool.callback = OpenURL(url=url)

            p.xaxis.visible = None
            p.xgrid.grid_line_color = None
            p.y_range.start = 0

            script,div = components(p)
            cdn_js = CDN.js_files[0]
            cdn_css = CDN.css_files
            return script, div, cdn_css, cdn_js
        else:
            print("No recommendations found")
            return "No recommendations found"

    
    
        