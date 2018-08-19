$(function () {
	$.getJSON('data/totals.json', function(json) {
    let len=json.length
    if(len>0){
			var line=json.shift()
			document.getElementById('acadCount').innerHTML=line.school_count+document.getElementById('acadCount').innerHTML
			document.getElementById('sponAcadCount').innerHTML=line.estab_type_count.sponsored_academy+document.getElementById('sponAcadCount').innerHTML
			document.getElementById('convAcadCount').innerHTML=line.estab_type_count.converter_academy+document.getElementById('convAcadCount').innerHTML
			document.getElementById('fsCount').innerHTML=line.estab_type_count.free_school+document.getElementById('fsCount').innerHTML
			document.getElementById('utcssCount').innerHTML=line.estab_type_count.utc_studio_school+document.getElementById('utcssCount').innerHTML
			document.getElementById('primCount').innerHTML=line.estab_phase_count.primary+document.getElementById('primCount').innerHTML
			document.getElementById('secCount').innerHTML=line.estab_phase_count.secondary+document.getElementById('secCount').innerHTML
			document.getElementById('thruCount').innerHTML=line.estab_phase_count.all_through+document.getElementById('thruCount').innerHTML
			document.getElementById('apCount').innerHTML=line.estab_phase_count.alternative_provision+document.getElementById('apCount').innerHTML
			document.getElementById('specCount').innerHTML=line.estab_phase_count.special+document.getElementById('specCount').innerHTML
			document.getElementById('post16Count').innerHTML=line.estab_phase_count.post_16+document.getElementById('post16Count').innerHTML
			document.getElementById('trustCount').innerHTML=line.trust_count+document.getElementById('trustCount').innerHTML
			document.getElementById('satCount').innerHTML=line.sat_count+document.getElementById('satCount').innerHTML
			document.getElementById('matCount').innerHTML=line.mat_count+document.getElementById('matCount').innerHTML
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
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "pupil_numbers_schools",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "no_pupil_numbers_schools",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.primary",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.secondary",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.all_through",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.alternative_provision",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.special",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_phase_count.post_16",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_type_count.sponsored_academy",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_type_count.converter_academy",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_type_count.free_school",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_type_count.utc_studio_school",
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
