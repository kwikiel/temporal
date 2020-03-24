



fetch('window.location.href'+'/json').then(res=>res.json()).then(res=>{

    let data1 = []; 
        res.forEach(element => {
            
            data1.push((element.mid))
        });
    
      
        // options
        var margin = {"top": 20, "right": 10, "bottom": 10, "left": 30 }
        var width = 500;
        var height = 1000;
        var rectWidth = 90;
        
        // data
        var data = data1;
        
        // scales
        var xMax = 5 * rectWidth;
        var xScale = d3.scaleLinear()
            .domain([0, xMax])
            .range([margin.left, width - margin.right]);
        var yMax = d3.max(data, function(d){return d});
        var yScale = d3.scaleLinear()
            .domain([0, yMax])
            .range([height - margin.bottom, margin.top]);
         
        // svg element
        var svg = d3.select('svg');
            
        // bars 
        var rect = svg.selectAll('rect')
            .data(data)
            .enter().append('rect')
            .attr('x', function(d, i){ 
            return xScale(i * rectWidth)})
            .attr('y', function(d){
            return yScale(d)})
            .attr('width', xScale(rectWidth) - margin.left)
            .attr('height', function(d){
            return height - margin.bottom - yScale(d)})
                .attr('fill', function(d){
            return "red"})
            .attr('margin', 0);
        
        // axes
        var xAxis = d3.axisBottom()
            .scale(xScale)
            .tickFormat(d3.format('d'));
        var yAxis = d3.axisLeft()
            .scale(yScale)
            .tickFormat(d3.format('d'));
        
        svg.append('g')
              .attr('transform', 'translate(' + [0, height - margin.bottom] + ')')
              .call(xAxis);
          svg.append('g')
              .attr('transform', 'translate(' + [margin.left, 0] + ')')
              .call(yAxis);
            
    })
    
    
    
    
    
    