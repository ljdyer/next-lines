var NON_CHANGING_KEYS = [9, 16, 17, 18, 20, 33, 34, 35, 36, 37, 38, 39, 40, 44, 45];

function handleAsk(){
    showThinking();
    disableEdit();
    let inputLine = $("#question-input").val();
    getAnswer(inputLine);
}

function getAnswer(inputLine){
    fetch('/get_answer', {method: "POST", body: inputLine}).then(
        response => response.text().then(json_response => {
            response = JSON.parse(json_response);
            console.log(response);
            if (response.success){
                $('#next-line').text(response.next_line);
                $('#song-name').text(response.song_name);
                $('#artist-name').text(response.artist_name);
                showAnswer();
            } else{
                showPass();
            }
            enableEdit();
        })
    );
}

function handleQuestionInputKeyup(event){
    if (event.which == 13) {
        if ($('#ask').prop('disabled') == false) {
            handleAsk();
        }
    } else if (!(NON_CHANGING_KEYS.includes(event.which))) {
        handleEdit();
    }
}

function handleEdit(){
    if ($('#answer-answer').is(":visible")){
        $('#answer-previous').show();
    }
    enableAsk();
}
        
function showThinking(){
    hideAllAnswerAndFeedbackDivs();
    $('#feedback').children('div').hide();
    $('#answer-thinking').show();
}

function showAnswer(){
    hideAllAnswerAndFeedbackDivs();
    $('#answer-answer').show();
    feedbackPlease();
}

function showPass(){
    hideAllAnswerAndFeedbackDivs();
    $('#answer-pass').show();
}

function hideAllAnswerAndFeedbackDivs(){
    $('#answer').children('div').hide();
    $('#feedback').children('div').hide();
}

function feedbackCorrect(){
    feedbackThanks();
}

function feedbackIncorrect(){
    feedbackThanks();
}

function feedbackPlease(){
    $('#feedback').children('div').hide();
    $('#feedback-please').show();
    $('#feedback-buttons').show();
}

function feedbackThanks(){
    $('#feedback').children('div').hide();
    $('#feedback-thanks').show();
}

function disableEdit(){
    $('#question-input').prop('disabled', true);
    $('#ask').prop('disabled', true);
}

function enableEdit(){
    $('#question-input').prop('disabled', false);
    $('#question-input').focus();
}

function enableAsk(){
    $('#ask').prop('disabled', false);
}


$(document).ready(function () {
    $('#ask').click(function(){
        handleAsk();
    });
    $('#feedback-correct').click(function(){
        feedbackCorrect();
    });
    $('#feedback-incorrect').click(function(){
        feedbackIncorrect();
    });
    $("#question-input").on('change paste', function () {
        handleEdit();
    });
    $("#question-input").keyup(function(event) {
        handleQuestionInputKeyup(event);
    });
    $("#question-input").focus();
});