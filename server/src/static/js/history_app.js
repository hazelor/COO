/**
 * Created by guoxiao on 16/2/27.
 */


function render_chart(title, data){
    $('#container').highcharts({                   //图表展示容器，与div的id保持一致
        chart: {
            type: 'line',                         //指定图表的类型，默认是折线图（line）
            zoomType: 'x',
        },
        title:{
            text: title
        },
        xAxis: {
            type: 'datetime',
            },
        yAxis: {
            title: {
                text: title                  //指定y轴的标题
            },
            plotLines: [{
                value: 0,
                width: 1,
                color:'blue'
                //color: '#808080'
            }]
        },
        tooltip: {
            backgroundColor:'#fff',
            borderColor:'black',
            formatter: function () {        //数据提示框中单个点的格式化函数
                return '<b>' + this.series.name+ '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 3);   //小数后几位
            }
        },
        legend: {
                enabled: true
            },
        series: [{                                 //指定数据列
            name: title,                          //数据列名
            data: data                              //数据
        }]
    });
}


$(function(){
    render_chart("",[])
        });


function selected_history(){
    //alert(document.getElementById('start_time').value)
    var start_time_str = document.getElementById('start_time').value;
    var end_time_str = document.getElementById('end_time').value;
    var start_time = new Date(Date.parse(start_time_str.replace(/-/g, "/")));
    var end_time = new Date(Date.parse(end_time_str.replace(/-/g, "/")));
    var interval = (end_time.getTime()-start_time.getTime());
    var data_name = $('#data_name').children('option:selected').text();
    $.ajax({
        url:'history/query',
        type:'GET',
        dataType:'text',
        data:{'mac_address':$('#chamber_name').children('option:selected').attr('value').split(',')[0],
              'position':$('#chamber_name').children('option:selected').attr('value').split(',')[1],
              'type':$('#data_name').children('option:selected').attr('value'),
              'start_time':document.getElementById('start_time').value,
              'end_time':document.getElementById('end_time').value
              },
        success:function(data, status){
            var jdata= $.parseJSON(data)
            render_chart(data_name, jdata)
        },
    })
}


function chamber_changed(){
    var current_chamber_key = document.getElementById("chamber_name").value;
    $.ajax({
        url:'/history',
        type:'get',
        data:{'current_chamber_key': current_chamber_key},
        success:function(data, status){
            data_dict = JSON.parse(data)
            $("#data_name option").remove();
            $.each(data_dict, function(key,content){
                $("#data_name").append("<option value="+key+">"+content+"</option>");
            });
        }
    })
}

