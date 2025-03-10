from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.utils import is_admin
from models.expense_concepts import ExpenseConcepts
from controllers.expenseConceptsController import OdooSaleOrderTool
import logging

logger = logging.getLogger(__name__)

expense_concepts = Blueprint('expense_concepts', __name__, url_prefix='/portal_proveedores')

@expense_concepts.route('/perfilconsulta2025/consultas')
@is_admin
@login_required
def expense_concepts_list_view():
    expense_concepts = ExpenseConcepts.get_all()
    return render_template('home/expense_concepts/list.html', expense_concepts=expense_concepts)
@expense_concepts.route('/get')
@is_admin
@login_required
def get_invoices():
    return OdooSaleOrderTool()

@expense_concepts.route('/perfilconsulta2025')
@is_admin
@login_required
def consultas_dashboard():
    return render_template('home/dashboard.html')