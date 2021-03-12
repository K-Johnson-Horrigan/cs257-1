//Authors: Antonia Ritter and Kai Johnson
//CS257
//Feb-March 2021

/**
 * This file describes supplementary methods called by the function
 * displayGraph() in webapp.js
 */

function makeAnnualTable(results){
  var html = '<h4>Annual Production</h4>'
                      + '<table><thead><tr><th scope="col">Crop</th>'
                      + '<th scope="col">Year</th>'
                      + '<th scope="col">Production (tons)</th></tr></thead><tbody>';
  for(var crop in results){
    for(var year in results[crop]){
      if(results[crop][year] != null){
        html += '<tr><th scope="row">' + crop + '</th><td>' + year + '</td><td>' + results[crop][year].toLocaleString() + '</td>';
      }
    }
  }
  html += '</tbody></table>';
  return html;
}

// takes results in format {crop: [year: production, year: production], crop...}
// returns something like [[crop, production], [crop, production]] sorted by production (descending)
function sortGraphResults(results){
  // sorted results = [[crop, totalProduction], [crop, totalProduction], ...]
  var sortedResults = [];
  // fill sortedResults
  for(var crop in results){
    var totalProduction = 0;
    for(var year in results[crop]){
      if(results[crop][year] != null){
        totalProduction += results[crop][year];
      }
    }
    sortedResults.push([crop, totalProduction]) // not yet sorted
  }
  // sort the array
  sortedResults.sort(function(a,b){return b[1] - a[1];});
  return sortedResults;
}

// takes sorted results in format [[crop, totalProduction], [crop, totalProduction], ...]
// returns html for a table with headints Crop and production
function makeTotalTable(sortedResults){
  var html = '<h4>Total Production</h4>'
            + '<table><thead><tr><th scope="col">Crop</th>'
            + '<th scope="col">Production (tons)</th></tr></thead><tbody>';

  for(var row in sortedResults){
    var crop  = sortedResults[row][0];
    var totalProduction = sortedResults[row][1];
    if(totalProduction>0){
      html += '<tr><th scope="row">' + crop + '</th><td>' + totalProduction.toLocaleString() + '</td>';
    }
  }

  html += '</tbody></table>';
  return html;
}

// sorted results in the form [[crop, totalProduction], [crop, totalProduction], ...]
// results in the form {crop: {year: production, year: production, …}, crop: …}
function initializeGraph(sortedResults, results) {

  // number of crops to display on graph
  var maxCrops = 8;

  // insert graph canvas
  var element = document.getElementById('display-graph');
  if (element) {
    // chartjs graph gets inserted here
    element.innerHTML = '<canvas id="crop-graph"></canvas>';
  }

  // get top crops to graph
  var topResults = []; // a list of crops
  // if it's a one-crop query
  if (Object.keys(results).length==1){
    maxCrops = 1;
  }
  for (var i = 0; i < maxCrops; i++){
    topResults.push(sortedResults[i][0]);
  }

  var colors = ['red', 'orange', 'yellowgreen', 'green', 'darkgreen', 'blue', 'purple', '#F7BFB4'];

  // get years for x-axis
  var years = [];
  for (var year in results[topResults[0]]){ //loop though first crop
    years.push(year);
  }

  // "datasets" are the lines
  // the things in datasets are: {label: corn, backgroundColor: a color, borderColor: a color, data: [production, production, ...], fill: false}
  var cropLines = [];
  // results = {crop: {year: production, year: production, …}, crop: …}
  for (var index in topResults){
    crop = topResults[index];
    var productionData = [];
    for (var year in results[crop]){
      productionData.push(results[crop][year])
    }
    var line = {label: crop, backgroundColor: colors[index], borderColor: colors[index], data: productionData, fill: false}
    cropLines.push(line)
  }

  var ctx = document.getElementById('crop-graph').getContext('2d');
  var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: {
        // the x-axis
        labels: years,
        // the lines
        datasets: cropLines
    },
    // Configuration options go here
    options: {
      hover: {
        mode: 'nearest',
        intersect: true
      },
      scales: {
        xAxes: [{
          display: true,
          scaleLabel: {display: true, labelString: 'Year'}
        }],
        yAxes: [{
          display: true,
          scaleLabel: {display: true, labelString: 'Production (tons)'}
        }]
      },
      legend: {display: true, position: 'right'}
    }
  });
}
