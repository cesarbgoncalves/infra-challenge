import os
import threading
import yaml
from time import sleep

threads = []

def limpa_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def build_application(app, version):
    threads.append(app)
    print(f"Construindo a imagem: {app}")
    os.system(f"docker build -t cesarbgoncalves/infra-challenge:{version} .")
    os.system(f"docker push cesarbgoncalves/infra-challenge:{version}")
    print(f"Aplicação {app} construida com sucesso!")
    threads.remove(app)
    

def docker_compose_up():
    print("Iniciando Docker Compose...")
    os.popen("docker-compose -f docker-compose/docker-compose.yaml up -d").read()
    print("Docker Compose iniciado com sucesso!")
    
    
def build_and_deploy(app, version):
    print(f" Atualizando para a versão {version}")
    threading.Thread(target=build_application, args=(app, version)).start()

def remove_remaining_containers():
    print("Parando os containers em execução...")
    os.system("docker-compose -f docker-compose/docker-compose.yaml down")
    containers = os.popen('docker ps -aq').read().split('\n')
    containers.remove('')
    if len(containers) > 0:
        print(f"There are still {containers} containers created")
        for container in containers:
            print(f"Stopping container {container}")
            os.system(f"docker container stop {container}")
        os.system("docker container prune -f")

def kubernetes_deploy(version):
    print("\nIniciando o deploy do banco de dados...\n")
    os.system("kubectl -n infra-challenge apply -f kubernetes/bd/")
    sleep(8)
    os.system("kubectl -n infra-challenge get pods")
    
    sleep(15)
    
    print(f"\nIniciando o deploy da aplicação, na versão {version}...\n")
    os.system("kubectl -n infra-challenge apply -f kubernetes/app/")
    sleep(8)
    os.system("kubectl -n infra-challenge get pods")
    
def get_current_version():
    with open("kubernetes/app/deployment.yaml", "r") as f:
        versao = f.readlines()
        for line in versao:
            if "image: cesarbgoncalves/infra-challenge:" in line:
                return line.split(":")[2].strip()

def get_version():
    current_version = get_current_version()
    version = input(f"Informe a versão da Imagem ou [M] para manter a atual({current_version}): ")
    if version.upper() == "M":
        return current_version
    else:
        print(f"Alterando a versão da aplicação de: {current_version} para {version}...")
        update_version(version)
        return version


def update_version(version):
    with open("kubernetes/app/deployment.yaml", 'r') as file:
        manifest = yaml.safe_load(file)

    # Percorre todas as definições de containers e atualiza a versão da imagem
    for container in manifest['spec']['template']['spec']['containers']:
        image_name, current_version = container['image'].rsplit(':', 1)
        print(f"Imagem atual: {image_name}: {current_version}")
        container['image'] = f"{image_name}:{version}"
        print(f"Imagem atualizada: {container['image']}")
    # Salva o manifesto atualizado
    with open("kubernetes/app/deployment.yaml", 'w') as file:
        yaml.dump(manifest, file, default_flow_style=False)
        print(f"Manifesto salvo com a nova versão da imagem: {version}")


if __name__ == "__main__":
    while True:
        limpa_tela()
        opcao = input("\nDeseja realizar o deploy em:\n \n[K]ubernetes ou no \n[D]ocker? \n\nPara Sair, pressione [S]\n")
        if opcao.upper() == "S":
            print("Saindo...")
            sleep(1)
            break

        elif opcao.upper() == "K":
            version = get_version()
            build_and_deploy("infra_challenge", version)
            print(f"\nDeploy no Kubernetes na versão {version}...\n")
            kubernetes_deploy(version)
            print("\nDeploy no Kubernetes concluído com sucesso!\n")
            break

        elif opcao.upper() == "D":
            version = get_version()
            build_and_deploy("infra_challenge", version=version)
            while len(threads) > 0:
                pass
            remove_remaining_containers()
            threading.Thread(target=docker_compose_up).start()
            os.system("docker ps")
            print("\nDeploy no Docker concluído com sucesso!\n")
            break
        else:
            print("Opção inválida!")
            sleep(1)
            limpa_tela()
        
    
    
    
    