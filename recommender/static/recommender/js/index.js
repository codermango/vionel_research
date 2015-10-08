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
        if(featureLabel[i].innerHTML == "imdbGenres") {
            featureLabel[i].style.color = "red";
        } else if (featureLabel[i].innerHTML == "imdbMainactors") {
            featureLabel[i].style.color = "rebeccapurple";
        } else if (featureLabel[i].innerHTML == "imdbDirectors") {
            featureLabel[i].style.color = "greenyellow";
        } else if (featureLabel[i].innerHTML == "imdbKeywords") {
            featureLabel[i].style.color = "peru";
        } else if (featureLabel[i].innerHTML == "wikiKeywords") {
            featureLabel[i].style.color = "pink";
        } else if (featureLabel[i].innerHTML == "vionelThemes") {
            featureLabel[i].style.color = "yellow";
        } else if (featureLabel[i].innerHTML == "vionelScene") {
            featureLabel[i].style.color = "blue";
        } else if (featureLabel[i].innerHTML == "locationCountry") {
            featureLabel[i].style.color = "CornflowerBlue";
        } else if (featureLabel[i].innerHTML == "locationCity") {
            featureLabel[i].style.color = "Teal";
        }
    }


});