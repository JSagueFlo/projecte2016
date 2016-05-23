// Configuració de les gràfiques històriques

var chart_aigua_data = [['','Temp Aigua']];
var chart_aire_data = [['','Temp Aire']];
var chart_vent_data = [['','Vent']];

mitjanes.map(function(reg) {

   chart_aigua_data.push([
       (reg.mes || reg.dia || reg.hora).toString(), reg.tmp_aigua
   ]);
   chart_aire_data.push([
       (reg.mes || reg.dia || reg.hora).toString(), reg.tmp_aire
   ]);
   chart_vent_data.push([
       (reg.mes || reg.dia || reg.hora).toString(), reg.wind_speed
   ]);
});
google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data_aigua = google.visualization.arrayToDataTable(chart_aigua_data);

    var options_aigua = {
        legend: { position: 'none' },
        vAxis: { format: '#.# °C' , viewWindow: {max: 25, min: 5}, gridlines: { color: '#b2dfdb' }},
        hAxis: { gridlines: { count: 31, color: '#b2dfdb'}},
        colors: ['#009688'],
        chartArea: { backgroundColor: '#f2fafa' }
    };

    var chart = new google.charts.Line(document.getElementById('chart_aigua'));

    chart.draw(data_aigua, google.charts.Line.convertOptions(options_aigua));

    var data_aire = google.visualization.arrayToDataTable(chart_aire_data);

    var options_aire = {
        legend: { position: 'none' },
        vAxis: { format: '#.# °C' , viewWindow: {max: 40, min: -5}, gridlines: { color: '#b2dfdb' }},
        hAxis: { gridlines: { count: 31, color: '#b2dfdb'}},
        colors: ['#009688'],
        chartArea: { backgroundColor: '#f2fafa' }
    };

    var chart = new google.charts.Line(document.getElementById('chart_aire'));

    chart.draw(data_aire, google.charts.Line.convertOptions(options_aire));

    var data_vent = google.visualization.arrayToDataTable(chart_vent_data);

    var options_vent = {
        legend: { position: 'none' },
        vAxis: { format: '#.# Km/h' , viewWindow: {max: 60, min: 0}, gridlines: { color: '#b2dfdb' }},
        hAxis: { gridlines: { count: 31, color: '#b2dfdb'}},
        colors: ['#009688'],
        chartArea: { backgroundColor: '#f2fafa' }
    };

    var chart = new google.charts.Line(document.getElementById('chart_vent'));

    chart.draw(data_vent, google.charts.Line.convertOptions(options_vent));
}

$(window).on('resize', function() {
    drawChart();
});
