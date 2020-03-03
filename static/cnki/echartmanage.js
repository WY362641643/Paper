// JavaScript Document


function processValueShort(params){
	if(params != null && params.length>0){
		if(params == "青龙满族自治县"){
			params = "青龙县";
		}
		if(params == "丰宁满族自治县"){
			params = "丰宁县";
		}
		if(params == "宽城满族自治县"){
			params = "宽城县";
		}
		if(params == "围场满族蒙古族自治县"){
			params = "围场县";
		}
		if(params == "孟村回族自治县"){
			params = "孟村县";
		}
		if(params == "大厂回族自治县"){
			params = "大厂自治县";
		}
	}	
	var newParamsName = "";// 最终拼接成的字符串
	var paramsNameNumber = params.length;// 实际标签的个数
	var provideNumber = 0;
	if(paramsNameNumber > 9){
		 provideNumber = 2;// 每行能显示的字的个数
	}else if(paramsNameNumber>7){
	      provideNumber = 3;// 每行能显示的字的个数
	}else{
	      provideNumber = 2;// 每行能显示的字的个数
	}
	var rowNumber = Math.ceil(paramsNameNumber / provideNumber);// 换行的话，需要显示几行，向上取整
	/**
	 * 判断标签的个数是否大于规定的个数， 如果大于，则进行换行处理 如果不大于，即等于或小于，就返回原标签
	 */
	// 条件等同于rowNumber>1
	if (paramsNameNumber > 4) {
	    /** 循环每一行,p表示行 */
	    for (var p = 0; p < rowNumber; p++) {
	        var tempStr = "";// 表示每一次截取的字符串
	        var start = p * provideNumber;// 开始截取的位置
	        var end = start + provideNumber;// 结束截取的位置
	        // 此处特殊处理最后一行的索引值
	        if (p == rowNumber - 1) {
	            // 最后一次不换行
	            tempStr = params.substring(start, paramsNameNumber);
	        } else {
	            // 每一次拼接字符串并换行
	            tempStr = params.substring(start, end) + "\n";
	        }
	        newParamsName += tempStr;// 最终拼成的字符串
	    }
	} else {
	      newParamsName = params.split("").join("\n");
	}
	return newParamsName;
}

function processValueLong(params){
	var newParamsName = "";// 最终拼接成的字符串
	var paramsNameNumber = params.length;// 实际标签的个数
	var provideNumber = 0;
	if(paramsNameNumber==3){
	      provideNumber = 2;// 每行能显示的字的个数
	}else if(paramsNameNumber>4&&paramsNameNumber<=7){
	      provideNumber = 4;// 每行能显示的字的个数
	}else if(paramsNameNumber>7){
		provideNumber = 4;
	}
	var rowNumber = Math.ceil(paramsNameNumber / provideNumber);// 换行的话，需要显示几行，向上取整
	/**
	 * 判断标签的个数是否大于规定的个数， 如果大于，则进行换行处理 如果不大于，即等于或小于，就返回原标签
	 */
	// 条件等同于rowNumber>1
	 if (paramsNameNumber > 3) { 
	    /** 循环每一行,p表示行 */
	    for (var p = 0; p < rowNumber; p++) {
	        var tempStr = "";// 表示每一次截取的字符串
	        var start = p * provideNumber;// 开始截取的位置
	        var end = start + provideNumber;// 结束截取的位置
	        // 此处特殊处理最后一行的索引值
	        if (p == rowNumber - 1) {
	            // 最后一次不换行
	            tempStr = params.substring(start, paramsNameNumber);
	        } else {
	            // 每一次拼接字符串并换行
	            tempStr = params.substring(start, end) + "\n";
	        }
	        newParamsName += tempStr;// 最终拼成的字符串
	    }
	    } else {
	     // newParamsName = params.split("").join("\n");
	      newParamsName = params;
	} 
	return newParamsName;
}

// 判断myChart是否已存在
function judgeEchart(myChart){
	if (myChart != null && myChart != "" && myChart != undefined) {
        myChart.dispose();
	}
}