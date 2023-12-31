d3.json('http://135.181.84.87:8181/customers?page=10&size=14000')
  .then(function(data) {
    const resultData = data.result; // Get data from the "result" key
    console.log(resultData); // Check your data from the "result" key

    // Aggregate data to calculate average price, power, and count of clients per brand
    const aggregatedData = Array.from((d3.group(resultData, d => d.car.brand)), ([key, values]) => {
        return {
          brand: key,
          avgPrice: d3.mean(values, d => d.car.price),
          avgPower: d3.mean(values, d => d.car.power),
          countClients: values.length
        };
      });
    console.log(aggregatedData); // Check the aggregated data

//1. Bubble-chart Power-Price
// Define the SVG dimensions
const margin = { top: 30, right: 110, bottom: 40, left: 50 };
const width = 620 - margin.left - margin.right;
const height = 350 - margin.top - margin.bottom;

// Append an SVG element to the body
const svg = d3.select("#bubble-chart")
  .append("svg")
  .attr('width', width + margin.left + margin.right)
  .attr('height', height + margin.top + margin.bottom)
  .append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);

// Define scales for price and power
const priceScale = d3.scaleLinear()
  .domain([0, d3.max(aggregatedData, d => d.avgPrice)+0.1*d3.max(aggregatedData, d => d.avgPrice)]) 
  .range([0, width]);

const powerScale = d3.scaleLinear()
  .domain([0, d3.max(aggregatedData, d => d.avgPower)+0.1*d3.max(aggregatedData, d => d.avgPower)])
  .range([height, 0]);

const bubbleSizeScale = d3.scaleLinear()
  .domain([0, d3.max(aggregatedData, d => d.countClients)])
  .range([5, 30]);

// Filter out unique brands
const uniqueBrands = [...new Set(resultData.map(d => d.car.brand))];
console.log(uniqueBrands);

const BrandsColorScale = d3.scaleOrdinal()
    .domain(uniqueBrands)
    .range(['#F5C63C','#F47F6B','#BB5098','#7A5197','#5344A9','#148B64','#7BBE82','#F1EAAF','#F7D2C7','#74BEEA',
            '#1F4486','#A4C557','#BE324F','#77B2BD','#B0B0D7','#CA8F98','#8B6E7F','#EEF36A','#FF1654','#2EC4B6']);

// Create circles representing cars on the SVG
svg.selectAll("circle")
  .data(aggregatedData)
  .enter()
  .append("circle")
  .attr("cx", d => priceScale(d.avgPrice))
  .attr("cy", d => powerScale(d.avgPower))
  .attr("r", d => bubbleSizeScale(d.countClients))
  .attr("fill", d => BrandsColorScale(d.brand))
  .on('mouseover', (event, d) => {
        d3.select(event.currentTarget)
        .transition()
        .duration(200)
        .style('opacity', 0.5)
        // Set tooltip content and position
        bubbleTooltip.html(`<strong>${d.brand}</strong><br/>Average price: ${d.avgPrice.toFixed(2)} euro <br/>Average power: ${d.avgPower.toFixed(2)} horse-power <br/>Number of Clients: ${d.countClients}`)
        bubbleTooltip.transition().duration(200).style('opacity', 0.9)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 20) + "px");
    })
    .on('mousemove', (event) => {
        bubbleTooltip.style("transform","translateY(-55%)")
          .style('left',(event.pageX + 10)+'px')
          .style('top',(event.pageY - 30)+'px');
      })
      .on('mouseleave', () => {
        d3.select(event.currentTarget).style('opacity', 1)
        bubbleTooltip.transition().style('opacity', 0);
      });

    // Create a tooltip
    const bubbleTooltip = d3.select('#bubble-chart')
    .append('div')
    .attr('class', 'tooltip')
    .style('opacity', 0)
    .attr('class', 'tooltip')
    .style('position', 'absolute')
    .style('background-color', 'white')
    .style('border', 'solid')
    .style('border-width', '1px')
    .style('border-radius', '5px')
    .style('padding', '10px');

// Create X and Y axes
const xAxis = d3.axisBottom(priceScale);
const yAxis = d3.axisLeft(powerScale);

// Append X axis to the SVG
svg.append("g")
  .attr("class", "x-axis")
  .attr("transform", `translate(0, ${height})`)
  .call(xAxis);

// Add X axis label
svg.append("text")
  .attr("x", width/2)
  .attr("y", height+0.9*margin.bottom)
  .style("text-anchor", "middle")
  .text("Average price (euro)");

// Append Y axis to the SVG
svg.append("g")
  .attr("class", "y-axis")
  .call(yAxis);

// Add Y axis label
svg.append("text")
  .attr("transform", "rotate(-90)")
  .attr("x", -height/2)
  .attr("y", -1.3*margin.top)
  .style("text-anchor", "middle")
  .text("Average power (hp)");

// Create legend
const legend = svg.append("g")
  .attr("class", "legend")
  .attr("transform", `translate(${width+0.5*margin.top},${-margin.top})`);

legend.selectAll("rect")
  .data(uniqueBrands)
  .enter()
  .append("rect")
  .attr("x", 0)
  .attr("y", (d, i) => i * 20)
  .attr("width", 10)
  .attr("height", 10)
  .attr("fill", d => BrandsColorScale(d));

legend.selectAll("text")
  .data(uniqueBrands)
  .enter()
  .append("text")
  .style("font-size", "12px")
  .attr("x", 15)
  .attr("y", (d, i) => i * 20 + 10)
  .text(d => d);

//2. Stack-Bar Chart Brand-Sexe
// Transform data into a format suitable for the chart (count of cars by brand and gender)
const brandCounts = resultData.reduce((accumulator,entry) => {
    const brand = entry.car.brand;
    const gender = entry.gender;
    // Initialize brand if not present in the accumulator
    if (!accumulator[brand]) {
        accumulator[brand] = {
          brand: brand,
          Female: 0,
          Male: 0
        };
      }
      // Increment gender count for the brand
      if (gender === 'F') {
        accumulator[brand].Female++;
      } else if (gender === 'M') {
        accumulator[brand].Male++;
      }    
      return accumulator;
  }, {});

  const stackedData = Object.values(brandCounts);
  console.log(stackedData);

// Define SVG dimensions and margins
    const stackedBarMargin = { top: 30, right: 30, bottom: 30, left: 50 };
    const stackedBarWidth = 1410 - stackedBarMargin.left - stackedBarMargin.right;
    const stackedBarHeight = 350 - stackedBarMargin.top - stackedBarMargin.bottom;

    // Append SVG to chart-container
    const svg2 = d3.select("#chart-container")
      .append("svg")
      .attr("width", stackedBarWidth + stackedBarMargin.left + stackedBarMargin.right)
      .attr("height", stackedBarHeight + stackedBarMargin.top + stackedBarMargin.bottom)
      .append("g")
      .attr("transform", `translate(${stackedBarMargin.left},${stackedBarMargin.top})`);

    // Define color scale
    const color = d3.scaleOrdinal()
      .domain(["Male", "Female"])
      .range(["#0072BC", "#EF4A60"]);

    // Define X and Y scales
    const x = d3.scaleBand()
      .domain(stackedData.map(d => d.brand))
      .range([0, stackedBarWidth])
      .padding(0.1);

    const y = d3.scaleLinear()
        .domain([0, d3.max(stackedData, d => d.Male + d.Female) - 0.25 * (d3.max(stackedData, d => d.Male + d.Female))])
        .nice()
        .range([stackedBarHeight, 0]);

    // Create stacked bars
    svg2.selectAll("g")
      .data(stackedData)
      .enter().append("g")
      .attr("transform", d => `translate(${x(d.brand)},0)`)
      .selectAll("rect")
      // display the data on the bars (female, male) one on top of the other.
      .data(d => [{ gender: "Male", value: d.Male }, { gender: "Female", value: d.Female }])
      .enter().append("rect")
      .attr("x", d => x.bandwidth() / 4)
      .attr("y", d => y(d.value))
      .attr("width", x.bandwidth() / 2)
      .attr("height", d => stackedBarHeight - y(d.value))
      .attr("fill", d => color(d.gender))
      .on('mouseover', (event, d) => {
        d3.select(event.currentTarget)
        .transition()
        .duration(200)
        .style('opacity', 0.5)

        const currentBrand = d3.select(event.currentTarget.parentNode).datum().brand; // Assuming the brand is associated with each bar
      
        // Find the corresponding object in stackedData for the current brand
        const currentData = stackedData.find(entry => entry.brand === currentBrand);
      
        // Extract 'Male' and 'Female' counts
        const gender = d.gender;
        const value = currentData ? currentData[gender] : 0; // Set default value to 0 if data for the brand is not found
      
        // Show tooltip
        tooltip.transition().duration(200).style('opacity', 0.9);
        tooltip.html(`Gender: ${gender}<br>Value: ${value}`);
      })
      .on('mousemove', (event) => {
        tooltip.style("transform","translateY(-55%)")
          .style('left',(event.pageX + 10)+'px')
          .style('top',(event.pageY - 30)+'px');
      })
      .on('mouseleave', () => {
        d3.select(event.currentTarget).style('opacity', 1)
        tooltip.transition().style('opacity', 0);
      });
      
      // Create a tooltip
        const tooltip = d3.select('#chart-container')
        .append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)
        .attr('class', 'tooltip')
        .style('position', 'absolute')
        .style('background-color', 'white')
        .style('border', 'solid')
        .style('border-width', '1px')
        .style('border-radius', '5px')
        .style('padding', '10px');

        // Add X axis
        svg2.append("g")
        .attr("transform", `translate(0,${stackedBarHeight})`)
        .call(d3.axisBottom(x));

        // Add X axis label
        svg2.append("text")
        .attr("x", stackedBarWidth/2)
        .attr("y", stackedBarHeight+stackedBarMargin.bottom)
        .style("text-anchor", "middle")
        .text("Car brand");

        // Add Y axis
        svg2.append("g")
        .call(d3.axisLeft(y));

        // Add Y axis label
        svg2.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", 0-stackedBarHeight/2)
        .attr("y", 0-1.3*stackedBarMargin.top)
        .style("text-anchor", "middle")
        .text("Number of customers");

        //3. Scatter plot
        const scatterData = resultData
        console.log(scatterData)
        
        // Filter out data points where either co2_emissions or energy_cost is null
        const filteredData = scatterData.filter(d => d.car.co2_emissions !== null && d.car.energy_cost !== null);
        console.log(filteredData);
        const scatterMargin = { top: 30, right: 20, bottom: 40, left: 50 };
        const scatterWidth = 570 - scatterMargin.left - scatterMargin.right;
        const scatterHeight = 350 - scatterMargin.top - scatterMargin.bottom;
        
        // List of unique brand-name pairs with co2_emissions and energy_cost
        const brandData = resultData.map(d => ({
            brandName: `${d.car.brand} ${d.car.name}`,
            co2Emissions: d.car.co2_emissions,
            energyCost: d.car.energy_cost
          }));
          
          const uniqueBrandData = Array.from(new Set(brandData.map(JSON.stringify).filter(
            (value, index, self) => {
              const parsed = JSON.parse(value);
              return parsed.co2Emissions !== null && parsed.energyCost !== null;
            }
          ))).map(JSON.parse);
          
          console.log(uniqueBrandData);
        
        // Create SVG element
          const svg3 = d3.select("#scatter-plot-matrix")
          .append("svg")
          .attr("width", scatterWidth + scatterMargin.left + scatterMargin.right)
          .attr("height", scatterHeight + scatterMargin.top + scatterMargin.bottom)
          .append("g")
          .attr("transform", `translate(${scatterMargin.left},${scatterMargin.top})`);
        
          const xScatter = d3.scaleLinear()
          .domain([0, d3.max(filteredData, d => d.car.co2_emissions)+0.1*d3.max(filteredData, d => d.car.co2_emissions)])
          .range([0, scatterWidth]);
        
          const yScatter = d3.scaleLinear()
          .domain([0, d3.max(filteredData, d => d.car.energy_cost+0.1*d3.max(filteredData, d => d.car.energy_cost))])
          .range([scatterHeight, 0]);
        
            // Add X axis
            svg3.append("g")
            .attr("class", "x-axis")
            .attr("transform", `translate(0,${scatterHeight})`)
            .call(d3.axisBottom(xScatter));
        
            // Add X axis label
            svg3.append("text")
            .attr("x", scatterWidth/2)
            .attr("y", scatterHeight+0.9*scatterMargin.bottom)
            .style("text-anchor", "middle")
            .text("CO2 emissions");
        
            // Add Y axis
            svg3.append("g")
            .attr("class", "y-axis")
            .call(d3.axisLeft(yScatter));
        
            // Add Y axis label
            svg3.append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", 0-scatterHeight/2)
            .attr("y", 0-1.3*scatterMargin.top)
            .style("text-anchor", "middle")
            .text("Energy cost");
        
             // Create the grid.
            svg3.append("g")
            .attr("stroke", "currentColor")
            .attr("stroke-opacity", 0.1)
            .call(g => g.append("g")
                .selectAll("line")
                .data(xScatter.ticks())
                .join("line")
                .attr("x1", d => 0.5 + xScatter(d))
                .attr("x2", d => 0.5 + xScatter(d))
                .attr("y1", 0.5)
                .attr("y2", scatterHeight))
            .call(g => g.append("g")
                .selectAll("line")
                .data(yScatter.ticks())
                .join("line")
                .attr("y1", d => 0.5 + yScatter(d))
                .attr("y2", d => 0.5 + yScatter(d))
                .attr("x1", 0.5)
                .attr("x2", scatterWidth));
        
            // Add a layer of dots
            svg3.append("g")
            .attr("stroke", "black")
            .attr("stroke-width", 0.5)
            .selectAll("circle")
            .data(filteredData)
            .join("circle")
            .attr("cx", d => xScatter(d.car.co2_emissions))
            .attr("cy", d => yScatter(d.car.energy_cost))
            .attr("r", 4)
            .attr("fill", d => BrandsColorScale(d.car.brand));
        
            // Creation of a tooltip
            const scatterTooltip = d3.select('#scatter-plot-matrix')
            .append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0)
            .attr('class', 'tooltip')
            .style('position', 'absolute')
            .style('background-color', 'white')
            .style('border', 'solid')
            .style('border-width', '1px')
            .style('border-radius', '5px')
            .style('padding', '10px');
        
            // Adding a tooltip on the chart
            svg3.selectAll("circle")
            .on('mouseover', (event, d) => {
                d3.select(event.currentTarget)
                .transition()
                .duration(200)
                .style('opacity', 0.5)
                // Set tooltip content and position
                scatterTooltip.html(`<strong>${d.car.brand} ${d.car.name}</strong><br/>CO2 emissions: ${d.car.co2_emissions.toFixed(3)} g/km <br/>Energy cost: ${d.car.energy_cost.toFixed(2)} euro`)
                scatterTooltip.transition().duration(200).style('opacity', 0.9)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 20) + "px");
            })
        
            .on('mousemove', (event) => {
                scatterTooltip.style("transform","translateY(-55%)")
                    .style('left',(event.pageX + 10)+'px')
                    .style('top',(event.pageY - 30)+'px');
                })
        
            .on('mouseleave', () => {
                d3.select(event.currentTarget).style('opacity', 1)
                scatterTooltip.transition().style('opacity', 0);
                });
        
            //Zooming a scatter plot
            const zoom = d3.zoom()
            .scaleExtent([1, 40])
            .extent([[0, 0], [scatterWidth, scatterHeight]])
            .on("zoom", zoomed);
        
            svg3.call(zoom);
        
            function zoomed({transform}) {
            const zx = transform.rescaleX(xScatter).interpolate(d3.interpolateRound);
            const zy = transform.rescaleY(yScatter).interpolate(d3.interpolateRound);
        
            svg3.selectAll("circle")
                .attr("cx", d => zx(d.car.co2_emissions))
                .attr("cy", d => zy(d.car.energy_cost));
        
            svg3.selectAll(".x-axis").call(d3.axisBottom(zx));
            svg3.selectAll(".y-axis").call(d3.axisLeft(zy));
            }
        
            const defs = svg3.append("defs");
        
            // Male filter field
            const maleFilter = defs.append("filter")
                .attr("id", "maleFilter")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", scatterWidth)
                .attr("height", scatterHeight);
        
            maleFilter.append("feColorMatrix")
                .attr("type", "matrix")
                .attr("values", "1 0 0 0 0 0 0.3 0 0 0 0 0 1 0 0 0 0 0 0.3 0");
        
            // Female filter field
            const femaleFilter = defs.append("filter")
                .attr("id", "femaleFilter")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", scatterWidth)
                .attr("height", scatterHeight);
        
            femaleFilter.append("feColorMatrix")
                .attr("type", "matrix")
                .attr("values", "0.3 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0");
        
            // Fonction pour mettre à jour le graphe de dispersion
            function updateScatterPlotWithFilters() {
              // Récupérer les états des checkboxes
              const isMaleChecked = maleCheckbox.property("checked");
              const isFemaleChecked = femaleCheckbox.property("checked");
              const selectedMaritalStatuses = Array.from(document.querySelectorAll('.marital-status-checkbox input[type="checkbox"]:checked'))
                  .map(checkbox => checkbox.id.replace('-checkbox', ''));

              // Filtrer les données en fonction des sélections
              const filtered = filteredData.filter(d => {
                  const genderMatch = (isMaleChecked && d.gender === "M") || (isFemaleChecked && d.gender === "F");
                  const maritalStatusMatch = selectedMaritalStatuses.length === 0 || selectedMaritalStatuses.includes(d.marital_status);
                  return genderMatch && maritalStatusMatch;
              });
        
                  // Supprimer les anciens points et ajouter les nouveaux
                  svg3.selectAll("circle").remove();
                  svg3.selectAll("circle")
                      .data(filtered)
                      .enter()
                      .append("circle")
                      .attr("cx", d => xScatter(d.car.co2_emissions))
                      .attr("cy", d => yScatter(d.car.energy_cost))
                      .attr("r", 4)
                      .attr("fill", d => BrandsColorScale(d.car.brand))
                      .on('mouseover', function (event, d) {
                          d3.select(event.currentTarget)
                              .transition()
                              .duration(200)
                              .style('opacity', 0.5);
        
                          scatterTooltip.html(`<strong>${d.car.brand} ${d.car.name}</strong><br/>CO2 emissions: ${d.car.co2_emissions.toFixed(3)} g/km<br/>Energy cost: ${d.car.energy_cost.toFixed(2)} euro`)
                              .transition().duration(200).style('opacity', 0.9)
                              .style("left", (event.pageX + 10) + "px")
                              .style("top", (event.pageY - 20) + "px");
                      })
                      .on('mousemove', function (event) {
                          scatterTooltip.style("transform","translateY(-55%)")
                              .style('left', (event.pageX + 10) + 'px')
                              .style('top', (event.pageY - 30) + 'px');
                      })
                      .on('mouseleave', function () {
                          d3.select(event.currentTarget).style('opacity', 1);
                          scatterTooltip.transition().style('opacity', 0);
                      });
        
              }

              // Création de checkboxes pour chaque statut marital unique
                  const uniqueMaritalStatus = [...new Set(resultData.map(d => d.marital_status))];
                  const checkboxContainer = document.getElementById('checkbox-container');

                  uniqueMaritalStatus.forEach(status => {
                    const div = document.createElement('div');
                    div.className = 'marital-status-checkbox';

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = status.toLowerCase().replace(/\s+/g, '-') + '-checkbox';

                    const label = document.createElement('label');
                    label.htmlFor = checkbox.id;
                    label.textContent = status;

                    div.appendChild(checkbox);
                    div.appendChild(label);
                    checkboxContainer.appendChild(div);
                  });
        
                // Attacher les gestionnaires d'événements aux checkboxes
                const maleCheckbox = d3.select("#male-checkbox");
                const femaleCheckbox = d3.select("#female-checkbox");

                maleCheckbox.on("change", updateScatterPlotWithFilters);
                femaleCheckbox.on("change", updateScatterPlotWithFilters);
                document.querySelectorAll('.marital-status-checkbox input[type="checkbox"]').forEach(checkbox => {
                  checkbox.addEventListener('change', updateScatterPlotWithFilters);
                });

                // Initial update
                updateScatterPlotWithFilters();
              })

  .catch(error => {
    console.error('Error while import data:', error);
  });

