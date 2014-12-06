// JavaScript Document
var Model = function(){
	this.petNest = {
		tips : ko.observable(),
		temp : ko.observable(),
		wet : ko.observable(),
		tempComfort : ko.observable(),
		wetComfort : ko.observable(),
		air : ko.observable(),
		dehumidifier : ko.observable(),
		petList : ko.observableArray(),
		tempData : ko.observable(),
		wetData : ko.observable()
	};
};
Model.prototype = {
	loadpet : function(){
		var self = this;
		self.petNest.tips($("#tips").val());
		self.petNest.temp($("#temp").val() + "℃");
		self.petNest.wet($("#humidity").val() + "%");
		self.petNest.tempComfort($("#tempComfort").val());
		self.petNest.wetComfort($("#wetComfort").val());
		self.petNest.air($("#air").val());
		self.petNest.dehumidifier($("#dehumidifier").val());
	},
	loadpetlist : function(openId){
		var self = this;
		$.getJSON("json/pet.json",function(data){
			self.petNest.petList(data.petList);
		});
	}
};