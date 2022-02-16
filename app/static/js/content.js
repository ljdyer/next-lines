var NON_CHANGING_KEYS = [9, 16, 17, 18, 20, 33, 34, 35, 36, 37, 38, 39, 40, 44, 45];

function getAnswer(){
    thinking();
    $('#question-input').prop('disabled', true);
    $('#ask').prop('disabled', true);
    let inputLine = $("#question-input").val()
    fetch('/get_answer', {method: "POST", body: inputLine}).then(
        response => response.text().then(
            json_response => {
                response = JSON.parse(json_response);
                if (response['success']){
                    $('#next-line').text(response['next_line']);
                    $('#song-name').text(response['song_name']);
                    $('#artist-name').text(response['artist_name']);
                    $('#answer-thinking').hide();
                    $('#answer-pass').hide();
                    $('#answer-answer').show();
                    feedbackPlease();
                } else{
                    $('#answer-thinking').hide();
                    $('#answer-answer').hide();
                    $('#answer-pass').show();
                }
                $('#question-input').prop('disabled', false);
                $("#question-input").focus();
                $('#answer').show();
                $('#answer-previous').hide();
            })
        );
}

function thinking(){
    $('#answer-thinking').show();
    $('#answer-previous').hide();
    $('#answer-answer').hide();
    $('#feedback').hide();
}

function newQuestion(){
    $('#ask').prop('disabled', false);
    $('#answer-previous').show();
    $('#feedback').hide();
}

function feedbackCorrect(){
    feedbackThanks();
}

function feedbackIncorrect(){
    feedbackThanks();
}

function feedbackPlease(){
    $('#feedback').show();
    $('#feedback-correct').show();
    $('#feedback-incorrect').show();
    $('#feedback-please').text('Is this answer correct?');
    $('#feedback-please').show();
}

function feedbackThanks(){
    $('#feedback-correct').hide();
    $('#feedback-incorrect').hide();
    $('#feedback-please').text('Thank you for providing feedback');
}


$(document).ready(function () {
    $("#question-input").focus();
    $('#question-form').submit(function(event){
        event.preventDefault();
    })
    $('#ask').click(function(){
        getAnswer();
    });
    $('#feedback-correct').click(function(){
        feedbackCorrect();
    })
    $('#feedback-incorrect').click(function(){
        feedbackIncorrect();
    })
    $("#question-input").on('change paste', function () {
        newQuestion();
    });
    $("#question-input").keyup(function(event) {
        if (event.which == 13){
            if ($('#ask').prop('disabled') == false) {
                getAnswer();
            }
        } else if (NON_CHANGING_KEYS.includes(event.which)) {
        } else{
            newQuestion();
        }
    });

});