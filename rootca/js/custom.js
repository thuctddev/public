(function($){
  $(document).ready(function(){
    $(".link-content").click(function(){
      $.get('templates/'+$(this).data("link"), function(data){
        $(".right-site").html(data);
      }, 'text');
    });
    $(".main-menu ul li:first a").click();
  });
})(jQuery);