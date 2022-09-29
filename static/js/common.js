// 검색창 활성화시키는 함수
function active_search_input_box() {
    $('#search_icon').css("display", "none")
    $('#search_active_button').css("display", "none")
    $('#search_input_box').css("width", "90%")
    $('#search_input_box').focus()
}

// profile 마진값 계산하는 함수
function update_profile_margin() {
    let screen_width = $(window).width()
    let self_width = $('#main_body').width()
    let margin = screen_width - self_width
    let margin_right = (margin / 2).toString()

    let str = margin_right + "px"
    $('#profile_box').css("right", str)
}

// 스토리 슬라이드 함수
// vector : 슬라이드 방향 - 0:왼쪽, 1:오른쪽
function move_story_slide(vector) {
    let margin_text = $('#stories').css('margin-left')
    let width_text = $('#stories').css('width')
    let box_text = $('#card').css('width')

    let margin_num = Number(margin_text.slice(0, -2))
    let width_num = Number(width_text.slice(0, -2))
    let box_num = Number(box_text.slice(0, -2))

    let max_margin = 0  // 최대 마진 값
    let move_margin = 150   // 한번 이동할 때 움직일 마진 값

    if (width_num > box_num) {
        max_margin = width_num - box_num
    }

    if (vector == 1) {
        if (margin_num == 0) {
            $('#bg_slide_button_left').css("opacity", "1")
            $('#bg_slide_button_left').css("display", "block")
        }
        margin_num = margin_num - move_margin
        if (margin_num < -1 * max_margin) {
            margin_num = -1 * max_margin
            $('#bg_slide_button_right').css("opacity", "0")
            $('#bg_slide_button_right').css("display", "none")
        }
    } else {
        if (margin_num == -1 * max_margin) {
            $('#bg_slide_button_right').css("opacity", "1")
            $('#bg_slide_button_right').css("display", "block")
        }
        margin_num = margin_num + move_margin
        if (margin_num > 0) {
            margin_num = 0
            $('#bg_slide_button_left').css("opacity", "0")
            $('#bg_slide_button_left').css("display", "none")
        }
    }
    let update_margin = (margin_num).toString() + "px"

    $('#stories').css('margin-left', update_margin)
}

// 포스트 텍스트 더보기 버튼 함수
function view_post_text_more(name) {
    $(`.post_text_btn[name=${name}]`).css('display', 'none')
    $(`.post_text_more[name=${name}]`).css('display', 'block')
}

// 로딩시 profile 마진값 다시 계산
$(document).ready(function () {
    update_profile_margin()
})

$(function () {
    // 검색창에서 focus를 다른 곳으로 옮길 때
    $('#search_input_box').blur(()=>{
        $('#search_icon').css("display", "block")
        $('#search_active_button').css("display", "block")
        $('#search_input_box').css("width", "70%")
    })


    // 화면 사이즈 변경 시
    // profile 마진값 다시 계산
    $(window).resize(function () {
        update_profile_margin()
    });

    // 현재 선택된 댓글창에 상태에 따라 게시 버튼 효과 변경
    $('.post_comment_input').on('focus blur keyup', () => {
        let name = $(':focus').attr('name');

        if ($(`.post_comment_input[name='${name}']`).val() === "") {
            $(`.post_comment_input_btn[name='${name}']`).css('opacity', '0.5')
        } else {
            $(`.post_comment_input_btn[name='${name}']`).css('opacity', '1')
        }
    })
});

