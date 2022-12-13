const carousel = document.querySelector(".carousel"),

    firstImg = carousel.querySelectorAll("img")[0],
    arrowIcons = document.querySelectorAll(".wrapper button");

    slides = carousel.querySelectorAll("img")
    clonefirst = firstImg.cloneNode(true);
    clonelast = slides[slides.length - 1].cloneNode(true);
    clonefirst.style.display = 'none';
    carousel.append(clonefirst);
    slick = document.querySelectorAll('.slick-item');
    slick[0].classList.add('active');
    active_slick = 0;
    check_limit = 0;
    slick_limit = slick.length;
    var slidesLength = slides.length;
    let isDragStart = false, isDragging = false, prevPageX, prevScrollLeft, positionDiff;
    const showHideIcons = () => {
        // showing and hiding prev/next icon according to carousel scroll left value
        let scrollWidth = carousel.scrollWidth - carousel.clientWidth; // getting max scrollable width
        arrowIcons[0].style.display = carousel.scrollLeft == 0 ? "none" : "block";
        arrowIcons[1].style.display = carousel.scrollLeft == scrollWidth ? "none" : "block";
    }
    arrowIcons.forEach(icon => {
        icon.addEventListener("click", () => {
            let firstImgWidth = firstImg.clientWidth + 14; // getting first img width & adding 14 margin value
            // if clicked icon is left, reduce width value from the carousel scroll left else add to it
            carousel.scrollLeft += icon.id == "left" ? -firstImgWidth : firstImgWidth;
            setTimeout(() => showHideIcons(), 60); // calling showHideIcons after 60ms
            if(icon.id == "left"){
                if(active_slick > 0){
                    slick[active_slick].classList.remove('active');
                    slick[active_slick-1].classList.add('active');
                    active_slick--;
                }
            }
            if(icon.id == "right"){
                if(active_slick < slick_limit - 1){
                    slick[active_slick].classList.remove('active');
                    slick[active_slick+1].classList.add('active');    
                }
                active_slick++;
                if(active_slick == slick_limit - 2){
                    carousel.lastChild.style.display = 'inline'
                }
                if(active_slick == slick_limit){
                    slick[active_slick-1].classList.remove('active');
                    slick[0].classList.add('active');
                    setTimeout(function(){
                        carousel.classList.add('dragging');
                        carousel.scrollLeft = 0;
                        carousel.classList.remove('dragging');
                        active_slick = 0;
                    }, 300);    
                } 
            }
            
        });
    });
    const autoSlide = () => {
        // if there is no image left to scroll then return from here

        positionDiff = Math.abs(positionDiff); // making positionDiff value to positive
        let firstImgWidth = firstImg.clientWidth + 14;
        // getting difference value that needs to add or reduce from carousel left to take middle img center
        let valDifference = firstImgWidth - positionDiff;
        if(carousel.scrollLeft > prevScrollLeft) { // if user is scrolling to the right
            if(active_slick < slick_limit - 1){
                slick[active_slick].classList.remove('active');
                slick[active_slick+1].classList.add('active');    
            }
            active_slick++;
            if(active_slick == slick_limit - 2){
                carousel.lastChild.style.display = 'inline'
            }
            return carousel.scrollLeft += positionDiff > firstImgWidth / 4 ? valDifference : -positionDiff;
        }
        // if user is scrolling to the left
        if(active_slick > 0){
            slick[active_slick].classList.remove('active');
            slick[active_slick-1].classList.add('active');
            active_slick--;
        }
        
        carousel.scrollLeft -= positionDiff > firstImgWidth / 4 ? valDifference : -positionDiff;
    }
    const dragStart = (e) => {
        // updatating global variables value on mouse down event
        isDragStart = true;
        prevPageX = e.pageX || e.touches[0].pageX;
        prevScrollLeft = carousel.scrollLeft;
    }
    const dragging = (e) => {
        // scrolling images/carousel to left according to mouse pointer
        if(!isDragStart) return;
        e.preventDefault();
        isDragging = true;
        carousel.classList.add("dragging");
        positionDiff = (e.pageX || e.touches[0].pageX) - prevPageX;
        carousel.scrollLeft = prevScrollLeft - positionDiff;
        showHideIcons();
    }
    const dragStop = () => {
        isDragStart = false;
        carousel.classList.remove("dragging");
        if(!isDragging) return;
        isDragging = false;
        autoSlide();
        if(active_slick == slick_limit){
            slick[active_slick-1].classList.remove('active');
            slick[0].classList.add('active');
            setTimeout(function(){
                carousel.classList.add('dragging');
                carousel.scrollLeft = 0;
                carousel.classList.remove('dragging');
                active_slick = 0;
            }, 300);    
        }         
    }  
    carousel.addEventListener("mousedown", dragStart);
    carousel.addEventListener("touchstart", dragStart);
    document.addEventListener("mousemove", dragging);
    carousel.addEventListener("touchmove", dragging);
    document.addEventListener("mouseup", dragStop);
    carousel.addEventListener("touchend", dragStop);

$(document).ready(function() {
        var elementPosition = $('.proceed-to-checkout').offset();
        $(window).scroll(function(){
                if($(window).scrollTop() > elementPosition.top){
                    $('.stickyBtn').slideDown();
                } else {
                    $('.stickyBtn').slideUp();
                }    
        });
     })

