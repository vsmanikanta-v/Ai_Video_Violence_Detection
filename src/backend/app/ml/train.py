"""Offline CNN-LSTM training script for violence detection.

Trains a lightweight CNN-LSTM model on labeled video clips and saves a .keras
model file that can be loaded by the backend via ML_MODEL_PATH.

Usage (from repo root):
    uv run python src/backend/app/ml/train.py \\
        --violent-dir    path/to/violent_videos \\
        --non-violent-dir path/to/non_violent_videos \\
        --output         src/backend/models/violence_model.keras

Then set in src/backend/.env:
    ML_MODEL_PATH=src/backend/models/violence_model.keras

Model input: variable-length frame sequence, each frame IMG_SIZE x IMG_SIZE x 3.
Model output: float in [0, 1] — violence probability.
"""

import argparse
import sys
import time
from pathlib import Path

import numpy as np

# Training constants — kept small for CPU training speed
_TRAIN_FRAMES = 16  # frames per video during training
_IMG_SIZE = 64  # height and width of each frame
_VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}


def _extract_frames(video_path: Path, n_frames: int, img_size: int) -> np.ndarray | None:
    """Extract n_frames evenly-spaced frames from video_path.

    Returns float32 array of shape (n_frames, img_size, img_size, 3) or None on failure.
    Shorter videos are zero-padded; longer videos are sampled uniformly.
    """
    try:
        import cv2
    except ImportError:
        print("ERROR: OpenCV not installed. Run: uv add opencv-python-headless")
        sys.exit(1)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return None

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    if total <= 0:
        cap.release()
        return None

    # Evenly-spaced indices across the full video duration
    indices = [int(i * total / n_frames) for i in range(n_frames)]
    frames: list[np.ndarray] = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret or frame is None:
            # Pad with black frame
            frames.append(np.zeros((img_size, img_size, 3), dtype=np.uint8))
            continue
        frame = cv2.resize(frame, (img_size, img_size), interpolation=cv2.INTER_LINEAR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)
    cap.release()

    if len(frames) < n_frames // 2:
        return None  # Too few readable frames

    # Pad to exactly n_frames if needed
    while len(frames) < n_frames:
        frames.append(np.zeros((img_size, img_size, 3), dtype=np.uint8))

    arr = np.stack(frames[:n_frames], axis=0).astype(np.float32) / 255.0
    return arr  # (n_frames, img_size, img_size, 3)


def _load_dataset(
    violent_dir: Path,
    non_violent_dir: Path,
    n_frames: int,
    img_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Load all videos from both directories. Returns (X, y) arrays."""
    X: list[np.ndarray] = []
    y: list[float] = []

    for label, directory, name in [
        (1.0, violent_dir, "VIOLENT"),
        (0.0, non_violent_dir, "NON_VIOLENT"),
    ]:
        videos = sorted(p for p in directory.iterdir() if p.suffix.lower() in _VIDEO_EXTS)
        print(f"  {name}: found {len(videos)} video(s) in {directory}")
        for vp in videos:
            frames = _extract_frames(vp, n_frames, img_size)
            if frames is not None:
                X.append(frames)
                y.append(label)
                print(f"    [ok] {vp.name}")
            else:
                print(f"    [skip] {vp.name} — could not read frames")

    if not X:
        print("\nERROR: No usable videos found. Check directory paths.")
        sys.exit(1)

    return np.stack(X, axis=0), np.array(y, dtype=np.float32)


def _build_model(img_size: int, lstm_dropout: float = 0.3) -> "keras.Model":  # type: ignore[name-defined]  # noqa: F821
    """Build CNN-LSTM model with variable-length time input.

    Architecture:
        Input:  (None, img_size, img_size, 3)  — variable frame count
        TimeDistributed Conv2D (16 filters) + MaxPool
        TimeDistributed Conv2D (32 filters) + MaxPool
        TimeDistributed GlobalAveragePooling2D  → (None, T, 32)
        LSTM (64 units, configurable dropout)   → (None, 64)
        Dense (1, sigmoid)                      → violence probability
    """
    import keras
    from keras import layers

    inp = keras.Input(shape=(None, img_size, img_size, 3), name="frames")

    # Per-frame spatial feature extraction
    x = layers.TimeDistributed(layers.Conv2D(16, (3, 3), activation="relu", padding="same"), name="conv1")(inp)
    x = layers.TimeDistributed(layers.MaxPool2D((2, 2)), name="pool1")(x)
    x = layers.TimeDistributed(layers.Conv2D(32, (3, 3), activation="relu", padding="same"), name="conv2")(x)
    x = layers.TimeDistributed(layers.MaxPool2D((2, 2)), name="pool2")(x)
    x = layers.TimeDistributed(layers.GlobalAveragePooling2D(), name="gap")(x)

    # Temporal pattern learning across frame sequence
    x = layers.LSTM(64, dropout=lstm_dropout, name="lstm")(x)

    out = layers.Dense(1, activation="sigmoid", name="violence_prob")(x)

    model = keras.Model(inputs=inp, outputs=out, name="violence_cnn_lstm")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-4),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train CNN-LSTM violence detection model (CPU-friendly, offline).")
    parser.add_argument(
        "--violent-dir",
        required=True,
        type=Path,
        help="Directory containing violent video clips",
    )
    parser.add_argument(
        "--non-violent-dir",
        required=True,
        type=Path,
        help="Directory containing non-violent video clips",
    )
    parser.add_argument(
        "--output",
        default="src/backend/models/violence_model.keras",
        type=Path,
        help="Output .keras model file path (default: src/backend/models/violence_model.keras)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=20,
        help="Training epochs (default: 20; increase for more accuracy)",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=_TRAIN_FRAMES,
        help=f"Frames per video for training (default: {_TRAIN_FRAMES})",
    )
    parser.add_argument(
        "--img-size",
        type=int,
        default=_IMG_SIZE,
        help=f"Frame height/width in pixels (default: {_IMG_SIZE})",
    )
    args = parser.parse_args()

    if not args.violent_dir.is_dir():
        print(f"ERROR: violent-dir not found: {args.violent_dir}")
        sys.exit(1)
    if not args.non_violent_dir.is_dir():
        print(f"ERROR: non-violent-dir not found: {args.non_violent_dir}")
        sys.exit(1)

    print("=" * 60)
    print("CNN-LSTM Violence Detection — Training")
    print("=" * 60)
    print(f"  Frames per video : {args.frames}")
    print(f"  Frame size       : {args.img_size}x{args.img_size}")
    print(f"  Epochs           : {args.epochs}")
    print(f"  Output           : {args.output}")
    print()

    print("Step 1/3 — Loading dataset...")
    X, y = _load_dataset(args.violent_dir, args.non_violent_dir, args.frames, args.img_size)
    n_violent = int(y.sum())
    n_non_violent = int((1 - y).sum())
    print(f"\n  Total  : {len(X)} samples")
    print(f"  VIOLENT     : {n_violent}")
    print(f"  NON_VIOLENT : {n_non_violent}")
    print(f"  Array shape : {X.shape}")  # (N, frames, img_size, img_size, 3)

    if n_violent == 0 or n_non_violent == 0:
        print("\nERROR: Need at least one video per class (VIOLENT and NON_VIOLENT).")
        sys.exit(1)

    print("\nStep 2/3 — Building model...")
    # For tiny datasets: disable LSTM dropout so the model can memorise training samples
    lstm_dropout = 0.0 if len(X) < 10 else 0.3
    model = _build_model(args.img_size, lstm_dropout=lstm_dropout)
    model.summary()

    # Shuffle so violent/non-violent samples are interleaved before any split
    indices = np.random.permutation(len(X))
    X, y = X[indices], y[indices]

    # With < 10 samples a val split removes too much training data — skip it
    val_split = 0.2 if len(X) >= 10 else 0.0
    # batch_size=1 for tiny datasets → 1 gradient update per sample per epoch (more updates)
    batch_size = 1 if len(X) < 10 else min(4, len(X))

    # Class weights — give equal importance to each class regardless of count
    total = len(y)
    class_weight = {
        0: total / (2.0 * max(int((1 - y).sum()), 1)),
        1: total / (2.0 * max(int(y.sum()), 1)),
    }
    print(
        f"\nStep 3/3 — Training ({args.epochs} epochs, batch={batch_size}, "
        f"val_split={val_split}, class_weights={class_weight})..."
    )
    t0 = time.perf_counter()
    model.fit(
        X,
        y,
        epochs=args.epochs,
        batch_size=batch_size,
        validation_split=val_split,
        class_weight=class_weight,
        verbose=1,
    )
    elapsed = time.perf_counter() - t0
    print(f"\nTraining complete in {elapsed:.1f}s")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(args.output))
    print(f"\nModel saved: {args.output.resolve()}")
    print()
    print("Next steps:")
    print("  1. Add to src/backend/.env:")
    print(f"       ML_MODEL_PATH={args.output.resolve()}")
    print("  2. Restart the backend — inference will use the real model.")


if __name__ == "__main__":
    main()
