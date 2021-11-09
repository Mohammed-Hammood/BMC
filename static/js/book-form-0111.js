    var bookSlug = document.getElementById('book_slug_id').value;
    var form = document.getElementById('book_form_id');
    var formContainer = document.getElementById('main_book_form_container_id');

    function getFileName(event){
        var file;
            file = document.getElementById("id_file").files[0].name;
            document.getElementById("id_title").value = file;
    }

    function getBookForm() {
        $('#forms_container_id').show();
        $('#text_alert_id').hide();
        $('#main_tags_container_id').show();
        $('#upload_again_btn_id').hide();
        $('#progress_container_id').hide();
        $('#upload_btn_id').show();
        $('#main_created_tags_container_id').html("");
    }
    form.addEventListener("submit", preventBookFormEvents);
    function preventBookFormEvents(event) {
        event.preventDefault();
        $('#forms_container_id').hide();
        BookUpload();

    }
    function BookUpload() {
        var title = document.getElementById("id_title").value;
        var file = document.getElementById("id_file").files[0];
        var file_cdn = document.getElementById("id_file_cdn").value;
        var thumbnail_cdn = document.getElementById("id_thumbnail_cdn").value;
        var description = document.getElementById("id_description").value;
        var thumbnail = document.getElementById("id_thumbnail").value;
        var category = document.getElementById("id_category").value;
        var container = document.getElementById("main_created_tags_container_id");
        var tags = container.getElementsByClassName("single-tag-container");
        var data = new FormData(form);
        data.append("title", title);
        data.append("file", file);
        data.append("file_cdn", file_cdn);
        data.append("thumbnail_cdn", thumbnail_cdn);
        data.append("description", description);
        data.append("thumbnail", thumbnail);
        data.append("category", category);
        data.append("csrfmiddlewaretoken", csrf_token);
        data.append("count", tags.length.toString());
        for(var i = 0; i < tags.length; i++){
            var loop = tags[i];
            data.append(["tag_"+i].toString(), loop.id.split('_tag_container_id')[0]);
        }

        $.ajax({
            url: __upload_book_url__,
            type: 'POST',
            enctype: "multipart/form-data",
            processData:false,
            cache:false,
            dataType: "html",
            contentType:false,
            beforeSend: function (xhr) {
                uploadStart();
                var cancelBtn = document.getElementById('cancel_btn_id');
                cancelBtn.addEventListener("click", canceled);
                function canceled(){ xhr.abort(); uploadAbort();}
            },
            xhr:function(){
                var myXhr = $.ajaxSettings.xhr();
                myXhr.upload.addEventListener("progress", function (ev) {
                    if(ev.lengthComputable){
                        var percent = Math.round(ev.loaded * 100 / ev.total) + '%';
                            $('progress').attr({value: ev.loaded, max: ev.total});
                            $('#percent_id').html(percent)
                    }
                }, false); return myXhr
            },
            data: data,

            success: function (data) {
                if(data !== "None"){
                    $('#uploaded_book_container_id').append(data);
                    uploadFinished();
                }
                else {
                    uploadError();
                }
            },
            complete:function(){
                $('#upload_btn_id').css('display', 'none');
                $('#upload_again_btn_id').css('display', 'block');
                form.reset();
            },
            error: function (error) {
            console.log("Error: " + error.status + ', ' + error.statusText + ', '+ error)
            }
        });
    }
    function uploadAbort() {
        var alertText = $('#text_alert_id');
        alertText.attr("class", "alert alert-warning");
        alertText.html(uploading_canceled_text);
         $('#progress_container_id').fadeOut(1500);
        $('progress').attr("value", "0");
        $('#percent_id').html("0%")

    }
    function uploadFinished() {
        var alertText = $('#text_alert_id');
        $('#main_tags_container_id').hide();
        alertText.attr("class", "alert alert-success");
        alertText.html(uploading_finished_text);
        $('#progress_container_id').fadeOut(4000);
    }
    function uploadStart() {
        var alertText = $('#text_alert_id');
         $('#progress_container_id').show();
         $('#main_tags_container_id').hide();
         $('#main_loading_container_id').css("display", "block");
         alertText.attr("class", "alert alert-info");
         alertText.html(uploading_started_text);
    }
    function uploadError() {
        var alertText = $('#text_alert_id');
         $('#progress_container_id').hide();
         $('#main_tags_container_id').hide();
         $('#main_loading_container_id').css("display", "block");
         alertText.attr("class", "alert alert-warning");
         alertText.html(uploading_error_text);
    }

    function validFileInput() {
    var input = document.getElementById("id_thumbnail");
    if (input.files.length > 0) {getImage();}
    }
    function getImage() {
        var img = document.getElementById("img_id");
        var input = document.getElementById("id_thumbnail").files[0];
        var thumbnail_cdn = document.getElementById("id_thumbnail_cdn").value;
        var download_link_1 = document.getElementById("id_download_link_1").value;
        var download_link_2 = document.getElementById("id_download_link_2").value;
        var form = document.getElementById("book_form_id");
        var parent_slug = document.getElementById("book_slug_id").value;
        var data = new FormData(form);
        var type = "bk";
        data.append("img", input);
        data.append("type", type);
        data.append("thumbnail_cdn", thumbnail_cdn);
        data.append("download_link_1", download_link_1);
        data.append("download_link_2", download_link_2);
        data.append("parent_slug", parent_slug);
        data.append("csrfmiddlewaretoken", csrf_token);

        $.ajax({
            url:__change_thumbnail_url__,
            type:"POST",
            enctype: "multipart/form-data",
            dataType:"json",
            processData:false,
            cache:false,
            contentType:false,
            data: data,
            beforeSend:function () {
                img.src = __loader_progress_url__;
            },
            success:function (data) {
                if(data !== "None"){
                    img.src = data.src;
                }
                else {
                    // do nothing
                }
            },
            error:function (err) {
                console.log("err: ", err.statusText, ", ", err.status, err)
            }

        });
    }

    function preventBookUpdateFormEvents(event) {
        event.preventDefault();
        $('#main_book_form_container_id').hide();
        $('#loader_container_id').css("display", "block");
        BookUpdate();
    }
    function BookUpdate() {
        var title = document.getElementById("id_title").value;
        var description = document.getElementById("id_description").value;
        var parent_slug = document.querySelector("input[id='book_slug_id']").value;
        var thumbnail_cdn = document.getElementById("id_thumbnail_cdn").value;
        var file_cdn = document.getElementById("id_file_cdn").value;
        var download_link_1 = document.getElementById("id_download_link_1").value;
        var download_link_2 = document.getElementById("id_download_link_2").value;
        var category = document.getElementById("id_category").value;
        var container = document.getElementById("main_created_tags_container_id");
        var tags = container.getElementsByClassName("single-tag-container");
        var data = new FormData(form);
        data.append("title", title);
        data.append("description", description);
        data.append("thumbnail_cdn", thumbnail_cdn);

        data.append("file_cdn", file_cdn);
        data.append("download_link_1", download_link_1);
        data.append("download_link_2", download_link_2);
        data.append("category", category);
        data.append("parent_slug", parent_slug);
        data.append("csrfmiddlewaretoken", csrf_token);
        data.append("count", tags.length.toString());
        for(var i = 0; i < tags.length; i++){
            var loop = tags[i];
            data.append(["tag_"+i].toString(), loop.id.split('_tag_container_id')[0]);
        }

        $.ajax({
            url: __upload_update_url__,
            type: 'POST',
            enctype: "multipart/form-data",
            processData:false,
            cache:false,
            dataType: "html",
            contentType:false,
            data: data,
            success: function (data) {
                if(data !== "None"){
                    $('#card_body_id').html(data);
                }
                else {
                    // do nothing
                    console.log("nothing returned")
                }
            },
            complete:function(){
            },
            error: function (error) {
            console.log("Error: " + error.status + ', ' + error.statusText + ', '+ error)
            }
        });
    }
    var tagInput = document.getElementById("tag_input_id");
    tagInput.addEventListener("keypress", tagPD);
        function tagPD(event){
        if(event.keyCode === 13){TagsCreate("bk");}
    }
    window.addEventListener("load", getTagsCount);