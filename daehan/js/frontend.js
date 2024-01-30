$(window).scroll(function () {
    $('.number').numeric();
    $('.price_format').number(true ,0);

	var top = $(window).scrollTop();
	if (top > 0) {
		jQuery('.back-go-top').show();
	} else {
		jQuery('.back-go-top').hide()
	}

	$(".popupRgFormMb").click(function(e) {
		$("#popupRegForm").trigger('click');
	});

    $("#popupHotlineMb").click(function(e) {
        $("#popupHotline").trigger('click');
    });

	$(".slider-horizontal").slick({
        arrows: true,
        slidesToShow:3,
        slidesToScroll: 1,
        speed: 1000,
        autoplay: true,
        autoplaySpeed: 4000,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });

    $(".box_thongso .boxinfo_title").click(function(e) {
    	if ($(this).hasClass('active')) {
    		$(this).removeClass('active');
    		$(".box_thongso .boxinfo_content").show();
    	}else{
    		$(this).addClass('active');
    		$(".box_thongso .boxinfo_content").hide();
    	}
    });
    $(".box_thongso .boxinfo_title").trigger('click');

    $("#slideNewsOther").slick({
    	arrows:true,
    	dots:false,
    	autoplay: true,
        slidesToShow : 3,
        speed: 1000,
        autoplaySpeed: 4000,
        responsive: [
            {
                breakpoint:767,
                settings: {
                    slidesToShow : 2,
                    arrows:true,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
});

$(document).ready(function() {
    $(".desc table").addClass("table1").wrap("<div class='table-responsive'></div>");
});