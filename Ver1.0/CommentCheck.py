import os
import glob
import matplotlib.pyplot as matplot
import japanize_matplotlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait

file_count = 0
total_count = 0
comment_count = 0

use_files = []
png_name = "circle.png"
pdf_name = "circle.pdf"

#下の階層用
for files in glob.glob("*/**/*"):
    name, extension = os.path.splitext(files)
    if extension == ".py":
        use_files.append(name + extension)
        file_count += 1
        pyfile = open(files)
        lines = pyfile.readlines()
        pyfile.close()
        replace_line = [linedata.replace(' ','') for linedata in lines]
        replace_and_strip_line = [replacedata.replace('\n','') for replacedata in replace_line]

        #コメント判定
        for pyline in replace_and_strip_line:
            total_count += len(pyline)
            if pyline.startswith("#", 0):
                comment_count += len(pyline)

#同じ階層用
for files in glob.glob("*"):
    name, extension = os.path.splitext(files)
    if extension == ".py":
        use_files.append(name + extension)
        file_count += 1
        pyfile = open(files)
        lines = pyfile.readlines()
        pyfile.close()
        replace_line = [linedata.replace(' ','') for linedata in lines]
        replace_and_strip_line = [replacedata.replace('\n','') for replacedata in replace_line]

        for pyline in replace_and_strip_line:
            total_count += len(pyline)
            if pyline.startswith("#", 0):
                comment_count += len(pyline)

#円グラフ描画
not_comment_count = total_count - comment_count
circledata = [not_comment_count, comment_count]
labels = ["プログラム文", "コメント"]

a, ax = matplot.subplots()
ax.pie(circledata, labels = labels, startangle = 90, autopct="%1.1f%%")
matplot.title("コメント比率", fontsize = 24)

matplot.savefig(png_name)

#PDF作成
pdf = canvas.Canvas(pdf_name, pagesize=portrait(A4))
pdf.drawImage(png_name, 0, 500, 450, 300)

pdf.drawCentredString(107, 500, "Total:    " + "{:10}".format(str(total_count)))
pdf.drawCentredString(110, 480, "Comment: " + "{:10}".format(str(comment_count)))
pdf.drawCentredString(113, 460, "Files:          " + "{:10}".format(str(file_count)))
pdf.drawCentredString(107, 400, "FileName_and_Path")
x, y = 215, 375
for file_name in use_files:
    pdf.drawCentredString(x, y, file_name)
    y -= 15
pdf.save()

#画像ファイル削除(circle.png)
os.remove("circle.png")