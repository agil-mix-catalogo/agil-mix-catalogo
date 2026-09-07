# ============================================================
# app_catalogo_web.py
# ÁGIL MIX JEANS WEAR - CATÁLOGO ONLINE
# ============================================================

import json
import os
import re
import sqlite3
import urllib.parse

from datetime import datetime

from flask import (
    Flask,
    redirect,
    render_template_string,
    request,
    send_file,
    session,
    url_for,
    make_response,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

app = Flask(__name__)

app.secret_key = 'dalvan_secret_key_2026'


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DB_PATH = os.path.join(
    BASE_DIR,
    'dalvan.db'
)


PASTA_IMAGENS = os.path.join(
    BASE_DIR,
    'imagens'
)


PASTA_PRODUTOS = os.path.join(
    PASTA_IMAGENS,
    'produtos'
)


PASTA_MOSTRUARIOS = os.path.join(
    PASTA_IMAGENS,
    'mostruarios'
)


# ============================================================
# WHATSAPP
# ============================================================

WHATSAPP_LOJA = '5581996716172'


# ============================================================
# EXTENSÕES
# ============================================================

EXTENSOES_IMAGEM = (
    '.jpg',
    '.jpeg',
    '.png',
    '.webp',
    '.bmp',
    '.gif'
)


# ============================================================
# TEMPLATE HTML
# ============================================================

TEMPLATE_HTML = """

<!DOCTYPE html>

<html lang="pt-BR">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        Ágil Mix Jeans Wear - Catálogo Online
    </title>


    <style>

        * {
            box-sizing: border-box;
        }


        body {

            background-color: #172033;

            color: #E5E7EB;

            font-family:
                'Segoe UI',
                Tahoma,
                Geneva,
                Verdana,
                sans-serif;

            margin: 0;

            padding: 0;

        }


        /* ====================================================
           CABEÇALHO
           ==================================================== */

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


        /* ====================================================
           SLIDER
           ==================================================== */

        .slider-container {

            max-width: 900px;

            margin: 20px auto;

            position: relative;

            border-radius: 12px;

            overflow: hidden;

            box-shadow:
                0 4px 15px rgba(0,0,0,0.5);

            border: 1px solid #2E3F66;

            background-color: #1F2A44;

        }


        .slider-track {

            display: flex;

            width: 100%;

            transition:
                transform 0.5s ease-in-out;

        }


        .slide {

            min-width: 100%;

            width: 100%;

            position: relative;

            overflow: hidden;

        }


        .slide img {

            width: 100%;

            height: 350px;

            object-fit: cover;

            display: block;

            cursor: pointer;

            background-color: #0F172A;

        }


        .slide-legenda {

            position: absolute;

            bottom: 0;

            left: 0;

            right: 0;

            background:
                rgba(15, 23, 42, 0.85);

            color: #FACC15;

            padding: 12px;

            text-align: center;

            font-size: 15px;

            font-weight: bold;

            border-top: 1px solid #2E3F66;

        }


        .slider-btn {

            position: absolute;

            top: 50%;

            transform: translateY(-50%);

            background-color:
                rgba(15, 23, 42, 0.75);

            color: #FFF;

            border: none;

            width: 45px;

            height: 45px;

            cursor: pointer;

            font-size: 24px;

            border-radius: 50%;

            transition:
                background-color 0.2s,
                transform 0.2s;

            z-index: 10;

        }


        .slider-btn:hover {

            background-color: #2563EB;

            transform:
                translateY(-50%) scale(1.08);

        }


        .slider-prev {

            left: 15px;

        }


        .slider-next {

            right: 15px;

        }


        .slider-dots {

            text-align: center;

            padding: 10px;

            background: #1F2A44;

        }


        .dot {

            display: inline-block;

            height: 10px;

            width: 10px;

            margin: 0 4px;

            background-color: #475569;

            border-radius: 50%;

            cursor: pointer;

            transition:
                background-color 0.3s,
                transform 0.2s;

        }


        .dot:hover {

            transform: scale(1.2);

        }


        .dot.active {

            background-color: #FACC15;

            transform: scale(1.15);

        }


        /* ====================================================
           CONTAINER
           ==================================================== */

        .container {

            max-width: 900px;

            margin: 20px auto;

            padding: 10px;

        }


        /* ====================================================
           BUSCA
           ==================================================== */

        .search-container {

            background-color: #1F2A44;

            padding: 15px;

            border-radius: 12px;

            margin-bottom: 20px;

            border: 1px solid #2E3F66;

            display: flex;

            gap: 10px;

            flex-direction: column;

        }


        .search-row {

            display: flex;

            gap: 10px;

            width: 100%;

        }


        .search-container input {

            flex-grow: 1;

            padding: 10px 15px;

            border-radius: 6px;

            border: 1px solid #2E3F66;

            background-color: #0F172A;

            color: #FFF;

            font-size: 14px;

            outline: none;

        }


        .search-container input:focus {

            border-color: #2563EB;

        }


        .search-container button {

            background-color: #2563EB;

            color: #FFF;

            font-weight: bold;

            border: none;

            padding: 10px 20px;

            border-radius: 6px;

            cursor: pointer;

            font-size: 14px;

        }


        .search-container button:hover {

            background-color: #1d4ed8;

        }


        .btn-limpar {

            background-color: #475569 !important;

            text-decoration: none;

            display: flex;

            align-items: center;

            justify-content: center;

            padding: 10px 15px;

            border-radius: 6px;

            color: #FFF;

            font-weight: bold;

            font-size: 14px;

        }


        .btn-limpar:hover {

            background-color: #334155 !important;

        }


        .search-hint {

            font-size: 12px;

            color: #94A3B8;

            margin: 0;

        }


        /* ====================================================
           PRODUTO
           ==================================================== */

        .produto-card {

            background-color: #1F2A44;

            border-radius: 12px;

            padding: 15px;

            margin-bottom: 18px;

            display: flex;

            flex-direction: column;

            box-shadow:
                0 4px 6px rgba(0,0,0,0.3);

            border: 1px solid #2E3F66;

        }


        .prod-corpo {

            display: flex;

            gap: 20px;

            align-items: flex-start;

            flex-wrap: wrap;

        }


        .prod-fotos-container {

            display: flex;

            gap: 10px;

            flex-shrink: 0;

        }


        .prod-img-grande {

            width: 120px;

            height: 120px;

            background-color: #0F172A;

            border-radius: 10px;

            object-fit: cover;

            display: block;

            color: #94A3B8;

            font-size: 11px;

            text-align: center;

            border: 2px solid #2563EB;

            box-shadow:
                0 4px 10px rgba(0,0,0,0.5);

            cursor: pointer;

            transition:
                transform 0.2s;

            padding: 4px;

        }


        .prod-img-grande:hover {

            transform: scale(1.03);

        }


        .prod-detalhes {

            flex-grow: 1;

            display: flex;

            flex-direction: column;

            gap: 6px;

        }


        .prod-nome {

            font-size: 18px;

            font-weight: bold;

            color: #E5E7EB;

        }


        .prod-preco {

            font-size: 17px;

            color: #22C55E;

            font-weight: bold;

        }


        /* ====================================================
           SEM FOTO
           ==================================================== */

        .sem-foto {

            width: 120px;

            height: 120px;

            background-color: #0F172A;

            border-radius: 10px;

            display: flex;

            align-items: center;

            justify-content: center;

            color: #94A3B8;

            font-size: 12px;

            text-align: center;

            border: 2px solid #475569;

            padding: 10px;

        }


        /* ====================================================
           GRADE
           ==================================================== */

        .grade-container {

            margin-top: 15px;

            background-color: #0F172A;

            padding: 12px;

            border-radius: 8px;

            display: flex;

            flex-wrap: wrap;

            gap: 8px;

            align-items: center;

            justify-content: space-between;

            border: 1px solid #1E293B;

        }


        .tamanho-box {

            display: flex;

            flex-direction: column;

            align-items: center;

            background: #172033;

            padding: 6px 10px;

            border-radius: 6px;

            border: 1px solid #2E3F66;

        }


        .tamanho-box label {

            font-size: 12px;

            color: #FACC15;

            font-weight: bold;

            margin-bottom: 2px;

        }


        .tamanho-estoque {

            font-size: 10px;

            color: #38BDF8;

            margin-bottom: 4px;

            font-weight: bold;

        }


        .tamanho-box input {

            width: 48px;

            height: 32px;

            background-color: #1F2A44;

            border: 1px solid #2E3F66;

            color: #FFF;

            text-align: center;

            border-radius: 4px;

            font-size: 14px;

        }


        /* ====================================================
           CARRINHO
           ==================================================== */

        .carrinho-float {

            position: fixed;

            bottom: 0;

            left: 0;

            right: 0;

            background-color: #1F2A44;

            padding: 15px;

            border-top: 2px solid #2563EB;

            box-shadow:
                0 -4px 10px rgba(0,0,0,0.5);

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

            text-decoration: none;

        }


        .btn-enviar:hover {

            background-color: #16a34a;

        }


        /* ====================================================
           MODAL
           ==================================================== */

        #modalZoom {

            display: none;

            position: fixed;

            z-index: 9999;

            left: 0;

            top: 0;

            width: 100vw;

            height: 100vh;

            background-color:
                rgba(0,0,0,0.92);

            align-items: center;

            justify-content: center;

            padding: 20px;

        }


        .modal-conteudo {

            width: auto;

            max-width: 92vw;

            height: auto;

            max-height: 88vh;

            object-fit: contain;

            border-radius: 10px;

            background-color: #0F172A;

            border: 2px solid #2563EB;

            box-shadow:
                0 10px 40px rgba(0,0,0,0.7);

        }


        .fechar {

            position: fixed;

            top: 20px;

            right: 25px;

            color: #fff;

            font-size: 40px;

            font-weight: bold;

            cursor: pointer;

            z-index: 10000;

            background:
                rgba(0,0,0,0.7);

            width: 45px;

            height: 45px;

            border-radius: 50%;

            display: flex;

            align-items: center;

            justify-content: center;

            border: 1px solid #fff;

        }


        .fechar:hover {

            background-color: #2563EB;

        }


        /* ====================================================
           AVISO SEM MOSTRUÁRIO
           ==================================================== */

        .sem-mostruario {

            max-width: 900px;

            margin: 20px auto;

            padding: 20px;

            text-align: center;

            background: #1F2A44;

            border: 1px solid #2E3F66;

            border-radius: 12px;

            color: #94A3B8;

        }


        /* ====================================================
           RESPONSIVO
           ==================================================== */

        @media (max-width: 650px) {


            h1 {

                font-size: 20px;

            }


            .container {

                padding: 8px;

            }


            .search-row {

                flex-direction: column;

            }


            .search-row button,

            .btn-limpar {

                width: 100%;

            }


            .prod-corpo {

                flex-direction: column;

            }


            .prod-fotos-container {

                width: 100%;

                justify-content: center;

            }


            .prod-img-grande,

            .sem-foto {

                width: 150px;

                height: 150px;

            }


            .prod-detalhes {

                width: 100%;

            }


            .prod-nome {

                font-size: 16px;

            }


            .slider-container {

                margin: 10px;

            }


            .slide img {

                height: 280px;

            }


            .slider-btn {

                width: 38px;

                height: 38px;

                font-size: 20px;

            }


            .slider-prev {

                left: 8px;

            }


            .slider-next {

                right: 8px;

            }


            .form-cliente {

                flex-direction: column;

            }


        }

    </style>

</head>


<body>


    <!-- ====================================================
         CABEÇALHO
         ==================================================== -->

    <header>

        <h1>
            Ágil Mix Jeans Wear - Catálogo Online
        </h1>

        <p>
            Escolha a quantidade por tamanho e finalize direto pelo WhatsApp
        </p>

    </header>


    <!-- ====================================================
         SLIDER DE MOSTRUÁRIO
         ==================================================== -->

    {% if mostruarios %}

    <div
        class="slider-container"
        id="sliderContainer"
    >


        <button
            type="button"
            class="slider-btn slider-prev"
            onclick="mudarSlide(-1)"
            aria-label="Foto anterior"
        >
            &#10094;
        </button>


        <div
            class="slider-track"
            id="sliderTrack"
        >

            {% for img_nome in mostruarios %}

            <div class="slide">

                <img
                    src="{{ url_for(
                        'ver_mostruario',
                        nome=img_nome
                    ) }}"
                    alt="Mostruário Ágil Mix - {{ img_nome }}"
                    loading="{% if loop.first %}eager{% else %}lazy{% endif %}"
                    onclick="abrirZoom(this.src)"
                    onerror="fotoSliderErro(this)"
                >


                <div class="slide-legenda">

                    ✨ Ágil Mix Jeans Wear
                    —
                    Coleção em Destaque

                </div>

            </div>

            {% endfor %}

        </div>


        <button
            type="button"
            class="slider-btn slider-next"
            onclick="mudarSlide(1)"
            aria-label="Próxima foto"
        >
            &#10095;
        </button>


        <div
            class="slider-dots"
            id="sliderDots"
        >

            {% for img_nome in mostruarios %}

            <span
                class="dot {% if loop.first %}active{% endif %}"
                onclick="definirSlide({{ loop.index0 }})"
                aria-label="Ir para foto {{ loop.index }}"
            ></span>

            {% endfor %}

        </div>


    </div>


    {% else %}


    <div class="sem-mostruario">

        📸 Nenhuma foto do mostruário foi encontrada.

    </div>


    {% endif %}


    <!-- ====================================================
         CATÁLOGO
         ==================================================== -->

    <div
        class="container"
        style="margin-bottom: 140px;"
    >


        <!-- BUSCA -->

        <form
            method="GET"
            action="/"
            class="search-container"
        >


            <div class="search-row">


                <input
                    type="text"
                    name="busca"
                    value="{{ termo_busca }}"
                    placeholder="Ex: C640, CP7259, bermuda, calça..."
                >


                <button type="submit">

                    🔍 Buscar

                </button>


                {% if termo_busca %}

                <a
                    href="/"
                    class="btn-limpar"
                >

                    Limpar

                </a>

                {% endif %}


            </div>


            <p class="search-hint">

                💡 Dica: Você pode digitar várias referências ou termos de uma só vez.

            </p>


        </form>


        <!-- ==================================================
             FORMULÁRIO
             ================================================== -->

        <form
            action="/enviar_pedido"
            method="POST"
            id="formPedido"
        >


            {% for p in produtos %}


            <div class="produto-card">


                <div class="prod-corpo">


                    <!-- FOTO DO PRODUTO -->

                    <div class="prod-fotos-container">


                        {% if p[14] %}


                        <img
                            src="{{ url_for(
                                'ver_imagem_id',
                                prod_id=p[0]
                            ) }}"
                            class="prod-img-grande"
                            onclick="abrirZoom(
                                '{{ url_for(
                                    'ver_imagem_id',
                                    prod_id=p[0]
                                ) }}'
                            )"
                            title="Clique para ampliar"
                            alt="Foto de {{ p[1] }}"
                            onerror="fotoErro(this)"
                        >


                        {% else %}


                        <div class="sem-foto">

                            📷<br>

                            Sem Foto

                        </div>


                        {% endif %}


                    </div>


                    <!-- DADOS -->

                    <div class="prod-detalhes">


                        <div class="prod-nome">

                            {{ p[1] }}
                            -
                            {{ p[2] }}

                        </div>


                        <div class="prod-preco">

                            R$
                            {{ "%.2f"|format(p[4]) }}

                        </div>


                        <div
                            style="
                                font-size: 13px;
                                color: #94A3B8;
                            "
                        >

                            Grupo:
                            <b>{{ p[9] }}</b>

                            |

                            Ref:
                            <b>{{ p[10] }}</b>

                        </div>


                        <div
                            style="
                                font-size: 13px;
                                color: #38BDF8;
                            "
                        >

                            Estoque Total:
                            <b>{{ p[5] }}</b>
                            un

                        </div>


                        <div
                            style="
                                font-size: 11px;
                                color: #64748B;
                                margin-top: 4px;
                            "
                        >

                            📷 Foto:
                            {{ p[14] }}

                        </div>


                    </div>


                </div>


                <!-- ==================================================
                     GRADE
                     ================================================== -->

                {% set grade_dict = p[13]|from_json %}


                {% if grade_dict %}


                <div class="grade-container">


                    <span
                        style="
                            font-size: 12px;
                            color: #94A3B8;
                            width: 100%;
                            margin-bottom: 2px;
                        "
                    >

                        Quantidade por Tamanho:

                    </span>


                    {% for tam, qtd in grade_dict.items() %}


                    <div class="tamanho-box">


                        <label>

                            {{ tam }}

                        </label>


                        <span class="tamanho-estoque">

                            Disp: {{ qtd }}

                        </span>


                        <input
                            type="number"
                            name="item_{{ p[0] }}_{{ tam }}"
                            value="0"
                            min="0"
                            max="{{ qtd }}"
                        >


                    </div>


                    {% endfor %}


                </div>


                {% endif %}


            </div>


            {% endfor %}


            <!-- ==================================================
                 CARRINHO / WHATSAPP
                 ================================================== -->

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


                <button
                    type="submit"
                    class="btn-enviar"
                >

                    🚀 Enviar Pedido Pronto para o WhatsApp

                </button>


            </div>


        </form>


    </div>


    <!-- ====================================================
         MODAL DE ZOOM
         ==================================================== -->

    <div
        id="modalZoom"
        onclick="fecharZoom()"
    >


        <span
            class="fechar"
            onclick="event.stopPropagation(); fecharZoom();"
        >

            &times;

        </span>


        <img
            class="modal-conteudo"
            id="imgAmpliada"
            onclick="event.stopPropagation();"
            alt="Imagem ampliada"
        >


    </div>


    <!-- ====================================================
         JAVASCRIPT
         ==================================================== -->

    <script>


        /* ==================================================
           SLIDER
           ================================================== */


        let slideAtual = 0;


        const sliderTrack =
            document.getElementById(
                'sliderTrack'
            );


        const slides =
            document.querySelectorAll(
                '.slide'
            );


        const dots =
            document.querySelectorAll(
                '.dot'
            );


        const totalSlides =
            slides.length;


        let intervaloSlider = null;


        /* ==================================================
           MOSTRAR SLIDE
           ================================================== */

        function mostrarSlide(index) {


            if (
                !sliderTrack ||
                totalSlides === 0
            ) {

                return;

            }


            if (
                index >= totalSlides
            ) {

                slideAtual = 0;

            }

            else if (
                index < 0
            ) {

                slideAtual =
                    totalSlides - 1;

            }

            else {

                slideAtual = index;

            }


            sliderTrack.style.transform =
                'translateX(-' +
                (slideAtual * 100) +
                '%)';


            dots.forEach(
                function(dot) {

                    dot.classList.remove(
                        'active'
                    );

                }
            );


            if (
                dots[slideAtual]
            ) {

                dots[slideAtual]
                    .classList.add(
                        'active'
                    );

            }

        }


        /* ==================================================
           PRÓXIMO / ANTERIOR
           ================================================== */

        function mudarSlide(direcao) {


            mostrarSlide(
                slideAtual + direcao
            );


        }


        /* ==================================================
           FOTO ESPECÍFICA
           ================================================== */

        function definirSlide(index) {


            mostrarSlide(index);


            reiniciarSliderAutomatico();


        }


        /* ==================================================
           SLIDER AUTOMÁTICO
           ================================================== */

        function iniciarSliderAutomatico() {


            if (
                totalSlides <= 1
            ) {

                return;

            }


            if (
                intervaloSlider
            ) {

                clearInterval(
                    intervaloSlider
                );

            }


            intervaloSlider =
                setInterval(
                    function() {

                        mudarSlide(1);

                    },
                    8000
                );


        }


        function reiniciarSliderAutomatico() {


            if (
                intervaloSlider
            ) {

                clearInterval(
                    intervaloSlider
                );

            }


            iniciarSliderAutomatico();


        }


        iniciarSliderAutomatico();


        /* ==================================================
           PAUSAR QUANDO PASSAR O MOUSE
           ================================================== */

        const sliderContainer =
            document.getElementById(
                'sliderContainer'
            );


        if (
            sliderContainer
        ) {


            sliderContainer.addEventListener(
                'mouseenter',
                function() {

                    if (
                        intervaloSlider
                    ) {

                        clearInterval(
                            intervaloSlider
                        );

                    }

                }
            );


            sliderContainer.addEventListener(
                'mouseleave',
                function() {

                    iniciarSliderAutomatico();

                }
            );


        }


        /* ==================================================
           TOUCH / CELULAR
           ================================================== */

        let toqueInicialX = 0;

        let toqueFinalX = 0;


        if (
            sliderContainer
        ) {


            sliderContainer.addEventListener(
                'touchstart',
                function(event) {

                    toqueInicialX =
                        event.changedTouches[0].screenX;

                },
                {
                    passive: true
                }
            );


            sliderContainer.addEventListener(
                'touchend',
                function(event) {

                    toqueFinalX =
                        event.changedTouches[0].screenX;


                    const diferenca =
                        toqueFinalX -
                        toqueInicialX;


                    if (
                        Math.abs(diferenca) > 50
                    ) {


                        if (
                            diferenca < 0
                        ) {

                            mudarSlide(1);

                        }

                        else {

                            mudarSlide(-1);

                        }


                        reiniciarSliderAutomatico();

                    }

                },
                {
                    passive: true
                }
            );


        }


        /* ==================================================
           ZOOM
           ================================================== */

        function abrirZoom(src) {


            if (!src) {

                return;

            }


            const modal =
                document.getElementById(
                    'modalZoom'
                );


            const modalImg =
                document.getElementById(
                    'imgAmpliada'
                );


            modalImg.src = src;


            modal.style.display =
                'flex';


        }


        function fecharZoom() {


            const modal =
                document.getElementById(
                    'modalZoom'
                );


            const modalImg =
                document.getElementById(
                    'imgAmpliada'
                );


            modal.style.display =
                'none';


            modalImg.src = '';


        }


        /* ==================================================
           ERRO FOTO PRODUTO
           ================================================== */

        function fotoErro(img) {


            if (!img) {

                return;

            }


            const div =
                document.createElement(
                    'div'
                );


            div.className =
                'sem-foto';


            div.innerHTML =
                '📷<br>Foto não encontrada';


            if (
                img.parentNode
            ) {

                img.parentNode.replaceChild(
                    div,
                    img
                );

            }


        }


        /* ==================================================
           ERRO FOTO SLIDER
           ================================================== */

        function fotoSliderErro(img) {


            if (!img) {

                return;

            }


            const slide =
                img.parentElement;


            if (
                slide
            ) {

                slide.style.display =
                    'none';

            }


            console.warn(
                'Foto do mostruário não encontrada:',
                img.src
            );


        }


        /* ==================================================
           TECLA ESC
           ================================================== */

        document.addEventListener(
            'keydown',
            function(event) {


                if (
                    event.key === 'Escape'
                ) {

                    fecharZoom();

                }


                if (
                    event.key === 'ArrowLeft'
                ) {

                    if (
                        document.getElementById(
                            'modalZoom'
                        ).style.display !== 'flex'
                    ) {

                        mudarSlide(-1);

                        reiniciarSliderAutomatico();

                    }

                }


                if (
                    event.key === 'ArrowRight'
                ) {

                    if (
                        document.getElementById(
                            'modalZoom'
                        ).style.display !== 'flex'
                    ) {

                        mudarSlide(1);

                        reiniciarSliderAutomatico();

                    }

                }


            }
        );


        /* ==================================================
           INICIAR PRIMEIRO SLIDE
           ================================================== */

        mostrarSlide(0);


    </script>


</body>

</html>

"""


# ============================================================
# TEMPLATE DE SUCESSO
# ============================================================

TEMPLATE_SUCESSO = """

<!DOCTYPE html>

<html lang="pt-BR">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        Pedido Enviado - Ágil Mix Jeans Wear
    </title>


    <style>


        body {

            background-color: #172033;

            color: #E5E7EB;

            font-family:
                'Segoe UI',
                Tahoma,
                Geneva,
                Verdana,
                sans-serif;

            margin: 0;

            padding: 0;

            display: flex;

            align-items: center;

            justify-content: center;

            height: 100vh;

            text-align: center;

        }


        .card-sucesso {

            background-color: #1F2A44;

            padding: 40px;

            border-radius: 12px;

            border: 1px solid #2E3F66;

            box-shadow:
                0 4px 15px rgba(0,0,0,0.5);

            max-width: 450px;

            width: 90%;

        }


        h1 {

            color: #FACC15;

            font-size: 22px;

            margin-bottom: 10px;

        }


        p {

            color: #94A3B8;

            font-size: 15px;

            margin-bottom: 25px;

        }


        .btn-zap {

            background-color: #22C55E;

            color: #000;

            font-weight: bold;

            border: none;

            padding: 14px 20px;

            border-radius: 6px;

            font-size: 16px;

            cursor: pointer;

            text-decoration: none;

            display: inline-block;

            width: 100%;

            box-sizing: border-box;

            margin-bottom: 15px;

        }


        .btn-voltar {

            background-color: #0F172A;

            color: #38BDF8;

            font-weight: bold;

            border: 1px solid #2E3F66;

            padding: 12px 20px;

            border-radius: 6px;

            font-size: 14px;

            text-decoration: none;

            display: inline-block;

            width: 100%;

            box-sizing: border-box;

        }


    </style>

</head>


<body>


    <div class="card-sucesso">


        <h1>

            Pedido Registrado com Sucesso! 🎉

        </h1>


        <p>

            O estoque foi atualizado e seu pedido foi montado.
            Clique abaixo para enviar para o WhatsApp da loja.

        </p>


        {% if disponivel and link_zap %}


        <button
            id="btnZap"
            class="btn-zap"
            onclick="executarWhatsApp()"
        >

            💬 Enviar Pedido para o WhatsApp

        </button>


        {% endif %}


        <a
            href="{{ url_for('index') }}"
            id="btnVoltar"
            class="btn-voltar"
        >

            🔄 Voltar ao Catálogo

        </a>


    </div>


    <script>


        const link_zap_raw =
            "{{ link_zap|safe if link_zap else '' }}";


        function executarWhatsApp() {


            if (!link_zap_raw) {

                return;

            }


            fetch(
                '/consumir_pedido',
                {
                    method: 'POST'
                }
            );


            setTimeout(
                function() {

                    window.open(
                        link_zap_raw,
                        '_blank'
                    );

                },
                300
            );


        }


    </script>


</body>

</html>

"""


# ============================================================
# FILTRO JSON
# ============================================================

@app.template_filter('from_json')
def from_json_filter(s):


    if not s:

        return {}


    if isinstance(
        s,
        dict
    ):

        return s


    try:

        return json.loads(s)

    except Exception:

        return {}


# ============================================================
# LISTAR FOTOS DOS PRODUTOS
# ============================================================

def listar_fotos_numeradas():


    fotos = {}


    if not os.path.isdir(
        PASTA_PRODUTOS
    ):

        print()

        print(
            '[FOTOS] ERRO: pasta não encontrada:'
        )

        print(
            PASTA_PRODUTOS
        )

        return fotos


    try:

        arquivos =
            os.listdir(
                PASTA_PRODUTOS
            )

    except Exception as erro:

        print(
            f'[FOTOS] Erro lendo pasta: {erro}'
        )

        return fotos


    for arquivo in arquivos:


        nome_base, extensao = os.path.splitext(
            arquivo
        )


        if (
            not extensao
            or
            extensao.lower()
            not in EXTENSOES_IMAGEM
        ):

            continue


        if not nome_base.isdigit():

            continue


        numero = int(
            nome_base
        )


        caminho = os.path.join(
            PASTA_PRODUTOS,
            arquivo
        )


        if os.path.isfile(
            caminho
        ):

            fotos[numero] = caminho


    print()

    print(
        '[FOTOS] Fotos numeradas encontradas:'
    )


    for numero in sorted(
        fotos
    ):

        print(
            f'   {numero} -> '
            f'{os.path.basename(fotos[numero])}'
        )


    return fotos


# ============================================================
# LISTAR FOTOS DO MOSTRUÁRIO
# ============================================================

def listar_mostruarios():


    mostruarios = []


    print()

    print(
        '=' * 70
    )

    print(
        '[SLIDER] PROCURANDO FOTOS DO MOSTRUÁRIO'
    )

    print(
        '=' * 70
    )

    print(
        '[SLIDER] Pasta:'
    )

    print(
        PASTA_MOSTRUARIOS
    )


    if not os.path.isdir(
        PASTA_MOSTRUARIOS
    ):

        print()

        print(
            '[SLIDER] ERRO: pasta não encontrada!'
        )

        print(
            PASTA_MOSTRUARIOS
        )

        print(
            '=' * 70
        )

        return mostruarios


    try:

        arquivos = os.listdir(
            PASTA_MOSTRUARIOS
        )


        for arquivo in arquivos:


            caminho = os.path.join(
                PASTA_MOSTRUARIOS,
                arquivo
            )


            if not os.path.isfile(
                caminho
            ):

                continue


            extensao = os.path.splitext(
                arquivo
            )[1].lower()


            if (
                extensao
                in
                EXTENSOES_IMAGEM
            ):

                mostruarios.append(
                    arquivo
                )


    except Exception as erro:

        print(
            f'[SLIDER] ERRO ao ler pasta: {erro}'
        )

        return mostruarios


    # ========================================================
    # ORDENAÇÃO NATURAL
    # ========================================================

    def ordem_natural(nome):

        partes = re.split(
            r'(\\d+)',
            nome
        )


        resultado = []


        for parte in partes:


            if parte.isdigit():

                resultado.append(
                    int(parte)
                )

            else:

                resultado.append(
                    parte.lower()
                )


        return resultado


    mostruarios.sort(
        key=ordem_natural
    )


    print()

    print(
        f'[SLIDER] '
        f'{len(mostruarios)} foto(s) encontrada(s).'
    )


    for i, foto in enumerate(
        mostruarios,
        start=1
    ):

        print(
            f'   {i} -> {foto}'
        )


    print(
        '=' * 70
    )


    return mostruarios


# ============================================================
# DESCOBRIR FOTO DO PRODUTO
# ============================================================

def obter_numero_foto_produto(
    prod_id
):


    conn = None


    try:


        conn = sqlite3.connect(
            DB_PATH,
            timeout=10.0
        )


        cursor = conn.cursor()


        cursor.execute(
            '''
            SELECT id
            FROM produtos
            WHERE grupo LIKE ?
            ORDER BY nome ASC, id ASC
            ''',
            (
                '%confec%',
            )
        )


        produtos_ids = [

            linha[0]

            for linha
            in cursor.fetchall()

        ]


    except Exception as erro:


        print(
            '[FOTOS] '
            f'Erro obtendo ordem: {erro}'
        )


        return None


    finally:


        if conn:

            conn.close()


    try:


        posicao =
            produtos_ids.index(
                prod_id
            )


    except ValueError:


        print(
            f'[FOTOS] Produto ID '
            f'{prod_id} não encontrado.'
        )


        return None


    return posicao + 1


# ============================================================
# SERVIR FOTO DO PRODUTO
# ============================================================

@app.route(
    '/ver_imagem_id/<int:prod_id>'
)
def ver_imagem_id(
    prod_id
):


    print()

    print(
        f'[FOTO] Produto solicitado: '
        f'{prod_id}'
    )


    numero_foto =
        obter_numero_foto_produto(
            prod_id
        )


    if numero_foto is None:

        return '', 404


    fotos =
        listar_fotos_numeradas()


    caminho =
        fotos.get(
            numero_foto
        )


    if (
        caminho
        and
        os.path.isfile(caminho)
    ):


        print(
            f'[FOTO] Produto {prod_id} '
            f'-> foto {numero_foto} '
            f'-> {os.path.basename(caminho)}'
        )


        try:


            resposta =
                make_response(
                    send_file(caminho)
                )


            resposta.headers[
                'Cache-Control'
            ] = (
                'no-store, no-cache, '
                'must-revalidate, max-age=0'
            )


            return resposta


        except Exception as erro:


            print(
                f'[FOTO] Erro enviando foto: '
                f'{erro}'
            )


            return '', 500


    print(
        f'[FOTO] Foto {numero_foto} '
        f'não encontrada.'
    )


    return '', 404


# ============================================================
# SERVIR FOTO DO MOSTRUÁRIO
# ============================================================

@app.route(
    '/ver_mostruario/<path:nome>'
)
def ver_mostruario(
    nome
):


    # Segurança:
    # impede que seja utilizado caminho externo.

    nome = os.path.basename(
        nome
    )


    caminho =
        os.path.join(
            PASTA_MOSTRUARIOS,
            nome
        )


    if (
        os.path.isfile(caminho)
    ):


        try:


            resposta =
                make_response(
                    send_file(caminho)
                )


            resposta.headers[
                'Cache-Control'
            ] = (
                'no-store, no-cache, '
                'must-revalidate, max-age=0'
            )


            return resposta


        except Exception as erro:


            print(
                f'[SLIDER] Erro enviando '
                f'{nome}: {erro}'
            )


            return '', 500


    print(
        f'[SLIDER] Arquivo não encontrado: '
        f'{caminho}'
    )


    return '', 404


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route('/')
def index():


    termo_busca =
        request.args.get(
            'busca',
            ''
        ).strip()


    # ========================================================
    # MOSTRUÁRIOS
    # ========================================================

    mostruarios =
        listar_mostruarios()


    # ========================================================
    # BANCO
    # ========================================================

    conn =
        sqlite3.connect(
            DB_PATH,
            timeout=10.0
        )


    conn.execute(
        'PRAGMA journal_mode=WAL;'
    )


    cursor =
        conn.cursor()


    try:


        # ====================================================
        # BUSCA
        # ====================================================

        if termo_busca:


            palavras =
                termo_busca.split()


            condicoes = []


            parametros = [
                '%confec%'
            ]


            for palavra in palavras:


                condicoes.append(
                    '''
                    (
                        referencia LIKE ?
                        OR nome LIKE ?
                        OR codigo LIKE ?
                        OR descricao LIKE ?
                    )
                    '''
                )


                p_like =
                    f'%{palavra}%'


                parametros.extend(
                    [
                        p_like,
                        p_like,
                        p_like,
                        p_like
                    ]
                )


            sql_where =
                'WHERE grupo LIKE ? AND ('
                +
                ' OR '.join(
                    condicoes
                )
                +
                ')'


            query = f'''
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
                {sql_where}
                ORDER BY nome ASC, id ASC
            '''


            cursor.execute(
                query,
                parametros
            )


        # ====================================================
        # TODOS
        # ====================================================

        else:


            query = '''
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
                WHERE grupo LIKE ?
                ORDER BY nome ASC, id ASC
            '''


            cursor.execute(
                query,
                (
                    '%confec%',
                )
            )


        produtos_originais =
            cursor.fetchall()


    finally:

        conn.close()


    # ========================================================
    # MAPA GLOBAL DAS FOTOS
    #
    # MUITO IMPORTANTE:
    #
    # A ordem é calculada com TODOS os produtos,
    # antes da busca.
    #
    # Portanto:
    #
    # Produto 1 -> 1.jpg
    # Produto 2 -> 2.jpg
    # Produto 3 -> 3.jpg
    #
    # Uma pesquisa não altera essa associação.
    # ========================================================

    conn =
        sqlite3.connect(
            DB_PATH,
            timeout=10.0
        )


    cursor =
        conn.cursor()


    try:


        cursor.execute(
            '''
            SELECT id
            FROM produtos
            WHERE grupo LIKE ?
            ORDER BY nome ASC, id ASC
            ''',
            (
                '%confec%',
            )
        )


        ids_ordem = [

            linha[0]

            for linha
            in cursor.fetchall()

        ]


    finally:

        conn.close()


    mapa_fotos = {}


    for indice, id_produto in enumerate(
        ids_ordem,
        start=1
    ):


        mapa_fotos[
            id_produto
        ] = indice


    # ========================================================
    # FOTOS EXISTENTES
    # ========================================================

    fotos_existentes =
        listar_fotos_numeradas()


    # ========================================================
    # ADICIONAR FOTO AO PRODUTO
    # ========================================================

    produtos = []


    for produto
    in produtos_originais:


        prod_id =
            produto[0]


        numero_foto =
            mapa_fotos.get(
                prod_id
            )


        if (
            numero_foto
            in
            fotos_existentes
        ):

            numero_foto_final =
                numero_foto

        else:

            numero_foto_final =
                None


        produto_novo =
            produto + (
                numero_foto_final,
            )


        produtos.append(
            produto_novo
        )


        print(
            f'[CATALOGO] '
            f'ID={prod_id} '
            f'posição={numero_foto} '
            f'foto={numero_foto_final}'
        )


    # ========================================================
    # RENDERIZAR
    # ========================================================

    return render_template_string(

        TEMPLATE_HTML,

        produtos=produtos,

        mostruarios=mostruarios,

        termo_busca=termo_busca

    )


# ============================================================
# ENVIAR PEDIDO
# ============================================================

@app.route(
    '/enviar_pedido',
    methods=['POST']
)
def enviar_pedido():


    nome =
        request.form.get(
            'cliente_nome',
            'Cliente'
        )


    tel =
        request.form.get(
            'cliente_tel',
            ''
        )


    itens_pedido = []


    total_geral = 0.0


    conn =
        sqlite3.connect(
            DB_PATH,
            timeout=10.0
        )


    conn.execute(
        'PRAGMA journal_mode=WAL;'
    )


    cursor =
        conn.cursor()


    try:


        # ====================================================
        # CONTAS A RECEBER
        # ====================================================

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS contas_receber (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                cliente TEXT NOT NULL,

                telefone TEXT,

                valor REAL NOT NULL,

                data TEXT NOT NULL,

                status TEXT DEFAULT 'PENDENTE'

            )
            '''
        )


        # ====================================================
        # ITENS
        # ====================================================

        for chave, value
        in request.form.items():


            if not chave.startswith(
                'item_'
            ):

                continue


            qtd =
                int(value)
                if value.isdigit()
                else 0


            if qtd <= 0:

                continue


            partes =
                chave.split('_')


            if len(partes) < 3:

                continue


            prod_id =
                partes[1]


            tamanho =
                '_'.join(
                    partes[2:]
                )


            cursor.execute(
                '''
                SELECT
                    nome,
                    preco,
                    estoque,
                    grade_json,
                    referencia
                FROM produtos
                WHERE id = ?
                ''',
                (
                    prod_id,
                )
            )


            p =
                cursor.fetchone()


            if not p:

                continue


            (
                nome_prod,
                preco,
                estoque_geral,
                grade_json_str,
                referencia
            ) = p


            subtotal =
                qtd * preco


            total_geral += subtotal


            ref_texto = (

                f' (Ref: {referencia})'

                if referencia

                else ''

            )


            itens_pedido.append(

                f'• {qtd}x '
                f'{nome_prod}'
                f'{ref_texto} '
                f'(Tam: {tamanho}) '
                f'- R$ '
                f'{subtotal:.2f}'
                .replace(
                    '.',
                    ','
                )

            )


            # ================================================
            # GRADE
            # ================================================

            try:


                grade_dict = (

                    json.loads(
                        grade_json_str
                    )

                    if grade_json_str

                    else {}

                )


            except Exception:


                grade_dict = {}


            atual_tam =
                float(
                    grade_dict.get(
                        tamanho,
                        0.0
                    )
                )


            novo_tam =
                max(
                    0.0,
                    atual_tam - qtd
                )


            grade_dict[
                tamanho
            ] = (

                int(novo_tam)

                if novo_tam.is_integer()

                else novo_tam

            )


            # ================================================
            # ESTOQUE
            # ================================================

            novo_est_geral =
                max(
                    0.0,
                    float(
                        estoque_geral or 0
                    ) - qtd
                )


            cursor.execute(
                '''
                UPDATE produtos

                SET
                    estoque = ?,
                    grade_json = ?

                WHERE id = ?
                ''',
                (
                    novo_est_geral,

                    json.dumps(
                        grade_dict,
                        ensure_ascii=False
                    ),

                    prod_id
                )
            )


        # ====================================================
        # NENHUM ITEM
        # ====================================================

        if not itens_pedido:


            return (

                "<script>"
                "alert("
                "'Selecione pelo menos um item na grade!'"
                ");"
                "window.history.back();"
                "</script>"

            )


        # ====================================================
        # REGISTRA CONTA
        # ====================================================

        data_atual =
            datetime.now().strftime(
                '%d/%m/%Y %H:%M'
            )


        cursor.execute(
            '''
            INSERT INTO contas_receber
            (
                cliente,
                telefone,
                valor,
                data,
                status
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                'PENDENTE'
            )
            ''',
            (
                nome,
                tel,
                total_geral,
                data_atual
            )
        )


        conn.commit()


    finally:

        conn.close()


    # ========================================================
    # MENSAGEM WHATSAPP
    # ========================================================

    msg = (

        f'Olá! Meu nome é *{nome}* '
        f'(WhatsApp: {tel}) '
        f'e gostaria de fechar este pedido:\n\n'

        +

        '\n'.join(
            itens_pedido
        )

        +

        f'\n\n*Valor Total:* '
        f'R$ {total_geral:.2f}'
        .replace(
            '.',
            ','
        )

        +

        '\nAguardando instruções '
        'de pagamento e entrega.'

    )


    link_zap = (

        'https://web.whatsapp.com/send'
        f'?phone={WHATSAPP_LOJA}'
        f'&text='
        f'{urllib.parse.quote(msg)}'

    )


    session[
        'link_zap'
    ] = link_zap


    session[
        'disponivel'
    ] = True


    return redirect(
        url_for(
            'sucesso'
        )
    )


# ============================================================
# SUCESSO
# ============================================================

@app.route(
    '/sucesso'
)
def sucesso():


    return render_template_string(

        TEMPLATE_SUCESSO,

        link_zap=session.get(
            'link_zap',
            ''
        ),

        disponivel=session.get(
            'disponivel',
            False
        )

    )


# ============================================================
# CONSUMIR PEDIDO
# ============================================================

@app.route(
    '/consumir_pedido',
    methods=['POST']
)
def consumir_pedido():


    session[
        'disponivel'
    ] = False


    session[
        'link_zap'
    ] = ''


    return '', 204


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == '__main__':


    print()

    print(
        '=' * 70
    )


    print(
        '       ÁGIL MIX JEANS WEAR - CATÁLOGO ONLINE'
    )


    print(
        '=' * 70
    )


    print()

    print(
        'BASE DO PROGRAMA:'
    )

    print(
        BASE_DIR
    )


    print()

    print(
        'BANCO DE DADOS:'
    )

    print(
        DB_PATH
    )


    print()

    print(
        'PASTA DE PRODUTOS:'
    )

    print(
        PASTA_PRODUTOS
    )


    print()

    print(
        'PASTA DE MOSTRUÁRIOS:'
    )

    print(
        PASTA_MOSTRUARIOS
    )


    print()


    if os.path.isfile(
        DB_PATH
    ):

        print(
            '[OK] Banco de dados encontrado.'
        )

    else:

        print(
            '[ERRO] Banco de dados NÃO encontrado!'
        )


    if os.path.isdir(
        PASTA_PRODUTOS
    ):

        fotos =
            listar_fotos_numeradas()


        print(
            '[OK] Pasta de produtos encontrada.'
        )


        print(
            f'[OK] {len(fotos)} fotos de produtos encontradas.'
        )

    else:

        print(
            '[ERRO] Pasta de produtos NÃO encontrada!'
        )


    if os.path.isdir(
        PASTA_MOSTRUARIOS
    ):

        mostruarios =
            listar_mostruarios()


        print(
            '[OK] Pasta de mostruários encontrada.'
        )


        print(
            f'[OK] {len(mostruarios)} fotos de mostruário encontradas.'
        )

    else:

        print(
            '[ERRO] Pasta de mostruários NÃO encontrada!'
        )


    print()

    print(
        'Servidor iniciando em:'
    )


    print(
        'http://localhost:5000'
    )


    print()

    print(
        '=' * 70
    )


    print()


    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )