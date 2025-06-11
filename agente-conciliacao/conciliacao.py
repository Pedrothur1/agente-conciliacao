import pandas as pd

def padroniza_base_cliente(path):
    df = pd.read_excel(path)
    df_pad = pd.DataFrame()
    df_pad['Data'] = pd.to_datetime(df['Data movimento'], dayfirst=True, errors='coerce')
    df_pad['Conta'] = df['Conta bancária'].astype(str).str.strip()
    df_pad['Valor'] = df['Valor (R$)'].astype(float)
    df_pad['Tipo'] = df['Tipo da operação'].strip()
    return df_pad

def padroniza_extrato_caixa(path):
    df = pd.read_excel(path, skiprows=1)
    df_pad = pd.DataFrame()
    df_pad['Data'] = pd.to_datetime(df['Unnamed: 1'], errors='coerce')
    df_pad['Conta'] = 'Caixa'
    df_pad['Valor'] = pd.to_numeric(df['Unnamed: 4'], errors='coerce')
    df_pad['Tipo'] = df_pad['Valor'].apply(lambda x: 'Crédito' if x > 0 else 'Débito')
    return df_pad

def padroniza_extrato_itau(path):
    df_raw = pd.read_excel(path, header=None)
    start = None
    for i in range(10, len(df_raw)):
        try:
            pd.to_datetime(df_raw.iloc[i,0], errors='raise')
            float(str(df_raw.iloc[i,3]).replace(',','.'))
            start = i
            break
        except:
            continue
    if start is None:
        raise Exception("Não foi possível identificar o início dos dados do extrato Itaú")
    df = pd.read_excel(path, skiprows=start, names=["Data","Histórico","Agência","Documento","Valor","Saldo"])
    df_pad = pd.DataFrame()
    df_pad['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df_pad['Conta'] = 'Itaú'
    df_pad['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    df_pad['Tipo'] = df_pad['Valor'].apply(lambda x: 'Crédito' if x > 0 else 'Débito')
    return df_pad

def conciliacao_1_1(base, extrato):
    base = base.copy()
    base['Conciliado'] = False
    for idx, row in extrato.iterrows():
        mask = (
            (base['Data'] == row['Data']) &
            (base['Conta'].str.lower() == row['Conta'].lower()) &
            (abs(base['Valor'] - row['Valor']) < 0.01) &
            (base['Tipo'] == row['Tipo']) &
            (~base['Conciliado'])
        )
        if mask.any():
            base.loc[mask, 'Conciliado'] = True
    return base
