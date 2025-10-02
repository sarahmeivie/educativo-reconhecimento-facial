Plano de Projeto: Protótipo de Análise de Foco e Emoção com Relatório Final
Versão: 1.0
Data: 2 de Outubro de 2025
Tempo de Desenvolvimento Estimado: 8 horas

1. Resumo do Projeto
Este documento detalha o plano de implementação para o desenvolvimento de um protótipo funcional em Python. O sistema utilizará uma webcam para analisar o comportamento de um usuário em tempo real, focando em duas métricas principais: atenção (foco visual) e expressão facial (emoção). Ao final de cada sessão, um relatório detalhado em formato JSON será gerado com os timestamps de cada evento detectado.

2. Objetivo Final
Ao final das 8 horas de desenvolvimento, o entregável será um único script Python (main.py) que:

Inicia a webcam e executa um processo de calibração para mapear o olhar do usuário na tela.

Exibe uma Área de Interesse (ROI) que simula uma atividade.

Monitora e exibe em tempo real o status de "Focado" ou "Distraído".

Monitora e exibe em tempo real a emoção dominante do usuário.

Ao encerrar a aplicação, salva automaticamente um arquivo relatorio_atividade.json com o registro cronológico de todos os eventos de foco e emoção.

3. Requisitos e Ferramentas
Hardware: Uma webcam funcional.

Software:

Python 3.8 ou superior.

As seguintes bibliotecas Python, que devem ser instaladas previamente:

Bash

pip install opencv-python mediapipe numpy deepface
4. Estrutura do Projeto

Módulo de Visão: Responsável pela captura da câmera e detecção de landmarks faciais (MediaPipe).

Módulo de Calibração: Lógica para mapear o olhar do usuário às coordenadas da tela.

Módulo de Análise: Lógica principal que determina o status de foco e emoção.

Módulo de Registro e Relatório: Responsável por registrar eventos e gerar o arquivo JSON final.

5. Plano de Implementação Detalhado (Cronograma de 8 Horas)
Milestone 1: Configuração do Ambiente e Estrutura Básica (Cronograma: Hora 0 - 1)
Objetivo do Bloco: Preparar todo o ambiente de desenvolvimento e garantir que as bibliotecas estão funcionando.

Sequência de Desenvolvimento:

Criar a pasta do projeto e o arquivo main.py.

Instalar as dependências listadas na seção 3.

Escrever o código inicial em main.py para importar as bibliotecas e confirmar que não há erros.

Entregável: Um ambiente de desenvolvimento pronto e um script que executa sem erros de importação.

Milestone 2: Captura de Vídeo e Detecção Facial (Cronograma: Hora 1 - 2.5)
Objetivo do Bloco: Visualizar o feed da webcam e confirmar que o MediaPipe está detectando e rastreando o rosto corretamente.

Sequência de Desenvolvimento:

Implementar o acesso à webcam usando cv2.VideoCapture().

Criar o loop principal do programa para ler e exibir os frames.

Inicializar o modelo Face Mesh do MediaPipe.

Dentro do loop, processar cada frame com o Face Mesh.

Utilizar as funções de desenho do MediaPipe para sobrepor a malha facial no vídeo.

Entregável: Uma janela de aplicação que exibe o vídeo da webcam com a malha facial 3D sobreposta em tempo real.

Milestone 3: Implementação do Módulo de Calibração (Cronograma: Hora 2.5 - 5)
Objetivo do Bloco: Criar a lógica que "ensina" o programa a correlacionar a posição do rosto/olhar do usuário com as coordenadas da tela. Esta é a etapa mais crítica.

Sequência de Desenvolvimento:

Criar um "modo de calibração" que é executado no início do programa.

Desenhar 4 alvos visuais nos cantos da tela.

Programar a lógica para que, a cada vez que o usuário olhe para um alvo e pressione uma tecla, o sistema capture as coordenadas de landmarks faciais chave (ex: ponta do nariz, cantos dos olhos).

Armazenar os 4 conjuntos de pontos da tela e os 4 conjuntos de pontos faciais correspondentes.

Calcular a matriz de transformação perspectiva usando cv2.getPerspectiveTransform().

Entregável: Uma matriz_transformacao que mapeia o espaço facial para o espaço da tela.

Milestone 4: Análise de Foco e Início do Registro (Cronograma: Hora 5 - 6.5)
Objetivo do Bloco: Utilizar a matriz de calibração para determinar o foco do usuário em tempo real e começar a registrar os eventos.

Sequência de Desenvolvimento:

Inicializar as variáveis de estado e tempo (usando datetime) antes do loop principal para o log de eventos.

No modo de operação normal (pós-calibração), desenhar um retângulo na tela para servir como a Área de Interesse (ROI).

A cada frame, extrair o ponto de referência do olhar e aplicar a matriz_transformacao com cv2.perspectiveTransform().

Verificar se o ponto resultante está dentro da ROI para definir o estado_foco_atual.

Implementar a lógica de detecção de mudança de estado de foco para registrar o início e o fim de cada período de "Focado" e "Distraído" na lista log_eventos.

Entregável: A aplicação exibe o status de foco em tempo real e a lista log_eventos é preenchida com os dados de foco.

Milestone 5: Integração da Análise de Emoção e Registro (Cronograma: Hora 6.5 - 7.5)
Objetivo do Bloco: Adicionar a camada de análise de emoção, mantendo a performance do sistema.

Sequência de Desenvolvimento:

Adicionar um contador de frames ao loop principal.

Implementar uma condição para executar a análise de emoção com DeepFace.analyze() apenas periodicamente (ex: a cada 60 frames), para não sobrecarregar o processador.

Envolver a chamada do DeepFace em um bloco try-except para lidar com frames onde nenhum rosto é encontrado.

Aplicar a mesma lógica de detecção de mudança de estado para as emoções, registrando o início e o fim de cada período emocional ("happy", "sad", "neutral", etc.) na lista log_eventos.

Entregável: A aplicação exibe foco e emoção em tempo real. A lista log_eventos agora contém ambos os tipos de evento.

Milestone 6: Geração e Salvamento do Relatório Final (Cronograma: Hora 7.5 - 8)
Objetivo do Bloco: Finalizar a sessão de análise e salvar todos os dados coletados em um formato estruturado.

Sequência de Desenvolvimento:

Implementar o código que será executado após o encerramento do loop principal (quando o usuário pressionar 'q').

Adicionar os últimos eventos em andamento à lista de log, usando o momento de encerramento como timestamp final.

Estruturar um dicionário Python final contendo metadados da sessão (início, fim, duração) e a lista completa de eventos.

Utilizar a biblioteca json para exportar este dicionário para o arquivo relatorio_atividade.json.

Entregável: Um arquivo JSON é gerado ao final da execução com todos os dados da sessão.

6. O Produto Final
Ao concluir este plano, você terá um protótipo robusto e uma ferramenta de coleta de dados. O arquivo relatorio_atividade.json gerado terá uma estrutura similar a esta:

JSON

{
    "inicio_atividade": "2025-10-02T17:47:59.123456",
    "fim_atividade": "2025-10-02T17:49:30.654321",
    "duracao_total_segundos": 91.53,
    "eventos": [
        {
            "tipo": "foco",
            "status": "Focado",
            "inicio": "2025-10-02T17:47:59.123456",
            "fim": "2025-10-02T17:48:15.789012"
        },
        {
            "tipo": "emocao",
            "status": "neutral",
            "inicio": "2025-10-02T17:47:59.123456",
            "fim": "2025-10-02T17:48:20.111222"
        },
        {
            "tipo": "foco",
            "status": "Distraido",
            "inicio": "2025-10-02T17:48:15.789012",
            "fim": "2025-10-02T17:48:40.456789"
        },
        {
            "tipo": "emocao",
            "status": "happy",
            "inicio": "2025-10-02T17:48:20.111222",
            "fim": "2025-10-02T17:49:30.654321"
        },
        {
            "tipo": "foco",
            "status": "Focado",
            "inicio": "2025-10-02T17:48:40.456789",
            "fim": "2025-10-02T17:49:30.654321"
        }
    ]
}