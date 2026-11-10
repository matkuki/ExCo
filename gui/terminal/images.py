"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Qt-free inline-image support for the terminal emulator.
##
##      Two wire protocols are decoded here:
##        - the Kitty graphics protocol (APC "G" payloads, chunked base64,
##          transmit / transmit+display / put / delete / query);
##        - sixel graphics (DCS payloads ending in 'q').
##
##      Both produce placements anchored to a *stack row* (history rows below
##      the live screen plus the viewport row), the same coordinate system the
##      OSC 8 spans and OSC 133 marks use. The screen shifts them when the
##      bounded scrollback drops a row, remaps them through a resize reflow and
##      clears them when the screen changes identity (RIS, scrollback clear,
##      alternate-screen transition). The view owns the QImage decoding and the
##      painting; this module never imports Qt.
##
##      No Qt imports on purpose: the parsers are pure state and are tested
##      standalone.

import base64
import binascii
import math
from typing import Dict, List, Optional, Tuple

from gui.terminal.reflow import ReflowResult

# Bounds. An application can stream arbitrary amounts of image data; every
# buffer that survives a feed is capped so a runaway producer cannot grow the
# process without limit. The values are far above what a TUI preview needs.
MAX_PLACEMENTS: int = 128
MAX_TRANSMITTED_IMAGES: int = 64
MAX_IMAGE_BYTES: int = 8 * 1024 * 1024
MAX_TOTAL_IMAGE_BYTES: int = 64 * 1024 * 1024
MAX_PAYLOAD_CHARS: int = 24 * 1024 * 1024
MAX_SIXEL_DIMENSION: int = 4096
MAX_SIXEL_PIXELS: int = 4 * 1000 * 1000

# Default VT340 sixel palette, used until the stream defines a slot. The
# remaining indices stay black until defined, matching xterm.
_SIXEL_DEFAULT_PALETTE: Tuple[Tuple[int, int, int], ...] = (
    (0, 0, 0),
    (20, 20, 80),
    (80, 20, 20),
    (80, 20, 80),
    (20, 80, 20),
    (20, 80, 80),
    (80, 80, 20),
    (53, 53, 53),
    (26, 26, 26),
    (33, 33, 99),
    (99, 33, 33),
    (99, 33, 99),
    (33, 99, 33),
    (33, 99, 99),
    (99, 99, 33),
    (204, 204, 204),
)


def _clamp(value: int, low: int = 0, high: int = 255) -> int:
    """Clamp *value* into the inclusive range *low*..*high*."""
    if value < low:
        return low
    if value > high:
        return high
    return value


def _hls_to_rgb(hue: int, lightness: int, saturation: int) -> Tuple[int, int, int]:
    """Convert a sixel HLS triple (0-360, 0-100, 0-100) to RGB (0-255)."""
    h: float = (hue % 360) / 360.0
    light: float = _clamp(lightness, 0, 100) / 100.0
    s: float = _clamp(saturation, 0, 100) / 100.0
    if s == 0.0:
        grey: int = int(round(light * 255))
        return grey, grey, grey
    second: float = light * (1.0 + s) if light <= 0.5 else light + s - light * s
    first: float = 2.0 * light - second

    def channel(value: float) -> float:
        if value < 0.0:
            value += 1.0
        if value > 1.0:
            value -= 1.0
        if value < 1.0 / 6.0:
            return first + (second - first) * 6.0 * value
        if value < 1.0 / 2.0:
            return second
        if value < 2.0 / 3.0:
            return first + (second - first) * (2.0 / 3.0 - value) * 6.0
        return first

    return (
        _clamp(int(round(channel(h + 1.0 / 3.0) * 255))),
        _clamp(int(round(channel(h) * 255))),
        _clamp(int(round(channel(h - 1.0 / 3.0) * 255))),
    )


def _parse_number(value: str) -> int:
    """Parse a decimal integer, returning 0 for an empty or invalid token."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _png_size(data: bytes) -> Optional[Tuple[int, int]]:
    """Read the pixel size out of a PNG's IHDR chunk, or None.

    The view decodes the pixels with QImage; the size is needed here, without
    Qt, to give the placement a cell span and to advance the cursor after it.
    """
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if data[12:16] != b"IHDR":
        return None
    width: int = int.from_bytes(data[16:20], "big")
    height: int = int.from_bytes(data[20:24], "big")
    if width <= 0 or height <= 0:
        return None
    return width, height


def decode_sixel(data: str) -> Optional[Tuple[int, int, bytes]]:
    """Decode a sixel payload into ``(width, height, RGBA bytes)``.

    Undefined pixels keep alpha 0 (transparent), which is how a terminal
    composites sixel over its own background. Malformed or oversized payloads
    return None; the caller treats that as "consumed, but nothing to show".
    """
    palette: List[Tuple[int, int, int]] = list(_SIXEL_DEFAULT_PALETTE)
    palette.extend([(0, 0, 0)] * (256 - len(palette)))
    current: int = 0
    x: int = 0
    y: int = 0
    rows: List[bytearray] = []
    declared_width: int = 0
    declared_height: int = 0
    max_x: int = 0

    def ensure(px: int, py: int) -> bool:
        nonlocal max_x
        if px < 0 or py < 0:
            return True
        if px >= MAX_SIXEL_DIMENSION or py >= MAX_SIXEL_DIMENSION:
            return False
        while len(rows) <= py:
            rows.append(bytearray())
        row: bytearray = rows[py]
        if len(row) <= px:
            row.extend(b"\x00" * (px + 1 - len(row)))
        if px + 1 > max_x:
            max_x = px + 1
        return True

    def draw_char(bits: int) -> bool:
        nonlocal x
        for bit in range(6):
            if bits & (1 << bit):
                if not ensure(x, y + bit):
                    return False
                rows[y + bit][x] = current
        x += 1
        return True

    index: int = 0
    length: int = len(data)
    while index < length:
        char: str = data[index]
        if char == '"':
            # Raster attributes: "Pan;Pad;Ph;Pv
            index += 1
            params: List[str] = []
            current_param: str = ""
            while index < length and (data[index].isdigit() or data[index] == ";"):
                if data[index] == ";":
                    params.append(current_param)
                    current_param = ""
                else:
                    current_param += data[index]
                index += 1
            if current_param:
                params.append(current_param)
            if len(params) >= 4:
                declared_width = max(0, _parse_number(params[2]))
                declared_height = max(0, _parse_number(params[3]))
            continue
        if char == "#":
            # Colour introducer / definition: #Pc or #Pc;Pu;Px;Py;Pz
            index += 1
            params = []
            current_param = ""
            while index < length and (data[index].isdigit() or data[index] == ";"):
                if data[index] == ";":
                    params.append(current_param)
                    current_param = ""
                else:
                    current_param += data[index]
                index += 1
            if current_param:
                params.append(current_param)
            if params:
                slot: int = _parse_number(params[0])
                if len(params) >= 5:
                    system: int = _parse_number(params[1])
                    if system == 2:
                        colour = (
                            _clamp(_parse_number(params[2])),
                            _clamp(_parse_number(params[3])),
                            _clamp(_parse_number(params[4])),
                        )
                    elif system == 1:
                        colour = _hls_to_rgb(
                            _parse_number(params[2]),
                            _parse_number(params[3]),
                            _parse_number(params[4]),
                        )
                    else:
                        colour = (0, 0, 0)
                    if 0 <= slot < 256:
                        palette[slot] = colour
                if 0 <= slot < 256:
                    current = slot
            continue
        if char == "!":
            # Repeat: !<count><sixel char>
            index += 1
            digits: str = ""
            while index < length and data[index].isdigit():
                digits += data[index]
                index += 1
            count: int = _parse_number(digits) if digits else 1
            if index >= length:
                break
            sixel: str = data[index]
            index += 1
            if "?" <= sixel <= "~":
                bits: int = ord(sixel) - 63
                for _ in range(min(max(count, 1), MAX_SIXEL_DIMENSION)):
                    if not draw_char(bits):
                        return None
            continue
        if char == "$":
            x = 0
            index += 1
            continue
        if char == "-":
            y += 6
            x = 0
            index += 1
            continue
        if "?" <= char <= "~":
            if not draw_char(ord(char) - 63):
                return None
            index += 1
            continue
        # Whitespace and any other control character carry no pixels.
        index += 1

    width: int = max(declared_width, max_x)
    height: int = max(declared_height, len(rows))
    if width <= 0 or height <= 0:
        return None
    if width * height > MAX_SIXEL_PIXELS:
        return None
    pixels: bytearray = bytearray(width * height * 4)
    for py in range(min(height, len(rows))):
        row = rows[py]
        for px in range(min(len(row), width)):
            colour_index: int = row[px]
            red, green, blue = palette[colour_index]
            offset: int = (py * width + px) * 4
            pixels[offset] = red
            pixels[offset + 1] = green
            pixels[offset + 2] = blue
            pixels[offset + 3] = 255
    return width, height, bytes(pixels)


class ImageData:
    """One decoded image's pixels, shared by every placement of it.

    ``kind`` is ``"rgb"`` (3 bytes per pixel), ``"rgba"`` (4 bytes) or
    ``"png"`` (the original compressed stream). ``width``/``height`` are the
    pixel dimensions; they are 0 for a PNG whose header could not be read.
    """

    __slots__ = ("image_id", "kind", "width", "height", "data")

    def __init__(
        self, image_id: int, kind: str, width: int, height: int, data: bytes
    ) -> None:
        self.image_id: int = image_id
        self.kind: str = kind
        self.width: int = width
        self.height: int = height
        self.data: bytes = data


class Placement:
    """One image shown at a stack position.

    ``row``/``column`` are in the screen's stack coordinates. ``rows`` and
    ``columns`` are the cell span (always at least 1 once the store has the
    cell metrics); ``cell_sized`` says whether the span came from the protocol
    (``c``/``r``) and the image must be stretched into it, or from the pixel
    size and the image should keep its natural dimensions.
    """

    __slots__ = (
        "image",
        "placement_id",
        "row",
        "column",
        "rows",
        "columns",
        "z_index",
        "source_x",
        "source_y",
        "source_width",
        "source_height",
        "cell_sized",
        "cursor_policy",
        "serial",
    )

    def __init__(
        self,
        image: ImageData,
        placement_id: int,
        row: int,
        column: int,
        rows: int,
        columns: int,
        z_index: int,
        source_x: int,
        source_y: int,
        source_width: int,
        source_height: int,
        cell_sized: bool,
        cursor_policy: int = 0,
        serial: int = 0,
    ) -> None:
        self.image: ImageData = image
        self.placement_id: int = placement_id
        self.row: int = row
        self.column: int = column
        self.rows: int = rows
        self.columns: int = columns
        self.z_index: int = z_index
        self.source_x: int = source_x
        self.source_y: int = source_y
        self.source_width: int = source_width
        self.source_height: int = source_height
        self.cell_sized: bool = cell_sized
        self.cursor_policy: int = cursor_policy
        self.serial: int = serial


class _KittyChunk:
    """Accumulated Kitty APC fragments while ``m=1`` keeps the transfer open."""

    __slots__ = ("control", "parts", "size")

    def __init__(self, control: Dict[str, str], data: str) -> None:
        self.control: Dict[str, str] = dict(control)
        self.parts: List[str] = [data]
        self.size: int = len(data)


def _parse_kitty_control(text: str) -> Dict[str, str]:
    """Parse the ``key=value,key=value`` control string of a Kitty APC."""
    values: Dict[str, str] = {}
    for item in text.split(","):
        if not item:
            continue
        key, separator, value = item.partition("=")
        if not key:
            continue
        values[key] = value if separator else ""
    return values


def _decode_base64(text: str) -> Optional[bytes]:
    """Decode Kitty base64, tolerating padding that a chunk split left behind."""
    compact: str = "".join(text.split())
    compact = compact.rstrip("=")
    if not compact:
        return None
    compact += "=" * (-len(compact) % 4)
    try:
        return base64.b64decode(compact, validate=False)
    except (binascii.Error, ValueError):
        return None


class ImageStore:
    """Placements and transmitted images for one screen.

    ``version`` is bumped whenever the placement list changes identity (add,
    delete, clear, or a reflow/scroll that drops one), so the view knows when
    its QImage cache can be pruned. A row shift or remap that keeps every
    placement does not bump it: the cached pixels are still valid.
    """

    def __init__(self) -> None:
        self.placements: List[Placement] = []
        self.version: int = 0
        self.cell_width: float = 8.0
        self.cell_height: float = 16.0
        self._images: Dict[int, ImageData] = {}
        self._chunk: Optional[_KittyChunk] = None
        self._next_image_id: int = 1
        self._next_serial: int = 1

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def set_cell_metrics(self, width: float, height: float) -> None:
        """Record the renderer's cell size so pixels can become cells."""
        self.cell_width = max(float(width), 1.0)
        self.cell_height = max(float(height), 1.0)

    def _cell_span(self, width: int, height: int) -> Tuple[int, int]:
        """Cell span covering *width* x *height* pixels (at least 1x1)."""
        columns: int = max(1, int(math.ceil(width / self.cell_width)))
        rows: int = max(1, int(math.ceil(height / self.cell_height)))
        return rows, columns

    # ------------------------------------------------------------------
    # Lifetime
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Drop every placement, transmitted image and half-received chunk."""
        had_content: bool = bool(self.placements or self._images or self._chunk)
        self.placements = []
        self._images = {}
        self._chunk = None
        if had_content:
            self.version += 1

    def shift(self, rows: int) -> None:
        """Move placements up by *rows* dropped history rows.

        A placement whose whole cell span fell above the retained stack is
        gone with the text it was anchored to. One that is only partly above
        the top keeps its negative row: the view clips it, exactly like a
        partially visible glyph.
        """
        if rows <= 0 or not self.placements:
            return
        kept: List[Placement] = []
        for placement in self.placements:
            placement.row -= rows
            if placement.row + max(placement.rows, 1) <= 0:
                continue
            kept.append(placement)
        if len(kept) != len(self.placements):
            self.version += 1
        self.placements = kept

    def remap(self, result: ReflowResult) -> None:
        """Move every placement through a resize reflow's position map."""
        if not self.placements:
            return
        kept: List[Placement] = []
        for placement in self.placements:
            position: Optional[Tuple[int, int]] = result.map_position(
                placement.row, placement.column
            )
            if position is None:
                continue
            placement.row, placement.column = position
            kept.append(placement)
        if len(kept) != len(self.placements):
            self.version += 1
        self.placements = kept

    # ------------------------------------------------------------------
    # Kitty graphics protocol
    # ------------------------------------------------------------------

    def kitty_apc(
        self, payload: str, row: int, column: int
    ) -> Tuple[Optional[str], Optional[Placement]]:
        """Handle one APC payload.

        Returns ``(response, placement)``: *response* is written back to the
        application (a query reply, or None), and *placement* is the image
        just displayed (None for a transmit-only or delete request). *payload*
        is everything between ``ESC _`` and ``ST``; Kitty graphics payloads
        start with ``G``, and any other APC is ignored.
        """
        if not payload.startswith("G"):
            return None, None
        control_text, separator, data_text = payload[1:].partition(";")
        control: Dict[str, str] = _parse_kitty_control(control_text)
        if self._chunk is not None:
            # A continuation carries only m (and possibly q); keep the first
            # chunk's full control block.
            for key, value in control.items():
                if key != "m":
                    self._chunk.control.setdefault(key, value)
            self._chunk.parts.append(data_text)
            self._chunk.size += len(data_text)
            if self._chunk.size > MAX_PAYLOAD_CHARS:
                self._chunk = None
                return None, None
            if control.get("m") == "1":
                return None, None
            pending: _KittyChunk = self._chunk
            self._chunk = None
            control = pending.control
            data_text = "".join(pending.parts)
        elif control.get("m") == "1":
            if len(data_text) > MAX_PAYLOAD_CHARS:
                return None, None
            self._chunk = _KittyChunk(control, data_text)
            return None, None
        return self._apply_kitty(control, data_text, row, column)

    def _apply_kitty(
        self, control: Dict[str, str], data_text: str, row: int, column: int
    ) -> Tuple[Optional[str], Optional[Placement]]:
        action: str = control.get("a", "t")
        if action == "q":
            image_id: str = control.get("i", "")
            if image_id:
                return "\x1b_Gi={};OK\x1b\\".format(image_id), None
            return "\x1b_G;OK\x1b\\", None
        if action == "d":
            self._delete(control)
            return None, None
        if action == "p":
            image = self._transmitted(control)
            if image is None:
                return None, None
            return None, self._place(image, control, row, column)
        if action in ("t", "T"):
            image = self._transmit(control, data_text)
            if image is None:
                return None, None
            if action == "T":
                return None, self._place(image, control, row, column)
            return None, None
        return None, None

    def _transmit(self, control: Dict[str, str], data_text: str) -> Optional[ImageData]:
        """Decode a transmitted image and remember it by id."""
        raw: Optional[bytes] = _decode_base64(data_text)
        if raw is None or len(raw) > MAX_IMAGE_BYTES:
            return None
        image_format: int = _parse_number(control.get("f", "32") or "32")
        width: int = max(0, _parse_number(control.get("s", "0")))
        height: int = max(0, _parse_number(control.get("v", "0")))
        if image_format == 100:
            kind: str = "png"
            size: Optional[Tuple[int, int]] = _png_size(raw)
            if size is None:
                return None
            width, height = size
        elif image_format == 24:
            kind = "rgb"
            if width <= 0 or height <= 0 or len(raw) < width * height * 3:
                return None
            raw = raw[: width * height * 3]
        elif image_format == 32:
            kind = "rgba"
            if width <= 0 or height <= 0 or len(raw) < width * height * 4:
                return None
            raw = raw[: width * height * 4]
        else:
            return None
        image_id: int = _parse_number(control.get("i", "0"))
        if image_id <= 0:
            image_id = self._next_image_id
            self._next_image_id += 1
        elif image_id >= self._next_image_id:
            self._next_image_id = image_id + 1
        image = ImageData(image_id, kind, width, height, raw)
        self._images[image_id] = image
        self._trim_transmitted()
        return image

    def _trim_transmitted(self) -> None:
        """Evict the oldest transmitted images over the total byte budget."""
        total: int = sum(len(image.data) for image in self._images.values())
        while (
            total > MAX_TOTAL_IMAGE_BYTES or len(self._images) > MAX_TRANSMITTED_IMAGES
        ) and self._images:
            oldest: int = next(iter(self._images))
            total -= len(self._images[oldest].data)
            del self._images[oldest]

    def _trim_placements(self) -> None:
        """Drop the oldest placements over the count or total byte budget.

        Placements share ImageData, so this counts a shared image once per
        placement; the over-count only makes the bound more conservative.
        """
        total: int = sum(len(placement.image.data) for placement in self.placements)
        while len(self.placements) > MAX_PLACEMENTS or (
            total > MAX_TOTAL_IMAGE_BYTES and len(self.placements) > 1
        ):
            removed: Placement = self.placements.pop(0)
            total -= len(removed.image.data)

    def _transmitted(self, control: Dict[str, str]) -> Optional[ImageData]:
        """Look up a previously transmitted image for ``a=p``."""
        image_id: int = _parse_number(control.get("i", "0"))
        if image_id <= 0:
            return None
        return self._images.get(image_id)

    def _place(
        self, image: ImageData, control: Dict[str, str], row: int, column: int
    ) -> Placement:
        """Record a placement for *image* at (*row*, *column*)."""
        placement_id: int = _parse_number(control.get("p", "0"))
        columns: int = max(0, _parse_number(control.get("c", "0")))
        rows: int = max(0, _parse_number(control.get("r", "0")))
        cell_sized: bool = bool(columns > 0 or rows > 0)
        if columns <= 0 or rows <= 0:
            # A pixel-only image gets its span from the cell metrics, so the
            # scroll/overflow bookkeeping knows how many rows it covers.
            if image.width > 0 and image.height > 0:
                span_rows, span_columns = self._cell_span(image.width, image.height)
                rows = rows or span_rows
                columns = columns or span_columns
            else:
                rows = rows or 1
                columns = columns or 1
        placement = Placement(
            image,
            placement_id,
            row,
            column,
            rows,
            columns,
            _parse_number(control.get("z", "0")),
            max(0, _parse_number(control.get("x", "0"))),
            max(0, _parse_number(control.get("y", "0"))),
            max(0, _parse_number(control.get("w", "0"))),
            max(0, _parse_number(control.get("h", "0"))),
            cell_sized,
            _parse_number(control.get("C", "0")),
            self._allocate_serial(),
        )
        # Re-placing the same (image, placement) moves it instead of stacking
        # a second copy, which is what a TUI redrawing an animation expects.
        self.placements = [
            existing
            for existing in self.placements
            if not (
                existing.image.image_id == image.image_id
                and existing.placement_id == placement_id
            )
        ]
        self.placements.append(placement)
        self._trim_placements()
        self.version += 1
        return placement

    def _delete(self, control: Dict[str, str]) -> None:
        """Apply a Kitty ``a=d`` delete request."""
        what: str = control.get("d", "a")
        image_id: int = _parse_number(control.get("i", "0"))
        placement_id: int = _parse_number(control.get("p", "0"))
        before: int = len(self.placements)
        if what == "a":
            self.placements = []
        elif what == "i":
            if image_id <= 0:
                return
            self.placements = [
                placement
                for placement in self.placements
                if placement.image.image_id != image_id
            ]
        elif what == "p":
            if image_id <= 0 and placement_id == 0:
                return
            self.placements = [
                placement
                for placement in self.placements
                if not (
                    (image_id <= 0 or placement.image.image_id == image_id)
                    and (placement_id == 0 or placement.placement_id == placement_id)
                )
            ]
        else:
            # Cursor-, frame-, z- and coordinate-based deletes are not
            # supported; ignore them rather than guessing.
            return
        if len(self.placements) != before:
            self.version += 1

    # ------------------------------------------------------------------
    # Sixel graphics
    # ------------------------------------------------------------------

    def sixel_dcs(self, payload: str, row: int, column: int) -> Optional[Placement]:
        """Handle one DCS payload; return the placement when it was sixel.

        None means the payload was not a sixel image (a DECRQSS ``$q``, a
        session-id DCS, ...) and the caller should keep swallowing it.
        """
        header, separator, data = payload.partition("q")
        if not separator or header.strip("0123456789;"):
            return None
        decoded: Optional[Tuple[int, int, bytes]] = decode_sixel(data)
        if decoded is None:
            # It *was* sixel, just malformed or oversized. Nothing to show;
            # the DCS payload is still swallowed by the caller.
            return None
        width, height, pixels = decoded
        span_rows, span_columns = self._cell_span(width, height)
        placement = Placement(
            ImageData(self._allocate_image_id(), "rgba", width, height, pixels),
            0,
            row,
            column,
            span_rows,
            span_columns,
            0,
            0,
            0,
            0,
            0,
            False,
            serial=self._allocate_serial(),
        )
        self.placements.append(placement)
        self._trim_placements()
        self.version += 1
        return placement

    def _allocate_image_id(self) -> int:
        """Return an id no transmitted image can collide with."""
        image_id: int = self._next_image_id
        self._next_image_id += 1
        return image_id

    def _allocate_serial(self) -> int:
        """Return a placement token the view can key its QImage cache on.

        ``id(placement)`` is not safe for that: CPython reuses an address as
        soon as the object is freed, and a reflow/overflow can drop a
        placement and allocate its replacement in the same pass.
        """
        serial: int = self._next_serial
        self._next_serial += 1
        return serial
