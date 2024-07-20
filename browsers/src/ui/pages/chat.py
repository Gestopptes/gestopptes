from ..router import hd,router

@router.route("/chat")
def homepage():
    hd.h1("chat")

    state = hd.state(chat_history=None)
    if state.chat_history is None:
        state.chat_history = []

    hd.text(state.chat_history)

    with hd.form() as form:
        with hd.hbox():
            chatmsg_form =     form.text_input('new message')
            chatmsg = chatmsg_form.value
            btn = form.submit_button(disabled=not chatmsg)

        hd.text('ur msg: ' + chatmsg)
    if btn.clicked:
        hd.text("sent: ", chatmsg)
        state.chat_history.append(chatmsg)
        chatmsg_form.value = ""
        