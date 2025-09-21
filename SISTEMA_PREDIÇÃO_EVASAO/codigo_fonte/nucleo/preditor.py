"""
Sistema principal de predição de evasão estudantil.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd

from ..utilitarios import obter_registrador, CarregadorDados
from ..configuracao import configuracoes
from ..modelos import PreditorEvasaoEstudantil
from ..regras_negocio import MotorRegrasNegocio, AnalisadorCurriculo, ResultadoRegra

registrador = obter_registrador(__name__)

@dataclass
class PredicaoAluno:
    """Dados de predição para um aluno."""
    nome: str
    matricula: str
    situacao_atual: str
    curso: str
    sexo: str
    turma: str
    status_predicao: str  # MATRICULADO ou RISCO_EVASAO
    situacao_predita: str
    probabilidade_situacao: str
    probabilidade_evasao_total: str
    nivel_urgencia: str
    fator_principal: str
    valor_importancia: float
    confianca_predicao: str
    fonte_predicao: str
    predicao_ml_original: str
    prob_ml_original: str
    top_1_situacao_ml: str
    top_1_probabilidade_ml: str
    top_2_situacao_ml: str
    top_2_probabilidade_ml: str
    top_3_situacao_ml: str
    top_3_probabilidade_ml: str

class SistemaPredicaoEvasao:
    """Sistema principal de predição de evasão estudantil."""
    
    def __init__(self):
        """Inicializa o sistema."""
        self.preditor_ml = PreditorEvasaoEstudantil()
        self.motor_regras_negocio = None
        self.analisador_curriculo = None
        self._inicializado = False
    
    def inicializar(self) -> None:
        """
        Inicializa todos os componentes do sistema.
        
        Raises:
            Exception: Se houver erro na inicialização
        """
        try:
            registrador.info("Inicializando sistema de predição de evasão...")
            
            # Carregar modelo ML
            self.preditor_ml.carregar_modelo()
            
            # Carregar grade curricular
            df_disciplinas, df_cursos = CarregadorDados.carregar_dados_curriculares()
            
            # Inicializar analisador de currículo
            self.analisador_curriculo = AnalisadorCurriculo(df_disciplinas, df_cursos)
            
            # Inicializar motor de regras de negócio
            self.motor_regras_negocio = MotorRegrasNegocio(self.analisador_curriculo)
            
            self._inicializado = True
            registrador.info("Sistema inicializado com sucesso")
            
        except Exception as e:
            registrador.error(f"Erro na inicialização do sistema: {e}")
            raise
    
    def predizer_alunos(self, arquivo_alunos: Path) -> Tuple[List[PredicaoAluno], Dict[str, Any]]:
        """
        Faz predições para todos os alunos no arquivo.
        
        Args:
            arquivo_alunos: Caminho para o arquivo com dados dos alunos
            
        Returns:
            Tuple com lista de predições e estatísticas
        """
        if not self._inicializado:
            raise RuntimeError("Sistema não foi inicializado. Chame inicializar() primeiro.")
        
        registrador.info(f"Iniciando predições para arquivo: {arquivo_alunos}")
        
        # Carregar dados
        df = CarregadorDados.carregar_excel_com_deteccao_cabecalho(arquivo_alunos)
        registrador.info(f"Dados carregados: {len(df)} alunos")
        
        # Preprocessar dados para o modelo ML
        df_processado = self.preditor_ml.preprocessar_dados(df)
        
        # Fazer predições ML
        predicoes_ml, probabilidades_ml, valores_shap = self.preditor_ml.fazer_predicoes(df_processado)
        
        # Resetar contadores de regras
        self.motor_regras_negocio.resetar_contadores()
        
        # Processar cada aluno
        predicoes = []
        contador_matriculados = 0
        contador_risco_evasao = 0
        
        for i, (_, dados_aluno) in enumerate(df.iterrows()):
            # Obter predição ML para este aluno
            predicao_ml = predicoes_ml[i]
            probabilidade_ml = max(probabilidades_ml[i])
            
            # Aplicar regras de negócio
            resultado_regra = self.motor_regras_negocio.aplicar_regras_negocio(
                dados_aluno.to_dict(), predicao_ml, probabilidade_ml
            )
            
            # Criar objeto de predição
            predicao_aluno = self._criar_predicao_aluno(
                dados_aluno, resultado_regra, i, probabilidades_ml[i], 
                valores_shap, df_processado.columns.tolist(), i
            )
            
            predicoes.append(predicao_aluno)
            
            # Contar resultados
            if predicao_aluno.status_predicao == 'MATRICULADO':
                contador_matriculados += 1
            else:
                contador_risco_evasao += 1
        
        # Compilar estatísticas
        estatisticas = {
            'total_students': len(predicoes),
            'enrolled_students': contador_matriculados,
            'dropout_risk_students': contador_risco_evasao,
            'enrolled_percentage': (contador_matriculados / len(predicoes)) * 100,
            'dropout_risk_percentage': (contador_risco_evasao / len(predicoes)) * 100,
            'rules_summary': self.motor_regras_negocio.obter_resumo_regras()
        }
        
        registrador.info(f"Predições concluídas: {contador_matriculados} matriculados, {contador_risco_evasao} em risco")
        
        return predicoes, estatisticas
    
    def _criar_predicao_aluno(self, dados_aluno: pd.Series, resultado_regra: ResultadoRegra,
                             indice_predicao_ml: int, probabilidades_ml: List[float],
                             valores_shap: Any, nomes_features: List[str], 
                             indice_aluno: int) -> PredicaoAluno:
        """Cria objeto de predição para um aluno."""
        
        # Informações básicas do aluno
        nome = str(dados_aluno.get('Nome', f'Aluno_{indice_aluno+1}'))
        matricula = CarregadorDados.limpar_identificador_aluno(dados_aluno.to_dict())
        situacao_atual = str(dados_aluno.get('Situação', 'Não informada'))
        curso = str(dados_aluno.get('Curso', 'Não informado'))
        sexo = str(dados_aluno.get('Sexo', 'Não informado'))
        turma = str(dados_aluno.get('Turma Atual', 'Não informada'))
        
        # Determinar status da predição
        if resultado_regra.situacao == 'Matriculado':
            status_predicao = 'MATRICULADO'
        else:
            status_predicao = 'RISCO_EVASAO'
        
        # Calcular nível de urgência baseado no status e probabilidade
        if status_predicao == 'MATRICULADO':
            # Alunos matriculados estão OK, sem urgência
            nivel_urgencia = 'NENHUMA'
        else:
            # Para alunos em risco, usar probabilidade para definir urgência
            probabilidade_num = resultado_regra.probabilidade
            if probabilidade_num >= 0.9:
                nivel_urgencia = 'URGENTE'
            elif probabilidade_num >= 0.8:
                nivel_urgencia = 'ALTA'
            elif probabilidade_num >= 0.7:
                nivel_urgencia = 'MEDIA'
            else:
                nivel_urgencia = 'BAIXA'
        
        # Obter fator principal (feature mais importante do SHAP)
        fator_principal = "N/A"
        valor_importancia = 0.0
        try:
            if len(valores_shap) > indice_aluno and len(nomes_features) > 0:
                valores_aluno = valores_shap[indice_aluno] if hasattr(valores_shap[indice_aluno], '__len__') else []
                if len(valores_aluno) > 0:
                    # Converter para numpy array se necessário
                    import numpy as np
                    valores_array = np.array(valores_aluno)
                    
                    # Para modelos multiclasse, valores SHAP têm forma (n_features, n_classes)
                    # Calcular a importância absoluta máxima por feature (entre todas as classes)
                    if valores_array.ndim == 2:  # Shape (n_features, n_classes)
                        # Para cada feature, pegar o valor SHAP com maior magnitude absoluta
                        importancias_features = np.max(np.abs(valores_array), axis=1)
                        indice_max = np.argmax(importancias_features)
                        
                        if indice_max < len(nomes_features):
                            fator_principal = nomes_features[indice_max]
                            # Valor específico que teve maior impacto para esta feature
                            classe_max = np.argmax(np.abs(valores_array[indice_max]))
                            valor_importancia = float(valores_array[indice_max, classe_max])
                    elif valores_array.ndim == 1:  # Shape (n_features,) - modelo binário
                        indice_max = np.argmax(np.abs(valores_array))
                        if indice_max < len(nomes_features):
                            fator_principal = nomes_features[indice_max]
                            valor_importancia = float(valores_array[indice_max])
        except Exception as e:
            # Se houver algum erro com SHAP, usar valores padrão
            registrador.debug(f"Erro ao processar valores SHAP para aluno {indice_aluno}: {e}")
            fator_principal = "N/A"
            valor_importancia = 0.0
        
        # Mapear features técnicas para nomes amigáveis
        mapeamento_features = {
            'Pend. Financ.': 'Pend. Financ.',
            'Faltas Consecutivas': 'Faltas Consec.',
            'Pend. Acad.': 'Pend. Acad.',
        }
        fator_principal_amigavel = mapeamento_features.get(fator_principal, fator_principal)
        
        # Preparar informações sobre predições ML (top 3)
        # Usar as classes reais do modelo - verificar diferentes chaves possíveis
        if self.preditor_ml.info_classes:
            if 'class_names' in self.preditor_ml.info_classes:
                nomes_classes = list(self.preditor_ml.info_classes['class_names'])
            elif 'classes' in self.preditor_ml.info_classes:
                nomes_classes = list(self.preditor_ml.info_classes['classes'])
            elif 'situacao_mapping' in self.preditor_ml.info_classes:
                nomes_classes = list(self.preditor_ml.info_classes['situacao_mapping'].values())
            else:
                # Usar as chaves do próprio dicionário
                nomes_classes = list(self.preditor_ml.info_classes.keys()) if isinstance(self.preditor_ml.info_classes, dict) else ['Classe_0', 'Classe_1', 'Classe_2', 'Classe_3', 'Classe_4', 'Classe_5']
        else:
            nomes_classes = ['Classe_0', 'Classe_1', 'Classe_2', 'Classe_3', 'Classe_4', 'Classe_5']
            
        probabilidades_ordenadas = sorted(enumerate(probabilidades_ml), key=lambda x: x[1], reverse=True)
        
        # Verificar se há probabilidades válidas
        if not probabilidades_ordenadas or len(nomes_classes) == 0:
            top_1_situacao = 'N/A'
            top_1_prob = '0%'
            top_2_situacao = 'N/A' 
            top_2_prob = '0%'
            top_3_situacao = 'N/A'
            top_3_prob = '0%'
        else:
            # Garantir que os índices estão dentro dos limites
            idx_0 = probabilidades_ordenadas[0][0] if len(probabilidades_ordenadas) > 0 else 0
            top_1_situacao = nomes_classes[idx_0] if idx_0 < len(nomes_classes) else 'N/A'
            top_1_prob = f"{probabilidades_ordenadas[0][1]*100:.1f}%" if probabilidades_ordenadas else '0%'
            
            idx_1 = probabilidades_ordenadas[1][0] if len(probabilidades_ordenadas) > 1 else 0
            top_2_situacao = nomes_classes[idx_1] if len(probabilidades_ordenadas) > 1 and idx_1 < len(nomes_classes) else 'N/A'
            top_2_prob = f"{probabilidades_ordenadas[1][1]*100:.1f}%" if len(probabilidades_ordenadas) > 1 else '0%'
            
            idx_2 = probabilidades_ordenadas[2][0] if len(probabilidades_ordenadas) > 2 else 0
            top_3_situacao = nomes_classes[idx_2] if len(probabilidades_ordenadas) > 2 and idx_2 < len(nomes_classes) else 'N/A'
            top_3_prob = f"{probabilidades_ordenadas[2][1]*100:.1f}%" if len(probabilidades_ordenadas) > 2 else '0%'
        
        # Fonte da predição
        if resultado_regra.regra_aplicada == 'ML':
            fonte_predicao = 'Predição ML'
        else:
            fonte_predicao = f"Regra {resultado_regra.regra_aplicada}: {resultado_regra.razao}"
        
        return PredicaoAluno(
            nome=nome,
            matricula=matricula,
            situacao_atual=situacao_atual,
            curso=curso,
            sexo=sexo,
            turma=turma,
            status_predicao=status_predicao,
            situacao_predita=resultado_regra.situacao,
            probabilidade_situacao=f"{resultado_regra.probabilidade*100:.1f}%",
            probabilidade_evasao_total=f"{resultado_regra.probabilidade*100:.1f}%",
            nivel_urgencia=nivel_urgencia,
            fator_principal=fator_principal_amigavel,
            valor_importancia=abs(valor_importancia),
            confianca_predicao='Alta',
            fonte_predicao=fonte_predicao,
            predicao_ml_original=top_1_situacao,
            prob_ml_original=top_1_prob,
            top_1_situacao_ml=top_1_situacao,
            top_1_probabilidade_ml=top_1_prob,
            top_2_situacao_ml=top_2_situacao,
            top_2_probabilidade_ml=top_2_prob,
            top_3_situacao_ml=top_3_situacao,
            top_3_probabilidade_ml=top_3_prob
        )