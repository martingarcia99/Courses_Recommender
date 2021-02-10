from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.resources import CDN
from bokeh.models import FactorRange, OpenURL, TapTool, Legend, LegendItem
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

            #url = "https://laproject.herokuapp.com/course/@courses"
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

    def createAverageRatingGraph(self, rating, semester):

        semesters = ['ss19', 'ws19-20', 'ss20', 'ws20-21']
        #avg. of course rating
        avg = []
        status = ["Is Present", "Is Not Yet Present","Is Not Yet Present","Is Not Yet Present"]
        status1 = ["Is Not Yet Present","Is Present","Is Not Yet Present","Is Not Yet Present"]
        status2 = ["Is Not Yet Present", "Is Not Yet Present","Is Not Yet Present","Is Not Yet Present"]

        rating = rating.replace(",",".")
        if semester == 'ss19':
            avg = [float(rating),5,5,5]
            source = ColumnDataSource(data=dict(semester=semesters, avg=avg, status=status, color=["green","blue","blue","blue"]))
        elif semester == 'ws19-20':
            avg = [5,float(rating), 5, 5]
            source = ColumnDataSource(data=dict(semester=semesters, avg=avg, status=status1, color=["blue","green","blue","blue"]))
        else:
            avg = [5,5,5,5]
            source = ColumnDataSource(data=dict(semester=semesters, avg=avg, status=status2, color=["blue","blue","blue","blue"]))
        
        # source = ColumnDataSource(data=dict(semester=semesters, avg=avg, color=["green","blue","blue","blue"]))

        print(semesters)
        print(avg)
        TOOLTIPS = [("AverageRating", "@avg")]

        p2 = figure(x_range=semesters, plot_height=250, tools="hover,pan,box_select,zoom_in,zoom_out,save,reset,tap", tooltips=TOOLTIPS)

        p2.vbar(x='semester', top='avg', width=0.9, fill_alpha=0.5, color='color',source=source, legend='status')

        p2.line(x=semesters, y=avg, color="red", line_width=2)

        # url = "https://trello.com/c/YcD1oQfR/36-bokeh-visualization-of-the-recommendation"
        # taptool = p2.select(type=TapTool)
        # taptool.callback = OpenURL(url=url)
        
        p2.y_range.start = 0
        p2.x_range.range_padding = 0.1
        p2.xaxis.major_label_orientation = 1
        p2.xgrid.grid_line_color = None
        p2.legend.location = "top_left"
        script2,div2 = components(p2)
        cdn_js2 = CDN.js_files[0]
        cdn_css2 = CDN.css_files
        return script2, div2, cdn_css2, cdn_js2
    
    
        