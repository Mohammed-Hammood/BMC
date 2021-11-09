    function moreBtnsToggle(parent_slug, type){
    var btns = document.getElementById(type +"_more_btns_container_id_"+parent_slug);
    if (btns.style.display === 'none'){
        btns.style.display = 'block';
    }
    else{
        btns.style.display = 'none';
    }
    }

    function objectLikeToggle(parent_slug, type) {
        var likeBtn = document.getElementById(type+"_like_btn_id_"+parent_slug);
        var dislikeBtn = document.getElementById(type+"_dislike_btn_id_"+parent_slug);
        var likeCount = document.getElementById(type+"_like_count_id_" + parent_slug);
        var dislikeCount = document.getElementById(type+"_dislike_count_id_" + parent_slug);
        $.ajax({
            url: __general_object_like_toggle_url__,
            type: 'GET',
            dataType: "json",
            beforeSend:function(){
                if(likeBtn.style.color === "black"){
                    likeBtn.style.color = "blue";
                    likeCount.innerHTML = parseInt(likeCount.innerHTML) + 1;
                    if (dislikeBtn.style.color === "blue"){
                        dislikeBtn.style.color = "black";
                        dislikeCount.innerHTML = parseInt(dislikeCount.innerHTML) - 1;
                    }
                }else {
                     likeBtn.style.color = "black";
                     dislikeBtn.style.color = "black";
                     likeCount.innerHTML = parseInt(likeCount.innerHTML) - 1;
                }

            },
            data: {'parent_slug': parent_slug, "type": type},
            success: function(data){
                if(data !== 'None'){
                    // if(data.like_color !== likeBtn.style.color){likeBtn.style.color = data.like_color;}
                    // if(data.like_count !== parseInt(likeCount.innerHTML)){likeCount.innerHTML = data.like_count;}
                    // if(data.dislike_color !== dislikeBtn.style.color){dislikeBtn.style.color = data.dislike_color;}
                    // if(data.dislike_count !== parseInt(dislikeCount.innerHTML)){dislikeCount.innerHTML = data.dislike_count;}
                }
                else {
                    // do nothing..
                }
            },

            error:function (error) {
                console.log("Error: " + error.status + ', '+error.statusText + error)
            }
        })
    }

    function objectDislikeToggle(parent_slug, type) {
        var likeBtn = document.getElementById(type+"_like_btn_id_"+parent_slug);
        var dislikeBtn = document.getElementById(type+"_dislike_btn_id_"+parent_slug);
        var likeCount = document.getElementById(type+"_like_count_id_" + parent_slug);
        var dislikeCount = document.getElementById(type+"_dislike_count_id_" + parent_slug);
        $.ajax({
            url: __general_object_dislike_toggle_url__,
            type: 'GET',
            dataType: "json",
            beforeSend:function(){
                if(dislikeBtn.style.color === "black"){
                    dislikeBtn.style.color = "blue";
                    dislikeCount.innerHTML = parseInt(dislikeCount.innerHTML) + 1;
                    if(likeBtn.style.color === "blue"){
                     likeCount.innerHTML = parseInt(likeCount.innerHTML) - 1;
                     likeBtn.style.color = "black";
                    }
                }else {
                     dislikeBtn.style.color = "black";
                     likeBtn.style.color = "black";
                     dislikeCount.innerHTML = parseInt(dislikeCount.innerHTML) - 1;
                }
            },
            data: {'parent_slug': parent_slug, "type": type},
            success: function(data){
                if(data !== 'None'){
                    // if(data.like_color !== likeBtn.style.color){likeBtn.style.color = data.like_color;}
                    // if(data.like_count !== parseInt(likeCount.innerHTML)){likeCount.innerHTML = data.like_count;}
                    // if(data.dislike_color !== dislikeBtn.style.color){dislikeBtn.style.color = data.dislike_color;}
                    // if(data.dislike_count !== parseInt(dislikeCount.innerHTML)){dislikeCount.innerHTML = data.dislike_count;}
                }
                else {
                    // do nothing..
                }
            },

            error:function (error) {
                console.log("Error: " + error.status + ', '+error.statusText + error)
            }
        })
    }

    function generalCommentAdd(event, type) {
    var parent_slug = event.target.id.split(type + '_comment_form_id-')[1];
    var form = document.getElementById(event.target.id);
    var comment = form.elements["comment"].value;
        $.ajax({
            url: __general_comment_add_url__,
            type: 'POST',
            dataType: "html",
            data: {'comment': comment, "parent_slug": parent_slug, "type": type},
            beforeSend: function () {
                form.reset();
            },
            success: function(data){
                if (data !== 'None'){
                    $("#main_"+ type + "_comments_container_id-"+ parent_slug).prepend(data);
                }
                else {
                    /// Do Nothing...
                }
            },
            complete:function () {
              getCommentsCount(parent_slug, type);
            },
            error:function (error) {
                console.log("Error: " + error.status +', ' +error.statusText + error)
            }
        })
    }

    function generalObjectDelete(objectSlug, type) {
        $('#ObjectDeleteModal').modal();
        document.getElementById("confirm_obj_del_btn_id").addEventListener("click", delObj);
        function delObj() {
            $.ajax({
                url: __general_object_delete_url__,
                dataType: "json",
                type: "POST",
                data: {"objectSlug": objectSlug, "type": type},
                beforeSend:function () {
                    document.getElementById("obj_del_content_container_id").style.display = "none";
                    document.getElementById("d-p-loader").style.display = "block";
                },
                success:function (data) {
                    if (data !== "None"){
                        document.getElementById("single_"+type+"_container_id_" + objectSlug).innerHTML = "";
                    }
                    else {
                        // do nothing...
                    }
                },
                complete:function () {
                    $('#ObjectDeleteModal').modal('hide');
                    document.getElementById("obj_del_content_container_id").style.display = "block";
                    document.getElementById("d-p-loader").style.display = "none";
                },
                error:function (xhr, status, err) {
                    console.log("xhr: "+ xhr + ", status: " + status + ", err: " + err);
                }
            })

        }
        document.getElementById('cancel_obj_del_btn_id').addEventListener('click', cancelObjDel);
        function cancelObjDel() {
            $('#ObjectDeleteModal').modal('hide');
            type = '';
            objectSlug = '';
        }
    }

    function generalCommentsSort(parent_slug, type) {
        var sort = document.getElementById(type+'_comments_sort_id-'+ parent_slug).selectedIndex;
        var sortTypeStorage = document.getElementById(type+'_sort_type_storage_id-'+parent_slug);
        var btnLoader = document.getElementById(type+'_btn_comments_loader_id-' +parent_slug);
        var imgLoader = document.getElementById(type+'_img_comments_loader_id-'+parent_slug);
        var mainContainer =  document.getElementById("main_"+type+"_comments_container_id-"+parent_slug);
        var loadedComments = mainContainer.getElementsByClassName("single-comment-container").length;
        var loaderContainer = document.getElementById(type+"_comments_loader_container_id-"+parent_slug);
        var commentsCount = document.getElementById(type+"_comments_count_container_id-"+parent_slug).innerHTML;
        $.ajax({
            url:__general_comments_sort_url__,
            dataType: "html",
            type: "POST",
            data: {"sort": sort, "parent_slug": parent_slug, "type": type, "number": loadedComments},
            beforeSend: function () {
                loaderContainer.style.display = 'flex';
                btnLoader.style.display = 'none';
                imgLoader.style.display = 'block';
                $("#main_"+type+"_comments_container_id-"+parent_slug).html('');
                getCommentsCount(parent_slug, type);
            },
            success:function (data) {
                btnLoader.style.display = 'inline';
                imgLoader.style.display = 'none';
                $("#main_"+type+"_comments_container_id-"+parent_slug).html(data);
            },
            complete:function(){
                sortTypeStorage.value = sort;
                getCommentsCount(parent_slug, type);
                var loadedLength = mainContainer.getElementsByClassName("single-comment-container").length;
                if (parseFloat(commentsCount) === loadedLength) {
                        loaderContainer.style.display = 'none';
                    }
                    else {
                        loaderContainer.style.display = 'flex';
                    }
            },
            error: function (err) {
            console.log(" Error: " +err.status+ ", " + err.statusText + ", " +err)
            }
        })
    }
    var commentsLoaderComplete = false;
    function generalCommentsLoad(parent_slug, type) {
        var sortTypeStorage = document.getElementById(type+'_sort_type_storage_id-'+parent_slug).value;
        var btnLoader = document.getElementById(type+'_btn_comments_loader_id-' +parent_slug);
        var imgLoader = document.getElementById(type+'_img_comments_loader_id-'+parent_slug);
        var mainContainer =  document.getElementById("main_"+type+"_comments_container_id-"+parent_slug);
        var loadedComments = mainContainer.getElementsByClassName("single-comment-container").length;
        var loaderContainer = document.getElementById(type+"_comments_loader_container_id-"+parent_slug);
        var commentsCount = document.getElementById(type+"_comments_count_container_id-"+parent_slug).innerHTML;
        $.ajax({
            url:__general_comments_load_url__,
            dataType: "html",
            type: "POST",
            data: {"sort": sortTypeStorage, "parent_slug": parent_slug, "type": type, "number": loadedComments},
            beforeSend: function () {
                commentsLoaderComplete = true;
                loaderContainer.style.display = 'flex';
                btnLoader.style.display = 'none';
                imgLoader.style.display = 'block';

            },
            success:function (data) {
                btnLoader.style.display = 'inline';
                imgLoader.style.display = 'none';
                if (data !== "None"){
                    $("#main_"+type+"_comments_container_id-"+parent_slug).append(data);
                }
                else {
                    // Do nothing..
                }
            },
            complete:function(){
                sortTypeStorage.value = sortTypeStorage;
                var loadedLength = mainContainer.getElementsByClassName("single-comment-container").length;
                if (parseFloat(commentsCount) === loadedLength) {
                    loaderContainer.style.display = 'none';
                    commentsLoaderComplete = true;
                    }
                else {
                    loaderContainer.style.display = 'flex';
                    commentsLoaderComplete = false;
                    }
            },
            error: function (err) {
            console.log(" Error: " +err.status+ ", " + err.statusText + ", " +err)
            }
        })
    }

    function getFileName(event) {
        var form = document.getElementById(event.target.form.id);
        var title = form.elements["id_title"];
        title.value = event.target.files.item(0).name;
    }

    function tagViewInc(type, tag_slug){
        $.ajax({
            url: __tag_views_inc_url__,
            dataType: "json",
            data: {"tag_slug": tag_slug, "type": type},
            type: "POST",
            success:function (data) {
                if (data !== "None"){
                   // do nothing
                }
                else {
                    // do nothing...
                }
            },
            error:function (xhr, status, err) {
                console.log("xhr: "+ xhr + ", status: " + status + ", err: " + err);
            }
        })

    }

    function generalCommentLikeToggle(commentSlug, type) {
        var likeBtn = document.getElementById('comment_like_btn_'+commentSlug);
        var dislikeBtn = document.getElementById('comment_dislike_btn_'+commentSlug);
        var LikeCountContainer = document.getElementById('comment_like_count_' + commentSlug);
        var DislikeCountContainer = document.getElementById('comment_dislike_count_' + commentSlug);
        $.ajax({
         url: __general_comment_like_toggle_url__,
         type: 'GET',
         dataType: "json",
         data: {"comment_slug": commentSlug, "type": type},
         success: function (data) {
             likeBtn.style.color = data.like_color;
             dislikeBtn.style.color = data.dislike_color;
             LikeCountContainer.innerHTML = data.like_count;
             DislikeCountContainer.innerHTML = data.dislike_count;
         },
         error: function (error) {
             console.log("Error: " + error.status + ', ' + error.statusText + ', '+ error)
         }
        });
    }

    function generalCommentDislikeToggle(commentSlug, type) {
        var likeBtn = document.getElementById('comment_like_btn_'+commentSlug);
        var dislikeBtn = document.getElementById('comment_dislike_btn_'+commentSlug);
        var LikeCountContainer = document.getElementById('comment_like_count_' + commentSlug);
        var DislikeCountContainer = document.getElementById('comment_dislike_count_' + commentSlug);
        $.ajax({
         url: __general_comment_dislike_toggle_url__,
         type: 'GET',
         dataType: "json",
         data: {"comment_slug": commentSlug, "type": type},
         success: function (data) {
             likeBtn.style.color = data.like_color;
             dislikeBtn.style.color = data.dislike_color;
             LikeCountContainer.innerHTML = data.like_count;
             DislikeCountContainer.innerHTML = data.dislike_count;
         },
         error: function (error) {
             console.log("Error: " + error.status + ', ' + error.statusText + ', '+ error)
         }
        });
    }

    function generalCommentDeletion(parent_slug, comment_slug, type) {
        $("#CommentDeletionModal").modal();
        document.getElementById('confirm_comment_delete_id').addEventListener('click', function () {
             $.ajax({
                 url: __general_comment_delete_url__,
                 dataType: "json",
                 type:'POST',
                 data: {"comment_slug": comment_slug, "type": type},
                 beforeSend:function () {
                     $('#CommentDeletionModal').modal('hide');
                 },
                 success:function (data) {
                     if (data !== 'None'){
                        $('#single_comment_container_id_'+ comment_slug).html('');
                        }
                        else {
                        //could-not-deleted
                     }
                 },
                 complete:function () {
                     getCommentsCount(parent_slug, type);
                 },
                 error: function (err) {
                    console.log(" Error: " +err.status+ " " + err.statusText + ", " +err)
                }
             })
        });
        document.getElementById('cancel_comment_delete_btn_id').addEventListener('click', function () {
            comment_slug = 0;
            type = '';
        })
    }

    function getGeneralCForm(comment_slug, type) {
        $.ajax({
            url:__get_general_comment_form_url__,
            dataType: "html",
            type:'POST',
            data: {"comment_slug": comment_slug, "type": type},
            success:function (data) {
                if(data !== 'None'){
                    $('#CommentUpdateModal').modal();
                    $('#modal_comment_form_update_container_id').html(data);
                }
                else {
                    //No data...
                }
            },
            error: function (err) {console.log("Error: " + err.status + ", " + err.statusText + ", " + err)}
         })
    }
    function generalCUPD(event, comment_slug, type){
    event.preventDefault();
    SaveCommentUpdate(comment_slug, type);
    }

    function SaveCommentUpdate(comment_slug, type) {
        var comment = document.getElementById('comment_update_form-'+ comment_slug).elements['comment'].value;
        $.ajax({
            url: __save_comment_changes_url__,
            type: 'POST',
            dataType: "html",
            data: {'comment': comment, "comment_slug": comment_slug, "type": type},
            beforeSend:function () {
                $('#CommentUpdateModal').modal('hide');
                $('#modal_comment_form_update_container_id').html('');
            },
            success: function(data){
                if (data !== 'None'){
                    $('#single_comment_container_id_'+ comment_slug).html(data);
                }
                else {
                 // Do nothing ...
                }
            },
            error:function (xhr, status, err) {
                console.log("xhr: " + xhr + ', ' + status + ', '+ err)
            }
        })
    }

    function preventCFEvents(event, type) {
     event.preventDefault();
     generalCommentAdd(event, type);
    }

    function sectionsToggle(parent_slug, type, section) {
    var sections, btnsContainer, buttons, i, sectionsContainer;
    sectionsContainer = document.getElementById(type+"_sections_container_id_"+parent_slug);
    sections = sectionsContainer.getElementsByClassName("object-sections");
    btnsContainer = document.getElementById(type+"_more_btns_container_id_"+parent_slug);
    buttons = btnsContainer.getElementsByTagName("button");
    for (i = 0; i < sections.length; i++) {
        sections[i].style.display = 'none';
        buttons[i].style.color = 'white';
    }
    document.getElementById(type+"_"+section+"_section_id_"+parent_slug).style.display = 'block';
    document.getElementById(type+"_"+section+"_btn_id_"+parent_slug).style.color = 'red';
    }
    function getCommentsCount(parent_slug, type){
            $.ajax({
            url: __general_comment_count_url__,
            type: 'POST',
            dataType: "json",
            data: {"parent_slug": parent_slug, "type": type},
            success: function(data){
                if(data !== 'None'){
                    $("#"+ type +"_comments_count_container_id-"+ parent_slug).html(data);
                    $("#"+ type +"_comments_count_id_"+ parent_slug).html(data);
                }
                else {
                    // do nothing..
                }
            },
            error:function (error) {
                console.log("Error: " + error.status + error.statusText + error)
            }
        })
    }

    var objectsLoaderToggle = false;
    function generalObjectsLoader(type, tag, filter, loadCount, parent_slug) {
        var container = document.getElementById("main_objects_container_id");
        var objectsCount = container.getElementsByClassName("single-object-container");
        var imgLoader = document.getElementById("img_loader_id");
        var textLoader = document.getElementById("btn_loader_id");
        var searchValue = document.getElementById("search_value_id").value;
        var category = document.getElementById('category_value_id').value;
        var total = document.getElementById("total_objects_id").value;
        var mainLoaderCont = document.getElementById("objects_loader_container_id");
        $.ajax({
            url: __general_objects_loader_url__,
            dataType: "html",
            type: "POST",
            beforeSend:function(xhr){
                objectsLoaderToggle = true;
                imgLoader.style.display = 'block';
                textLoader.style.display = 'none';
            },
            data: {"parent_slug": parent_slug, "loadCount":loadCount,
                "filter":filter, "tag":tag, "objectsCount": objectsCount.length,
                "searchValue":searchValue, "type":type, "c": category
            },
            success: function (data) {
                if(data !== "None"){$("#main_objects_container_id").append(data);}
                else {
                    // do nothing..
                }
            },
            complete:function(){
                if(objectsCount.length >= parseInt(total)){
                    // true means all objects have been loaded.
                    objectsLoaderToggle = true;
                    mainLoaderCont.style.display = "none";
                }else {
                    objectsLoaderToggle = false;
                    imgLoader.style.display = 'none';
                    textLoader.style.display = 'block';
                }

            },

            error:function (xhr, status, statusText) {
                console.log("error: ",status,', statusText: , ', statusText);
            }
        })
    }

    // general tags functions
    function removeTag(tag_slug){
        var container = document.getElementById("main_created_tags_container_id");
        var tag = document.getElementById(tag_slug+"_tag_container_id");
        container.removeChild(tag);
        getTagsCount();
    }

    function TagsCreate(type) {
        var tag = document.getElementById("tag_input_id");
        $.ajax({
            url: __general_tags_create_url__,
            dataType: "html",
            data: {"tag": tag.value, "type": type},
            type: "POST",
            beforeSend:function () {
                tag.value = '';
            },
            success:function (data) {
                if (data !== "None"){
                    $('#main_created_tags_container_id').prepend(data);
                }
                else {
                    // do nothing...

                }
            },
            complete:function () {
                tag.value = "";
                // tag.value.replace("\n", "");
                tag.value.replace(/(\r?\n|\r\n?)/, "");
                getTagsCount();
            },
            error:function (xhr, status, err) {
                console.log("xhr: "+ xhr + ", status: " + status + ", err: " + err);
            }
        })
        }

    function getTagsCount(){
        var container ,tags, input;
            input = document.getElementById("tag_input_id");
            container = document.getElementById("main_created_tags_container_id");
            tags = container.getElementsByClassName("single-tag-container");
            if(tags.length >= 8){
                // please do not try to change the limited no of tags because we only
                // allow to save 7 tags event if the code in front end allow more thant that
                input.setAttribute("disabled", "")
            }
            else {
                input.removeAttribute("disabled")
            }
    }
    // general tags function end

    function generalFriendShipRequest(friend) {
        // var FriendshipBtn = document.getElementById("friendship_btn_id");
        var FriendshipIcon = document.getElementById(friend+"_friendship_icon_id");
        var FriendshipText = document.getElementById(friend+"_friendship_text_id");
        $.ajax({
            url: __friendship_request_toggle_url__,
            dataType: "json",
            type:'POST',
            data: {"friend": friend},
            success:function (data) {
                if(data !== 'None'){
                    FriendshipIcon.className = data.friendship_icon;
                    FriendshipText.innerHTML = data.friendship_text;
                }
                else {
                    //No data...
                    // SOTTH();
                }
            },
            error: function (err) {console.log("Error: " + err.status + ", " + err.statusText + ", " + err)}
         })
    }

    function generalFriendshipToggle(friend, status, type) {
        $.ajax({
            url: __friendship_friend_toggle_url__,
            dataType: "html",
            type:'POST',
            beforeSend:function(){
                if(type === "rq"){
                    var FrndReqNotification = document.getElementById("friend_request_notif_count_contr_id");
                    var FrndReqCount = document.getElementById("friend_request_count_contr_id");
                    var container = document.getElementById("friends_requests_container_id");
                    var request = document.getElementById("f_r_id_"+friend);
                    container.removeChild(request);
                    if(parseInt(FrndReqNotification.innerHTML) <= 1){
                        FrndReqNotification.innerHTML = parseInt(FrndReqNotification.innerHTML) - 1;
                        FrndReqCount.innerHTML = parseInt(FrndReqCount.innerHTML) - 1;
                        FrndReqNotification.style.display = "none";
                    }
                    else{
                        FrndReqNotification.innerHTML = parseInt(FrndReqNotification.innerHTML) - 1;
                        FrndReqCount.innerHTML = parseInt(FrndReqCount.innerHTML) - 1;
                    }
                }
            },
            data: {"friend": friend, "status": status},
            success:function (data) {
                if(data !== 'None'){
                    if(window.location.pathname.match("/a/") ||window.location.pathname.match("/users/")){
                        document.getElementById(friend+"_friendship_btns_container_id").innerHTML = data
                    }
                }
                else {
                    //No data...
                }
            },
            error: function (err) {console.log("Error: " + err.status + ", " + err.statusText + ", " + err)}
         })
    }

    function objectDownloadIncrement(type, parent_slug){
        $.ajax({
            url: __object_download_increment_url__,
            dataType: "json",
            data: {"parent_slug": parent_slug, "type": type},
            type: "POST",
            success:function (data) {
                // do nothing..
            },
            error:function (xhr, status, err) {
                console.log("xhr: "+ xhr + ", status: " + status + ", err: " + err);
            }
        });

    }

    function objectViewsIncrement(type, parent_slug){
        $.ajax({
            url: __object_views_increment_url__,
            dataType: "json",
            data: {"parent_slug": parent_slug, "type": type},
            type: "POST",
            success:function (data) {
                // do nothing..
            },
            error:function (xhr, status, err) {
                console.log("xhr: "+ xhr + ", status: " + status + ", err: " + err);
            }
        });

    }

    function followToggle(uploader) {
        var followBtn = document.getElementById(uploader+'_follow_btn_id');
        var countContainer = document.getElementById(uploader+'_follow_count_id');
        var textStatus = document.getElementById(uploader+'_follow_text_status_id');

        $.ajax({
         url: __general_follow_url__,
         type: 'POST',
         dataType: "json",
         data: {"uploader": uploader},
         success: function (data) {
             if(data !== "None"){
                 followBtn.className = data.class;
                 countContainer.innerHTML = data.count;
                 textStatus.innerHTML = data.textStatus;
             }
             else{
                 // do nothing
             }
         },
         error: function (error) {
             console.log("Error: " + error.status + ', ' + error.statusText + ', '+ error)
         }
        });
    }

    function loginModal() {
        $('#LoginModel').modal();
    }
