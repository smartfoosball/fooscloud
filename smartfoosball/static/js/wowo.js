// JavaScript Document
var viewModel = new Model();
var lineElementId ="#temp_wet_line";
var pages = {
	current_page : 0,
	prepage : function(openId,deviceId,method){
		this.current_page --;
		var historyJSON = {
			openId : openId,
			method : method,
			deviceId : deviceId,
			flag : this.current_page
		};
		$(".ajaxloading").show();
		$.post("WowoServlet",historyJSON,function(data){
			drawLine([ "00:00", "04:00", "08:00", "12:00", "16:00", "20:00" ],
					[ 26, 25, 22, 45, 26, 28 ], [ 75, 82, 78, 80, 50, 85 ],
					function(data) {
						lineDapte(lineElementId);
						drawingGraphs(lineElementId, data);
					});
			$(".dateTime").text(data.Date);
			$(".ajaxloading").hide();
		});
	},
	nextpage : function(openId,deviceId,method){
		if(this.current_page < 0){
			this.current_page ++;
			var historyJSON = {
				openId : openId,
				method : method,
				deviceId : deviceId,
				flag : this.current_page
			};
			$(".ajaxloading").show();
			$.post("WowoServlet",historyJSON,function(data){
				console.info(data);
				drawLine([ "00:00", "04:00", "08:00", "12:00", "16:00", "20:00" ],
						[ 26, 25, 12, 25, 26, 28 ], [ 75, 82, 78, 60, 90, 85 ],
						function(data) {
							lineDapte(lineElementId);
							drawingGraphs(lineElementId, data);
						});
				$(".dateTime").text(data.Date);
				$(".ajaxloading").hide();
			});
		}
	}
};

function setCommand1(air) {
	var cmd = 0;
	if(air){
		viewModel.petNest.air("true");
		viewModel.petNest.dehumidifier("false");
		cmd = 1;
	}else{
		viewModel.petNest.air("false");
		cmd = 0;
	}
	var json = {
		openId : $("#openId").val(),
		deviceId : $("#deviceId").val(),
		cmd : cmd
	};
	$.post("ControlServlet", json, function(data) {

	});
	console.info(cmd);
}
function setCommand2(dehumidifier) {
	var cmd = 0;
	if(dehumidifier){
		viewModel.petNest.dehumidifier("true");
		viewModel.petNest.air("false");
		cmd = 2;
	}else{
		viewModel.petNest.dehumidifier("false");
		cmd = 0;
	}
	var json = {
		openId : $("#openId").val(),
		deviceId : $("#deviceId").val(),
		cmd : cmd
	};
	$.post("ControlServlet", json, function(data) {

	});
	console.info(cmd);
}

$(document).ready(
		function(e) {
			var openId = $("#openId").val();
			var deviceId = $("#deviceId").val();
			var method = "history";
			ko.applyBindings(viewModel.petNest, document.getElementById('pet'));
			viewModel.loadpet();
			var historyJSON = {
				openId : openId,
				method : "history",
				deviceId : deviceId,
				flag : 0
			};
			$.post("WowoServlet",historyJSON,function(data){
				drawLine([ "00:00", "04:00", "08:00", "12:00", "16:00", "20:00" ],
						[ 26, 25, 22, 25, 26, 28 ], [ 75, 82, 78, 80, 90, 85 ],
						function(data) {
							lineDapte(lineElementId);
							drawingGraphs(lineElementId, data);
						});
				$(".dateTime").text(data.Date);
			});
			$(".sliderDown").click(function(e) {
				$(".box1").animate({
					top : "-100%"
				}, "slow");
				$(".box2").animate({
					top : "0"
				}, "slow");
			});
			$(".sliderUp").click(function(e) {
				$(".box2").animate({
					top : "100%"
				}, "slow");
				$(".box1").animate({
					top : "0"
				}, "slow");
			});
			$(".pre").click(function(){
				pages.prepage(openId,deviceId,method);
				
			});
			$(".next").click(function(){
				pages.nextpage(openId,deviceId,method);
			});
		});