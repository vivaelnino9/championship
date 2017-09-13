$(document).ready(function(){
    $('[data-toggle="popover"]').popover();

    $('#submit').click(function(){
      var team_name = $(this).attr("data-team")
      var tournament = $(this).attr("data-tour")
      $(this).hide();
      $('#loading-spinner').show();
      $.ajax({
        url:'/tournament_signup/',
        data : {
          'team_name' : team_name,
          'tournament' : tournament,
          'add' : true
        },
        success : function(data) {
            location.reload();
        },
      },)
    });

    $('#remove').click(function(){
      var team_name = $(this).attr("data-team")
      var tournament = $(this).attr("data-tour")
      $.confirm({
        title: '',
        content: 'Are you sure you want to remove your signup?',
        buttons: {

            cancel: function () {
                $.alert('Canceled!');
            },
            confirm: {
                text: 'Confirm',
                btnClass: 'btn-blue',
                keys: ['enter', 'shift'],
                action: function(){
                  $('#signed-up').hide();
                  $('#loading-spinner').show();
                  $.ajax({
                    url:'/tournament_signup/',
                    data : {
                      'team_name' : team_name,
                      'tournament' : tournament,
                      'add' : false
                    },
                    success : function(data) {
                        $.alert('Signup removed!');
                        location.reload();
                    },
                  },)

                }
            }
        }
      });
    });
});
