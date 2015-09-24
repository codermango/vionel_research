$(function() {
    $('#submitBtn').click(function() {
        var userInput = $("[name='inputMovies']").val();
        var rcNum = $("[name='recommendNum']").val();

        if (userInput == "") {
            alert("Please input movie imdb ids, seperated by comma.");
            return false;
        } else if (rcNum == "") {
            alert("Please input number of recommend movies");
            return false;
        } else {
            return true;
        }
    });

    // change the font color of recommend reason
    var featureLabel = $(".feature");
    for(var i=0; i<featureLabel.length; i++) {
        if(featureLabel[i].innerHTML == "genre") {
            featureLabel[i].style.color = "red";
        } else if (featureLabel[i].innerHTML == "actor") {
            featureLabel[i].style.color = "rebeccapurple";
        } else if (featureLabel[i].innerHTML == "director") {
            featureLabel[i].style.color = "greenyellow";
        } else if (featureLabel[i].innerHTML == "keyword") {
            featureLabel[i].style.color = "peru";
        }
    }


});