
    function bookDownloadFunc(arg) {
        objectDownloadIncrement("bk", arg);
    }
    document.getElementById('search_form_id').addEventListener('submit', validSearch);
    function validSearch(event) {
        console.log("work");
        var input = document.getElementById('search_value_id');
        if(input.value.trim() === ''){
            input.value = '';

            event.preventDefault();
        }
    }
    var objectsLoadBtn = document.querySelector("div[id='main_objects_loader_container_id']");
    objectsLoadBtn.addEventListener("click", loadMoreObjects);


    window.addEventListener("scroll", loadMoreObjects);
    function loadMoreObjects(){
        if($(window).scrollTop() + $(window).height() >  $(document).height() - $(document).height() /8){
            if(window.navigator.onLine === true && objectsLoaderToggle === false){
                  if(document.location.pathname.match("tags=")){
                      const tag = document.location.pathname.split("tags=")[1];
                        generalObjectsLoader("bk", tag);
                  }
                  else if (document.location.pathname.match("liked_books")){
                        generalObjectsLoader("bk", "", "like");
                  }
                  else if (document.location.pathname.match("/category=")){
                      const ca = document.location.pathname.split("/category=")[1];
                      generalObjectsLoader("bk", "", "cy", 3, ca);
                  }
                  else if (document.location.pathname.match("/a/uploaders/") ) {
                      generalObjectsLoader("bk", "", "p", 1);
                  }
                   else if (document.location.pathname.match("/a/") ) {
                      const uploader = document.location.pathname.split("/a/")[1];
                      generalObjectsLoader("bk", "", "a", 4, uploader);
                  }
                  else {
                      generalObjectsLoader("bk");}
            }
        }
    }





