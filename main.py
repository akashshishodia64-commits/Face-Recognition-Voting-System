import cv2
import face_recognition
import numpy as np
from pathlib import Path
import pickle
import os
from datetime import datetime

class FaceRecognitionVotingSystem:
    def __init__(self, known_faces_dir='known_faces', tolerance=0.6):
        self.known_faces_dir = known_faces_dir
        self.tolerance = tolerance
        self.known_face_encodings = []
        self.known_face_names = []
        self.voters_db = {}
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load and encode known faces from the known_faces directory"""
        for person_name in os.listdir(self.known_faces_dir):
            person_dir = os.path.join(self.known_faces_dir, person_name)
            if not os.path.isdir(person_dir):
                continue
            
            for image_name in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_name)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                
                if face_encodings:
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append(person_name)
        
        print(f"Loaded {len(self.known_face_encodings)} known faces")
    
    def recognize_face(self, image_path):
        """Recognize a face from an image"""
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        results = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=self.tolerance
            )
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, 
                face_encoding
            )
            
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                confidence = 1 - face_distances[best_match_index]
                results.append({
                    'name': name,
                    'confidence': confidence,
                    'matched': True
                })
            else:
                results.append({
                    'name': 'Unknown',
                    'confidence': 0,
                    'matched': False
                })
        
        return results
    
    def register_voter(self, voter_id, name):
        """Register a new voter"""
        self.voters_db[voter_id] = {
            'name': name,
            'has_voted': False,
            'timestamp': None
        }
    
    def cast_vote(self, voter_id, vote):
        """Record a vote from a verified voter"""
        if voter_id not in self.voters_db:
            return {'success': False, 'message': 'Voter not registered'}
        
        if self.voters_db[voter_id]['has_voted']:
            return {'success': False, 'message': 'Voter has already voted'}
        
        self.voters_db[voter_id]['has_voted'] = True
        self.voters_db[voter_id]['timestamp'] = datetime.now().isoformat()
        self.voters_db[voter_id]['vote'] = vote
        
        return {'success': True, 'message': 'Vote recorded successfully'}
    
    def get_voting_status(self):
        """Get the current voting status"""
        total_registered = len(self.voters_db)
        total_voted = sum(1 for v in self.voters_db.values() if v['has_voted'])
        
        return {
            'total_registered': total_registered,
            'total_voted': total_voted,
            'turnout_percentage': (total_voted / total_registered * 100) if total_registered > 0 else 0
        }

if __name__ == '__main__':
    system = FaceRecognitionVotingSystem()
    print("Face Recognition Voting System initialized")
