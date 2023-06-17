function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const host = 'http://127.0.0.1:8000/'
const vote = 'vote/'
const set_correct = 'set_correct/'
const csrf_token = getCookie('csrftoken')

$(".like_button_plus, .like_button_minus").on('click', function (ev) {
    info_bar = $(this).parent().children('#_info')
    count = $(this).parent().children('.count')
    data_type = info_bar.data('type')
    data_id = info_bar.data('id')
    if ($(this).hasClass('plus')) {
        rate_type = 'p'
    } else {
        rate_type = 'm'
    }
    const request = new Request(
        host+vote,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            body:  'type='+data_type+'&id='+data_id+"&rate="+rate_type,
        }
    );

    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => count.text(response_json.new_rating)
        )
    );
});

$(".correct_checkbox").on('change', function (ev) {
    data_id = $(this).data('id')

    const request = new Request(
        host+set_correct,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            body: '&id='+data_id,
        }
    );

    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => {
                $(this).prop('checked', response_json.is_correct);
                
            }
        )
    );
});
