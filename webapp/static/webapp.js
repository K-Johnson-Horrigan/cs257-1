//Authors: Antonia Ritter and Kai Johnson
//CS257 
//Feb-March 2021


function loadMenus() {
  var url = getAPIBaseURL() + '/menus/';
  fetch(url, {method: 'get'})
  .then((response) => response.json())
  .then(function(menus) {
    var dropdowns = ['countries', 'crops', 'years'];
    for (var i = 0; i < dropdowns.length; i++){
      var dropdown = dropdowns[i];
      var html = '';
      var elements = menus[0][dropdown];
      html += '<select id="' + dropdown + '_dropdown">';
      for(var j = 0; j < elements.length; j++){
        html += '<option value="' + elements[j] + '">' + elements[j] + '</option>';
      }
      html += '</select>';
      var menuElement = document.getElementById(dropdown + '_col');
      if (menuElement) {
          menuElement.innerHTML = html;
      }
    }
  })
  .catch(function(error) {
      console.log(error);
  });
}


function onDisplayButtonPress(){
    wipeScreenClean();
    
    var country = document.getElementById('countries_dropdown').value;
    var crop = document.getElementById('crops_dropdown').value;
    var year = document.getElementById('years_dropdown').value;

    var displayType = getDisplayType(country, crop, year);
    var url = getURL(displayType, country, crop, year);
    display(displayType, url);
}


function wipeScreenClean(){
  document.getElementById('display-single').innerHTML = '';
  document.getElementById('display-map').innerHTML = '';
  document.getElementById('display-graph').innerHTML = '';
  document.getElementById('display-table').innerHTML = '';
}


function getDisplayType(country, crop, year){
  if (country === 'All countries') { return 'map'; }
  else if (year === 'All years') { return 'graph'; }
  else if (crop === 'All crops') { return 'table'; }
  else { return 'single'; }
  return '';
}

function getURL(displayType, country, crop, year){
  url = getAPIBaseURL();
  if (displayType === 'map') { url += '/mapped_production/' + crop + '/' + year; }
  else if (displayType === 'graph') { url += '/graphed_production/' + country + '/' + crop; }
  else if (displayType === 'table') { url += '/tabled_production/' + country + '/' + year; }
  else if (displayType === 'single') { url += '/single_production/' + country + '/' + crop + '/' + year; }
  return url;
}


function display(displayType, url){
  fetch(url, {method: 'get'})
  .then((response) => response.json())
  .then(function(results) {
      if (displayType === 'map') { displayMap(results); }
      else if (displayType === 'graph') { displayGraph(results); }
      else if (displayType === 'table') { displayTable(results); }
      else if (displayType === 'single') { displaySingle(results); }
  })
  .catch(function(error) {
      console.log(error);
  });
}


// takes results in format {crop: [year: production, year: production], crop...}
function displayGraph(results){
  var sortedResults = sortGraphResults(results);
  initializeGraph(sortedResults, results);

  // Totals table (crop and total production over time)
  var html = makeTotalTable(sortedResults);

  // Annual table (crop, year, and production that year) IT'S A REALLY LONG TABLE
  //html += makeAnnualTable(results) 

  var element = document.getElementById('display-table');
  if (element) {
      element.innerHTML = html;
  }
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


// takes results of form {crop: yield, crop: yield, ...}
// sorts the results
// and makes a table with columns Crop and Production 
// sorted in descending order 
function displayTable(results){
  sortedResults = [];
  var html = '<h4>Crop Production</h4><table>'
            + '<thead><tr><th scope="col">Crop</th>'
            + '<th scope="col">Production (tons)</th>'
            + '</tr></thead><tbody>';
  for(var crop in results){
    if(results[crop] != null){
      sortedResults.push([crop, results[crop]]) // not yet sorted 
    }
  }
  // sort
  sortedResults.sort(function(a,b){return b[1] - a[1];});
  // loop through and add to html table 
  for(var row in sortedResults){
    var crop  = sortedResults[row][0];
    var production = sortedResults[row][1];
    html += '<tr><th scope="row">' + crop + '</th><td>' + production.toLocaleString() + '</td>';
  }
  // finish table 
  html += '</tbody></table>';
  // insert into html page 
  var element = document.getElementById('display-table');
  if (element) {
      element.innerHTML = html;
  }
}


function displaySingle(results){
  var html = '';
  if (results > 0){
    html = '<p> This hyper-specific request found: ' + results + ' tons.</p>';
  }
  else{
    html = '<p>Looks like nothing was produced!</p>';
  }
  var menuListElement = document.getElementById('display-single');
  if (menuListElement) {
      menuListElement.innerHTML = html;
  }
}


function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}


function initialize() {
    loadMenus();
    var button = document.getElementById('display_button');
    button.onclick = onDisplayButtonPress;
}


window.onload = initialize;


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

function displayMap(results){
  var mapElement = document.getElementById('display-map');
  if (mapElement) {
    // map gets inserted here
    // so map container spacing doesn't mess up other displays
    mapElement.innerHTML = '<div id="display-map-container"></div><br>'
                          + '<div id="legend-map"></div>';
  }
  
  var colors = ['#ffffcc', '#ffff99','#d2ff4d', '#bfff00', '#99ff99', '#00e600', '#00cc00', '#009900', '#006600', '#003300'];
  //low production color -> high production color

  var highestProduction = getHighestProduction(results);
  var productionColorKey = createProductionColorKey(highestProduction, colors);
  var colorizedResults = assignColorsToCountries(results, productionColorKey);

  initializeMap(colorizedResults);
  displayLegend(productionColorKey);

  var sortedResults = sortMapResults(results);
  var tableHTML = makeMapTable(sortedResults); 
  var tableElement = document.getElementById('display-table');
  if (tableElement) {
      tableElement.innerHTML = tableHTML;
  }
}

/*Returns a 2D array (since order matters) with of pairs of production step value and the corresponding color hex*/
function createProductionColorKey(highestProduction, colors){
  var step = highestProduction / colors.length;
  var productionColorKey = [];
  for (var i = 1; i <= colors.length; i++){
    productionColorKey.push([(i * step), colors[i-1]]);
  }
  return productionColorKey;
}

/*Retrieves the production value for the first item in the sorted dictionary of results*/
function getHighestProduction(results){
  var highestProduction = 0;
  for (var key in results){
    if (highestProduction == 0){
      highestProduction = results[key]['production'];
      return highestProduction;
    }
  }
}

/*Creates and returns a dictionary that is essentially just 'results'
with an additional field per country describing color,
assigned based on the color brackets of 'productionColorKey'*/
function assignColorsToCountries(results, productionColorKey){
  var colorizedResults = {};
  var other = results;
  for (var abbreviation in results){
    colorizedResults[abbreviation] = {};
    color = '';
    for (var i = 0; i < productionColorKey.length; i ++){
      if (results[abbreviation]['production'] <= productionColorKey[i][0]){
        color = productionColorKey[i][1];
        break;
      }
    }
    colorizedResults[abbreviation]['fillColor'] = color;
    colorizedResults[abbreviation]['countryName'] = results[abbreviation]['country_name'];
    colorizedResults[abbreviation]['production'] = results[abbreviation]['production'];
  }
  return colorizedResults;
}

function initializeMap(resultsWithColorFills) {
    var map = new Datamap({ element: document.getElementById('display-map-container'), // where in the HTML to put the map
                            scope: 'world', // which map?
                            projection: 'equirectangular', // what map projection? 'mercator' is also an option
                            data: resultsWithColorFills, // here's some data that will be used by the popup template
                            fills: { defaultFill: '#ffffff'},
                            geographyConfig: {
                              //  popupOnHover: false, // You can disable the hover popup
                                popupTemplate: hoverPopupTemplate,
                                borderColor: '#000000',
                                highlightFillColor: '#3D3D3D', // You can disable the color change on hover
                                highlightBorderColor: '#000000'
                                }
                          });
}

function hoverPopupTemplate(geography, data){
  //return 1;
  var production = 0;
  if (data && 'production' in data) {
      production = data.production;
  }

  var template = '<div class="hoverpopup-map"><strong>' + geography.properties.name + '</strong><br>\n'
                  + '<strong>Production:</strong> ' + production.toLocaleString() + '<br>\n'
                  + '</div>';

  return template;
}

function displayLegend(productionColorKey){
  html = '<h5>Legend (production in tons):</h5>';
  var previousStep = 0;
  for (var i = 0; i < productionColorKey.length; i++){
    var textColor = productionColorKey[productionColorKey.length - 1 - i][1];
    html += '<div style="background-color:' + productionColorKey[i][1] 
          + ';color:' + textColor + ';">' + Math.round(previousStep).toLocaleString() + ' - ' 
          + Math.round(productionColorKey[i][0]).toLocaleString() + '</div>';
    
          // this code makes the legend rows not full screen width
          // '<div class="row"><div class="col-4"></div>' +
          // + '<div class="col-4" style="background-color:' + productionColorKey[i][1] 
          // + ';color:' + textColor + ';">' + Math.round(previousStep) + ' - ' 
          // + Math.round(productionColorKey[i][0]) + '</div>'
          // + '<div class="col-4"></div></div>';
    previousStep = productionColorKey[i][0];
  }
  var legendElement = document.getElementById('legend-map');
  if (legendElement) {
      legendElement.innerHTML = html;
  }
}


// takes results of the form {USA: {production: 189900, country_name: United States of America}, AUS: {production: 5, country_name: Australia], …}
// returns sorted results [[United States of America, 189900], [Australia, 5], ...]
function sortMapResults(results){
  var sortedResults = []; 
  for (var country_abb in results){
    console.log(country_abb);
    sortedResults.push([results[country_abb]['country_name'], results[country_abb]['production']]); 
  }

  // sort the array 
  sortedResults.sort(function(a,b){ 
    return b[1] - a[1];
  });
  return sortedResults;
}

// takes sorted results [[United States of America, 189900], [Australia, 5], ...]
function makeMapTable(sortedResults){
  var html = '<h4>Total Production</h4>'
            + '<table><thead><tr><th scope="col">Country</th>'
            + '<th scope="col">Production (tons)</th></tr></thead><tbody>';
  for (var row of sortedResults){
    html += '<tr><th scope="row">' + row[0] + '</th><td>' + row[1].toLocaleString() + '</td>';
  }
  html += '</tbody></table>';
  return html;
}
