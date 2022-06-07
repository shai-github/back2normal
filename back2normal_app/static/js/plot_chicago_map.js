/*
Code adapted from Mike Bostock, D3 + Leaflet
https://bost.ocks.org/mike/leaflet/
* */

d3.json("static/Boundaries - ZIP Codes.geojson", function (error, collection) {
    if (error) throw error;

    var map = new L.Map("map", {center: [41.83813, -87.72998], zoom: 11})
        .addLayer(new L.TileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"));

    // turn off map zoom
    map.touchZoom.disable();
    map.doubleClickZoom.disable();
    map.scrollWheelZoom.disable();
    map.boxZoom.disable();
    map.keyboard.disable();
    // map.removeControl(map.zoomControl);

    var svg = d3.select(map.getPanes().overlayPane).append("svg"),
        g = svg.append("g").attr("class", "leaflet-zoom-hide");

    var labels = svg.append("svg:g")
        .attr("id", "labels")
        .attr("class", "Title");

    var transform = d3.geo.transform({point: projectPoint}),
        path = d3.geo.path().projection(transform);

    var feature = g.selectAll("path")
        .data(collection.features)
        .enter().append("path");

    map.on("viewreset", reset);
    reset();

    // Reposition the SVG to cover the features.
    function reset() {
        var bounds = path.bounds(collection),
            topLeft = bounds[0],
            bottomRight = bounds[1];

        svg.attr("width", bottomRight[0] - topLeft[0])
            .attr("height", bottomRight[1] - topLeft[1])
            .style("left", topLeft[0] + "px")
            .style("top", topLeft[1] + "px");

        g.attr("transform", "translate(" + -topLeft[0] + "," + -topLeft[1] + ")");

        feature.attr("d", path);
    }

    var clickChart = d3.selectAll("path").on("click", function (e) {

        document.getElementById("rightzip").innerHTML = "ZIP Code: " + e.properties.zip;
        document.getElementById("righttitle").innerHTML = neighborhood_lookup[e.properties.zip];
        document.getElementById("rightdash").style.display = "block";
        document.getElementById("rightdash").style.overflowY = "scroll";
        document.getElementById("rightabout").style.display = "none";
        updatePieChart(e.properties.zip)
        updateBarChart(e.properties.zip)
        scatter(e.properties.zip)
        scatter_gt(e.properties.zip)
    })

    // Use Leaflet to implement a D3 geometric transformation.
    function projectPoint(x, y) {
        var point = map.latLngToLayerPoint(new L.LatLng(y, x));
        this.stream.point(point.x, point.y);
    }

});