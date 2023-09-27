$(function () {
    bindClickBtnLogin();
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function bindClickBtnLogin() {
    $('#btnLogin').click(function () {
        event.preventDefault();
        $('.error').empty()
        $.ajax({
            url: "/user/login/",
            data: $('#LoginForm').serializeArray(),
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            type: "POST",
            dataType: "JSON",
            success: function (res) {
                if (res.success) {
                    location.href = "/"
                } else {
                    console.log(res.errors)
                    $.each(res.errors, function (key, value) {
                        $('#id_' + key).next().text(value[0])
                    })
                }
            }
        })
    })
}