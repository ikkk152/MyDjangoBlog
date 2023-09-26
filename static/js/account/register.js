$(function () {
    bindClickBtnRegister();
    bindClickBtnSendEmail();
    getCookie();
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

function bindClickBtnRegister() {
    $('#btnRegister').click(function () {
        event.preventDefault();
        $('.error').empty()
        $.ajax({
            url: "/user/register/",
            data: $('#RegisterForm').serializeArray(),
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            type: "POST",
            dataType: "JSON",
            success: function (res) {
                if (res.success) {
                    location.href = "/user/login/"
                } else {
                    $.each(res.errors, function (key, value) {
                        $('#id_' + key).next().text(value[0])
                    })
                }
            }
        })
    })
}

function bindClickBtnSendEmail() {
    $('#btnSendEmail').click(function () {
        $('#id_email').next().empty()
        event.preventDefault();
        const email = $("#id_email").val();
        $.ajax({
            url: '/user/register/code/',
            data: {
                'email': email,
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            dataType: "JSON",
            type: "POST",
            success: function (res) {
                if (res.success) {
                    // 开始禁用按钮和倒计时
                    let countdown = 60;
                    $('#btnSendEmail').prop('disabled', true);  // 禁用按钮

                    let timer = setInterval(function () {
                        if (countdown <= 0) {
                            clearInterval(timer);  // 清除计时器
                            $('#btnSendEmail').prop('disabled', false);  // 启用按钮
                            $('#btnSendEmail').text('发送验证码');  // 恢复按钮的原始文本
                        } else {
                            $('#btnSendEmail').text('重发验证码 (' + countdown + 's)');
                            countdown--;
                        }
                    }, 1000);
                } else {
                    $('#id_email').next().text(res.errors)

                }
            }
        })
    })
}