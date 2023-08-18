import textwrap


def menu():
    menu = """\n

    Selecione uma das opções:

    **************** MENU ****************
    
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [0]\tSair

    **************************************

    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n Depósito realizado, em alguns instantes o valor estará disponível em sua conta.")
    else:
        print("\n Operação falhou! Revise o valor informado.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    
    if excedeu_saldo:
        print("\n Operação falhou! Saldo insuficiente.")

    elif excedeu_limite:
        print("\n Operação falhou! O valor do saque extrapolou o limite diário.")

    elif excedeu_saques:
        print("\n O número máximo de tentativas extrapolou, permitido apenas 03 por dia.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n Aguarde a contagem das notas e retire no local indicado.")

    else:
        print("\n Operação falhou! Valor informado nulo.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n**************** EXTRATO ****************")
    print("Não houve movimentações nesta data." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("******************************************")
    

def criar_usuario(usuarios):
    cpf = input("Digite os números do CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Usuário possui cadastro com o CPF informado!")
        return

    nome = input("Digite o nome completo (sem abreviações): ")
    data_nascimento = input("Digite a data de nascimento (seguir o modelo dd-mm-aaaa): ")
    endereco = input("Digite o endereço residencial/comercial (rua/logradouro - nro - bairro - cidade/sigla estado - CEP local - ponto de referência): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("O cadastro de usuário foi realizado em nosso sistema!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Conta gerada!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n Usuário inexistente, o fluxo para a criação de conta está finalizado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor para efetuar o depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor para efetuar o saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "6":
            criar_usuario(usuarios)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "0":
            print("Obrigado por nos escolher! Aguardamos o seu retorno!")   
            break

        else:
            print("Operação anulada, por favor selecione novamente a opção pretendida, conforme o menu disponível.")


main()