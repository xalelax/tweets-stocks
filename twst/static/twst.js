google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function floorDate(datetime) {
    var newDate = new Date(datetime);
    newDate.setHours(0);
    newDate.setMinutes(0);
    newDate.setSeconds(0);
    return newDate;
}

function drawChart() {

    var symbol = document.getElementById("symbol").value;
    var word = document.getElementById("word").value;

    symbol = (symbol === "") ? "GOOG" : symbol
    word = (word === "") ? "Quantum" : word

    url = '/data/'+symbol+'/'+word

    var jsonData = $.ajax({
        url,
        dataType: "json",
        async: false // TODO: async later
    }).responseJSON;

    console.log(jsonData);
    if ('error' in jsonData) {
	window.alert(jsonData.error);
	return
    }

    var stockDataRaw = jsonData.stock_data;
    var tweets = jsonData.tweets;

    // Create the stock data table.
    var stockData = new google.visualization.DataTable();
    stockData.addColumn('date', 'Date');
    stockData.addColumn('number', 'Low');
    stockData.addColumn('number', 'Open');
    stockData.addColumn('number', 'Close');
    stockData.addColumn('number', 'High');

    for(i = 0; i < stockDataRaw.t.length; i++)
        stockData.addRow([
	    floorDate(stockDataRaw.t[i]),
	    stockDataRaw.l[i],
	    stockDataRaw.o[i],
	    stockDataRaw.c[i],
	    stockDataRaw.h[i]])

    // Create tweets data table
    var twitterData = new google.visualization.DataTable();
    twitterData.addColumn('date', 'Date');
    twitterData.addColumn('number', 'Retweet Count');
    twitterData.addColumn({type: 'string', role: 'tooltip'});

    for(i = 0; i < tweets.length; i++) {
	tweet = tweets[i];
	tweetInfos = '@' + tweet.author + ': ' + tweet.text;
	twitterData.addRow([
	    floorDate(tweet.created_at),
	    tweet.retweet_count,
	    tweetInfos]);
    }

    twitterData.sort([{column: 0}]);

    var joinedData = google.visualization.data.join(
	stockData, twitterData, 'full', [[0, 0]], [1,2,3,4], [1,2]);

    // Set chart options
    var options = {title: symbol + ' price and ' + word + ' tweets',
		   candlestick: {
		       fallingColor: { strokeWidth: 0, fill: '#a52714' }, // red
		       risingColor: { strokeWidth: 0, fill: '#0f9d58' }   // green
		   },
		   tooltip: {ignoreBounds: true},
		   seriesType: 'candlesticks',
		   isStacked: true,
		   series: {
		       0: {labelInLegend: symbol},
		       1: {type: 'scatter',
			   labelInLegend: 'Tweets',
			   targetAxisIndex: 1,
			   pointShape: {type: 'star'},
			   pointSize: 10
			  }
		   },
		   vAxes: {
		       0: {title: 'Price (Arbitrary units)'},
		       1: {title: 'Retweet count',
			   scaleType: 'log'}
		   }
		  };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
    chart.draw(joinedData, options);
}
