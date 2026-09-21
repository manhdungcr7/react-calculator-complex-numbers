import fitz
import os

pages = [10,11,24,25,31,40,44,72,73,80,84,96,97,100,108,109,110,113,114,116,
         121,123,127,130,132,137,138,141,142,144,148,153,160,168,169,171,176,
         177,184,190,193,195,208,209,210,211,214,215,217,220,222,225,229,232,
         237,239,244,245]

doc = fitz.open('DAP AN.pdf')
os.makedirs('scratch/pages', exist_ok=True)
for p in pages:
    page = doc[p-1]
    pix = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2))
    pix.save(f'scratch/pages/page_{p:03d}.png')
print('rendered', len(pages), 'pages')
