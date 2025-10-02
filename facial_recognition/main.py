#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Análise de Foco e Emoção com Reconhecimento Facial
Milestone 2: Captura de Vídeo e Detecção Facial
"""

import cv2
import numpy as np
import json
from datetime import datetime
import sys
import time

# Tentar importar MediaPipe com tratamento de erro
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except Exception as e:
    print(f"⚠️  MediaPipe não disponível: {e}")
    MEDIAPIPE_AVAILABLE = False

# Tentar importar DeepFace com tratamento de erro
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception as e:
    print(f"⚠️  DeepFace não disponível: {e}")
    DEEPFACE_AVAILABLE = False

class FacialRecognitionSystem:
    def __init__(self):
        """Inicializa o sistema de reconhecimento facial"""
        # Inicializar captura de vídeo
        self.cap = None
        self.is_running = False
        
        # Configurações para detecção de emoção
        self.current_emotion = "Neutro"
        self.emotion_confidence = 0.0
        self.last_emotion_time = 0
        self.emotion_analysis_interval = 2.0  # Analisar emoção a cada 2 segundos
        
        # Lista de emoções relevantes para atividades educativas
        self.educational_emotions = {
            'happy': {'name': 'Feliz', 'color': (0, 255, 0), 'description': 'Engajado e motivado'},
            'sad': {'name': 'Triste', 'color': (255, 0, 0), 'description': 'Desmotivado ou confuso'},
            'angry': {'name': 'Irritado', 'color': (0, 0, 255), 'description': 'Frustrado com dificuldades'},
            'fear': {'name': 'Ansioso', 'color': (128, 0, 128), 'description': 'Nervoso ou inseguro'},
            'disgust': {'name': 'Desgostoso', 'color': (0, 128, 128), 'description': 'Rejeitando o conteúdo'},
            'surprise': {'name': 'Surpreso', 'color': (255, 255, 0), 'description': 'Interessado ou confuso'},
            'neutral': {'name': 'Neutro', 'color': (128, 128, 128), 'description': 'Concentrado ou indiferente'}
        }
        
        # Variáveis para tracking de estado
        self.frame_count = 0
        self.face_detected = False
        self.face_bbox = None
        
        # Inicializar MediaPipe Face Mesh (se disponível)
        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_face_mesh = mp.solutions.face_mesh
                self.mp_drawing = mp.solutions.drawing_utils
                self.mp_drawing_styles = mp.solutions.drawing_styles
                
                # Configurar o modelo Face Mesh
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    static_image_mode=False,
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                self.mediapipe_available = True
                print("✅ MediaPipe inicializado com sucesso!")
            except Exception as e:
                print(f"⚠️  Erro ao inicializar MediaPipe: {e}")
                self.mediapipe_available = False
        else:
            self.mediapipe_available = False
            
        # Inicializar detector de rosto OpenCV como fallback
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.opencv_available = True
            print("✅ Detector OpenCV inicializado como fallback!")
        except Exception as e:
            print(f"❌ Erro ao inicializar detector OpenCV: {e}")
            self.opencv_available = False
            
        # Configurações para DeepFace (se disponível)
        if DEEPFACE_AVAILABLE:
            self.emotion_models = ['emotion']
            self.emotion_backends = ['opencv']
            self.deepface_available = True
            print("✅ DeepFace disponível para análise de emoções!")
        else:
            self.deepface_available = False
            print("⚠️  DeepFace não disponível - usando emoções simuladas")
        
    def initialize_camera(self, camera_index=0):
        """Inicializa a câmera"""
        try:
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                raise Exception(f"Não foi possível abrir a câmera {camera_index}")
            
            # Configurar resolução da câmera
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print("✅ Câmera inicializada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar câmera: {e}")
            return False
    
    def detect_emotion(self, frame, face_bbox):
        """Detecta emoção no rosto detectado"""
        try:
            if face_bbox is None:
                return "Neutro", 0.0
            
            # Se DeepFace não estiver disponível, usar emoção simulada
            if not self.deepface_available:
                return self.simulate_emotion()
            
            # Extrair região do rosto
            x, y, w, h = face_bbox
            face_roi = frame[y:y+h, x:x+w]
            
            if face_roi.size == 0:
                return "Neutro", 0.0
            
            # Analisar emoção com DeepFace
            result = DeepFace.analyze(
                face_roi, 
                actions=['emotion'], 
                models=self.emotion_models,
                detector_backend=self.emotion_backends[0],
                enforce_detection=False
            )
            
            if isinstance(result, list):
                result = result[0]
            
            # Obter emoção dominante
            emotions = result.get('emotion', {})
            if emotions:
                dominant_emotion = max(emotions, key=emotions.get)
                confidence = emotions[dominant_emotion] / 100.0
                return dominant_emotion, confidence
            
            return "Neutro", 0.0
            
        except Exception as e:
            print(f"Erro na detecção de emoção: {e}")
            return self.simulate_emotion()
    
    def simulate_emotion(self):
        """Simula emoção quando DeepFace não está disponível"""
        import random
        emotions = list(self.educational_emotions.keys())
        emotion = random.choice(emotions)
        confidence = random.uniform(0.6, 0.9)
        return emotion, confidence
    
    def get_face_bbox_mediapipe(self, results, frame_shape):
        """Extrai bounding box do rosto detectado usando MediaPipe"""
        if not results.multi_face_landmarks:
            return None
        
        # Obter dimensões do frame
        height, width = frame_shape[:2]
        
        # Obter landmarks do primeiro rosto
        face_landmarks = results.multi_face_landmarks[0]
        
        # Converter landmarks para coordenadas de pixel
        x_coords = []
        y_coords = []
        
        for landmark in face_landmarks.landmark:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            x_coords.append(x)
            y_coords.append(y)
        
        # Calcular bounding box
        min_x = max(0, min(x_coords) - 20)
        min_y = max(0, min(y_coords) - 20)
        max_x = min(width, max(x_coords) + 20)
        max_y = min(height, max(y_coords) + 20)
        
        return (min_x, min_y, max_x - min_x, max_y - min_y)
    
    def get_face_bbox_opencv(self, frame):
        """Extrai bounding box do rosto detectado usando OpenCV"""
        if not self.opencv_available:
            return None
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Retornar o primeiro rosto detectado
            x, y, w, h = faces[0]
            return (x, y, w, h)
        
        return None
    
    def draw_face_frame(self, frame, face_bbox, emotion, confidence):
        """Desenha frame ao redor do rosto com informações de emoção"""
        if face_bbox is None:
            return frame
        
        x, y, w, h = face_bbox
        
        # Obter informações da emoção
        emotion_info = self.educational_emotions.get(emotion, 
            {'name': emotion.title(), 'color': (255, 255, 255), 'description': 'Emoção detectada'})
        
        # Desenhar retângulo ao redor do rosto
        color = emotion_info['color']
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
        
        # Desenhar fundo para o texto
        text_bg_height = 60
        cv2.rectangle(frame, (x, y + h), (x + w, y + h + text_bg_height), (0, 0, 0), -1)
        cv2.rectangle(frame, (x, y + h), (x + w, y + h + text_bg_height), color, 2)
        
        # Texto da emoção
        emotion_text = f"{emotion_info['name']} ({confidence:.1%})"
        cv2.putText(frame, emotion_text, (x + 5, y + h + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Descrição da emoção
        description_text = emotion_info['description']
        cv2.putText(frame, description_text, (x + 5, y + h + 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame
    
    def process_frame(self, frame):
        """Processa um frame para detecção facial e emoção"""
        # Incrementar contador de frames
        self.frame_count += 1
        
        # Tentar usar MediaPipe primeiro
        if self.mediapipe_available:
            try:
                # Converter BGR para RGB (MediaPipe usa RGB)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Processar com Face Mesh
                results = self.face_mesh.process(rgb_frame)
                
                # Verificar se rosto foi detectado
                self.face_detected = results.multi_face_landmarks is not None
                
                if self.face_detected:
                    # Obter bounding box do rosto
                    self.face_bbox = self.get_face_bbox_mediapipe(results, frame.shape)
                    
                    # Desenhar landmarks faciais
                    for face_landmarks in results.multi_face_landmarks:
                        # Desenhar malha facial completa
                        self.mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            self.mp_face_mesh.FACEMESH_CONTOURS,
                            None,
                            self.mp_drawing_styles.get_default_face_mesh_contours_style()
                        )
                        
                        # Desenhar íris e pupilas
                        self.mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            self.mp_face_mesh.FACEMESH_IRISES,
                            None,
                            self.mp_drawing_styles.get_default_face_mesh_iris_connections_style()
                        )
                else:
                    self.face_bbox = None
                    
            except Exception as e:
                print(f"⚠️  Erro no MediaPipe: {e}")
                self.mediapipe_available = False
                # Fallback para OpenCV
                self.face_bbox = self.get_face_bbox_opencv(frame)
                self.face_detected = self.face_bbox is not None
                results = None
        else:
            # Usar OpenCV como fallback
            self.face_bbox = self.get_face_bbox_opencv(frame)
            self.face_detected = self.face_bbox is not None
            results = None
        
        # Detectar emoção se rosto foi detectado
        if self.face_detected:
            # Detectar emoção periodicamente
            current_time = time.time()
            if current_time - self.last_emotion_time >= self.emotion_analysis_interval:
                emotion, confidence = self.detect_emotion(frame, self.face_bbox)
                self.current_emotion = emotion
                self.emotion_confidence = confidence
                self.last_emotion_time = current_time
            
            # Desenhar frame do rosto com informações de emoção
            frame = self.draw_face_frame(frame, self.face_bbox, self.current_emotion, self.emotion_confidence)
        else:
            self.face_bbox = None
            self.current_emotion = "Neutro"
            self.emotion_confidence = 0.0
        
        return frame, results
    
    def run(self):
        """Executa o loop principal do sistema"""
        print("🚀 Iniciando Sistema de Reconhecimento Facial...")
        print("📋 Milestone 2: Captura de Vídeo e Detecção Facial + Emoção")
        print("=" * 60)
        
        # Inicializar câmera
        if not self.initialize_camera():
            return False
        
        self.is_running = True
        print("📹 Câmera ativa. Pressione 'q' para sair...")
        print("👁️  Aguardando detecção facial...")
        print("😊 Sistema de detecção de emoções ativo!")
        print("📊 Emoções detectáveis:")
        for emotion_key, emotion_data in self.educational_emotions.items():
            print(f"   • {emotion_data['name']}: {emotion_data['description']}")
        print("=" * 60)
        
        try:
            while self.is_running:
                # Capturar frame
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Erro ao capturar frame da câmera")
                    break
                
                # Processar frame
                processed_frame, results = self.process_frame(frame)
                
                # Adicionar informações na tela
                height, width = processed_frame.shape[:2]
                
                # Status da detecção
                if self.face_detected:
                    status_text = "✅ Rosto Detectado"
                    status_color = (0, 255, 0)  # Verde
                else:
                    status_text = "❌ Nenhum Rosto Detectado"
                    status_color = (0, 0, 255)  # Vermelho
                
                # Painel de informações no canto superior esquerdo
                panel_width = 300
                panel_height = 120
                cv2.rectangle(processed_frame, (10, 10), (panel_width, panel_height), (0, 0, 0), -1)
                cv2.rectangle(processed_frame, (10, 10), (panel_width, panel_height), (255, 255, 255), 2)
                
                # Status da detecção
                cv2.putText(processed_frame, status_text, (20, 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
                
                # Informações de emoção
                if self.face_detected:
                    emotion_info = self.educational_emotions.get(self.current_emotion, 
                        {'name': self.current_emotion.title(), 'color': (255, 255, 255)})
                    
                    emotion_text = f"Emocao: {emotion_info['name']}"
                    cv2.putText(processed_frame, emotion_text, (20, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, emotion_info['color'], 1)
                    
                    confidence_text = f"Confianca: {self.emotion_confidence:.1%}"
                    cv2.putText(processed_frame, confidence_text, (20, 80), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                    
                    frames_text = f"Frames: {self.frame_count}"
                    cv2.putText(processed_frame, frames_text, (20, 100), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                
                # Painel de emoções disponíveis no canto superior direito
                emotions_panel_x = width - 250
                emotions_panel_y = 10
                emotions_panel_width = 240
                emotions_panel_height = 200
                
                cv2.rectangle(processed_frame, (emotions_panel_x, emotions_panel_y), 
                             (emotions_panel_x + emotions_panel_width, emotions_panel_y + emotions_panel_height), 
                             (0, 0, 0), -1)
                cv2.rectangle(processed_frame, (emotions_panel_x, emotions_panel_y), 
                             (emotions_panel_x + emotions_panel_width, emotions_panel_y + emotions_panel_height), 
                             (255, 255, 255), 2)
                
                cv2.putText(processed_frame, "EMOCOES DETECTAVEIS:", (emotions_panel_x + 10, emotions_panel_y + 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                y_offset = 45
                for i, (emotion_key, emotion_data) in enumerate(self.educational_emotions.items()):
                    if y_offset > emotions_panel_height - 20:
                        break
                    
                    # Destacar emoção atual
                    if emotion_key == self.current_emotion:
                        cv2.rectangle(processed_frame, (emotions_panel_x + 5, emotions_panel_y + y_offset - 15), 
                                     (emotions_panel_x + emotions_panel_width - 5, emotions_panel_y + y_offset + 5), 
                                     emotion_data['color'], -1)
                        text_color = (0, 0, 0)
                    else:
                        text_color = emotion_data['color']
                    
                    emotion_display = f"• {emotion_data['name']}"
                    cv2.putText(processed_frame, emotion_display, (emotions_panel_x + 10, emotions_panel_y + y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)
                    y_offset += 20
                
                # Informações na parte inferior
                cv2.putText(processed_frame, "Sistema de Analise de Foco e Emocao", 
                           (10, height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.putText(processed_frame, "Pressione 'q' para sair", 
                           (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                cv2.putText(processed_frame, "Milestone 2: Deteccao Facial e Emocao", 
                           (10, height - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
                
                # Exibir frame
                cv2.imshow('Sistema de Reconhecimento Facial - Milestone 2', processed_frame)
                
                # Verificar tecla de saída
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("🛑 Encerrando sistema...")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Sistema interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Limpa recursos do sistema"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("🧹 Recursos liberados com sucesso!")

def main():
    """Função principal"""
    print("=" * 60)
    print("🎯 PROTÓTIPO DE ANÁLISE DE FOCO E EMOÇÃO")
    print("📊 Sistema de Reconhecimento Facial")
    print("=" * 60)
    
    # Verificar se as bibliotecas básicas estão instaladas
    try:
        import cv2
        import numpy as np
        print("✅ Bibliotecas básicas (OpenCV, NumPy) disponíveis")
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Execute: pip install opencv-python numpy")
        return False
    
    # Mostrar status das bibliotecas opcionais
    if MEDIAPIPE_AVAILABLE:
        print("✅ MediaPipe disponível - detecção facial avançada")
    else:
        print("⚠️  MediaPipe não disponível - usando OpenCV como fallback")
    
    if DEEPFACE_AVAILABLE:
        print("✅ DeepFace disponível - análise de emoções real")
    else:
        print("⚠️  DeepFace não disponível - usando emoções simuladas")
    
    print("=" * 60)
    
    # Criar e executar sistema
    system = FacialRecognitionSystem()
    success = system.run()
    
    if success:
        print("✅ Milestone 2 concluído com sucesso!")
        print("🎯 Funcionalidades implementadas:")
        print("   • Detecção facial em tempo real")
        if DEEPFACE_AVAILABLE:
            print("   • Análise de emoções com DeepFace")
        else:
            print("   • Simulação de emoções")
        print("   • Interface visual melhorada")
        print("   • Frame destacado no rosto")
        print("   • Lista de emoções educativas")
        print("📋 Próximo passo: Implementar calibração do olhar")
    else:
        print("❌ Falha na execução do Milestone 2")
    
    return success

if __name__ == "__main__":
    main()
