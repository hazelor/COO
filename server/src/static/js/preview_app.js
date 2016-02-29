/**
 * Created by guoxiao on 16/2/27.
 */
var sign
function on_selecteditem_change(){
    render_chart()
    //var chart = $('#container').highcharts()
    //var series = chart.series;
    //series[0].remove(false)
    //series[1].remove(false)
    if(sign){
        clearInterval(sign)
    }
    if ($('#chamber_name').children('option:selected').val() != ''){
        //var title = {
        //    text:$('#chamber_name').children('option:selected').text()
        //}
        //var chart = new Highcharts.Chart()
        //chart.setTitle(title)
        sign=setInterval(
            function(){
                $.ajax({
                    url:'preview/realtime',
                    type:'get',
                    dataType:'text',
                    data:{'current_chamber_key':$('#chamber_name').children('option:selected').attr('value'),
                          //'postion':'',
                          //'type':''
                         },
                    success:function(data, status){
                        var data = $.parseJSON(data)
                        var detail_data = data[0]
                        var plot_data = data[1]
                        if(plot_data != ''){
                            //var plot_data = $.parseJSON(data)
                            var chart = $('#container').highcharts()
                            var series = chart.series;
                            serie_1_len = series[0].data.length
                            serie_2_len = series[1].data.length
                            if(serie_1_len != 0){
                                if(series[0].data[serie_1_len-1]['x'] != plot_data[0][0]){
                                    if(plot_data[0][0]-series[0].data[0]['x']>=60*1000){
                                        series[0].addPoint(plot_data[0],true,true)
                                    }
                                    else{
                                        series[0].addPoint(plot_data[0],true,false)
                                    }
                                }
                            }
                            else{
                                series[0].addPoint(plot_data[0],true,false)
                            }
                            if(serie_2_len != 0){
                                if(series[1].data[serie_2_len-1]['x'] != plot_data[1][0]){
                                    if(plot_data[1][0]-series[1].data[0]['x']>=60*1000){
                                        series[1].addPoint(plot_data[1],true,true)
                                    }
                                    else{
                                        series[1].addPoint(plot_data[1],true,false)
                                    }
                                }

                            }
                            else{
                                series[1].addPoint(plot_data[1],true,false)
                            }
                        }
                        if(detail_data != ''){
                            var innerHTML_str = '<colgroup><col class="col-xs-1"><col class="col-xs-3"></colgroup><thead><tr><th>项目</th><th>信息</th></tr></thead>'
                            //for(item in detail_data){
                            //    for(key in item)
                            //        innerHTML_str = innerHTML_str+'<tr>'+'<td>'+key+'</td>'+'<td>'+item[key]+'</td>'+'</tr>'
                            //}
                            //alert(innerHTML_str)
                            //document.getElementById('detail_content').innerHTML = innerHTML_str
                            for (var i=0;i<(detail_data.length)/2;i++){
                                innerHTML_str = innerHTML_str+'<tr>'+'<td>'+detail_data[2*i]+'</td>'+'<td>'+detail_data[2*i+1]+'</td>'+'</tr>'
                            }
                            document.getElementById('detail_content').innerHTML = innerHTML_str
                            //alert(innerHTML_str)
                        }
                    }
                })
            },2000
        )
    }
}

$(function(){
    //$(function(){
    //    render_chart()
    //    });
    on_selecteditem_change()
})
function render_chart(){
    Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        $('#container').highcharts({
            chart: {

                type: 'spline',                      //曲线样式
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                //events: {
                //    load: function () {
                //
                //        // set up the updating of the chart each second
                //        var series = this.series[0];
                //        setInterval(function () {                            //setInterval定时器
                //            var x = (new Date()).getTime(), // current time
                //                y = Math.random();
                //            series.addPoint([x, y], true, true);
                //        }, 1000);
                //    }
                //}
            },
            title:{
                text:'CO2浓度'
            },

            xAxis: {
                type: 'datetime',
                minRange:60*1000
                //minRange:60*1000

            },
            yAxis: {
                title: {
                    text: 'ppm'
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
            exporting: {
                enabled: false
            },
            series: [{
                    name: '测量浓度',
                    //data: (function () {
                    //    // generate an array of random data
                    //    var data = [],
                    //        time = (new Date()).getTime(),
                    //        i;
                    //
                    //    for (i = -19; i <= 0; i += 1) {
                    //        data.push({
                    //            x: time + i * 1000,
                    //            y: Math.random()
                    //        });
                    //    }
                    //    return data;
                    //}())
                },
                {
                    name: '目标浓度',
                    //data: (function () {
                    //    // generate an array of random data
                    //    var data = [],
                    //        time = (new Date()).getTime(),
                    //        i;
                    //
                    //    for (i = -19; i <= 0; i += 1) {
                    //        data.push({
                    //            x: time + i * 1000,
                    //            y: Math.random()
                    //        });
                    //    }
                    //    return data;
                    //}())
                }]
        })
}