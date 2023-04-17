style_default = """
    QWidget {
        background-color: #181818;
        color: #ffffff;
        font-weight: bold;
    }
    
    QPushButton {
        background-color: #212121;
        border: 2px solid #aaaaaa;
        border-radius: 10%;
        color: #ffffff;
        font-size: 15px;
    }
    
    QPushButton::hover {
        background-color: #3d3d3d;
        border: 3px solid #ffffff;
        border-radius: 10%;
        color: #ffffff;
        font-size: 17px;
    }
    
    QLabel {
        font-size: 15px;
    }
    
    QLabel#stats {
        font-size: 30px;
    }
    
    QCheckBox {
        font-size: 15px;
    }
    
    QComboBox {
        border: 1px solid #ffffff;
        border-radius: 2%;
        font-size: 15px;
        padding-left: 20px;
        color: #ffffff;
    }
    
    QComboBox::hover {
        font-size: 17px;
    }
    
    QComboBox::drop-down {
        border: 0px;
    }
    
    QComboBox::on {
        border: 4px #aaaaaa;
    }
    
    QComboBox QListView {
        border: 3px solid rgba(170, 170, 170, 105);
        border-radius: 5px;
        padding: 5px; 
        outline: 0px;
    }
    
    QComboBox QListView::item {
        padding-left: 10px;
        border: 5px solid red;
        background-color: #3d3d3d;
    }
    
    QComboBox QListView::item::hover {
        background-color: #aaaaaa;
        color: #000000;
    } 
"""

style_light = """
    QWidget {
        background-color: #add8e6;
        color: #000000;
        font-weight: bold;
    }

    QPushButton {
        background-color: #40b5aD;
        border: 2px solid #000000;
        border-radius: 10%;
        color: #000000;
        font-size: 15px;
    }

    QPushButton::hover {
        background-color: #40e0d0;
        border: 3px solid #000000;
        border-radius: 10%;
        color: #000000;
        font-size: 17px;
    }

    QLabel {
        font-size: 15px;
    }
    
    QLabel#stats {
        font-size: 30px;
    }
        
    QCheckBox {
        font-size: 15px;
    }
    
    QComboBox {
        border: 1px solid #000000;
        border-radius: 2%;
        font-size: 15px;
        padding-left: 20px;
        color: #000000;
    }

    QComboBox::hover {
        font-size: 17px;
    }

    QComboBox::drop-down {
        border: 0px;
    }

    QComboBox::on {
        border: 4px #aaaaaa;
    }

    QComboBox QListView {
        border: 3px solid rgba(170, 170, 170, 105);
        border-radius: 5px;
        padding: 5px; 
        outline: 0px;
    }

    QComboBox QListView::item {
        padding-left: 10px;
        border: 5px solid red;
        background-color: #3d3d3d;
    }

    QComboBox QListView::item::hover {
        background-color: #aaaaaa;
        color: #000000;
    }
"""