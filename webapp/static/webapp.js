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


function displayMap(results){
  initializeMap()
}


function displayGraph(results){
  /*
  var html = '<p> display graph of results:</p>';
  for(var key in results){
    html += '<p> crop: ' + key + '</p>'
    for(var subkey in results[key]){
      html += '<p>' + subkey + ' : ' + results[key][subkey] + '</p>';
    }
  }
  var menuListElement = document.getElementById('display-graph');
  if (menuListElement) {
      menuListElement.innerHTML = html;
  }
  */
  var html = '<thead><tr><th scope="col">Crop</th>' 
                      + '<th scope="col">Year</th>'
                      + '<th scope="col">Yield (tons)</th></tr></thead><tbody>';
  for(var crop in results){
    for(var year in results[crop]){
      if(results[crop][year] != null){
        html += '<tr><th scope="row">' + crop + '</th><td>' + year + '</td><td>' + results[crop][year] + '</td>';
      }
    }
  }
  html += '</tbody>';
  var menuListElement = document.getElementById('display-table');
  if (menuListElement) {
      menuListElement.innerHTML = html;
  }
  //initializeGraph()
}


function displayTable(results){
  var html = '<thead><tr><th scope="col">Crop</th><th scope="col">Yield (tons)</th></tr></thead><tbody>';
  for(var key in results){
    if(results[key] != null){
      html += '<tr><th scope="row">' + key + '</th><td>' + results[key] + '</td>';
    }
  }
  html += '</tbody>';
  var menuListElement = document.getElementById('display-table');
  if (menuListElement) {
      menuListElement.innerHTML = html;
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

var extraCountryInfo = {USA: {yield: 100, fillColor: '#2222aa'}, CAN: {yield: 100, fillColor: '#2222aa'}};
var mapFills = {defaultFill: '#2222aa', CAN: '#2222aa'};

function initializeMap() {
    var map = new Datamap({ element: document.getElementById('display-map'), // where in the HTML to put the map
                            scope: 'world', // which map?
                            projection: 'equirectangular', // what map projection? 'mercator' is also an option
                            data: extraCountryInfo, // here's some data that will be used by the popup template
                            fills: { defaultFill: '#aa2222'},
                            geographyConfig: {
                                popupOnHover: false, // You can disable the hover popup
                                highlightOnHover: false, // You can disable the color change on hover
                                }
                          });
}

function initializeGraph() {
  var data = {
    labels: [2016, 2017, 2018, 2019],
    series: [
      { className: 'thing1', data: [400, 400, 500, 300] },
      { className: 'thing2', data: [600, 300, 400, 500] },
    ]};
  var options = {}
  new Chartist.Line('#display-graph', data, options);
}
