from datetime import datetime, timedelta

ano_em_vigor = datetime.now().year
tabelas ={
      0 : "Plano_de_Accao",
      1 : "Saidas_da_RGT",
      2: "Controlo_de_Alcoolemia",
      3: "Controlo_de_Acidentes_de_Trabalho",
      4:"Controlo_de_Incidentes_de_Trabalho",
      5:"Cronograma_Minutos_Seguranca",
      6:"Controlo_Accoes_de_HSE",
      7:"Controlo_de_Impressoras_Doadas",
      8:"Plano_de_Prevencao_de_Doencas_Promocao_da_Saude"
  }

ficheiro ={
     0:"MP.85.DMC - Plano de Acção.xlsx",
     1:"MP.30.DMC - Saídas das RGTs.xlsx",
     2:"MP.49.DMC - Controlo de Alcoolemia.xlsx",
     3:"MP.58.DMC - Controlo de Acidente de Trabalho.xlsx",
     4:"FO.63.DMC - Controlo de Incidentes de Trabalho.xlsx",
     5:"MP.82.DMC - Cronograma - Minutos de Segurança.xlsx",
     6:"MP.38.DMC - Controlo das acções de HSE.xlsx",
     7:"MP.65.DMC - Controlo de Impressoras Doadas.xlsx",
     8:"MP.46.DMC - Plano de Prevenção de Doenças e Promoção da Saúde.xlsx"
  }

folha ={
     0 : "2024-2025",
     1:" ",
     2:f"CONTROLO {ano_em_vigor}",
     3 : f"{ano_em_vigor}",
     4 : f"{ano_em_vigor}",
     5: f"MS - {ano_em_vigor}",
     6:f"{ano_em_vigor}",
     7:" ",
     8:f"{ano_em_vigor}"

  }

campo ={
     0 : "Ano",
     1:"Ano",
     2:"Ano",
     3:"Ano",
     4:"Ano",
     5:"Data Prevista",
     6:"Ano",
     7:"Data de doação",
     8:"Data/Inicio Agendamento"
  }
titulo ={
     0 : "Plano de Acção",
     1: "Saídas da RGT",
     2:"Controlo de Alcoolemia",
     3:"Controlo de Acidentes de Trabalho",
     4:"Controlo de Incidentes de Trabalho",
     5:"Cronograma - Minutos de Segurança",
     6:"Controlo - Acções de HSE",
     7:"Controlo de Impressoras Doadas",
     8:"Plano de Prevenção de Doenças e Promoção da Saúde"
  }



