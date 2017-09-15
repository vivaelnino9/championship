$(document).ready(function(){
  $('.edit-link').click(function(){
    $(this).hide()
    $('.edit-player').show()
    $('.edit-cancel').show()
    $('#edit-save').show()
    $('.add-section').show()
  });
  $('.edit-cancel').click(function(){
    $(this).hide()
    $('.edit-link').show()
    $('.edit-player').hide()
    $('.edit-confirm').hide()
    $('.edit-player-text').hide()
    $('.player-link').show()
    $('#edit-save').hide()
    $('.add-section').hide()
  })
  $('.edit-player-span').click(function(){
    var data_player = $(this).attr('data-player')
    $('#edit-' + data_player).hide() // x and pencil
    $('#link-' + data_player).hide() // player name
    $('#confirm-' + data_player).show() // x and check mark
    $('#text-' + data_player).show() // text area
  });
  $('.edit-cancel-text').click(function(){
    var data_player = $(this).attr('data-player')
    $('#edit-' + data_player).show() // x and pencil
    $('#link-' + data_player).show() // player name
    $('#confirm-' + data_player).hide() // x and check mark
    $('#text-' + data_player).hide() // text area
  });
  $('#edit-save').click(function(){
    if ($(".edit-player-text[data-field='captain']").val() == ''){
      $.alert({
          title: '',
          content: "You can't remove a captain/coach!",
      });
      return;
    }
    $('#edit-save').hide()
    $('#loading-spinner').show()
    $.ajax({
      url:'/roster_change/',
      data : {
        'team_name' : $(this).attr('data-team'),
        'captain' : $(".edit-player-text[data-field='captain']").val(),
        'player1' : $(".edit-player-text[data-field='player1']").val(),
        'player2' : $(".edit-player-text[data-field='player2']").val(),
        'player3' : $(".edit-player-text[data-field='player3']").val(),
        'player4' : $(".edit-player-text[data-field='player4']").val(),
        'new_field' : $('.add-player-text').attr('data-field'),
        'new_player' : $('.add-player-text').val(),
      },
      success : function(data) {
          console.log(data);
          location.reload();
      },
    },)
  })
  $('.edit-player-text, .add-player-text').keydown(function(e){
    if (e.keyCode == 13){
      e.preventDefault();
      $('#edit-save').click()
    }
  });
  $('.edit-player-text, .add-player-text').keyup(function(e){
    var len = $(this).val().length;
    if (len >= 14){
      $(this).attr('cols', '30');
    }
    else{
      $(this).attr('cols', '15');
    }
  });
  $('.add-player-link').click(function(){
    $(this).hide()
    $('.add-player').hide()
    $('.add-confirm').show()
    $('.add-player-text').show()
    $('.add-cancel-text').show()
  })
  $('.add-cancel-text').click(function(){
    $(this).hide()
    $('.add-player').show()
    $('.add-confirm').hide()
    $('.add-player-text').hide()
    $('.add-player-link').show()

  })
});
