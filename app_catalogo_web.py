# app_catalogo_web.py
import sqlite3
import json
import os
import urllib.parse
from flask import Flask, render_template_string, request, redirect, url_for, send_file

app = Flask(__name__)

DB_PATH = "dalvan.db"
WHATSAPP_LOJA = "5581999998888"  # Substitua pelo WhatsApp da Ágil Aviamentos com DDD


TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ágil Aviamentos - Catálogo Online</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            background-color: #172033;
            color: #E5E7EB;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #1F2A44;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #2563EB;
        }

        h1 {
            margin: 0;
            color: #FACC15;
            font-size: 24px;
        }

        p {
            color: #94A3B8;
            font-size: 14px;
            margin: 5px 0 0 0;
        }

        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 10px;
        }

        .produto-card {
            background-color: #1F2A44;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        .prod-info {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        /*
         * FOTO PEQUENA DO CATÁLOGO
         */
        .prod-img {
            width: 80px;
            height: 80px;
            min-width: 80px;
            background-color: #0F172A;
            border-radius: 8px;
            object-fit: cover;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94A3B8;
            font-size: 12px;
            text-align: center;
            cursor: zoom-in;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .prod-img:hover {
            transform: scale(1.06);
            box-shadow: 0 0 0 2px #2563EB;
        }

        .prod-detalhes {
            flex-grow: 1;
        }

        .prod-nome {
            font-size: 16px;
            font-weight: bold;
            color: #E5E7EB;
            margin-bottom: 4px;
        }

        .prod-preco {
            font-size: 15px;
            color: #22C55E;
            font-weight: bold;
        }

        .grade-container {
            margin-top: 12px;
            background-color: #0F172A;
            padding: 10px;
            border-radius: 8px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            justify-content: space-between;
        }

        .tamanho-box {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .tamanho-box label {
            font-size: 11px;
            color: #FACC15;
            font-weight: bold;
            margin-bottom: 2px;
        }

        .tamanho-box input {
            width: 45px;
            height: 30px;
            background-color: #1F2A44;
            border: 1px solid #2E3F66;
            color: #FFF;
            text-align: center;
            border-radius: 4px;
            font-size: 13px;
        }

        .carrinho-float {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #1F2A44;
            padding: 15px;
            border-top: 2px solid #2563EB;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 100;
        }

        .form-cliente {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .form-cliente input {
            flex-grow: 1;
            padding: 10px;
            border-radius: 6px;
            border: none;
            background-color: #0F172A;
            color: #FFF;
            font-size: 14px;
        }

        .btn-enviar {
            background-color: #22C55E;
            color: #000;
            font-weight: bold;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-size: 15px;
            cursor: pointer;
            text-align: center;
            width: 100%;
        }

        .btn-enviar:hover {
            background-color: #16a34a;
        }


        /* =========================================================
           MODAL DE IMAGEM AMPLIADA
           ========================================================= */

        #modalZoom {
            display: none;
            position: fixed;
            z-index: 99999;
            inset: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.96);
            align-items: center;
            justify-content: center;
            padding: 70px 30px 40px 30px;
            overflow: hidden;
        }

        /*
         * A imagem agora pode ocupar praticamente toda a tela.
         * width/height NÃO ficam em auto.
         */
        #imgAmpliada {
            display: block;
            width: auto;
            height: auto;

            /* tamanho máximo real da imagem na tela */
            max-width: 95vw;
            max-height: 88vh;

            min-width: 200px;
            min-height: 200px;

            object-fit: contain;
            object-position: center;

            border-radius: 10px;
            background: #111827;

            box-shadow:
                0 0 0 2px rgba(255,255,255,0.10),
                0 20px 70px rgba(0,0,0,0.85);

            cursor: zoom-in;

            transition: transform 0.20s ease;
            transform: scale(1);
        }

        /*
         * Quando a foto é muito pequena, não deixamos o navegador
         * manter os 80x80 do catálogo.
         */
        #imgAmpliada.ampliada {
            max-width: 95vw !important;
            max-height: 88vh !important;
        }

        .zoom-area {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: auto;
            padding: 20px;
        }

        .fechar {
            position: fixed;
            top: 15px;
            right: 20px;
            color: #fff;
            font-size: 38px;
            font-weight: bold;
            cursor: pointer;
            z-index: 100001;
            background: rgba(0,0,0,0.75);
            width: 52px;
            height: 52px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #fff;
            line-height: 1;
            user-select: none;
        }

        .fechar:hover {
            color: #22C55E;
            border-color: #22C55E;
            transform: scale(1.05);
        }

        .controles-zoom {
            position: fixed;
            bottom: 18px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 100001;
            display: flex;
            gap: 8px;
            background: rgba(0,0,0,0.78);
            padding: 8px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.15);
        }

        .controles-zoom button {
            width: 44px;
            height: 40px;
            border: none;
            border-radius: 8px;
            background: #1F2A44;
            color: white;
            font-size: 21px;
            font-weight: bold;
            cursor: pointer;
        }

        .controles-zoom button:hover {
            background: #2563EB;
        }

        .controles-zoom .btn-reset {
            width: auto;
            padding: 0 12px;
            font-size: 13px;
        }

        @keyframes aparecerZoom {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        @keyframes imagemZoom {
            from {
                opacity: 0;
                transform: scale(0.80);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        #modalZoom.aberto {
            animation: aparecerZoom 0.18s ease-out;
        }

        #modalZoom.aberto #imgAmpliada {
            animation: imagemZoom 0.22s ease-out;
        }

        @media (max-width: 600px) {
            .container {
                padding: 8px;
            }

            #modalZoom {
                padding: 60px 8px 70px 8px;
            }

            #imgAmpliada {
                max-width: 98vw;
                max-height: 82vh;
            }

            .fechar {
                top: 8px;
                right: 8px;
                width: 46px;
                height: 46px;
                font-size: 32px;
            }

            .controles-zoom {
                bottom: 8px;
            }

            .prod-img {
                width: 75px;
                height: 75px;
                min-width: 75px;
            }
        }
    </style>
</head>

<body>

    <header>
        <h1>Ágil Aviamentos & Confecções</h1>
        <p>Clique na foto para ampliar • Escolha a grade e finalize pelo WhatsApp</p>
    </header>


    <div class="container" style="margin-bottom: 140px;">

        <form action="/enviar_pedido" method="POST" id="formPedido">

            {% for p in produtos %}

            <div class="produto-card">

                <div class="prod-info">

                    {% if p[6] and p[6] != '' %}

                    <img
                        src="{{ url_for('ver_imagem', caminho=p[6]) }}"
                        class="prod-img"
                        data-imagem="{{ url_for('ver_imagem', caminho=p[6]) }}"
                        onclick="abrirZoom(this.dataset.imagem)"
                        onerror="this.style.display='none'"
                        title="Clique para ampliar"
                        alt="Foto do produto"
                    >

                    {% else %}

                    <div class="prod-img">Sem Foto</div>

                    {% endif %}


                    <div class="prod-detalhes">

                        <div class="prod-nome">
                            {{ p[1] }} - {{ p[2] }}
                        </div>

                        <div class="prod-preco">
                            R$ {{ "%.2f"|format(p[4]) }}
                        </div>

                        <div style="font-size: 12px; color: #94A3B8; margin-top: 2px;">
                            Grupo: {{ p[9] }} | Ref: {{ p[10] }}
                        </div>

                    </div>

                </div>


                {% if p[13] and p[13] != '{}' %}

                <div class="grade-container">

                    <span style="font-size: 12px; color: #94A3B8; width: 100%; margin-bottom: 4px;">
                        Quantidade por Tamanho:
                    </span>

                    {% set grade = p[13]|from_json %}

                    {% for tam, qtd_est in grade.items() %}

                    <div class="tamanho-box">

                        <label>{{ tam }}</label>

                        <input
                            type="number"
                            name="item_{{ p[0] }}_{{ tam }}"
                            value="0"
                            min="0"
                            max="{{ qtd_est }}"
                        >

                    </div>

                    {% endfor %}

                </div>

                {% endif %}

            </div>

            {% endfor %}


            <div class="carrinho-float">

                <div class="form-cliente">

                    <input
                        type="text"
                        name="cliente_nome"
                        placeholder="Seu Nome Completo"
                        required
                    >

                    <input
                        type="tel"
                        name="cliente_tel"
                        placeholder="Seu WhatsApp (com DDD)"
                        required
                    >

                </div>

                <button type="submit" class="btn-enviar">
                    🚀 Enviar Pedido Pronto para o WhatsApp
                </button>

            </div>

        </form>

    </div>


    <!-- =========================================================
         MODAL DE IMAGEM AMPLIADA
         ========================================================= -->

    <div id="modalZoom" onclick="fecharZoom(event)">

        <span
            class="fechar"
            onclick="fecharZoom(event)"
            title="Fechar"
        >
            &times;
        </span>

        <div class="zoom-area" onclick="fecharZoom(event)">

            <img
                id="imgAmpliada"
                class="ampliada"
                src=""
                alt="Imagem ampliada"
                onclick="event.stopPropagation()"
            >

        </div>


        <div class="controles-zoom" onclick="event.stopPropagation()">

            <button type="button" onclick="alterarZoom(-0.15)" title="Diminuir">
                −
            </button>

            <button type="button" onclick="resetarZoom()" class="btn-reset">
                100%
            </button>

            <button type="button" onclick="alterarZoom(0.15)" title="Aumentar">
                +
            </button>

        </div>

    </div>


    <script>

        let escalaZoom = 1;


        function abrirZoom(src) {

            const modal = document.getElementById("modalZoom");
            const imagem = document.getElementById("imgAmpliada");

            escalaZoom = 1;

            imagem.style.transform = "scale(1)";
            imagem.src = src;

            /*
             * Remove qualquer tamanho herdado da miniatura.
             */
            imagem.style.width = "auto";
            imagem.style.height = "auto";

            modal.style.display = "flex";
            modal.classList.add("aberto");

            document.body.style.overflow = "hidden";

            /*
             * Garante que a imagem fique centralizada depois
             * de carregar.
             */
            imagem.onload = function() {
                imagem.classList.add("ampliada");
                imagem.style.transform = "scale(1)";
            };

        }


        function fecharZoom(event) {

            if (event) {
                /*
                 * Só fecha quando o clique foi no fundo do modal
                 * ou no botão X.
                 */
                const alvo = event.target;

                if (
                    alvo.id !== "modalZoom" &&
                    !alvo.classList.contains("fechar")
                ) {
                    return;
                }
            }

            const modal = document.getElementById("modalZoom");

            modal.style.display = "none";
            modal.classList.remove("aberto");

            document.getElementById("imgAmpliada").src = "";

            document.body.style.overflow = "";

            escalaZoom = 1;
        }


        function alterarZoom(valor) {

            const imagem = document.getElementById("imgAmpliada");

            escalaZoom += valor;

            if (escalaZoom < 0.50) {
                escalaZoom = 0.50;
            }

            if (escalaZoom > 3.00) {
                escalaZoom = 3.00;
            }

            imagem.style.transform = "scale(" + escalaZoom + ")";

        }


        function resetarZoom() {

            escalaZoom = 1;

            document.getElementById("imgAmpliada").style.transform =
                "scale(1)";

        }


        /*
         * Duplo clique na foto:
         * aumenta bastante.
         */
        document.getElementById("imgAmpliada").addEventListener(
            "dblclick",
            function(event) {

                event.stopPropagation();

                if (escalaZoom === 1) {
                    escalaZoom = 1.8;
                } else {
                    escalaZoom = 1;
                }

                this.style.transform =
                    "scale(" + escalaZoom + ")";

            }
        );


        /*
         * Roda do mouse sobre a imagem:
         * permite ampliar/reduzir.
         */
        document.getElementById("imgAmpliada").addEventListener(
            "wheel",
            function(event) {

                event.preventDefault();
                event.stopPropagation();

                if (event.deltaY < 0) {
                    alterarZoom(0.15);
                } else {
                    alterarZoom(-0.15);
                }

            },
            { passive: false }
        );


        /*
         * ESC fecha a imagem.
         */
        document.addEventListener(
            "keydown",
            function(event) {

                if (event.key === "Escape") {
                    fecharZoom();
                }

            }
        );

    </script>

</body>
</html>
"""


@app.template_filter('from_json')
def from_json_filter(s):
    try:
        return json.loads(s)
    except Exception:
        return {}


@app.route('/ver_imagem')
def ver_imagem():
    caminho = request.args.get('caminho', '')

    if caminho and os.path.exists(caminho):
        return send_file(caminho)

    return "", 404


@app.route('/')
def index():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            codigo,
            nome,
            descricao,
            preco,
            estoque,
            foto_caminho,
            preco_custo,
            estoque_minimo,
            grupo,
            referencia,
            fornecedor,
            permitir_negativo,
            grade_json
        FROM produtos
        ORDER BY nome ASC
    """)

    produtos = cursor.fetchall()

    conn.close()

    return render_template_string(
        TEMPLATE_HTML,
        produtos=produtos
    )


@app.route('/enviar_pedido', methods=['POST'])
def enviar_pedido():

    nome = request.form.get('cliente_nome', 'Cliente')
    tel = request.form.get('cliente_tel', '')

    itens_pedido = []
    total_geral = 0.0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for chave, value in request.form.items():

        if chave.startswith('item_'):

            qtd = int(value) if value.isdigit() else 0

            if qtd > 0:

                partes = chave.split('_')

                prod_id = partes[1]
                tamanho = partes[2]

                cursor.execute(
                    "SELECT nome, preco FROM produtos WHERE id = ?",
                    (prod_id,)
                )

                p = cursor.fetchone()

                if p:

                    nome_prod, preco = p[0], p[1]

                    subtotal = qtd * preco
                    total_geral += subtotal

                    itens_pedido.append(
                        f"• {qtd}x {nome_prod} "
                        f"(Tam: {tamanho}) - R$ {subtotal:.2f}"
                        .replace('.', ',')
                    )

    conn.close()

    if not itens_pedido:

        return """
        <script>
            alert('Selecione pelo menos um item na grade!');
            window.history.back();
        </script>
        """

    msg = (
        f"Olá! Meu nome é *{nome}* "
        f"e gostaria de fechar este pedido:\\n\\n"
    )

    msg += "\\n".join(itens_pedido)

    msg += (
        f"\\n\\n*Valor Total:* "
        f"R$ {total_geral:.2f}".replace('.', ',')
    )

    msg += "\\nAguardando instruções de pagamento e entrega."

    link_zap = (
        f"https://api.whatsapp.com/send"
        f"?phone={WHATSAPP_LOJA}"
        f"&text={urllib.parse.quote(msg)}"
    )

    return redirect(link_zap)


if __name__ == '__main__':

    print(
        "Servidor do Catálogo Online rodando em "
        "http://127.0.0.1:5000"
    )

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
