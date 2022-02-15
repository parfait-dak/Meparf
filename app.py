import os
# importer Flask
from flask import Flask, abort, jsonify,  request
from flask_sqlalchemy import SQLAlchemy  # importer SQLAlchemy
# import urllib.parse
#from urllib.parse import quote_pluspip
from flask_migrate import Migrate



app = Flask(__name__)  # Créer une instance de l'application
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ax+3@localhost:5432/projetapi'
app.config['SQLACHELMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)  # Créer une instance de BD
migrate = Migrate(app, db)


class Categorie(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    libelle_categorie = db.Column(db.String(50), nullable=False)
    books = db.relationship('Livre', backref='Categorie', lazy=True)

    def __init__(self,  libelle_categorie,books):
        self.libelle_categorie = libelle_categorie
        self.books=books

    def insert(self):
        db.session.add(self)
        db.session.commit()
     

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'libelle': self.libelle_categorie,
            }    
        
    
db.create_all()

class Livre(db.Model):
    __tablename__='livres'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(50), nullable=False)
    titre=db.Column(db.String(100),unique=True,nullable=False)
    date_publication=db.Column(db.Date(),nullable=False)
    auteur=db.Column(db.String(100),nullable=False)
    editeur=db.Column(db.String(100),nullable=False)
    categorie_id=db.Column(db.Integer, db.ForeignKey('categories.id'),nullable=False)
    
    def __init__(self, isbn,titre,date_publication,auteur,editeur,categorie_id):
        self.isbn = isbn
        self.titre = titre
        self.date_publication = date_publication
        self.auteur = auteur
        self.editeur = editeur
        self.categorie_id = categorie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()
     

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'isbn': self.isbn,
            'titre': self.titre,
            'date_publication': self.date_publication,
            'auteur': self.auteur,
            'editeur': self.editeur,
            'categorie_id': self.categorie_id,
            }    
db.create_all()


#############################################################
# fonction permettant d'afficher les éléments d'une liste
#############################################################

def get_all_l(request):
    items = [item.format() for item in request]
    return items

##############################
# Lister tous les livres
##############################

@app.route('/livres')
def get_books():
    livres = Livre.query.all()
    livres = get_all_l(livres)
    return jsonify({
        'success': True,
        'livre': livres,
        'total_livre': len(livres)
    })


#################################################
# Chercher un livre en particulier par son id
#################################################
@app.route('/livres/<int:id>')
def get_livre(id):
    livre = Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        return livre.format()


#######################################
 # Lister toutes les categories
#######################################


@app.route('/categories')
def get_categories():
    categories = Categorie.query.all()
    categories = get_all_l(categories)
    return jsonify({
        'success': True,
        'categorie': categories,
        'total_categories': len(categories)
    })
    
########################################
# Chercher une categorie par son id
########################################

@app.route('/categories/<int:id>')
def get_categorie(id):
    cat = Categorie.query.get(id)
    if cat is None:
        #abort(404)
         return jsonify({
            "succes": False,
            "error" : 404,
            "message" : "Livre  non trouver"
        }),404
    else:
        return cat.format()

############################
# Supprimer un livre
############################

@app.route('/livres/<int:id>', methods=['DELETE'])
def del_book(id):
    livre = Livre.query.get(id)
    livre.delete()
    return jsonify({
        'success': True,
        'delete successfully': id,
    })
    
#############################
# Supprimer une categorie
#############################

@app.route('/categories/<int:id>', methods=['DELETE'])
def del_categorie(id):
    cat = Categorie.query.get(id)
    cat.delete()
    return jsonify({
        'success': True,
        'delete successfully': id,
    })

 ###########################################
    # Modifier les informations d'un livre
###########################################
@app.route('/livres/<int:id>', methods=['PATCH'])
def change_book(id):
    body = request.get_json()
    book = Livre.query.get(id)
    try:
        if 'titre' in body and 'auteur' in body and 'editeur' in body:
            book.titre = body['titre']
            book.auteur = body['auteur']
            book.editeur = body['editeur']
            book.update()
            return book.format()
    except:
        #abort(404)
        return jsonify({
            "succes": False,
            "error" : 404,
            "message" : "Modification non effectuer"
        }),404
        
        

########################################
# Modifier le libellé d'une categorie
########################################

@app.route('/categories/<int:id>', methods=['PATCH'])
def change_name(id):
    body = request.get_json()
    category = Categorie.query.get(id)
    try:
        if 'libelle_categorie' in body:
            category.libelle_categorie = body['libelle_categorie']
            category.update()
        return category.format()
    except:
        #abort(404)
         return jsonify({
            "succes": False,
            "error" : 404,
            "message" : "Modification non effectuer"
        }),404
        
    
################################################
# Lister la liste des livres d'une categorie
################################################

@app.route('/livres/categories/<int:id>')
def book_category(id):
    try:
        category = Categorie.query.get(id)
        books = Livre.query.filter_by(categorie_id=id).all()
        books = get_all_l(books)
        return jsonify({
            'Success': True,
            'Status_code': 200,
            'total': len(books),
            'classe': category.format(),
            'books': books 
            })
    except:
       #abort(404)
        return jsonify({
            "succes": False,
            "error" : 404,
            "message" : "Affichage de livre par categorie non effectuer"
        }),404
       
    finally:
         db.session.close()
         


         
