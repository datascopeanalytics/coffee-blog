var radius = 65,
padding = 5,
i = 0;

var color = d3.scale.ordinal()
.range(['#ffc0cb','#f49c62','#da7732','#be5415','#a12f04','#800000']);

var regions = [{"region": "Caribbean", "words":["butterscotch", "smoky", "toast","nut", "cedar", "raisin", "orange", "apricot", "butter", "fir"]},
{"region": "South America", "words":["caramel", "cocoa", "milk", "honeydew", "hazelnut", "walnut", "cherry", "licorice", "almond", "tamarind"]},
{"region": "Asia_Indonesia", "words":["earth", "leaves", "grapefruit", "wood", "scorched", "tobacco", "malt", "papaya", "coconut", "banana"]},
{"region": "Central America", "words":["pecan", "spice", "nectarine", "oak", "lily", "thyme", "whisky", "rye", "grapy", "pineapple"]},
{"region": "Africa", "words":["currant", "blueberry", "berry", "honey", "floral", "lemon", "rose", "blackberry", "brandy", "lavendar"]},
{"region": "Hawaii", "words":["refreshing", "apple", "plum", "blossom", "tomato", "astringent", "vanilla", "sugar", "lilac", "mint"]}];

var arc = d3.svg.arc()
.outerRadius(radius)
.innerRadius(radius - 18);

var pie = d3.layout.pie()
.sort(null)
.value(function(d) { return d.population; });

d3.csv("region_pies.csv", function(error, data) {
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Region"; }));

  data.forEach(function(d) {
    d.ages = color.domain().map(function(name) {
      return {name: name, population: +d[name]};
    });
  });

  var legend = d3.select("#region_container").append("svg")
  .attr("class", "legend")
  .attr("width", radius * 1.5)
  .attr("height", radius * 5)
  .style("font-size","13px")
  .selectAll("g")
  .data(color.domain().slice().reverse())
  .enter().append("g")
  .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
  .attr("width", 18)
  .attr("height", 18)
  .style("fill", color);

  legend.append("text")
  .attr("x", 24)
  .attr("y", 9)
  .attr("dy", ".35em")
  .text(function(d) { return d; });

  var svg = d3.select("#region_container").selectAll(".pie")
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
  .style("fill", function(d) { return color(d.data.name); });

  svg.selectAll(".arc").append("title").text(function(d) {
    return ((d.data.population/10)*100 + "% " + d.data.name); });

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
    .style("text-anchor", "middle")
    .text(function(d) {
      return regions[i++].words[j];})
    }

  });
