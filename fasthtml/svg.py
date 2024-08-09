from fasthtml.components import ft_hx, Svg, AltGlyph, AltGlyphDef, AltGlyphItem, Animate, AnimateColor, AnimateMotion, AnimateTransform, Circle, ClipPath, Color_profile, Cursor, Defs, Desc, Ellipse, FeBlend, FeColorMatrix, FeComponentTransfer, FeComposite, FeConvolveMatrix, FeDiffuseLighting, FeDisplacementMap, FeDistantLight, FeFlood, FeFuncA, FeFuncB, FeFuncG, FeFuncR, FeGaussianBlur, FeImage, FeMerge, FeMergeNode, FeMorphology, FeOffset, FePointLight, FeSpecularLighting, FeSpotLight, FeTile, FeTurbulence, Filter, Font, Font_face, Font_face_format, Font_face_name, Font_face_src, Font_face_uri, ForeignObject, G, Glyph, GlyphRef, Hkern, Image, Line, LinearGradient, Marker, Mask, Metadata, Missing_glyph, Mpath, Pattern, Polygon, Polyline, RadialGradient, Rect, Set, Stop, Switch, Symbol, Text, TextPath, Tref, Tspan, Use, View, Vkern
from fastcore.xml import FT

def Path(*args, **kwargs)->FT: return ft_hx('path', *args, **kwargs)

