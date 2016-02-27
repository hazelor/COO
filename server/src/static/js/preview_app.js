/**
 * Created by guoxiao on 16/2/27.
 */
var sign
function on_selecteditem_change(){
    clearInterval(sign)
    if ($('#chamber_name').children('option:selected').val() != ''){
        sign=setInterval(
            function(){
                $.ajax({
                    url:'preview/realtime',
                    type:'get',
                    dataType:'text',
                    data:{'mac_address':$('#chamber_name').children('option:selected').text(),
                          'postion':'',
                          'type':'' },
                    success:function(data, status){
                        var jdata = $.parseJSON(data)
                    }
                })
            },2000
        )
    }
}
