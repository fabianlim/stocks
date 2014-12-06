// a rewrite of radialBarChart by prcweb
// a more compartmentalized design 
// some added features

function radialBarChart() {

    // function init
    function init(d) {

        // d would be an array of objects 
        // in the form [{data: ... array ...}, ...
        //              {data: ... array ...}]

        // parameter defaults
        var barHeight = init.barHeight || 100;
        var domain    = init.domain    || [0, 100];

        // if array, assume they all have the same keys
        // use jQuery to check if array
        if ($.isArray(d))
            d = d[0]; // only need the single element

        // create the bar scale
        barScale = d3.scale.linear().domain(domain).range([0, barHeight]);

        // get keys
        keys = d3.map(d.data).keys();

        // get numBars
        numBars = keys.length;

        // return object
        return {
            barScale: barScale, 
            numBars: numBars,
            keys: keys,
        };
    }

    // prep data 
    function prepHorizonData(d) {
        
        var horizon = prepHorizonData.horizon; 
            shrinkage = function (x) {
            return x >= 0 ?  
                Math.floor( x / horizon) : 
                -shrinkage(-x);
        };

        // take the first layer, duplicate it, a
        // and replace the first duplicate with 
        // the "shrinkage"
        // TODO : causes horizon chart to ignore other
        // layers
        d = [d[0], jQuery.extend(true, {}, d[0])];
        d3.map(d[0].data).forEach(function(k, v) {
            d[0].data[k] = shrinkage(v);
            d[1].data[k] = Math.abs(v) > 1e-4 ? v : 0;
        });

        return d;
    }

    // construct the svg translate command by x and y
    function svgTranslate(x, y) {
        return 'translate(' + (+x) + ',' + (+y) + ')';
    }

    // construct the svg rotate command given angle a, 
    // rotation center (cx, cy)
    function svgRotate(a, cx, cy) {
        cx = cx || 0;
        cy = cy || 0;
        return 'rotate('+ (+a) + ',' + (+cx) + ',' + (+cy) + ')';
    }

    // function buildChart 
    function buildChart(container) {

        // pass in container that will hold the chart

        // parameter defaults
        var barHeight = buildChart.barHeight || 100;
        var margin = buildChart.margin || 
            {top: 20, right: 20, bottom: 20, left: 20};

        // build the svg container
        var chart_group = d3.select(container).append('svg') 
            // svg group has squarish drawing area
            .style('width', 2 * barHeight + margin.left + margin.right + 'px')
            .style('height', 2 * barHeight + margin.top + margin.bottom + 'px')
        .append('g') 
            // radial bar chart has the pen moved to the center
            // of the square drawing area
            .classed('radial-barchart', true)
            .attr('transform',  // move 
                svgTranslate(margin.left + barHeight, 
                margin.top + barHeight));

        return chart_group; // return the modified container
    }

    // drawLayers
    function drawLayers(chart_group, d) {

        // select
        var layers = chart_group.selectAll('g.layer')
            .data(d);

        // layers enter
        layers.enter().append('g')
            .attr('class', function(d, i) {
                return 'layer-' + i;
            })
            .classed('layer', true);

        // layers exit
        layers.exit().remove();

        // return layers from drawLayers namespace
        return layers;
    }

    // draw horizon type segements
    function drawHorizonSegments(layer, d, barScale) {
        // parameters
        var horizon = drawHorizonSegments.horizon || 100;
        var colors = drawHorizonSegments.colors;

        // outer radius wraps around on horizon
        var or = function(d, i) {
            return d < 0 || (d !== 0 && (d % horizon) === 0) ? 
                barScale(horizon) : 
                barScale(d % horizon);
        };

        // inner radius wraps around on horizon
        var ir = function(d) {
            return d >= 0 || (d !== 0 && (d % horizon) === 0) ? 
                0 : 
                barScale((d % horizon) + horizon);
        };

        var values = d3.map(d.data).values();
        var m = Math.floor(colors.length/2), 
            shrinkage = function (x) {
                return x >= 0 ?  
                    Math.floor( x / horizon) : 
                    -shrinkage(-x);
            },
            getcolor = function (x){
                var offset = (x % horizon) === 0 ? 
                    (x >= 0 ? 
                        x - 1 :  // if x is on the horizon positive
                        x ) :
                    Math.floor(x);
                return colors[offset + m];
            };

        drawSegmentsBuilder(layer,
            //values.map(shrinkage), 
            values,
            barScale, 
            or, 
            ir,
        getcolor);

    }

    // function drawSegments
    function drawSegmentsBuilder(layer, d, barScale, or, ir, colors) {

        var transitionDuration = 
            drawSegmentsBuilder.transitionDuration || 1000;

        var sa = function(d, i) { 
            return (i * 2 * Math.PI) / numBars; };
        var ea = function(d, i) { 
            return ((i + 1) * 2 * Math.PI) / numBars; };

        // select
        var segments = layer.selectAll('path')
            .data(d);

        // enter
        segments.enter().append('path');

        // exit
        // remove dangling segments
        segments.exit().remove();

        // arc drawing (with transition)
        segments.transition().duration(transitionDuration)
            .attr('d', d3.svg.arc() // tell d3 to draw arc
                .innerRadius(ir) // inner radius
                .outerRadius(or) // outer radius
                .startAngle(sa)  // start from this angle
                .endAngle(ea))  // arc until this angle
            .style('fill', function(d) {
                return colors(d);
            });

        // return segments 
        return segments;
    }

    // dont really seem to need this, makes for more lightweight code
    // new style getters/setters
    // (function () {
        //     var barHeight;
        //     Object.defineProperty(init, "barHeight", {
            //         get: function () { return barHeight; },
            //         set: function (value) { barHeight = value; }
    //     });
    // }());

    // function draw overlays
    // i.e. draw the grid lines etc,
    function drawOverlays(g, keys, numBars) {
        // pass in the chart group and data keys

        var tickCircleValues = drawOverlays.tickCircleValues;
        var barHeight = drawOverlays.barHeight || 100;

        // Spokes
        g.append('g')
            .classed('spokes', true)
            .selectAll('line')
            .data(keys)
        .enter().append('line')
            .attr('y2', -barHeight)
            .attr('transform', 
                function(d, i) {return svgRotate(i * 360 / numBars);}); 

        // Outer circle
        g.append('circle')
            .attr('r', barHeight)
            .classed('outer', true)
            .style('fill', 'none');

        // Concentric circles at specified tick values
        g.append('g')
            .classed('tick-circles', true)
            .selectAll('circle')
            .data(tickCircleValues)
        .enter().append('circle')
            .attr('r', function(d) {return barScale(d);})
            .style('fill', 'none');
    }

    // function draw labels
    function drawVerticalLabels(g, keys, numBars) {
        // pass in the chart g

        var barHeight = drawVerticalLabels.barHeight || 100;

        // Labels
        var labels = g.append('g')
            .classed('labels', true);

        // write text
        labels.selectAll('text').data(keys).enter().append('text')
            // .style('writing-mode', 'tb')
            .style('text-anchor', 'start')
            // .style('glyph-orientation-vertical', 0)
            // .style('letter-spacing', -3)
            .attr('transform', 
                function (d, i) {
                    return svgRotate(-90) + 
                        svgTranslate(barHeight+10,0) + 
                        svgRotate((i + 0.5) * 360 / numBars, -(barHeight+10), 0);
            })
            .text(function(d) {return d;});
    }

    // function chartBuilder
    function chartBuilder(init, 
        prepData,
        buildChart, 
        drawLayers,
        drawSegments,
        drawOverlays,
    drawLabels) {

        var chart = function(selection) {

            // call once for each selection
            selection.each(function(d) {

                // call init 
                var init_params = init(d);

                // call prep Data
                d = prepData(d);

                // call initChart
                var chart_g =d3.select(this).select('svg')
                    .select('g');
                    exists = chart_g[0][0] !== null;

                if (!exists)
                    chart_g = buildChart(this);

                // call drawLayers
                var layers = drawLayers(chart_g, d);

                // call drawSegments
                layers.each(function (layer, i) {
                    drawSegments(
                        chart_g.selectAll('g.layer-' + i),
                        d[i],
                    init_params.barScale);
                });

                if (!exists) {
                    // // call drawOverlays
                    drawOverlays(chart_g, 
                        init_params.keys, 
                    init_params.numBars);

                    // call drawLabels
                    drawLabels(chart_g,
                        init_params.keys, 
                    init_params.numBars);
                }

            });

        };

        // (chaining) setters 
        chart.barHeight = function(x) { 
            init.barHeight = x;
            buildChart.barHeight = x;
            drawOverlays.barHeight = x;
            drawVerticalLabels.barHeight = x;
            return chart;
        };

        chart.margin = function(x) { 
            buildChart.margin = x;
            return chart;
        };

        chart.colorscheme = function(x) { 
            // init.colors= x;
            drawHorizonSegments.colors= x;
            return chart;
        };

        chart.domain = function(x) { 
            init.domain= x;
            prepHorizonData.horizon = x[1];
            drawHorizonSegments.horizon = x[1];
            return chart;
        };

        chart.tickCircleValues= function(x) { 
            drawOverlays.tickCircleValues= x;
            return chart;
        };

        // return from the chartBuilder namespace
        return chart;
    }

    // reveal these charts from the radialBarChart namespace
    return {
        horizon: chartBuilder(init, prepHorizonData, buildChart, drawLayers, drawHorizonSegments, drawOverlays, drawVerticalLabels),
    };

}
