import hashlib, base64, logging, requests, traceback
from flask import Flask, render_template, request
from logging.handlers import RotatingFileHandler, SMTPHandler
from datetime import datetime

app = Flask(__name__)

class Config(object):
    DEBUG = False
    THREADS_PER_PAGE = 2
    MAIL_SERVER = 'mail.redtone.com'
    MAIL_PORT = 587

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

app.config.from_object(DevelopmentConfig)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s")
handler = RotatingFileHandler('ipay.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

ADMINS = ['wingfei.siew@redtone.com']
mailhandler = SMTPHandler('mail.redtone.com', 'redtonernd@redtone.com', ADMINS, '[IPAY] ERROR')
mailhandler.setLevel(logging.ERROR)
app.logger.addHandler(mailhandler)

MERCHANTKEY = 'gBzekIE174'

def get_signature(s):
    k = hashlib.sha1(s).digest()
    b = base64.b64encode(k)
    return b

def build_signature(merchantcode, refno, amount, ecurrency):
    amt = amount.replace('.', '').replace(',', '')
    ls = [MERCHANTKEY, merchantcode, refno, amt, ecurrency]
    k = ''.join(ls)
    signature = get_signature(k)
    return signature

def build_response_signature(merchantcode, paymentid, refno, amount, ecurrency, status):
    amt = amount.replace('.', '').replace(',', '')
    ls = [MERCHANTKEY, merchantcode, paymentid, refno, amt, ecurrency, status]
    k = ''.join(ls)
    signature = get_signature(k)
    return signature

@app.route('/')
def index():
    return 'ok'

@app.route('/submit')
def submit():
    o = {
        'MerchantCode': 'M05252',
        'PaymentId': '',
        'RefNo': 'A1' + datetime.now().strftime('%Y%m%d%H%M%S'),
        'Amount': '1.00',
        'Currency': 'MYR',
        'ProdDesc': 'Photo Print',
        'UserName': 'wfsiew',
        'UserEmail': 'siewwingfei@hotmail.com',
        'UserContact': '0126500100',
        'Remark': '',
        'Lang': 'UTF-8',
        'Signature': ''
    }
    o['Signature'] = build_signature(o['MerchantCode'], o['RefNo'], o['Amount'], o['Currency'])

    return render_template('submit.html', o=o)

@app.route('/response', methods=['POST'])
def response():
    try:
        merchantcode = request.form["MerchantCode"]
        paymentid = request.form["PaymentId"]
        refno = request.form["RefNo"]
        amount = request.form["Amount"]
        ecurrency = request.form["Currency"]
        remark = request.form["Remark"]
        transid = request.form["TransId"]
        authcode = request.form["AuthCode"]
        estatus = request.form["Status"]
        errdesc = request.form["ErrDesc"]
        signature = request.form["Signature"]

        app.logger.info(request.form)
        qs = build_response_signature(merchantcode, paymentid, refno, amount, ecurrency, estatus)
        app.logger.info(qs)

        v = 'Payment fail.'

        if estatus == '1' and qs == signature:
            v = 'Thank you for payment.'

        return v

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return unicode(e)

@app.route('/backend/response', methods=['POST'])
def backend_response():
    try:
        merchantcode = request.form["MerchantCode"]
        paymentid = request.form["PaymentId"]
        refno = request.form["RefNo"]
        amount = request.form["Amount"]
        ecurrency = request.form["Currency"]
        remark = request.form["Remark"]
        transid = request.form["TransId"]
        authcode = request.form["AuthCode"]
        estatus = request.form["Status"]
        errdesc = request.form["ErrDesc"]
        signature = request.form["Signature"]

        app.logger.info(request.form)
        qs = build_response_signature(merchantcode, paymentid, refno, amount, ecurrency, estatus)
        app.logger.info(qs)

        v = 'Fail'

        if estatus == '1' and qs == signature:
            v = 'RECEIVEOK'

        return v

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return unicode(e)

@app.route('/req')
def requery():
    o = {
        'RefNo': '',
        'Amount': ''
    }
    return render_template('requery.html',  o=o)

@app.route('/req/submit', methods=['POST'])
def requery_submit():
    k = {
        'MerchantCode': 'M05252',
        'RefNo': request.form['RefNo'],
        'Amount': request.form['Amount']
    }
    url = 'https://www.mobile88.com/ePayment/enquiry.asp'
    r = requests.post(url, data=k)
    
    o = {
        'RefNo': k['RefNo'],
        'Amount': k['Amount'],
        'Data': r.text
    }
    return render_template('requery.html', o=o)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)