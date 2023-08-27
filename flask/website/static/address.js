document.addEventListener("DOMContentLoaded", function () {
    // sido option 추가
    hangjungdong.sido.forEach(function (code) {
      document.querySelector("#sido").appendChild(fn_option(code.sido, code.codeNm));
    });
  
    // sido 변경시 시군구 option 추가
    document.querySelector("#sido").addEventListener("change", function () {
      var sigugun = document.querySelector("#sigugun");
      sigugun.style.display = "block";
      sigugun.innerHTML = "";
      sigugun.appendChild(fn_option("", "선택"));
  
      hangjungdong.sigugun.forEach(function (code) {
        if (document.querySelector("#sido").value == code.sido) {
          sigugun.appendChild(fn_option(code.sigugun, code.codeNm));
        }
      });
  
      if (document.querySelector("#sido").value == "36") {
        sigugun.style.display = "none";
        sigugun.querySelector("option:nth-child(2)").selected = true;
        sigugun.dispatchEvent(new Event("change"));
      }
    });
  
    // 시군구 변경시 행정동 옵션추가
    document.querySelector("#sigugun").addEventListener("change", function () {
      var dong = document.querySelector("#dong");
      dong.innerHTML = "";
  
      hangjungdong.dong.forEach(function (code) {
        if (
          document.querySelector("#sido").value == code.sido &&
          document.querySelector("#sigugun").value == code.sigugun
        ) {
          dong.appendChild(fn_option(code.dong, code.codeNm));
        }
      });
  
      dong.insertBefore(fn_option("", "선택"), dong.firstChild);
      dong.querySelector("option[value='']").selected = true;
    });
  
    document.querySelector("#dong").addEventListener("change", function () {
      var sido = document.querySelector("#sido").value;
      var sigugun = document.querySelector("#sigugun").value;
      var dong = document.querySelector("#dong").value;
      var dongCode = sido + sigugun + dong + "00";
    });
  });
  
  function fn_option(code, name) {
    var option = document.createElement("option");
    option.value = code;
    option.text = name;
    return option;
  }