from fasthtml.components import ft_hx, AltGlyph, AltGlyphDef, AltGlyphItem, Animate, AnimateColor, AnimateMotion, AnimateTransform, Circle, ClipPath, Color_profile, Cursor, Defs, Desc, Ellipse, FeBlend, FeColorMatrix, FeComponentTransfer, FeComposite, FeConvolveMatrix, FeDiffuseLighting, FeDisplacementMap, FeDistantLight, FeFlood, FeFuncA, FeFuncB, FeFuncG, FeFuncR, FeGaussianBlur, FeImage, FeMerge, FeMergeNode, FeMorphology, FeOffset, FePointLight, FeSpecularLighting, FeSpotLight, FeTile, FeTurbulence, Filter, Font, Font_face, Font_face_format, Font_face_name, Font_face_src, Font_face_uri, ForeignObject, G, Glyph, GlyphRef, Hkern, Image, Line, LinearGradient, Marker, Mask, Metadata, Missing_glyph, Mpath, Pattern, Polygon, Polyline, RadialGradient, Rect, Set, Stop, Switch, Symbol, Text, TextPath, Tref, Tspan, Use, View, Vkern

def Svg(*args, viewBox=None, h=None, w=None, height=None, width=None, **kwargs):
    "An SVG tag; xmlns is added automatically, and viewBox defaults to height and width if not provided"
    if h: height=h
    if w: width=w
    if not viewBox and height and width: viewBox=f'0 0 {width} {height}'
    return ft_hx('svg', *args, xmlns="http://www.w3.org/2000/svg", viewBox=viewBox, height=height, width=width, **kwargs)

def Path(*args, **kwargs): return ft_hx('path', *args, **kwargs)

