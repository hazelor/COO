/**
 * Created by guoxiao on 16/2/27.
 */

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
