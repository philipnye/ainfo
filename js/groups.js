if (window.location.href.split('/')[2]=='127.0.0.1:8000'){
	var group_code=window.location.href.split('/')[4]
}
else if (window.location.href.split('/')[2]=='philipnye.github.io') {		// XXX Will need updating if URL structure changes
	var group_code=window.location.href.split('/')[5]
}

var growthChartData,
	groupTickInterval

$(function () {
	function initialiseTooltips() {
		$('[data-toggle="tooltip"]').tooltip()
	}

	function drawGrowthChart() {
		Highcharts.chart('growth-chart', {
			chart: {
				type: 'line'
			},
		    legend: {
				enabled: false
			},
			series: [{
		        data: growthChartData,
		        step: 'left'
		    }],
			title: {
		        text: null
		    },
			tooltip: {
				formatter: function () {
		            return this.key + '<br>' + this.y;
		        }
			},
			xAxis: {
				tickInterval: groupTickInterval,
				tickWidth: 1,
				type: 'category'
			},
			yAxis: {
				allowDecimals: false,
				min: 0,
				title: {
					text: 'Schools'
				}
			}
		});
	}

var tabs = document.getElementsByClassName("tabbed-content")[0].getElementsByClassName("nav-link")
var tabsObj = {}

for (let tab of tabs) {
	tabsObj[tab.hash]=tab.textContent
}

$('.tabbed-content a').on('click', function (e) {
	for (let tab of tabs) {
		if ($(this)[0].hash!=tab.hash) {
			tab.textContent='...'
		}
	}
	$(this)[0].textContent=tabsObj[$(this)[0].hash]
})

	function setValuesAndTooltips(json) {
	    let len=json.length
	    if (len>0) {
	    	for (let i=0; i<len; i++) {
	        	var line=json.shift()
	        	if (line.group_code==group_code){
					var key=Math.max.apply(null,Object.keys(line.school_count_ts))
					document.getElementById('group-name').innerHTML=line.group_name
					document.getElementById('group-description').innerHTML=line.description
					if (line.school_count_ts[key]==1) {
						document.getElementById('acadCount').innerHTML=line.school_count_ts[key].toLocaleString('en', {useGrouping:true})+' '+document.getElementById('acadCount').innerHTML
					}
					else {
						document.getElementById('acadCount').innerHTML=line.school_count_ts[key].toLocaleString('en', {useGrouping:true})+' academies'
					}
					document.getElementById('sponAcadCount').innerHTML=line.estab_type_count.sponsored_academy.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('sponAcadCount').innerHTML
					document.getElementById('convAcadCount').innerHTML=line.estab_type_count.converter_academy.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('convAcadCount').innerHTML
					document.getElementById('fsCount').innerHTML=line.estab_type_count.free_school.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('fsCount').innerHTML
					document.getElementById('utcssCount').innerHTML=line.estab_type_count.utc_studio_school.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('utcssCount').innerHTML
					document.getElementById('primCount').innerHTML=line.estab_phase_count.primary.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('primCount').innerHTML
					document.getElementById('secCount').innerHTML=line.estab_phase_count.secondary.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('secCount').innerHTML
					document.getElementById('thruCount').innerHTML=line.estab_phase_count.all_through.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('thruCount').innerHTML
					document.getElementById('apCount').innerHTML=line.estab_phase_count.alternative_provision.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('apCount').innerHTML
					document.getElementById('specCount').innerHTML=line.estab_phase_count.special.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('specCount').innerHTML
					document.getElementById('post16Count').innerHTML=line.estab_phase_count.post_16.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('post16Count').innerHTML
					var regionsCount = 0;
					for (var j = 0; j < Object.keys(line.region_count).length; ++j) {
					    if (Object.values(line.region_count)[j] > 0) {
					        regionsCount++;
						}
					}
					document.getElementById('regionsCount').innerHTML=regionsCount.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('regionsCount').innerHTML
					if (regionsCount>1) {
						document.getElementById('regionsCount').innerHTML=document.getElementById('regionsCount').innerHTML + 's'
					}
					document.getElementById('pupsCount').innerHTML=line.pupil_numbers.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('pupsCount').innerHTML
					if (line.no_pupil_numbers_schools>0){
						var tooltipText='Pupil numbers are only available for ' + line.pupil_numbers_schools + ' out of ' + line.school_count_ts[key] +' schools'
						document.getElementById('pupsCount').innerHTML=document.getElementById('pupsCount').innerHTML + '<sup><i class="fas fa-exclamation-circle" data-toggle="tooltip" title="' + tooltipText + '"></i></sup>'
					}

					growthChartData=Object.keys(line.school_count_ts).map(function(key) {		// convert key-value pairs object to array of arrays, as required by Highcharts, and using integers rather than strings
  						return [Number(key), line.school_count_ts[key]];
					});
					for (i in growthChartData) {
						var yearPart=growthChartData[i][0].toString().substring(0,4)
						var monthPart=growthChartData[i][0].toString().substring(4,6)
						var date = "01/" + monthPart + "/"  + yearPart
						growthChartData[i]=[date, growthChartData[i][1]]
					}
					groupTickInterval=growthChartData.length-1

					break

				}
			}
		}
		initialiseTooltips()
		drawGrowthChart()
	}

	$.getJSON('../../data/groups_demo.json', setValuesAndTooltips)		// async callback

	$('#schoolsTable').DataTable({
		ajax: {
		  url: '../../data/schools.json',		// NB: non-demo version doesn't containt school_count_ts
		  dataSrc: function (json) {
		    let data=[]
		    let len=json.length
		    if(len>0){
		      for(let i=0; i<len; i++){
		        var line=json.shift()
		        if (line.group_code==group_code){
		          data.push(line)
		        }
		      }
		    }
		  	return data;
		  }
		},
		dom: '<"tableTop"f>t<"tableBottom"ilp>',
	    deferRender: true,
	    columns: [{
	        data: "urn",
	        orderSequence: ["asc", "desc"]
		},
		{
			data: "laestab",
			orderSequence: ["desc", "asc"]
		},
		{
			data: "estab_name",
			orderSequence: ["desc", "asc"]
		},
		{
			data: "estab_phase",
			orderSequence: ["desc", "asc"]
		},
		{
			data: "estab_type",
			orderSequence: ["desc", "asc"]
		},
		{
			data: "la",
			orderSequence: ["desc", "asc"]
		},
		{
			data: "region",
			orderSequence: ["desc", "asc"]
		},
		{
			data: "open_date",
			render: $.fn.dataTable.render.moment('DD-MM-YYYY','DD/MM/YY'),
			orderSequence: ["desc", "asc"],
		},
		{
			data: "pupils",
			render: $.fn.dataTable.render.number(','),
			className: "center" ,
			orderSequence: ["desc", "asc"]
		},
		{
			data: "percentage_fsm",
			className: "center" ,
			orderSequence: ["desc", "asc"]
		}
		// {
			//   data: "trust_name",
			//   orderSequence: ["desc", "asc"]
		// },
		// {
			//   data: "sponsor_name",
			//   orderSequence: ["desc", "asc"]
			// }
	    ],
	    order: [2, 'asc']
	});
})
