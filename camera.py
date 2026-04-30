import cv2
import face_recognition
from main import FaceRecognitionVotingSystem

class CameraVotingInterface:
    def __init__(self):
        self.system = FaceRecognitionVotingSystem()
        self.camera = cv2.VideoCapture(0)
        self.running = False
    
    def start_voting_session(self):
        """Start a real-time face recognition voting session"""
        self.running = True
        
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                break
            
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find faces and encodings
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            # Process each face
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(
                    self.system.known_face_encodings,
                    face_encoding,
                    tolerance=self.system.tolerance
                )
                face_distances = face_recognition.face_distance(
                    self.system.known_face_encodings,
                    face_encoding
                )
                
                best_match_index = np.argmin(face_distances)
                name = "Unknown"
                color = (0, 0, 255)  # Red for unknown
                
                if matches[best_match_index]:
                    name = self.system.known_face_names[best_match_index]
                    color = (0, 255, 0)  # Green for recognized
                
                # Scale back up face locations
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Draw box around face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            cv2.imshow('Face Recognition Voting System', frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    interface = CameraVotingInterface()
    interface.start_voting_session()