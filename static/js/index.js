
function searchModeChange(id) {
    let tag1 = document.getElementById("search_mode1");
    let tag2 = document.getElementById("search_mode2");
    let tag3 = document.getElementById("search_mode3");
    let default_form_block = document.getElementById("default_form_block");
    let condition_form_block = document.getElementById("condition_form_block");
    let batch_form_block = document.getElementById("batch_form_block");
    console.log(id);
    if (id === "search_mode1") {
        //修改对应的样式
        tag1.style.color = "#759afa";
        tag1.style.fontWeight = "bolder";
        tag1.style.fontSize = "24px";
        tag2.style.color = "#B5B5B5";
        tag2.style.fontWeight = "bold";
        tag2.style.fontSize = "18px";
        tag3.style.color = "#B5B5B5";
        tag3.style.fontWeight = "bold";
        tag3.style.fontSize = "18px";
        //显示 隐藏
        default_form_block.style.display = "block";
        condition_form_block.style.display = "none";
        batch_form_block.style.display = "none";
    } else if (id === "search_mode2") {
        //修改对应的样式
        tag2.style.color = "#759afa";
        tag2.style.fontWeight = "bolder";
        tag2.style.fontSize = "24px";
        tag1.style.color = "#B5B5B5";
        tag1.style.fontWeight = "bold";
        tag1.style.fontSize = "18px";
        tag3.style.color = "#B5B5B5";
        tag3.style.fontWeight = "bold";
        tag3.style.fontSize = "18px";
        //显示 隐藏
        default_form_block.style.display = "none";
        condition_form_block.style.display = "block";
        batch_form_block.style.display = "none";
    } else if (id === "search_mode3"){
        //修改对应的样式
        tag3.style.color = "#759afa";
        tag3.style.fontWeight = "bolder";
        tag3.style.fontSize = "24px";
        tag1.style.color = "#B5B5B5";
        tag1.style.fontWeight = "bold";
        tag1.style.fontSize = "18px";
        tag2.style.color = "#B5B5B5";
        tag2.style.fontWeight = "bold";
        tag2.style.fontSize = "18px";
        //显示 隐藏
        default_form_block.style.display = "none";
        condition_form_block.style.display = "none";
        batch_form_block.style.display = "block";
    } else
        alert("未知的类型");
}

