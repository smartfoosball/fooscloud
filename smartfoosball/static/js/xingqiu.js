// JavaScript Document
var viewModel = new Model();
var lineElementId = "#temp_wet_line";
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
function drawLineData(openId,deviceId){
	console.info("openId:"+openId);
	console.info("deviceId:"+deviceId);
	pages.current_page = 0;
	var historyJSON = {
			openId : openId,
			method : "history",
			deviceId : deviceId
		};
	$(".ajaxloading").show();
	$.post("WowoServlet",historyJSON,function(data){
		drawLine([ "00:00", "04:00", "08:00", "12:00", "16:00", "20:00" ],
				[ 26, 25, 12, 25, 26, 28 ], [ 75, 82, 78, 60, 90, 85 ],
				function(data) {
					lineDapte(lineElementId);
					drawingGraphs(lineElementId, data);
					$(".ajaxloading").hide();
					$(".box1").animate({
						left : "-100%"
					}, "slow");
					$(".box3").animate({
						left : "0"
					}, "slow");
				});
		$(".dateTime").text(data.Date);
	});
}
$(document).ready(
		function(e) {
			ko.applyBindings(viewModel.petNest, document.getElementById('petList'));
			viewModel.petNest.petList(device);
			var openId = device[0].openId;
			var deviceId =  device[0].deviceId;
			$(".invitation").click(function(e) {
				window.location.href = "/Gokitdog/JionServlet?method=jion&openId="+ device[0].openId +"&groupId=" + $("#groupId").val();
			});
			$(".sliderUp").click(function(){
				$(".box1").animate({
					left : "0"
				}, "slow");
				$(".box3").animate({
					left : "100%"
				}, "slow");
			});
			$(".pre").click(function(){
				pages.prepage(openId,deviceId,"history");
			});
			$(".next").click(function(){
				pages.nextpage(openId,deviceId,"history");
			});
			
		});
