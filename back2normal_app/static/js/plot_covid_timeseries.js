/*
Code adapted from @imdineshrewal
https://codepen.io/imdineshgrewal/pen/MNvPXv?editors=1111
 */

var data4 = covid_case_vacc_data

// set the dimensions and margins of the graph
var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 860 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3
    .select("#dynamic_series")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg4 = svg
    .append("svg")
    .attr("id", "cvg_svgC4")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g");
// .attr("transform", "translate(" + +")");

// -------------------------------Data manipulation--------
// const parse = d3.timeParse("%Y-%m-%d");

const parse4 = d3.timeParse("%Y-%m-%d %H:%M:%S")

//rename columns of data 4
data4 = data4.map((datum) =>{
    datum.date = parse4(datum.STD_DATE);
    datum.covid_val1 = datum.AVG7DAY_total_doses_daily
    datum.covid_val2 = datum.AVG7DAY_confirmed_cases_change
    return datum
})

//filter out NaNs
function filterNaNs(dataset) {
    var filtered_data = [];
    for (x in dataset) {
        if ((dataset[x].covid_val1 == dataset[x].covid_val1)
            && (dataset[x].covid_val2 == dataset[x].covid_val2)) {
            filtered_data.push(dataset[x]);
        }
    }
    return filtered_data
}

data4 = filterNaNs(data4)

//filter on zip function
function filterOnZipCovid(selected_ZIP) {
    var filtered_data = [];
    for (x in data4) {
        if (data4[x].ZIPCODE == selected_ZIP) {
            filtered_data.push(data4[x]);
        }
    }
    return filtered_data
}


// -------------------------------Data manipulation ends--------
// Add X axis --> it is a date format
var xAxisScale = d3
    .scaleTime()
    .domain(
        d3.extent(data4, function (d) {
            return d.date;
        })
    )
    .range([0, width]);

svg
    .append("g")
    .attr("class", "myXaxis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xAxisScale));

// Add Y axis
var yAxisScale = d3
    .scaleLinear()
    .domain([
        0, 600
    ])
    .range([height, 0]);

yAxis = svg.append("g").call(d3.axisLeft(yAxisScale));


svg.append("rect").attr("x", width-200).attr('y', 0).attr('width', 225).attr('height', 45).attr('stroke', 'black').attr("stroke-width", 0.5).attr('fill', 'white')
svg.append("circle").attr("cx",width-185).attr("cy",15).attr("r", 6).style("fill", "#588c7e");
svg.append("circle").attr("cx",width-185).attr("cy",30).attr("r", 6).style("fill", "#d96459");
svg.append("text").attr("x", width-175).attr("y", 15).text("Vaccinations").style("font-size", "15px").attr("alignment-baseline","middle");
svg.append("text").attr("x",width-175).attr("y", 30).text("Covid Cases").style("font-size", "15px").attr("alignment-baseline","middle");



function scatter(selected_ZIP) {

    d3.select("#cvg_svgC4").selectAll("path").remove();
    covid_subset_data = filterOnZipCovid(selected_ZIP)

    yAxis.remove()

    var yAxisScale = d3
        .scaleLinear()
        .domain([
            0,
            d3.max(covid_subset_data, function (ds) {
                return Math.max(ds.covid_val1, ds.covid_val2);
            })
        ])
        .range([height, 0]);

    yAxis = svg.append("g").call(d3.axisLeft(yAxisScale));


    svg4
        .append("path")
        .datum(covid_subset_data) //replaced data3 with data4
        .attr("fill", "none")
        .attr("stroke", "none")
        .attr("stroke-width", 3)
        .attr(
            "d",
            d3
                .line()
                .x(function (d) {
                    return xAxisScale(d.date);
                })
                .y(function (d) {
                    return yAxisScale(d.covid_val1);
                })
        )
        .style("stroke", "#588c7e");

    svg4
        .append("path")
        .datum(covid_subset_data)
        .attr("fill", "none")
        .attr("stroke", "none")
        .attr("stroke-width", 3)
        .attr(
            "d",
            d3
                .line()
                .x(function (d) {
                    return xAxisScale(d.date);
                })
                .y(function (d) {
                    return yAxisScale(d.covid_val2);
                })
        )
        .style("stroke", "#d96459");

    svg4
        .select(".myXaxis")
        .transition()
        .duration(800)
        .attr("opacity", "1")
        .call(d3.axisBottom(xAxisScale));

}
