function openNav() {
    $('#mySidenav').animate({width:'280px'}, 100);
    setTimeout(function(){
      $('#mySidenav a, #mySidenav p').css('color','#b5b5b5');
    }, 350);

}

function closeNav() {
    $('#mySidenav a, #mySidenav p').css('color','#868e96');
    setTimeout(function(){
      $('#mySidenav').animate({width:'0px'}, 100);
    }, 120);
}
