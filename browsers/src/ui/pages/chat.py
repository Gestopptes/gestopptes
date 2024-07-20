from ..router import hd,router
from ..comp import overflow_box, pre

def get_chat_history():
    from llama_index.core.llms import ChatMessage
    messages = [
        ChatMessage(
            role="system", content="You are a colorful personality"
        ),
        ChatMessage(role="user", content="My Old message Here"),
    ]
    return messages

# from dataclasses import dataclass
# @dataclass
# class FakeChatMessage:
#     """Class for keeping track of an item in inventory."""
#     role: str
#     content: str
    

def submit_message(msg_text):
    from llama_index.core.llms import ChatMessage
    new_user_msg = ChatMessage(role="user", content=msg_text)
    new_system_msg = ChatMessage(role="system", content="You Said: \n'" + msg_text+"'")
    return [new_user_msg, new_system_msg]


def display_msg(msg):
    align = "end" if msg.role == "user" else "start"
    with hd.box(align=align, width="80%"):
        with hd.box(align=align, width="80%"):
            hd.h5(msg.role)
            with pre(background_color="#eee"):
                with hd.box(gap=1):
                    hd.text(msg.content)


@router.route("/chat")
def chatpage():
    hd.h1("chat")
    state = hd.state(chat_history=None)
    if state.chat_history is None:
        state.chat_history = get_chat_history()
    with hd.vbox(height="80%"):
        with overflow_box(overflow="scroll", height="100%", width="50%", align="center") as ovf_box:
            for i, msg in enumerate(state.chat_history):
                with hd.scope(i):
                    display_msg(msg)
    with hd.form() as form:
        with hd.hbox():
            chatmsg_form =     form.text_input('new message')
            chatmsg = chatmsg_form.value
            btn = form.submit_button(disabled=not chatmsg)
        hd.text('ur msg: ' + chatmsg)
    if btn.clicked:
        hd.text("sent: ", chatmsg)
        state.chat_history.extend(submit_message(chatmsg))
        chatmsg_form.value = ""