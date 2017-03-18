from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class ImgCreator():

    def __init__(self):
        self.x_width = 2840 #dinA4 @300dpi
        self.y_height= 3508 #dinA4 @300dpi

        self.x_margins = 40 #custom margin
        self.y_margins = 20

        self.x_after_margins = self.x_width -(5*self.x_margins) # x+1 margins
        self.y_after_margins = self.y_height - (4 * self.y_margins)

        self.box_width = self.x_after_margins / 4 # remainder / x
        self.box_height = self.y_after_margins / 2
        self.small_box_height = self.box_height / 2

        self.img = Image.new("RGB", (self.x_width, self.y_height), "white")
        self.drawer = ImageDraw.Draw(self.img)

        self._coords = []

    def put_rectangle(self, box_height, y_margin, col):
        self._coords.append([])
        for idx, x in enumerate(range(self.x_margins,
                self.x_after_margins, self.box_width + self.x_margins)):
            # (x,y) start, (x,y) end
            self._coords[col].append([])
            self.put_coords(len(self._coords) - 1, idx, (x, y_margin),
                (x + self.box_width, y_margin + box_height))
            self.drawer.rectangle(((x, y_margin),
                                  (x + self.box_width, y_margin + box_height)),
                                  outline="black")
            self.fill_border(x, y_margin, self.box_width, box_height, 4)

    def fill_border(self, prev_x, prev_y, box_width, box_height, px_size):
        if px_size > 0:
            self.drawer.rectangle(((prev_x + 1, prev_y + 1),
                                  (prev_x + box_width - 2, prev_y + box_height - 2)),
                                  outline="black")
            self.fill_border(prev_x + 1, prev_y + 1, box_width -2,
                             box_height - 2, px_size - 1)


    def put_all_boxes(self):
        self._coords = []
        self.put_rectangle(self.box_height, self.y_margins, 0)
        self.put_rectangle(self.small_box_height,
                self.box_height + 2*self.y_margins ,1 )
        self.put_rectangle(self.small_box_height,
                self.box_height + self.small_box_height + 3*self.y_margins , 2)


    def put_coords(self, row, col, coordx, coordy):
        self._coords[row][col] = (coordx, coordy)


    def save_img(self, path):
        self.img.save(path)

    def put_all_text(self, textlist):
        for row_idx, row in enumerate(textlist):
            if row_idx == 2:
                for field in range(4):
                    font = ImageFont.truetype("../res/Roboto-Black.ttf", 52)
                    self.drawer.text((self._coords[row_idx][field][0][0]+8,
                        self._coords[row_idx][field][0][1]), 'NOTES:',
                        (0,0,0), font=font)
            else: 
                for col_idx, text in enumerate(row):
                        self.put_text(row_idx, col_idx, text)

    def put_text(self, row, col, text):
        font = ImageFont.truetype("../res/Roboto-Black.ttf", 52)
        coords_begin = self._coords[row][col][0]
        coords_end = self._coords[row][col][1]
        box_width = coords_end[0] - coords_begin[0]
        box_height = coords_end[1] - coords_begin[1]
        textsize = self.drawer.textsize(str(text[0]), font)
        #assert textsize <= box_width
        text_w, text_h = textsize
        cth = coords_begin[1]
        self.drawer.text((coords_begin[0]+3, cth),
            str(text[0]), (0, 0, 0), font=font)
        cth += text_h + 5

        if row == 0:
            for time, line in text[1]:
                if time == '':
                    self.drawer.text((coords_begin[0]+8, cth),
                        str(line), (0, 0, 0), font=font)
                    cth += text_h

            for time, line in text[1]:
                if time != '':
                    line = str(line)
                    self.drawer.text((coords_begin[0]+8, cth),
                        time, (0, 0, 0), font=font)
                    cth += text_h + 5
                    self.drawer.text((coords_begin[0]+8, cth),
                            line, (0, 0, 0), font=font)
                    cth += text_h + 5
        elif row == 1:
            for line in text[1]:
                line = str(line)
                self.drawer.text((coords_begin[0]+8, cth),
                        line, (0, 0, 0), font=font)
                cth += text_h + 5

