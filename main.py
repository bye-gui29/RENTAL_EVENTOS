from flask import Flask, jsonify, request
from datetime import datetime

from database import db
from models import Equipamentos, Estoque, Funcionario


app = Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:aluno@localhost:5432/RENTAL_EVENTOS"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)



@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "API RENTAL EVENTOS funcionando!"
    })



@app.route("/equipamentos", methods=["POST"])
def cadastrar_equipamento():

    dados = request.get_json()

    equipamento = Equipamentos(
        Marca=dados["Marca"],
        Modelo=dados["Modelo"],
        Categoria=dados["Categoria"],
        Potencia=dados.get("Potencia"),
        Material=dados["Material"],
        Peso=dados["Peso"],
        Dimensoes=dados["Dimensoes"],
        cor=dados["cor"],
        Quantidade_disponivel=dados.get(
            "Quantidade_disponivel",
            0
        ),
        Quantidade_minima=dados.get(
            "Quantidade_minima",
            0
        )
    )

    db.session.add(equipamento)
    db.session.commit()

    return jsonify({
        "mensagem": "Equipamento cadastrado com sucesso!",
        "Id": equipamento.Id
    }), 201




@app.route("/equipamentos", methods=["GET"])
def consultar_equipamentos():

    equipamentos = Equipamentos.query.all()

    lista = []

    for equipamento in equipamentos:

        lista.append({
            "Id": equipamento.Id,
            "Marca": equipamento.Marca,
            "Modelo": equipamento.Modelo,
            "Categoria": equipamento.Categoria,
            "Potencia": equipamento.Potencia,
            "Material": equipamento.Material,
            "Peso": equipamento.Peso,
            "Dimensoes": equipamento.Dimensoes,
            "cor": equipamento.cor,
            "Quantidade_disponivel":
                equipamento.Quantidade_disponivel,
            "Quantidade_minima":
                equipamento.Quantidade_minima
        })

    return jsonify(lista)



@app.route("/equipamentos/<int:id>", methods=["GET"])
def consultar_equipamento(id):

    equipamento = db.session.get(Equipamentos, id)

    if not equipamento:
        return jsonify({
            "erro": "Equipamento não encontrado."
        }), 404

    return jsonify({
        "Id": equipamento.Id,
        "Marca": equipamento.Marca,
        "Modelo": equipamento.Modelo,
        "Categoria": equipamento.Categoria,
        "Potencia": equipamento.Potencia,
        "Material": equipamento.Material,
        "Peso": equipamento.Peso,
        "Dimensoes": equipamento.Dimensoes,
        "cor": equipamento.cor,
        "Quantidade_disponivel":
            equipamento.Quantidade_disponivel,
        "Quantidade_minima":
            equipamento.Quantidade_minima
    })




@app.route("/equipamentos/<int:id>", methods=["PUT"])
def atualizar_equipamento(id):

    equipamento = db.session.get(Equipamentos, id)

    if not equipamento:
        return jsonify({
            "erro": "Equipamento não encontrado."
        }), 404

    dados = request.get_json()

    equipamento.Marca = dados.get(
        "Marca",
        equipamento.Marca
    )

    equipamento.Modelo = dados.get(
        "Modelo",
        equipamento.Modelo
    )

    equipamento.Categoria = dados.get(
        "Categoria",
        equipamento.Categoria
    )

    equipamento.Potencia = dados.get(
        "Potencia",
        equipamento.Potencia
    )

    equipamento.Material = dados.get(
        "Material",
        equipamento.Material
    )

    equipamento.Peso = dados.get(
        "Peso",
        equipamento.Peso
    )

    equipamento.Dimensoes = dados.get(
        "Dimensoes",
        equipamento.Dimensoes
    )

    equipamento.cor = dados.get(
        "cor",
        equipamento.cor
    )

    equipamento.Quantidade_minima = dados.get(
        "Quantidade_minima",
        equipamento.Quantidade_minima
    )

    db.session.commit()

    return jsonify({
        "mensagem": "Equipamento atualizado com sucesso!"
    })




@app.route("/equipamentos/<int:id>", methods=["DELETE"])
def excluir_equipamento(id):

    equipamento = db.session.get(Equipamentos, id)

    if not equipamento:
        return jsonify({
            "erro": "Equipamento não encontrado."
        }), 404

    movimentacoes = Estoque.query.filter_by(
        Equipamentos=id
    ).first()

    if movimentacoes:
        return jsonify({
            "erro":
                "Não é possível excluir este equipamento "
                "porque existem movimentações no estoque."
        }), 400

    db.session.delete(equipamento)
    db.session.commit()

    return jsonify({
        "mensagem": "Equipamento excluído com sucesso!"
    })



@app.route("/estoque/entrada", methods=["POST"])
def registrar_entrada():

    dados = request.get_json()

    equipamento_id = dados["Equipamentos"]
    funcionario_id = dados["funcionarioId"]
    quantidade = dados["quantidade"]

    equipamento = db.session.get(
        Equipamentos,
        equipamento_id
    )

    funcionario = db.session.get(
        Funcionario,
        funcionario_id
    )

    if not equipamento:
        return jsonify({
            "erro": "Equipamento não encontrado."
        }), 404

    if not funcionario:
        return jsonify({
            "erro": "Funcionário não encontrado."
        }), 404

    if quantidade <= 0:
        return jsonify({
            "erro": "A quantidade deve ser maior que zero."
        }), 400

    equipamento.Quantidade_disponivel += quantidade

    movimentacao = Estoque(
        Equipamentos=equipamento_id,
        entrada=datetime.now(),
        funcionarioId=funcionario_id,
        Tipo_movimentacao="ENTRADA",
        numero_locacoes=0
    )

    db.session.add(movimentacao)
    db.session.commit()

    return jsonify({
        "mensagem": "Entrada registrada com sucesso!",
        "quantidade_disponivel":
            equipamento.Quantidade_disponivel
    }), 201



@app.route("/estoque/saida", methods=["POST"])
def registrar_saida():

    dados = request.get_json()

    equipamento_id = dados["Equipamentos"]
    funcionario_id = dados["funcionarioId"]
    quantidade = dados["quantidade"]

    equipamento = db.session.get(
        Equipamentos,
        equipamento_id
    )

    funcionario = db.session.get(
        Funcionario,
        funcionario_id
    )

    if not equipamento:
        return jsonify({
            "erro": "Equipamento não encontrado."
        }), 404

    if not funcionario:
        return jsonify({
            "erro": "Funcionário não encontrado."
        }), 404

    if quantidade <= 0:
        return jsonify({
            "erro": "A quantidade deve ser maior que zero."
        }), 400

    if equipamento.Quantidade_disponivel < quantidade:
        return jsonify({
            "erro": "Quantidade insuficiente em estoque."
        }), 400

    equipamento.Quantidade_disponivel -= quantidade

    movimentacao = Estoque(
        Equipamentos=equipamento_id,
        entrada=datetime.now(),
        Saida=datetime.now(),
        funcionarioId=funcionario_id,
        Tipo_movimentacao="SAIDA",
        numero_locacoes=quantidade
    )

    db.session.add(movimentacao)
    db.session.commit()

    return jsonify({
        "mensagem": "Saída registrada com sucesso!",
        "quantidade_disponivel":
            equipamento.Quantidade_disponivel
    }), 201




@app.route("/estoque/alertas", methods=["GET"])
def alertas_estoque():

    equipamentos = Equipamentos.query.all()

    alertas = []

    for equipamento in equipamentos:

        if (
            equipamento.Quantidade_disponivel
            <= equipamento.Quantidade_minima
        ):

            alertas.append({
                "Id": equipamento.Id,
                "Marca": equipamento.Marca,
                "Modelo": equipamento.Modelo,
                "Quantidade_disponivel":
                    equipamento.Quantidade_disponivel,
                "Quantidade_minima":
                    equipamento.Quantidade_minima,
                "alerta":
                    "ESTOQUE ABAIXO OU IGUAL AO MÍNIMO"
            })

    return jsonify(alertas)



@app.route("/estoque/historico", methods=["GET"])
def historico_estoque():

    movimentacoes = Estoque.query.order_by(
        Estoque.Id.desc()
    ).all()

    historico = []

    for movimentacao in movimentacoes:

        historico.append({
            "Id": movimentacao.Id,

            "Equipamentos":
                movimentacao.Equipamentos,

            "Marca":
                movimentacao.equipamento.Marca,

            "Modelo":
                movimentacao.equipamento.Modelo,

            "funcionarioId":
                movimentacao.funcionarioId,

            "funcionario":
                movimentacao.funcionario.email,

            "entrada":
                movimentacao.entrada,

            "Saida":
                movimentacao.Saida,

            "Tipo_movimentacao":
                movimentacao.Tipo_movimentacao,

            "numero_locacoes":
                movimentacao.numero_locacoes
        })

    return jsonify(historico)


if __name__ == "__main__":
    app.run(debug=True)