//jshint esversion:6

function createPass(){
    let characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
                't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '~', '!', 
                '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '?', 'A', 'B', 'C', 'D', 'E', 
                'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
                'Y', 'Z'];

    let lowerc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    let upperc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    let numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    let symbols = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '?'];

    const passwordLength = 15;
    let newPassword = "";

    let charTypes = [lowerc, upperc, numbers, symbols];

    function getRandonInt(min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random()*(max - min) + min);
    };

    for(let t of charTypes) {
        let randomIndex = getRandonInt(0, t.length);
        let randomChar = t[randomIndex];
        newPassword += randomChar;
    };

    let count = newPassword.length;

    while(count < passwordLength) {
        randomIndex = getRandonInt(0, characters.length);
        randomChar = characters[randomIndex]
        newPassword += randomChar
        count += 1
    };

    newPassword = newPassword.split('').sort(function(){return 0.5-Math.random()}).join('');
    return newPassword
};


function fillPassInput() {
    document.querySelector('#passInput').value = createPass();
};


function deleteRecord(button) {
    var buttonId = button.id;
    confirm("Are you sure you want to delete this record?")
    $.ajax({
        url: '/delete-record',
        method: 'POST',
        data: { record_id: buttonId },
        success: function(response) {
            var redirectUrl = response.redirect_url;
            window.location.href = redirectUrl;
        },
        error: function(error) {
            console.log(error);
        },
      });

};

function togglePassword(button) {
    let recordId = button.id.slice(4);
    let passId = "pass" + recordId;
    let selectedPass = document.getElementById(passId);
    let inputType = selectedPass.getAttribute('type');
    if (inputType === 'password') {
        selectedPass.setAttribute('type', 'text')
    } else {
        selectedPass.setAttribute('type', 'password')
    };
};

function copyPassword(button) {
    let recordId = button.id.slice(4);
    let passId = "pass" + recordId;
    // Get the text field
    var copyText = document.getElementById(passId);
    console.log(copyText);
  
    // Select the text field
    copyText.select();
  
     // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);
};




