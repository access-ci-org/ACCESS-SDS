

$(document).ready(function() {
    $('#softwareTable').DataTable({
        data: tableData,
        columns: [
            { title: "Software Name", data: "software_name" },
            { title: "RP Software", data: "rp_software" },
            { title: "Description", data: "description" },
            { title: "Software Type", data: "software_type" },
            { title: "Software Class", data: "software_class" },
            { title: "Research Area", data: "research_area" },
            { title: "Research Discipline", data: "research_discipline" },
            { title: "RP Software Documentation", data: "RP Software Documentation" }
        ],
        dom: 'Bfrtip',
        buttons: [
            'colvis'
        ],
        searchBuilder: true
    });
});
