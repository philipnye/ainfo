var group_code,
	growthChartData,
	groupTickInterval,
	mobileCheck,
	tabs,
	tabsObj,
	tabbedContentWidth,
	regionObj = {}

window.mobilecheck=function() {
	mobileCheck=false;
	(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) mobileCheck = true;})(navigator.userAgent||navigator.vendor||window.opera);
};

function abbreviateTabText() {
	tabsObj={}

	for (let tab of tabs) {
		tabsObj[tab.hash]=tab.textContent		// stash initial tab text
		if (0<tab.getAttribute("data-tab-order")) {		// display tab text for first two tabs
			tab.textContent='...'
		}
	}

	$('.tabbed-content a').on('click', function (e) {
		for (let tab of tabs) {
			if (Number(tab.getAttribute("data-tab-order")) != Number($(this)[0].getAttribute("data-tab-order"))) {
				tab.textContent='...'
			}
			else {
				tab.textContent=tabsObj[tab.hash]
			}
		}
	})
}

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
					regionObj[Object.keys(line.region_count)[j]]=Object.values(line.region_count)[j]
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

function drawMap() {
	var width = tabbedContentWidth,
	    height = 400*tabbedContentWidth/445;		// 445px is default/max width of tabbed-content on a monitor

	var svg = d3.select("#regions-map")
	    .attr("width", width)
	    .attr("height", height);

	d3.json("../../data/map/regions.json", function(error, uk) {
		if (error) return console.error(error);

		var regions = topojson.feature(uk, uk.objects.eer);

		var projection = d3.geo.albers()
		    .center([0, 52.9])
		    .rotate([1.9, 0])
		    .parallels([50, 60])
		    .scale(3500*tabbedContentWidth/445)
		    .translate([width/2, height/2]);

		var path = d3.geo.path()
	    	.projection(projection);

		tip = d3.tip()
			.attr('class', 'd3-tip')
			.direction(function(d) {
				if (d.properties.EER13NM.toLowerCase() == 'north east') {
					return 'w';
				}
				else if (d.properties.EER13NM.toLowerCase() == 'north west') {
					return 'e';
				}
				else if (d.properties.EER13NM.toLowerCase() == 'yorkshire and the humber') {
					return 'n';
				}
				else if (d.properties.EER13NM.toLowerCase() == 'east midlands') {
					return 'n';
				}
				else if (d.properties.EER13NM.toLowerCase() == 'west midlands') {
					return 'w';
				}
				else if (d.properties.EER13NM.toLowerCase() == 'east of england') {
					return 'w';
				}
				else if (d.properties.EER13NM.toLowerCase() == 'london') {
					return 'n';
				}
				else if (d.properties.EER13NM.toLowerCase() == 'south east') {
					return 'n';
				}
				else if (d.properties.EER13NM.toLowerCase() == 'south west') {
					return 'e';
				}
			})
			.html(function(d) {
				if (getRegionData(d).values==1) {
					var unit = 'academy'
				}
				else {
					var unit = 'academies'
				}
				return '<p class="tip-title">' + reformatRegionNames(getRegionData(d).keys) + '</p><p>' + getRegionData(d).values + ' ' + unit + '</p>'
			});

		svg.call(tip)

		svg.append("path")
		    .datum(regions)
		    .attr("d", path);

		svg.selectAll(".region")
		    .data(topojson.feature(uk, uk.objects.eer).features)
		  	.enter()
			.append("path")
		    .attr("class", function(d) { return "region " + d.properties.EER13NM.toLowerCase().replace(/\ /g,'-'); })
			.classed('present', function(d) {
				return getRegionData(d).values>0;
			})
		    .attr("data-region", function(d) { return d.properties.EER13NM })
		    .attr("data-count", function(d) {
				return getRegionData(d).values;
			})
		    .attr("d", path)
			.on("mouseover", tip.show)
			.on("mouseout", tip.hide)

	});
}

function getRegionData(d) {
	for (var j = 0; j < Object.keys(regionObj).length; ++j) {
		if (Object.keys(regionObj)[j]==d.properties.EER13NM.toLowerCase().replace(/\ /g,'_')) {		// NB: underscore rather than hyphen
			return {
		        keys: Object.keys(regionObj)[j],
		        values: Object.values(regionObj)[j]
		    };
		}
	}
}

function reformatRegionNames(region) {
	var region = region.replace(/\_/g,' ')
	region = region.charAt(0).toUpperCase() + region.slice(1);
	region = region.replace('england','England')
	region = region.replace('london','London')
	region = region.replace('midlands','Midlands')
	region = region.replace('yorkshire','Yorkshire')
	region = region.replace('humber','Humber')
	return region
}

function roundUpTabbedContentWidth() {
	var tabsWidth = 0
	for (let tab of tabs) {
		tabsWidth += tab.clientWidth
	}
	var widthDiff = tabbedContentWidth-tabsWidth
	if (widthDiff<50) {
		widthDiff = widthDiff/5
		for (let tab of tabs) {
			tab.style.width = tab.clientWidth + widthDiff + "px"
		}
	}
}

$(function () {
	if (window.location.href.split('/')[2]=='127.0.0.1:8000'){
		group_code=window.location.href.split('/')[4]
	}
	else if (window.location.href.split('/')[2]=='philipnye.github.io') {		// XXX Will need updating if URL structure changes
		group_code=window.location.href.split('/')[5]
	}

	window.mobilecheck()

	tabs=document.getElementsByClassName("tabbed-content")[0].getElementsByClassName("nav-link")

	var element = document.getElementsByClassName("tabbed-content")[0]
	var computedStyle = getComputedStyle(element);
	tabbedContentWidth = element.clientWidth;
	tabbedContentWidth -= parseFloat(computedStyle.paddingLeft) + parseFloat(computedStyle.paddingRight);

	if (mobileCheck==true) {
		abbreviateTabText()
	}

	$.getJSON('../../data/groups_demo.json', setValuesAndTooltips)		// async callback

	var table = $('#schoolsTable').DataTable({
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
	    columns: [
        {
            data: null,
            defaultContent: '<i class="fas fa-chevron-right"></i>',
            className: 'details-control center',
            orderable: false
        },
		{
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
	    ],
	    order: [2, 'asc']
	});

	function expand(d) {
	    return '<table>' +
	        '<tr>' +
	            '<td>Trust:</td>' +
	            '<td>' + d.trust_name + '</td>' +
	        '</tr>' +
	        '<tr>' +
	            '<td>Sponsor:</td>' +
	            '<td>' + d.sponsor_name + '</td>' +
	        '</tr>' +
	    '</table>'
	}

    $('#schoolsTable tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if ( row.child.isShown() ) {
			$(this)[0].innerHTML = '<i class="fas fa-chevron-right"></i>'
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
			$(this)[0].innerHTML = '<i class="fas fa-chevron-down"></i>'
            row.child( expand(row.data()) ).show();
            tr.addClass('shown');
        }
    } );

	roundUpTabbedContentWidth()
	drawMap()

})
