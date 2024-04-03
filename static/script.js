function boldText(text_to_add) {
         let emailBody = document.getElementById("emailBody");
         let start_position = emailBody.selectionStart;
         let end_position = emailBody.selectionEnd;

         document.getElementById("emailBody").focus();

         emailBody.value = `${emailBody.value.substring(
                0,
                start_position
         )}${text_to_add}${emailBody.value.substring(
             end_position,
             emailBody.value.length
         )}`;

};
function italicText(text_to_add){
         let emailBody = document.getElementById("emailBody");
         let start_position = emailBody.selectionStart;
         let end_position = emailBody.selectionEnd;

         document.getElementById("emailBody").focus();
         emailBody.value = `${emailBody.value.substring(
                0,
                start_position
         )}${text_to_add}${emailBody.value.substring(
                end_position,
                emailBody.value.length
         )}`;
};
function underlineText(text_to_add){
          let emailBody = document.getElementById("emailBody");
          let start_position = emailBody.selectionStart;
          let end_position = emailBody.selectionEnd;

          document.getElementById("emailBody").focus();
          emailBody.value = `${emailBody.value.substring(
                0,
                start_position
          )}${text_to_add}${emailBody.value.substring(
                end_position,
                emailBody.value.length
          )}`;
};
function nextLine(text_to_add){
          let emailBody = document.getElementById("emailBody");
          let start_position = emailBody.selectionStart;
          let end_position = emailBody.selectionEnd;

          document.getElementById("emailBody").focus();
          emailBody.value = `${emailBody.value.substring(
                0,
                start_position
          )}${text_to_add}${emailBody.value.substring(
                end_position,
                emailBody.value.length
          )}`;
};
function validation(){
    if(document.emaildata.file.value.length < 35){
        document.getElementById("result").innerHTML="*CSV file - Please enter proper file directory.*";
        openErrorPopup();
        return false;
    }
//    else if(document.emaildata.subject.value.length < 5){
//        document.getElementById("result").innerHTML="*Subject - Please enter proper subject.*";
//        openErrorPopup();
//        return false;
//    }
    else{

        openPopup();

    }
}
function excelValidation(){
    if(document.exceldata.excelfile.value.length < 35){
        document.getElementById("result").innerHTML="*Excel file - Please enter proper file directory.*";
        openErrorPopup();
        return false;
    }
    else if(document.exceldata.vendor.value.length < 7){
        document.getElementById("result").innerHTML="*Vendor Code - Please enter proper vendor code.*";
        openErrorPopup();
        return false;
    }
//    else if(document.exceldata.orderunit.value != "/^[A-Za-z]+$/"){
//        document.getElementById("result").innerHTML="*Order Unit - Please enter proper unit.*";
//        openErrorPopup();
//        return false;
//    }
    else{
        openPopup();

    }
}
let popup = document.getElementById("popup");
function openPopup(){
//      if (document.emaildata.file.value.length > 35 && document.emaildata.subject.value.length > 5)
          document.getElementById("popup").classList.add("open-slide");
}
function closePopup(){
      document.getElementById("popup").classList.remove("open-slide");
}
let savepopup = document.getElementById("savepopup");
function openSavePopup(){
    if (document.emaildata.file.value.length > 35)
          document.getElementById("savepopup").classList.add("open-slide");
}
function closeSavePopup(){
    document.getElementById("savepopup").classList.remove("open-slide");
}
let errorpopup = document.getElementById("errorpopup");
function openErrorPopup(){
        document.getElementById("errorpopup").classList.add("open-slide");
}
function closeErrorPopup(){
    document.getElementById("errorpopup").classList.remove("open-slide");
}
function passwordValidation(){
    var input1 = document.getElementById("signUpPassword").value;
    var input2 = document.getElementById("retypePassword").value;
    check1 = document.getElementById("check1");
    check2 = document.getElementById("check2");
    check3 = document.getElementById("check3");
    check4 = document.getElementById("check4");

    input1 = input1.trim();
    input2 = input2.trim();

    if(input1.length >= 8){
        check1.style.color = "#00A97A";
    }
    else{
        check1.style.color = "red";
    }
    if(input1.match(/[^A-Za-z0-9-'']/i)){
        check2.style.color = "#00A97A";
    }
    else{
        check2.style.color = "red";
    }
    if(input1.match(/[0-9]/i)){
        check3.style.color = "#00A97A";
    }
    else{
        check3.style.color = "red";
    }
    if(input1 == input2){
        check4.style.color = "#00A97A";
    }
    else{
        check4.style.color = "red";
    }
    if ((check1.style.color && check2.style.color && check3.style.color && check4.style.color) != "red"){
         document.getElementById("btnSignUp").disabled = false;
    } else {
         document.getElementById("btnSignUp").disabled = true;
    }
}

const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", ()=> {
    container.classList.add("sign-up-mode");
});
sign_in_btn.addEventListener("click", ()=> {
    container.classList.remove("sign-up-mode");
});