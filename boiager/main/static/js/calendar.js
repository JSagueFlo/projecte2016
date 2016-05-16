$('#calendar').pickadate({
    min: min_data,
    max: max_data,
    format: 'yyyy/mm/dd',
    today: 'Avui',
    clear: '',
    close: 'Tancar',
    firstDay: 1,
    monthsFull: ['gener', 'febrer', 'març', 'abril', 'maig', 'juny', 'juliol', 'agost', 'setembre', 'octubre', 'novembre', 'desembre'],
    monthsShort: ['gen', 'feb', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'oct', 'nov', 'des'],
    weekdaysFull: ['diumenge', 'dilluns', 'dimarts', 'dimecres', 'dijous', 'divendres', 'dissabte'],
    weekdaysShort: ['dg', 'dl', 'dt', 'dc', 'dj', 'dv', 'ds'],
    selectMonths: true,
    selectYears: true,
});

$('#calendar').on('change', function(){
    var data = $(this).val().split('/');
    window.location.href = url + data[0] + '/' + data[1] + '/' + data[2] + '/';
});
