from pathlib import Path
p=Path('index.html')
s=p.read_text()
a=s.index(" const pairs=[['Red','#b72f35']", s.index('performanceTeeModal'))
b=s.index(" const modal=document.getElementById('performanceTeeModal')", a)
replacement=""" const pairs=[['Sport Grey','#9fa4aa'],['Black','#1a1c1b'],['Light Grey','#c4c6c7'],['Prairie Dust','#7a6f59'],['Military Green','#515e4a'],['Sage','#8c9988'],['Charcoal','#4d524e'],['Brown','#8a795c'],['Olive Green','#66704f'],['Light Sage','#a8b7a4'],['White','#eff0f4'],['Dark Grey','#55585d'],['Red','#af182b']];
 const files=['IMG_0385.jpeg','IMG_0386.jpeg','IMG_0387.jpeg','IMG_0388.jpeg','IMG_0389.jpeg','IMG_0390.jpeg','IMG_0391.jpeg','IMG_0392.jpeg','IMG_0393.jpeg','IMG_0394.jpeg','IMG_0395.jpeg','IMG_0396.jpeg','IMG_0397.jpeg','IMG_0398.jpeg','IMG_0399.jpeg','IMG_0400.jpeg','IMG_0401.jpeg','IMG_0402.jpeg','IMG_0403.jpeg','IMG_0404.jpeg','IMG_0405.jpeg','IMG_0406.jpeg','IMG_0408.jpeg','IMG_0409.jpeg','IMG_0410.jpeg','IMG_0411.jpeg'];
"""
s=s[:a]+replacement+s[b:]
s=s.replace('Gangster Bougie Self Made Still Bougie Performance T-Shirt Red front','Gangster Bougie Self Made Still Bougie Performance T-Shirt Sport Grey front',1)
s=s.replace('<strong id="performanceTeeColour">Red</strong>','<strong id="performanceTeeColour">Sport Grey</strong>',1)
s=s.replace('14 colourways • US$46.99','13 colourways • US$46.99',1)
p.write_text(s)
