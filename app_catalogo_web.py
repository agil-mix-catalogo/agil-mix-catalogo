# app_catalogo_web.py
import json
import os
import sqlite3
from datetime import datetime
from flask import (
    Flask,
    redirect,
    render_template_string,
    request,
    send_file,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = 'dalvan_secret_key_2026'
DB_PATH = 'dalvan.db'

# >>> WHATSAPP DA EMPRESA <<<
WHATSAPP_LOJA = '5581996716172'

# Caminho da pasta de mostruários conforme a imagem
PASTA_MOSTRUARIOS = r'C:\Agil Mix\imagens\mostruarios'

TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ágil Mix Jeans Wear - Catálogo Online</title>
    <style>
        body { background-color: #172033; color: #E5E7EB; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
        header { background-color: #1F2A44; padding: 20px; text-align: center; border-bottom: 2px solid #2563EB; }
        h1 { margin: 0; color: #FACC15; font-size: 24px; }
        p { color: #94A3B8; font-size: 14px; margin: 5px 0 0 0; }
        
        /* Estilos do Slider de Mostruário */
        .slider-container { max-width: 900px; margin: 20px auto; position: relative; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #2E3F66; background-color: #1F2A44; }
        .slider-track { display: flex; transition: transform 0.5s ease-in-out; }
        .slide { min-width: 100%; box-sizing: border-box; position: relative; }
        .slide img { width: 100%; height: 350px; object-fit: cover; display: block; }
        .slide-legenda { position: absolute; bottom: 0; left: 0; right: 0; background: rgba(15, 23, 42, 0.85); color: #FACC15; padding: 10px; text-align: center; font-size: 15px; font-weight: bold; border-top: 1px solid #2E3F66; }
        
        .slider-btn { position: absolute; top: 50%; transform: translateY(-50%); background-color: rgba(15, 23, 42, 0.7); color: #FFF; border: none; padding: 12px; cursor: pointer; font-size: 18px; border-radius: 50%; transition: background 0.2s; z-index: 10; }
        .slider-btn:hover { background-color: #2563EB; }
        .slider-prev { left: 15px; }
        .slider-next { right: 15px; }
        
        .slider-dots { text-align: center; padding: 10px; background: #1F2A44; }
        .dot { display: inline-block; height: 10px; width: 10px; margin: 0 4px; background-color: #475569; border-radius: 50%; cursor: pointer; transition: background 0.3s; }
        .dot.active { background-color: #FACC15; }

        .container { max-width: 900px; margin: 20px auto; padding: 10px; }
        
        /* Estilos para a Barra de Pesquisa Múltipla */
        .search-container { background-color: #1F2A44; padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #2E3F66; display: flex; gap: 10px; flex-direction: column; }
        .search-row { display: flex; gap: 10px; width: 100%; }
        .search-container input { flex-grow: 1; padding: 10px 15px; border-radius: 6px; border: 1px solid #2E3F66; background-color: #0F172A; color: #FFF; font-size: 14px; outline: none; }
        .search-container button { background-color: #2563EB; color: #FFF; font-weight: bold; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 14px; }
        .search-container button:hover { background-color: #1d4ed8; }
        .btn-limpar { background-color: #475569 !important; text-decoration: none; display: flex; align-items: center; justify-content: center; padding: 10px 15px; border-radius: 6px; color: #FFF; font-weight: bold; font-size: 14px; }
        .btn-limpar:hover { background-color: #334155 !important; }
        .search-hint { font-size: 12px; color: #94A3B8; margin: 0; }

        .produto-card { background-color: #1F2A44; border-radius: 12px; padding: 15px; margin-bottom: 18px; display: flex; flex-direction: column; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 1px solid #2E3F66; }
        .prod-corpo { display: flex; gap: 20px; align-items: flex-start; flex-wrap: wrap; }
        
        .prod-fotos-container { display: flex; gap: 10px; flex-shrink: 0; }
        .prod-img-grande { width: 120px; height: 120px; background-color: #0F172A; border-radius: 10px; object-fit: cover; display: flex; align-items: center; justify-content: center; color: #94A3B8; font-size: 12px; text-align: center; border: 2px solid #2563EB; box-shadow: 0 4px 10px rgba(0,0,0,0.5); cursor: pointer; transition: transform 0.2s; }
        .prod-img-grande:hover { transform: scale(1.02); }
        
        .prod-detalhes { flex-grow: 1; display: flex; flex-direction: column; gap: 6px; }
        .prod-nome { font-size: 18px; font-weight: bold; color: #E5E7EB; }
        .prod-preco { font-size: 17px; color: #22C55E; font-weight: bold; }
        
        .grade-container { margin-top: 15px; background-color: #0F172A; padding: 12px; border-radius: 8px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: space-between; border: 1px solid #1E293B; }
        .tamanho-box { display: flex; flex-direction: column; align-items: center; background: #172033; padding: 6px 10px; border-radius: 6px; border: 1px solid #2E3F66; }
        .tamanho-box label { font-size: 12px; color: #FACC15; font-weight: bold; margin-bottom: 2px; }
        .tamanho-estoque { font-size: 10px; color: #38BDF8; margin-bottom: 4px; font-weight: bold; }
        .tamanho-box input { width: 48px; height: 32px; background-color: #1F2A44; border: 1px solid #2E3F66; color: #FFF; text-align: center; border-radius: 4px; font-size: 14px; }
        
        .carrinho-float { position: fixed; bottom: 0; left: 0; right: 0; background-color: #1F2A44; padding: 15px; border-top: 2px solid #2563EB; box-shadow: 0 -4px 10px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 10px; z-index: 100; }
        .form-cliente { display: flex; gap: 10px; flex-wrap: wrap; }
        .form-cliente input { flex-grow: 1; padding: 10px; border-radius: 6px; border: none; background-color: #0F172A; color: #FFF; font-size: 14px; }
        .btn-enviar { background-color: #22C55E; color: #000; font-weight: bold; border: none; padding: 12px; border-radius: 6px; font-size: 15px; cursor: pointer; text-align: center; width: 100%; text-decoration: none; }
        .btn-enviar:hover { background-color: #16a34a; }

        #modalZoom { display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100vw; height: 100vh; background-color: rgba(0,0,0,0.92); align-items: center; justify-content: center; }
        .modal-conteudo { width: 90vw; max-width: 500px; height: auto; max-height: 75vh; object-fit: contain; border-radius: 10px; background-color: #0F172A; border: 2px solid #2563EB; }
        .fechar { position: fixed; top: 20px; right: 25px; color: #fff; font-size: 40px; font-weight: bold; cursor: pointer; z-index: 10000; background: rgba(0,0,0,0.7); width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid #fff; }
    </style>
</head>
<body>
    <header>
        <h1>Ágil Mix Jeans Wear - Catálogo Online</h1>
        <p>Escolha a quantidade por tamanho e finalize direto pelo WhatsApp</p>
    </header>

    <!-- Slider / Mostruário Dinâmico -->
    {% if mostruarios %}
    <div class="slider-container">
        <button class="slider-btn slider-prev" onclick="mudarSlide(-1)">&#10094;</button>
        <button class="slider-btn slider-next" onclick="mudarSlide(1)">&#10095;</button>
        
        <div class="slider-track" id="sliderTrack">
            {% for img_nome in mostruarios %}
            <div class="slide">
                <img src="{{ url_for('ver_mostruario', nome=img_nome) }}" alt="Mostruário">
                <div class="slide-legenda">✨ Ágil Mix Jeans Wear - Coleção em Destaque</div>
            </div>
            {% endfor %}
        </div>

        <div class="slider-dots" id="sliderDots">
            {% for img_nome in mostruarios %}
            <span class="dot {% if loop.first %}active{% endif %}" onclick="definirSlide({{ loop.index0 }})"></span>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    <div class="container" style="margin-bottom: 140px;">
        <!-- Barra de Pesquisa Múltipla por Referência / Nome / Código -->
        <form method="GET" action="/" class="search-container">
            <div class="search-row">
                <input type="text" name="busca" value="{{ termo_busca }}" placeholder="Ex: C640, CP7259, bermuda, calça (separe por espaços para buscar vários)...">
                <button type="submit">🔍 Buscar</button>
                {% if termo_busca %}
                <a href="/" class="btn-limpar">Limpar</a>
                {% endif %}
            </div>
            <p class="search-hint">💡 Dica: Você pode digitar várias referências ou termos de uma só vez (ex: <i>C640 CP7259 calça</i>).</p>
        </form>

        <form action="/enviar_pedido" method="POST" id="formPedido">
            {% for p in produtos %}
            <div class="produto-card">
                <div class="prod-corpo">
                    <div class="prod-fotos-container">
                        {% if p[6] and p[6] != '' %}
                        <img src="{{ url_for('ver_imagem', caminho=p[6]) }}" class="prod-img-grande" onclick="abrirZoom('{{ url_for('ver_imagem', caminho=p[6]) }}')" onerror="this.style.display='none'" title="Frente (Ampliar)">
                        {% else %}
                        <div class="prod-img-grande">Sem Foto</div>
                        {% endif %}

                        {% if p[14] is defined and p[14] and p[14] != '' %}
                        <img src="{{ url_for('ver_imagem', caminho=p[14]) }}" class="prod-img-grande" onclick="abrirZoom('{{ url_for('ver_imagem', caminho=p[14]) }}')" onerror="this.style.display='none'" title="Costas (Ampliar)">
                        {% endif %}
                    </div>

                    <div class="prod-detalhes">
                        <div class="prod-nome">{{ p[1] }} - {{ p[2] }}</div>
                        <div class="prod-preco">R$ {{ "%.2f"|format(p[4]) }}</div>
                        <div style="font-size: 13px; color: #94A3B8;">Grupo: <b>{{ p[9] }}</b> | Ref: <b>{{ p[10] }}</b></div>
                        <div style="font-size: 13px; color: #38BDF8;">Estoque Total: <b>{{ p[5] }}</b> un</div>
                    </div>
                </div>

                {% set grade_dict = p[13]|from_json %}
                {% if grade_dict %}
                <div class="grade-container">
                    <span style="font-size: 12px; color: #94A3B8; width: 100%; margin-bottom: 2px;">Quantidade por Tamanho:</span>
                    {% for tam, qtd in grade_dict.items() %}
                    <div class="tamanho-box">
                        <label>{{ tam }}</label>
                        <span class="tamanho-estoque">Disp: {{ qtd }}</span>
                        <input type="number" name="item_{{ p[0] }}_{{ tam }}" value="0" min="0" max="{{ qtd }}">
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
            {% endfor %}

            <div class="carrinho-float">
                <div class="form-cliente">
                    <input type="text" name="cliente_nome" placeholder="Seu Nome Completo" required>
                    <input type="tel" name="cliente_tel" placeholder="Seu WhatsApp (com DDD)" required>
                </div>
                <button type="submit" class="btn-enviar">🚀 Enviar Pedido Pronto para o WhatsApp</button>
            </div>
        </form>
    </div>

    <div id="modalZoom" onclick="fecharZoom()">
        <span class="fechar">&times;</span>
        <img class="modal-conteudo" id="imgAmpliada">
    </div>

    <script>
        let slideAtual = 0;
        const slides = document.querySelectorAll('.slide');
        const dots = document.querySelectorAll('.dot');
        const totalSlides = slides.length;

        function mostrarSlide(index) {
            if (totalSlides === 0) return;
            if (index >= totalSlides) slideAtual = 0;
            else if (index < 0) slideAtual = totalSlides - 1;
            else slideAtual = index;

            const track = document.getElementById('sliderTrack');
            if(track) {
                track.style.transform = 'translateX(' + (-slideAtual * 100) + '%)';
            }

            dots.forEach(dot => dot.classList.remove('active'));
            if(dots[slideAtual]) {
                dots[slideAtual].classList.add('active');
            }
        }

        function mudarSlide(direcao) {
            mostrarSlide(slideAtual + direcao);
        }

        function definirSlide(index) {
            mostrarSlide(index);
        }

        if (totalSlides > 1) {
            setInterval(function() {
                mudarSlide(1);
            }, 4000);
        }

        function abrirZoom(src) {
            var modal = document.getElementById("modalZoom");
            var modalImg = document.getElementById("imgAmpliada");
            modal.style.display = "flex";
            modalImg.src = src;
        }
        function fecharZoom() {
            document.getElementById("modalZoom").style.display = "none";
        }
    </script>
</body>
</html>
"""

TEMPLATE_SUCESSO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pedido Enviado - Ágil Mix Jeans Wear</title>
    <style>
        body { background-color: #172033; color: #E5E7EB; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center; }
        .card-sucesso { background-color: #1F2A44; padding: 40px; border-radius: 12px; border: 1px solid #2E3F66; box-shadow: 0 4px 15px rgba(0,0,0,0.5); max-width: 450px; width: 90%; }
        h1 { color: #FACC15; font-size: 22px; margin-bottom: 10px; }
        p { color: #94A3B8; font-size: 15px; margin-bottom: 25px; }
        
        .btn-zap { background-color: #22C55E; color: #000; font-weight: bold; border: none; padding: 14px 20px; border-radius: 6px; font-size: 16px; cursor: pointer; text-decoration: none; display: inline-block; width: 100%; box-sizing: border-box; margin-bottom: 15px; transition: all 0.3s; }
        .btn-zap:hover { background-color: #16a34a; }
        .btn-zap.clicado { background-color: #15803d !important; color: #cbd5e1 !important; pointer-events: none !important; opacity: 0.7; }
        
        .btn-voltar { background-color: #0F172A; color: #64748B; font-weight: bold; border: 1px solid #1E293B; padding: 12px 20px; border-radius: 6px; font-size: 14px; text-decoration: none; display: inline-block; width: 100%; box-sizing: border-box; pointer-events: none; opacity: 0.5; transition: all 0.3s; }
        .btn-voltar.liberado { background-color: #0F172A; color: #38BDF8; border: 1px solid #2E3F66; pointer-events: auto; opacity: 1; cursor: pointer; }
        .btn-voltar.liberado:hover { background-color: #1E293B; }
    </style>
</head>
<body>
    <div class="card-sucesso">
        <h1>Pedido Registrado com Sucesso! 🎉</h1>
        <p>O estoque foi atualizado e seu pedido foi montado. Clique abaixo para enviar para o WhatsApp da loja.</p>
        
        {% if disponivel and link_zap %}
        <button id="btnZap" class="btn-zap" onclick="executarWhatsApp()">💬 Enviar Pedido para o WhatsApp</button>
        {% else %}
        <button class="btn-zap clicado" disabled>✔ Pedido já enviado</button>
        {% endif %}
        
        <a href="{{ url_for('index') }}" id="btnVoltar" class="btn-voltar {% if not disponivel %}liberado{% endif %}">🔄 Voltar ao Catálogo</a>
    </div>

    <script>
        const link_zap_raw = "{{ link_zap|safe if link_zap else '' }}";
        var jaAbriu = false;

        function executarWhatsApp() {
            if (jaAbriu || !link_zap_raw) return;
            jaAbriu = true;

            var btnZap = document.getElementById('btnZap');
            var btnVoltar = document.getElementById('btnVoltar');

            btnZap.innerHTML = '✔ Abrindo WhatsApp...';
            btnZap.classList.add('clicado');

            // Libera o botão de voltar ao catálogo imediatamente
            btnVoltar.classList.add('liberado');

            // Consome o pedido na sessão para evitar reenvios
            fetch('/consumir_pedido', { method: 'POST' });

            // Abre direto no chat limpo do WhatsApp Web
            setTimeout(function() {
                window.open(link_zap_raw, '_blank');
            }, 300);
        }
    </script>
</body>
</html>
"""


@app.template_filter('from_json')
def from_json_filter(s):
  if not s:
    return {}
  if isinstance(s, dict):
    return s
  try:
    return json.loads(s)
  except:
    return {}


@app.route('/ver_imagem')
def ver_imagem():
  caminho = request.args.get('caminho', '')
  if caminho and os.path.exists(caminho):
    return send_file(caminho)
  return '', 404


@app.route('/ver_mostruario/<path:nome>')
def ver_mostruario(nome):
  caminho_completo = os.path.join(PASTA_MOSTRUARIOS, nome)
  if os.path.exists(caminho_completo):
    return send_file(caminho_completo)
  return '', 404


@app.route('/')
def index():
  termo_busca = request.args.get('busca', '').strip()

  mostruarios = []
  if os.path.exists(PASTA_MOSTRUARIOS):
    extensoes_validas = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
    mostruarios = [
        f
        for f in os.listdir(PASTA_MOSTRUARIOS)
        if f.lower().endswith(extensoes_validas)
    ]

  conn = sqlite3.connect(DB_PATH, timeout=10.0)
  conn.execute('PRAGMA journal_mode=WAL;')
  cursor = conn.cursor()

  try:
    if termo_busca:
      palavras = termo_busca.split()
      condicoes = []
      parametros = ['%confec%']

      for palavra in palavras:
        condicoes.append(
            '(referencia LIKE ? OR nome LIKE ? OR codigo LIKE ? OR descricao LIKE'
            ' ?)'
        )
        p_like = f'%{palavra}%'
        parametros.extend([p_like, p_like, p_like, p_like])

      sql_where = 'WHERE grupo LIKE ? AND (' + ' OR '.join(condicoes) + ')'

      query = f"""
            SELECT id, codigo, nome, descricao, preco, estoque, foto_caminho, 
                   preco_custo, estoque_minimo, grupo, referencia, fornecedor, 
                   permitir_negativo, grade_json 
            FROM produtos 
            {sql_where}
            ORDER BY nome ASC
        """
      cursor.execute(query, parametros)
    else:
      query = """
            SELECT id, codigo, nome, descricao, preco, estoque, foto_caminho, 
                   preco_custo, estoque_minimo, grupo, referencia, fornecedor, 
                   permitir_negativo, grade_json 
            FROM produtos 
            WHERE grupo LIKE ? 
            ORDER BY nome ASC
        """
      cursor.execute(query, ('%confec%',))

    produtos = cursor.fetchall()
  finally:
    conn.close()

  return render_template_string(
      TEMPLATE_HTML,
      produtos=produtos,
      mostruarios=mostruarios,
      termo_busca=termo_busca,
  )


@app.route('/enviar_pedido', methods=['POST'])
def enviar_pedido():
  nome = request.form.get('cliente_nome', 'Cliente')
  tel = request.form.get('cliente_tel', '')

  itens_pedido = []
  total_geral = 0.0

  conn = sqlite3.connect(DB_PATH, timeout=10.0)
  conn.execute('PRAGMA journal_mode=WAL;')
  cursor = conn.cursor()

  try:
    # Garante a criação da tabela e adiciona automaticamente qualquer coluna que esteja faltando
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS contas_receber (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                telefone TEXT,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                status TEXT DEFAULT 'PENDENTE'
            )
        """)

    # Verifica e adiciona colunas caso a tabela já exista de uma versão antiga
    colunas_existentes = [
        col[1] for col in cursor.execute('PRAGMA table_info(contas_receber)')
    ]
    if 'telefone' not in colunas_existentes:
      cursor.execute('ALTER TABLE contas_receber ADD COLUMN telefone TEXT')
    if 'data' not in colunas_existentes:
      cursor.execute('ALTER TABLE contas_receber ADD COLUMN data TEXT')
    if 'status' not in colunas_existentes:
      cursor.execute(
          "ALTER TABLE contas_receber ADD COLUMN status TEXT DEFAULT 'PENDENTE'"
      )

    for chave, value in request.form.items():
      if chave.startswith('item_'):
        qtd = int(value) if value.isdigit() else 0
        if qtd > 0:
          partes = chave.split('_')
          prod_id = partes[1]
          tamanho = partes[2]

          cursor.execute(
              'SELECT nome, preco, estoque, grade_json, referencia FROM produtos WHERE id = ?',
              (prod_id,),
          )
          p = cursor.fetchone()
          if p:
            nome_prod, preco, estoque_geral, grade_json_str, referencia = (
                p[0],
                p[1],
                p[2],
                p[3],
                p[4],
            )
            subtotal = qtd * preco
            total_geral += subtotal

            ref_texto = f' (Ref: {referencia})' if referencia else ''
            itens_pedido.append(
                f'• {qtd}x {nome_prod}{ref_texto} (Tam: {tamanho}) - R$'
                f' {subtotal:.2f}'.replace('.', ',')
            )

            grade_dict = {}
            try:
              grade_dict = json.loads(grade_json_str) if grade_json_str else {}
            except:
              grade_dict = {}

            atual_tam = float(grade_dict.get(tamanho, 0.0))
            novo_tam = max(0.0, atual_tam - qtd)
            grade_dict[tamanho] = (
                int(novo_tam) if novo_tam.is_integer() else novo_tam
            )

            novo_est_geral = max(0.0, float(estoque_geral or 0) - qtd)
            novo_grade_json = json.dumps(grade_dict)

            cursor.execute(
                'UPDATE produtos SET estoque = ?, grade_json = ? WHERE id = ?',
                (novo_est_geral, novo_grade_json, prod_id),
            )

    if not itens_pedido:
      return (
          "<script>alert('Selecione pelo menos um item na"
          " grade!'); window.history.back();</script>"
      )

    # Lança automaticamente o registro em Contas a Receber
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    cursor.execute(
        """
            INSERT INTO contas_receber (cliente, telefone, valor, data, status)
            VALUES (?, ?, ?, ?, 'PENDENTE')
        """,
        (nome, tel, total_geral, data_atual),
    )

    conn.commit()
  finally:
    conn.close()

  msg = (
      f'Olá! Meu nome é *{nome}* (WhatsApp: {tel}) e gostaria de fechar este'
      ' pedido:\n\n'
      + '\n'.join(itens_pedido)
      + f'\n\n*Valor Total:* R$ {total_geral:.2f}'.replace('.', ',')
  )
  msg += '\nAguardando instruções de pagamento e entrega.'

  import urllib.parse

  link_zap = f'https://web.whatsapp.com/send?phone={WHATSAPP_LOJA}&text={urllib.parse.quote(msg)}'

  session['link_zap'] = link_zap
  session['disponivel'] = True

  return redirect(url_for('sucesso'))


@app.route('/sucesso')
def sucesso():
  link_zap = session.get('link_zap', '')
  disponivel = session.get('disponivel', False)
  return render_template_string(
      TEMPLATE_SUCESSO, link_zap=link_zap, disponivel=disponivel
  )


@app.route('/consumir_pedido', methods=['POST'])
def consumir_pedido():
  session['disponivel'] = False
  session['link_zap'] = ''
  return '', 204


if __name__ == '__main__':
  print('Servidor do Catálogo Online rodando em http://127.0.0.1:5000')
  app.run(host='0.0.0.0', port=5000, debug=True)