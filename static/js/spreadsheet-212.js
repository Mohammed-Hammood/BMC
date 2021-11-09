    window.addEventListener("load", setMaterialValue);
    function setMaterialValue() {
        if(!window.location.pathname.match("/spreadsheets")){
            const container = document.getElementById('material_options_container_id');
            const material = container.querySelector("#id_material");
            const stored = document.getElementById("material_value_id");
            if(stored.value !== ""){
                material.value = stored.value;
            }else{
                material.options[0].setAttribute("selected", "");
            }
        }
    }
    function setFilterStartDate() {
        const startDate = document.getElementById("start_date_input_id");
        const endDate = document.getElementById("end_date_input_id");
        if(endDate.value < startDate.value){
            startDate.value = endDate.value;
        }
    }
    function setFilterEndDate() {
        const startDate = document.getElementById("start_date_input_id");
        const endDate = document.getElementById("end_date_input_id");
        if(startDate.value > endDate.value){
            endDate.value = startDate.value;
        }
    }
    function lectureSectionsToggle(id) {
        var container = document.getElementById("main_sections_container_id");
        const sections = container.getElementsByClassName("single-section-container");
        if(document.getElementById(id).style.display === "none"){
            for (var i = 0; i< sections.length; i++){
                var loop = sections[i];
                loop.style.display = "none";
            }
            document.getElementById(id).style.display = "block";
        }
        else {
            for (i = 0; i< sections.length; i++){
                loop = sections[i];
                loop.style.display = "none";
            }
        }
    }
    function copySharingLink() {
        const link = document.getElementById('sharing_link_input_id');
        link.select();
        document.execCommand("copy");
    }
    var spreadsheet_form = document.getElementById('spreadsheet_form_id');
    spreadsheet_form.addEventListener("submit", create_spreadsheet);
    function create_spreadsheet(event) {
        event.preventDefault();
        var title = spreadsheet_form.querySelector("input").value;
        $.ajax({
            url: __create_new_spreadsheet_url__,
            type: 'POST',
            dataType: "html",
            data: {'title': title,},
            beforeSend: function () {
                spreadsheet_form.reset();
            },
            success: function(data){
                if (data !== 'None'){
                    $("#main_objects_container_id").prepend(data);
                    const count = document.getElementById('spreadsheet_count_cont_id');
                    count.innerHTML = parseInt(count.innerHTML) + 1;
                }
                else {
                    /// Do Nothing...
                }
            },
            error:function (error) {
                console.log("Error: " + error.status +', ' +error.statusText + error)
            }
        })
    }
    function contributorSectionsToggle(id){
        var container = document.getElementById("contributors_section_container_id");
        const sections = container.getElementsByClassName("single-contributor-container");
        if(document.getElementById(id+"_contributor_container_id").style.display === "none"){
            for (var i = 0; i< sections.length; i++){
                var loop = sections[i];
                loop.style.display = "none";
            }
            document.getElementById(id+"_contributor_container_id").style.display = "block";
        }
        else {
            for (i = 0; i< sections.length; i++){
                loop = sections[i];
                loop.style.display = "none";
            }
        }
    }
    function contributorToggle(type, event) {
        lectureSectionsToggle('contributors_sec_container_id');
        event.preventDefault();
        var parent_slug = document.getElementById("parent_slug_id").value;
        var select = document.getElementById("contributor_"+type+"_select_id");
        var contributor = select.options[select.selectedIndex].value;
        $.ajax({
            url: __contributors_toggle_url__,
            dataType: "html",
            type: "POST",
            data: {"spreadsheet_slug": parent_slug, "type": type, "contributor": contributor},
            success:function (data) {
                if (data !== "None"){
                   $("#contributors_container_id").html(data);
                }
                else {
                    // Do nothing..
                }
            },
            error: function (err) {
            console.log(" Error: " +err.status+ ", " + err.statusText + ", " +err)
            }
        })
    }
    window.addEventListener("scroll", loadMoreSpreadsheets);
    function loadMoreSpreadsheets(){
        if($(window).scrollTop() + $(window).height() >  $(document).height() - $(document).height() /8){
            if(window.navigator.onLine === true && spreadsheetsLoaderToggle === false){
                const type = document.getElementById("object_type_id").value;
                if(type !== "update"){
                   loadMoreObjects(type);
            }
                }

        }
    }
    var spreadsheetsLoaderToggle = false;
    function loadMoreObjects(type) {
        const parent_slug = document.getElementById("parent_slug_id").value;
        var btnLoader = document.getElementById('btn_loader_id');
        var imgLoader = document.getElementById('img_loader_id');
        var objectsContainer =  document.getElementById("main_objects_container_id");
        var loadedObjects = objectsContainer.getElementsByClassName("single-object-container");
        var loaderContainer = document.getElementById("objects_loader_container_id");
        var totalObjects = document.getElementById("total_objects_id").value;
        var searchValue = document.getElementById("search_value_id").value;
        var materialValue = document.getElementById("material_value_id").value;
        var startDate = document.getElementById("start_date_value_id").value;
        var endDate = document.getElementById("end_date_value_id").value;
        $.ajax({
            url: __objects_loader_url__,
            dataType: "html",
            type: "POST",
            data: {"parent_slug": parent_slug, "type": type,
                "loaded_objects": loadedObjects.length, "material":materialValue,
                "start_date":startDate, "end_date":endDate, "search":searchValue
            },
            beforeSend: function () {
                spreadsheetsLoaderToggle = true;
                loaderContainer.style.display = 'flex';
                btnLoader.style.display = 'none';
                imgLoader.style.display = 'block';
            },
            success:function (data) {
                btnLoader.style.display = 'inline';
                imgLoader.style.display = 'none';
                if (data !== "None"){
                    $("#main_objects_container_id").append(data);
                }
                else {
                    // Do nothing..
                    console.log("nothing returned..");
                }
            },
            complete:function(){
                if (parseInt(loadedObjects.length) >= parseInt(totalObjects)) {
                    loaderContainer.style.display = 'none';
                    spreadsheetsLoaderToggle = true;
                    }
                else {
                    loaderContainer.style.display = 'flex';
                    spreadsheetsLoaderToggle = false;
                    }
            },
            error: function (err) {
            console.log(" Error: " +err.status+ ", " + err.statusText + ", " +err)
            }
        })
}
    function validSearch(event){
        var input = document.getElementById('search_input_id');
        if(input.value.trim() === ''){
            input.value = '';
            event.preventDefault();
        }
    }
    function PrevLectFormEvent(event) {
        event.preventDefault();
        CreateLecture();
    }
    function CreateLecture() {
        var title = document.getElementById("id_title").value;
        var file = document.getElementById("id_file").files[0];
        var material_id = document.getElementById("id_material");
        var material = material_id.options[material_id.selectedIndex].value;
        var comment = document.getElementById("id_comment").value;
        var operation = document.getElementById("operation_value_id").value;
        var doctor_selector = document.getElementById("id_doctor");
        var doctor_id = doctor_selector.options[doctor_selector.selectedIndex].value;
        var lectureForm = document.querySelector("form[id='lecture_form_id']");
        var parent_slug = document.querySelector("input[id='parent_slug_id']").value;
        var lecture_id = document.querySelector("input[id='lecture_id']").value;
        var data = new FormData(lectureForm);
        data.append("title", title);
        data.append("file", file);
        data.append("material", material);
        data.append("comment", comment);
        data.append("operation", operation);
        data.append("parent_slug", parent_slug);
        data.append("lecture_id", lecture_id);
        data.append("doctor_id", doctor_id);
        data.append("csrfmiddlewaretoken", csrf_token);
        $.ajax({
            url: __lecture_create_url__,
            type: 'POST',
            enctype: "multipart/form-data",
            processData:false,
            cache:false,
            dataType: "html",
            contentType:false,
            beforeSend: function (xhr) {
                uploadStart();
                // var cancelBtn = document.getElementById('cancel_btn_id');
                // cancelBtn.addEventListener("click", canceled);
                // function canceled(){ xhr.abort(); uploadAbort();}
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
                    $('#main_objects_container_id').prepend(data);
                    uploadFinished();
                }
                else {
                    uploadError();
                }
            },
            complete:function(){
                $('#upload_btn_id').css('display', 'none');
                $('#upload_again_btn_id').css('display', 'block');
                lectureForm.reset();
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
         // $('#main_tags_container_id').hide();
         $('#main_form_container_id').hide();
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

    window.addEventListener("load", setViewsIncrement);

    function setViewsIncrement() {
        var type = document.getElementById("view_inc_type_id").value;
        var parent_slug = document.getElementById("parent_slug_id").value;
        if(!window.location.pathname.match("/spreadsheets")) {
            objectViewsIncrement(type, parent_slug);
        }

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
