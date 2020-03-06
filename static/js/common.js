function isFunc(func){
	return func!=undefined && typeof(func)=="function";
}

function addTab(title, url) {
	if ($("#workCenter").tabs("exists", title)) {
		$("#workCenter").tabs("select", title);
		return;
	}
	var height = parseInt($("#workCenter").parent().css("height")) - 35;
	var width = parseInt($("#workCenter").parent().css("width")) - 12;
	var content = "<iframe src='"+url+"' width='"+width+"' height='"+height+"px' frameborder='0'></iframe>";
	$("#workCenter").tabs("add", {
		title : title,
		closable : true,
		content : content
	});
}

/**
 * 打开window组件
 * @param exp jquery选择器
 * @param initFunc 在开始窗口前的初始化函数，可选
 */
function openWin(exp,initFunc){
	if(isFunc(initFunc)){
		initFunc();
	}
	$(exp).window("open");
}

function closeWin(exp,destoryFunc){
	$(exp).window("close");
	if(isFunc(destoryFunc)){
		destoryFunc();
	}
}

/**
 * eaysui ajax form的通用函数
 * @param exp jquery选择器
 * @param url 表单提交的URL
 * @param callback 回调函数，会传作为data参数
 */
function ajax_form(exp,url,callback){
	$(exp).form('submit',{
		url:url,
		success:function(data){
			if(isFunc(callback)){
				callback(data);			
			}
		},
		onLoadError:function(){
			$.messager.alert("load form error!");	
		}
	});
}

/**
 * easyui datagird批量删除通用函数
 * @param url 提交的URL
 * @param exp jquery选择器
 * @param paramName 提交的参数名
 * @param field easyui datagrid的row中的字段名
 * @param callback 回调函数
 */
function gridDelete(url,exp,paramName,field,callback){
	var rows = $(exp).datagrid("getSelections");
	if(rows.length==0){
		$.messager.alert("消息","请选择需要操作的数据。");
		return;
	}
	$.messager.confirm("提示","批量操作请谨慎！",function(r){
		if(r){
			var params = "";
			for(var i=0;i<rows.length;i++) {
				params += paramName+"="+encodeURIComponent(rows[i][field])+"&";
			}
			if(url.indexOf("?")==-1) {
				url += "?"+params;
			}else{
				url += "&"+params;
			}
			$.get(url,function(data,stauts){
				if(isFunc(callback)){
					callback(data);
				}
			});
		}
	});
}

function gridDeleteWidthParams(url,exp,params,callback){
	var rows = $(exp).datagrid("getSelections");
	if(rows.length==0){
		$.messager.alert("消息","请选择需要操作的数据。");
		return;
	}
	$.messager.confirm("提示","批量操作请谨慎！",function(r){
		if(r){
			if(url.indexOf("?")==-1) {
				url += "?"+params;
			}else{
				url += "&"+params;
			}
			$.get(url,function(data,stauts){
				if(isFunc(callback)){
					callback(data);
				}
			});
		}
	});
}

/**
 * easyui validate type，该规则为只限定 数字、字母、下划线，并且以字母开头
 */
$.extend($.fn.validatebox.defaults.rules, {
    enLeter: {
        validator: function(value, param){
        	var reg = new RegExp("[A-Za-z]\\w*");
            return reg.test(value);
        },
        message: '该字段只能包含字母、数字、下线线并以字母开头.'
    }
});

/**
 * easyui validate type，该规则为只限定数字
 */
$.extend($.fn.validatebox.defaults.rules, {
    number: {
        validator: function(value, param){
        	var reg = new RegExp("\\d+");
            return reg.test(value);
        },
        message: '该字段只能为数字'
    }
});