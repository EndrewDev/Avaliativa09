import subprocess, json, os

def tracert_to_url(url, sisoperacional):
    print('Aguardando...')
    try:
        if sisoperacional == 'Windows':
            # Executa o comando tracert
            result = subprocess.run(['tracert', '-d', url], capture_output=True, text=True, shell=True) 
        elif sisoperacional == 'Linux':
            result = subprocess.run(['traceroute', '-n', url], capture_output=True, text=True)
        else:
            return f'Sistema operacioanl não suportado: {sisoperacional}'
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Erro ao executar o comando: {result.stderr}"
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"
    
def cria_arquivo(url, resultado):
    data = {url: resultado}
    with open('Dicionario_URL.json', 'w') as f:
        json.dump(data, f, indent=4)
