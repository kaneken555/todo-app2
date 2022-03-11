from datetime import datetime, date, timedelta
import random
from random import shuffle

from flask import Flask, flash, render_template, render_template, request, redirect, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc

import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

import numpy as np


from keras.preprocessing.image import (
    ImageDataGenerator,
    load_img,
    img_to_array,
    array_to_img
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


engine = create_engine("sqlite:///todo.db", connect_args={"check_same_thread":False})


Session = sessionmaker(bind=engine)
session = Session()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)
     # point追加
    point = db.Column(db.Integer, nullable=False)
    # object追加
    object = db.Column(db.String(30),nullable=False)
    # effort追加
    effort = db.Column(db.Integer, nullable=False)
    # lucky追加
    lucky = db.Column(db.Integer, nullable=False)

# pointデータベース
app1 = Flask(__name__)
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo1.db'
db1 = SQLAlchemy(app1)
engine1 = create_engine("sqlite:///todo1.db", connect_args={"check_same_thread":False})
Session1 = sessionmaker(bind=engine1)
session1 = Session1()

class Point(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    due = db1.Column(db1.DateTime, nullable=False,unique=False)
    point = db1.Column(db1.Integer, nullable=False)
    

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        all_total_point_list = session.query(Post.point).all()
        all_total_point = 0
        for list in all_total_point_list:
            all_total_point = all_total_point + list.point
        return render_template('index.html', posts=posts, today=date.today(), all_total_point=all_total_point)
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

         # point add
        point = request.form.get('point')
        object = request.form.get('object')
        effort = request.form.get('effort')
        lucky = request.form.get('lucky')


        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title, detail=detail, due=due, point=point,object=object,effort=effort,lucky=lucky)

        db.session.add(new_post)
        db.session.commit()


        # todayの総ポイントに0を追加
        today = datetime.today()
        today = today.replace(hour=0,minute=0,second=0,microsecond=0)
        yesterday1 = today + timedelta(days=-1)
        yesterday2 = today + timedelta(days=-2) 
        yesterday3 = today + timedelta(days=-3)
        yesterday4 = today + timedelta(days=-4)
        yesterday5 = today + timedelta(days=-5)
        yesterday6 = today + timedelta(days=-6)
        yesterday7 = today + timedelta(days=-7)
        point_all = session1.query(Point).all()
        due_list = []
        for list in point_all:
            # point2 = Point.query.get(list.id)
            due_list.append(list.due)

        # pointデータベースに追加
# today
        if today not in due_list:
            # 今日のトータルポイントを計算
            today_list = session.query(Post.point).filter(Post.due==today).all()
            today_total_point = 0
            for list in today_list:
                today_total_point = today_total_point + list.point
            session1.add(Point(due=today, point=today_total_point))
            session1.commit()

        else:
            # pointを更新
            today_date = session1.query(Point).filter(Point.due==today).first()
            today_date.point = 0
            session1.commit()

        # 今日のトータルポイントを計算
        today_list = session.query(Post.point).filter(Post.due==today).all()
        today_total_point = 0
        for list in today_list:
            today_total_point = today_total_point + list.point
        today_total = session1.query(Point).filter(Point.due==today).first()
        today_total.point = today_total_point
        session1.commit()
# yeterday1
        if yesterday1 not in due_list:
            # 今日のトータルポイントを計算
            yesterday1_list = session.query(Post.point).filter(Post.due==yesterday1).all()
            yesterday1_total_point = 0
            for list in yesterday1_list:
                yesterday1_total_point = yesterday1_total_point + list.point
            session1.add(Point(due=yesterday1, point=yesterday1_total_point))
            session1.commit()
        else:
            # pointを更新
            yesterday1_date = session1.query(Point).filter(Point.due==yesterday1).first()
            yesterday1_date.point = 0
            session1.commit()
        # 今日のトータルポイントを計算
        yesterday1_list = session.query(Post.point).filter(Post.due==yesterday1).all()
        yesterday1_total_point = 0
        for list in yesterday1_list:
            yesterday1_total_point = yesterday1_total_point + list.point
        yesterday1_total = session1.query(Point).filter(Point.due==yesterday1).first()
        yesterday1_total.point = yesterday1_total_point
        session1.commit()

# yeterday2
        if yesterday2 not in due_list:
            # 今日のトータルポイントを計算
            yesterday2_list = session.query(Post.point).filter(Post.due==yesterday2).all()
            yesterday2_total_point = 0
            for list in yesterday2_list:
                yesterday2_total_point = yesterday2_total_point + list.point
            session1.add(Point(due=yesterday2, point=yesterday2_total_point))
            session1.commit()
        else:
            # pointを更新
            yesterday2_date = session1.query(Point).filter(Point.due==yesterday2).first()
            yesterday2_date.point = 0
            session1.commit()
        # 今日のトータルポイントを計算
        yesterday2_list = session.query(Post.point).filter(Post.due==yesterday2).all()
        yesterday2_total_point = 0
        for list in yesterday2_list:
            yesterday2_total_point = yesterday2_total_point + list.point
        yesterday2_total = session1.query(Point).filter(Point.due==yesterday2).first()
        yesterday2_total.point = yesterday2_total_point
        session1.commit()

            
# yeterday3
        if yesterday3 not in due_list:
            # 今日のトータルポイントを計算
            yesterday3_list = session.query(Post.point).filter(Post.due==yesterday3).all()
            yesterday3_total_point = 0
            for list in yesterday3_list:
                yesterday3_total_point = yesterday3_total_point + list.point
            session1.add(Point(due=yesterday3, point=yesterday3_total_point))
            session1.commit()
        else:
            # pointを更新
            yesterday3_date = session1.query(Point).filter(Point.due==yesterday3).first()
            yesterday3_date.point = 0
            session1.commit()
        # 今日のトータルポイントを計算
        yesterday3_list = session.query(Post.point).filter(Post.due==yesterday3).all()
        yesterday3_total_point = 0
        for list in yesterday3_list:
            yesterday3_total_point = yesterday3_total_point + list.point
        yesterday3_total = session1.query(Point).filter(Point.due==yesterday3).first()
        yesterday3_total.point = yesterday3_total_point
        session1.commit()

# yeterday4
        if yesterday4 not in due_list:
            # 今日のトータルポイントを計算
            yesterday4_list = session.query(Post.point).filter(Post.due==yesterday4).all()
            yesterday4_total_point = 0
            for list in yesterday4_list:
                yesterday4_total_point = yesterday4_total_point + list.point
            session1.add(Point(due=yesterday4, point=yesterday4_total_point))
            session1.commit()
        else:
            # pointを更新
            yesterday4_date = session1.query(Point).filter(Point.due==yesterday4).first()
            yesterday4_date.point = 0
            session1.commit()
        # 今日のトータルポイントを計算
        yesterday4_list = session.query(Post.point).filter(Post.due==yesterday4).all()
        yesterday4_total_point = 0
        for list in yesterday4_list:
            yesterday4_total_point = yesterday4_total_point + list.point
        yesterday4_total = session1.query(Point).filter(Point.due==yesterday4).first()
        yesterday4_total.point = yesterday4_total_point
        session1.commit()

# yeterday5
        if yesterday5 not in due_list:
            # 今日のトータルポイントを計算
            yesterday5_list = session.query(Post.point).filter(Post.due==yesterday5).all()
            yesterday5_total_point = 0
            for list in yesterday5_list:
                yesterday5_total_point = yesterday5_total_point + list.point
            session1.add(Point(due=yesterday5, point=yesterday5_total_point))
            session1.commit()
        else:
            # pointを更新
            yesterday5_date = session1.query(Point).filter(Point.due==yesterday5).first()
            yesterday5_date.point = 0
            session1.commit()
        # 今日のトータルポイントを計算
        yesterday5_list = session.query(Post.point).filter(Post.due==yesterday5).all()
        yesterday5_total_point = 0
        for list in yesterday5_list:
            yesterday5_total_point = yesterday5_total_point + list.point
        yesterday5_total = session1.query(Point).filter(Point.due==yesterday5).first()
        yesterday5_total.point = yesterday5_total_point
        session1.commit()

# yeterday6
        if yesterday6 not in due_list:
            # 今日のトータルポイントを計算
            yesterday6_list = session.query(Post.point).filter(Post.due==yesterday6).all()
            yesterday6_total_point = 0
            for list in yesterday6_list:
                yesterday6_total_point = yesterday6_total_point + list.point
            session1.add(Point(due=yesterday6, point=yesterday6_total_point))
            session1.commit()
        else:
            # pointを更新
            yesterday6_date = session1.query(Point).filter(Point.due==yesterday6).first()
            yesterday6_date.point = 0
            session1.commit()
        # 今日のトータルポイントを計算
        yesterday6_list = session.query(Post.point).filter(Post.due==yesterday6).all()
        yesterday6_total_point = 0
        for list in yesterday6_list:
            yesterday6_total_point = yesterday6_total_point + list.point
        yesterday6_total = session1.query(Point).filter(Point.due==yesterday6).first()
        yesterday6_total.point = yesterday6_total_point
        session1.commit()

# yeterday7
        if yesterday7 not in due_list:
            # 今日のトータルポイントを計算
            yesterday7_list = session.query(Post.point).filter(Post.due==yesterday7).all()
            yesterday7_total_point = 0
            for list in yesterday7_list:
                yesterday7_total_point = yesterday7_total_point + list.point
            session1.add(Point(due=yesterday7, point=yesterday7_total_point))
            session1.commit()
        else:
            # pointを更新
            yesterday7_date = session1.query(Point).filter(Point.due==yesterday7).first()
            yesterday7_date.point = 0
            session1.commit()
        # 今日のトータルポイントを計算
        yesterday7_list = session.query(Post.point).filter(Post.due==yesterday7).all()
        yesterday7_total_point = 0
        for list in yesterday7_list:
            yesterday7_total_point = yesterday7_total_point + list.point
        yesterday7_total = session1.query(Point).filter(Point.due==yesterday7).first()
        yesterday7_total.point = yesterday7_total_point
        session1.commit()

        return redirect('/')


@app.route('/kakeibo')
def kakeibo():
    return render_template('kakeibo.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create1')
def create1():
    return render_template('create1.html')


@app.route('/helppre', methods =['GET', 'POST'])
def helppre():
    
    return render_template('helppre.html')


# History
@app.route('/history', methods =['GET', 'POST'])
def history():

    posts = Post.query.order_by(Post.due).all()
    points = session1.query(Point).order_by(Point.due).all()
    
    return render_template('history.html', posts=posts, points=points)


@app.route('/help', methods =['GET', 'POST'])
def create_help():
    posts = Post.query.order_by(Post.due).all()
    title=[]

    goal = request.form.get('object')

    # object_list = ["テスト","プロジェクト","発表会","語学学習","ゲーム","恋愛","就職","生活習慣","受験","その他"]
    object_list = []
    object_all =session.query(Post).all()
    for list in object_all:
        object_list.append(list.object)

    if goal in object_list:
        list_goal = session.query(Post).filter(Post.object==goal).all()
        for list in list_goal :
            title.append(list.title)
            random.shuffle(title)
        
    else:
        for list in posts :
            title.append(list.title)
            random.shuffle(title)


    return render_template('help.html', posts=posts , title=title)
        

@app.route('/unpograph')
def unpograph():
    # 今日の日付を取得
    today = datetime.today()
    today = today.replace(hour=0,minute=0,second=0,microsecond = 0)



# todayより前の7日をフィルターして、dayとpointリストを作製
    day_seven =session1.query(Point).order_by(desc(Point.due)).filter(Point.due<today).limit(7).all()
    day=[]
    point=[]
    for list in day_seven:
        tstr = list.due.strftime("%Y/%m/%d")
        day.append(tstr)
        point.append(list.point)          

    return render_template('unpograph.html',today=today,day=day,point=point)

@app.route('/effort')
def effort():
    return render_template('effort.html')

@app.route('/lucky')
def lucky():
    return render_template('lucky.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    post = Post.query.get(id)
    if request.method =='GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

@app.route("/static/BGM")
def play(BGM):
    return send_from_directory("static", BGM)


# Delete
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    
    return redirect('/')



# Delete_point
@app.route('/delete_point/<int:id>')
def delete_point(id):
    point = session1.query(Point).get(id)

    session1.delete(point)
    session1.commit()
    
    return redirect('/')




#こっからしたは機械学習のやつ
#分類したいクラスと学習に用いた画像のサイズ
classes = [1,2,3,4,5,6,7,8]
unsei_list = ['とんでもねえことがあるかも','マジでいいことあるぜ','よきかなあ','いいことあるかもよー','今日もいいことあったらええなあ','徳を積んで運をつかめ','プラス思考で運勢かわる！','人間万事塞翁が馬']
ganbatta = [0.4,0.6,0.8,1,1,1.2,1.4,1.6]
yokattakoto = [1.6,1.4,1.2,1,1,0.8,0.6,0.4]

img_size = 50

#アップロードされた画像を保存するフォルダ名とアップロードを許可する拡張子
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#アップロードされたファイルの拡張子のチェックをする関数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#学習済みモデルをロード
model = load_model('classfier_model.h5')


@app.route('/pre_graph', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')

            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            #受け取った画像を読み込み、np形式に変換
            img = image.load_img(filepath, grayscale=True, target_size=(img_size,img_size))
            img = img.convert('RGB')
            #画像データを50 x 50に変換
            img = img.resize((img_size, img_size))
            # 画像データをnumpy配列に変換
            img = np.asarray(img)
            img = img / 255.0
            result = model.predict(np.array([img]))
            predicted = result.argmax()
            pred_answer = "今日の運勢ランキングは " + str(classes[predicted]) + " 位です"
            unsei = unsei_list[predicted]
            ganbatta_w = ganbatta[predicted]
            yokattakoto_w = yokattakoto[predicted]


            return render_template("pre_graph.html",answer=pred_answer,answer2=unsei,filepath=filepath,ganbatta_w=ganbatta_w,yokattakoto_w=yokattakoto_w)

    return render_template("pre_graph.html",answer="")




if __name__ == '__main__':
    app.run(debug=True)



