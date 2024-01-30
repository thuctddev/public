$(document).ready(function(){
    $(".slorthermm").slick({
        arrows:true,
        dots:false,
        autoplay: true,
        slidesToShow : 3,
        autoplaySpeed: 5000,
        speed: 1000,
        responsive: [
            {
            breakpoint: 767,
                settings: {
                    slidesToShow : 2,
                }
            }
        ]
    });
    // 
    $('.vhinheight .vvdecss').each(function(){
        var that = $(this);
        that.parents(".vhinheight").append('<div class="dsview"><div class="vhviewtt"><div class="showview"><a class="" href="javascript:void(0)"><span>Đọc tiếp</span></a></div><div class="hideview"><a class="" href="javascript:void(0)"><span>Thu gọn</span></a></div></div></div>');
        var innerhpc = that.innerHeight();
        if(innerhpc > 1300){
            that.css({
                'height' : 1300,
                'overflow' : 'hidden'
            })
            that.addClass('vchange');
            that.siblings('.dsview').find('.showview').show();
            that.siblings('.dsview').find('.showview a').on('click', function(){
                that.css({
                    'height' : 'auto',
                })
                that.removeClass('vchange');
                that.siblings('.dsview').find('.showview').hide();
                that.siblings('.dsview').find('.hideview').show();
            })
            that.siblings('.dsview').find('.hideview a').on('click', function(){
                that.css({
                    'height' : 1300,
                })
                that.addClass('vchange');
                that.siblings('.dsview').find('.showview').show();
                that.siblings('.dsview').find('.hideview').hide();
            })
        }
    })
    // 
    /*$(".slmbthumbs").slick({
        arrows:true,
        dots:false,
        autoplay: true,
        slidesToShow : 1,
        autoplaySpeed: 5000,
        speed: 1000,
    });*/
    // 
    /*$('.hplinkstabs').mnfixed({
        break: 992,
        zindex: 10,
        top: 66
    });*/
    $('.tplinkstabs a[href^="#"]').on('click', function(event) {
        var target = $( $(this).attr('href') );
        if( target.length ) {
            event.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top - 146
            }, 1000);
        }
    });
    // 
    $(window).scroll(function () {
        var scrollDistance = $(window).scrollTop();
        $(".tproductmm").each(function (i) {
            if ($(this).offset().top - 150 <= scrollDistance) {
                $(".tplinkstabs ul li.current").removeClass("current");
                $(".tplinkstabs ul li").eq(i).addClass("current");
            }
        });
    }).scroll()
    // 
    $(".tproductmf .mftitle").click(function(){
        if(!$(this).parents(".tproductmf").hasClass("active")){
            $(this).parents(".tproductmf").addClass("active");
            $(this).parents(".tproductmf").find(".mfconts").stop().slideUp();
        }
        else{
            $(this).parents(".tproductmf").removeClass("active");

            $(this).parents(".tproductmf").find(".mfconts").stop().slideDown();
        }
    }); 
})