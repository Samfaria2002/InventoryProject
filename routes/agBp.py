from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from model.agModel import Agenda, Desktop
from sqlalchemy import func, or_, desc
import time
import json

#Instancia o Blueprint
agBp = Blueprint('agBp', __name__)

#acesso a página principal
@agBp.route('/')
def pagina_home():
    return render_template('ag_home.html')

#página de erro de pesquisa
@agBp.route('/error')
def error():
    return render_template('error_search.html')

#rota para acesso do repositório
@agBp.route('/agenda')
def lista_agenda():
    agenda_query = Agenda.query.all()
    return render_template('ag_lista.html', agenda = agenda_query)

#acesso ao template e função para criar um registro
@agBp.route('/agenda/create')
def cria_agenda():
    return render_template('ag_cria.html')

#função para adicionar novos registros
@agBp.route('/agenda/add', methods=['POST'])
def adiciona_agenda():
    
    agendaNome = request.form["nome"]
    agendaEdicao = request.form["edicao"]
    agendaVersao = request.form["versao"]
    agendaFisico = request.form["fisico"]
    agendaLicensa = request.form["licensa"]

    agenda = Agenda(nome = agendaNome, edicao = agendaEdicao, versao = agendaVersao, fisico = agendaFisico, licensa = agendaLicensa)
    db.session.add(agenda)
    db.session.commit()

    return redirect(url_for('agBp.return_agenda_json'))

#Filtra a pesquisa pelo id
@agBp.route('/agenda/update/<agenda_id>')
def atualiza_agenda(agenda_id = 0):
    agenda_query = Agenda.query.filter_by(id = agenda_id).first()
    return render_template('ag_atualiza.html', agenda = agenda_query)

#função para atualizar um registro
@agBp.route('/agenda/upd', methods=['POST'])
def agenda_upd():

    agendaId = request.form['id']
    agendaNome = request.form['nome']
    agendaEdicao = request.form["edicao"]
    agendaVersao = request.form["versao"]
    agendaFisico = request.form["fisico"]
    agendaLicensa = request.form["licensa"]

    agenda = Agenda.query.filter_by(id = agendaId).first()
    agenda.nome = agendaNome
    agenda.edicao = agendaEdicao
    agenda.versao = agendaVersao
    agenda.fisico = agendaFisico
    agenda.licensa = agendaLicensa
    db.session.add(agenda)
    db.session.commit()

    return redirect(url_for('agBp.lista_agenda'))

#deletar pelo id especificado
@agBp.route('/agenda/delete/<agenda_id>')
def agenda_deleta(agenda_id = 0):
    agenda_query = Agenda.query.filter_by(id = agenda_id).first()
    return render_template('ag_deleta.html', agenda = agenda_query)

#função para apagar o registro
@agBp.route('/agenda/dlt', methods=['POST'])
def agenda_dlt():

    agendaId = request.form['id']
    agenda = Agenda.query.filter_by(id = agendaId).first()
    db.session.delete(agenda)
    db.session.commit()

    # Atualizar IDs no banco de dados
    agenda_restantes = Agenda.query.order_by(Agenda.id).all()
    for index, agenda in enumerate(agenda_restantes):
        agenda.id = index + 1
    db.session.commit()

    # Atualizar IDs no arquivo JSON
    with open('Y:\Inventario TI\Inventario\software.json', 'r', encoding='utf-8') as arquivo:
        try:
            existing_data = json.load(arquivo)
        except json.JSONDecodeError:
            existing_data = {"software": []}

    existing_data["software"] = [item for item in existing_data["software"] if item["id"] != int(agendaId)]

    for index, item in enumerate(existing_data["software"]):
        item["id"] = index + 1

    with open('Y:\Inventario TI\Inventario\software.json', 'w', encoding='utf-8') as arquivo:
        json.dump(existing_data, arquivo, indent=4, ensure_ascii=False)
        
    return redirect(url_for('agBp.lista_agenda'))

@agBp.route('/agenda/search', methods=['POST'])
def executar_pesquisa():
    pesquisa = request.form.get('pesquisa')

    pesquisa_query = Agenda.query.filter(
        or_(
            Agenda.nome.ilike(f'%{pesquisa}%'),
            Agenda.edicao.ilike(f'%{pesquisa}%'),
            Agenda.versao.ilike(f'%{pesquisa}%'),
            Agenda.fisico == pesquisa,
            Agenda.licensa == pesquisa
        )
    ).all()

    if pesquisa_query:
        return render_template('ag_pesquisa.html', agenda = pesquisa_query)
    else:
        return redirect(url_for('agBp.error'))
    

'''

'''

'''

'''


@agBp.route('/desktop')
def lista_desktop():
    desktop_query = Desktop.query.all()

    return render_template('ag_desktop.html', desktop = desktop_query)

@agBp.route('/desktop/create')
def cria_desktop():
    return render_template('ag_criadesk.html')

@agBp.route('/desktop/add', methods=['POST'])
def adiciona_desktop():

    desktopNome = request.form.get('nome')
    desktopUsuario = request.form.get('usuario')
    desktopDepartamento = request.form.get('departamento')
    desktopSistema = request.form.get('sistema')
    desktopOffice = request.form.get('office')
    desktopTag = request.form.get('tag')
    desktopPatrimonio = request.form.get('patrimonio')

    desktop = Desktop(nome = desktopNome, usuario = desktopUsuario, departamento = desktopDepartamento, sistema = desktopSistema, office = desktopOffice, 
    tag = desktopTag, patrimonio = desktopPatrimonio)

    db.session.add(desktop)
    db.session.commit()

    return(redirect(url_for('agBp.return_desktop_json')))

@agBp.route('/desktop/update/<desktop_id>')
def atualiza_desktop(desktop_id = 0):
    desktop_query = Desktop.query.filter_by(id = desktop_id).first()

    return render_template('ag_atualizadesk.html', desktop = desktop_query)

@agBp.route('/desktop/upd', methods=['POST'])
def desktop_update():

    desktopId = request.form.get('id')
    desktopNome = request.form.get('nome')
    desktopUsuario = request.form.get('usuario')
    desktopDepartamento = request.form.get('departamento')
    desktopSistema = request.form.get('sistema')
    desktopOffice = request.form.get('office')
    desktopTag = request.form.get('tag')
    desktopPatrimonio = request.form.get('patrimonio')

    desktop_query = Desktop.query.filter_by(id = desktopId).first()
    desktop_query.nome = desktopNome
    desktop_query.usuario = desktopUsuario
    desktop_query.departamento = desktopDepartamento
    desktop_query.sistema = desktopSistema
    desktop_query.office = desktopOffice
    desktop_query.tag = desktopTag
    desktop_query.patrimonio = desktopPatrimonio

    db.session.add(desktop_query)
    db.session.commit()

    return redirect(url_for('agBp.lista_desktop'))

@agBp.route('/desktop/delete/<desktop_id>')
def deleta_desktop(desktop_id = 0):
    desktop_query = Desktop.query.filter_by(id = desktop_id).first()

    return render_template('ag_deletadesk.html', desktop = desktop_query)

@agBp.route('/desktop/dlt', methods=['POST'])
def desktop_delete():

    desktop_id = request.form.get('id')
    desktop = Desktop.query.filter_by(id = desktop_id).first()
    db.session.delete(desktop)
    db.session.commit()
    
    # Atualizar IDs no banco de dados
    desktop_restantes = Desktop.query.order_by(Desktop.id).all()
    for index, desktop in enumerate(desktop_restantes):
        desktop.id = index + 1
    db.session.commit()

    # Atualizar IDs no arquivo JSON
    with open('Y:\Inventario TI\Inventario\desktop.json', 'r', encoding='utf-8') as arquivo:
        try:
            existing_data = json.load(arquivo)
        except json.JSONDecodeError:
            existing_data = {"desktop": []}

    existing_data["desktop"] = [item for item in existing_data["desktop"] if item["id"] != int(desktop_id)]

    for index, item in enumerate(existing_data["desktop"]):
        item["id"] = index + 1

    with open('Y:\Inventario TI\Inventario\desktop.json', 'w', encoding='utf-8') as arquivo:
        json.dump(existing_data, arquivo, indent=4, ensure_ascii=False)

    return redirect(url_for('agBp.lista_desktop'))

@agBp.route('/desktop/search', methods=['POST'])
def pesquisa_desktop():

    pesquisa = request.form.get('pesquisa')

    pesquisa_query = Desktop.query.filter(
        or_(
            Desktop.nome.ilike(f'%{pesquisa}%'),
            Desktop.departamento.ilike(f'%{pesquisa}%'),
            Desktop.usuario.ilike(f'%{pesquisa}%'),
            Desktop.sistema.ilike(f'%{pesquisa}%'),
            Desktop.office.ilike(f'%{pesquisa}%'),
            Desktop.tag == pesquisa,
            Desktop.patrimonio == pesquisa
        )
    ).all()

    if pesquisa_query:
        return render_template('ag_pesquisadesk.html', desktop = pesquisa_query)
    else:
        return redirect(url_for('agBp.error'))
    

'''

'''

'''

'''


@agBp.route('/json/agenda')
def return_agenda_json():
    query_all = Agenda.query.all()

    with open('software.json', 'r', encoding='utf-8') as arquivo:
        try:
            existing_data = json.load(arquivo)
        except json.JSONDecodeError:
            existing_data = {"software": []}

    existing_id = {item['id'] for item in existing_data["software"]}

    novos_dados = []
    for query in query_all:
        if query.id not in existing_id:
            json_query = {
                "id": query.id,
                "nome": query.nome,
                "edicao": query.edicao,
                "versao": query.versao,
                "fisico": query.fisico,
                "licensa": query.licensa
            }
            novos_dados.append(json_query)

    if novos_dados:
        data = {"software": existing_data["software"] + novos_dados}

        with open('software.json', 'w', encoding='utf-8') as arquivo:
            json.dump(data, arquivo, indent=4, ensure_ascii=False)

    return redirect(url_for('agBp.lista_agenda'))

@agBp.route('/json/desktop')
def return_desktop_json():
    query_all = Desktop.query.all()

    with open('desktop.json', 'r', encoding='utf-8') as arquivo:
        try:
            existing_data = json.load(arquivo)
        except json.JSONDecodeError:
            existing_data = {"desktop": []}

    existing_id = {item['id'] for item in existing_data["desktop"]}

    novos_dados = []
    for query in query_all:
        if query.id not in existing_id:
            json_query = {
                "id": query.id,
                "nome": query.nome,
                "tag": query.tag,
                "patrimônio": query.patrimonio,
                "departamento": query.departamento,
                "usuário": query.usuario,
                "sistema": query.sistema,
                "office": query.office
            }
            novos_dados.append(json_query)

    if novos_dados:
        data = {"desktop": existing_data["desktop"] + novos_dados}

        with open('desktop.json', 'w', encoding='utf-8') as arquivo:
            json.dump(data, arquivo, indent=4, ensure_ascii=False)

    return redirect(url_for('agBp.lista_desktop'))