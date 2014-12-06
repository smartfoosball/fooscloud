// JavaScript Document
$(document).ready(function(e) {
	var openId = $("#openId").val();
	var groupId = null;
	$(".createBtn").click(function(e) {
		var groupName = $(".name_input").val();
		if( groupName == ""){
			alert("名字不能为空哦！");
			return false;
		}
		var json = {
			openId : openId,
			groupName : groupName
		};
		$(".ajaxloading").show();
		$.post("CreateServlet",json,function(data){
				groupId = data;
				$(".createname").text(groupName);
				$(".ajaxloading").hide();
				$(".box1").animate({
					left : "-100%"
				}, "slow");
				$(".box2").animate({
					left : "0"
				}, "slow");
		});
	});
	$(".invitation").click(function(e) {
		window.location.href = "/Gokitdog/JionServlet?method=jion&openId="+ openId +"&groupId=" + groupId;
	});
});