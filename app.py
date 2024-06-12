import os.path
import time
from datetime import datetime
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from time import sleep
from wordcloud import WordCloud
from werkzeug.security import generate_password_hash, check_password_hash
import win32com.client as client
import matplotlib.ticker as ticker
import pythoncom
import torch
import pandas as pd
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from transformers import *
import openpyxl
from tkinter import *
from tkinter import messagebox
from parrot import Parrot
import csv

db = SQLAlchemy()
app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)

def paraphrase():
    parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
    phrases = ["I am testing my name", "Today is a amazing day to hangout with the family in Malaysia"]
    for phrase in phrases:
        print("-" * 100)
        print("Input_phrase: ", phrase)
        print("-" * 100)
        para_phrases = parrot.augment(input_phrase=phrase, use_gpu=False)
        for para_phrase in para_phrases:
            print(para_phrase)
    return render_template('massSend.html', para_phrases=para_phrases)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mass_send', methods=['POST'])
def saveValue():
    file = request.form['file']
    content = request.form['content']
    chunks = request.form['num-chunks']
    time = request.form['time-interval']

    pythoncom.CoInitialize()
    with open(file, newline='') as lines:
        reader = csv.reader(lines)
        header = next(reader)
        individual = [row for row in reader]

    # Emails to send out every cycle
    chunks = [individual[x:x + int(chunks)] for x in range(0, len(individual), int(chunks))]

    template = content
    outlook = client.Dispatch("Outlook.Application")
    if 'submitType' in request.form:
        if request.form['submitType'] == 'Submit':
            for chunk in chunks:
                for name, email, subject, attachment in chunk:
                    if attachment == '':
                        message = outlook.CreateItem(0)
                        message.To = email
                        message.Subject = subject
                        index = message.HTMLbody.find('>', message.HTMLbody.find('<body'))
                        message.HTMLBody = message.HTMLbody[:index + 1] + template.format(name)
                        # message.Send()
                        message.Display()

                    else:
                        message = outlook.CreateItem(0)
                        # message.Display()
                        message.To = email
                        message.Subject = subject
                        #Get signature
                        # message.GetInspector
                        index = message.HTMLbody.find('>', message.HTMLbody.find('<body'))
                        message.HTMLBody = message.HTMLbody[:index + 1] + template.format(name)

                        attachments = attachment.split(', ')
                        for i in range(len(attachments)):
                            message.Attachments.Add(attachments[i])
                        # message.Send()
                        message.Display()
                sleep(int(time))

            specialChar = ['<strong>','</strong>','<i>','</i>','<u>','</u>','<p>','</p>','<br>','<ol>','</ol>','<span class="ql-ui" contenteditable="false">','</span>',
                           '<li data-list="ordered">','<li data-list="bullet">','</li>','<em>','</em>']
            for char in specialChar:
                template = ' '.join(template.split(char))
            words = template.strip().split()
            print(words)
            tdy = datetime.now()
            tdymonth = tdy.strftime("%b")
            combineWords = ','.join(words)
            txtfile = open(tdymonth + ".txt", 'a')
            readfile = open(tdymonth + ".txt", 'r')
            first_char = readfile.read(1)
            # txtfile = open("wordContent.txt", 'a')
            if not first_char:
                txtfile.write(combineWords)
            else:
                txtfile.write("," + combineWords)
            txtfile.close()

            return render_template('loading.html'), {"Refresh": "4; url=mass_send"}

        elif request.form['submitType'] == 'Save':
            for chunk in chunks:
                for name, email, subject, attachment in chunk:
                    if attachment == '':
                        message = outlook.CreateItem(0)
                        message.To = email
                        message.Subject = subject
                        # Get signature
                        message.GetInspector
                        index = message.HTMLbody.find('>', message.HTMLbody.find('<body'))
                        message.HTMLBody = message.HTMLbody[:index + 1] + template.format(name) + message.HTMLbody[index + 1:]
                        message.Save()

                    else:
                        message = outlook.CreateItem(0)
                        message.To = email
                        message.Subject = subject
                        # Get signature
                        message.GetInspector
                        index = message.HTMLbody.find('>', message.HTMLbody.find('<body'))
                        message.HTMLBody = message.HTMLbody[:index + 1] + template.format(name) + message.HTMLbody[index + 1:]
                        attachments = attachment.split(', ')
                        for i in range(len(attachments)):
                            message.Attachments.Add(attachments[i])
                        message.Save()
        #     if attachment == '':
        #         for chunk in chunks:
        #             for name, email in chunk:
        #                 message = outlook.CreateItem(0)
        #                 message.To = email
        #                 message.Subject = subject
        #                 message.HTMLBody = template.format(name)
        #                 message.Save()
        #             # sleep(int(time))
        #     else:
        #         for chunk in chunks:
        #             for name, email in chunk:
        #                 message = outlook.CreateItem(0)
        #                 message.To = email
        #                 message.Subject = subject
        #                 message.HTMLBody = template.format(name)
        #                 for i in range(len(attachments)):
        #                     message.Attachments.Add(attachments[i])
        #                 message.Save()
        #             # sleep(int(time))
            return render_template('loading.html'), {"Refresh": "4; url=mass_send"}
    elif 'paraphrase-btn' in request.form:
        specialChar = ['<strong>', '</strong>', '<i>', '</i>', '<u>', '</u>', '<p>', '</p>', '<br>', '<ol>', '</ol>',
                       '<span class="ql-ui" contenteditable="false">', '</span>',
                       '<li data-list="ordered">', '<li data-list="bullet">', '</li>', '<em>', '</em>']
        for char in specialChar:
            template = ' '.join(template.split(char))
        words = template.strip().split()
        combineWords = ' '.join(words)

        parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")
        phrases = combineWords
        para_phrases = parrot.augment(input_phrase=phrases, use_gpu=False, diversity_ranker="levenshtein")
        print(para_phrases)
        #Access the text values only from the tuple list
        result = [phrase[0] for phrase in para_phrases]
        print("This will display only the text of the tuple: " + str(result[0]))

        return render_template('massSend.html', result=result, length=len(result))
        # return render_template('loading.html'), {"Refresh": "4; url=mass_send"}

@app.route('/mass_send')
def massSend():
    return render_template('massSend.html')

@app.route('/dashboard')
def dashboard():
    tdy = datetime.now()
    tdymonth = tdy.strftime("%b")
    month = tdy.strftime("%B")
    try:
        with open(tdymonth + '.txt', 'r', encoding='utf-8') as file:
            word = file.read().lower()
        words = word.split(',')

        if word != '':
            wordcloud = WordCloud(width=800, height=400, background_color='#101820').generate(word)
            wordcloud.to_file('static/wordcloud.png')
            word_count = Counter(words)

            sorted_word_counts = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))
            top_10_words = list(sorted_word_counts.keys())[:10]
            top_10_counts = [sorted_word_counts[item] for item in top_10_words]

            plt.figure(figsize=(10, 6))
            # plt.bar(word_count.keys(), word_count.values())
            plt.bar(top_10_words, top_10_counts)
            plt.xlabel('Words')
            plt.ylabel('Count')
            plt.title('Word Count Bar Chart')
            plt.xticks(rotation=45, ha='right')
            plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
            plt.tight_layout()
            plt.savefig('static/barchart.png')
        return render_template('dashboard.html', month=month)
    except FileNotFoundError as e:
        app.logger.error(f"File not found: {e}")
        raise e
@app.errorhandler(FileNotFoundError)
def file_error(error):
    return render_template('emptyContent.html'),404,{"Refresh": "4; url=mass_send"}

@app.route('/excel')
def excelTemp():
    return render_template('excelTemp.html')

@app.route('/excel', methods=['POST'])
def excelFunc():
    CSVfile = request.form['CSVfile']
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    attachment = request.form['attachment']

    with open(CSVfile, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow([name, email, subject, attachment])

    return render_template('loading.html'), {"Refresh": "4; url=excel"}

@app.route('/loading')
def submitLoading():
    return render_template('submitLoading.html'),{"Refresh": "0.5; url=/"}

@app.route('/login', methods=['GET','POST'])
def signIn():
    if request.method == 'POST':
        if 'sign-in-btn' in request.form:
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for(index))
                else:
                    print("wrong")
                    # flash("Incorrect login", category='error')
            else:
                print("not exist")
                # flash("Email does not exists", category='error')

        elif 'sign-up-btn' in request.form:
            signUpEmail = request.form['signUpEmail']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            signUpPassword = request.form['signUpPassword']
            user = User.query.filter_by(email=signUpEmail).first()
            if user:
                print("already exist")
                # flash("Email already exist", category='error')
            else:
                new_user = User(email=signUpEmail,password=generate_password_hash(signUpPassword),
                                first_name=firstName, last_name=lastName)
                db.session.add(new_user)
                db.session.commit()
                login_user(user, remember=True)


    return render_template('loginPage.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for(signIn))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
