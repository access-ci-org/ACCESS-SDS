/*////////////////////////////////////////////
    Software 'Details' Modal Event Listener //
*/////////////////////////////////////////////   
$('#softwareDetails-modal').on('show.bs.modal', function (event) {
    var link = $(event.relatedTarget) // link that triggered the modal
    var software = link.data('id') // Extract info from data-* attributes
    var modal = $(this)
    modal.find('.modal-title')
    $('#softwareDetails-modal').modal('show');
});  