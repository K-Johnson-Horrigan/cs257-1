// Authors: Antonia Ritter and Kai Johnson
// CS257
// Feb-March 2021

/**
 * This file describes supplementary methods called by the function
 * displayGraph() in webapp.js
 */


 /**
 * Returns a 2D array (since order matters) of pairs of crop and production
 * @param  {array} results           an array in format {crop: [year: production, year: production], crop...}
 * @return {array}                   a 2D array with pairs crop and production sorted by production (descending)
 */
function sortGraphResults(results){
  // sorted results = [[crop, totalProduction], [crop, totalProduction], ...]
  var sortedResults = [];
  // fill sortedResults
  for(var crop in results){
    var totalProduction = 0;
    var productionExists = false;
    for(var year in results[crop]){
      if(results[crop][year] != null){
        totalProduction += results[crop][year];
        productionExists = true;
      }
    }
    if (productionExists){
      sortedResults.push([crop, totalProduction]) // not yet sorted
    }
  }
  // sort the array
  sortedResults.sort(function(a,b){return b[1] - a[1];});
  return sortedResults;
}


 /**
 * Generates the data and details used to create a graph in buildGraph()
 * @param  {array} results           an array in format {crop: [year: production, year: production], crop...}
 * @param  {array} sortedResults     a 2D array with pairs crop and production sorted by production (descending)
 */
// sorted results in the form [[crop, totalProduction], [crop, totalProduction], ...]
// results in the form {crop: {year: production, year: production, …}, crop: …}
function initializeGraph(sortedResults, results) {

  // if there are non-null results
  if (sortedResults.length > 0){

    // number of crops to display on graph
    var maxCrops = 8;
    // if it's a one-crop query
    if (Object.keys(results).length==1){
      maxCrops = 1;
    }

    // get top crops to graph
    var topResults = []; // a list of crops
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
        production = results[crop][year];
        productionData.push(production);
      }
      // put all the information together for a line
      var line = {label: crop, backgroundColor: colors[index], borderColor: colors[index], data: productionData, fill: false}
      // add to list of all lines
      cropLines.push(line)
    }

    buildGraph(years, cropLines);
    makeTotalTable(sortedResults);

  } else {
    noResultsMessage();
  }
}


/**
* Creates a line graph of crop production over the years and inserts it into the html
* @param  {array} years           an array of years
* @param  {array} cropLines       an array of dictionaries where each contains the information for one graph line
*/
function buildGraph(years, cropLines) {
 // insert graph canvas
 var element = document.getElementById('display-graph');
 if (element) {
   // chartjs graph gets inserted here
   element.innerHTML = '<canvas id="crop-graph"></canvas>';
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
         scaleLabel: {display: true, labelString: 'Production (tons)'},
         ticks: {
           beginAtZero: true
         }
       }]
     },
     legend: {display: true, position: 'right'}
   }
 });
}


/**
 * Creates a table of crop and production and inserts it into the html
 * @param  {array} sortedResults     a 2D array with pairs crop and production sorted by production (descending)
 */
function makeTotalTable(sortedResults){
  var html = '<h4>Total Production</h4>'
            + '<table><thead><tr><th scope="col">Crop</th>'
            + '<th scope="col">Production (tons)</th></tr></thead><tbody>';

  for(var row in sortedResults){
    var crop  = sortedResults[row][0];
    var totalProduction = sortedResults[row][1];
    //if(totalProduction>0){
    html += '<tr><th scope="row">' + crop + '</th><td>' + totalProduction.toLocaleString() + '</td>';
    //}
  }

  html += '</tbody></table>';
  var element = document.getElementById('display-table');
  if (element) {
    element.innerHTML = html;
  }
}
