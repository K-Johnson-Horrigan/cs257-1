// Authors: Antonia Ritter and Kai Johnson
// CS257
// Feb-March 2021


/**
 * This file describes supplementary methods called by the function
 * displayMap() in webapp.js
 */


 /**
  * Returns the greates production value of the returned countries
  * @param  {dictionary} results the dictionary of (sorted by production) results
  * @return {int}                the production of the first element in the dictionry, the highest production
  */
 function getHighestProduction(results){
   var highestProduction = 0;
   for (var key in results){
     if (highestProduction == 0){
       highestProduction = results[key]['production'];
       return highestProduction;
     }
   }
 }

 
/**
 * Returns a 2D array (since order matters) of pairs of
 * production step value and the corresponding color hex
 * @param  {int}  highestProduction  the highest production value of the displayed countries
 * @param  {array} colors            an array of hex color values
 * @return {array}                   a 2D array with pairs step value and corresponding color
 */
function createProductionColorKey(highestProduction, colors){
  var step = highestProduction / colors.length;
  var productionColorKey = [];
  for (var i = 1; i <= colors.length; i++){
    productionColorKey.push([(i * step), colors[i-1]]);
  }
  return productionColorKey;
}


/**
 * Creates and returns a dictionary that is essentially just 'results'
 * with an additional field per country describing color,
 * assigned based on the color brackets of 'productionColorKey'
 * @param  {dictionary} results             the dictionary of results in format
                                            {'USA': 'production': 8000, 'country_name', 'United States of America', ...}
 * @param  {array}       productionColorKey  a 2D array of step-color pairs
 * @return {dictionary}                     results but with the added field of a color
 */
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


/**
 * Creates and displays a world map according to the user's parameters
 * @param  {dictionary} resultsWithColorFills each country abbreviation and its color fill, production, and name
 */
function initializeMap(resultsWithColorFills) {
    var map = new Datamap({ element: document.getElementById('display-map-container'), // where in the HTML to put the map
                            scope: 'world', // which map?
                            projection: 'equirectangular', // what map projection? 'mercator' is also an option
                            data: resultsWithColorFills, // here's some data that will be used by the popup template
                            fills: { defaultFill: '#ffffff'},
                            geographyConfig: {
                                popupTemplate: hoverPopupTemplate,
                                borderColor: '#000000',
                                highlightFillColor: false, // You can disable the color change on hover
                                highlightBorderColor: '#000000'
                                }
                          });
}


/**
 * Returns the description of a popup containing
 * country name and production for when a country is hovered over
 * @param  {}           geography the geography of the map
 * @param  {dictionary} data      the data of the map, contianing
 * @return                        the html description of the popup
 */
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


/**
 * Displays the map legend
 * @param  {dictionary} productionColorKey the 2D array describing step-color pairs
 */
function displayLegend(productionColorKey){
  html = '<h5>Legend (production in tons):</h5>';
  var previousStep = 0;
  for (var i = 0; i < productionColorKey.length; i++){
    var textColor = productionColorKey[productionColorKey.length - 1 - i][1];
    var backgroundColor = productionColorKey[i][1];
    var step = productionColorKey[i][0];
    html += '<div style="background-color:' + backgroundColor
          + ';color:' + textColor + ';">' + Math.round(previousStep).toLocaleString() + ' - '
          + Math.round(step).toLocaleString() + '</div>';
    previousStep = productionColorKey[i][0];
  }
  var legendElement = document.getElementById('legend-map');
  if (legendElement) {
      legendElement.innerHTML = html;
  }
}


/**
 * Returns a sorted array of the map data
 * @param  {dictionary} results data in format {'USA': {'production': 189900, 'country_name': United States of America}
 * @return {array}              data in format [[United States of America, 189900], [Australia, 5], ...]
 */
function sortMapResults(results){
  var sortedResults = [];
  for (var countryAbb in results){
    console.log(countryAbb);
    sortedResults.push([results[countryAbb]['country_name'], results[countryAbb]['production']]);
  }

  // sort the array
  sortedResults.sort(function(a,b){
    return b[1] - a[1];
  });
  return sortedResults;
}


/**
 * Displays a table of each country and its production
 * @param  {array} sortedResults data in format [[United States of America, 189900], [Australia, 5], ...]
 */
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
