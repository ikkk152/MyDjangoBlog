$(function () {
    bindClickBtnRegister();
})

function bindClickBtnRegister() {
    $('#btnRegister').click(function () {
        event.preventDefault();
        $('.error').empty()
        $.ajax({
            url: "{% url 'register' %}",
            data: $('#RegisterForm').serializeArray(),
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            type: "POST",
            dataType: "JSON",
            success: function (res) {
                if (res.success) {
                    location.href = "{% url 'index' %}"
                } else {
                    $.each(res.errors, function (key, value) {
                        $('#id_' + key).next().text(value[0])
                    })
                }
            }
        })
    })
}