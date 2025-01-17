//Authors: Antonia Ritter and Kai Johnson
//CS257
//Feb-March 2021

/**
 * This file describes supplementary methods called by the function
 * buildStartingPage() in webapp.js
 */

/**
 * the dropdowns for "countries" "crops" and "years" and created and populated
 * @param {dictionary} countriesCropsYears has keys "countries" "crops" and "years"
 *                                         and corresponding values a list of elements for that category
 */
function buildMenus(countriesCropsYears){
  for(var category in countriesCropsYears){
    var html = '';
    var elements = countriesCropsYears[category];
    html += '<select id="' + category + '-dropdown">';
    for(var j = 0; j < elements.length; j++){
      html += '<option value="' + elements[j] + '">' + elements[j] + '</option>';
    }
    html += '</select>';
    var categoryColumn = document.getElementById(category + '-col');
    if (categoryColumn) {
      categoryColumn.innerHTML = html;
    }
  }
}

/**
 * Returns a randomly selected country crop year combination,
 * randomization weighted so that "All" options ("All countries" etc) have a
 * 50% chance and a unqiue option (eg "China") has a 50% chance, since "All" options
 * produce more interesting displays
 * @param  {dictionary} countriesCropsYears contains keys "countries", "crops", and "years"
 *                                          with values the list of unique values for each of those categories
 * @return {dictionary}                     contains same keys "countries", "crops", and "years" but
 *                                          with values as a randomly selected element from each catergory
 */
function chooseRandomCountryCropYear(countriesCropsYears){
  var randomElements = {};
  for (var category in countriesCropsYears){
    var randomElement = '';
    // generates 1 (all) or 0 (not all)
    var notAllOrAll = Math.floor(Math.random() * 2);
    if (notAllOrAll == 1){ //selects the "All" option for the category
      var allIndex = 0;
      randomElement = countriesCropsYears[category][allIndex];
    }
    else { //selects some random option other than the "All" option
      var notAllRandomIndex = Math.floor(Math.random() * (countriesCropsYears[category].length - 1)) + 1;
      randomElement = countriesCropsYears[category][notAllRandomIndex];
    }
    randomElements[category] = randomElement;
  }
  return randomElements;
}


/**
 * Sets the dropdown selections to the randomized dropdown values
 * @param {dictionary} randomCountryCropYear a dictionary with keys "countries", "crops", and "years" with
 *                                           values a randomly selected element from each catergory
 */
function menuSelectRandomCountryCropYear(randomCountryCropYear){
  for (var category in randomCountryCropYear){
    var dropdown = document.getElementById(category + '-dropdown');
    if (dropdown){
      dropdown.value = randomCountryCropYear[category];
    }
  }
}


/**Inserts startup message into html */
function startupMessage(){
  var html = '<p id="display-text">Here\'s a randomized selection to get you started. Now use the dropdown menus to select your own!</p> <p> Visit the <a href="about.html">about</a> page for details about display features.</p>'
  var element = document.getElementById('startup');
  if (element) {
    element.innerHTML = html;
  }
}


/**
 * Displays a message that there was no production for the selected combination.
 */
function noResultsMessage(){
  var element = document.getElementById('display-single');
  if (element) {
    // chartjs graph gets inserted here
    element.innerHTML = '<p id="display-text">No production was reported!</p>';
  }
}
