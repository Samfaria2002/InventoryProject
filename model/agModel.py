from flask import Flask
from extensions import db
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

class Agenda(db.Model):

    __tablename__ = "agenda"
    __bind_key__ = 'agenda'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    edicao = db.Column(VARCHAR(150))
    versao = db.Column(VARCHAR(150))
    fisico = db.Column(db.Integer)
    licensa = db.Column(db.Integer)

    def init(self, id, nome, edicao, versao, fisico, licensa):
        self.id = id
        self.nome = nome
        self.edicao = edicao
        self.versao = versao
        self.fisico = fisico
        self.licensa = licensa

    def __repr__(self):
        return "<Agenda(id={}, nome={}, edicao={}, versao={}, fisico={}, licensa={})>".format(self.id, self.nome, self.edicao, self.versao, self.fisico, self.licensa)


class Desktop(db.Model):

    __tablename__ = "desktop"
    __bind_key__ = 'desktop'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String(150))
    tag = db.Column(VARCHAR(255))
    patrimonio = db.Column(db.Integer)
    departamento = db.Column(VARCHAR(100))
    usuario = db.Column(db.String(150))
    sistema = db.Column(VARCHAR(255))
    office = db.Column(VARCHAR(255))

    def init(self, id, nome, tag, patrimonio, departamento, usuario, sistema, office):
        self.id = id
        self.nome = nome
        self.tag = tag
        self.patrimonio = patrimonio
        self.departamento = departamento
        self.usuario = usuario
        self.sistema = sistema
        self.office = office

    def __repr__(self):
        return "<Desktop(id={}, nome={}, tag={}, patrimonio={}, departamento={}, usuario={}, sistema={}, office={})>".format(self.id, self.nome, self.tag, self.patrimonio, self.departamento, self.usuario, self.sistema, self.office)