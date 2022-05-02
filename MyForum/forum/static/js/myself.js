window.onload=function(){
    var btn_name=document.getElementById("btn_name");
    var btn_sig=document.getElementById("btn_sig");
    var btn_img=document.getElementById("btn_img");
    var input=document.getElementsByTagName("input")[0];
    var subbtn=document.getElementsByTagName("input")[1];
    btn_name.onclick=function(){
        btn_img.style.display="none";
        btn_sig.style.display="none";
        btn_name.style.display="none";
        input.placeholder="修改用户名";
        input.style.display="block";
        subbtn.style.display="block";  
    }
    btn_sig.onclick=function(){
        btn_img.style.display="none";
        btn_sig.style.display="none";
        btn_name.style.display="none";
        input.placeholder="修改签名";
        input.style.display="block";
        subbtn.style.display="block";
        input.name="signature";
    }
    btn_img.onclick=function(){
        btn_img.style.display="none";
        btn_sig.style.display="none";
        btn_name.style.display="none";
        input.placeholder="修改头像";
        input.style.display="block";
        subbtn.style.display="block";
        input.name="img";      
    }
}