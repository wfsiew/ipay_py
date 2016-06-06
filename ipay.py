import hashlib, base64, logging, requests
from flask import Flask, render_template, request
<<<<<<< HEAD
from logging.handlers import RotatingFileHandler
from datetime import datetime

=======
from datetime import datetime
>>>>>>> 3928e5f8186afd938a3b3a1c43b6f259e5a88400
app = Flask(__name__)

class Config(object):
    DEBUG = False
    THREADS_PER_PAGE = 2

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

MERCHANTKEY = 'gBzekIE174'

def get_signature(s):
    k = hashlib.sha1(s).digest()
    b = base64.b64encode(k)
    return b

def build_signature(merchantcode, refno, amount, ecurrency):
<<<<<<< HEAD
=======
    merchantkey = 'gBzekIE174'
>>>>>>> 3928e5f8186afd938a3b3a1c43b6f259e5a88400
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
<<<<<<< HEAD
        'PaymentId': '2',
        'RefNo': 'A1' + datetime.now().strftime('%Y%m%d%H%M%S'),
=======
        'PaymentId': '16',
        'RefNo': 'A' + datetime.now().strftime('%Y%m%d%H%M%S'),
>>>>>>> 3928e5f8186afd938a3b3a1c43b6f259e5a88400
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

@app.route('/backend/response', methods=['POST'])
def backend_response():
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

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
=======
    return v
>>>>>>> 3928e5f8186afd938a3b3a1c43b6f259e5a88400
