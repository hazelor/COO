/**
 * Created by guoxiao on 16/2/27.
 */

function selected_history(){
    $.ajax({
        url:'history/query',
        type:'GET',
        dataType:'text',
        data:{'mac_address':'',
              'postion':$('#chamber_name').children('option:selected').text(),
              'type':$('#data_name').children('option:selected').text(),
              'start_time':$('#start_time').attr('value'),
              'end_time':$('#end_time').attr('value')
              },
        success:function(data, status){
            var jdata= $.parseJSON(data)
        },
    })
}