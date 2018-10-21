if (window.location.href.split('/')[2]=='127.0.0.1:8000'){
	var group_code=window.location.href.split('/')[4]
}
else if (window.location.href.split('/')[2]=='philipnye.github.io') {		// XXX Will need updating if URL structure changes
	var group_code=window.location.href.split('/')[5]
}

$(function () {
	function initialiseTooltips() {
			$('[data-toggle="tooltip"]').tooltip()
	}

	function setValuesAndTooltips(json) {
    let len=json.length
    if(len>0){
      for(let i=0; i<len; i++){
        var line=json.shift()
        if (line.group_code==group_code){
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
					document.getElementById('pupsCount').innerHTML=line.pupil_numbers.toLocaleString('en', {useGrouping:true})+document.getElementById('pupsCount').innerHTML
					if (line.no_pupil_numbers_schools>0){
						var tooltipText='Pupil numbers are only available for ' + line.pupil_numbers_schools + ' out of ' + line.school_count +' schools'
						document.getElementById('pupsCount').innerHTML=document.getElementById('pupsCount').innerHTML + '<sup><i class="fas fa-exclamation-circle" data-toggle="tooltip" title="' + tooltipText + '"></i></sup>'
					}
				}
			}
		}
		initialiseTooltips()
	}

	$.getJSON('../../data/groups.json', setValuesAndTooltips)		// async callback

  $('#schoolsTable').DataTable({
    ajax: {
      url: '../../data/schools.json',
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
        data: "pupils",
				render: $.fn.dataTable.render.number(','),
        orderSequence: ["desc", "asc"]
      },
      {
        data: "percentage_fsm",
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
        data: "estab_phase",
        orderSequence: ["desc", "asc"]
      },
      {
        data: "estab_type",
        orderSequence: ["desc", "asc"]
      },
      {
        data: "open_date",
				render: $.fn.dataTable.render.moment('DD-MM-YYYY','D MMMM YYYY'),
        orderSequence: ["desc", "asc"],
      },
      {
        data: "trust_name",
        orderSequence: ["desc", "asc"]
      },
      {
        data: "sponsor_name",
        orderSequence: ["desc", "asc"]
      }
    ],
    order: [2, 'asc']
  });
})
