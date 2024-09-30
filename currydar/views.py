from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from currydar.forms import EventForm
from currydar.models import Events
from app import db
import requests
import datetime

def get_weather(api_key, city):
    # OpenWeatherAPIのURLを設定
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    # APIにリクエストを送信
    response = requests.get(url)
    
    if response.status_code == 200:
        # レスポンスが成功の場合、JSONデータを取得
        data = response.json()
        
        # 必要な天気情報を抽出
        # main = data['main']
        weather = data['weather'][0]
        # temperature = main['temp']
        # feels_like = main['feels_like']
        weather_main = weather['main']
        
        # # 日付情報を抽出して変換
        # timestamp = data['dt']
        # date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        
        # 天気情報を表示
        # print(f"日付: {date}")
        # print(f"都市: {city}")
        # print(f"気温: {temperature}°C")
        # print(f"体感温度: {feels_like}°C")
        return "weather:"+weather_main
    else:
        # エラーメッセージを表示
        return response.status_code, "error"


from flask import Blueprint, render_template
import random

#Blueprint currydar_app
#アプリを生成する
currydar = Blueprint(
    "currydar",
    __name__,
    template_folder="templates",
    static_folder="static",
)





@currydar.route('/')
def currydar_app(): 
    weather = get_weather("133181fd446d837a42413992c3e8b9e2", "Okayama")
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    events = [
        {
            'title': weather,
            'date': today
        }
    ]
    if current_user.is_authenticated:
        myEvents = db.session.query(Events).filter_by(user_id=current_user.id).all()
        for event in myEvents:
            events.append({
                'title': event.event,
                'date': event.date
            })
    return render_template('currydar/calendar.html', events=events)

@currydar.route('/add', methods=["GET", "POST"])
@login_required
def add_event():
    form = EventForm() # currydar/forms.pyのEventFormクラスを使えるようにする

    if form.validate_on_submit(): # フォームが正しく入力されているかをチェック
        if db.session.query(Events).count() == 0:
            newId = 1
        else:
            newId = (db.session.query(Events).order_by(desc("id")).first()).id+1
        # DBに登録する情報を取得
        events = Events(
            id = newId,
            user_id = current_user.id,
            event=form.event.data, # DBのイベントテーブルのeventにフォームに入力されたイベントを代入
            date=form.date.data, # DBのイベントテーブルのdateにフォームに入力された日付を代入
        )

        # DBにユーザを登録
        db.session.add(events)
        db.session.commit()

        return redirect(url_for("currydar.show_event")) # ユーザー一覧画面へリダイレクトする
    # フォームが正しく入力されていない場合はcrud/create.htmlに遷移
    return render_template("currydar/add.html", form=form)


@currydar.route('/show')
@login_required
def show_event():
    events = db.session.query(Events).filter_by(user_id=current_user.id).order_by("date").all() 
    return render_template("currydar/show.html", events=events) # currydar/show.htmlに遷移（変数eventsにイベント情報一覧を入れて使えるようにする）

@currydar.route('/delete/<event_id>')
@login_required
def delete(event_id):
    db.session.query(Events).filter_by(id = event_id).delete()
    db.session.commit()
    return redirect(url_for("currydar.show_event"))