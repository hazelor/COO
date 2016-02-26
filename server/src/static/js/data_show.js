/**
 * Created by guoxiao on 16/2/26.
 */

$(function () {                                          //当文件加载完毕执行
    $(document).ready(function () {
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
                events: {
                    load: function () {

                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function () {                            //setInterval定时器
                            var x = (new Date()).getTime(), // current time
                                y = Math.random();
                            series.addPoint([x, y], true, true);
                        }, 1000);
                    }
                }
            },

            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150

            },
            yAxis: {
                title: {
                    text: '二氧化碳浓度'
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
                    name: '目标浓度',
                    data: (function () {
                        // generate an array of random data
                        var data = [],
                            time = (new Date()).getTime(),
                            i;

                        for (i = -19; i <= 0; i += 1) {
                            data.push({
                                x: time + i * 1000,
                                y: Math.random()
                            });
                        }
                        return data;
                    }())
                },
                {
                    name: '测量浓度',
                    data: (function () {
                        // generate an array of random data
                        var data = [],
                            time = (new Date()).getTime(),
                            i;

                        for (i = -19; i <= 0; i += 1) {
                            data.push({
                                x: time + i * 1000,
                                y: Math.random()
                            });
                        }
                        return data;
                    }())
                }]
        });
    });
});
