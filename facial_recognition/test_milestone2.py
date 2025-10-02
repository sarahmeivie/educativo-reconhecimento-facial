#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o Milestone 2
Verifica se todas as dependências estão instaladas e funcionando
"""

def test_imports():
    """Testa se todas as bibliotecas podem ser importadas"""
    print("🔍 Testando importações...")
    
    try:
        import cv2
        print(f"✅ OpenCV versão: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ Erro ao importar OpenCV: {e}")
        return False
    
    try:
        import mediapipe as mp
        print(f"✅ MediaPipe versão: {mp.__version__}")
    except ImportError as e:
        print(f"❌ Erro ao importar MediaPipe: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy versão: {np.__version__}")
    except ImportError as e:
        print(f"❌ Erro ao importar NumPy: {e}")
        return False
    
    try:
        import deepface
        print(f"✅ DeepFace versão: {deepface.__version__}")
    except ImportError as e:
        print(f"❌ Erro ao importar DeepFace: {e}")
        return False
    
    return True

def test_camera():
    """Testa se a câmera está disponível"""
    print("\n📹 Testando câmera...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Câmera não disponível")
            return False
        
        # Tentar capturar um frame
        ret, frame = cap.read()
        if not ret:
            print("❌ Não foi possível capturar frame da câmera")
            cap.release()
            return False
        
        print(f"✅ Câmera funcionando - Resolução: {frame.shape[1]}x{frame.shape[0]}")
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar câmera: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE DO MILESTONE 2")
    print("=" * 60)
    
    # Testar importações
    imports_ok = test_imports()
    
    # Testar câmera
    camera_ok = test_camera()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DOS TESTES")
    print("=" * 60)
    
    if imports_ok and camera_ok:
        print("✅ Todos os testes passaram!")
        print("🚀 Você pode executar: python main.py")
        return True
    else:
        print("❌ Alguns testes falharam")
        if not imports_ok:
            print("💡 Execute: pip install -r requirements.txt")
        if not camera_ok:
            print("💡 Verifique se sua câmera está conectada e funcionando")
        return False

if __name__ == "__main__":
    main()
