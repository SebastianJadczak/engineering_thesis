function scrollToBottomChatBot() {
        const element = document.getElementById('conversation');
        element.scrollTop = element.scrollHeight;

    }
const handle_conversation_with_bot = (event) => {
    event.preventDefault()
    let csrf_token_input = document.querySelector('div#bot input[name=csrfmiddlewaretoken]').value
    let user_question = document.getElementById('user_question').value
    let conversation = document.getElementById('conversation')
    let ans = document.createElement("p");
    let que = document.createElement("p");

    $.ajax({
        type: "POST",
        url: "../../",
        data: {
            csrfmiddlewaretoken: csrf_token_input,
            user_question: user_question
        },
        success:
            function (result) {
                que.textContent = user_question
                ans.textContent = result.response
                conversation.appendChild(que)
                conversation.appendChild(ans)
                scrollToBottomChatBot()
            },
        error: function () {
            alert('error');
        }
    });
}