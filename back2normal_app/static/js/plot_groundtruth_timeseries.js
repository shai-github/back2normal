/*
Code adapted from @imdineshrewal
https://codepen.io/imdineshgrewal/pen/MNvPXv?editors=1111
 */

var data_gt = gt_records

// set the dimensions and margins of the graph
var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 860 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg_gt = d3
    .select("#groundTruth")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg4_gt = svg_gt
    .append("svg")
    .attr("id", "cvg_svgC4_gt")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g");
// .attr("transform", "translate(" + +")");

// -------------------------------Data manipulation--------
// const parse = d3.timeParse("%Y-%m-%d");

const parse_gt = d3.timeParse("%Y-%m-%d %H:%M:%S")

//rename columns of data 4
data_gt = data_gt.map((datum) =>{
    datum.date = parse_gt(datum.STD_DATE);
    datum.value1 = datum.AVG7DAY_RESTAURANT
    datum.value2 = datum.AVG7DAY_BARS
    datum.value3 = datum.AVG7DAY_GROCERY
    datum.value4 = datum.AVG7DAY_PARKS_BEACHES
    datum.value5 = datum.AVG7DAY_SCHOOLS_LIBRARIES

    return datum
})

//filter out NaNs
function filterNaNs(dataset) {
    var filtered_data = [];
    for (x in dataset) {
        if ((dataset[x].value1 == dataset[x].value1)
            && (dataset[x].value2 == dataset[x].value2)
            && (dataset[x].value3 == dataset[x].value3)
            && (dataset[x].value4 == dataset[x].value4)
            && (dataset[x].value5 == dataset[x].value5)) {
            filtered_data.push(dataset[x]);
        }
    }
    return filtered_data
}

data_gt = filterNaNs(data_gt)

//filter on zip function
function filterOnZip(selected_ZIP) {
    var filtered_data = [];
    for (x in data_gt) {
        if (data_gt[x].ZIPCODE == selected_ZIP) {
            filtered_data.push(data_gt[x]);
        }
    }
    return filtered_data
}


// -------------------------------Data manipulation ends--------
// Add X axis --> it is a date format
var xAxisScale_gt = d3
    .scaleTime()
    .domain(
        d3.extent(data_gt, function (d) {
            return d.date;
        })
    )
    .range([0, width]);

svg_gt
    .append("g")
    .attr("class", "myXaxis_gt")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xAxisScale_gt));

// Add Y axis
var yAxisScale_gt = d3
    .scaleLinear()
    .domain([
        0, 200
        // d3.max(data_gt, function (d) {
        //     return Math.max(d.value, d.value2);
        // })
    ])
    .range([height, 0]);

svg_gt.append("g").call(d3.axisLeft(yAxisScale_gt));

svg_gt.append("rect").attr("x", width - 200).attr('y', 0).attr('width', 225).attr('height', 90).attr('stroke', 'black').attr("stroke-width", 0.5).attr('fill', 'white')
svg_gt.append("circle").attr("cx",width-185).attr("cy",15).attr("r", 6).style("fill", "#ffd571");
svg_gt.append("circle").attr("cx",width-185).attr("cy",30).attr("r", 6).style("fill", "#bbd196");
svg_gt.append("circle").attr("cx",width-185).attr("cy",45).attr("r", 6).style("fill", "#56556e");
svg_gt.append("circle").attr("cx",width-185).attr("cy",60).attr("r", 6).style("fill", "#a35d6a");
svg_gt.append("circle").attr("cx",width-185).attr("cy",75).attr("r", 6).style("fill", "#51c2d5");
svg_gt.append("text").attr("x", width-175).attr("y", 15).text("Restaurants").style("font-size", "15px").attr("alignment-baseline","middle");
svg_gt.append("text").attr("x", width-175).attr("y", 30).text("Bars").style("font-size", "15px").attr("alignment-baseline","middle");
svg_gt.append("text").attr("x", width-175).attr("y", 45).text("Grocery").style("font-size", "15px").attr("alignment-baseline","middle");
svg_gt.append("text").attr("x", width-175).attr("y", 60).text("Parks and Beaches").style("font-size", "15px").attr("alignment-baseline","middle");
svg_gt.append("text").attr("x", width-175).attr("y", 75).text("Schools and Libraries").style("font-size", "15px").attr("alignment-baseline","middle");


function scatter_gt(selected_ZIP) {

    d3.select("#cvg_svgC4_gt").selectAll("path").remove();

    subset_data = filterOnZip(selected_ZIP)

    svg4_gt
        .append("path")
        .datum(subset_data)
        .attr("fill", "none")
        .attr("stroke", "none")
        .attr("stroke-width", 3)
        .attr(
            "d",
            d3
                .line()
                .x(function (d) {
                    return xAxisScale_gt(d.date);
                })
                .y(function (d) {
                    return yAxisScale_gt(d.value1);
                })
        )
        .style("stroke", "#ffd571");

    svg4_gt
        .append("path")
        .datum(subset_data)
        .attr("fill", "none")
        .attr("stroke", "none")
        .attr("stroke-width", 3)
        .attr(
            "d",
            d3
                .line()
                .x(function (d) {
                    return xAxisScale_gt(d.date);
                })
                .y(function (d) {
                    return yAxisScale_gt(d.value2);
                })
        )
        .style("stroke", "#bbd196");

    svg4_gt
        .append("path")
        .datum(subset_data)
        .attr("fill", "none")
        .attr("stroke", "none")
        .attr("stroke-width", 3)
        .attr(
            "d",
            d3
                .line()
                .x(function (d) {
                    return xAxisScale_gt(d.date);
                })
                .y(function (d) {
                    return yAxisScale_gt(d.value3);
                })
        )
        .style("stroke", "#56556e");

    svg4_gt
        .append("path")
        .datum(subset_data)
        .attr("fill", "none")
        .attr("stroke", "none")
        .attr("stroke-width", 3)
        .attr(
            "d",
            d3
                .line()
                .x(function (d) {
                    return xAxisScale_gt(d.date);
                })
                .y(function (d) {
                    return yAxisScale_gt(d.value4);
                })
        )
        .style("stroke", "#a35d6a");

    svg4_gt
        .append("path")
        .datum(subset_data)
        .attr("fill", "none")
        .attr("stroke", "none")
        .attr("stroke-width", 3)
        .attr(
            "d",
            d3
                .line()
                .x(function (d) {
                    return xAxisScale_gt(d.date);
                })
                .y(function (d) {
                    return yAxisScale_gt(d.value5);
                })
        )
        .style("stroke", "#51c2d5");

    svg4_gt
        .select(".myXaxis_gt")
        .transition()
        .duration(800)
        .attr("opacity", "1")
        .call(d3.axisBottom(xAxisScale_gt));

}
