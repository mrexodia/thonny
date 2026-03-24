import tkinter as tk

from thonny.tktextext import EnhancedText


TEST_TEXT = """a = 1
b = 2
c = a + b
d = a + b + c
"""


def _click(text, index, shift=False):
    x, y, _, _ = text.bbox(index)
    x += 1
    y += 1
    text.event_generate("<Shift-1>" if shift else "<1>", x=x, y=y)
    text.event_generate("<ButtonRelease-1>", x=x, y=y)
    text.update()


def _drag(text, start_index, end_index):
    x1, y1, _, _ = text.bbox(start_index)
    x2, y2, _, _ = text.bbox(end_index)
    text.event_generate("<1>", x=x1 + 1, y=y1 + 1)
    text.event_generate("<B1-Motion>", x=x2 + 1, y=y2 + 1)
    text.event_generate("<ButtonRelease-1>", x=x2 + 1, y=y2 + 1)
    text.update()


def test_shift_click_starts_from_current_cursor_position():
    root = tk.Tk()
    try:
        text = EnhancedText(root, width=40, height=10)
        text.pack()
        text.insert("1.0", TEST_TEXT)
        root.update()

        _click(text, "3.5")
        for _ in range(5):
            text.event_generate("<Left>")
            text.update()

        _click(text, "4.end", shift=True)

        assert [text.index(r) for r in text.tag_ranges("sel")] == ["3.0", "4.13"]
    finally:
        root.destroy()


def test_shift_click_fix_does_not_break_plain_mouse_selection():
    root = tk.Tk()
    try:
        text = EnhancedText(root, width=40, height=10)
        text.pack()
        text.insert("1.0", TEST_TEXT)
        root.update()

        _click(text, "3.5")
        for _ in range(5):
            text.event_generate("<Left>")
            text.update()
        _click(text, "4.end", shift=True)

        _drag(text, "2.0", "2.3")

        assert [text.index(r) for r in text.tag_ranges("sel")] == ["2.0", "2.3"]
    finally:
        root.destroy()


def test_escape_clears_selection():
    root = tk.Tk()
    try:
        text = EnhancedText(root, width=40, height=10)
        text.pack()
        text.insert("1.0", TEST_TEXT)
        root.update()

        text.tag_add("sel", "2.0", "2.3")
        assert text.clear_selection() == "break"

        assert [text.index(r) for r in text.tag_ranges("sel")] == []
    finally:
        root.destroy()
