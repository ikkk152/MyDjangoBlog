import {getCookie} from '../cookie.js';

$(function () {
    bindClickBtnLogin();
})

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
                    location.href = "/";
                } else {
                    $.each(res.errors, function (key, value) {
                        $('#id_' + key).next().text(value[0])
                    })
                }
            }
        })
    })
}