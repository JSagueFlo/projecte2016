function mesToString(mes) {
    mesos = ['','Gener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Desembre'];
    return mesos[parseInt(mes)];
}

$('#sidebar').append('<ul id="menu"></ul>');

for (var any in dates) {
    var item_any = $('<li></li>').html('<a href="'+url+any+'/">'+ any +'</a>').append('<ul class="mesos"></ul>').attr('id', any);
    $('#menu').prepend(item_any);
    for (var mes in dates[any]) {
        var item_mes = $('<li></li>').html('<a href="'+url+any+'/'+mes+'/">'+ mesToString(mes) +'</a>').append('<ul class="dies"></ul>').attr('id',  any + '-' + mes);
        $('#'+any+' .mesos:nth-child(2)').prepend(item_mes);
        for (var dia in dates[any][mes]) {
            var item_dia = $('<li></li>').html('<a href="'+url+any+'/'+mes+'/'+dia+'/">'+ dia +'</a>').attr('id', any +'-'+ mes +'-'+ dia);
            $('#'+any+'-'+mes+' .dies:nth-child(2)').prepend(item_dia);
        }
    }
}

