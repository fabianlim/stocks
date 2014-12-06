// write a PCA visualizer
// inspired by weiglemc's block

$(document).ready(function() {

    function singularValuesLineChart(){
        
        // var margin = {top: 20, right: 20, bottom: 30, left: 40},
        var margin = {top: 20, right: 20, bottom: 30, left: 60},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

        // setup the scales
        var xScale = d3.scale.linear().range([0, width]);
        var yScale = d3.scale.log().range([height, 0]).nice();

        // An area generator, for the light fill.
        var area = d3.svg.area()
            .interpolate("monotone")
            .x(function(d, i) { return xScale(i+1); })
            .y0(height)
            .y1(function(d) { return yScale(d); });

        // construct the chart
        var chart = function(selection) {
            
            selection.each(function(d) {
                // d is the datum attached to the selection

                // add the graph canvas 
                var svg = d3.select(this).append("svg")
                    .style("width", width + margin.left + margin.right)
                    .style("height", height + margin.top + margin.bottom)
                .append("g")
                    .attr("transform", 
                        "translate(" + 
                        margin.left + "," + margin.top + ")");

                
                var tag_html = function (name, x) { 
                    return "<strong>" + name + " :</strong> <span style='color:red'>" + x + "</span>";},
                    tip = d3.tip()
                      .attr('class', 'd3-tip')
                      .offset([-10, 0])
                      .html(function(d, i) {
                        return tag_html("Std-dev", d.toExponential(1)) + 
                            "</br>"+ tag_html("Comp    ", i+1);});

                svg.call(tip);

                // set the domain
                var xAxis = d3.svg.axis()
                    .scale(xScale.domain([1, d.length]))
                    .orient("bottom");

                // y scale
                var yAxis = d3.svg.axis()
                    .scale(yScale.domain(d3.extent(d)))
                    .tickValues(function(d) {
                        return d.map(
                            function(x) {
                                // exponent in base 10
                                function exponent(y) {
                                    return Math.floor(
                                        Math.log(x) / Math.log(10));
                                }
                                return Math.pow(10, exponent(x));
                            }
                        );
                    })
                    .orient("left");

                // x-axis
                svg.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis);

                // y-axis
                svg.append("g")
                    .attr("class", "y axis")
                    .call(yAxis);

                // Add the clip path.
                svg.append("clipPath")
                    .attr("id", "clip")
                    .append("rect")
                    .attr("width", width)
                    .attr("height", height);

                // Add the area path.
                svg.append("path")
                    .attr("class", "area")
                    .attr("clip-path", "url(#clip)")
                    .attr("d", area(d));

                // for the appearing lines
                var cross_lines = svg.append("g")
                    .style("display", "none");

                // mouseOver callback
                var mouseOver = function(d, i) {
                    var circle = d3.select(this);
                    circle.transition().duration(50)
                        .attr("r", 10);

                    // unset cross_lines display style
                    cross_lines.style("display", null);

                    // draw horizontal line
                    cross_lines.append("line")
                        .attr("class", "crossline")
                        .attr("x1", 0)
                        .attr("x2", circle.attr("cx"))
                        .attr("y1", circle.attr("cy"))
                        .attr("y2", circle.attr("cy"));

                    // draw vertical line
                    cross_lines.append("line")
                        .attr("class", "crossline")
                        .attr("x1", circle.attr("cx"))
                        .attr("x2", circle.attr("cx"))
                        .attr("y1", circle.attr("cy"))
                        .attr("y2", height);

                    // tip
                    tip.show(d, i);
                };

                // mouseOut callback
                var mouseOut = function() {
                    var circle = d3.select(this);
                    circle.transition().duration(50)
                        .attr("r", 5 );

                    // set display style
                    cross_lines.style("display", null);

                    // remove the lines
                    cross_lines.selectAll("line").remove();
                    
                    // tip
                    tip.hide();
                };

                // // draw dots
                svg.selectAll(".dot")
                    .data(d)
                  .enter().append("circle")
                    .attr("class", "dot")
                    .attr("r", 5)
                    //.attr("cx", xMap)
                    .attr("cx", function(d, i) { 
                        return xScale(i+1);
                    })
                    // attr("cy", yMap)
                    .attr("cy", function(d) { 
                        return yScale(d);
                    })
                    .on("mouseover", mouseOver)
                    .on("mouseout", mouseOut)
                    .on("click", function(d, i) {
                        d3.selectAll('.dot').classed("on", false);
                        d3.select(this).classed("on", 'true');
                        if (chart.click_func) {
                            chart.click_func(i);
                        }
                    });

                // draw axis labels
                svg.append("text")
                    .attr("class", "label")
                    .attr("transform", "translate(0," + height + ")")
                    .attr("x", width)
                    .attr("y", -6)
                    .style("text-anchor", "end")
                    .text("Component");

                svg.append("text")
                    .attr("class", "label")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Standard-Dev");
            });
        };

        return chart;
    }

    // create the radialBarChart
    var radial_chart = radialBarChart()
        .horizon
        .barHeight(150)
        .margin({top: 100, right: 100, bottom: 100, left: 100})
        .colorscheme(colorbrewer.RdBu[4])
        .domain([0, 1])
        .tickCircleValues([0.2, 0.4, 0.6, 0.8]);

    // create the line chart
    var line_chart = singularValuesLineChart();

    // took this from Stack Overflow
    function parseQueryString(q) {
            var params = {},
                e,
                a = /\+/g,  // Regex for replacing addition symbol with a space
                r = /([^&=]+)=?([^&]*)/g,
                d = function (s) { 
                    return decodeURIComponent(s.replace(a, " ")); 
                };

            while (e = r.exec(q))
                params[d(e[1])] = d(e[2]);

            return params;
    }

    // work around because I cannot seem to find a way to get the
    // query string from the get request. location.search will not
    // work when the window that issues the get request has an
    // empty query
    var queryDict;
    if (location.search) {
        queryDict = parseQueryString(location.search.substring(1));
    } else {
        // if location search is empty, try localStorage
        queryDict = JSON.parse(localStorage.getItem('pca'));
    }

    // display the data
    var algo_url = queryDict.algo_url;
    delete queryDict.algo_url; // the algo_url portion is not needed

    $.get(algo_url, 
            queryDict,
            function(data) {

                // parse the eigen dirs data and store 
                var eigen_dirs = JSON.parse(data.eigen_dirs);

                // set the click function of the line chart
                line_chart.click_func = function(i) {
                    var d = {};
                    for (var key in eigen_dirs) {
                        d[key] = eigen_dirs[key][i];
                    }

                    var g = d3.select('#pca-visualizer')
                        .selectAll('#radial-chart')
                        .data([[{data: d}]])
                        .call(radial_chart);
                };

                // show the line graph
                d3.select("#pca-visualizer")
                    .select('#line-chart')
                    .datum(data.singular_values)
                    .call(line_chart);
                    
                (function () {
                    // create an empty radial chart that 
                    // shows the features

                    var d = {};
                    for (var key in eigen_dirs) {
                        d[key] = 0;
                    }

                    d3.select('#pca-visualizer')
                        .select('#radial-chart')
                        .datum([{data: d}])
                        .call(radial_chart);
                })();

                // update the validity of the computation
                $('#validity').html(function() {
                    return "Computed on " + data.input_validity;
                });

            },
            'json');
});
