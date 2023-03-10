from PyQt6.QtWidgets import QApplication, QWidget, \
    QDialog, QLabel, QMessageBox, QComboBox, QListWidget, QAbstractItemView
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QFont
import sys
from PIL import Image


def exit_application() -> None:
    sys.exit(0)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.filtersLayout = None
        self.roomLabel = None
        self.roomComboBox = None
        self.emailInput = None
        self.emailLabel = None
        self.roomsLabel = None
        self.roomsComboBox = None
        self.minAreaInput = None
        self.minAreaLabel = None
        self.selected_city = None
        self.districts = None
        self.district_list = None
        self.allOffersRbtn = None
        self.newOffersRbtn = None
        self.roomRbtn = None
        self.searchLabel = None
        self.minPriceLabel = None
        self.maxPriceLabel = None
        self.kindLayout = None
        self.priceLayout = None
        self.descriptionLabel = None
        self.textDistrictsLabel = None
        self.mapBtn = None
        self.exitBtn = None
        self.searchBtn = None
        self.apartmentRbtn = None
        self.minPriceInput = None
        self.maxPriceInput = None
        self.districtsList = None
        self.selected_districts = None
        self.image_map = None
        uic.loadUi("mainWindow.ui", self)
        self.mapBtn.clicked.connect(self.open_map_image)
        self.exitBtn.clicked.connect(exit_application)
        self.searchBtn.clicked.connect(self.search_apartments)

        self.minAreaLabel.hide()
        self.minAreaInput.hide()
        self.roomsComboBox.hide()
        self.roomsLabel.hide()
        self.emailLabel.hide()
        self.emailInput.hide()
        self.roomComboBox.hide()
        self.roomLabel.hide()

        self.apartmentRbtn.toggled.connect(self.flat_radio_btn_toggled)
        self.roomRbtn.toggled.connect(self.flat_radio_btn_toggled)
        self.allOffersRbtn.toggled.connect(self.type_radio_btn_toggled)
        self.newOffersRbtn.toggled.connect(self.type_radio_btn_toggled)

        self.city_combo_box = QComboBox(self)
        self.city_combo_box.setFixedHeight(30)
        self.city_combo_box.setFixedWidth(110)
        font = self.city_combo_box.font()
        font.setPointSize(11)
        self.city_combo_box.setFont(font)
        self.city_combo_box.insertItem(0, "SELECT CITY")
        self.city_combo_box.setCurrentIndex(0)
        self.city_combo_box.addItem("Warszawa")
        self.city_combo_box.addItem("Krak??w")
        self.city_combo_box.addItem("Wroc??aw")
        self.city_combo_box.addItem("Pozna??")
        self.city_combo_box.addItem("????d??")
        self.city_combo_box.addItem("Gda??sk")
        self.city_combo_box.addItem("Bia??ystok")
        self.city_combo_box.addItem("Sopot")
        self.city_combo_box.addItem("Katowice")
        self.city_combo_box.addItem("Gdynia")
        self.city_combo_box.addItem("Gliwice")
        self.city_combo_box.move(10, 10)

        self.district_list = QListWidget(self)
        self.district_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.district_list.move(10, 40)
        self.district_list.setVisible(False)
        self.city_combo_box.activated.connect(self.update_district_list)
        self.city_combo_box.currentIndexChanged.connect(self.handle_selection_change)

    def handle_selection_change(self, index):
        if self.city_combo_box.itemText(index) == "SELECT CITY":
            self.city_combo_box.setCurrentIndex(0)
            for i in range(1, self.city_combo_box.count()):
                if self.city_combo_box.itemText(i) != "SELECT CITY":
                    self.city_combo_box.setCurrentIndex(i)
                    break

    def flat_radio_btn_toggled(self):
        if self.apartmentRbtn.isChecked():
            self.minAreaLabel.show()
            self.minAreaInput.show()
            self.roomsComboBox.show()
            self.roomsLabel.show()
            self.roomComboBox.hide()
            self.roomLabel.hide()
        else:
            self.minAreaLabel.hide()
            self.minAreaInput.hide()
            self.roomsComboBox.hide()
            self.roomsLabel.hide()
            self.roomComboBox.show()
            self.roomLabel.show()

    def type_radio_btn_toggled(self):
        if self.newOffersRbtn.isChecked():
            self.emailInput.show()
            self.emailLabel.show()
        else:
            self.emailInput.hide()
            self.emailLabel.hide()

    def update_district_list(self, index):
        self.district_list.setVisible(True)
        city = self.city_combo_box.currentText()
        self.district_list.clear()
        font = self.district_list.font()
        font.setPointSize(12)
        self.district_list.setFont(font)
        self.district_list.setFixedHeight(460)
        self.district_list.setFixedWidth(200)
        if city == "Warszawa":
            self.selected_city = "warszawa"
            self.districts = ["All", "Bemowo", "Bia??o????ka", "Bielany", "Mokot??w", "Ochota", "Praga-Po??udnie",
                              "Praga-P????noc", "Rembert??w", "??r??dmie??cie", "Targ??wek", "Ursus", "Ursyn??w",
                              "Wawer", "Weso??a", "Wilan??w", "W??ochy", "Wola", "??oliborz"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Krak??w":
            self.selected_city = "krakow"
            self.districts = ["All", "Bie??czyce", "Bie??an??w-Prokocim", "Bronowice", "Czy??yny",
                              "D??bniki", "Grzeg??rzki", "Krowodrza", "??agiewniki-Borek Fa????cki",
                              "Mistrzejowice", "Nowa Huta", "Podg??rze", "Podg??rze Duchackie",
                              "Pr??dnik Bia??y", "Pr??dnik Czerwony", "Stare Miasto", "Swoszowice",
                              "Wzg??rza Krzes??awickie", "Zwierzyniec"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Wroc??aw":
            self.selected_city = "wroclaw"
            self.districts = ["All", "Fabryczna", "Psie Pole", "Stare Miasto", "??r??dmie??cie"]
            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Gda??sk":
            self.selected_city = "gdansk"
            self.districts = ["All", "Anio??ki", "Br??towo", "Brze??no", "Che??m z dzielnic?? Gda??sk Po??udnie", "Jasie??",
                              "Kokoszki", "Krakowiec - G??rki Zachodnie", "Letnica", "Matarnia", "M??yniska", "Nowy Port",
                              "Oliwa", "Olszynka", "Orunia - ??w. Wojciech - Lipce", "Osowa", "Piecki-Migowo",
                              "Przymorze Wielkie", "Rudniki", "Siedlce", "Stogi z Przer??bk??", "Strzy??a", "Suchanino",
                              "??r??dmie??cie", "Uje??cisko - ??ostowice", "VII Dw??r", "Wrzeszcz", "Wyspa Sobieszewska",
                              "Wzg??rze Mickiewicza", "Zaspa M??yniec", "Zaspa Roztaje",
                              "??abianka - Wejhera - Jelitkowo - Tysi??clecia"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "????d??":
            self.selected_city = "lodz"
            self.districts = ["All", "Ba??uty", "G??rna", "Polesie", "??r??dmie??cie", "Widzew"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Pozna??":
            self.selected_city = "poznan"
            self.districts = ["All", "Chartowo", "D??biec", "G??rczyn", "Grunwald", "Je??yce", "Junikowo", "Komandoria",
                              "??acina", "??awica", "??azarz", "Naramowice", "Ogrody", "Pi??tkowo", "Podolany", "Rataje",
                              "Smochowice", "So??acz", "Stare Miasto", "Staro????ka", "Strzeszyn", "Szczepankowo", "??r??dka",
                              "Warszawskie", "Wilda", "Winiary", "Winogrady"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Gdynia":
            self.selected_city = "gdynia"
            self.districts = ["All", "Babie Do??y", "Chwarzno-Wiczlino", "Chylonia", "Cisowa", "D??browa", "Dzia??ki Le??ne",
                              "Grab??wek", "Kamienna G??ra", "Karwiny", "Leszczynki", "Ma??y Kack", "Ob??u??e", "Oksywie",
                              "Or??owo", "Podg??rze", "Pustki Cisowskie-Demptowo", "Red??owo", "??r??dmie??cie", "Wielki Kack",
                              "Witomino-Le??nicz??wka", "Witomino-Radiostacja", "Wzg??rze ??wi??tego Maksymiliana"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Sopot":
            self.selected_city = "sopot"
            self.districts = ["All", "Centrum", "Dolny Sopot", "G??rny Sopot"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Bia??ystok":
            self.selected_city = "bialystok"
            self.districts = ["All", "Antoniuk", "Bacieczki", "Bema", "Bia??ostoczek", "Bojary", "Centrum", "Dojlidy",
                              "Dojlidy G??rne", "Dziesi??ciny I", "Dziesi??ciny II", "Jarosz??wka", "Kawaleryjskie",
                              "Le??na Dolina", "Mickiewicza", "M??odych", "Nowe Miasto", "Piaski", "Piasta I", "Piasta II",
                              "Przydworcowe", "Sienkiewicza", "Skorupy", "S??oneczny Stok", "Starosielce", "Wygoda",
                              "Wysoki Stoczek", "Zawady", "Zielone Wzg??rza"]
            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Gliwice":
            self.selected_city = "gliwice"
            self.districts = ["All", "Bojk??w", "Brzezinka", "Czechowice", "Kopernika", "Ligota Zabrska", "??ab??dy",
                              "Obro??c??w Pokoju", "Ostropa", "Politechnika", "Sikornik", "So??nica", "Stare Gliwice",
                              "Szobiszowice", "??r??dmie??cie", "Trynek", "Wilcze Gard??o", "Wojska Polskiego",
                              "W??jtowa Wie??", "Zatorze", "??erniki"]

            for district in self.districts:
                self.district_list.addItem(district)
        elif city == "Katowice":
            self.selected_city = "katowice"
            self.districts = ["All", "Bogucice", "Bryn??w-cz. Wsch.-Osiedle Zgrzebioka", "D??b", "D??br??wka Ma??a", "Giszowiec",
                              "Jan??w-Nikiszowiec", "Kostuchna", "Koszutka", "Ligota-Panewniki", "Murcki",
                              "Osiedle Paderewskiego-Muchowiec", "Osiedle Tysi??clecia", "Osiedle Witosa",
                              "Piotrowice-Ochojec", "Podlesie", "Szopienice-Burowiec", "??r??dmie??cie", "We??nowiec-J??zefowiec",
                              "Za????ska Ha??da-Bryn??w cz. Zach.", "Za??????e", "Zarzecze", "Zawodzie"]

            for district in self.districts:
                self.district_list.addItem(district)

    def open_map_image(self) -> None:
        if self.selected_city is not None:
            path = "../images/"+self.selected_city + ".png"
            img = Image.open(path)
            width, height = img.size
            self.image_map = QDialog(self)
            self.image_map.setFixedSize(width, height)
            self.image_map.setWindowTitle("Map of districts")
            label = QLabel(self.image_map)
            pixmap = QPixmap(path)
            label.setPixmap(pixmap)
            self.image_map.exec()
        else:
            QMessageBox.information(self, "Info", "You have not selected any city")

    def search_apartments(self) -> None:
        self.selected_districts = [item.text() for item in self.district_list.selectedItems()]

        if len(self.selected_districts) == 0:
            QMessageBox.information(self, "Error", "You have not selected any district")

        if "All" in self.districts:
            self.districts.remove("All")

        for district in self.selected_districts:
            if district == "All":
                self.selected_districts = self.districts

        try:
            min_price = int(self.minPriceInput.text())
        except ValueError:
            min_price = None
            QMessageBox.information(self, "Error", "You entered the wrong minimum price.\nIt must be a integer")

        try:
            max_price = int(self.maxPriceInput.text())
        except ValueError:
            max_price = None
            QMessageBox.information(self, "Error", "You entered the wrong maximum price.\nIt must be a integer")

        link = ""
        if self.apartmentRbtn.isChecked():
            link += "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/"+self.selected_city+"/"
        elif self.roomRbtn.isChecked():
            link += "https://www.olx.pl/d/nieruchomosci/stancje-pokoje/"+self.selected_city+"/"
        else:
            QMessageBox.information(self, "Error", "You have not chosen whether you want to\n"
                                                   "look for a room or an apartment")
        area = 0
        if self.apartmentRbtn.isChecked():
            try:
                area = int(self.minAreaInput.text())
            except ValueError:
                area = None
                QMessageBox.information(self, "Error", "You entered the wrong min area.\nIt must be a integer")

        email = ''
        if self.newOffersRbtn.isChecked():
            if len(self.emailInput.text()) > 0:
                email = self.emailInput.text()
            else:
                email = None
                QMessageBox.information(self, "Error", "You not entered the email.")

        if len(self.selected_districts) > 0 and isinstance(min_price, int) and \
                isinstance(min_price, int) and len(link) > 0 and isinstance(area, int) \
                and (isinstance(email, str)):
            if self.allOffersRbtn.isChecked() and self.apartmentRbtn.isChecked():
                window.close()
                from allApartmentScraping import run_all_apartments
                run_all_apartments(max_price, min_price, link, self.selected_districts, int(self.minAreaInput.text()), self.roomsComboBox.currentText())
            elif self.allOffersRbtn.isChecked() and self.roomRbtn.isChecked():
                window.close()
                from allRoomsScraping import run_all_rooms
                run_all_rooms(max_price, min_price, link, self.selected_districts, self.roomComboBox.currentText())
            elif self.newOffersRbtn.isChecked() and self.apartmentRbtn.isChecked():
                window.close()
                from newApartmentScraping import new_apartments_scraping
                new_apartments_scraping(max_price, min_price, link, self.selected_districts, int(self.minAreaInput.text()), self.roomsComboBox.currentText(), self.emailInput.text())
            elif self.newOffersRbtn.isChecked() and self.roomRbtn.isChecked():
                window.close()
                from newRoomScraping import new_room_scraping
                new_room_scraping(max_price, min_price, link, self.selected_districts, self.roomComboBox.currentText(), self.emailInput.text())
            else:
                QMessageBox.information(self, "Error", "You have not chosen whether you want to\n"
                                                       "look for new or all ad")


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
