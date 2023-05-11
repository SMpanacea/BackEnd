# schemas.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import secret_key.config as config
import json

#자동으로 model과 데이터를 매치해주는 모듈
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.models import User, BookMark, db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        unknown = 'exclude'  # 알려지지 않은 필드를 자동으로 제외
        sqla_session = db.session

    # 값이 주어지지 않으면 자동으로 채움 
    # required = True시 무조건 받아야 함
    uid = auto_field()
    upw = auto_field()
    email = auto_field()
    nickname = auto_field()
    gender = auto_field()
    birth = auto_field()
    profile = auto_field()

class BookMarkSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BookMark
        load_instance = True
        unknown = 'exclude'  # 알려지지 않은 필드를 자동으로 제외
        sqla_session = db.session

    uid = auto_field()
    itemSeq = auto_field()
    itemName = auto_field()
    itemImage = auto_field()
    updateDe = auto_field()

class Medicine:
    def __init__(self, serviceKey = config.key, pageNo = '1', 
                numOfRows = '10', entpName = '', itemName = '', 
                itemSeq = '', efcyQesitm = '', useMethodQesitm = '', 
                atpnWarnQesitm = '', atpnQesitm = '', intrcQesitm = '', 
                seQesitm = '', depositMethodQesitm = '', openDe = '', 
                updateDe = '', type = 'json'):
    
        self.serviceKey = serviceKey
        self.pageNo = pageNo
        self.numOfRows = numOfRows
        self.entpName = entpName
        self.itemName = itemName
        self.itemSeq = itemSeq
        self.efcyQesitm = efcyQesitm
        self.useMethodQesitm  = useMethodQesitm
        self.atpnWarnQesitm  = atpnWarnQesitm
        self.atpnQesitm  = atpnQesitm
        self.intrcQesitm  = intrcQesitm
        self.seQesitm  = seQesitm
        self.depositMethodQesitm  = depositMethodQesitm
        self.openDe  = openDe
        self.updateDe  = updateDe
        self.type = type

    def get_params(self):
        return {
            'serviceKey': self.serviceKey,
            'pageNo': self.pageNo,
            'numOfRows': self.numOfRows,
            'entpName': self.entpName,
            'itemName': self.itemName,
            'itemSeq': self.itemSeq,
            'efcyQesitm': self.efcyQesitm,
            'useMethodQesitm': self.useMethodQesitm,
            'atpnWarnQesitm': self.atpnWarnQesitm,
            'atpnQesitm': self.atpnQesitm,
            'intrcQesitm': self.intrcQesitm,
            'seQesitm': self.seQesitm,
            'depositMethodQesitm': self.depositMethodQesitm,
            'openDe': self.openDe,
            'updateDe': self.updateDe,
            'type': self.type
        }

    # post로 받은 json을 객체 처리
    @classmethod
    def from_request_json(cls, request_json):
        kwargs = json.loads(request_json.decode('utf-8'))
        return cls(**kwargs)
    
    # get으로 받은 args를 객체 처리
    @classmethod
    def from_request_args(cls, request):
        return cls(
            itemSeq = request.args.get("itemSeq", ''),   # 품목기준코드
            pageNo = request.args.get("pageNo", "1"),   # 페이지 번호
            itemName = request.args.get("itemName", ''),#제품명
            entpName = request.args.get("entpName", ''), #업체명
            efcyQesitm = request.args.get("efcyQesitm", ''), #효능 
            )
    

class Multi_Info:
    def __init__(self, serviceKey = config.key,
                pageNo = '1', 
                numOfRows = '100',
                type = 'json', 
                typeName = '병용금기', 
                ingrCode = '', 
                itemName = '', 
                start_change_date = '', 
                end_change_date = '', 
                itemSeq = ''):
        self.serviceKey = serviceKey
        self.pageNo = pageNo
        self.numOfRows = numOfRows
        self.type = type
        self.typeName = typeName
        self.ingrCode = ingrCode
        self.itemName = itemName
        self.start_change_date = start_change_date
        self.end_change_date = end_change_date
        self.itemSeq = itemSeq

    def get_params(self):
        return {
            'serviceKey': self.serviceKey,
            'pageNo': self.pageNo,
            'numOfRows': self.numOfRows,
            'type': self.type,
            'typeName': self.typeName,
            'ingrCode': self.ingrCode,
            'itemName': self.itemName,
            'start_change_date': self.start_change_date,
            'end_change_date': self.end_change_date,
            'itemSeq': self.itemSeq
        }