$(document).ready(function(){
  $('#search-button').click(function(){
    var input = $('#search-input').val()
    if (input != ''){
      window.location  = '/search/' + input
    }
  })
})
$(document).keypress(function(e) {
    if(e.which == 13) {
        $('#search-button').trigger('click')
    }
});
