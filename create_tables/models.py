'''from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()'''

from flask_login import current_user,UserMixin
from .. import db
import datetime
from dateutil import relativedelta


'''class User(Base):
    __tablename__ = 'connexion'
    id_con = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    mail = Column(String)
    matricule = Column(String)
    mot_de_passe = Column(String)

    def __repr__(self):
        return "<User(nom='{}', prenom='{}', mail='{}', matricule='{}', mot_de_passe='{}')>"\
                .format(self.nom, self.prenom, self.mail, self.matricule, self.mot_de_passe)'''

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20))
    prenom = db.Column(db.String(50))
    mail = db.Column(db.String(100))
    matricule = db.Column(db.String(10))
    mot_de_passe = db.Column(db.String(255))
    #role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
    role=db.relationship('Role', secondary='user_roles')
    expire_data=db.Column(db.DateTime,default=datetime.datetime.today().date()+relativedelta.relativedelta(months=3))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<Role {}>".format(self.name)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))





'''class Checkpoint(db.Model):
    __tablename__ = 'point_control'
    id_control = Column(Integer, primary_key=True)
    white_list = Column(String)
    montant_cheque = Column(String)
    seuil_montant = Column(String)

    def __repr__(self):
        return "<Checkpoint(white_list='{}',montant_cheque='{}', seuil_montant='{}')>"\
                .format(self.while_list, self.montant_cheque, self.seuil_montant)'''


#user = User(
#     nom = 'paul',
#     prenom = 'elie',
#     mail='paul.elie@live.fr',
#     matricule = '1538',
#     mot_de_passe = 'azerty'
#)

#trace = Trace(
#    nom_traitant = 'paul',
#    mail_traitant = 'paul.elie@live.fr',
#    num_cheque = '43550',
#    montant_cheque = '500000',
#    compte_client = 'C008',
#    nom_beneficiaire = 'yves',
#    seuil_montant ='superieur'
#)

#checkpoint = Checkpoint(
#    white_list = 'ok',
#    montant_cheque = 'ok',
#    seuil_montant = 'ok'
#)
