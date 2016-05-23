// Configuració de les gràfiques en viu que es refresquen cada 5s mitjançant AJAX

var ultims = ultims_registres.map(function(reg) {
    return reg.fields;
});

var chart_aigua_data = [['','Temp Aigua']];
var chart_aire_data = [['','Temp Aire']];
var chart_vent_data = [['','Vent']];

var tmp_water_now = $('#tmp_water_now');
var tmp_water_min = $('#tmp_water_min');
var tmp_water_max = $('#tmp_water_max');
var tmp_air_now = $('#tmp_air_now');
var tmp_air_min = $('#tmp_air_min');
var tmp_air_max = $('#tmp_air_max');
var wind_speed_now = $('#wind_speed_now');
var wind_speed_min = $('#wind_speed_min');
var wind_speed_max = $('#wind_speed_max');

function changeValues(reg) {
    var tmp_water = parseFloat(reg.tmp_water).toFixed(1);
    var tmp_air = parseFloat(reg.tmp_air).toFixed(1);
    var wind_speed = parseFloat(reg.wind_speed).toFixed(1);

    tmp_water_now.text(tmp_water);
    if (parseFloat(tmp_water) > parseFloat(tmp_water_max.text()))
        tmp_water_max.text(tmp_water);
    else if (parseFloat(tmp_water) < parseFloat(tmp_water_min.text()))
        tmp_water_min.text(tmp_water);
    
    tmp_air_now.text(tmp_air);
    if (parseFloat(tmp_air) > parseFloat(tmp_air_max.text()))
        tmp_air_max.text(tmp_air);
    else if (parseFloat(tmp_air) < parseFloat(tmp_air_min.text()))
        tmp_air_min.text(tmp_air);
    
    wind_speed_now.text(wind_speed);
    if (parseFloat(wind_speed) > parseFloat(wind_speed_max.text()))
        wind_speed_max.text(wind_speed);
    else if (parseFloat(wind_speed) < parseFloat(wind_speed_min.text()))
        wind_speed_min.text(wind_speed);
}

ultims.map(function(reg) {

   chart_aigua_data.push([
       new Date(reg.timestamp), parseFloat(reg.tmp_water)
   ]);
   chart_aire_data.push([
       new Date(reg.timestamp), parseFloat(reg.tmp_air)
   ]);
   chart_vent_data.push([
       new Date(reg.timestamp), parseFloat(reg.wind_speed)
   ]);
});

google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data_aigua = google.visualization.arrayToDataTable(chart_aigua_data);

    var options_aigua = {
        legend: { position: 'none' },
        vAxis: { format: '#.# °C' , viewWindow: {max: 25, min: 5}, gridlines: { color: '#b2dfdb' }},
        hAxis: { type: 'timeofday', gridlines: { count: 2, color: '#b2dfdb'}},
        colors: ['#009688'],
        chartArea: { backgroundColor: '#f2fafa' }
    };

    var chart = new google.charts.Line(document.getElementById('chart_aigua'));

    chart.draw(data_aigua, google.charts.Line.convertOptions(options_aigua));

    var data_aire = google.visualization.arrayToDataTable(chart_aire_data);

    var options_aire = {
        legend: { position: 'none' },
        vAxis: { format: '#.# °C' , viewWindow: {max: 40, min: -5}, gridlines: { color: '#b2dfdb' }},
        hAxis: { type: 'timeofday', gridlines: { count: 10, color: '#b2dfdb'}},
        colors: ['#009688'],
        chartArea: { backgroundColor: '#f2fafa' }
    };

    var chart = new google.charts.Line(document.getElementById('chart_aire'));

    chart.draw(data_aire, google.charts.Line.convertOptions(options_aire));

    var data_vent = google.visualization.arrayToDataTable(chart_vent_data);

    var options_vent = {
        legend: { position: 'none' },
        vAxis: { format: '#.# Km/h' , viewWindow: {max: 60, min: 0}, gridlines: { color: '#b2dfdb' }},
        hAxis: { type: 'timeofday', gridlines: { count: 10, color: '#b2dfdb'}},
        colors: ['#009688'],
        chartArea: { backgroundColor: '#f2fafa' }
    };

    var chart = new google.charts.Line(document.getElementById('chart_vent'));

    chart.draw(data_vent, google.charts.Line.convertOptions(options_vent));
}

$(window).on('resize', function() {
    drawChart();
});

setInterval(function() {
    console.log("fetching new data...");
    $.ajax({
        url: window.location.pathname,
        type: 'GET',
        dataType: 'json',
        cache: false
    })
    .done(function(data) {
        var jsondata = JSON.parse(data);
        ultims = jsondata.map(function(reg) {
            return reg.fields;
        });
        
        ultim = ultims[9];
        changeValues(ultim);

        chart_aigua_data = [['','Temp Aigua']];
        chart_aire_data = [['','Temp Aire']];
        chart_vent_data = [['','Vent']];

        ultims.map(function(reg) {

           chart_aigua_data.push([
               new Date(reg.timestamp), parseFloat(reg.tmp_water)
           ]);
           chart_aire_data.push([
               new Date(reg.timestamp), parseFloat(reg.tmp_air)
           ]);
           chart_vent_data.push([
               new Date(reg.timestamp), parseFloat(reg.wind_speed)
           ]);
        });
        drawChart();
    });
}, 5000);
