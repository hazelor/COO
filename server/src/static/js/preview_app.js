/**
 * Created by guoxiao on 16/2/27.
 */
var sign
function on_selecteditem_change(){
    render_chart([[],[]])
    var date = new Date()
    var end_time = date.pattern("yyyy-MM-dd hh:mm")
    var date_milliseconds = date.getTime()
    date_milliseconds -= 1000*60*19
    date = new Date(date_milliseconds)
    var start_time = date.pattern("yyyy-MM-dd hh:mm")
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
        loading_begin('数据准备中')
        //alert('--------test--------')
        $.ajax({
                url:'history/query',
                type:'GET',
                dataType:'text',
                data:{'mac_address':$('#chamber_name').children('option:selected').attr('value').split(',')[0],
                      'position':$('#chamber_name').children('option:selected').attr('value').split(',')[1],
                      'type':'',
                      'start_time':start_time,
                      'end_time':end_time
                      },
                success:function(data, status){
                    if(data==''){
                        //alert('所选择的时间段没有数据!')
                        loading_end()
                        return
                    }
                    else{
                        var jdata= $.parseJSON(data)
                        render_chart(jdata)
                        loading_end()
                    }

                },
            })
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
                                    if(plot_data[0][0]-series[0].data[0]['x']>=20*60*1000){
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
                                    if(plot_data[1][0]-series[1].data[0]['x']>=20*60*1000){
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
				var value = parseFloat(detail_data[2*i+1])
				value = value.toFixed(2)
                                innerHTML_str = innerHTML_str+'<tr>'+'<td>'+detail_data[2*i]+'</td>'+'<td>'+value+'</td>'+'</tr>'
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
    var opts = {
      lines: 12,            // The number of lines to draw
      length: 7,            // The length of each line
      width: 5,             // The line thickness
      radius: 10,           // The radius of the inner circle
      scale: 1.0,           // Scales overall size of the spinner
      corners: 1,           // Roundness (0..1)
      color: '#000',        // #rgb or #rrggbb
      opacity: 1/4,         // Opacity of the lines
      rotate: 0,            // Rotation offset
      direction: 1,         // 1: clockwise, -1: counterclockwise
      speed: 1,             // Rounds per second
      trail: 100,           // Afterglow percentage
      fps: 20,              // Frames per second when using setTimeout()
      zIndex: 2e9,          // Use a high z-index by default
      className: 'spinner', // CSS class to assign to the element
      top: '100px',           // center vertically
      left: '50%',          // center horizontally
      shadow: false,        // Whether to render a shadow
      hwaccel: false,       // Whether to use hardware acceleration (might be buggy)
      position: 'absolute'  // Element positioning
    };
    var target = document.getElementsByClassName('LoadingImg');
    //alert(target)
    //var spinner = new Spinner(opts).spin(target);
    var spinner = new Spinner().spin(target[0]);
    //$(function(){
    //    render_chart()
    //    });
    on_selecteditem_change()
})


function loading_begin(loading_message){
    $(".LoadingBg").height(document.body.clientWidth);
    $(".LoadingBg").show();
    $(".LoadingImg").fadeIn(300);
    $(".Loading_message").html("<p>"+loading_message+"</p>")
    $(".Loading_message").fadeIn(300)

}
function loading_end(){
    $('.LoadingBg, .LoadingImg, .Loading_message').hide();
}



function render_chart(datas){
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
                minRange:20*60*1000
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
                    data:datas[0]
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
                    data:datas[1]
                }]
        })
}

Date.prototype.pattern=function(fmt) {
    var o = {
    "M+" : this.getMonth()+1, //月份
    "d+" : this.getDate(), //日
    "h+" : this.getHours(), //小时
    "H+" : this.getHours(), //小时
    "m+" : this.getMinutes(), //分
    "s+" : this.getSeconds(), //秒
    "q+" : Math.floor((this.getMonth()+3)/3), //季度
    "S" : this.getMilliseconds() //毫秒
    };
    var week = {
    "0" : "/u65e5",
    "1" : "/u4e00",
    "2" : "/u4e8c",
    "3" : "/u4e09",
    "4" : "/u56db",
    "5" : "/u4e94",
    "6" : "/u516d"
    };
    if(/(y+)/.test(fmt)){
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    if(/(E+)/.test(fmt)){
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[this.getDay()+""]);
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(fmt)){
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
        }
    }
    return fmt;
}
