function similarityCurve(data, metric) {
    $("#heatmap3").html("")

	//need to change this data[0][1]
    data[0][1]  = 0
var margin = {top: 26, right: 0, bottom: 0, left: 30 },
    margin2 = {top: 5, right: 0, bottom: 0, left: 30 },
    width = globalWidth - margin.left - margin.right - 220,
    height = 100 - margin.top - margin.bottom,
    height2 = 100 - margin.top - margin.bottom;
                      
var x = d3.scale.linear().domain([0, data.length]).range([0, width]),
    x2 = d3.scale.linear().domain([0, data.length]).range([0, width]),
    y = d3.scale.linear().range([height, 0]),
    y2 = d3.scale.linear().range([height2, 0]);

var xAxis = d3.svg.axis().scale(x).orient("bottom"),
    xAxis2 = d3.svg.axis().scale(x2).orient("bottom").ticks(100),
    yAxis = d3.svg.axis().scale(y).orient("left")
          .orient("left").ticks(5);

var zoom = d3.behavior.zoom()
    .scaleExtent([1, 4])
    .on("zoom", zoomed);

var area = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x(d[0]); })
    .y0(height)
    .y1(function(d) { return y(d[1]); });

    brushSimilarity = []

    brushSimilarity = d3.svg.brush()
            .x(x)
            .extent([globalStartTimeStep,globalEndTimeStep]);

var area2 = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x2(d[0]); })
    .y0(height2)
    .y1(function(d) { return y2(d[1]); });

var svg = d3.select("#heatmap3")
    .attr("width", width + margin.left + margin.right+20)
    .attr("height", height + margin.top + margin.bottom);


var context = svg.append("g")
    .attr("class", "context")
    .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");


// Add rect cover the zoomed graph and attach zoom event.
var appendData = function(data) {
	x.domain(d3.extent(data.map(function(d) {  return d[0]; })));
	  y.domain([0, d3.max(data.map(function(d) { return d[1]; }))]);
	  x2.domain(x.domain());
	  y2.domain(y.domain());

	  // Set up zoom behavior
	  context.append("path")
            .datum(data)
            .attr("class", "area")
            .attr("stroke", "black")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 1)
            .attr("d", area2);

    for (k=1; k<stateValues.length-1; k++){
        var rect = []
        rect = context.selectAll("g")
            .data(stateValues[k])
          .enter().append("svg:g")

        rect1 = rect.append("rect")
                .attr("x", function (d,i) {return x(d[0])+2;} )
                .attr("y", 2 + k*6)
                .attr("rx", 6)
                .attr("ry", 6)
                .attr("width", function (d,i) { return x(d[1]-d[0]) + 5;})
                .attr("height", 72 - k*9)
                .attr("fill", "steelblue")
                .attr("fill-opacity", 0.025)
                .attr("stroke", "steelblue")
                .attr("stroke-linejoin", "round")
                .attr("stroke-linecap", "round")
                .attr("stroke-width", 2);

        rect.append("text")
            .attr("x", function (d,i) { return x(d[0])+ (2-k)*9;} )
            .attr("y", 15+ k*6)
            .text(function(d,i){return String(k)});
    }
    context.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("svg")
        .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("y", 1)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text(String(metric));

	  context.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height2 + ")")
	      .call(xAxis2);

	  // brushSimilarityUpdate = context.append("g")
	  //     .attr("class", "x brush")
   //        .call(brushSimilarity)
	  //   .selectAll("rect")
	  //     .attr("y", -6)
	  //     .attr("height", height2 + 9);


    function zoomed() {
          var xz = d3.event.transform.rescaleX(x);
          xGroup.call(xAxis.scale(xz));
          areaPath.attr("d", area.x(function(d) { return xz(d.date); }));
    }

	}
      var brushCell;

        function zoomed() {
            
            container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }



      function brushed() {
          var extent0 = brushSimilarity.extent(),
              extent1;

          // if dragging, preserve the width of the extent
          if (d3.event.mode === "move") {
            var d0 = Math.round(extent0[0])
               d1 = Math.round(extent0[1]);
            extent1 = [d0, d1];

            $( "#timeStepSlider" ).slider( "values", [extent1[0],extent1[1]]);
            
            brushTemporalMetric.extent([extent1[0],extent1[1]])
            brushTemporalMetric(d3.select(".brush1").transition().duration(1));
            brushTemporalMetric.event(d3.select(".brush1").transition().delay(1).duration(1))

            brushNodeSpecificTemporalMetric.extent([extent1[0],extent1[1]])
            brushNodeSpecificTemporalMetric(d3.select(".brush2").transition().duration(0));
            brushNodeSpecificTemporalMetric.event(d3.select(".brush2").transition().delay(1).duration(5))

            brushHeatmap.extent([extent1[0],extent1[1]])
            brushHeatmap(d3.select(".brushForHeatmap").transition().duration(0));
            brushHeatmap.event(d3.select(".brushForHeatmap").transition().delay(1).duration(5))
          }
          else {
            extent1 = extent0;

            $( "#timeStepSlider" ).slider( "values", [extent1[0],extent1[1]]);
            d3.select(this).call(brushSimilarity.extent(extent1));
          }
      }
    appendData(data);
}	