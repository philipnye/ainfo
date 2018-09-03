$(function () {
	$.getJSON('data/totals.json', function(json) {
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
			document.getElementById('trustCount').innerHTML=line.trust_count.toLocaleString('en', {useGrouping:true})+document.getElementById('trustCount').innerHTML
			document.getElementById('satCount').innerHTML=line.sat_count.toLocaleString('en', {useGrouping:true})+document.getElementById('satCount').innerHTML
			document.getElementById('matCount').innerHTML=line.mat_count.toLocaleString('en', {useGrouping:true})+document.getElementById('matCount').innerHTML
		}
	});
	$('#trustsTable').DataTable({
    "ajax": {
      "url": 'data/trusts.json',
      "dataSrc": "" // handle the fact we're passing in a JSON array rather than a JSON object i.e. not {"data": [{...},...]}
    },
    "deferRender": true,
    "columns": [{
        "data": "trust_name",
        "orderSequence": ["asc", "desc"]
      },
      {
        "data": "school_count",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "pupil_numbers",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "pupil_numbers_schools",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "no_pupil_numbers_schools",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.primary",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.secondary",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.all_through",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.alternative_provision",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.special",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.post_16",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_type_count.sponsored_academy",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_type_count.converter_academy",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_type_count.free_school",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_type_count.utc_studio_school",
				"render": $.fn.dataTable.render.number( ','),
        "orderSequence": ["desc", "asc"]
      }
    ],
    "order": [1, 'desc'],
    "columnDefs": [{
      "targets": 0,
      "render": function(data, type, row, meta) {
        return '<a href="' + row.trust_page_url + '">' + data + '</a>';
      }
    }]
  });
});
