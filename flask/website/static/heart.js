// 좋아요 기능 관련 jquery

// open 페이지 open 정보 좋아요
function toggle_like_open_open(info_id, type) {
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

// hot 페이지 hot 정보 좋아요
function toggle_like_hot_hot(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/hot/update_like",
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
            url: "/hot/update_like",
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

// key1 페이지 좋아요
function toggle_like_key1(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/keyword1/update_like",
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
            url: "/keyword1/update_like",
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

// key2 페이지 좋아요
function toggle_like_key2(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/keyword2/update_like",
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
            url: "/keyword2/update_like",
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

// key3 페이지 좋아요
function toggle_like_key3(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/keyword3/update_like",
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
            url: "/keyword3/update_like",
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

// key4 페이지 좋아요
function toggle_like_key4(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/keyword4/update_like",
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
            url: "/keyword4/update_like",
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

// key5 페이지 좋아요
function toggle_like_key5(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/keyword5/update_like",
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
            url: "/keyword5/update_like",
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

// key6 페이지 좋아요
function toggle_like_key6(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/keyword6/update_like",
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
            url: "/keyword6/update_like",
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

// home 페이지 open 정보 좋아요 
function toggle_like_main_open(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/update_like",
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
            url: "/update_like",
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

// home 페이지 hot 정보 좋아요 
function toggle_like_main_hot(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/update_like_hot",
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
            url: "/update_like_hot",
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

// home 페이지 키워드 정보 좋아요 
function toggle_like_main_keyword(info_id, type) {
    console.log(info_id, type)
    let $a_like = $(`#${info_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    console.log($i_like)
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/update_like_key",
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
            url: "/update_like_key",
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