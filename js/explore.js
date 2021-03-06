var table,
	newSortCol,
	currentSortCol=1,
	currentSortDirection='desc'

function initialiseTooltips() {
	$('[data-toggle="tooltip"]').tooltip()
}

function setValues(json) {
    let len=json.length
    if(len>0){
		var line=json.shift()
		document.getElementById('acadCount').innerHTML=line.school_count.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('acadCount').innerHTML
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
		document.getElementById('groupCount').innerHTML=line.group_count.toLocaleString('en', {useGrouping:true})+' '+document.getElementById('groupCount').innerHTML
	}
};

function drawTable() {
	table = $('#groupsTable').DataTable({
	    ajax: {
			url: 'data/groups_demo.json',
			dataSrc: ""		// handle the fact we're passing in a JSON array rather than a JSON object i.e. not {data: [{...},...]}
	    },
		dom: '<"row tableTop"<"col-sm-12"f>>' + 't' + '<"tableBottom"<"row"<"col-sm-6"l><"col-sm-6"i>><"row"<"col-sm-12"p>>>',
		scrollX: true,
		deferRender: true,
		drawCallback: function(settings) {
	    	initialiseTooltips()
	    },
	    columns: [{
	        data: "group_name",
			render: function(data, type, row, meta) {
		        return '<a href="' + row.group_page_url + '">' + data + '</a>';
			},
			width: "480px",
	        orderable: true,
		},
		{
	        data: "school_count",
	        orderable: false,
			className: "left-border"
		},
		{
	        data: "pupil_numbers",
			render: function(data, type, row, meta) {
				if (row.no_pupil_numbers_schools>0){
					var tooltipText='Pupil numbers are only available for ' + row.pupil_numbers_schools + ' out of ' + row.school_count +' schools'
					return '<span class="pupilNumbersFlagged" data-toggle="tooltip" title="' + tooltipText + '">' + data.toLocaleString('en-GB') + '</span>';
				}
				else {
					return data.toLocaleString('en-GB')
				}
			},
	        orderable: false,
			className: "left-border"
		},
		{
	        data: "estab_phase_count.primary",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false,
			className: "left-border"
		},
		{
	        data: "estab_phase_count.secondary",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false
		},
		{
	        data: "estab_phase_count.all_through",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false
		},
		{
	        data: "estab_phase_count.alternative_provision",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false
		},
		{
	        data: "estab_phase_count.special",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false
		},
		{
	        data: "estab_phase_count.post_16",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false
		},
		{
	        data: "estab_type_count.sponsored_academy",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false,
			className: "left-border"
		},
		{
	        data: "estab_type_count.converter_academy",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false
		},
		{
	        data: "estab_type_count.free_school",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false
		},
		{
	        data: "estab_type_count.utc_studio_school",
			render: $.fn.dataTable.render.number( ','),
	        orderable: false
		},
		{
			data: null,
			defaultContent: "",
			width: "160px",		// to match 'length' of column headers
			orderable: false
		}],
	    "order": [1, 'desc']
	});
}

$(function () {
	$.getJSON('data/totals.json', setValues)		// async callback
});

$("a[href='#tab-table']").on('shown.bs.tab', function (e) {
	if (table == null) {
		drawTable()
	}
});


$("#groupsTable").find("thead").on('click', 'div', function(){		// sorting upon clicking on table column names
    newSortCol =  table.column(this.parentElement).index();		// parentElement, as we need the containing th, rather than the div
	if (newSortCol==currentSortCol) {
		if ($('#groupsTable').DataTable().order()[0][1]) {		// on first clicking the default-sorted column, .order seems to not return an array. Hence, we only try to read the array where it exists. Where it doesn't, initial value for currentSortDirection should make sure on-click action should work correctly
			currentSortDirection=$('#groupsTable').DataTable().order()[0][1]
		}
		if (currentSortDirection=='desc') {
			$('#groupsTable').DataTable().order([newSortCol, 'asc']).draw()
		}
		else {
			$('#groupsTable').DataTable().order([newSortCol, 'desc']).draw()
		}
	}
	else {
		$('#groupsTable').DataTable().order([newSortCol, 'desc']).draw()
	}
	currentSortCol=newSortCol
});
