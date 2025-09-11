from manim import *
import numpy as np

class ManyBrownian(MovingCameraScene):
    def construct(self):
        # ---- parametri ----
        seed, T, dt, sigma = 7, 12.0, 0.02, 1.0
        n_paths, run_time, extent = 50, 8, 5.5

        # sfondo
        self.camera.background_color = "#0d0f14"
        grid = NumberPlane(
            x_range=[-extent, extent, 1], y_range=[-extent, extent, 1],
            background_line_style={"stroke_color": GREY_E, "stroke_width": 1, "stroke_opacity": 0.18},
            faded_line_style={"stroke_color": GREY_E, "stroke_width": 1, "stroke_opacity": 0.06},
        )
        self.add(grid)

        # ---- simulazione (NumPy) ----
        np.random.seed(seed)
        N = int(T/dt) + 1

        def bm2d():
            dW = np.sqrt(dt) * np.random.normal(size=(N-1, 2))
            X  = np.vstack([np.zeros(2), np.cumsum(sigma * dW, axis=0)])  # (N,2)
            return X

        # paths 2D → 3D (z=0) per Manim
        def to3(P2):
            return np.column_stack((P2, np.zeros(len(P2))))  # (N,3)

        paths3 = [to3(bm2d()) for _ in range(n_paths)]

        # ---- mobjects ----
        vlines = VGroup()
        for i, P3 in enumerate(paths3):
            V = VMobject()
            # inizializza con almeno 2 punti 3D
            V.set_points_as_corners(P3[:2].tolist())
            if i == 0:
                V.set_stroke(width=6).set_color_by_gradient(BLUE_D, TEAL_A, YELLOW_A)
            else:
                V.set_stroke(GREY_B, width=2, opacity=0.28)
            vlines.add(V)

        main_dot = Dot(radius=0.06, color=WHITE).move_to(paths3[0][0])
        halo = Circle(radius=0.18).set_stroke(0).set_fill(WHITE, opacity=0.12).move_to(main_dot)
        self.add(*vlines, halo, main_dot)

        # leggera zoom
        self.play(self.camera.frame.animate.scale(0.95), run_time=0.6)

        # ---- animazione: crescita sincronizzata ----
        def grow(alpha):
            idx = max(1, int(alpha * (N - 1)))
            for V, P3 in zip(vlines, paths3):
                V.set_points_as_corners(P3[:idx+1].tolist())
            main_dot.move_to(paths3[0][idx])
            halo.move_to(paths3[0][idx])

        self.play(UpdateFromAlphaFunc(vlines, lambda _m, a: grow(a)),
                  run_time=run_time, rate_func=linear)

        self.play(FocusOn(main_dot), Flash(main_dot, flash_radius=0.25), run_time=0.7)
        self.wait(0.4)