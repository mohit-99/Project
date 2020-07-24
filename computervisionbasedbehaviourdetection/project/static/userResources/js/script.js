(function ($) {

    "use strict";

    //Hide Loading Box (Preloader)
    function handlePreloader() {
        if ($('.preloader').length) {
            $('.preloader').delay(200).fadeOut(500);
        }
    }

    //Update Header Style and Scroll to Top
    function headerStyle() {
        if ($('.main-header').length) {
            var windowpos = $(window).scrollTop();
            var siteHeader = $('.main-header');
            var scrollLink = $('.scroll-top');
            if (windowpos >= 110) {
                siteHeader.addClass('fixed-header');
                scrollLink.addClass('open');
            } else {
                siteHeader.removeClass('fixed-header');
                scrollLink.removeClass('open');
            }
        }
    }

    headerStyle();

    // dropdown menu
    var mobileWidth = 992;
    var navcollapse = $('.navigation li.dropdown');

    $(window).on('resize', function () {
        navcollapse.children('ul').hide();
    });

    navcollapse.hover(function () {
        if ($(window).innerWidth() >= mobileWidth) {
            $(this).children('ul').stop(true, false, true).slideToggle(300);
        }
    });

    //Submenu Dropdown Toggle
    if ($('.main-header .navigation li.dropdown ul').length) {
        $('.main-header .navigation li.dropdown').append('<div class="dropdown-btn"><span class="fa fa-angle-down"></span></div>');

        //Dropdown Button
        $('.main-header .navigation li.dropdown .dropdown-btn').on('click', function () {
            $(this).prev('ul').slideToggle(500);
        });

        //Disable dropdown parent link
        $('.navigation li.dropdown > a').on('click', function (e) {
            e.preventDefault();
        });
    }

    // Scroll to a Specific Div
    if ($('.scroll-to-target').length) {
        $(".scroll-to-target").on('click', function () {
            var target = $(this).attr('data-target');
            // animate
            $('html, body').animate({
                scrollTop: $(target).offset().top
            }, 1000);

        });
    }

    // Elements Animation
    if ($('.wow').length) {
        var wow = new WOW({
            mobile: false
        });
        wow.init();
    }

    //Contact Form Validation
    if ($('#contact-form').length) {
        $('#contact-form').validate({
            rules: {
                username: {
                    required: true
                },
                email: {
                    required: true,
                    email: true
                },
                phone: {
                    required: true
                },
                subject: {
                    required: true
                },
                message: {
                    required: true
                }
            }
        });
    }

    //Fact Counter + Text Count
    if ($('.count-box').length) {
        $('.count-box').appear(function () {

            var $t = $(this),
                n = $t.find(".count-text").attr("data-stop"),
                r = parseInt($t.find(".count-text").attr("data-speed"), 10);

            if (!$t.hasClass("counted")) {
                $t.addClass("counted");
                $({
                    countNum: $t.find(".count-text").text()
                }).animate({
                    countNum: n
                }, {
                    duration: r,
                    easing: "linear",
                    step: function () {
                        $t.find(".count-text").text(Math.floor(this.countNum));
                    },
                    complete: function () {
                        $t.find(".count-text").text(this.countNum);
                    }
                });
            }

        }, {accY: 0});
    }


    //LightBox / Fancybox
    if ($('.lightbox-image').length) {
        $('.lightbox-image').fancybox({
            openEffect: 'fade',
            closeEffect: 'fade',
            helpers: {
                media: {}
            }
        });
    }


    // clients-carousel
    if ($('.clients-carousel').length) {
        $('.clients-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: false,
            smartSpeed: 3000,
            autoplay: true,
            navText: ['<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 2
                },
                600: {
                    items: 3
                },
                800: {
                    items: 4
                },
                1200: {
                    items: 5
                }

            }
        });
    }


    //Testimonial Carousel
    if ($('.testimonial-carousel').length) {
        $('.testimonial-carousel').owlCarousel({
            animateOut: 'slideOutDown',
            animateIn: 'zoomIn',
            loop: true,
            margin: 30,
            nav: true,
            smartSpeed: 10000,
            autoHeight: true,
            autoplay: true,
            autoplayTimeout: 10000,
            navText: ['<span class=""></span>', '<span class=""></span>'],
            dots: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1024: {
                    items: 1
                }
            }
        });
    }

    //three-column-carousel
    if ($('.three-column-carousel').length) {
        $('.three-column-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            smartSpeed: 3000,
            autoplay: 4000,
            navText: ['<span class=""></span>', '<span class=""></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 2
                },
                800: {
                    items: 2
                },
                1024: {
                    items: 3
                }
            }
        });
    }


    //two-column-carousel
    if ($('.two-column-carousel').length) {
        $('.two-column-carousel').owlCarousel({
            loop: true,
            margin: 50,
            nav: true,
            smartSpeed: 3000,
            autoplay: 4000,
            navText: ['<span class=""></span>', '<span class=""></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 1
                },
                800: {
                    items: 2
                },
                1024: {
                    items: 2
                }
            }
        });
    }

    // Four Item Carousel
    if ($('.four-item-carousel').length) {
        $('.four-item-carousel').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            autoHeight: true,
            smartSpeed: 500,
            autoplay: 5000,
            navText: ['<span class=""></span>', '<span class=""></span>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                800: {
                    items: 3
                },
                1024: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });
    }

    //three-column-carousel
    if ($('.three-column-carousel-two').length) {
        $('.three-column-carousel-two').owlCarousel({
            loop: true,
            margin: 0,
            nav: true,
            smartSpeed: 3000,
            autoplay: 4000,
            navText: ['<span class=""></span>', '<span class=""></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 1
                },
                800: {
                    items: 2
                },
                1024: {
                    items: 3
                }
            }
        });
    }


    //Sortable Masonary with Filters
    function enableMasonry() {
        if ($('.sortable-masonry').length) {

            var winDow = $(window);
            // Needed variables
            var $container = $('.sortable-masonry .items-container');
            var $filter = $('.filter-btns');

            $container.isotope({
                filter: '*',
                masonry: {
                    columnWidth: '.masonry-item.small-column'
                },
                animationOptions: {
                    duration: 500,
                    easing: 'linear'
                }
            });


            // Isotope Filter 
            $filter.find('li').on('click', function () {
                var selector = $(this).attr('data-filter');

                try {
                    $container.isotope({
                        filter: selector,
                        animationOptions: {
                            duration: 500,
                            easing: 'linear',
                            queue: false
                        }
                    });
                } catch (err) {

                }
                return false;
            });


            winDow.on('resize', function () {
                var selector = $filter.find('li.active').attr('data-filter');

                $container.isotope({
                    filter: selector,
                    animationOptions: {
                        duration: 500,
                        easing: 'linear',
                        queue: false
                    }
                });
            });


            var filterItemA = $('.filter-btns li');

            filterItemA.on('click', function () {
                var $this = $(this);
                if (!$this.hasClass('active')) {
                    filterItemA.removeClass('active');
                    $this.addClass('active');
                }
            });
        }
    }

    enableMasonry();


    //Accordion Box
    if ($('.accordion-box').length) {
        $(".accordion-box").on('click', '.acc-btn', function () {

            var outerBox = $(this).parents('.accordion-box');
            var target = $(this).parents('.accordion');

            if ($(this).hasClass('active') !== true) {
                $(outerBox).find('.accordion .acc-btn').removeClass('active');
            }

            if ($(this).next('.acc-content').is(':visible')) {
                return false;
            } else {
                $(this).addClass('active');
                $(outerBox).children('.accordion').removeClass('active-block');
                $(outerBox).find('.accordion').children('.acc-content').slideUp(300);
                target.addClass('active-block');
                $(this).next('.acc-content').slideDown(300);
            }
        });
    }


    //Jquery Spinner / Quantity Spinner
    if ($('.quantity-spinner').length) {
        $("input.quantity-spinner").TouchSpin({
            verticalbuttons: true
        });
    }


    //Tabs Box
    if ($('.tabs-box').length) {
        $('.tabs-box .tab-buttons .tab-btn').on('click', function (e) {
            e.preventDefault();
            var target = $($(this).attr('data-tab'));

            if ($(target).is(':visible')) {
                return false;
            } else {
                target.parents('.tabs-box').find('.tab-buttons').find('.tab-btn').removeClass('active-btn');
                $(this).addClass('active-btn');
                target.parents('.tabs-box').find('.tabs-content').find('.tab').fadeOut(0);
                target.parents('.tabs-box').find('.tabs-content').find('.tab').removeClass('active-tab');
                $(target).fadeIn(300);
                $(target).addClass('active-tab');
            }
        });
    }


    // Select menu 
    function selectDropdown() {
        if ($(".selectmenu").length) {
            $(".selectmenu").selectmenu();

            var changeSelectMenu = function (event, item) {
                $(this).trigger('change', item);
            };
            $(".selectmenu").selectmenu({change: changeSelectMenu});
        }
        ;
    }


    // FLYOUT SEARCH BAR
    jQuery(".header-flyout-searchbar i").on("click", function () {
        jQuery("body").toggleClass("flyout-searchbar-active");
    });
    jQuery(".flyout-search-close").on("click", function () {
        jQuery("body").removeClass("flyout-searchbar-active");
    });


    // ------------------------------- AOS Animation
    if ($("[data-aos]").length) {
        AOS.init({
            duration: 1000,
            mirror: true
        });
    }


    if ($('.paroller').length) {
        $('.paroller').paroller({
            factor: 0.05,            // multiplier for scrolling speed and offset, +- values for direction control  
            factorLg: 0.05,          // multiplier for scrolling speed and offset if window width is less than 1200px, +- values for direction control  
            type: 'foreground',     // background, foreground  
            direction: 'horizontal' // vertical, horizontal  
        });
    }


    /*	=========================================================================
    When document is Scrollig, do
    ========================================================================== */

    jQuery(document).on('ready', function () {
        (function ($) {
            // add your functions
            selectDropdown();
        })(jQuery);
    });


    /* ==========================================================================
   When document is Scrollig, do
   ========================================================================== */

    $(window).on('scroll', function () {
        headerStyle();
    });


    /* ==========================================================================
   When document is loaded, do
   ========================================================================== */

    $(window).on('load', function () {
        handlePreloader();
        enableMasonry();
    });


})(window.jQuery);