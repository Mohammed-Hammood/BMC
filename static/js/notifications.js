    var notificationsLoaderToggle = false;
    var objectsLoadBtn = document.querySelector("div[id='main_notifications_loader_container_id']");
    objectsLoadBtn.addEventListener("click", loadMoreObjects);
    window.addEventListener("scroll", loadMoreObjects);
    function loadMoreObjects(){
        if($(window).scrollTop() + $(window).height() >  $(document).height() - $(document).height() /8){
            if(window.navigator.onLine === true && notificationsLoaderToggle === false){
                notificationsLoader();

            }
        }
    }



    function notificationsLoader(loadCount) {
        var container = document.getElementById("main_notifications_container_id");
        var objectsCount = container.getElementsByClassName("single-notification-container");
        var imgLoader = document.querySelector("img[id='img_loader_id'");
        var textLoader = document.querySelector("div[id='btn_loader_id']");
        var total = document.querySelector("input[id='total_notifications_id'").value;
        var mainLoaderCont = document.querySelector("div[id='objects_loader_container_id']");
        $.ajax({
            url: __notifications_loader_url__,
            dataType: "html",
            type: "POST",
            beforeSend:function(xhr){
                notificationsLoaderToggle = true;
                imgLoader.style.display = 'block';
                textLoader.style.display = 'none';
            },
            data: {"loadCount":loadCount, "objectsCount": objectsCount.length},
            success: function (data) {
                if(data !== "None"){$("#main_notifications_container_id").append(data);}
                else {
                    // do nothing..
                    console.log("nothing....");
                }
            },
            complete:function(){
                if(objectsCount.length >= parseInt(total)){
                    // true means all objects have been loaded.
                    notificationsLoaderToggle = true;
                    mainLoaderCont.style.display = "none";
                }else {
                    notificationsLoaderToggle = false;
                    imgLoader.style.display = 'none';
                    textLoader.style.display = 'block';
                }

            },

            error:function (xhr, status, statusText) {
                console.log("error: ",status,', statusText: , ', statusText);
            }
        })
    }



