# Stream Table Flow Model — Analysis & Successful Aspects

**Source URL (crawl attempt):**  
https://waldo.webdav.acequia.io/gsd-vis-2487/guerin/week5-assignments/

**Crawl result:** The site returned a device registration page only; assignment listings and individual model pages were not accessible without registering. This analysis therefore draws on (1) published StreamTable and flow-visualization literature, and (2) the stream table implementations in this repo (`projects/stream-table-demo_feb4/`).

---

## Two Meanings of “Stream Table”

1. **StreamTable (data visualization)**  
   An area-proportional visualization for 2D tables with weighted cells: columns as non-overlapping vertical streams, rows as horizontal bands; each cell is a rectangle whose area equals the cell weight. See Espenant & Mondal, *StreamTable: An Area Proportional Visualization for Tables with Flowing Streams*, WALCOM 2022 ([GWF Publications](https://gwf-uwaterloo.github.io/gwf-publications/G22-10001)).

2. **Stream table flow model (simulation)**  
   A physical or digital model of flow in a stream table (e.g., Emriver-style): terrain, inlet/outlet, and particles that move under a flow field (e.g., gradient-driven). Your demos (`index.html`, `draft2.html`) are implementations of this kind.

Below, “stream table flow model” refers to the **simulation** type; “StreamTable” refers to the **visualization** type where relevant.

---

## Most Successful Aspects of the Stream Table Flow Model

### 1. **Gradient-driven flow field**

- **What:** Flow direction and strength are derived from a scalar field (e.g., luminance) so particles move from light to dark (or high to low).
- **Why it works:** One editable field (e.g., a brush-painted grayscale “terrain”) drives the whole flow; no need to hand-author vectors everywhere. Matches intuition (water flows downhill / toward drain).
- **In your demos:** `getGradientValue()` samples the gradient; `Turtle`/`Particle.update()` applies gradient-based force. Linear gradient (left→right) plus a dark radial region at the drain creates a clear flow path.

### 2. **Inlet and drain**

- **What:** Fixed inlet (e.g., left, mid-height) and drain (e.g., right) with clear geometry; particles spawn at the inlet and are removed at the drain.
- **Why it works:** Gives a single, readable flow narrative (source → path → sink) and keeps particle count bounded.
- **In your demos:** `inletX/Y`, `drainX/Y`; spawn in `addTurtles()`/`addParticles()`; removal when position is inside the drain rectangle.

### 3. **Brush-editable terrain**

- **What:** User paints on the gradient/terrain (grayscale) with configurable size, color (gray level), opacity, feather, and noise.
- **Why it works:** Supports experimentation and “what-if” scenarios (dams, channels, obstacles) without coding; the same gradient drives the flow so feedback is immediate.
- **In your demos:** `drawOnGradient()` updates both display and underlying gradient data; brush parameters (e.g., feather, noise) allow natural-looking terrain.

### 4. **Particle/turtle representation**

- **What:** Discrete agents (turtles/particles) with position, velocity, and optional size/type; they integrate the flow field over time.
- **Why it works:** Makes flow visible and intuitive; different sizes/colors can represent sediment classes (e.g., small/medium/large).
- **In your demos:** Three size classes with distinct colors (e.g., blue/orange/red-purple); size affects damping so “larger” particles are slightly more persistent.

### 5. **Velocity damping and boundaries**

- **What:** Velocity is damped each step; hard boundaries (table top/bottom, inlet/drain) and optional bounce/friction at the bottom.
- **Why it works:** Prevents runaway motion, keeps flow on the table, and makes deposition/behavior at boundaries interpretable.
- **In your demos:** `velocityDamping` plus size-based damping; explicit checks for canvas edges, drain, and `tableSurfaceY` with bounce and friction.

### 6. **Heat map overlay (aggregate behavior)**

- **What:** A grid accumulates particle presence (or count) over time, then visualizes it (e.g., blue→green→yellow→red) with optional decay.
- **Why it works:** Shifts focus from single particles to “where does flow go?” and “where does sediment accumulate?”; decay keeps the map responsive to recent conditions.
- **In your demos:** `draft2.html` uses a grid, per-frame accumulation, logarithmic scaling for color, and a decay rate so the heat map fades over ~30 seconds.

### 7. **Real-time controls**

- **What:** Sliders (and optional buttons) for flow rate, particle density, velocity damping, and brush parameters.
- **Why it works:** Supports exploration and comparison (e.g., low vs high flow, different terrain) without reloading; aligns with the exploratory nature of stream table experiments.

---

## Aspects from StreamTable (Data Viz) That Transfer Well

If you ever connect “stream table flow” to **table/cartogram** style visualization (StreamTable):

- **Area = weight:** Cell area proportional to a value keeps quantities readable.
- **Minimize excess area:** Tighter layout (less empty space) improves readability.
- **Maximize cell adjacencies in streams:** Keeping consecutive cells adjacent in a stream reduces “wiggle” and makes rows/columns easier to follow.

These are design goals for the layout algorithm, not the flow simulation, but they share the idea that good aesthetics (clear paths, minimal clutter) make the representation more successful.

---

## Summary Table

| Aspect                     | Role in success                                      |
|---------------------------|------------------------------------------------------|
| Gradient-driven flow      | Single editable field drives entire flow direction   |
| Inlet + drain             | Clear narrative and bounded particle count          |
| Brush-editable terrain    | User-driven experimentation and immediate feedback   |
| Particle/turtle agents    | Visible, intuitive flow and sediment representation |
| Damping + boundaries      | Stable, interpretable motion and deposition          |
| Heat map + decay          | Aggregate “where does it go?” view over time        |
| Real-time controls        | Exploratory use without code changes                 |

---

## References

- Espenant, J., & Mondal, D. (2022). *StreamTable: An Area Proportional Visualization for Tables with Flowing Streams.* WALCOM: Algorithms and Computation, 97–108.  
  https://gwf-uwaterloo.github.io/gwf-publications/G22-10001  
- Local implementations: `projects/stream-table-demo_feb4/index.html` (Emriver Stream Table Model), `projects/stream-table-demo_feb4/draft2.html` (Emriver Stream Table — Heat Map).
