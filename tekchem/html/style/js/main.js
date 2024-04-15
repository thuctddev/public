$(document).ready(function () {
    $('.slide-index').owlCarousel({
        items: 1,
        loop: 1,
        margin: 0,
        nav: 1,
        navText: ['<img src="/html/style/images/prev-slide.webp" alt="icon">', '<img src="/html/style/images/next-slide.webp" alt="icon">'],
        dots: 0,
        autoplay: 1,
        autoplayTimeout: 5000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1,
                dots: 0,
                nav: 0,
            },
            767: {
                items: 1,
                dots: 0,
                nav: 0,
            },
            992: {
                items: 1,
            },
        }
    });

    $('.slide-service').owlCarousel({
        items: 4,
        loop: 1,
        margin: 20,
        nav: 1,
        navText: ['<img src="./images/prev-slide1.webp" alt="">', '<img src="./images/next-slide1.webp" alt="">'],
        dots: 0,
        autoplay: 1,
        autoplayTimeout: 5000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1,
                dots: 0,
                nav: 0,
            },
            576: {
                items: 2,
                dots: 0,
                nav: 0,
            },
            767: {
                items: 2,
                dots: 0,
                nav: 0,
            },
            992: {
                items: 4,
            },
        }
    });

    $('.slide-brand').owlCarousel({
        items: 5,
        loop: 1,
        margin: 15,
        center: 1,
        nav: 1,
        navText: ['<img src="./images/prev-slide1.webp" alt="">', '<img src="./images/next-slide1.webp" alt="">'],
        dots: 0,
        autoplay: 1,
        autoplayTimeout: 5000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 2,
                dots: 0,
                nav: 0,
                center: 0,
            },
            576: {
                items: 3,
                dots: 0,
                nav: 0,
                center: 1,
            },
            992: {
                items: 5,
            },
        }
    });

    $('.slide-news').owlCarousel({
        items: 3,
        loop: 1,
        margin: 30,
        nav: 0,
        navText: ['<i class="ti-angle-left"></i>', '<i class="ti-angle-right"></i>'],
        dots: 0,
        autoplay: 1,
        autoplayTimeout: 5000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1,
                dots: 0,
                nav: 0,
            },
            767: {
                items: 2,
                dots: 0,
                nav: 0,
            },
            992: {
                items: 3,
            },
        }
    });

    $('.slide-customer').owlCarousel({
        items: 5,
        loop: 1,
        margin: 0,
        nav: 1,
        navText: ['<img src="./images/prev-slide1.webp" alt="">', '<img src="./images/next-slide1.webp" alt="">'],
        dots: 0,
        autoplay: 1,
        autoplayTimeout: 5000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 2,
                dots: 0,
                nav: 0,
            },
            767: {
                items: 3,
                dots: 0,
                nav: 0,
            },
            992: {
                items: 5,
            },
        }
    });

    $('.contact-list-slide').owlCarousel({
        items: 4,
        nav: 0,
        dots: 0,
        autoplay: 1,
        autoplayTimeout: 6000,
        loop: 1,
        responsive: {
            0: {
                items: 1,
                dots: 1,
            },
            768: {
                dots: 1,
                items: 2,
            },
            992: {
                dots: 0,
                items: 3,
            },
            1400: {
                items: 4,
            },
        },
    });

    $('.slide-new-product').owlCarousel({
        items: 1,
        loop: 1,
        margin: 10,
        nav: 0,
        navText: ['<img src="./images/prev-slide1.webp" alt="">', '<img src="./images/next-slide1.webp" alt="">'],
        dots: 1,
        autoplay: 1,
        autoplayTimeout: 5000,
        smartSpeed: 1000,

        responsive: {
            0: {
                items: 1,
                dots: 0,
                nav: 0,
            },
            767: {
                items: 2,
                dots: 0,
            },
            992: {
                items: 1,
            },
        }
    });

    $('.list-product-new-slide').owlCarousel({
        items: 4,
        nav: 1,
        dots: 0,
        loop: 1,
        autoplay: 1,
        autoplayTimeout: 5000,
        smartSpeed: 1000,
        navText: ['<img src="./html/style/images/prev-slide1.webp" alt="">', '<img src="./html/style/images/next-slide1.webp" alt="">'],
        responsive: {
            0: {
                items: 1,
                nav: 0,
                dots: 1,
            },
            768: {
                items: 3,
                nav: 0,
                dots: 1,
            },
            992: {
                items: 4,
                nav: 1,
                dots: 0,
            },
        }
    });

    let owl = $('.owl-carousel');
    owl.owlCarousel();
    $('.next-slide').click(function () {
        owl.trigger('next.owl.carousel');
    })
    $('.prev-slide').click(function () {
        owl.trigger('prev.owl.carousel', [300]);
    })

    $('.recruitment-detail .img-recruitment').click(() => {
        let offset = $('.form-recruitment').offset().top - $('header').outerHeight();

        $('body,html').animate({
            scrollTop: offset - 50
        }, 1000);
    })

    if ($(window).width() > 992) {
        let heightChild1 = $('header .hd-bottom .container .menu li .child1').outerHeight();

        $('header .hd-bottom .container .menu li .child1 li .child2').css('height', heightChild1);
    }

    setTimeout(function () {
        $('.popup').addClass('active');
        $('.close-icon-popup').addClass('active');
        $('.overlay-popup').addClass('show');
    }, 3000);

    $('.close-icon-popup').click(function () {
        $('.popup').removeClass('active');
        $(this).removeClass('active');
        $('.overlay-popup').removeClass('show');
    })

    $('.overlay-popup').click(function () {
        $('.popup').removeClass('active');
        $('.close-icon-popup').removeClass('active');
        $(this).removeClass('show');
    })

    setTimeout(function () {
        showNextItem();
    }, 60000);

    $('.list-question .item h2').click(function () {
        $('.list-question .item .paragraph').not($(this).next()).slideUp();
        $(this).next().slideToggle();
    })
});

let items = $(".curtomer-order .item");
let currentIndex = 0;
function showNextItem() {
    let currentItem = $(items[currentIndex]);
    items.removeClass('active');
    setTimeout(function () {
        currentIndex = (currentIndex + 1) % items.length;
        showNextItem();
    }, 60000);
    currentItem.addClass('active');
    setTimeout(function () {
        $(".curtomer-order .item").removeClass('active');;
    }, 10000);
}

function menuDropDown(event) {
    if (event.parent().hasClass('active')) {
        event.parent().removeClass('active');
        event.next().slideUp();
    }
    else {
        event.parent().addClass('active');
        event.next().slideDown();
    }
};

function myFunction(x) {
    x.classList.toggle("change");
    if ($('.hd-bottom').hasClass('active')) {
        $('.hd-bottom').removeClass('active');
        $('.overlay-menu').removeClass('active');
        $('body').removeClass('body-disscroll');
    } else {
        $('.hd-bottom').addClass('active');
        $('.overlay-menu').addClass('active');
        $('body').addClass('body-disscroll');
        $('.category .container .left').removeClass('show');
        $('.overlay').removeClass('show');
    }
}

$('.plus-icon').click(function () {
    if ($(this).hasClass("change")) {
        $(this).parent().siblings('ul').slideUp();
        $(this).parent().removeClass("active");
        $(this).removeClass("change");
    }
    else {
        $('.plus-icon').removeClass("change");
        $(this).toggleClass("change");
        $('.item .item-main').removeClass("active");
        $(this).parent().toggleClass("active");
        $('.item ul').slideUp();
        $(this).parent().siblings('ul').slideDown();
    }
});

$("a[href='#top']").click(function () {
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
});

//filter category
$('.category .container .right .title-main i').click(function () {
    let MenuFilter = $('.category .container .left');
    MenuFilter.addClass('show');
    $('body').addClass('body-disscroll');
    $('.overlay').addClass('show');
});

$('.category .container .left .title i').click(function () {
    let MenuFilter = $('.category .container .left');
    MenuFilter.removeClass('show');
    $('body').removeClass('body-disscroll');
    $('.overlay').removeClass('show');
});

// Gọi sự kiện resize khi trang được tải
$(window).trigger('resize');

$(document).ready(function () {
    // Tìm phần tử có class "text" và tạo mục lục
    let text = $(".detail-content.table-content");
    let tableContent = $('.table-content-show #toc');

    // Tìm tiêu đề trong phần văn bản và tạo mục lục
    let headings = text.find("h2, h3");
    if (headings.length > 0) {
        // Tạo danh sách mục lục
        let tocList = $("<ul></ul>");
        headings.each(function (index) {
            let heading = $(this);
            let title = heading.text();
            let listItem = $("<li></li>");
            let link = $("<a></a>").attr("href", "javascript:void(0)").text(title);
            listItem.append(link);

            // Đặt class cho mục lục dựa trên cấp độ của tiêu đề
            if (heading.is("h2")) {
                listItem.addClass("heading");
            } else if (heading.is("h3")) {
                listItem.addClass("subheading");
            }

            // Đặt định mức mục lục tùy thuộc vào cấp độ của tiêu đề
            let level = parseInt(heading.prop("tagName").substring(1));
            listItem.css("margin-left", (level - 3) * 15 + "px");

            // Xử lý sự kiện click để cuộn đến tiêu đề tương ứng
            link.on("click", function () {
                $('html, body').animate({
                    scrollTop: heading.offset().top - 200
                }, 500);
            });

            // Thêm mục lục vào danh sách mục lục
            tocList.append(listItem);
        });

        // Thêm danh sách mục lục vào mục lục
        tableContent.append(tocList);
    } else {
        $('.table-content-show').css('display', 'none');
    }
});

$('.more-toc').click(function () {
    $(this).toggleClass('active');
    $('.paragraph-toc').toggleClass('active');
});

$('.btn-show').click(function () {
    $('.form-advise').toggleClass('active');
    $('.overlay').toggleClass('show');
});

$('.icon-close').click(function () {
    $('.form-advise').toggleClass('active');
    $('.overlay').toggleClass('show');
});

function OpenAlert(msg, success) {
    $('.alrt-popup .main').html(msg);
    success == true ? $('.alrt-popup').addClass('success') : $('.alrt-popup').removeClass('success');
    $('.alrt-popup,.overlay').addClass('show');
    $('.close-alrt').click(function () {
        CloseAlert();
    });
}

$('.paragraph-toc .contents .title p i').click(function () {
    $('#toc').slideToggle();
});