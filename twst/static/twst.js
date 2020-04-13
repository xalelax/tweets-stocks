google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);


function floorDate(datetime) {

    var newDate = new Date(datetime);

    newDate.setHours(0);
    newDate.setMinutes(0);
    newDate.setSeconds(0);

    return newDate;

}


function buildStockDataTable(rawData) {

    var stockDataRaw = rawData.stock_data;

    // Define skeleton of stock DataTable.
    var stockData = new google.visualization.DataTable();
    stockData.addColumn('date', 'Date');
    stockData.addColumn('number', 'Low');
    stockData.addColumn('number', 'Open');
    stockData.addColumn('number', 'Close');
    stockData.addColumn('number', 'High');

    // Populate it
    for(i = 0; i < stockDataRaw.t.length; i++)
        stockData.addRow([
	    floorDate(stockDataRaw.t[i]),
	    stockDataRaw.l[i],
	    stockDataRaw.o[i],
	    stockDataRaw.c[i],
	    stockDataRaw.h[i]]);

    return stockData;
}


function buildTwitterDataTable(rawData) {

    var tweets = rawData.tweets;

    // Create skeleton of tweets data table
    var twitterData = new google.visualization.DataTable();
    twitterData.addColumn('date', 'Date');
    twitterData.addColumn('number', 'Retweet Count');
    twitterData.addColumn({type: 'string', role: 'tooltip'});

    // Populate it
    for(i = 0; i < tweets.length; i++) {
	tweet = tweets[i];
	tweetInfos = '@' + tweet.author + ': ' + tweet.text;
	twitterData.addRow([
	    floorDate(tweet.created_at),
	    tweet.retweet_count,
	    tweetInfos]);
    };

    return twitterData;

}


function getRawData(symbol, word) {

    url = '/data/'+symbol+'/'+word;

    var response = $.ajax({url,
			   dataType: "json",
			   async: false // TODO: async later
			  }).responseJSON;

    return response;

}


var chartOptions = {titlePosition: 'none',
		    height: 400,
		    candlestick: {
			fallingColor: { stroke: "#03000d", fill: '#a52714' }, // red
			risingColor: { stroke: "#03000d", fill: '#0f9d58' }   // green
		    },
		    backgroundColor: "#fcf8f0",
		    tooltip: {isHtml: true},
		    seriesType: 'candlesticks',
		    isStacked: true,
		    legend: 'none',
		    series: {
			0: {labelInLegend: symbol},
			1: {type: 'scatter',
			    labelInLegend: 'Tweets',
			    targetAxisIndex: 1,
			    pointShape: {type: 'star'},
			    pointSize: 30,
			    color: "#00acee"
			   }
		    },
		    vAxes: {
			0: {title: 'Price (Arbitrary units)'},
			1: {title: 'Retweet count',
			    scaleType: 'log'}
		    }
		   };


function drawChart() {
    
    var symbol = document.getElementById("symbol").value;
    var word = document.getElementById("word").value;

    symbol = (symbol === "") ? "GOOG" : symbol
    word = (word === "") ? "Quantum" : word

    data = getRawData(symbol, word);

    if ('error' in data) {
	window.alert(data.error);
	return
    }

    stockData = buildStockDataTable(data)
    twitterData = buildTwitterDataTable(data)

    twitterData.sort([{column: 0}]);

    var joinedData = google.visualization.data.join(
	stockData, twitterData, 'full', [[0, 0]], [1,2,3,4], [1,2]);

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
    chart.draw(joinedData, chartOptions);
}
