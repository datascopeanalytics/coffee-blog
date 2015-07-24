var radius = 65,
    padding = 5;
var i = 0;

var colormap = {"Carbony":'#000000',
                "Earthy":'#1D3B08',
                "Nutty":'#F29557',
                "Fruity":'#ED0021',
                "Flowery":'#DC9EE9',
                "Sugary":'#FFD3E1'};

var region_color = d3.scale.ordinal()
    .range(d3.values(colormap))
    .domain(d3.keys(colormap));

var regions = [{"region": "Caribbean", "words":["butterscotch", "smoky", "toast","nut", "cedar", "raisin", "orange", "apricot", "butter", "fir"]},
               {"region": "South America", "words":["caramel", "cocoa", "milk", "honeydew", "hazelnut", "walnut", "cherry", "licorice", "almond", "tamarind"]},
               {"region": "Asia_Indonesia", "words":["earth", "leaves", "grapefruit", "wood", "scorched", "tobacco", "malt", "papaya", "coconut", "banana"]},
               {"region": "Central America", "words":["pecan", "spice", "nectarine", "oak", "lily", "thyme", "whisky", "rye", "grapy", "pineapple"]},
               {"region": "Africa", "words":["currant", "blueberry", "berry", "honey", "floral", "lemon", "rose", "blackberry", "juicy", "brandy"]},
               {"region": "Hawaii", "words":["refreshing", "apple", "plum", "blossom", "tomato", "vanilla", "sugar", "lilac", "ripe", "mint"]}];

var arc = d3.svg.arc()
    .outerRadius(radius)
    .innerRadius(radius - 18);

var pie = d3.layout.pie()
    .sort(null)
    .value(function(d) { return d.population; });

d3.csv("region_donuts.csv", function(error, data) {
    data.forEach(function(d) {
        d.ages = region_color.domain().map(function(name) {
            return {name: name, population: +d[name]};
        });
    });

    var legend = d3.select("#region-container").append("svg")
        .attr("class", "legend")
        .attr("width", radius * 1.5)
        .attr("height", radius * 5)
        .style("font-size","13px")
        .selectAll("g")
        .data(d3.keys(colormap))
        .enter().append("g")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", region_color);

    legend.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .text(function(d) { return d; });

    var svg = d3.select("#region-container").selectAll(".pie")
        .data(data)
        .enter().append("svg")
        .attr("class", "pie")
        .attr("width", radius * 2)
        .attr("height", radius * 5)
        .append("g")
        .attr("transform", "translate(" + radius + "," + radius + ")");

    svg.selectAll(".arc")
        .data(function(d) { return pie(d.ages); })
        .enter().append("path")
        .attr("class", "arc")
        .attr("d", arc)
        .style("fill", function(d) { return region_color(d.data.name); });

    svg.append("text")
        .attr("dy", ".35em")
        .style("font-size","12px")
        .style("text-anchor", "middle")
        .text(function(d) { return d.Region; });

    svg.append("text")
        .attr("dy", "7.7em")
        .style("font-size","10px")
        .style("text-anchor", "middle")
        .text("Top 10 Words")
        .style("font-weight", "bold");

    for (var j = 0; j < 10; j++){
        i = 0;
        var y = 9.2 + j*1.4;
        svg.append("text")
            .style("font-size","10px")
            .attr("dy", y + "em")
        // .attr("dx", "-2.0em")
            .style("text-anchor", "middle")
            .text(function(d) {
                return regions[i++].words[j];})
    }

});
