var radius = 65,
padding = 5,
i = 0;

var color = d3.scale.ordinal()
.range(['#ffc0cb','#f9986c','#e07339','#c25018','#a32b05','#800000']);

var roasts = [{"roast": "Dark", "words":["scorched","astringent","banana", "wood", "smoky","earth", "caramel","bittersweet","molasses","spice"]},
{"roast": "Medium-Dark", "words":["raisin","cedar","milk","earthiness", "butter", "nut", "grapefruit", "prune","fudgy","cream"]},
{"roast": "Medium", "words":["current","lemon","fir", "cocoa","cherry", "apricot", "blackberry", "lime", "butterscotch",  "pine"]},
{"roast": "Medium-Light", "words":["peach","floral","almond","orange","lily","pecan","plum","sandalwood", "thyme","kumquat" ]},
{"roast": "Light", "words":["nectarine", "rye", "honeysuckle","tangerine", "strawberry", "cacao", "grape", "whisky", "honey", "blueberry"]}];

var arc = d3.svg.arc()
.outerRadius(radius)
.innerRadius(radius - 18);

var pie = d3.layout.pie()
.sort(null)
.value(function(d) { return d.population; });

d3.csv("roast_pies.csv", function(error, data) {
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Roast"; }));

  data.forEach(function(d) {
    d.ages = color.domain().map(function(name) {
      return {name: name, population: +d[name]};
    });
  });

  var legend = d3.select("#roast_container").append("svg")
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

  var svg = d3.select("#roast_container").selectAll(".pie")
  .data(data)
  .enter().append("svg")
  .attr("class", "pie")
  .attr("width", radius * 2)
  .attr("height", radius * 5)
  .append("g")
  .attr("transform", "translate(" + radius + "," + radius + ")");

  svg.selectAll(".arc")
  .data(function(d) {
    return pie(d.ages); })
  .enter().append("path")
  .attr("class", "arc")
  .attr("d", arc)
  .style("fill", function(d) {
    return color(d.data.name); });

  svg.selectAll(".arc").append("title").text(function(d) {
    return ((d.data.population/10)*100 + "% " + d.data.name); });

  svg.append("text")
  .attr("dy", ".35em")
  .style("font-size","12px")
  .style("text-anchor", "middle")
  .text(function(d) { return d.Roast; });

  svg.append("text")
  .attr("dy", "7.7em")
  .style("font-size","10px")
  .style("text-anchor", "middle")
  .text("Top 10 Descriptors")
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
      return roasts[i++].words[j];})
    }

  });
