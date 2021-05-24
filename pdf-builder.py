#!/usr/bin/env python3

import os
from fpdf import FPDF
from subprocess import Popen, PIPE
from PIL import Image

title = 'ISSessions CTF 2021 - Documentation Booklet'

class PDF(FPDF):
    def header(self):
        pdf.set_title(title)
        pdf.set_author('ISSessions')
        img = Image.new('RGB', (215,300), "#0D0D0D" )
        img.save('background.png')
        pdf.image('background.png', x = 0, y = 0, w = 215, h = 300, type = '', link = '')

        pdf.set_text_color(148, 152, 166)
        pdf.set_draw_color(42, 45, 64)
        pdf.set_line_width(1.5)

        self.set_font('Arial', 'B', 18)
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        self.cell(w, 9, title, 1, 1, 'C', )
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def challenge_title(self, category_name, challenge_name):
        self.set_text_color(13, 13, 13)
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(88, 95, 115)
        self.cell(0, 8, category_name + ': ' + challenge_name, 0, 1, 'L', 1)
        self.ln(5)

    def challenge_body(self, name):
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        self.set_font('Arial', 'BU', 14)
        self.cell(0, 6, name.split('/').pop().replace('.txt', '').capitalize() + ':')
        self.ln(7)
        self.set_font('Arial', '', 12)
        pdf.set_text_color(148, 152, 166)
        self.multi_cell(0, 5, txt)
        self.ln(4)
    
    def challenge_details(self, author_name, flag):
        pdf.set_text_color(242, 5, 5)
        self.set_font('Arial', 'B', 12)
        self.cell(17,0,'Author: ')
        self.set_font('Arial', '', 12)
        pdf.set_text_color(148, 152, 166)
        self.cell(50, 0, author_name)
        self.set_font('Arial', 'B', 12)
        pdf.set_text_color(242, 5, 5)
        self.multi_cell(13, 0, 'Flag:')
        self.set_font('Arial', '', 12)
        pdf.set_text_color(148, 152, 166)
        self.multi_cell(40, 0, flag)
        self.ln(4)

    def write_challenge(self, category_name, challenge_name, file_names):
        grep = Popen(['grep', 'author', root.replace('documentation', 'challenge.yml')], stdout=PIPE)
        author_name = str(grep.communicate()[0]).split(": ")[1][:-3]
        grep = Popen(['grep', '    - FLAG{', root.replace('documentation', 'challenge.yml',)], stdout=PIPE)
        flag = str(grep.communicate()[0])[8:-3]
        self.add_page(format='A4')
        self.challenge_title(category_name, challenge_name)
        self.challenge_details(author_name, flag)
        if len(files) == 3:
            pdf.set_text_color(242, 220, 107)
            self.challenge_body(root + '/' + file_names[0])
            pdf.set_text_color(5, 242, 108)
            self.challenge_body(root + '/' + file_names[2])
            pdf.set_text_color(39, 127, 242)
            self.challenge_body(root + '/' + file_names[1])
        elif len(files) == 1:
            pdf.set_text_color(242, 220, 107)
            self.challenge_body(root + '/' + file_names[0])
        
pdf = PDF(format='A4')
pdf.set_margins(left=20, right=20, top=15)

for (root, dirs, files) in os.walk('.'):
    if not root.startswith('./.') and root != '.':
        category = root.replace('./', '')
        if category.endswith('/documentation'):
            challenge_name = category.split('/')[1]
            category_name = category.split('/')[0]
            pdf.write_challenge(category_name, challenge_name, files)
            print(category_name + ': ' + challenge_name)

pdf.output('ISSessionsCTF2021_Hosted_Documentation_Booklet.pdf','F')