from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, abort
from flask_sqlalchemy import SQLAlchemy
import io, csv, os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from functools import wraps

# --- Config ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-123')

db = SQLAlchemy(app)

# --- Models ---
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_empresa = db.Column(db.String(150), nullable=False)
    cnpj = db.Column(db.String(30))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(150))
    endereco = db.Column(db.String(250))
    nome_responsavel = db.Column(db.String(120))
    cpf = db.Column(db.String(30))
    numero_sedes = db.Column(db.String(50))
    equipamentos = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    tarefas = db.relationship('Tarefa', backref='cliente', cascade='all, delete-orphan', lazy=True)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pendente')
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

# --- Simple auth ---
VALID_USER = 'admin'
VALID_PASS = '1234'

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated

# --- Main routes (protected) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user == VALID_USER and pwd == VALID_PASS:
            session['logged_in'] = True
            session['user'] = user
            flash('Login realizado com sucesso!', 'success')
            nxt = request.args.get('next') or url_for('index')
            return redirect(nxt)
        flash('Usuário ou senha inválidos.', 'warning')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    clientes = Cliente.query.order_by(Cliente.nome_empresa).all()
    return render_template('index.html', clientes=clientes)

@app.route('/cliente/novo', methods=['GET', 'POST'])
@login_required
def novo_cliente():
    if request.method == 'POST':
        c = Cliente(
            nome_empresa=request.form.get('nome_empresa'),
            cnpj=request.form.get('cnpj'),
            telefone=request.form.get('telefone'),
            email=request.form.get('email'),
            endereco=request.form.get('endereco'),
            nome_responsavel=request.form.get('nome_responsavel'),
            cpf=request.form.get('cpf'),
            numero_sedes=request.form.get('numero_sedes'),
            equipamentos=request.form.get('equipamentos'),
            observacoes=request.form.get('observacoes')
        )
        db.session.add(c)
        db.session.commit()
        flash('Cliente criado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('cliente_form.html', cliente=None, acao='Novo')

@app.route('/cliente/<int:cliente_id>')
@login_required
def ver_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    tarefas = Tarefa.query.filter_by(cliente_id=cliente.id).order_by(Tarefa.status.desc()).all()
    return render_template('cliente.html', cliente=cliente, tarefas=tarefas)

@app.route('/cliente/<int:cliente_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    if request.method == 'POST':
        cliente.nome_empresa = request.form.get('nome_empresa')
        cliente.cnpj = request.form.get('cnpj')
        cliente.telefone = request.form.get('telefone')
        cliente.email = request.form.get('email')
        cliente.endereco = request.form.get('endereco')
        cliente.nome_responsavel = request.form.get('nome_responsavel')
        cliente.cpf = request.form.get('cpf')
        cliente.numero_sedes = request.form.get('numero_sedes')
        cliente.equipamentos = request.form.get('equipamentos')
        cliente.observacoes = request.form.get('observacoes')
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('ver_cliente', cliente_id=cliente.id))
    return render_template('cliente_form.html', cliente=cliente, acao='Editar')

@app.route('/cliente/<int:cliente_id>/excluir', methods=['POST'])
@login_required
def excluir_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluído.', 'warning')
    return redirect(url_for('index'))

@app.route('/cliente/<int:cliente_id>/tarefa/nova', methods=['GET', 'POST'])
@login_required
def nova_tarefa(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    if request.method == 'POST':
        t = Tarefa(
            titulo=request.form.get('titulo'),
            descricao=request.form.get('descricao'),
            status=request.form.get('status') or 'Pendente',
            cliente_id=cliente.id
        )
        db.session.add(t)
        db.session.commit()
        flash('Tarefa criada!', 'success')
        return redirect(url_for('ver_cliente', cliente_id=cliente.id))
    return render_template('tarefa_form.html', cliente=cliente, tarefa=None, acao='Nova')

@app.route('/tarefa/<int:tarefa_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    cliente = tarefa.cliente
    if request.method == 'POST':
        tarefa.titulo = request.form.get('titulo')
        tarefa.descricao = request.form.get('descricao')
        tarefa.status = request.form.get('status') or 'Pendente'
        db.session.commit()
        flash('Tarefa atualizada!', 'success')
        return redirect(url_for('ver_cliente', cliente_id=cliente.id))
    return render_template('tarefa_form.html', cliente=cliente, tarefa=tarefa, acao='Editar')

@app.route('/tarefa/<int:tarefa_id>/excluir', methods=['POST'])
@login_required
def excluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    cliente_id = tarefa.cliente_id
    db.session.delete(tarefa)
    db.session.commit()
    flash('Tarefa removida.', 'warning')
    return redirect(url_for('ver_cliente', cliente_id=cliente_id))

@app.route('/tarefa/<int:tarefa_id>/toggle')
@login_required
def toggle_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    tarefa.status = 'Concluída' if tarefa.status != 'Concluída' else 'Pendente'
    db.session.commit()
    return redirect(url_for('ver_cliente', cliente_id=tarefa.cliente_id))

# --- Export CSV (relatório completo) ---
@app.route('/export/csv')
@login_required
def export_csv():
    clientes = Cliente.query.order_by(Cliente.nome_empresa).all()
    output = io.StringIO()
    writer = csv.writer(output)
    header = ['id','nome_empresa','cnpj','telefone','email','endereco','nome_responsavel','cpf','numero_sedes','equipamentos','observacoes','tarefas']
    writer.writerow(header)
    for c in clientes:
        tarefas = []
        for t in c.tarefas:
            tarefas.append(f"{t.titulo}||{t.status}||{t.descricao or ''}")
        tarefas_str = ' ;; '.join(tarefas)
        writer.writerow([c.id, c.nome_empresa, c.cnpj, c.telefone, c.email, c.endereco, c.nome_responsavel, c.cpf, c.numero_sedes, c.equipamentos, c.observacoes, tarefas_str])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='clientes_full_report.csv')

# --- Export PDF (relatório completo) ---
@app.route('/export/pdf')
@login_required
def export_pdf():
    clientes = Cliente.query.order_by(Cliente.nome_empresa).all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin

    p.setFont('Helvetica-Bold', 16)
    p.drawString(margin, y, 'Relatório Completo de Clientes')
    y -= 30
    p.setFont('Helvetica', 9)

    for c in clientes:
        if y < 120:
            p.showPage()
            y = height - margin
            p.setFont('Helvetica', 9)
        p.setFont('Helvetica-Bold', 12)
        p.drawString(margin, y, f"{c.nome_empresa}  (ID: {c.id})")
        y -= 16
        p.setFont('Helvetica', 9)
        fields = [
            ('CNPJ', c.cnpj),
            ('Telefone', c.telefone),
            ('Email', c.email),
            ('Endereço', c.endereco),
            ('Responsável', c.nome_responsavel),
            ('CPF', c.cpf),
            ('Número de sedes', c.numero_sedes),
        ]
        for label, val in fields:
            text = f"{label}: {val or '-'}"
            p.drawString(margin+8, y, text)
            y -= 12
            if y < 100:
                p.showPage()
                y = height - margin
        p.drawString(margin+8, y, f"Equipamentos: { (c.equipamentos or '-')[:200] }")
        y -= 12
        p.drawString(margin+8, y, f"Observações: { (c.observacoes or '-')[:200] }")
        y -= 14
        p.setFont('Helvetica-Bold', 10)
        p.drawString(margin+8, y, 'Tarefas:')
        y -= 14
        p.setFont('Helvetica', 9)
        if c.tarefas:
            for t in c.tarefas:
                line = f"- {t.titulo} [{t.status}] - { (t.descricao or '-')[:180] }"
                if len(line) > 120:
                    parts = [line[i:i+120] for i in range(0, len(line), 120)]
                    for part in parts:
                        p.drawString(margin+16, y, part)
                        y -= 12
                        if y < 100:
                            p.showPage()
                            y = height - margin
                else:
                    p.drawString(margin+16, y, line)
                    y -= 12
                if y < 100:
                    p.showPage()
                    y = height - margin
        else:
            p.drawString(margin+16, y, '-')
            y -= 12
        p.line(margin, y, width-margin, y)
        y -= 16

    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='clientes_full_report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    # Garante que o banco existe antes de iniciar o servidor (compatível com qualquer versão do Flask)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
