    var bookSlug = document.getElementById('book_slug_id').value;
    var downloadBtn = document.getElementById('download_btn_id');
    var bookLikeBtn = document.getElementById('book_like_btn_id');
    var bookDislikeBtn = document.getElementById('book_dislike_btn_id');
    var likeCountContainer = document.getElementById('book_like_count_id');
    var dislikeCountContainer = document.getElementById('book_dislike_count_id');

    downloadBtn.addEventListener('click', bookDownloadFunc);
    function bookDownloadFunc() {
        objectDownloadIncrement("bk", bookSlug);
    }
    window.addEventListener("load", viewsInc);
    function viewsInc() {
        objectViewsIncrement("bk", bookSlug);
    }
    var closeBtn = document.getElementById('close_btn_alert_for_register_id');
    closeBtn.addEventListener('click', hideAlertForComment);
    function hideAlertForComment() {
        document.getElementById('alert_for_register_id').style.display = 'none';
    }

    function bookSectionsToggle(section) {
    var sections, btnsContainer, buttons, i, sectionsContainer;
    sectionsContainer = document.getElementById("sections_container_id");
    sections = sectionsContainer.getElementsByClassName("object-sections");
    btnsContainer = document.getElementById("extra_buttons_container_id");
    buttons = document.querySelectorAll("[class='btn']");
    for (i = 0; i < sections.length; i++) {
        sections[i].style.display = 'none';
        // buttons[i].style.color = 'white';
    }
    document.getElementById(section+"_section_id").style.display = 'block';
   // document.getElementById(section+"_btn_id").style.color = 'red';
    }

    var extraButtonsToggle = document.getElementById("extra_btn_toggle_id");
    extraButtonsToggle.addEventListener("click", extraBtnsToggle);
    function extraBtnsToggle(){
        var btnsContainer = document.getElementById("extra_buttons_container_id");
        if (btnsContainer.style.display === 'none'){
            btnsContainer.style.display = 'block';
        }
        else{
            btnsContainer.style.display = 'none';
        }
    }

    window.addEventListener("scroll", loadMoreObjects);
    function loadMoreObjects(){
        if($(window).scrollTop() + $(window).height() >  $(document).height() - $(document).height() /8){
            if(window.navigator.onLine === true && commentsLoaderComplete === false){
                    generalCommentsLoad(bookSlug, "bk");
            }
        }
    }