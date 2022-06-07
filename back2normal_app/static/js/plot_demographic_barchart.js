/*
Code adapted from
diethardsteiner Block 3287802
http://bl.ocks.org/diethardsteiner/3287802
*/

var label_lookup = {
    "unemploy_rate": "Unemployed",
    "pct_below_poverty_lvl": "In poverty",
    "pct_65_or_older": "Age >= 65",
    "pct_w_health_insur": "w/ health insurance"
}

var formatAsPercentage = d3.format("%"),
    formatAsPercentage1Dec = d3.format(".1%"),
    formatAsInteger = d3.format(","),
    fsec = d3.time.format("%S s"),
    fmin = d3.time.format("%M m"),
    fhou = d3.time.format("%H h"),
    fwee = d3.time.format("%a"),
    fdat = d3.time.format("%d d"),
    fmon = d3.time.format("%b")
;

var datasetBarChart = demographic_data
;

var group = "60637";

function datasetBarChosen(group) {
    var ds = [];
    for (x in datasetBarChart) {

        if (datasetBarChart[x].ZIPCODE == group) {
            if (['unemploy_rate', 'pct_below_poverty_lvl', 'pct_65_or_older', 'pct_w_health_insur'].includes(datasetBarChart[x].CATEGORY)) {
                ds.push(datasetBarChart[x]);
            }
        }
    }
    return ds;
}

function dsBarChartBasics() {

    var margin = {top: 30, right: 5, bottom: 20, left: 50},
        width = 520 - margin.left - margin.right,
        height = 375 - margin.top - margin.bottom,
        colorBar = d3.scale.category20(),
        barPadding = 1
    ;

    return {
        margin: margin,
        width: width,
        height: height,
        colorBar: colorBar,
        barPadding: barPadding
    }
        ;
}

function dsBarChart() {

    var firstDatasetBarChart = datasetBarChosen(group);

    var basics = dsBarChartBasics();

    var margin = basics.margin,
        width = basics.width,
        height = basics.height,
        colorBar = basics.colorBar,
        barPadding = basics.barPadding
    ;

    var xScale = d3.scale.linear()
        .domain([0, firstDatasetBarChart.length])
        .range([0, width])
    ;

    // Create linear y scale
    // Purpose: No matter what the data is, the bar should fit into the svg area; bars should not
    // get higher than the svg height. Hence incoming data needs to be scaled to fit into the svg area.
    var yScale = d3.scale.linear()
        // use the max funtion to derive end point of the domain (max value of the dataset)
        // do not use the min value of the dataset as min of the domain as otherwise you will not see the first bar
            .domain([0, d3.max(firstDatasetBarChart, function (d) {
                return d.VALUE;
            })])
            // As coordinates are always defined from the top left corner, the y position of the bar
            // is the svg height minus the data value. So you basically draw the bar starting from the top.
            // To have the y position calculated by the range function
            .range([height, 0])
    ;

    //Create SVG element

    var svg = d3.select("#barChart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id", "barChartPlot")
    ;

    var plot = svg
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    ;

    plot.selectAll("rect")
        .data(firstDatasetBarChart)
        .enter()
        .append("rect")
        .attr("x", function (d, i) {
            return xScale(i);
        })
        .attr("width", width / firstDatasetBarChart.length - barPadding)
        .attr("y", function (d) {
            return yScale(d.VALUE);
        })
        .attr("height", function (d) {
            return height - yScale(d.VALUE);
        })
        .attr("fill", "lightgrey")
    ;


    // Add y labels to plot

    plot.selectAll("text")
        .data(firstDatasetBarChart)
        .enter()
        .append("text")
        .text(function (d) {
            return formatAsPercentage1Dec(d.VALUE / 100);
        })
        .attr("text-anchor", "middle")
        // Set x position to the left edge of each bar plus half the bar width
        .attr("x", function (d, i) {
            return (i * (width / firstDatasetBarChart.length)) + ((width / firstDatasetBarChart.length - barPadding) / 2);
        })
        .attr("y", function (d) {
            return yScale(d.VALUE) + 14;
        })
        .attr("class", "yAxis")
    ;

    // Add x labels to chart

    var xLabels = svg
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + (margin.top + height) + ")")
    ;

    xLabels.selectAll("text.xAxis")
        .data(firstDatasetBarChart)
        .enter()
        .append("text")
        .text(function (d) {
            return label_lookup[d.CATEGORY];
        })
        .attr("text-anchor", "middle")
        // Set x position to the left edge of each bar plus half the bar width
        .attr("x", function (d, i) {
            return (i * (width / firstDatasetBarChart.length)) + ((width / firstDatasetBarChart.length - barPadding) / 2);
        })
        .attr("y", 15)
        .attr("class", "xAxis")
    //.attr("style", "font-size: 12; font-family: Helvetica, sans-serif")
    ;

}

dsBarChart();

function updateBarChart(group) {

    var currentDatasetBarChart = datasetBarChosen(group);

    var basics = dsBarChartBasics();

    var margin = basics.margin,
        width = basics.width,
        height = basics.height,
        barPadding = basics.barPadding
    ;

    var color = d3.scaleOrdinal()
        .domain(currentDatasetBarChart)
        .range(d3.schemeSet3);

    var xScale = d3.scale.linear()
        .domain([0, currentDatasetBarChart.length])
        .range([0, width])
    ;


    var yScale = d3.scale.linear()
        .domain([0, d3.max(currentDatasetBarChart, function (d) {
            return d.VALUE;
        })])
        .range([height, 0])
    ;

    var svg = d3.select("#barChart svg");

    var plot = d3.select("#barChartPlot")
        .datum(currentDatasetBarChart)
    ;

    /* Note that here we only have to select the elements - no more appending! */
    plot.selectAll("rect")
        .data(currentDatasetBarChart)
        .transition()
        .duration(750)
        .attr("x", function (d, i) {
            return xScale(i);
        })
        .attr("width", width / currentDatasetBarChart.length - barPadding)
        .attr("y", function (d) {
            return yScale(d.VALUE);
        })
        .attr("height", function (d) {
            return height - yScale(d.VALUE);
        })
        .attr("fill", function(d,i){return color(i)})
    ;

    plot.selectAll("text.yAxis") // target the text element(s) which has a yAxis class defined
        .data(currentDatasetBarChart)
        .transition()
        .duration(750)
        .attr("text-anchor", "middle")
        .attr("x", function (d, i) {
            return (i * (width / currentDatasetBarChart.length)) + ((width / currentDatasetBarChart.length - barPadding) / 2);
        })
        .attr("y", function (d) {
            return yScale(d.VALUE) + 14;
        })
        .text(function (d) {
            return formatAsPercentage1Dec(d.VALUE / 100);
        })
        .attr("class", "yAxis")
    ;

    // svg.selectAll("text.chart_title") // target the text element(s) which has a title class defined
    //     .attr("x", (width + margin.left + margin.right) / 2)
    //     .attr("y", 15)
    //     .attr("class", "chart_title")
    //     .attr("text-anchor", "middle")
    //     .text("Demographic Data")
    // ;
}
