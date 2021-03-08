//Authors: Antonia Ritter and Kai Johnson
//CS257
//Feb-March 2021


window.onload = initialize;

/*Upon loading the page the dropdown menus are populated and a button is displayed*/
function initialize() {
    loadMenus();
    var button = document.getElementById('display_button');
    button.onclick = onDisplayButtonPress;
}

/*The dropdown menus are populated by three lists received from an api requests, '/menus/' */
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

/*If the 'display' button is pressed,
  any pre-existing display content is removed,
  the dropdown menu selections are read,
  the display type (map, graph, etc) is determined based on the dropdown selections,
  the url for the api request is retrieved,
  and then the information the user requested is displayed.*/
function onDisplayButtonPress(){
    wipeScreenClean();

    var country = document.getElementById('countries_dropdown').value;
    var crop = document.getElementById('crops_dropdown').value;
    var year = document.getElementById('years_dropdown').value;

    var displayType = getDisplayType(country, crop, year);
    var url = getURL(displayType, country, crop, year);

    display(displayType, url);
}

/*All display type containers are set to empty.*/
function wipeScreenClean(){
  document.getElementById('display-single').innerHTML = '';
  document.getElementById('display-map').innerHTML = '';
  document.getElementById('display-graph').innerHTML = '';
  document.getElementById('display-table').innerHTML = '';
}

/**
 * returns the display type depending upon the dropdown selections
 * @param  {string} country the 'countries' dropdown selection
 * @param  {string} crop    the 'crops' dropdown selection
 * @param  {string} year    the 'years' dropdown selection
 * @return {string}         the display type (eg map, graph, etc.)
 */
function getDisplayType(country, crop, year){
  if (country === 'All countries') { return 'map'; }
  else if (year === 'All years') { return 'graph'; }
  else if (crop === 'All crops') { return 'table'; }
  else { return 'single'; }
  return '';
}

/**
 * returns the url for the desired data
 * @param  {string} displayType the display type (eg map, graph, etc.)
 * @param  {string} country     the 'countries' dropdown selection
 * @param  {string} crop        the 'crops' dropdown selection
 * @param  {string} year        the 'years' dropdown selection
 * @return {string}             the url
 */
function getURL(displayType, country, crop, year){
  url = getAPIBaseURL();
  if (displayType === 'map') { url += '/mapped_production/' + crop + '/' + year; }
  else if (displayType === 'graph') { url += '/graphed_production/' + country + '/' + crop; }
  else if (displayType === 'table') { url += '/tabled_production/' + country + '/' + year; }
  else if (displayType === 'single') { url += '/single_production/' + country + '/' + crop + '/' + year; }
  return url;
}

/**
 * returns basic api url
 * @return {string} the basic api url
 */
function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

/**
 * retrieves the results of the url from the api,
 * then passes them to the appropriate display method
 * @param  {string} displayType the display type (eg map, graph, etc.)
 * @param  {string} url         the specific url for the particular set of country/crop/year selections
 */
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


/*displayMap() and displayGraph() both take several suplementary methods
that are described in map.js and graph.js respectively */


/**
 * displays a world map with each country shaded acording to the amount of production
 * @param  {dictionary} results key as the abbreviation and
                                value as the production and name of each country
                                eg {'USA': 'production': 8000, 'country_name', 'United States of America', ...}
  */
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

/**
 * displays a line graph with each line representing a crop over time,
 * x-axis and time (in years) and y-axis as production (in tonnes)
 * @param  {dictionary} results key as crop
                                value as a dictionary with keys year and values production
                                eg {'Maize': {1961: 7000, 1962: 1000, ...} ...},
 */
function displayGraph(results){
  // takes results in format {crop: [year: production, year: production], crop...}
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

/**
 * displays a table of crops and their productions, sorted by production (descending)
 * @param  {list} results 2D list of crop-production pairs, sorted by production (descending)
                          eg [['Maize', 201000], ...]
 */
function displayTable(results){
  var html = '<h4>Crop Production</h4><table>'
            + '<thead><tr><th scope="col">Crop</th>'
            + '<th scope="col">Production (tons)</th>'
            + '</tr></thead><tbody>';

  //add rows
  for (var i = 0; i < results.length; i++){
    var crop = results[i][0];
    var production = results[i][1];
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

/**
 * displays the tonnes produced or a message if none was produced
 * @param  {int} results an integer description of how much was produced
 */
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
