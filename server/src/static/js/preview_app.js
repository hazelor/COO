/**
 * Created by guoxiao on 16/2/27.
 */
var sign
function on_selecteditem_change(){
    render_chart([[],[],[],[],[],[]], '目标浓度')
    var date = new Date()
    var end_time = date.pattern("yyyy-MM-dd hh:mm")
    var date_milliseconds = date.getTime()
    date_milliseconds -= 1000*60*59
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
        var historyDataRequest=$.ajax({
                url:'history/query',
                timeout:10000,
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
                        for(var i=0,len=jdata.length;i<len;i++){
                            if(jdata[i] == '')
                            {
                                jdata[i] = []
                            }
                        }
                        if($('#chamber_name').children('option:selected').attr('value').split(',')[1] == '5'){
                            render_chart(jdata, '测量浓度5min均值')
                        }
                        else{
                            render_chart(jdata, '目标浓度')
                        }
                        loading_end()
                    }

                },
                complete:function(XMLHttpRequest,status){
                    if(status=='timeout'){
                        historyDataRequest.abort();
                        loading_end();
                    }
                    else{
                        loading_end();
                    }
                }
                
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
                        if(data == ''){
                            data = ['', '']
                        }
                        var detail_data = data[0]
                        var plot_data = data[1]
                        if(plot_data != '')
                        {
                            var chart = $('#container_carbon').highcharts()
                            var series = chart.series
                            var serie_1_len = series[0].data.length
                            var serie_2_len = series[1].data.length
                            if(plot_data[0][0]!=''&&plot_data[0][1]!='')
                            { 
                                if(serie_1_len != 0){
                                    if(series[0].data[serie_1_len-1]['x'] != plot_data[0][0]){
                                        if(plot_data[0][0]-series[0].data[0]['x']>=60*60*1000){
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
                            }
                            if(plot_data[1][0]!=''&&plot_data[1][1]!='')
                            {
                                if(serie_2_len != 0){
                                    if(series[1].data[serie_2_len-1]['x'] != plot_data[1][0]){
                                        if(plot_data[1][0]-series[1].data[0]['x']>=60*60*1000){
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

                            chart = $('#container_humidity').highcharts()
                            series = chart.series
                            var serie_3_len = series[0].data.length
                            var serie_4_len = series[1].data.length
                            if(plot_data[2][0]!=''&&plot_data[2][1]!='')
                            {
                                if(serie_3_len != 0){
                                    if(series[0].data[serie_3_len-1]['x'] != plot_data[2][0]){
                                        if(plot_data[2][0]-series[0].data[0]['x']>=60*60*1000){
                                            series[0].addPoint(plot_data[2],true,true)
                                        }
                                        else{
                                            series[0].addPoint(plot_data[2],true,false)
                                        }
                                    }
                                }
                                else{
                                    series[0].addPoint(plot_data[2],true,false)
                                }
                            }
                            if(plot_data[3][0]!=''&&plot_data[3][1]!='')
                            {
                                if(serie_4_len != 0){
                                    if(series[1].data[serie_4_len-1]['x'] != plot_data[3][0]){
                                        if(plot_data[3][0]-series[1].data[0]['x']>=60*60*1000){
                                            series[1].addPoint(plot_data[3],true,true)
                                        }
                                        else{
                                            series[1].addPoint(plot_data[3],true,false)
                                        }
                                    }

                                }
                                else{
                                    series[1].addPoint(plot_data[3],true,false)
                                }
                            }

                            chart = $('#container_temperature').highcharts()
                            series = chart.series
                            var serie_5_len = series[0].data.length
                            var serie_6_len = series[1].data.length
                            if(plot_data[4][0]!=''&&plot_data[4][1]!='')
                            {
                                if(serie_5_len != 0){
                                    if(series[0].data[serie_5_len-1]['x'] != plot_data[4][0]){
                                        if(plot_data[4][0]-series[0].data[0]['x']>=60*60*1000){
                                            series[0].addPoint(plot_data[4],true,true)
                                        }
                                        else{
                                            series[0].addPoint(plot_data[4],true,false)
                                        }
                                    }
                                }
                                else{
                                    series[0].addPoint(plot_data[4],true,false)
                                }
                            }
                            if(plot_data[5][0]!=''&&plot_data[5][1]!='')
                            {
                                if(serie_6_len != 0){
                                    if(series[1].data[serie_6_len-1]['x'] != plot_data[5][0]){
                                        if(plot_data[5][0]-series[1].data[0]['x']>=60*60*1000){
                                            series[1].addPoint(plot_data[5],true,true)
                                        }
                                        else{
                                            series[1].addPoint(plot_data[5],true,false)
                                        }
                                    }

                                }
                                else{
                                    series[1].addPoint(plot_data[5],true,false)
                                }
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



function render_chart(datas, title){
    Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        $('#container_carbon').highcharts({
            chart: {

                type: 'spline',                      //曲线样式
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
            },
            title:{
                text:'CO2浓度'
            },

            xAxis: {
                type: 'datetime',
                minRange:60*60*1000
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
                    data:datas[0]
                },
                {
                    name: title,
                    data:datas[1]
                }]
        })


        $('#container_humidity').highcharts({
            chart: {

                type: 'spline',                      //曲线样式
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
            },
            title:{
                text:'湿度'
            },

            xAxis: {
                type: 'datetime',
                minRange:60*60*1000
                //minRange:60*1000

            },
            yAxis: {
                title: {
                    text: '%'
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
                    name: '空气湿度',
                    data:datas[2]
                },
                {
                    name: '土壤湿度',
                    data:datas[3]
                }]
        })


        $('#container_temperature').highcharts({
            chart: {

                type: 'spline',                      //曲线样式
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
            },
            title:{
                text:'温度'
            },

            xAxis: {
                type: 'datetime',
                minRange:60*60*1000
                //minRange:60*1000

            },
            yAxis: {
                title: {
                    text: '°C'
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
                    name: '空气温度',
                    data:datas[4]
                },
                {
                    name: '土壤温度',
                    data:datas[5]
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
