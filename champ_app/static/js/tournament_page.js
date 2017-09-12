$(document).ready(function(){
    $('[data-toggle="popover"]').popover();

    $('#submit').click(function(){
      $(this).hide();
      $('#loading-spinner').show();
      $.ajax({
        url:'/tournament_signup/',
        data : {
          'team_name' : $(this).attr("data-team"),
          'tournament' : $(this).attr("data-tour")
        },
        success : function(data) {
            location.reload();
        },
      },)
    });
});
