# Milestone 2: Captura de Vídeo e Detecção Facial

## 🎯 Objetivo
Visualizar o feed da webcam e confirmar que o MediaPipe está detectando e rastreando o rosto corretamente.

## 📋 Entregáveis
- [x] Acesso à webcam usando `cv2.VideoCapture()`
- [x] Loop principal do programa para ler e exibir os frames
- [x] Inicialização do modelo Face Mesh do MediaPipe
- [x] Processamento de cada frame com o Face Mesh
- [x] Desenho da malha facial 3D sobreposta no vídeo

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Testar o Ambiente
```bash
python test_milestone2.py
```

### 3. Executar o Sistema
```bash
python main.py
```

## 🎮 Controles
- **'q'**: Sair do programa
- **ESC**: Sair do programa

## 📊 Funcionalidades Implementadas

### ✅ Captura de Vídeo
- Inicialização automática da câmera
- Configuração de resolução (640x480)
- Taxa de quadros de 30 FPS

### ✅ Detecção Facial
- Modelo MediaPipe Face Mesh
- Detecção de landmarks faciais em tempo real
- Desenho da malha facial completa
- Destaque especial para íris e pupilas

### ✅ Interface Visual
- Status de detecção em tempo real
- Indicador visual "✅ Rosto Detectado" ou "❌ Nenhum Rosto Detectado"
- Informações do milestone atual
- Instruções de uso na tela

## 🔧 Estrutura do Código

### Classe `FacialRecognitionSystem`
- `__init__()`: Inicializa MediaPipe e configurações
- `initialize_camera()`: Configura e testa a câmera
- `process_frame()`: Processa frame com Face Mesh
- `run()`: Loop principal da aplicação
- `cleanup()`: Libera recursos

### Configurações do MediaPipe
```python
FaceMesh(
    static_image_mode=False,      # Modo vídeo
    max_num_faces=1,             # Máximo 1 rosto
    refine_landmarks=True,       # Landmarks refinados
    min_detection_confidence=0.5, # Confiança mínima detecção
    min_tracking_confidence=0.5   # Confiança mínima rastreamento
)
```

## 📈 Próximos Passos
- **Milestone 3**: Implementação do módulo de calibração
- Mapeamento do olhar para coordenadas da tela
- Sistema de calibração com 4 pontos

## 🐛 Solução de Problemas

### Câmera não funciona
- Verifique se a câmera está conectada
- Teste com `test_milestone2.py`
- Tente alterar o índice da câmera (0, 1, 2...)

### Erro de importação
- Execute: `pip install -r requirements.txt`
- Verifique se está no ambiente virtual correto

### Performance baixa
- Reduza a resolução da câmera
- Ajuste os parâmetros de confiança do MediaPipe

## 📝 Logs de Saída
O sistema exibe informações em tempo real:
- Status da câmera
- Status da detecção facial
- Instruções de uso
- Mensagens de erro (se houver)
