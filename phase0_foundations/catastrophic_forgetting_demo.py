"""
Phase 0 — Catastrophic Forgetting Demonstration
================================================
Your first concrete encounter with the central problem of Project Veena.

This script demonstrates the core failure mode that Veena's entire architecture
is designed to prevent: when a neural network learns Task B, it destroys its
ability to perform Task A. Then it shows how EWC partially addresses this.

Run this BEFORE reading about EWC. Experience the problem first.
Then implement the EWC class methods and run again.

Usage:
    # See the problem:
    python phase0_foundations/catastrophic_forgetting_demo.py

    # See the (partial) solution:
    python phase0_foundations/catastrophic_forgetting_demo.py --ewc

    # Experiment with regularization strength:
    python phase0_foundations/catastrophic_forgetting_demo.py --ewc --lambda_ewc 5000

Requirements: torch, torchvision, matplotlib, numpy
"""

import argparse
import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ExperimentConfig:
    """All hyperparameters in one place. No magic numbers in the code below."""
    # Data
    task_a_digits: list[int] = None
    task_b_digits: list[int] = None
    batch_size: int = 64

    # Model
    input_dim: int = 784       # 28x28 MNIST pixels
    hidden_dim: int = 256
    output_dim: int = 10       # 10 digit classes

    # Training
    epochs_per_task: int = 10
    learning_rate: float = 1e-3

    # EWC
    lambda_ewc: float = 500.0  # Regularization strength — key hyperparameter
    fisher_samples: int = 200  # Number of samples to estimate Fisher matrix

    # Output
    output_dir: str = "phase0_foundations/results"

    def __post_init__(self) -> None:
        if self.task_a_digits is None:
            self.task_a_digits = [0, 1, 2, 3, 4]
        if self.task_b_digits is None:
            self.task_b_digits = [5, 6, 7, 8, 9]


# ─────────────────────────────────────────────────────────────────────────────
# MODEL
# ─────────────────────────────────────────────────────────────────────────────

class SimpleClassifier(nn.Module):
    """
    Deliberately minimal MLP. The architecture is not the point here.
    The forgetting behaviour is the point.

    In Veena terms: this is a tiny version of the neural component that
    EWC protects during Tier 2 sleep cycle updates.
    """

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass. x shape: (batch, 1, 28, 28) → flattened internally."""
        return self.network(x.view(x.size(0), -1))


# ─────────────────────────────────────────────────────────────────────────────
# EWC — IMPLEMENT THESE METHODS (Phase 0 Exercise)
# ─────────────────────────────────────────────────────────────────────────────

class EWC:
    """
    Elastic Weight Consolidation — Kirkpatrick et al., 2017
    arXiv: 1612.00796

    After learning Task A, this class:
    1. Computes the Fisher Information Matrix (F_i for each parameter θ_i)
    2. Saves the current parameters as θ*

    When training on Task B, the loss becomes:
        Loss_total = Loss_B(θ) + (λ/2) * Σ_i F_i * (θ_i - θ*_i)²

    The second term is the EWC penalty. It resists changes to weights
    that were important (high F_i) for Task A.

    In Veena's architecture: this is the core mechanism of Tier 2 updates
    during sleep cycles. The Fisher matrix identifies which weights encode
    foundational knowledge and prevents the sleep cycle from overwriting them.

    ─────────────────────────────────────────────────────────────
    YOUR TASK: Implement _compute_fisher() and penalty()
    Read Section 2 of arXiv:1612.00796 before implementing.
    ─────────────────────────────────────────────────────────────
    """

    def __init__(
        self,
        model: nn.Module,
        dataloader: DataLoader,
        lambda_ewc: float,
        device: str,
        n_samples: int = 200
    ) -> None:
        self.model = model
        self.lambda_ewc = lambda_ewc
        self.device = device

        self.fisher: dict[str, torch.Tensor] = {}
        self.optimal_params: dict[str, torch.Tensor] = {}

        print(f"  EWC: Computing Fisher Information Matrix over {n_samples} samples...")
        self._compute_fisher(dataloader, n_samples)
        self._save_optimal_params()

        # Report Fisher statistics
        total_params = sum(f.numel() for f in self.fisher.values())
        mean_fisher = np.mean([f.mean().item() for f in self.fisher.values()])
        print(f"  EWC: Protecting {total_params:,} parameters | Mean Fisher: {mean_fisher:.6f}")

    def _compute_fisher(self, dataloader: DataLoader, n_samples: int) -> None:
        """
        Compute the empirical Fisher Information Matrix.

        F_i ≈ E[(∂ log p(y|x,θ) / ∂θ_i)²]

        Interpretation: F_i measures how much changing weight θ_i
        changes the model's output distribution on Task A data.
        High F_i = critical weight for Task A = protect it strongly.
        Low F_i = unimportant weight for Task A = can change freely.

        Implementation steps:
        1. Initialize Fisher dict to zeros for all parameters
        2. For each batch (up to n_samples total):
           a. Forward pass → get output logits
           b. Convert to log probabilities (log_softmax)
           c. Compute cross-entropy loss (or use log_prob of true labels)
           d. Backward pass → accumulate squared gradients
        3. Normalize by total number of samples processed

        ─── IMPLEMENT THIS ───
        """
        self.model.eval()

        # Initialize Fisher to zero for all trainable parameters
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.fisher[name] = torch.zeros_like(param.data)

        criterion = nn.CrossEntropyLoss()
        samples_processed = 0

        for inputs, targets in dataloader:
            if samples_processed >= n_samples:
                break

            inputs = inputs.to(self.device)
            targets = targets.to(self.device)
            batch_size = inputs.size(0)

            self.model.zero_grad()
            outputs = self.model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()

            # Accumulate squared gradients weighted by batch size
            for name, param in self.model.named_parameters():
                if param.requires_grad and param.grad is not None:
                    self.fisher[name] += param.grad.data.pow(2) * batch_size

            samples_processed += batch_size

        # Normalize by total samples processed
        for name in self.fisher:
            self.fisher[name] /= samples_processed

    def _save_optimal_params(self) -> None:
        """
        Save current parameters as θ* — the optimal parameters for Task A.
        These are the target values the EWC penalty pulls toward.
        """
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.optimal_params[name] = param.data.clone()

    def penalty(self) -> torch.Tensor:
        """
        Compute the EWC regularization penalty.

        = (λ/2) * Σ_i F_i * (θ_i - θ*_i)²

        This gets ADDED to the Task B cross-entropy loss during training.
        Large penalty = current weights have drifted far from Task A optimum
        on weights that were important for Task A.

        ─── IMPLEMENT THIS ───
        """
        loss = torch.tensor(0.0, device=self.device)

        for name, param in self.model.named_parameters():
            if name in self.fisher and name in self.optimal_params:
                fisher = self.fisher[name]
                optimal = self.optimal_params[name]
                # Element-wise: Fisher * (current - optimal)^2, then sum
                loss += (fisher * (param - optimal).pow(2)).sum()

        return (self.lambda_ewc / 2.0) * loss


# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────

def get_split_mnist(
    task_a_digits: list[int],
    task_b_digits: list[int],
    batch_size: int
) -> tuple[DataLoader, DataLoader, DataLoader, DataLoader]:
    """
    Split MNIST into two sequential tasks.

    Task A: subset of digits → model learns these first
    Task B: different subset → model learns these second (causing forgetting)

    Returns: train_a, test_a, train_b, test_b
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    train_data = datasets.MNIST('./data', train=True,  download=True, transform=transform)
    test_data  = datasets.MNIST('./data', train=False, download=True, transform=transform)

    def filter_by_digits(dataset: datasets.MNIST, digits: list[int]) -> Subset:
        indices = [i for i, (_, label) in enumerate(dataset) if label in digits]
        return Subset(dataset, indices)

    train_a = DataLoader(filter_by_digits(train_data, task_a_digits), batch_size=batch_size, shuffle=True)
    test_a  = DataLoader(filter_by_digits(test_data,  task_a_digits), batch_size=batch_size, shuffle=False)
    train_b = DataLoader(filter_by_digits(train_data, task_b_digits), batch_size=batch_size, shuffle=True)
    test_b  = DataLoader(filter_by_digits(test_data,  task_b_digits), batch_size=batch_size, shuffle=False)

    return train_a, test_a, train_b, test_b


# ─────────────────────────────────────────────────────────────────────────────
# TRAINING AND EVALUATION
# ─────────────────────────────────────────────────────────────────────────────

@torch.no_grad()
def evaluate(model: nn.Module, dataloader: DataLoader, device: str) -> float:
    """Compute classification accuracy on a dataloader."""
    model.eval()
    correct = total = 0
    for inputs, targets in dataloader:
        inputs, targets = inputs.to(device), targets.to(device)
        correct += (model(inputs).argmax(dim=1) == targets).sum().item()
        total += targets.size(0)
    return correct / total


def train_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    optimizer: optim.Optimizer,
    device: str,
    ewc: Optional[EWC] = None
) -> float:
    """
    Train for one epoch, optionally with EWC regularization.

    If ewc is provided: loss = cross_entropy + ewc.penalty()
    This is the core mechanism of how EWC prevents forgetting.
    """
    model.train()
    criterion = nn.CrossEntropyLoss()
    total_loss = 0.0

    for inputs, targets in dataloader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()

        ce_loss = criterion(model(inputs), targets)
        ewc_loss = ewc.penalty() if ewc is not None else torch.tensor(0.0)
        total_loss_val = ce_loss + ewc_loss

        total_loss_val.backward()
        optimizer.step()
        total_loss += ce_loss.item()  # Log CE loss separately (not EWC term)

    return total_loss / len(dataloader)


# ─────────────────────────────────────────────────────────────────────────────
# EXPERIMENT
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ExperimentResults:
    """Structured results for comparison across runs."""
    config: ExperimentConfig
    use_ewc: bool
    task_a_peak_acc: float
    task_a_final_acc: float
    task_b_final_acc: float
    forgetting_absolute: float
    forgetting_pct: float
    acc_history_a: list[float]
    acc_history_b: list[Optional[float]]


def run_experiment(
    config: ExperimentConfig,
    use_ewc: bool,
    device: str
) -> ExperimentResults:
    """
    Full sequential learning experiment.

    Phase 1: Train on Task A for N epochs
    Phase 2: Train on Task B for N epochs (with or without EWC)
    Measure: how much Task A accuracy was retained?
    """
    label = "WITH EWC" if use_ewc else "WITHOUT EWC (baseline)"
    sep = "=" * 65
    print(f"\n{sep}\n  EXPERIMENT: {label}\n{sep}\n")

    # Setup
    train_a, test_a, train_b, test_b = get_split_mnist(
        config.task_a_digits, config.task_b_digits, config.batch_size
    )
    model = SimpleClassifier(config.input_dim, config.hidden_dim, config.output_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)

    acc_history_a: list[float] = []
    acc_history_b: list[Optional[float]] = []

    # ── Phase 1: Train on Task A ──────────────────────────────────────────
    print(f"Phase 1: Training on Task A (digits {config.task_a_digits})")
    for epoch in range(config.epochs_per_task):
        train_epoch(model, train_a, optimizer, device, ewc=None)
        acc_a = evaluate(model, test_a, device)
        acc_history_a.append(acc_a)
        acc_history_b.append(None)
        if (epoch + 1) % 2 == 0:
            print(f"  Epoch {epoch+1:2d}/{config.epochs_per_task} | Task A: {acc_a:.3f}")

    task_a_peak = max(acc_history_a)
    print(f"\n  Peak Task A accuracy: {task_a_peak:.3f}")

    # ── EWC Setup ─────────────────────────────────────────────────────────
    ewc = None
    if use_ewc:
        print("\nComputing Fisher Information Matrix on Task A...")
        ewc = EWC(
            model=model,
            dataloader=train_a,
            lambda_ewc=config.lambda_ewc,
            device=device,
            n_samples=config.fisher_samples
        )

    # ── Phase 2: Train on Task B ──────────────────────────────────────────
    print(f"\nPhase 2: Training on Task B (digits {config.task_b_digits})")
    print("Monitoring Task A accuracy for forgetting...\n")

    for epoch in range(config.epochs_per_task):
        train_epoch(model, train_b, optimizer, device, ewc=ewc)
        acc_a = evaluate(model, test_a, device)
        acc_b = evaluate(model, test_b, device)
        acc_history_a.append(acc_a)
        acc_history_b.append(acc_b)
        if (epoch + 1) % 2 == 0:
            print(f"  Epoch {epoch+1:2d}/{config.epochs_per_task} | Task A: {acc_a:.3f} | Task B: {acc_b:.3f}")

    # ── Results ───────────────────────────────────────────────────────────
    task_a_final = acc_history_a[-1]
    task_b_final = acc_history_b[-1]
    forgetting_abs = task_a_peak - task_a_final
    forgetting_pct = (forgetting_abs / task_a_peak) * 100

    print(f"\n{sep}")
    print(f"  RESULTS — {label}")
    print(sep)
    print(f"  Task A peak accuracy:     {task_a_peak:.3f}")
    print(f"  Task A final accuracy:    {task_a_final:.3f}")
    print(f"  Forgetting (absolute):    {forgetting_abs:.3f}")
    print(f"  Forgetting (relative):    {forgetting_pct:.1f}%")
    print(f"  Task B final accuracy:    {task_b_final:.3f}")

    if not use_ewc:
        if forgetting_pct > 30:
            print(f"\n  ⚠️  SEVERE CATASTROPHIC FORGETTING: {forgetting_pct:.0f}% of Task A destroyed.")
            print("     This is the problem Veena's EWC + sleep cycle is built to solve.")
        elif forgetting_pct > 10:
            print(f"\n  ⚠️  SIGNIFICANT FORGETTING: {forgetting_pct:.0f}% of Task A degraded.")
    else:
        reduction = 1.0
        print(f"\n  EWC λ={config.lambda_ewc} | Forgetting reduced to {forgetting_pct:.1f}%")
        print(f"  Stability-plasticity trade-off: Task B accuracy = {task_b_final:.3f}")
        print(f"  (Higher λ → less forgetting, but lower Task B accuracy)")

    return ExperimentResults(
        config=config,
        use_ewc=use_ewc,
        task_a_peak_acc=task_a_peak,
        task_a_final_acc=task_a_final,
        task_b_final_acc=task_b_final,
        forgetting_absolute=forgetting_abs,
        forgetting_pct=forgetting_pct,
        acc_history_a=acc_history_a,
        acc_history_b=acc_history_b
    )


# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def plot_results(results: ExperimentResults, output_path: Path) -> None:
    """Generate and save the forgetting curve plot."""
    n_epochs = len(results.acc_history_a)
    epochs = list(range(1, n_epochs + 1))
    task_switch = results.config.epochs_per_task

    b_accs = [x if x is not None else float('nan') for x in results.acc_history_b]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    label = "EWC Protected" if results.use_ewc else "No Protection (Baseline)"
    fig.suptitle(f"Catastrophic Forgetting Demo — {label}", fontsize=13, fontweight='bold')

    # Left: accuracy over time
    ax = axes[0]
    ax.plot(epochs, results.acc_history_a, 'b-o', label='Task A (learned first)', lw=2, ms=4)
    ax.plot(epochs[task_switch:], b_accs[task_switch:], 'r-o', label='Task B (learned second)', lw=2, ms=4)
    ax.axvline(x=task_switch + 0.5, color='gray', ls='--', alpha=0.7, label='Task switch')
    ax.axhline(y=results.task_a_peak_acc, color='blue', ls=':', alpha=0.4, label=f'Task A peak ({results.task_a_peak_acc:.2f})')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy')
    ax.set_title('Accuracy Over Time')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1.05)

    # Right: summary bar chart
    ax = axes[1]
    categories = ['Task A\n(Peak)', 'Task A\n(After Task B)', 'Task B\n(Final)']
    values = [results.task_a_peak_acc, results.task_a_final_acc, results.task_b_final_acc]
    colors = ['royalblue', 'tomato' if not results.use_ewc else 'orange', 'seagreen']
    bars = ax.bar(categories, values, color=colors, alpha=0.85, edgecolor='white', lw=1.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{val:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_ylabel('Accuracy')
    ax.set_title(f'Summary | Forgetting: {results.forgetting_pct:.1f}%')
    ax.set_ylim(0, 1.15)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n  Plot saved: {output_path}")
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Catastrophic Forgetting Demo — Project Veena Phase 0"
    )
    parser.add_argument("--ewc", action="store_true",
                        help="Enable EWC regularization")
    parser.add_argument("--lambda_ewc", type=float, default=500.0,
                        help="EWC regularization strength (default: 500.0)")
    parser.add_argument("--epochs", type=int, default=10,
                        help="Epochs per task (default: 10)")
    parser.add_argument("--device", type=str, default="auto",
                        choices=["auto", "cpu", "cuda", "mps"])
    args = parser.parse_args()

    # Device selection
    if args.device == "auto":
        if torch.cuda.is_available():
            device = "cuda"
            print("Device: CUDA GPU detected")
        elif torch.backends.mps.is_available():
            device = "mps"
            print("Device: Apple MPS detected")
        else:
            device = "cpu"
            print("Device: CPU (no GPU detected — this will be slow)")
    else:
        device = args.device

    config = ExperimentConfig(
        epochs_per_task=args.epochs,
        lambda_ewc=args.lambda_ewc
    )

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = run_experiment(config, use_ewc=args.ewc, device=device)

    filename = f"forgetting_{'ewc_lambda' + str(int(args.lambda_ewc)) if args.ewc else 'baseline'}.png"
    plot_results(results, output_dir / filename)

    # Phase 0 learning prompts
    print("\n" + "─" * 65)
    print("PHASE 0 EXERCISE — Answer these before moving on:")
    print("─" * 65)
    if not args.ewc:
        print("1. Why exactly did Task A accuracy collapse? Which weights changed?")
        print("2. Is this forgetting catastrophic or gradual? What does that tell you?")
        print("3. Run again with --ewc and compare. What changed in the loss function?")
    else:
        print(f"1. You used λ={args.lambda_ewc}. Try λ=5000. What happens to Task B accuracy?")
        print("2. Why does high λ hurt Task B? What is the stability-plasticity trade-off?")
        print("3. How does Veena's Sleep Cycle address the λ tuning problem?")
        print("4. EWC fails after many tasks. Why? What architectural decision in Veena")
        print("   mitigates this? (Hint: what does the Episodic Buffer clear after each cycle?)")
    print("─" * 65)


if __name__ == "__main__":
    main()
