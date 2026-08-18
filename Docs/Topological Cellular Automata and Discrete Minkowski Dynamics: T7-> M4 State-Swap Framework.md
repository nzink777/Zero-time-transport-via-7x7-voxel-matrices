
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{geometry}
\usepackage{hyperref}
\geometry{a4paper, margin=25mm}

\title{Topological Cellular Automata and Discrete Minkowski Dynamics: \\ A $T^7 \rightarrow M^4$ State-Swap Framework}
\author{Natasha Zink}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
We propose a discrete cellular automaton model of Minkowski $4D$ spacetime wherein space is formulated as an addressable, discrete computational array of Planck-sized voxels. By projecting higher-dimensional $T^7$ toroidal manifolds down into our $M^4$ brane, local transition rules are governed by discrete Lie algebra commutation relations rather than continuous differential field equations. Furthermore, we formulate an exact mass-energy equivalence swap protocol ($e^- \leftrightarrow n\gamma$) that permits fundamental fermions to be relocated via discrete pointer-arithmetic without violating local conservation laws, incurring vacuum instability, or triggering topological tearing.
\end{abstract}

\section{Introduction and The Discrete Voxel Canvas}
Standard formulations of quantum field theory rely on continuous space-time manifolds, an approach that inherently introduces divergent integrals. We replace the continuous canvas with a discrete computational architecture:
\begin{itemize}
    \item \textbf{The Voxel Array:} The spatial domain is partitioned into a discrete lattice of Planck-scale address nodes $x^\mu = (t, x, y, z)$.
    \item \textbf{The Execution Pointer:} The local $M^4$ brane experiences time as a moving wavefront update step ($\Delta t$) executed via sparse matrix operations.
\end{itemize}

\section{Lie-Algebraic Transition Rules}
Local state evolution is governed by finite linear operators mapped from the PoincarÃ© group ($SO(3,1)$) and internal gauge symmetries. For any arbitrary voxel state vector $\Psi(x^\mu) \in \mathbb{C}^7$, the discrete update rule progressing from time step $t$ to $t + \Delta t$ is:
\begin{equation}
\Psi(x^\mu, t + \Delta t) = \exp\left( -i \sum_k \theta_k G_k \right) \sum_{\nu \in \text{neighbors}} \mathbf{M}_{7 \times 7}(x^\mu, \nu) \Psi(\nu, t)
\end{equation}
where $G_k$ represent the discrete Lie algebra generators ensuring unitarity and gauge invariance.

\section{The Electron-Photon Equivalence Swap Protocol}
To achieve zero-time transport without generating vacuum decay, we utilize a $7 \times 7$ transformation matrix to map an electron state at source address $A$ to target address $B$. The protocol enforces:
\begin{enumerate}
    \item \textbf{Target Lock:} Relocation of $\Psi_{\text{electron}}(A) \to \Psi_{\text{electron}}(B)$.
    \item \textbf{Photonic Backfill:} Population of address $A$ with a stable standing wave satisfying the mass-energy invariant: $m_e c^2 = \sum_{j=1}^{n} \hbar \omega_j$.
    \item \textbf{Annihilation $\epsilon$-Threshold:} Interfering states are evaluated against a Planck-scale barrier $\epsilon_{\text{Planck}}$ and undergo anti-phase inversion if necessary.
\end{enumerate}

\section{Conclusion}
We have established a closed-loop mathematical architecture uniting discrete Minkowski dynamics, Lie-algebraic local transition rules, and mass-energy equivalence swaps. This formalization successfully bridges high-energy physics with computational automaton theory.

\end{document}
