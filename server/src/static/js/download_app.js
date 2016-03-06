/**
 * Created by guoxiao on 16/2/27.
 */

var is_downloading = false;

function alert_if_downloading(){
    if(is_downloading)
    return '文件下载中,您确定要离开当前页面?'
}

function download_datas(){
    if(document.getElementById('start_time').value == ''){
        alert('请输入有效起始时间')
        return false
    }
    if(document.getElementById('end_time').value == ''){
        alert('请输入有效结束时间')
        return false
    }
    if(confirm('是否下载?')){
        is_downloading = true
        loading_begin('数据下载准备中')
        //loading_begin("下载准备中...")
        //alert('--------test--------')
        $.ajax({
            url:'/download',
            async: false,
            type:'get',
            data:{'is_file_download':true,
                  'start_time':document.getElementById('start_time').value,
                  'end_time':document.getElementById('end_time').value
                 },
            dataType:'text',
            success:function(data, status){
                if(data != ''){
                    var file_name = data

                    var href = '/static/download/'+file_name
                    //can_download = true
                    document.getElementById('download_link').href = href;
                    document.getElementById('download_link').download = file_name;
                    loading_end()
                    is_downloading = false
                    return true
                }
                else{
                    alert('获取数据失败!')
                    document.getElementById('download_link').href = ''
                    document.getElementById('download_link').download = ''
                    loading_end()
                    is_downloading = false
                    return false
                }
            },
            error:function(){
                    alert('获取数据失败!')
                    document.getElementById('download_link').href = ''
                    document.getElementById('download_link').download = ''
                    loading_end()
                    is_downloading = false
                    return false
            }
        })
    }
    else{
        //alert('获取数据失败!')
        document.getElementById('download_link').href = ''
        document.getElementById('download_link').download = ''
        return false
    }

}


Date.prototype.pattern=function(fmt) {
    var o = {
    "M+" : this.getMonth()+1, //月份
    "d+" : this.getDate(), //日
    "h+" : this.getHours()%12 == 0 ? 12 : this.getHours()%12, //小时
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

    //$(".LoadingBg").height(document.body.clientWidth);
    //$(".LoadingBg").show();
    //$(".LoadingImg").fadeIn(300);
    //$(".Loading_message").html("<p>"+'--------test--------'+"</p>")
    //$(".Loading_message").fadeIn(300)
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
