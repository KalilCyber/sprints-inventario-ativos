import json

ARQUIVO_INVENTARIO = "ativos_inventario.json"

def carregar_ativos(nome_arquivo):
    """Lê o arquivo JSON e carrega os ativos com tratamento de exceções de I/O."""
    print("[Carregando base de dados...]")
    ativos = []
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            ativos = json.load(arquivo)
            print("Inventário carregado com sucesso!")
            
    except FileNotFoundError:
        print(f" Arquivo '{nome_arquivo}' não encontrado. Um novo inventário será criado.")
    except json.JSONDecodeError:
        print(f" Erro Crítico: O arquivo '{nome_arquivo}' está corrompido (JSON inválido).")
        print(" Iniciando com uma lista vazia. Salvar novos dados poderá sobrescrever o arquivo corrompido.")
    except PermissionError:
        print(f" Erro de Permissão: Sem acesso de leitura ao arquivo '{nome_arquivo}'.")
    except Exception as e:
        print(f" Erro inesperado ao tentar ler o arquivo: {e}")
        
    return ativos

def salvar_ativos(ativos, nome_arquivo):
    """Grava a lista de ativos no arquivo JSON com tratamento de exceções de I/O."""
    print("\n[Salvando alterações...]")
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(ativos, arquivo, indent=4, ensure_ascii=False)
        print(" Dados salvos com sucesso no arquivo!")
        
    except PermissionError:
        print(f" Erro de Permissão: O sistema não tem privilégios para gravar em '{nome_arquivo}'.")
    except IOError as e:
        print(f" Erro de I/O (Entrada/Saída) ao tentar salvar o arquivo: {e}")
    except Exception as e:
        print(f" Erro inesperado ao tentar salvar os dados: {e}")

def cadastrar_novo_ativo(ativos):
    """Interface para cadastro de um novo ativo na memória."""
    print("\n--- CADASTRO DE NOVO ATIVO ---")
    
    hostname = input("Hostname do ativo (ex: SRV-01): ").strip()
    ip = input("Endereço IP (ex: 192.168.1.50): ").strip()
    sistema_operacional = input("Sistema Operacional: ").strip()
    
    if not hostname or not ip:
        print(" Operação cancelada: Hostname e IP são obrigatórios.")
        return

    novo_ativo = {
        "hostname": hostname,
        "ip": ip,
        "os": sistema_operacional,
        "status": "Ativo"
    }
    
    ativos.append(novo_ativo)
    print(f" Ativo '{hostname}' inserido na memória com sucesso!")

def listar_ativos(ativos):
    """Exibe todos os ativos cadastrados."""
    print("\n--- LISTA DE ATIVOS ---")
    if not ativos:
        print("Nenhum ativo cadastrado no inventário.")
        return
        
    for i, ativo in enumerate(ativos, 1):
        print(f"{i}. Hostname: {ativo['hostname']} | IP: {ativo['ip']} | OS: {ativo['os']}")

def main():
    # Tenta carregar o inventário ao iniciar o programa
    ativos_em_memoria = carregar_ativos(ARQUIVO_INVENTARIO)
    
    while True:
        print("\n=== MENU DE INVENTÁRIO DE SEGURANÇA ===")
        print("1. Cadastrar novo ativo")
        print("2. Listar ativos cadastrados")
        print("3. Salvar e Sair")
        
        opcao = input("Escolha uma opcao (1-3): ")
        
        if opcao == '1':
            cadastrar_novo_ativo(ativos_em_memoria)
        elif opcao == '2':
            listar_ativos(ativos_em_memoria)
        elif opcao == '3':
            # Tenta salvar os dados de forma segura ao encerrar
            salvar_ativos(ativos_em_memoria, ARQUIVO_INVENTARIO)
            print(" Sistema encerrado.")
            break
        else:
            print(" Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()