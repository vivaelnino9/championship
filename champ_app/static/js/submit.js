$(document).ready(function(){
  $('#submit-form').submit(function(){
    $(this).hide()
    $('#waiting-footer').show()
  })
});
