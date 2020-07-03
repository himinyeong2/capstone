function post_manipulate_plan(type) {
    var dateId = $(location).attr('search').slice($(location).attr('search').indexOf('=') + 1);
    let data = {
        'type': type,
        'plancontent': document.getElementById("plancontent").value,
        'date': dateId
    };
    fetch('/plan_manipulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.text())
        .then((res) => {
            if (res == "ERROR")
                alert("분석에 실패하였습니다.");
            else if (type == "DELETE") {
                alert("삭제가 완료되었습니다.");
                window.location.href = "/calendar";
            } else {
                alert("수정이 완료되었습니다.");
                window.location.href = "/result_plan?date=" + dateId;
            }
        }).catch((err) => {
            console.error("에러: ", err);
        });
}

function post_manipulate_diary(type) {
    var dateId = $(location).attr('search').slice($(location).attr('search').indexOf('=') + 1);
    let data = {
        'type': type,
        'diarycontent': document.getElementById("diarycontent").value,
        'date': dateId
    };
    fetch('/diary_manipulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.text())
        .then((res) => {
            if (res == "ERROR")
                alert("감정분석에 실패하였습니다.");
            else if (type == "DELETE") {
                alert("삭제가 완료되었습니다.");
                window.location.href = "/calendar";
            } else {
                alert("수정이 완료되었습니다.");
                window.location.href = "/result_diary?date=" + dateId;
            }
        }).catch((err) => {
            console.error("에러: ", err);
        });
}

function post_find_id() {
    let data = {
        'userName': document.getElementById("find_userName").value,
        'userEmail': document.getElementById("find_userEmail").value
    };
    fetch('/check_find_id', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => res.text())
        .then((res) => {
            alert("당신의 ID는 [" + res + "] 입니다");
        }).catch((err) => {
            console.error("에러: ", err);
        });
}

function post_find_pw() {
    let data = {
        'userId': document.getElementById("find_userId").value,
        'userEmail': document.getElementById("find_userEmail").value
    };
    fetch('/check_find_pw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => res.text())
        .then((res) => {
            alert("당신의 PASSWORD는 [" + res + "] 입니다");
        }).catch((err) => {
            console.error("에러: ", err);
        });
}


function chk_same_mon(object1, object2, object3) {
    var arr = object1.split('-');
    arr[0] *= 1;
    arr[1] *= 1;
    object2 *= 1;
    object3 *= 1;

    if (arr[0] == object2 && arr[1] == object3)
        return true;
    else
        return false;
}

function add_emoticon(cell, jsonData) {
    var cell_str, emo_str, emo, day, arr;
    var arr_str = jsonData.substring(1, jsonData.length - 1);
    arr = arr_str.split(',');

    for (var i = 0; i < (arr.length) / 2; i++) {
        cell_str = arr[i * 2].split(':')[1];
        if (cell.id == cell_str.substring(1, cell_str.length - 1)) {
            emo_str = arr[i * 2 + 1].split(':')[1];
            emo = emo_str.substring(1, emo_str.length - 2);
            day = cell_str.substring(1, cell_str.length - 1).split('-')[2];
            cell.innerHTML = day + "<img src='." + emo + "'alt='' />";
        }
    }
}

function add_emo(jsonData, year, month) {
    var cell_str, emo_str, cell, emo, day, arr;
    var arr_str = jsonData.substring(1, jsonData.length - 1);
    arr = arr_str.split(',');
    //arr = {'date':'','img':''}

    for (var i = 0; i < (arr.length) / 2; ++i) {
        cell_str = arr[i * 2].split(':')[1];
        cell = cell_str.substring(1, cell_str.length - 1);
        //cell = 2020-05-27
        emo_str = arr[i * 2 + 1].split(':')[1];
        emo = emo_str.substring(1, emo_str.length - 2);
        //emo = /static/...
        if (chk_same_mon(cell, year, month)) {
            day = cell.split('-')[2];
            document.getElementById(cell).innerHTML = day + "<img src='." + emo + "'alt='' />";
        }
    }
}

var today = new Date();
var date = new Date();

function prevCalendar(jsonData) {
    today = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    buildCalendar(jsonData);
    get_modal();
}

function nextCalendar(jsonData) {
    today = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
    buildCalendar(jsonData);
    get_modal();
}

function get_modal() {
    // 모달 버튼에 이벤트를 건다.
    $('.date').on('click', function () {
        $('#modalBox').modal('show');
        post_dateId(this.id);
    });
    // 모달 안의 취소 버튼에 이벤트를 건다.
    $('#closeModalBtn').on('click', function () {
        $('#modalBox').modal('hide');
    });

    $('#diary_res').on('click', function () {
        $('#modalBox').modal('show');
        post_dateId(this.id);
    });

    $('#closeModalBtn').on('click', function () {
        $('#modalBox').modal('hide');
    });
}

function buildCalendar(jsonData) {
    var doMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    var lastDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    var tbCalendar = document.getElementById("calendar");
    var tbCalendarYM = document.getElementById("tbCalendarYM");

    if ((today.getMonth() + 1) == 1) {
        tbCalendarYM.innerHTML = "January " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 2) {
        tbCalendarYM.innerHTML = "February " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 3) {
        tbCalendarYM.innerHTML = "March " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 4) {
        tbCalendarYM.innerHTML = "April " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 5) {
        tbCalendarYM.innerHTML = "May " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 6) {
        tbCalendarYM.innerHTML = "June " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 7) {
        tbCalendarYM.innerHTML = "July " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 8) {
        tbCalendarYM.innerHTML = "August " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 9) {
        tbCalendarYM.innerHTML = "September " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 10) {
        tbCalendarYM.innerHTML = "February " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 11) {
        tbCalendarYM.innerHTML = "November " + today.getFullYear();
    } else if ((today.getMonth() + 1) == 12) {
        tbCalendarYM.innerHTML = "December " + today.getFullYear();
    }

    while (tbCalendar.rows.length > 2) {
        tbCalendar.deleteRow(tbCalendar.rows.length - 1);
    }
    var row = null;
    row = tbCalendar.insertRow();
    var cnt = 0;
    for (i = 0; i < doMonth.getDay(); i++) {
        cell = row.insertCell();
        cnt = cnt + 1;
    }

    /*달력 출력*/
    for (i = 1; i <= lastDate.getDate(); i++) {
        cell = row.insertCell();
        cell.innerHTML = i;
        cell.classList.add("date");
        if ((today.getMonth() + 1) > 0 && (today.getMonth() + 1) < 10 && i > 0 && i < 10) {
            cell.id = today.getFullYear() + "-0" + (today.getMonth() + 1) + "-0" + i;
        } else if ((today.getMonth() + 1) > 9 && i > 0 && i < 10) {
            cell.id = today.getFullYear() + "-" + (today.getMonth() + 1) + "-0" + i;
        } else if ((today.getMonth() + 1) > 0 && (today.getMonth() + 1) < 10 && i > 9) {
            cell.id = today.getFullYear() + "-0" + (today.getMonth() + 1) + "-" + i;
        } else {
            cell.id = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + i;
        }
        cnt = cnt + 1;
        if (cnt % 7 == 1) {
            cell.style.color = "#F79DC2"
            //1번째의 cell에만 색칠
        }
        if (cnt % 7 == 0) {
            cell.style.color = "skyblue"
            row = calendar.insertRow();
        }
        if (jsonData.length != 2)
            add_emoticon(cell, jsonData);
    }
    // add_emo(jsonData, today.getFullYear().toString(), today.getMonth().toString());
}

// #header-iframe 배경 바뀌는 함수 수정!
function chg_if_bg() {
    parent.document.getElementById('header-iframe').style.background = "url('static/img/header_bg_half.png'), url('static/img/header_bg_navy.png')";

    parent.document.getElementById('header-iframe').style.backgroundPosition = "bottom right, bottom";
    parent.document.getElementById('header-iframe').style.backgroundRepeat = "no-repeat, no-repeat";
    if (parent.screen.width < 767.98) {
        parent.document.getElementById('header-iframe').style.backgroundSize = "auto 16.25em, contain";
    } else if (parent.screen.width >= 768 && parent.screen.width <= 1024) {
        parent.document.getElementById('header-iframe').style.backgroundSize = "auto 27.5em, contain";
    } else {
        parent.document.getElementById('header-iframe').style.backgroundSize = "auto 33em, contain";
    }
};


function chg_if_bg_def() {
    parent.document.getElementById('header-iframe').style.background = "url('static/img/header_bg.png'), url('static/img/header_bg_navy.png')";

    parent.document.getElementById('header-iframe').style.backgroundPosition = "bottom right, bottom";
    parent.document.getElementById('header-iframe').style.backgroundRepeat = "no-repeat, no-repeat";
    if (parent.screen.width < 767.98) {
        parent.document.getElementById('header-iframe').style.backgroundSize = "17.5em auto, contain";
    } else if (parent.screen.width >= 768 && parent.screen.width <= 1024) {
        parent.document.getElementById('header-iframe').style.backgroundSize = "33.5em auto, contain";
    } else {
        parent.document.getElementById('header-iframe').style.backgroundSize = "auto 32.5em, contain";
    }
};






function post_dup_chk(objectId) {

    let data = {
        'objectId': objectId,
        'object': document.getElementById(objectId).value
    };
    fetch('/check_dup_chk', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => res.text())
        .then((res) => {
            alert(res);
        }).catch((err) => {
            console.error("에러: ", err);
        });
}

function post_login() {
    let data = {
        'loginId': document.getElementById("loginId").value,
        'loginPw': document.getElementById("loginPw").value
    };
    fetch('/sign_in_check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.text())
        .then((res) => {
            if(res=="FAILED")
                alert("[로그인실패]아이디 혹은 패스워드를 확인하십시오.");
        }).catch((err) => {
            console.error("에러: ", err);
        }).finally(() => {
            window.parent.location.href = "/current";
        });

}

function post_signup() {
    let data = {
        'userName': document.getElementById("userName").value,
        'userEmail': document.getElementById("userEmail").value,
        'userId': document.getElementById("userId").value,
        'userPw': document.getElementById("userPw").value,
        'userPwCheck': document.getElementById("userPwCheck").value
    };
    fetch('/sign_up_check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => res.json())
        .then((res) => {
            alert("회원가입에 성공하였습니다.");
            console.log("성공: ", res);
        }).catch((err) => {
            console.error("에러: ", err);
        }).finally(() => {
            window.parent.location.href = "/";
        });
}



function post_dateId(dateId) {
    var opt1 = document.getElementById('diary_select');
    var opt2 = document.getElementById('plan_select');

    opt1.addEventListener('click', function () {
        window.location.href = "/diary?date=" + dateId;
    });

    opt2.addEventListener('click', function () {

        window.location.href = "/plan?date=" + dateId;
    });
}

function post_diary() {
    var dateId = $(location).attr('search').slice($(location).attr('search').indexOf('=') + 1);
    let data = {
        'diarycontent': document.getElementById("diarycontent").value,
        'date': dateId
    };
    fetch('/diary_check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.text())
        .then((res) => {
            if (res == "ERROR")
                alert("감정분석이 불가능합니다.");
            else{
                alert("다이어리 입력 완료");
                window.location.href = "/result_diary?date=" + dateId;
            }
        }).catch((err) => {
            console.error("에러: ", err);
        });
}

function post_plan() {
    var dateId = $(location).attr('search').slice($(location).attr('search').indexOf('=') + 1);
    let data = {
        'date': dateId,
        'plancontent': document.getElementById("plancontent").value
    };
    // wait_res('plan');
    fetch('/plan_check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => res.text())
        .then((res) => {
            if (res == "ERROR")
                alert("분석이 불가능합니다.");
            else{
                alert("계획 입력 완료");
                window.location.href = "/result_plan?date=" + dateId;
            }
        }).catch((err) => {
            console.error("에러: ", err);
        });
}

$(document).ready(function () {
    var btn = document.getElementsByClassName('chk_btn');
    for (var i = 0; btn.length; ++i) {
        btn[i].addEventListener('click', function () {
            var arr = (this.id).split('_');
            post_dup_chk(arr[0]);
        });
    }
});

$(document).ready(function () {
    var btn = document.getElementById('login_btn');

    btn.addEventListener('click', function () {
        post_login();
    });
});


$(document).ready(function () {
    var btn = document.getElementById('signup_btn');

    btn.addEventListener('click', function () {
        post_signup();
    });
});
$(document).ready(function () {
    var val = location.href.substr(
        location.href.lastIndexOf('=') + 1
    );
    var btn = document.getElementById('diary_sv_btn');

    btn.addEventListener('click', function () {
        post_diary();
    });
});
$(document).ready(function () {
    var val = location.href.substr(
        location.href.lastIndexOf('=') + 1
    );
    var btn = document.getElementById('plan_sv_btn');

    btn.addEventListener('click', function () {
        post_plan();
    });

});
$(document).ready(function () {
    var val = location.href.substr(
        location.href.lastIndexOf('=') + 1
    );
    var btn = document.getElementById('find_id_btn');

    btn.addEventListener('click', function () {
        post_find_id();
    });

});
$(document).ready(function () {
    var val = location.href.substr(
        location.href.lastIndexOf('=') + 1
    );
    var btn = document.getElementById('find_pw_btn');

    btn.addEventListener('click', function () {
        post_find_pw();
    });

});
$(document).ready(function () {
    var val = location.href.substr(
        location.href.lastIndexOf('=') + 1
    );
    var btn = document.getElementById('diary_edit_btn');

    btn.addEventListener('click', function () {
        post_manipulate_diary("EDIT");
    });

});
$(document).ready(function () {
    var val = location.href.substr(
        location.href.lastIndexOf('=') + 1
    );
    var btn = document.getElementById('diary_del_btn');

    btn.addEventListener('click', function () {
        post_manipulate_diary("DELETE");
    });

});
$(document).ready(function () {
    var val = location.href.substr(
        location.href.lastIndexOf('=') + 1
    );
    var btn = document.getElementById('plan_edit_btn');

    btn.addEventListener('click', function () {
        post_manipulate_plan("EDIT");
    });

});
$(document).ready(function () {
    var val = location.href.substr(
        location.href.lastIndexOf('=') + 1
    );
    var btn = document.getElementById('plan_del_btn');

    btn.addEventListener('click', function () {
        post_manipulate_plan("DELETE");
    });

});
