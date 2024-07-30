from datetime import datetime, timedelta
import openpyxl

class Usuario:
    def __init__(self, cpf):
        self.cpf = cpf
        self.nome = None
        self.data_cadastro = None

    def carregar_data_cadastro(self):
        try:
            workbook = openpyxl.load_workbook('usuarios.xlsx')
            sheet = workbook.active
            for row in sheet.iter_rows(values_only=True):
                if str(row[0]) == str(self.cpf):
                    self.nome = row[2] 
                    self.data_cadastro = row[1]
                     
                    workbook.close()
                    return True
            workbook.close()
        except Exception as e:
            print(f"Erro ao carregar dados do usuário: {e}")
        return False
    
    def get_primeiro_segundo_nome(self):
        if self.nome:
            nomes = self.nome.split()
            if len(nomes) > 1:
                return f"{nomes[0]} {nomes[1]}"
            else:
                return nomes[0]
        return ""

    def validar_senha(self, senha):
        cpf_sem_zeros = str(self.cpf).lstrip('0')
        senha_esperada = cpf_sem_zeros[:6]
        return senha == senha_esperada

    def calcular_tempo_restante(self):
        if self.data_cadastro:
            data_limite = self.data_cadastro + timedelta(days=180)
            tempo_restante = data_limite - datetime.today()
            return {'dias_restantes': tempo_restante.days if tempo_restante.days > 0 else 0,
                    'data_limite': data_limite.strftime('%d/%m/%Y'),
                    'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y')}
        return {'dias_restantes': 0, 'data_limite': None, 'data_cadastro': None}