Chart.defaults.global.defaultFontColor='white'; // Sets the default font color to white

// These variables will hold the Chart objects
var avgChart;
var countChart;

// Chart contexts variables
var avgContext;
var countContext;

// Default bar chart settings
var defaultBar = {
		type: 'horizontalBar',
//		data: {
//			labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"], Sets the labels of x-axis
//			datasets: [{
//				label: 'Average Movies Per Genre', Set the title
//				data: [12, 19, 3, 5, 2, 3],
//				backgroundColor: [
//					'rgba(255, 99, 132, 0.2)',
//					'rgba(54, 162, 235, 0.2)',
//					'rgba(255, 206, 86, 0.2)',
//					'rgba(75, 192, 192, 0.2)',
//					'rgba(153, 102, 255, 0.2)',
//					'rgba(255, 159, 64, 0.2)'
//				],
//				borderColor: [
//					'rgba(255,99,132,1)',
//					'rgba(54, 162, 235, 1)',
//					'rgba(255, 206, 86, 1)',
//					'rgba(75, 192, 192, 1)',
//					'rgba(153, 102, 255, 1)',
//					'rgba(255, 159, 64, 1)'
//				],
//				borderWidth: 1
//			}]
//		},
		options: {
			scales: {
				xAxes: [{
					ticks: {
						beginAtZero:true
					}
				}]
			},
			title: {
	            display: true,
//	            text: 'A title'
	        },
	        legend: {
	            display: false
	        }
		}
	};

$(document).ready(function() {
	avgContext = document.getElementById("avgChart").getContext('2d');
	countContext = document.getElementById("countChart").getContext('2d');
	chartNoFilter();
});

function chartNoFilter() {
	// REST call for count of movies per genre
	$.ajax({
		url: "/count", 
		dataType: "json",
		type: "GET",
		success: function(result){
			var label = [];
			var data = [];
			var charOp = JSON.parse(JSON.stringify(defaultBar)); // Copy template
			
			for(var i = 0; i < result.length; i++){
				label.push(result[i].name);
				data.push(result[i].moviecount);
			}
			
			var dataset = {
				labels: label,
				datasets: [{
					data: data,
					backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red
					borderColor: 'rgba(255,99,132,1)',
					borderWidth: 1
				}]
			};
			
			charOp.data = dataset;
			charOp.options.title.text = "Number of Movies Per Genre";
			charOp.options.tooltips = {
					callbacks: {
						label: function(tooltipItems, data) { 
	                        return 'Count : ' + tooltipItems.xLabel;
						}
					}
			}
            
			// Render the chart
			countChart = new Chart(countContext, charOp);
		}
	});
	
	// REST call for average movie rating per genre
	$.ajax({
		url: "/average", 
		dataType: "json",
		type: "GET",
		success: function(result){
			var label = [];
			var data = [];
			var charOp = JSON.parse(JSON.stringify(defaultBar)); // Copy default template
			
			for(var i = 0; i < result.length; i++){
				label.push(result[i].name);
				data.push(result[i].rating.toFixed(2));
			}
			
			var dataset = {
				labels: label,
				datasets: [{
					data: data,
					backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue
					borderColor: 'rgba(54, 162, 235, 1)',
					borderWidth: 1
				}]
			};
			
			charOp.data = dataset;
			
			// Set the title
			charOp.options.title.text = "Average Rating Per Movie";
			
			// Set the tooltip template of the chart
			charOp.options.tooltips = {
					callbacks: {
						label: function(tooltipItems, data) { 
	                        return 'Average : ' + tooltipItems.xLabel;
						}
					}
			}
			
			// Render the chart
			avgChart = new Chart(avgContext, charOp);
		}
	});
}

function destroyAllCharts() {
	avgChart.destroy();
	countChart.destroy();
}
