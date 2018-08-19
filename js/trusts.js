$(function () {
	$.getJSON('/data/trusts.json', function(json) {
    let len=json.length
    if(len>0){
      for(let i=0; i<len; i++){
        var line=json.shift()
        if (line.trust_code==trust_code){
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
					document.getElementById('pupsCount').innerHTML=line.pupil_numbers+document.getElementById('pupsCount').innerHTML
				}
			}
		}
	});
  $('#schoolsTable').DataTable({
    "ajax": {
      "url": '/data/schools.json',
      "dataSrc": function (json) {
        let data=[]
        let len=json.length
        if(len>0){
          for(let i=0; i<len; i++){
            var line=json.shift()
            if (line.trust_code==trust_code){
              data.push(line)
            }
          }
        }
      return data;
      }
    },
    "deferRender": true,
    "columns": [{
        "data": "urn",
        "orderSequence": ["asc", "desc"]
      },
      {
        "data": "laestab",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "estab_name",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "pupils",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "percentage_fsm",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "la",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "region",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "phase",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "type_of_estab",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "open_date",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "trust_name",
        "orderSequence": ["desc", "asc"]
      },
      {
        "data": "school_sponsor_name",
        "orderSequence": ["desc", "asc"]
      }
    ],
    "order": [2, 'asc']
  });
})
