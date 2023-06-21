from manim import *
import random


class Stochastic(Scene):
    def addBits(self, bitstream, bits):
        for bit in bits:
            # Create a text object for the bit
            bit_text = MathTex(str(bit)).move_to(RIGHT * 3)

            # If there are already bits in the bitstream
            if bitstream:
                # Shift all existing bits to the left
                self.play(*[ApplyMethod(b.shift, LEFT * 0.5) for b in bitstream], FadeIn(bit_text), run_time=0.3)

            bitstream.append(bit_text)
        return bitstream
    def construct(self):
        f = Variable(-1, "f", num_decimal_places=2).to_edge(UP + LEFT)
        p = Variable(0, "p", num_decimal_places=2).align_to(f, DOWN)
        bitstream = []
        self.play(Write(p), Write(f))
        self.addBits(bitstream, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        self.play(p.tracker.animate.set_value(0.25),f.tracker.animate.set_value(-0.5), *[FadeOut(b) for b in bitstream])
        bitstream = []
        self.addBits(bitstream, [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0])

        self.play(p.tracker.animate.set_value(0.5),f.tracker.animate.set_value(0), *[FadeOut(b) for b in bitstream])
        bitstream = []
        self.addBits(bitstream, [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1])

        self.play(p.tracker.animate.set_value(0.25),f.tracker.animate.set_value(-0.5), *[FadeOut(b) for b in bitstream])
        bitstream = []
        self.addBits(bitstream, [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1])

        self.play(p.tracker.animate.set_value(1),f.tracker.animate.set_value(1), *[FadeOut(b) for b in bitstream])
        bitstream = []
        self.addBits(bitstream, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])


class Tanh(Scene):
    def construct(self):
        p = [0.1, -1, 0.5, 0.8] # Values
        pi = [Variable(p[i], f"p_{i}", num_decimal_places=2) for i in range(len(p))]
        b = [MathTex("\cdots 0010111010011001", substrings_to_isolate=["1", "0"]), MathTex("\cdots 0000000000000000", substrings_to_isolate=["1", "0"]), MathTex("\cdots 1110110011101111", substrings_to_isolate=["1", "0"]), MathTex("\cdots 1111101111111110", substrings_to_isolate=["1", "0"])] # Bitstreams

        # List to hold each column
        columns = []

        columns_group = VGroup(*pi, *b).arrange_in_grid(buff=(3, 0.25), col_alignments="lc", flow_order="dr").move_to(UP * 2)

        ones =  [b for bits in [b[i].get_parts_by_tex("1") for i in range(len(b))] for b in bits]
        zeros = [b for bits in [b[i].get_parts_by_tex("0") for i in range(len(b))] for b in bits]

        # Add the group to the scene
        self.play(Write(columns_group))

        self.play(*[Indicate(e.set_color(YELLOW)) for e in ones])
        ones_var = Integer(number=34).move_to(LEFT + DOWN)
        copied_ones = [e.set_color(WHITE).copy() for e in ones]
        self.play(ReplacementTransform(Group(*copied_ones), ones_var))

        self.play(*[Indicate(e.set_color(YELLOW)) for e in zeros])
        zeros_var = Integer(number=30).next_to(ones_var, RIGHT * 2)
        copied_zeros = [e.set_color(WHITE).copy() for e in zeros]
        self.play(ReplacementTransform(Group(*copied_zeros), zeros_var))
        
        sum_equation = MathTex("p_1 + p_2 + p_3 + p_4 = 0.4")
        self.play(ReplacementTransform(Group(*[x.label.copy() for x in pi]), sum_equation))
        self.play(ReplacementTransform(Group(ones_var, zeros_var), MathTex("34 > 30").next_to(sum_equation, DOWN * 2)), ReplacementTransform(sum_equation, MathTex("0.4 > 0")))
        
        self.wait(2)
