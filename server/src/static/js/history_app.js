/**
 * Created by guoxiao on 16/2/27.
 */

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




window.onload=function(){
    var date = new Date()
    document.getElementById('end_time').value = date.pattern("yyyy-MM-dd hh:mm")
    var date_milliseconds = date.getTime()
    date_milliseconds -= 1000*60*60*24
    date = new Date(date_milliseconds)
    document.getElementById('start_time').value = date.pattern("yyyy-MM-dd hh:mm")



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
}

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



function render_chart(title1, data1, title2, data2){
    $('#container').highcharts({                   //图表展示容器，与div的id保持一致
        chart: {
            type: 'line',                         //指定图表的类型，默认是折线图（line）
            zoomType: 'x',
        },
        title:{
            text: '历史数据'
        },
        xAxis: {
            type: 'datetime',
            },
        yAxis: {
            title: {
                text: ''                  //指定y轴的标题
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
            name: title1,                          //数据列名
            data: data1                              //数据
        },
        {
            name: title2,
            data: data2
        }]
    });
}


$(function(){
    render_chart('',[],'',[])
        });


function selected_history(){
    //alert(document.getElementById('start_time').value)
    var start_time_str = document.getElementById('start_time').value;
    if(start_time_str == ''){
        alert('请输入有效起始时间')
        return
    }
    var end_time_str = document.getElementById('end_time').value;
    if(end_time_str == ''){
        alert('请输入有效结束时间')
        return
    }
    var start_str = (start_time_str+":00").replace(/-/g,"/")
    var start_date = new Date(start_str)
    var end_str = (end_time_str+":00").replace(/-/g,"/")
    var end_date = new Date(end_str)
    if(end_date-start_date>86400000){
//        alert(end_date-start_date)
        alert('所选时间间隔大于24小时!')
        return
    }
    var count = Math.floor((end_date-start_date)/2880000)
    //alert($('#data_name').children('option:selected').attr('value'))
    //var start_time = new Date(Date.parse(start_time_str.replace(/-/g, "/")));
    //var end_time = new Date(Date.parse(end_time_str.replace(/-/g, "/")));
    //var interval = (end_time.getTime()-start_time.getTime());
    var data_name1 = $('#data_name').children('option:selected').text();
    var data_name2 = ''
    if(data_name1 == '测量浓度'){
        data_name2 = '目标浓度'
    }
    loading_begin('数据准备中')
    //alert('--------test--------')
    var historyDataRequest=$.ajax({
        url:'history/query',
        timeout:30000,
        type:'GET',
        dataType:'text',
        data:{'mac_address':$('#chamber_name').children('option:selected').attr('value').split(',')[0],
              'position':$('#chamber_name').children('option:selected').attr('value').split(',')[1],
              'type':$('#data_name').children('option:selected').attr('value'),
              'start_time':document.getElementById('start_time').value,
              'end_time':document.getElementById('end_time').value
              },
        success:function(data, status){
            if(data==''){
                alert('所选择的时间段没有数据!')
                loading_end()
                return
            }
//            if(data=='N'){
//                alert('所选时间间隔大于24小时!')
//                loading_end()
//                return
//            }
            else{
                var jdata= $.parseJSON(data)
                if(jdata[0] == '' && jdata[1] == ''){
                    alert('所选择的时间段没有数据!')
                    loading_end()
                    return
                }
                else{
                    var data1 = new Array()
                    var data2 = new Array()
                    if(jdata[0] == ''){
//                        jdata[0] = new Array()
                    }
                    else{
                        for (var i=0;i<jdata[0].length;i++){
                            if(i%count==0){
                                data1.push(jdata[0][i])
                            }                 
                        }
                    }
                    if(jdata[1] == ''){
//                        jdata[1] = new Array()
                        data_name2 = ''
                    }
                    else{
                        for (var i=0;i<jdata[1].length;i++){
                            if(i%count==0){
                                data2.push(jdata[1][i])
                            }
                        }
                    }
                    render_chart(data_name1, data1, data_name2, data2)
                    loading_end()
                }
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
}


function chamber_changed(){
    var current_chamber_key = document.getElementById("chamber_name").value;
    $.ajax({
        url:'/history',
        type:'get',
        data:{'current_chamber_key': current_chamber_key},
        success:function(data, status){
            data_list = JSON.parse(data)
            $("#data_name option").remove();
            for(i=0;i<data_list.length;i++){
                //alert("<option value="+"'"+data_list[i][0]+"'"+">"+data_list[i][1]+"</option>")
                $("#data_name").append("<option value="+data_list[i][0]+">"+data_list[i][1]+"</option>");
            }
            //$.each(data_list, function(item){
            //    $("#data_name").append("<option value="+item[0]+">"+item[1]+"</option>");
            //});
        }
    })
}

