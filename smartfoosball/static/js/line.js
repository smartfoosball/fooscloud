// JavaScript Document
function drawingGraphs(ElementId, lineChartData) {
	// 曲线图参数设置
	var optionss = {
		// Boolean - If we show the scale above the chart data // 网格线是否在数据线的上面
		scaleOverlay : false,
		// Boolean - If we want to override with a hard coded scale //
		// 是否用硬编码重写y轴网格线线
		scaleOverride : false,

		// ** Required if scaleOverride is true **
		// Number - The number of steps in a hard coded scale // y轴刻度的个数
		scaleSteps : null,
		// Number - The value jump in the hard coded scale // y轴每个刻度的宽度
		scaleStepWidth : null,
		// Number - The scale starting value // y轴的起始值
		scaleStartValue : null,

		// String - Colour of the scale line // x轴y轴的颜色
		scaleLineColor : "rgba(255,255,255,1)",

		// Number - Pixel width of the scale line // x轴y轴的线宽
		scaleLineWidth : 1,

		// Boolean - Whether to show labels on the scale // 是否显示y轴的标签
		scaleShowLabels : false,

		// Interpolated JS string - can access value // 标签显示值
		scaleLabel : "<%=value%>",

		// String - Scale label font declaration for the scale label // 标签的字体
		scaleFontFamily : "'Arial'",

		// Number - Scale label font size in pixels // 标签字体的大小
		scaleFontSize : 12,

		// String - Scale label font weight style // 标签字体的样式
		scaleFontStyle : "normal",

		// String - Scale label font colour // 标签字体的颜色
		scaleFontColor : "#fff",

		// /Boolean - Whether grid lines are shown across the chart // 是否显示网格线
		scaleShowGridLines : false,

		// String - Colour of the grid lines // 网格线的颜色
		scaleGridLineColor : "rgba(0,0,0,.05)",

		// Number - Width of the grid lines // 网格线的线宽
		scaleGridLineWidth : 1,

		// Boolean - Whether the line is curved between points // 是否是曲线
		bezierCurve : false,

		// Boolean - Whether to show a dot for each point // 是否显示点
		pointDot : true,

		// Number - Radius of each point dot in pixels // 点的半径
		pointDotRadius : 12,

		// Number - Pixel width of point dot stroke // 数据线的线宽
		pointDotStrokeWidth : 3,

		// Boolean - Whether to show a stroke for datasets
		datasetStroke : true,

		// Number - Pixel width of dataset stroke
		datasetStrokeWidth : 16,

		// Boolean - Whether to fill the dataset with a colour // 数据线是否填充颜色
		datasetFill : false,

		// 是否填充数据
		dataset : true,

		// Boolean - Whether to animate the chart // 是否有动画效果
		animation : false,

		// Number - Number of animation steps // 动画的步数
		animationSteps : 60,

		// String - Animation easing effect // 动画的效果
		animationEasing : "easeOutQuart",

		// Function - Fires when the animation is complete // 动画完成后调用
		onAnimationComplete : null

	};
	var c = $(ElementId);
	var cxt = c.get(0).getContext("2d");
	return new Chart(cxt).Line(lineChartData, optionss);
}
function drawLine( xLabels, tempData, wetData, callback ){
	var tempDatad = new Array();
	var wetDatad = new Array();
	for (var i = 0; i < tempData.length; i++) {
		if (tempData[i] > 0) {
			tempDatad[i] = tempData[i];
		}
	}
	for (var i = 0; i < wetData.length; i++) {
		if (wetData[i] > 0) {
			wetDatad[i] = wetData[i];
		}
	}
	var lineChartData = {
		labels : xLabels,
		datasets : [{
			strokeColor : "rgba(255,152,153,1)",
			pointColor : "rgba(255,152,153,1)",
			pointStrokeColor : "#555",
			data : tempDatad,
			textColor : "rgba(255,152,153,1)",
			units : "℃"
		},{
			strokeColor : "rgba(102,203,255,1)",
			pointColor : "rgba(102,203,255,1)",
			pointStrokeColor : "#555",
			data : wetDatad,
			textColor : "rgba(102,203,255,1)",
			units : "%"
		}]
	};
	if( typeof(callback) != "undefined" ){
		callback(lineChartData);
	}
}
function lineDapte(elementId){
	$(elementId).attr("width","310");
	$(elementId).attr("height","260");
}