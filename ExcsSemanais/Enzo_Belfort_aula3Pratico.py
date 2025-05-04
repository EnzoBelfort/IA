import random

def criar_mapa():
    mapa = [['.' for _ in range(4)] for _ in range(4)]
    
    mapa[0][0] = "A"  
    
    linha_wumpus = random.randint(0, 3)
    coluna_wumpus = random.randint(0, 3)
    while linha_wumpus == 0 and coluna_wumpus == 0:
        linha_wumpus = random.randint(0, 3)
        coluna_wumpus = random.randint(0, 3)
    mapa[linha_wumpus][coluna_wumpus] = "W"  
    
    for _ in range(3):
        linha_buraco = random.randint(0, 3)
        coluna_buraco = random.randint(0, 3)
        while (linha_buraco == 0 and coluna_buraco == 0) or \
              mapa[linha_buraco][coluna_buraco] != '.':
            linha_buraco = random.randint(0, 3)
            coluna_buraco = random.randint(0, 3)
        mapa[linha_buraco][coluna_buraco] = "B"  
    
    linha_ouro = random.randint(0, 3)
    coluna_ouro = random.randint(0, 3)
    while (linha_ouro == 0 and coluna_ouro == 0) or \
          mapa[linha_ouro][coluna_ouro] != '.':
        linha_ouro = random.randint(0, 3)
        coluna_ouro = random.randint(0, 3)
    mapa[linha_ouro][coluna_ouro] = "O" 
    
    return mapa

def marcar_percepcoes(mapa):
    percepcoes = [[[] for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            if mapa[i][j] == "W":
                for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 4 and 0 <= nj < 4:
                        percepcoes[ni][nj].append("fedor")
            
            elif mapa[i][j] == "B":
                for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 4 and 0 <= nj < 4:
                        percepcoes[ni][nj].append("brisa")
            
            elif mapa[i][j] == "O":
                percepcoes[i][j].append("brilho")
    
    return percepcoes

def exibir_mapa_debug(mapa):
    """Exibe o mapa completo para debug"""
    print("\n----- MAPA DEBUG -----")
    for linha in mapa:
        print(' '.join(linha))
    print("---------------------\n")

def exibir_mapa_jogador(mapa, percepcoes, pos_jogador, visitadas):
    """Exibe o mapa como o jogador vê - apenas células visitadas"""
    print("\n----- MAPA VISÍVEL -----")
    for i in range(4):
        linha = []
        for j in range(4):
            if (i, j) in visitadas:
                if (i, j) == pos_jogador:
                    linha.append('A')
                else:
                    celula = mapa[i][j]
                    
                    if celula == 'W' or celula == 'B':
                        linha.append('.')
                    else:
                        linha.append(celula)
            else:
                linha.append('?')
        print(' '.join(linha))
    print("------------------------\n")

def iniciar_jogo():
    mapa = criar_mapa()
    percepcoes = marcar_percepcoes(mapa)
    
  
    pos_jogador = (0, 0)  
    direcao_jogador = 'leste' 
    flecha = True  
    ouro_coletado = False
    pontuacao = 0
    movimento_count = 0
    wumpus_vivo = True
    jogo_ativo = True
    visitadas = {pos_jogador}  
    
    print("Bem-vindo ao Mundo de Wumpus!")
    print("Comandos disponíveis: 'cima', 'baixo', 'dir', 'esq', 'atirar', 'pegar', 'escalar', 'sair'")
    

    while jogo_ativo:
        i, j = pos_jogador
        percepcoes_atuais = percepcoes[i][j]
        
        mensagem = f"Você está na posição [{i+1},{j+1}] olhando para {direcao_jogador}"
        
        if percepcoes_atuais:
            mensagem += " e percebe: " + ", ".join(percepcoes_atuais)
        else:
            mensagem += " e não percebe nada"
        
        print(mensagem)
        exibir_mapa_jogador(mapa, percepcoes, pos_jogador, visitadas)
        
        if mapa[i][j] == "W" and wumpus_vivo:
            print("Você encontrou o Wumpus e foi devorado! Fim de jogo.")
            pontuacao -= 100
            jogo_ativo = False
            break
        
        if mapa[i][j] == "B":
            print("Você caiu em um buraco! Fim de jogo.")
            pontuacao -= 100
            jogo_ativo = False
            break
        
        movimento = input("O que você quer fazer? ").strip().lower()
        movimento_count += 1
        
        if movimento == "sair":
            print("Jogo encerrado.")
            jogo_ativo = False
        
        elif movimento == "cima":
            nova_pos = None
            if direcao_jogador == 'norte' and i > 0:
                nova_pos = (i-1, j)
            elif direcao_jogador == 'sul' and i < 3:
                nova_pos = (i+1, j)
            elif direcao_jogador == 'leste' and j < 3:
                nova_pos = (i, j+1)
            elif direcao_jogador == 'oeste' and j > 0:
                nova_pos = (i, j-1)
                
            if nova_pos:
                pos_jogador = nova_pos
                visitadas.add(pos_jogador)
            else:
                print("Você bateu na parede!")
        
        elif movimento == "dir":
            if direcao_jogador == 'norte':
                direcao_jogador = 'leste'
            elif direcao_jogador == 'leste':
                direcao_jogador = 'sul'
            elif direcao_jogador == 'sul':
                direcao_jogador = 'oeste'
            elif direcao_jogador == 'oeste':
                direcao_jogador = 'norte'
            print(f"Virou para {direcao_jogador}.")
            
        elif movimento == "esq":
            if direcao_jogador == 'norte':
                direcao_jogador = 'oeste'
            elif direcao_jogador == 'oeste':
                direcao_jogador = 'sul'
            elif direcao_jogador == 'sul':
                direcao_jogador = 'leste'
            elif direcao_jogador == 'leste':
                direcao_jogador = 'norte'
            print(f"Virou para {direcao_jogador}.")
            
        elif movimento == "atirar":
            if flecha and wumpus_vivo:
                acertou = False
                if direcao_jogador == 'norte':
                    for ni in range(i-1, -1, -1):
                        if mapa[ni][j] == 'W':
                            acertou = True
                elif direcao_jogador == 'sul':
                    for ni in range(i+1, 4):
                        if mapa[ni][j] == 'W':
                            acertou = True
                elif direcao_jogador == 'leste':
                    for nj in range(j+1, 4):
                        if mapa[i][nj] == 'W':
                            acertou = True
                elif direcao_jogador == 'oeste':
                    for nj in range(j-1, -1, -1):
                        if mapa[i][nj] == 'W':
                            acertou = True
                
                flecha = False
                if acertou:
                    print("O Wumpus é morto e solta um grito. Você recebeu 50 pontos!")
                    wumpus_vivo = False
                    pontuacao += 50
                else:
                    print("A flecha não acertou nada!")
            else:
                if not flecha:
                    print("Você já usou sua flecha!")
                else:
                    print("O Wumpus já está morto!")
                    
        elif movimento == "pegar":
            if mapa[i][j] == "O":
                print("Você pegou o ouro!")
                mapa[i][j] = "."
                ouro_coletado = True
            else:
                print("Não há nada para pegar aqui.")
                
        elif movimento == "escalar":
            if pos_jogador == (0, 0):
                if ouro_coletado:
                    print("Parabéns! Você escapou com o ouro!")
                    pontuacao += 50  
                    pontuacao -= (movimento_count - 1)  
                    jogo_ativo = False
                else:
                    print("Você precisa pegar o ouro antes de escapar!")
            else:
                print("Você só pode escalar na entrada da caverna [1,1].")
                
        else:
            print("Comando não reconhecido.")
            movimento_count -= 1  
    
    print(f"Pontuação final: {pontuacao}")

def main():
    iniciar_jogo()

if __name__ == "__main__":
    main()