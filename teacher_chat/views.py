from flask import Blueprint, render_template, redirect, url_for, request
from teacher_chat.forms import ChatMessageForm
from teacher_chat.models import Chat, Chat_File, Chat_Read, Room, Room_Member, File
from auth.models import Teacher
from datetime import datetime
import uuid
from flask_login import login_required, current_user
from app import db

chat = Blueprint(
    "chat",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@chat.route('/', methods=['GET', 'POST'])
@login_required
def chat_page():
    # 教員か生徒かの判別
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")

    teacher_num = current_user.id  # 現在ログイン中の教員ID

    # 全教員アカウント（自分以外を表示）
    teachers = Teacher.query.filter(Teacher.id != teacher_num).all()

    # 選択された教員ID（URLパラメータから取得）
    selected_teacher_id = request.args.get("teacher_id")

    chatroom = None
    messages_with_teachers = []  # 教員名付きのメッセージを格納するリスト
    form = ChatMessageForm()

    # チャットルームの特定または作成
    if selected_teacher_id:
        room_name = f"{min(current_user.id, selected_teacher_id)}_{max(current_user.id, selected_teacher_id)}"
        chatroom = Room.query.filter_by(room_name=room_name).first()

        if not chatroom:
            # チャットルームを作成
            room_id = str(uuid.uuid4())
            chatroom = Room(room_id=room_id, room_name=room_name)
            db.session.add(chatroom)
            db.session.commit()

            # チャットルームメンバーの登録
            for teacher in [current_user.id, selected_teacher_id]:
                member = Room_Member(
                    room_id=chatroom.room_id,
                    teacher_num=teacher,
                    room_member_id=f"{chatroom.room_id}_{teacher}"
                )
                db.session.add(member)
            db.session.commit()

        # メッセージ送信処理
        if form.validate_on_submit():
            message_content = form.message.data
            new_message = Chat(
                chat_id=str(uuid.uuid4()),
                teacher_num=current_user.id,
                room_id=chatroom.room_id,
                discription=message_content,
                chat_date=datetime.now()
            )
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for("teacher.chat.chat_page", teacher_id=selected_teacher_id))

        # メッセージをJOINして教員名と一緒に取得
        messages_with_teachers = db.session.query(
            Chat.discription,
            Chat.chat_date,
            Teacher.teacher_name,
            Chat.chat_id,
        ).join(Teacher, Chat.teacher_num == Teacher.id).filter(
            Chat.room_id == chatroom.room_id
        ).order_by(Chat.chat_date).all()

    return render_template(
        "teacher_chat/chat_page.html",
        teachers=teachers,
        form=form,
        messages=messages_with_teachers,
        selected_teacher_id=selected_teacher_id,
    )
