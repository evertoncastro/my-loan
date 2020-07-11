from app import db


class LoanRequestModel(db.Model):
    __tablename__ = 'loan_request'
    id = db.Column(db.String(100), primary_key=True)
    cpf = db.Column(db.String(11))
    name = db.Column(db.String(50))
    birthdate = db.Column(
        db.Date,
        nullable=False
    )
    amount = db.Column(db.Float)
    terms = db.Column(db.Integer)
    income = db.Column(db.Float)
    status = db.Column(db.String(15), default='processing')
    result = db.Column(db.String(15))
    refused_policy = db.Column(db.String(15))
    approved_amount = db.Column(db.Float)
    approved_terms = db.Column(db.Integer)
    created = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp()
    )

    def create(self, session, **kwargs):
        new = self.__class__(**kwargs)
        session.add(new)
        return new

    def fetch(self, session, _id):
        return session.query(self.__class__).filter_by(id=_id).first()
