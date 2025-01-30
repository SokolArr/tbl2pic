class TableSettings:
    def __init__(self,
                 cell_width=200,
                 cell_height=50,
                 header_color = (255, 255, 255, 255),
                 cell_color = (255, 255, 255, 255),
                 font_size=20,
                 font_path="example/font/shrift.ttf",
                 background_image='example/img/bg.jpg',
                 background_color=(255, 255, 255, 255),
                 border_color=(0, 0, 0, 255),
                 border_thickness=2):
        
        self.header_color = header_color
        self.header_cell_padding = (10, 10, 10, 10)
        self.header_cell_text_align = 'center'
        
        self.cell_width = cell_width
        self.cell_height = cell_height
        
        self.cell_color = cell_color
        self.cell_padding = (10, 10, 10, 10)
        self.cell_text_align = 'center'
        
    
        self.font_size = font_size
        self.font_path = font_path
        
        self.background_image = background_image
        self.background_color = background_color
        self.border_color = border_color
        self.border_thickness = border_thickness

