$(document).ready(function() {
    vnTRUST.goTopStart();
    $(window).load(function() {
        var hash = window.location.hash;
        console.log(hash, hash == '');
        if (hash == '') {
            if ($("#vnt-content").hasClass("scroll_effect")) {
                jQuery('html,body').animate({
                    scrollTop: $(".scroll_effect").offset().top - $(".header_fixed").innerHeight() - 60
                }, 1400);
            }
        }
        if (hash == '#scroll') {
            jQuery('html,body').animate({
                scrollTop: $(".vnTScroll").offset().top - $(".header_fixed").innerHeight() - 60
            }, 1400);
        }
    });
    $(".menu_category .mc_title").click(function() {
        if (!$(this).parents(".menu_category").hasClass("active")) {
            $(this).parents(".menu_category").addClass("active");
        } else {
            $(this).parents(".menu_category").removeClass("active");
        }
    });
    $(window).click(function(e) {
        var $clicked = $(e.target);
        if (!$clicked.parents().hasClass('vnt-hotline')) {
            $(".vnt-hotline").removeClass('show');
        }
        if (!$clicked.parents().hasClass('vnt-search')) {
            $(".vnt-search").removeClass('show');
        }
        if (!$clicked.parents().hasClass("menu_category")) {
            $(".menu_category").removeClass("active");
        }
    });
    $(".menu_main > ul > li").each(function(e) {
    });
    $(".menu_main ul ul li").each(function() {
        var countsize = $(this).find("ul li").size();
        if (countsize > 0) {
            $(this).find("a:first").addClass("m-sub");
        }
    });
    $(".menu_main > ul > li").hover(function() {
        var $size = $(this).find('ul:first li').size();
        /*if($size > 0){
            $("#maskmenu").addClass('show');
        }*/
    }, function() {
        var $size = $(this).find('ul:first li').size();
        /*if($size > 0) {
            $("#maskmenu").removeClass('show');
        }*/
    });
    $(window).load(function() {
        var $heightmenu = $(".header_fixed").innerHeight();
        $(".vnt-menutop").css({
            'min-height': $heightmenu
        });
        $(window).resize(function() {
            $heightmenu = $(".header_fixed").innerHeight();
            $(".vnt-menutop").css({
                'min-height': $heightmenu
            });
        });
        var offestFixed = 0;
        if (typeof $(".vnt-menutop").offset() == 'object') {
            offestFixed = $(".vnt-menutop").offset().top;
        }
        if ((offestFixed + $heightmenu) < $(window).scrollTop()) {
            $(".vnt-menutop .header_fixed").addClass("active");
        }
        $(window).scroll(function() {
            var $scrollBar = $(window).scrollTop();
            if (typeof $(".vnt-menutop").offset() == 'object') {
                offestFixed = $(".vnt-menutop").offset().top;
            }
            if ((offestFixed + $heightmenu) < $scrollBar) {
                $(".vnt-menutop .header_fixed").addClass("active");
            } else {
                $(".vnt-menutop .header_fixed").removeClass("active");
            }
        });
        $(window).resize(function() {
            var $scrollBar = $(window).scrollTop();
            if (typeof $(".vnt-menutop").offset() == 'object') {
                offestFixed = $(".vnt-menutop").offset().top;
            }
            if ((offestFixed + $heightmenu) < $scrollBar) {
                $(".vnt-menutop .header_fixed").addClass("active");
            } else {
                $(".vnt-menutop .header_fixed").removeClass("active");
            }
        });
    });
    // 
    /*$(".vhbothead").mnfixed({
        zindex: 112,
        top: 0
    });*/
    // 
    $("#vnt-slide").slick({
		fade:true,
		autoplay:true,
        dots:true,
        arrows:true,
        autoplaySpeed: 5000,
        speed: 1000,
    });
    // 
    $(".vhtabmenu .mctitle").click(function(){
        if(!$(this).parents(".vhtabmenu").hasClass("active")){
            $(this).parents(".vhtabmenu").addClass("active");
            $(this).parent(".vhtabmenu").find(".mcconts").stop().slideDown();
        }
        else{
            $(this).parents(".vhtabmenu").removeClass("active");
            $(this).parent(".vhtabmenu").find(".mcconts").stop().slideUp();
        }
    });
});
$(document).ready(function() {
    $(".menu_category ul li").each(function() {
        var countsize1 = $(this).find("ul li").size();
        if (countsize1 > 0) {
            $(this).find("a:first").wrap("<div class='m-sub'></div>");
            $(this).find(".m-sub:first").append("<div class='button-submenu'></div>")
        }
    });
    $(".menu_category ul li ul").css({
        'display': 'none'
    });
    $(".menu_category ul li.current").find("> .m-sub .button-submenu").addClass("active");
    $(".menu_category ul li.current").find("> ul").css({
        'display': 'block'
    });
    /*$(".menu_category ul li .button-submenu").click(function(){
        if(! $(this).hasClass("active")){
            $(this).parent().parent().find("ul:first").stop().slideToggle(700);
            $(this).parent().parent().addClass("current");
            $(this).addClass("active");
            $(this).parent().parent().siblings().each(function(){
                if($(this).find(".m-sub:first").find(".button-submenu").hasClass("active")){
                    $(this).find("ul:first").stop().slideToggle(700);
                    $(this).find(".m-sub:first").find(".button-submenu").removeClass("active");
                    $(this).removeClass("current");
                }
            });
        }else{
            $(this).parent().parent().find("ul:first").stop().slideToggle(700);
            $(this).parent().parent().removeClass("current");
            $(this).removeClass("active");
        }
    });*/
    $(".menu_category ul li").hover(function() {
        if (!$(this).hasClass("current")) {
            $(this).find("ul:first").stop().slideToggle(700);
            $(this).addClass("active");
        }
        callback_scroll();
    }, function() {
        if (!$(this).hasClass("current")) {
            $(this).find("ul:first").stop().slideToggle(700);
            $(this).removeClass("active");
        }
        callback_scroll();
    })
    resize_menu_page();
    $(window).resize(function() {
        resize_menu_page();
    });
});
$(document).ready(function() {
    /*setTimeout(function(){
        var data_banner = $(".vnt-banner").royalSlider({
            loop: true,
            autoScaleSlider: true,
            imageScalePadding: 0,
            imageScaleMode: 'fill',
            autoScaleSliderWidth: '1600',
            autoScaleSliderHeight: '728',
            slidesSpacing: 0,
            arrowsNav: true,
            controlNavigation: 'none',
            sliderDrag: false,
            video: {
                autoHideArrows: false,
                autoHideControlNav: false,
                autoHideBlocks: true,
                youTubeCode: '<iframe src="https://www.youtube.com/embed/%id%?rel=1&autoplay=1&showinfo=0" frameborder="no" allowFullscreen></iframe>'
                //&controls=0
            },
            autoPlay: {
                // autoplay options go gere
                enabled: true,
                stopAtAction: false,
                pauseOnHover: false,
                delay: 3000,
                speed: 10000
            }
        }).data('royalSlider');
    }, 500);*/
});
/*$(document).ready(function() {
    $("body").lazyScrollLoading({
        lazyItemSelector : ".lazyloading",
        onLazyItemVisible : function(e, $lazyItems, $visibleLazyItems) {
            $visibleLazyItems.each(function() {
                $(this).addClass("show");
            });
        }
    });
});*/
$(window).load(function() {
    $("#div_scroll").css({
        height: $(".scroll-fixed").innerHeight()
    });
    $(window).scroll(function() {
        if (!(typeof $("#div_scroll").offset() == 'object')) {
            return false;
        }
        if ($(window).innerWidth() > 1024) {
            var $heightContent = $(".scroll-fixed").parents(".wrap-scroll").innerHeight();
            var $heightFixed = $heightContent + $("#div_scroll").offset().top - $(".scroll-fixed").innerHeight();
            if ($(window).scrollTop() > ($("#div_scroll").offset().top - 45) && $(window).scrollTop() < $heightFixed) {
                $(".scroll-fixed").css({
                    position: "fixed",
                    top: 46,
                    width: $("#div_scroll").width()
                });
            } else {
                $(".scroll-fixed").css({
                    position: "relative",
                    top: 0
                });
                if ($(window).scrollTop() > $heightFixed) {
                    $(".scroll-fixed").css({
                        position: "relative",
                        top: ($heightContent - $(".scroll-fixed").innerHeight())
                    });
                }
            }
        }
    });
    $(window).resize(function() {
        $(window).scroll(function() {
            if (!(typeof $("#div_scroll").offset() == 'object')) {
                return false;
            }
            if ($(window).innerWidth() > 1024) {
                var $heightContent = $(".scroll-fixed").parents(".wrap-scroll").innerHeight();
                var $heightFixed = $heightContent + $("#div_scroll").offset().top - $(".scroll-fixed").innerHeight();
                if ($(window).scrollTop() > ($("#div_scroll").offset().top - 45) && $(window).scrollTop() < $heightFixed) {
                    $(".scroll-fixed").css({
                        position: "fixed",
                        top: 46,
                        width: $("#div_scroll").width()
                    });
                } else {
                    $(".scroll-fixed").css({
                        position: "relative",
                        top: 0
                    });
                    if ($(window).scrollTop() > $heightFixed) {
                        $(".scroll-fixed").css({
                            position: "relative",
                            top: ($heightContent - $(".scroll-fixed").innerHeight())
                        });
                    }
                }
            }
        });
    });
});
function resize_menu_page() {
    if ($(window).innerWidth() < 1024) {
        // Fix khi xuá»‘ng giao diá»‡n Responsive
        $("#vnt-sidebar").hide();
        if ($('body,html').find('#vnt-sidebar .menu_category').length) {
            if ($(".titleR").find('.menu_category').length > 0) {
            } else {
                $(".titleR").append("<div class='menu_category'></div>");
                $(".titleR .menu_category").html($(".menu_category").html());
            }
        }
        $(".menu_category .mc_title").click(function() {
            if (!$(this).hasClass("active")) {
                $(this).parent().find("ul:first").stop().slideToggle(700);
                $(this).parent().addClass("current");
                $(this).addClass("active");
                $(this).parent().siblings().each(function() {
                    if ($(this).find(".m-sub:first").find(".button-submenu").hasClass("active")) {
                        $(this).find("ul:first").stop().slideToggle(700);
                        $(this).find(".m-sub:first").find(".button-submenu").removeClass("active");
                        $(this).removeClass("current");
                    }
                });
            } else {
                $(this).parent().find("ul:first").stop().slideToggle(700);
                $(this).parent().removeClass("current");
                $(this).removeClass("active");
            }
        });
        $(".menu_category .mc_title a").click(function() {
            if (!$(this).parent().hasClass("active")) {
                $(this).parent().parent().find("ul:first").stop().slideToggle(700);
                $(this).parent().parent().addClass("current");
                $(this).parent().addClass("active");
                $(this).parent().parent().siblings().each(function() {
                    if ($(this).parent().find(".m-sub:first").find(".button-submenu").hasClass("active")) {
                        $(this).parent().find("ul:first").stop().slideToggle(700);
                        $(this).parent().find(".m-sub:first").find(".button-submenu").removeClass("active");
                        $(this).parent().removeClass("current");
                    }
                });
            } else {
                $(this).parent().parent().find("ul:first").stop().slideToggle(700);
                $(this).parent().parent().removeClass("current");
                $(this).parent().removeClass("active");
            }
        });
        $(".menu_category ul li .button-submenu").click(function() {
            if (!$(this).hasClass("active")) {
                $(this).parent().parent().find("ul:first").stop().slideToggle(700);
                $(this).parent().parent().addClass("current");
                $(this).addClass("active");
                $(this).parent().parent().siblings().each(function() {
                    if ($(this).find(".m-sub:first").find(".button-submenu").hasClass("active")) {
                        $(this).find("ul:first").stop().slideToggle(700);
                        $(this).find(".m-sub:first").find(".button-submenu").removeClass("active");
                        $(this).removeClass("current");
                    }
                });
            } else {
                $(this).parent().parent().find("ul:first").stop().slideToggle(700);
                $(this).parent().parent().removeClass("current");
                $(this).removeClass("active");
            }
        });
    } else {
        $("#vnt-sidebar").show();
        $(".titleR").html('');
    }
}
function callback_scroll() {
    setTimeout(function() {
        $("#div_scroll").css({
            height: $(".scroll-fixed").height()
        });
        var $heightContent = $(".scroll-fixed").parents(".wrap-scroll").innerHeight();
        var $heightFixed = $heightContent + $("#div_scroll").offset().top - $(".scroll-fixed").innerHeight();
        if ($(window).scrollTop() > ($("#div_scroll").offset().top - 45) && $(window).scrollTop() < $heightFixed) {
            $(".scroll-fixed").css({
                position: "fixed",
                top: 46,
                width: $("#div_scroll").width()
            });
        } else {
            $(".scroll-fixed").css({
                position: "relative",
                top: 0
            });
            if ($(window).scrollTop() > $heightFixed) {
                $(".scroll-fixed").css({
                    position: "relative",
                    top: ($heightContent - $(".scroll-fixed").innerHeight())
                });
            }
        }
    }, 100);
}
// 
$(document).ready(function() {
    $(".searchtop .icon").click(function(){
        if(!$(this).parents(".searchtop").hasClass("active")){
            $(this).parents(".searchtop").addClass("active");
        }
        else{
            $(this).parents(".searchtop").removeClass("active");
        }
    });
    // 
    $(window).bind("click",function(e){
        var target=e.target;
        if(!$(target).parents(".searchtop").hasClass("active")){
            $(".searchtop").removeClass("active");
        }
    }); 
})