// 좋아요 기능 관련 jquery

function toggle_like(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/open/update_like",
            data: {
                show_id_give: info_id,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass("fa-heart-o").removeClass("fa-heart")
                $a_like.find("span.like-num").text(response["count"])
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/open/update_like",
            data: {
                show_id_give: info_id,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass("fa-heart").removeClass("fa-heart-o")
                $a_like.find("span.like-num").text(response["count"])
            }
        })
    }
}

function toggle_like2(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/open/update_like",
            data: {
                show_id_give: info_id,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass("fa-heart-o").removeClass("fa-heart")
                $a_like.find("span.like-num").text(response["count"])
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/open/update_like",
            data: {
                show_id_give: info_id,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass("fa-heart").removeClass("fa-heart-o")
                $a_like.find("span.like-num").text(response["count"])
            }
        })
    }
}