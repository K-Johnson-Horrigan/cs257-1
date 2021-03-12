//Authors: Antonia Ritter and Kai Johnson
//CS257
//Feb-March 2021

/**
 * This file describes supplementary methods called by the function
 * displayTable() in webapp.js
 */

function initializeChart(results){

    // number of crops to display 
    var maxCrops = 10; 

    // handle null case if results are given as nulls
    var allNull = true;

    // handle null case if results is null 
    if (results.length > 0){
        var productionData = []
        var cropLabels = [] 
        for (var i = 0; i < maxCrops; i++){
            var crop = results[i][0];
            var production = results[i][1]; 
            cropLabels.push(crop); 
            productionData.push(production);
            //handle null case 
            if (production != null){
                allNull = false; 
            }
        }
    }

    if (allNull) {
        noResultsMessage();
    } else {
        buildChart(productionData, cropLabels);
        makeTable(results); 
    }
}


function buildChart(productionData, cropLabels){

    // insert graph canvas
    var element = document.getElementById('display-graph');
    if (element) {
      // chartjs graph gets inserted here
      element.innerHTML = '<canvas id="crop-chart"></canvas>';
    }

    var colors = ['red', '#FF6D00', 'orange', 'yellowgreen', '#2DD311', 'darkgreen', 'blue', '#8700FF', 'purple', '#F7BFB4'];

    var ctx = document.getElementById('crop-chart').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'horizontalBar',
        data: {
            labels: cropLabels,
            datasets: [{
                data: productionData,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 1
            }]
        },
        options: {
        scales: {
            xAxes: [{
            display: true,
            scaleLabel: {display: true, labelString: 'Production (tons)'},
            ticks: {
                beginAtZero: true
            }
            }],
            yAxes: [{
            display: true,
            scaleLabel: {display: true, labelString: 'Crop'}
            }]
        },
        legend: {
            display: false, 
            position: 'right'
        }
        }
  });
}


function makeTable(results){

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