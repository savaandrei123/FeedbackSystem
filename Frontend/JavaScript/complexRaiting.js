
function send_complex_raiting() {
    var question1 = document.getElementsByName('rating-Q1');
    var question2 = document.getElementsByName('rating-Q2');
    var question3 = document.getElementsByName('rating-Q3');

    for(i = 0; i < question1.length; i++) {
        if(question1[i].checked)
        alert(question1[i].value)
    }
    for(i = 0; i < question2.length; i++) {
        if(question2[i].checked)
        alert(question2[i].value)
    }
    for(i = 0; i < question3.length; i++) {
        if(question3[i].checked)
        alert(question3[i].value)
    }

}
