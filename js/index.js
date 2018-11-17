$(function () {
	function initialiseTooltips() {
			$('[data-toggle="tooltip"]').tooltip()
	}

	function setValues(json) {
    let len=json.length
    if(len>0){
			var line=json.shift()
			document.getElementById('acadCount').innerHTML=line.school_count.toLocaleString('en', {useGrouping:true})+document.getElementById('acadCount').innerHTML
			document.getElementById('sponAcadCount').innerHTML=line.estab_type_count.sponsored_academy.toLocaleString('en', {useGrouping:true})+document.getElementById('sponAcadCount').innerHTML
			document.getElementById('convAcadCount').innerHTML=line.estab_type_count.converter_academy.toLocaleString('en', {useGrouping:true})+document.getElementById('convAcadCount').innerHTML
			document.getElementById('fsCount').innerHTML=line.estab_type_count.free_school.toLocaleString('en', {useGrouping:true})+document.getElementById('fsCount').innerHTML
			document.getElementById('utcssCount').innerHTML=line.estab_type_count.utc_studio_school.toLocaleString('en', {useGrouping:true})+document.getElementById('utcssCount').innerHTML
			document.getElementById('primCount').innerHTML=line.estab_phase_count.primary.toLocaleString('en', {useGrouping:true})+document.getElementById('primCount').innerHTML
			document.getElementById('secCount').innerHTML=line.estab_phase_count.secondary.toLocaleString('en', {useGrouping:true})+document.getElementById('secCount').innerHTML
			document.getElementById('thruCount').innerHTML=line.estab_phase_count.all_through.toLocaleString('en', {useGrouping:true})+document.getElementById('thruCount').innerHTML
			document.getElementById('apCount').innerHTML=line.estab_phase_count.alternative_provision.toLocaleString('en', {useGrouping:true})+document.getElementById('apCount').innerHTML
			document.getElementById('specCount').innerHTML=line.estab_phase_count.special.toLocaleString('en', {useGrouping:true})+document.getElementById('specCount').innerHTML
			document.getElementById('post16Count').innerHTML=line.estab_phase_count.post_16.toLocaleString('en', {useGrouping:true})+document.getElementById('post16Count').innerHTML
			document.getElementById('groupCount').innerHTML=line.group_count.toLocaleString('en', {useGrouping:true})+document.getElementById('groupCount').innerHTML
		}
	};

	$.getJSON('data/totals.json', setValues)		// async callback

	$('#groupsTable').DataTable({
    ajax: {
      url: 'data/groups.json',
      dataSrc: "" // handle the fact we're passing in a JSON array rather than a JSON object i.e. not {data: [{...},...]}
    },
		dom: '<"tableTop"f>t<"tableBottom"ilp>',
		deferRender: true,
		drawCallback: function(settings) {
        initialiseTooltips()
    },
    columns: [{
        data: "group_name",
				render: function(data, type, row, meta) {
	        return '<a href="' + row.group_page_url + '">' + data + '</a>';
	      },
        orderSequence: ["asc", "desc"]
      },
      {
        data: "school_count",
        orderSequence: ["desc", "asc"]
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
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_phase_count.primary",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_phase_count.secondary",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_phase_count.all_through",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_phase_count.alternative_provision",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_phase_count.special",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_phase_count.post_16",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_type_count.sponsored_academy",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_type_count.converter_academy",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_type_count.free_school",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_type_count.utc_studio_school",
				render: $.fn.dataTable.render.number( ','),
        orderSequence: ["desc", "asc"]
      }
    ],
    "order": [1, 'desc']
  });
});
