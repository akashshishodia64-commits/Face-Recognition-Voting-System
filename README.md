# Face Recognition Voting System

A Python-based voting system that uses facial recognition technology to verify voter identity and prevent duplicate voting.

## Features

- **Face Recognition**: Uses advanced face recognition to identify registered voters
- **Real-time Processing**: Live camera feed processing for immediate voter verification
- **Duplicate Vote Prevention**: Ensures each voter can only vote once
- **Voter Registration**: Register voters with their facial data
- **Voting Status Tracking**: Monitor voting progress and turnout

## Requirements

- Python 3.7+
- OpenCV
- face-recognition library
- numpy
- Pillow
- Flask (optional, for web interface)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/akashshishodia64-commits/face-recognition-voting-system.git
cd face-recognition-voting-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Prepare known faces directory:
```bash
mkdir known_faces
# Add subdirectories for each voter with their face images
# Structure: known_faces/voter_name/image1.jpg
```

## Usage

### Initialize the System

```python
from main import FaceRecognitionVotingSystem

system = FaceRecognitionVotingSystem()
```

### Start Camera Interface

```bash
python camera.py
```

This will open a live camera feed showing face recognition in real-time.

### Recognize a Face

```python
results = system.recognize_face('path/to/image.jpg')
print(results)
```

### Register a Voter

```python
system.register_voter('voter_001', 'John Doe')
```

### Cast a Vote

```python
result = system.cast_vote('voter_001', 'Candidate A')
print(result)
```

### Check Voting Status

```python
status = system.get_voting_status()
print(status)
```

## Project Structure

```
face-recognition-voting-system/
├── main.py              # Core voting system logic
├── camera.py            # Real-time camera interface
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
├── known_faces/        # Directory for storing known faces
│   ├── voter_1/
│   ├── voter_2/
│   └── ...
└── .gitignore          # Git ignore rules
```

## Configuration

### Tolerance Setting

Adjust the tolerance parameter in `FaceRecognitionVotingSystem` to control matching sensitivity:
- Lower values (0.3-0.5): Stricter matching
- Higher values (0.6-0.8): More lenient matching

```python
system = FaceRecognitionVotingSystem(tolerance=0.6)
```

## Security Considerations

- Store voter faces securely
- Implement encryption for vote records
- Use unique voter IDs
- Audit all voting transactions
- Implement backup systems

## Future Enhancements

- [ ] Flask web interface
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Multi-face recognition
- [ ] Liveness detection
- [ ] Vote encryption
- [ ] Admin dashboard
- [ ] Audit logs

## License

MIT License

## Contributing

Feel free to submit issues and enhancement requests!
