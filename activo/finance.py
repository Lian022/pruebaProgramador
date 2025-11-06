import requests

def _preparar_datos_flujo(datos):

    fco_por_periodo = {}
    max_periodo = 0
    periodo_final_ingresos = 0

    for item in datos:
        periodo = item.get('periodo')
        valor = item.get('valor', 0)
        concepto = item.get('concepto')

        if not periodo:
            continue

        if periodo not in fco_por_periodo:
            fco_por_periodo[periodo] = 0

        if concepto == 'ingresos':
            fco_por_periodo[periodo] += valor
            if periodo > periodo_final_ingresos:
                periodo_final_ingresos = periodo
        elif concepto == 'costos':
            fco_por_periodo[periodo] -= valor

        if periodo > max_periodo:
            max_periodo = periodo

    return fco_por_periodo, max_periodo, periodo_final_ingresos

def calcular_flujo_financiacion(datos, cupo_credito, porcentaje_max_desembolso, 
                                periodo_inicial_credito, periodo_final_credito, tasa_interes):
 
# --- PREPARACIÓN Y CONSTANTES ---
    fco_por_periodo, max_periodo, periodo_final_ingresos = _preparar_datos_flujo(datos)

    tasa_interes_mensual = tasa_interes / 12
    desembolso_max_mensual = cupo_credito * porcentaje_max_desembolso
    
# --- Períodos de pago según la regla
    periodo_pago_1 = periodo_final_ingresos - 1
    periodo_pago_2 = periodo_final_ingresos

# ---  PASADA 1: CALCULAR SALDO PARA PAGO ---

    saldo_temporal = 0
    for periodo in range(1, periodo_pago_1):
        fco = fco_por_periodo.get(periodo, 0)
        
        necesidad_caja_fco = -fco if fco < 0 else 0
        desembolso_del_mes = 0
        puede_desembolsar = (
            periodo >= periodo_inicial_credito and
            periodo <= periodo_final_credito and
            saldo_temporal < cupo_credito
        )

        if necesidad_caja_fco > 0 and puede_desembolsar:
            max_desembolso_por_cupo = cupo_credito - saldo_temporal
            desembolso_del_mes = min(necesidad_caja_fco, desembolso_max_mensual, max_desembolso_por_cupo)
        
        saldo_temporal += desembolso_del_mes

    monto_pago_mensual = saldo_temporal / 2

# ---  PASADA 2: CÁLCULO COMPLETO CON PAGOS ---
    
    lista_desembolsos = []
    lista_aportes = []
    
    saldo_credito_real = 0
    intereses_mes_anterior = 0

    for periodo in range(1, max_periodo + 1):
        
        fco = fco_por_periodo.get(periodo, 0)
        intereses_pagados = intereses_mes_anterior 
        
        pago_credito = 0
        if periodo == periodo_pago_1 or periodo == periodo_pago_2:
            pago_credito = min(monto_pago_mensual, saldo_credito_real)

        necesidad_caja_fco = -fco if fco < 0 else 0
        desembolso_del_mes = 0

        puede_desembolsar = (
            periodo >= periodo_inicial_credito and
            periodo <= periodo_final_credito and
            saldo_credito_real < cupo_credito
        )
        
        if necesidad_caja_fco > 0 and puede_desembolsar:
            max_desembolso_por_cupo = cupo_credito - saldo_credito_real
            desembolso_del_mes = min(necesidad_caja_fco, desembolso_max_mensual, max_desembolso_por_cupo)
            
            # Redondear a 2 decimales para evitar problemas de flotantes
            desembolso_del_mes = round(desembolso_del_mes, 2)
            lista_desembolsos.append({"periodo": periodo, "valor": desembolso_del_mes})

# --- Calcular FCN y Aporte necesario
        # FCN = FCO + Desembolsos - Intereses pagados - Pago del crédito 
        fcn = fco + desembolso_del_mes - intereses_pagados - pago_credito
        
        aporte_del_mes = 0
        if fcn < 0:
            aporte_del_mes = -fcn
            aporte_del_mes = round(aporte_del_mes, 2)
            lista_aportes.append({"periodo": periodo, "valor": aporte_del_mes})

        saldo_credito_real = saldo_credito_real + desembolso_del_mes - pago_credito
        intereses_mes_anterior = saldo_credito_real * tasa_interes_mensual

    return lista_desembolsos, lista_aportes

# --- BLOQUE DE EJECUCIÓN DE PRUEBA ---
if __name__ == "__main__":
    
    URL_DATOS = "https://storage.googleapis.com/siga-cdn-bucket/temporal_dm/datos_gerpro_prueba.json" 
    CUPO = 7000.0
    PCT_DESEMBOLSO = 0.08  # 8%
    PERIODO_INICIAL = 9    # Sep-19 (9no mes) o jul-19(7mo mes)
    PERIODO_FINAL = 23     # Nov20 (23vo mes) o jun-21(30vo mes)
    TASA_ANUAL = 0.12      # 12%

    print(f"Obteniendo datos de {URL_DATOS}...")
    try:
        response = requests.get(URL_DATOS)
        response.raise_for_status()  
        datos_proyecto = response.json()
        print(f"Datos obtenidos: {len(datos_proyecto)} registros.")
        
        desembolsos, aportes = calcular_flujo_financiacion(
            datos=datos_proyecto,
            cupo_credito=CUPO,
            porcentaje_max_desembolso=PCT_DESEMBOLSO,
            periodo_inicial_credito=PERIODO_INICIAL,
            periodo_final_credito=PERIODO_FINAL,
            tasa_interes=TASA_ANUAL
        )

# ---  Mostrar resultados
        print("\n--- RESULTADO: DESEMBOLSOS DE CRÉDITO ---")
        for item in desembolsos:
            print(f"  Periodo {item['periodo']}: ${item['valor']:,.2f}")

        print("\n--- RESULTADO: APORTES DE CAPITAL ---")
        for item in aportes:
            print(f"  Periodo {item['periodo']}: ${item['valor']:,.2f}")

    except requests.exceptions.RequestException as e:
        print(f"\nError: No se pudieron obtener los datos de la URL.")
        print(f"Detalle: {e}")
    except Exception as e:
        print(f"\nOcurrió un error durante el cálculo: {e}")