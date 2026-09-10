# LEGO Assembly Activity Classification Using Gaze and IMU Data

This repository contains the implementation and experiments for my **diploma thesis at the University of Ruse "Angel Kanchev"**, investigating whether LEGO assembly activities can be classified using **eye-tracking gaze and IMU data**.

The project uses recordings from a Pupil Labs Neon eye tracker. The goal is to recognize the participant's current activity ***without*** using the scene video as an input to the machine-learning models.

## Classification

The final classification consists of three activities:

| Class | Activity |
|:---:|---|
| 0 | Looking at guide book |
| 1 | Assembling |
| 2 | Searching for pieces |

The dataset contains recordings from 27 participants, of which **25** were usable for the final experiments.

The recordings contain:

- Gaze data — 200 Hz
- IMU data — 110 Hz
- Scene video — 30 FPS

The scene video is used for activity labeling, while the ***models use only gaze and IMU-related data.***

## Custom desktop application

Its main components include:

- Video playback
- Timeline-based navigation
- Activity event creation and editing
- Time navigation
- Recording data handling
- Label visualization
- Keyboard/event handling

The labeling application was used to produce the activity annotations required for the machine-learning experiments.

## Machine Learning Pipeline
```text
Raw Pupil Labs Data
        ↓
Data Preparation & Synchronization
        ↓
Activity Labeling
        ↓
Feature Extraction
        ↓
Temporal Windowing
        ↓
Model Training
        ↓
Classification
        ↓
Results Evaluation
```

The project uses both **raw measurements and engineered features**, including gaze velocity, pupil measurements, event statistics, entropy, spatial dispersion, gyroscope magnitude, and head movement stability.

The sensor ***data is divided into temporal windows*** before being provided to the neural networks. The main configuration uses 45 samples per window, corresponding to approximately 0.22 seconds.

## Models

Several neural-network architectures were investigated:

* MLP
* LSTM
* CNN
* CNN + LSTM
* LSTM + CNN
* CNN + LSTM Fusion
* CNN + Transformer

The CNN + Transformer architecture combines convolutional feature extraction with self-attention, allowing the model to learn relationships between different points in the temporal sequence.

Hyperparameter optimization was performed using Optuna.

## Results

Two evaluation approaches were investigated.

### Subject-specific

The best observed model achieved approximately **76.8% accuracy** using the CNN + Transformer architecture.

### Subject-independent

When evaluating participants that were not represented during training, performance decreased to approximately **52% accuracy**.

This difference demonstrates the difficulty of generalizing gaze and head-movement patterns between different people.

## Repository Structure
```text
.
├── Docker/                 # Docker/Jupyter environment
├── Labeling app/           # Custom activity-labeling application
├── notebooks/
│   ├── Data preparation.ipynb
│   ├── ML.ipynb
│   ├── Results evaluation.ipynb
│   └── DL/                 # Deep-learning experiments
│       ├── DL.ipynb
│       ├── DL-per subject.ipynb
│       ├── Windowing.ipynb
│       └── Optuna/
├── Component diagram.drawio
├── Presentation.odp
├── Documentation_Georgi_Chaparov_EN.pdf
├── Zapiska_Georgi_Chaparov_EN.docx
└── README.md
```

## Running the Project

The project can be run using the provided Docker configuration:

> [!IMPORTANT]
> You need to have Docker installed.

```CMD 
docker compose -f Docker/compose.yml up --build 
```

The notebooks can also be run directly in a suitable Python environment with the required dependencies installed.

## Documentation

The complete diploma thesis documentation is included in the repository:

Documentation_Georgi_Chaparov_EN.pdf

The repository also contains the thesis documentation in DOCX format and the presentation used for the thesis defense.

- Technologies
- Python
- PyTorch
- CUDA
- NumPy
- Polars
- Pandas
- scikit-learn
- Optuna
- Matplotlib
- Jupyter
- Docker

## Author

**Georgi Chaparov <br>
University of Ruse "Angel Kanchev" <br>
Computer Systems and Technologies <br>**