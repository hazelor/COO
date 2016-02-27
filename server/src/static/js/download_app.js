/**
 * Created by guoxiao on 16/2/27.
 */

var is_downloading = false;

function alert_if_downloading(){
    if(is_downloading)
    return '文件下载中,您确定要离开当前页面?'
}

function download_datas(){
    if(confirm('是否下载?')){
        is_downloading = true
        loading_begin("下载准备中...")
        $.ajax({
            url:'/download',
            async: false,
            type:'get',
            data:{'is_file_download': true },
            dataType:'text',
            success:function(data, status){
                if(data != ''){
                    var file_name = data
                    var href = '/static/download/'+file_name
                    //can_download = true
                    document.getElementById('download_link').href = href
                    document.getElementById('download_link').download = file_name
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