
$(document).ready(function() {
    var width = 1170;
    var height = 700;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(30)
        .size([width, height]);

    var svg = d3.select("#keyword_bubble").append("svg")
        .attr("width", width)
        .attr("height", height);

    d3.json("/static/moviedetail/data/bubble.json", function(error, graph) {
        if (error) throw error;

        force
            .nodes(graph.nodes)
            .links(graph.links)
            .start();

        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke-width", function(d) { return Math.sqrt(d.value); });

        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 10)
            .style("fill", function(d) { return color(d.group); })
            .call(force.drag);

        node.append("svg:title")
            .text(function(d) {
                var group = d.group
                if (group == 0) {
                    return d.title;
                } 
                 
            });

        var poster = d3.select("body").append("div").attr("class", "node-poster")
        node.on("mouseover", function(d) {
            var imdbid = d.imdbid
            var group = d.group
            if (group != 0) {
                poster.html("<img src='/static/images/posters/" + imdbid + ".jpg'>")
                  .style("left", (d3.event.pageX) + "px")
                  .style("top", (d3.event.pageY) + "px"); 
            } 
        });
        node.on("mouseout", function(d) {
            poster.html("");
        });
        node.on("click", function(d) {
            if (d.group != 0) {
                var url = "http://www.imdb.com/title/" + d.imdbid;
                window.open(url, '_blank');
            } else {
                var url = "https://en.wikipedia.org/w/index.php?curid=" + d.wikiid;
                window.open(url, '_blank');
            }
        });

        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        });
    });
});



