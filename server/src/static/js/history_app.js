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

function chamber_changed(){
    var current_chamber_key = document.getElementById("chamber_name").value;
    $.ajax({
        url:'/preview',
        type:'get',
        data:{'current_chamber_key': current_chamber_key},
        success:function(data, status){
            data_dict = JSON.parse(data)
            $("#data_name option").remove();
            $.each(data_dict, function(key,content){
                $("data_name").append("<option value="+key+">"+content+"</option>");
            });
        }
    })
}

