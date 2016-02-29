/**
 * Created by guoxiao on 16/2/27.
 */

function update_intervals(){
    var res = new Array();
    $('.dev_interval').each(function(){
        var mac_addr = $(this).children('span').text();
        var interval = $(this).children('.duration').children('option:selected').attr('value');
        var i_res = new Object();
        i_res['mac_address'] =mac_addr;
        i_res['interval'] = parseInt(interval);
        res.push(i_res);
    });
    $.ajax({
        url:'setting/interval',
        type:'GET',
        dataType:'text',
        data:{'setting_content':JSON.stringify(res)},
        success:function(data, status){

        },
    });
}