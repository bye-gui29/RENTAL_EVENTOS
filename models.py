from database import db


class Funcionario(db.Model):
    __tablename__ = "Funcionario"

    Id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(10), nullable=False)


class Equipamentos(db.Model):
    __tablename__ = "Equipamentos"

    Id = db.Column(db.Integer, primary_key=True)
    Marca = db.Column(db.String(100), nullable=False)
    Modelo = db.Column(db.String(100), nullable=False)
    Categoria = db.Column(db.String(100), nullable=False)
    Potencia = db.Column(db.String(100))
    Material = db.Column(db.String(100), nullable=False)
    Peso = db.Column(db.String(100), nullable=False)
    Dimensoes = db.Column(db.String(100), nullable=False)
    cor = db.Column(db.String(100), nullable=False)
    Quantidade_disponivel = db.Column(db.Integer, default=0)
    Quantidade_minima = db.Column(db.Integer, default=0)


class Estoque(db.Model):
    __tablename__ = "Estoque"

    Id = db.Column(db.Integer, primary_key=True)

    Equipamentos = db.Column(
        db.Integer,
        db.ForeignKey("Equipamentos.Id"),
        nullable=False
    )

    entrada = db.Column(db.DateTime, nullable=False)

    Saida = db.Column(db.DateTime)

    funcionarioId = db.Column(
        db.Integer,
        db.ForeignKey("Funcionario.Id"),
        nullable=False
    )

    Tipo_movimentacao = db.Column(
        db.String(100),
        nullable=False
    )

    numero_locacoes = db.Column(db.Integer)

    equipamento = db.relationship(
        "Equipamentos",
        backref="movimentacoes"
    )

    funcionario = db.relationship(
        "Funcionario",
        backref="movimentacoes"
    )