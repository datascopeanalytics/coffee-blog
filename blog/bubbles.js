var diameter = 475;
var format = d3.format(",d");
var bubblecolor = d3.scale.ordinal().range(['#ffa500','#d77306','#ae3e12','#800000']);

var bubble = d3.layout.pack()
.sort(null)
.size([diameter, diameter])
.padding(1.5);

var svg = d3.select("#bubbles").append("svg")
.attr("width", diameter)
.attr("height", diameter)
.attr("class", "bubble");

// d3.json("flare.json", function(error, root) {
d3.json("top_50_words.json", function(error, root) {
  var node = svg.selectAll(".node")
  .data(bubble.nodes(classes(root))
  .filter(function(d) { return !d.children; }))
      .enter().append("g")
  .attr("class", "node")
  .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  node.append("title")
  .text(function(d) { return d.className + ": " + format(d.value); });

  node.append("circle")
  .attr("r", function(d) { return d.r; })
  .style("fill", function(d) { return bubblecolor(d.packageName); });

  node.append("text")
  .attr("dy", ".3em")
  .style("text-anchor", "middle")
  .text(function(d) { return d.className.substring(0, d.r / 3); });
});

// Returns a flattened hierarchy containing all leaf nodes under the root.
function classes(root) {
  var classes = [];

  function recurse(name, node) {
    if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
    else classes.push({packageName: name, className: node.name, value: node.size});
  }

  recurse(null, root);
  return {children: classes};
}

d3.select(self.frameElement).style("height", diameter + "px");
