$(document).ready(function () {


    $("#likeButton").click(function () {
        $.ajax({
            type: "GET",
            url: location.href + '/add_like',
            success: function (data) {
                var json = jQuery.parseJSON(data);
                $("#h5").html(json.likes);
                if (json.is_like_set) {
                    $("#likeButton").css('color', 'red');
                } else {
                    $("#likeButton").css('color', '#efefef');
                }
            }
        });
        return false;
    });


    $("#comment_form").submit(function () {
        let str = document.getElementById("comment_text").value;
        $.ajax({
            type: "GET",
            url: location.href + '/add_comment',
            data: {
                "text": str,
            },
            success: function (data) {
                let json = jQuery.parseJSON(data);
                $('#comments').append(`<div class="media">
                <div id="comment" class="media-body d-flex mt-4">
                            <img src="/static/img/avatars/` + json.userAvatar + `"
                                 class="mr-3 rounded-circle user-comment-icon">
                        <div class="comment-body">
                        <h5>` + json.nickname + `</h5>
                    ` + str + `
                    </div>
                </div>
            </div>`);
                document.getElementById('comment_text').value = '';
                // $('#collapseExample').collapse()
                // document.getElementById('collapseExample').setAttribute('class', 'collapse');
            },
            error: function () {
                alert('Пожалуйста, авторизуйтесь!');
            }
        });
        return false;
    });
});